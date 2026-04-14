/**
 * Validate a Power BI PBIR .Report folder against Microsoft's published JSON schemas.
 *
 * All schemas (including transitive dollar-ref dependencies like semanticQuery) are fetched
 * and cached in .schema-cache/ then pre-loaded into AJV before any compilation.
 * This means compilation is synchronous and reliable — no async ref-loading surprises.
 *
 * Usage:   node validate_report.js <path-to-.Report-folder>
 * Exit 0 = passed. Non-zero = errors.
 */

"use strict";

const fs   = require("fs");
const path = require("path");

const Ajv        = (() => { const m = require("ajv");         return m.default ?? m; })();
const addFormats = (() => { const m = require("ajv-formats"); return m.default ?? m; })();

const CACHE_DIR = path.join(__dirname, ".schema-cache");

// -- Schema cache + fetch --------------------------------------------------

async function fetchSchema(url) {
  const cacheFile = path.join(CACHE_DIR, url.replace(/[^a-zA-Z0-9.]/g, "_") + ".json");
  if (fs.existsSync(cacheFile)) {
    try { return JSON.parse(fs.readFileSync(cacheFile, "utf8")); } catch { }
  }
  try {
    const res = await fetch(url, { signal: AbortSignal.timeout(12_000) });
    if (!res.ok) throw new Error("HTTP " + res.status);
    const schema = await res.json();
    fs.mkdirSync(CACHE_DIR, { recursive: true });
    fs.writeFileSync(cacheFile, JSON.stringify(schema, null, 2));
    return schema;
  } catch (err) {
    process.stderr.write("  [WARN] Cannot fetch " + url + ": " + err.message + "\n");
    return null;
  }
}

// Extract all external $ref base-URIs from a schema object (recursive).
function extractExternalRefs(schema) {
  const refs = new Set();
  function walk(obj) {
    if (!obj || typeof obj !== "object") return;
    if (typeof obj["$ref"] === "string" && !obj["$ref"].startsWith("#")) {
      refs.add(obj["$ref"].split("#")[0]);
    }
    for (const v of Object.values(obj)) walk(v);
  }
  walk(schema);
  return refs;
}

// Resolve a (possibly relative) ref URI against a base URI.
function resolveUri(ref, base) {
  if (!ref) return null;
  try { return new URL(ref, base).href; } catch { return null; }
}

/**
 * Transitively fetch all schemas referenced by the starting set.
 * Returns a Map<url, schemaObject>.
 */
async function fetchAllSchemas(startUrls) {
  const loaded  = new Map();
  const pending = [...startUrls];

  while (pending.length > 0) {
    const url = pending.pop();
    if (loaded.has(url)) continue;
    loaded.set(url, null); // mark visited

    const schema = await fetchSchema(url);
    if (!schema) continue;
    loaded.set(url, schema);

    // Find its deps and queue them
    for (const ref of extractExternalRefs(schema)) {
      const resolved = resolveUri(ref, schema["$id"] || url);
      if (resolved && !loaded.has(resolved)) {
        pending.push(resolved);
      }
    }
  }

  return loaded;
}

// -- AJV builder (sync compile after all schemas are pre-loaded) ----------

function buildAjv(schemasMap) {
  const ajv = new Ajv({ allErrors: true, strict: false, validateFormats: false });
  addFormats(ajv);

  // Add all schemas in one pass
  for (const [url, schema] of schemasMap) {
    if (!schema) continue;
    try { ajv.addSchema(schema, url); } catch { /* already added or invalid — skip */ }
  }

  // Compile validators for each schema, skip ones that still fail
  const validators = new Map();
  for (const [url] of schemasMap) {
    const entry = ajv.getSchema(url);
    if (!entry) continue;
    try {
      validators.set(url, ajv.compile(entry.schema));
    } catch (err) {
      process.stderr.write("  [WARN] Cannot compile " + url.split("/").slice(-3).join("/") + ": " + err.message.slice(0, 80) + "\n");
    }
  }
  return validators;
}

// -- File utilities --------------------------------------------------------

function* walk(dir, filename) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) yield* walk(full, filename);
    else if (!filename || entry.name === filename) yield full;
  }
}

function readJson(fp) {
  try { return JSON.parse(fs.readFileSync(fp, "utf8")); }
  catch (e) { return { _error: e.message }; }
}

const rel = (f, root) => path.relative(root, f);
const isKebab = (s) => /^[a-z0-9]+(-[a-z0-9]+)*$/.test(s);

// -- Structural cross-reference checks ------------------------------------

const BUILTIN = new Set([
  "card","cardVisual","multiRowCard","slicer","advancedSlicerVisual","listSlicer","textSlicer",
  "clusteredBarChart","clusteredColumnChart","barChart","columnChart",
  "hundredPercentStackedBarChart","hundredPercentStackedColumnChart",
  "lineChart","areaChart","stackedAreaChart",
  "lineClusteredColumnComboChart","lineStackedColumnComboChart",
  "waterfallChart","treemap","pieChart","donutChart","pivotTable","tableEx","funnel",
  "scatterChart","map","filledMap","shapeMap","azureMap",
  "gauge","kpi","ribbonChart","decompositionTreeVisual","keyInfluencersVisual","qnaVisual",
  "shape","basicShape","textbox","actionButton","image",
  "pageNavigator","bookmarkNavigator","scriptVisual","pythonVisual",
]);

function crossRefChecks(root, parsedMap, errors, warnings) {
  const def      = path.join(root, "definition");
  const pagesDir = path.join(def, "pages");

  const pagesJsonPath = path.join(def, "pages.json");
  if (fs.existsSync(pagesJsonPath) && fs.existsSync(pagesDir)) {
    const pd = parsedMap.get(pagesJsonPath);
    if (pd && !pd._error) {
      const ordered = new Set(pd.pageOrder || []);
      const actual  = new Set(fs.readdirSync(pagesDir).filter(n =>
        fs.statSync(path.join(pagesDir, n)).isDirectory()
      ));
      for (const p of ordered) if (!actual.has(p))  errors.push("ERROR  pages.json: '" + p + "' in pageOrder but folder missing");
      for (const p of actual)  if (!ordered.has(p)) warnings.push("WARN   pages.json: folder '" + p + "' not in pageOrder");
    }
  }

  if (fs.existsSync(pagesDir)) {
    for (const folder of fs.readdirSync(pagesDir)) {
      const pageDir = path.join(pagesDir, folder);
      if (!fs.statSync(pageDir).isDirectory()) continue;
      if (!isKebab(folder)) warnings.push("WARN   pages/" + folder + ": not kebab-case");

      const pjPath = path.join(pageDir, "page.json");
      if (!fs.existsSync(pjPath)) {
        errors.push("ERROR  pages/" + folder + ": missing page.json");
      } else {
        const pj = parsedMap.get(pjPath);
        if (pj && !pj._error && pj.name !== folder)
          errors.push("ERROR  " + rel(pjPath, root) + ": name='" + pj.name + "' but folder='" + folder + "'");
      }

      const visualsDir = path.join(pageDir, "visuals");
      if (fs.existsSync(visualsDir))
        for (const vf of fs.readdirSync(visualsDir)) {
          if (!isKebab(vf)) warnings.push("WARN   pages/" + folder + "/visuals/" + vf + ": not kebab-case");
          // Check visual folder has visual.json (orphaned scaffold detection)
          const vfPath = path.join(visualsDir, vf);
          if (fs.statSync(vfPath).isDirectory() && !fs.existsSync(path.join(vfPath, "visual.json")))
            errors.push("ERROR  pages/" + folder + "/visuals/" + vf + ": missing visual.json (orphaned scaffold)");
        }
    }
  }

  // Drillthrough / tooltip / displayOption page validation
  const VALID_DISPLAY = new Set(["FitToPage", "FitToWidth", "ActualSize"]);
  if (fs.existsSync(pagesDir)) {
    for (const folder of fs.readdirSync(pagesDir)) {
      const pageDir = path.join(pagesDir, folder);
      if (!fs.statSync(pageDir).isDirectory()) continue;
      const pjPath = path.join(pageDir, "page.json");
      if (!fs.existsSync(pjPath)) continue;
      const pj = parsedMap.get(pjPath);
      if (!pj || pj._error) continue;

      // displayOption validation
      if (pj.displayOption != null && !VALID_DISPLAY.has(pj.displayOption))
        errors.push("ERROR  pages/" + folder + "/page.json: invalid displayOption '" + pj.displayOption + "'");

      const pageType = pj.type || 0;
      if (pageType === 2) { // drillthrough
        if (!pj.filters && !pj.allFilters)
          warnings.push("WARN   pages/" + folder + "/page.json: drillthrough page (type=2) has no filters — users won't be able to drill through");
      }
      if (pageType === 1) { // tooltip
        const w = pj.width, h = pj.height;
        if (w && h && (w > 680 || h > 480))
          warnings.push("WARN   pages/" + folder + "/page.json: tooltip page (type=1) has large dimensions (" + w + "x" + h + ") — typically 320x240");
      }
    }
  }

  const rjPath = path.join(def, "report.json");
  if (fs.existsSync(rjPath)) {
    const rd = parsedMap.get(rjPath);
    if (rd && !rd._error) {
      const registered = new Set(rd.publicCustomVisuals || []);
      const usedCustom = new Set();
      if (fs.existsSync(pagesDir))
        for (const vjPath of walk(pagesDir, "visual.json")) {
          const vd = parsedMap.get(vjPath);
          if (!vd || vd._error) continue;
          const vt = vd.visual && vd.visual.visualType;
          if (vt && !BUILTIN.has(vt)) usedCustom.add(vt);
        }
      for (const cv of registered) if (!usedCustom.has(cv))  warnings.push("WARN   report.json: '" + cv + "' registered but not used");
      for (const vt of usedCustom)  if (!registered.has(vt)) errors.push("ERROR  report.json: '" + vt + "' used but not in publicCustomVisuals");
    }
  }
}

// -- Main -----------------------------------------------------------------

async function main() {
  let reportRoot = process.argv[2];
  if (!reportRoot) { console.error("Usage: node validate_report.js <path-to-.Report-folder>"); process.exit(1); }
  reportRoot = path.resolve(reportRoot);

  if (!reportRoot.endsWith(".Report") && fs.existsSync(reportRoot)) {
    const c = fs.readdirSync(reportRoot).filter(n => n.endsWith(".Report"));
    if      (c.length === 1) reportRoot = path.join(reportRoot, c[0]);
    else if (c.length > 1)  { console.error("Multiple .Report folders; specify one."); process.exit(1); }
    else                    { console.error("No .Report folder at " + reportRoot); process.exit(1); }
  }

  const definition = path.join(reportRoot, "definition");
  if (!fs.existsSync(definition)) { console.error("Missing definition/ folder"); process.exit(1); }

  // Collect + parse files
  const jsonFiles  = [...walk(definition)].filter(f => f.endsWith(".json"));
  const pbirFile   = path.join(reportRoot, "definition.pbir");
  if (fs.existsSync(pbirFile)) jsonFiles.push(pbirFile);

  const parsedMap  = new Map();
  const schemaUrls = new Set();
  for (const f of jsonFiles) {
    const data = readJson(f);
    parsedMap.set(f, data);
    if (!data._error && data["$schema"]) schemaUrls.add(data["$schema"]);
  }

  // Fetch all schemas + their transitive deps
  const schemaCount = schemaUrls.size;
  process.stdout.write("Fetching schemas (including transitive deps, cached after first run)... ");
  const schemasMap = await fetchAllSchemas(schemaUrls);
  const fetchedCount = [...schemasMap.values()].filter(Boolean).length;
  console.log("done. (" + fetchedCount + " schemas loaded, " + schemaCount + " direct)");

  // Build AJV with all pre-loaded schemas
  const validators = buildAjv(schemasMap);
  console.log("Compiled " + validators.size + " validators.\n");

  // Validate each file
  const errors   = [];
  const warnings = [];
  let validated  = 0, skipped = 0;

  for (const [f, data] of parsedMap) {
    if (data._error) {
      errors.push("ERROR  " + rel(f, reportRoot) + ": Invalid JSON — " + data._error);
      skipped++; continue;
    }
    const v = data["$schema"] && validators.get(data["$schema"]);
    if (!v) { skipped++; continue; }
    if (!v(data) && v.errors) {
      for (const e of v.errors) {
        const loc = e.instancePath || "(root)";
        errors.push("ERROR  " + rel(f, reportRoot) + ": " + loc + " — " + e.message);
      }
    }
    validated++;
  }

  crossRefChecks(reportRoot, parsedMap, errors, warnings);

  console.log("Checked " + validated + "/" + jsonFiles.length + " files against their schema (" + skipped + " skipped)\n");

  if (warnings.length) {
    console.log("-".repeat(60) + "\nWARNINGS (" + warnings.length + ")\n" + "-".repeat(60));
    warnings.forEach(w => console.log("  " + w));
    console.log();
  }
  if (errors.length) {
    console.log("-".repeat(60) + "\nERRORS (" + errors.length + ")\n" + "-".repeat(60));
    errors.forEach(e => console.log("  " + e));
    console.log("\n❌  Validation FAILED — " + errors.length + " error(s)");
    process.exit(1);
  } else {
    console.log("✅  Validation PASSED — no errors (" + warnings.length + " warning(s))");
  }
}

main().catch(err => { console.error("Unexpected error:", err); process.exit(2); });