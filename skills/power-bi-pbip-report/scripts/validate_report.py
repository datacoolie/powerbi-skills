"""
Validate a Power BI PBIR report folder against Microsoft's published JSON schemas.

Usage:
    python validate_report.py <path-to-.Report-folder>
    python validate_report.py <path-to-.Report-folder> --offline

Checks:
    1. JSON syntax — every .json and .pbir file must parse cleanly
    2. JSON Schema validation — validates each file against its $schema URL
       (fetches schemas + transitive $ref dependencies, caches in .schema-cache/)
    3. Required properties — fallback structural checks per file type
    4. Cross-references — page folders ↔ pages.json, bookmarks, custom visuals
    5. Naming conventions — kebab-case for page/visual folders

Options:
    --offline   Use only cached schemas (no network). Falls back to structural
                checks if schemas are not cached.

Exit code 0 = all checks pass. Non-zero = errors found.

Dependencies:
    - jsonschema + referencing (pip install jsonschema)  — for full schema validation
    - Without jsonschema, the script still runs all structural checks (with a warning).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import urljoin
from urllib.request import Request, urlopen
from urllib.error import URLError

# Ensure the scripts directory is on sys.path for sibling imports
_SCRIPTS_DIR = Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from pbir_utils import setup_logging  # noqa: E402

# --- Optional jsonschema import (graceful degradation) ---

try:
    import jsonschema
    from jsonschema import Draft202012Validator, ValidationError  # noqa: F401
    from referencing import Registry, Resource  # noqa: F401
    HAS_JSONSCHEMA = True
except ImportError:
    HAS_JSONSCHEMA = False

SCRIPTS_DIR = Path(__file__).resolve().parent
CACHE_DIR = SCRIPTS_DIR / ".schema-cache"


# --- Configuration ---

REQUIRED_PROPERTIES = {
    "report.json": ["themeCollection"],
    "page.json": ["name", "displayName", "displayOption"],
    "visual.json": ["name", "position"],
    "pages.json": [],  # only $schema required
    "version.json": ["version"],
    "definition.pbir": ["version", "datasetReference"],
    "bookmarks.json": [],
    "mobile.json": [],
    "reportExtensions.json": [],  # only $schema required; present when report-level measures exist
}

# Page types — Power BI encodes page purpose via the 'type' integer field.
PAGE_TYPE_REPORT = 0       # default report page
PAGE_TYPE_TOOLTIP = 1      # tooltip page
PAGE_TYPE_DRILLTHROUGH = 2 # drillthrough page

VISUAL_POSITION_PROPS = ["x", "y", "height", "width"]

VALID_DISPLAY_OPTIONS = {"FitToPage", "FitToWidth", "ActualSize"}


# --- Schema fetching & caching ---

def _cache_path(url: str) -> Path:
    """Return the local cache file for a schema URL (same convention as the old JS validator)."""
    safe = re.sub(r"[^a-zA-Z0-9.]", "_", url) + ".json"
    return CACHE_DIR / safe


def _fetch_schema(url: str, *, offline: bool = False) -> dict | None:
    """Fetch a JSON schema by URL, with on-disk cache.

    Only URLs matching the allowlist are fetched to prevent SSRF.
    """
    # SSRF hardening: only fetch from known Microsoft schema origins
    _ALLOWED_PREFIXES = (
        "https://developer.microsoft.com/json-schemas/",
        "https://raw.githubusercontent.com/microsoft/",
    )
    if not any(url.startswith(prefix) for prefix in _ALLOWED_PREFIXES):
        print(f"  [WARN] Blocked fetch of non-allowlisted URL: {url}", file=sys.stderr)
        return None

    cached = _cache_path(url)
    if cached.is_file():
        try:
            return json.loads(cached.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass  # corrupt cache — refetch

    if offline:
        return None

    try:
        req = Request(url, headers={"User-Agent": "validate_report.py/1.0"})
        with urlopen(req, timeout=12) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        cached.write_text(json.dumps(data, indent=2), encoding="utf-8")
        return data
    except (URLError, OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"  [WARN] Cannot fetch {url}: {exc}", file=sys.stderr)
        return None


def _extract_external_refs(schema: dict) -> set[str]:
    """Recursively extract all external $ref base-URIs from a schema object."""
    refs: set[str] = set()

    def walk(obj: object) -> None:
        if not isinstance(obj, dict):
            if isinstance(obj, list):
                for item in obj:
                    walk(item)
            return
        ref = obj.get("$ref")
        if isinstance(ref, str) and not ref.startswith("#"):
            refs.add(ref.split("#")[0])
        for v in obj.values():
            walk(v)

    walk(schema)
    return refs


def fetch_all_schemas(start_urls: set[str], *, offline: bool = False) -> dict[str, dict]:
    """Transitively fetch all schemas referenced by the starting set. Returns {url: schema}."""
    loaded: dict[str, dict] = {}
    pending = list(start_urls)
    visited: set[str] = set()

    while pending:
        url = pending.pop()
        if url in visited:
            continue
        visited.add(url)

        schema = _fetch_schema(url, offline=offline)
        if schema is None:
            continue
        loaded[url] = schema

        base = schema.get("$id", url)
        for ref in _extract_external_refs(schema):
            resolved = urljoin(base, ref)
            if resolved not in visited:
                pending.append(resolved)

    return loaded


def build_schema_validators(schemas: dict[str, dict]) -> dict[str, object] | None:
    """Compile jsonschema validators for each fetched schema. Returns {url: validator} or None."""
    if not HAS_JSONSCHEMA or not schemas:
        return None

    # Build a referencing.Registry with all fetched schemas
    registry = Registry()
    for url, schema in schemas.items():
        resource = Resource.from_contents(schema, default_specification=jsonschema.Draft202012Validator)
        registry = registry.with_resource(url, resource)
        # Also register by $id if present
        schema_id = schema.get("$id")
        if schema_id and schema_id != url:
            registry = registry.with_resource(schema_id, resource)

    validators: dict[str, object] = {}
    for url, schema in schemas.items():
        try:
            validators[url] = Draft202012Validator(schema, registry=registry)
        except Exception as exc:
            short = "/".join(url.split("/")[-3:])
            print(f"  [WARN] Cannot compile {short}: {str(exc)[:80]}", file=sys.stderr)
    return validators


# --- Helpers ---

class ValidationResult:
    def __init__(self):
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, file: str, msg: str):
        self.errors.append(f"ERROR  {file}: {msg}")

    def warn(self, file: str, msg: str):
        self.warnings.append(f"WARN   {file}: {msg}")

    @property
    def ok(self) -> bool:
        return len(self.errors) == 0


def rel(path: Path, root: Path) -> str:
    """Return a short relative path string for display."""
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def is_kebab_case(name: str) -> bool:
    """Check if a name follows lowercase-kebab-case convention."""
    return bool(re.match(r"^[a-z0-9]+(-[a-z0-9]+)*$", name))


# --- Validators ---

def validate_json_syntax(file_path: Path, root: Path, result: ValidationResult) -> dict | None:
    """Parse a JSON file and return the data, or None on failure."""
    try:
        text = file_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        try:
            text = file_path.read_text(encoding="utf-8-sig")
        except Exception as e:
            result.error(rel(file_path, root), f"Cannot read file: {e}")
            return None

    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        result.error(rel(file_path, root), f"Invalid JSON: {e}")
        return None


def validate_schema_property(data: dict, file_path: Path, root: Path, result: ValidationResult):
    """Check that the file has a $schema property."""
    if "$schema" not in data:
        result.warn(rel(file_path, root), "Missing $schema property")


def validate_required_properties(data: dict, file_path: Path, root: Path, result: ValidationResult):
    """Check required properties based on file type."""
    file_name = file_path.name

    # Match against known file types
    if file_name == "definition.pbir":
        key = "definition.pbir"
    elif file_name in REQUIRED_PROPERTIES:
        key = file_name
    elif file_name.endswith(".bookmark.json"):
        return  # bookmark files have varied structure
    else:
        return

    for prop in REQUIRED_PROPERTIES.get(key, []):
        if prop not in data:
            result.error(rel(file_path, root), f"Missing required property: '{prop}'")

    # Extra check for visual.json position
    if file_name == "visual.json" and "position" in data:
        pos = data["position"]
        for p in VISUAL_POSITION_PROPS:
            if p not in pos:
                result.error(rel(file_path, root), f"Missing position.{p}")

    # Extra check for visual.json — must have either 'visual' or 'visualGroup'
    if file_name == "visual.json":
        if "visual" not in data and "visualGroup" not in data:
            result.error(rel(file_path, root), "Must have either 'visual' or 'visualGroup' property")

    # Drillthrough / tooltip page validation
    if file_name == "page.json":
        page_type = data.get("type", PAGE_TYPE_REPORT)
        if page_type == PAGE_TYPE_DRILLTHROUGH:
            # Drillthrough pages should have filters or allFilters configured
            if "filters" not in data and "allFilters" not in data:
                result.warn(
                    rel(file_path, root),
                    "Drillthrough page (type=2) has no 'filters' or 'allFilters' — "
                    "users won't be able to drill through to this page"
                )
        if page_type == PAGE_TYPE_TOOLTIP:
            # Tooltip pages should have appropriate width/height (typically 320x240)
            w = data.get("width")
            h = data.get("height")
            if w and h and (w > 680 or h > 480):
                result.warn(
                    rel(file_path, root),
                    f"Tooltip page (type=1) has large dimensions ({w}x{h}) — "
                    "tooltip pages are typically 320x240 or similar small sizes"
                )

        # Validate displayOption has a recognized value
        display_opt = data.get("displayOption")
        if display_opt is not None and display_opt not in VALID_DISPLAY_OPTIONS:
            result.error(
                rel(file_path, root),
                f"Invalid displayOption: '{display_opt}' — "
                f"must be one of {sorted(VALID_DISPLAY_OPTIONS)}"
            )


def validate_visual_query(data: dict, file_path: Path, root: Path, result: ValidationResult):
    """Check that visual.json has valid query structure if it has a visual with queryRef."""
    if file_path.name != "visual.json":
        return
    visual = data.get("visual")
    if not visual:
        return

    # Check visualType exists — every visual must declare its type
    if "visualType" not in visual:
        result.error(rel(file_path, root), "visual object missing 'visualType'")

    # Check query structure — From entities must have valid Entity/Name
    query = visual.get("query")
    if query:
        commands = query.get("Commands", query.get("commands", []))
        for cmd in commands:
            semantic_query = cmd.get("SemanticQueryDataShapeCommand", {})
            q = semantic_query.get("Query", {})
            from_items = q.get("From", [])
            for item in from_items:
                if "Entity" not in item and "Name" not in item:
                    result.error(
                        rel(file_path, root),
                        f"Query From item missing Entity/Name: {json.dumps(item)[:100]}"
                    )


def validate_cross_references(root: Path, parsed_cache: dict[str, dict | None], result: ValidationResult):
    """Check that page folders match pages.json entries and other cross-refs."""
    definition = root / "definition"
    if not definition.is_dir():
        result.error("definition/", "Missing definition/ folder")
        return

    def get_parsed(file_path: Path) -> dict | None:
        """Return cached parse result, or parse if not cached (without re-reporting syntax errors)."""
        key = str(file_path)
        if key in parsed_cache:
            return parsed_cache[key]
        try:
            text = file_path.read_text(encoding="utf-8")
            return json.loads(text)
        except Exception:
            return None

    # Check pages.json vs actual page folders
    pages_json_path = definition / "pages.json"
    pages_dir = definition / "pages"

    if pages_json_path.is_file() and pages_dir.is_dir():
        data = get_parsed(pages_json_path)
        if data:
            page_order = data.get("pageOrder", [])
            actual_pages = {d.name for d in pages_dir.iterdir() if d.is_dir()}
            listed_pages = set(page_order)

            # Pages in pages.json but missing as folders
            for p in page_order:
                if p not in actual_pages:
                    result.error("pages.json", f"Page '{p}' listed in pageOrder but folder not found")

            # Folders that exist but aren't listed in pages.json
            for p in actual_pages:
                if p not in listed_pages:
                    result.warn("pages.json", f"Page folder '{p}' exists but not listed in pageOrder")

    # Check that each page folder has a page.json
    if pages_dir.is_dir():
        for page_folder in pages_dir.iterdir():
            if page_folder.is_dir():
                if not (page_folder / "page.json").is_file():
                    result.error(
                        rel(page_folder, root),
                        "Page folder missing page.json"
                    )

                # Check page.json name matches folder name
                page_json = page_folder / "page.json"
                if page_json.is_file():
                    pdata = get_parsed(page_json)
                    if pdata and pdata.get("name") != page_folder.name:
                        result.error(
                            rel(page_json, root),
                            f"page.json 'name' is '{pdata.get('name')}' but folder is '{page_folder.name}'"
                        )

                # Check visual folders have visual.json (orphaned scaffold detection)
                visuals_dir = page_folder / "visuals"
                if visuals_dir.is_dir():
                    for visual_folder in visuals_dir.iterdir():
                        if visual_folder.is_dir():
                            if not (visual_folder / "visual.json").is_file():
                                result.error(
                                    rel(visual_folder, root),
                                    "Visual folder missing visual.json (orphaned scaffold)"
                                )

    # Check bookmarks cross-references
    bookmarks_dir = definition / "bookmarks"
    if bookmarks_dir.is_dir():
        bookmarks_json = bookmarks_dir / "bookmarks.json"
        if bookmarks_json.is_file():
            bdata = get_parsed(bookmarks_json)
            if bdata:
                bookmark_order = []
                for group in bdata.get("bookmarkGroups", []):
                    for child in group.get("children", []):
                        if "name" in child:
                            bookmark_order.append(child["name"])
                # Standalone bookmarks
                for bm in bdata.get("bookmarks", []):
                    if "name" in bm:
                        bookmark_order.append(bm["name"])

                actual_bookmarks = {
                    f.stem.replace(".bookmark", "")
                    for f in bookmarks_dir.glob("*.bookmark.json")
                }

                for bm in bookmark_order:
                    if bm not in actual_bookmarks:
                        result.warn(
                            "bookmarks.json",
                            f"Bookmark '{bm}' referenced but .bookmark.json not found"
                        )

                # Check for duplicate bookmark names in bookmark groups
                seen_names = set()
                for name in bookmark_order:
                    if name in seen_names:
                        result.warn("bookmarks.json", f"Duplicate bookmark name: '{name}'")
                    seen_names.add(name)

        # Deep bookmark validation — check internal references
        for bm_file in bookmarks_dir.glob("*.bookmark.json"):
            bm_data = get_parsed(bm_file)
            if not bm_data:
                continue
            # Check activeSection references a real page
            exploration = bm_data.get("explorationState", {})
            active_section = exploration.get("activeSection")
            if active_section and pages_dir.is_dir():
                if not (pages_dir / active_section).is_dir():
                    result.warn(
                        rel(bm_file, root),
                        f"activeSection '{active_section}' references non-existent page"
                    )

    # Check report.json publicCustomVisuals are used somewhere
    report_json = definition / "report.json"
    if report_json.is_file():
        rdata = get_parsed(report_json)
        if rdata:
            registered_visuals = set()
            for cv in rdata.get("publicCustomVisuals", []):
                registered_visuals.add(cv)

            # Scan all visual.json files to find which custom visual types are actually used
            used_visual_types = set()
            if pages_dir.is_dir():
                for vj in pages_dir.rglob("visual.json"):
                    vdata_check = get_parsed(vj)
                    if vdata_check:
                        vtype = vdata_check.get("visual", {}).get("visualType", "")
                        if vtype:
                            used_visual_types.add(vtype)

            # Custom visuals that are registered but never used
            for cv in registered_visuals:
                if cv not in used_visual_types:
                    result.warn("report.json", f"Custom visual '{cv}' registered but not used in any visual")

            # Check: visual uses a non-built-in type but it's not registered
            BUILTIN_TYPES = {
                "card", "cardVisual", "multiRowCard", "slicer",
                "advancedSlicerVisual", "listSlicer", "textSlicer",
                "clusteredBarChart", "clusteredColumnChart", "barChart", "columnChart",
                "hundredPercentStackedBarChart", "hundredPercentStackedColumnChart",
                "lineChart", "areaChart", "stackedAreaChart",
                "lineClusteredColumnComboChart", "lineStackedColumnComboChart",
                "waterfallChart", "treemap", "pieChart", "donutChart",
                "pivotTable", "tableEx", "funnel",
                "scatterChart", "map", "filledMap", "shapeMap", "azureMap",
                "gauge", "kpi", "ribbonChart", "decompositionTreeVisual",
                "keyInfluencersVisual", "qnaVisual",
                "shape", "basicShape", "textbox", "actionButton", "image",
                "pageNavigator", "bookmarkNavigator",
                "scriptVisual", "pythonVisual",
            }
            for vtype in used_visual_types:
                if vtype not in BUILTIN_TYPES and vtype not in registered_visuals:
                    result.error(
                        "report.json",
                        f"Visual type '{vtype}' used but not registered in publicCustomVisuals"
                    )


def validate_naming(root: Path, result: ValidationResult):
    """Check naming conventions for page and visual folders."""
    pages_dir = root / "definition" / "pages"
    if not pages_dir.is_dir():
        return

    for page_folder in pages_dir.iterdir():
        if not page_folder.is_dir():
            continue
        if not is_kebab_case(page_folder.name):
            result.warn(
                rel(page_folder, root),
                f"Page folder '{page_folder.name}' is not kebab-case"
            )

        visuals_dir = page_folder / "visuals"
        if visuals_dir.is_dir():
            for visual_folder in visuals_dir.iterdir():
                if visual_folder.is_dir() and not is_kebab_case(visual_folder.name):
                    result.warn(
                        rel(visual_folder, root),
                        f"Visual folder '{visual_folder.name}' is not kebab-case"
                    )


# --- Main ---

def validate_report(report_path: Path, *, offline: bool = False) -> ValidationResult:
    """Run all validations on a .Report/ folder."""
    result = ValidationResult()

    if not report_path.is_dir():
        result.error(str(report_path), "Path is not a directory")
        return result

    definition = report_path / "definition"
    if not definition.is_dir():
        result.error(str(report_path), "Missing definition/ folder")
        return result

    # 1. JSON syntax validation on ALL json/pbir files
    json_files = list(definition.rglob("*.json"))

    # Also check definition.pbir at report root
    pbir_file = report_path / "definition.pbir"
    if pbir_file.is_file():
        json_files.append(pbir_file)

    parsed_cache: dict[str, dict | None] = {}
    schema_urls: set[str] = set()
    parsed_count = 0
    for jf in json_files:
        data = validate_json_syntax(jf, report_path, result)
        parsed_cache[str(jf)] = data
        if data is not None:
            parsed_count += 1
            validate_schema_property(data, jf, report_path, result)
            validate_required_properties(data, jf, report_path, result)
            validate_visual_query(data, jf, report_path, result)
            # Collect $schema URLs for schema validation
            s = data.get("$schema")
            if isinstance(s, str) and s.startswith("http"):
                schema_urls.add(s)

    # 2. JSON Schema validation (if jsonschema is available)
    schema_validated = 0
    if schema_urls:
        if not HAS_JSONSCHEMA:
            print("  [INFO] jsonschema not installed — skipping full schema validation.", file=sys.stderr)
            print("         Install with: pip install jsonschema", file=sys.stderr)
        else:
            print(f"Fetching schemas (including transitive deps, cached after first run)... ", end="", flush=True)
            schemas = fetch_all_schemas(schema_urls, offline=offline)
            print(f"done. ({len(schemas)} schemas loaded, {len(schema_urls)} direct)")

            validators = build_schema_validators(schemas)
            if validators:
                for jf_str, data in parsed_cache.items():
                    if data is None:
                        continue
                    s = data.get("$schema")
                    if not s or s not in validators:
                        continue
                    v = validators[s]
                    try:
                        errors_list = list(v.iter_errors(data))
                    except Exception:
                        continue
                    if errors_list:
                        jf_path = Path(jf_str)
                        for err in sorted(errors_list, key=lambda e: str(e.path)):
                            loc = "/".join(str(p) for p in err.absolute_path) or "(root)"
                            result.error(rel(jf_path, report_path), f"{loc} — {err.message}")
                    schema_validated += 1

    # 3. Cross-reference checks (uses cached parse results to avoid duplicate errors)
    validate_cross_references(report_path, parsed_cache, result)

    # 4. Naming convention checks
    validate_naming(report_path, result)

    # Summary
    schema_msg = f", {schema_validated} schema-validated" if schema_validated else ""
    print(f"\nValidated {parsed_count}/{len(json_files)} files in {report_path.name}{schema_msg}")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate a Power BI PBIR .Report folder against Microsoft's published JSON schemas.",
        epilog="Examples:\n"
               "  python validate_report.py ./MyReport.Report\n"
               "  python validate_report.py ./MyReport.Report --offline\n",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("report", type=Path, help="Path to the .Report folder (or parent containing one)")
    parser.add_argument("--offline", action="store_true",
                        help="Use only cached schemas (no network). Falls back to structural checks.")
    parser.add_argument("--verbose", action="store_true", help="Show debug details")
    parser.add_argument("--quiet", action="store_true", help="Only show warnings and errors")
    args = parser.parse_args()

    log = setup_logging("validate_report", verbose=args.verbose, quiet=args.quiet)

    report_path = args.report.resolve()

    # If user pointed to the project root, find the .Report folder
    if not report_path.name.endswith(".Report"):
        candidates = list(report_path.glob("*.Report"))
        if len(candidates) == 1:
            report_path = candidates[0]
        elif len(candidates) > 1:
            log.error("Multiple .Report folders found. Specify one: %s", [c.name for c in candidates])
            return 1
        else:
            log.error("No .Report folder found in %s", report_path)
            return 1

    result = validate_report(report_path, offline=args.offline)

    if result.warnings:
        log.info("")
        log.info("=" * 60)
        log.info("WARNINGS (%d):", len(result.warnings))
        log.info("=" * 60)
        for w in result.warnings:
            log.info("  %s", w)

    if result.errors:
        log.info("")
        log.info("=" * 60)
        log.info("ERRORS (%d):", len(result.errors))
        log.info("=" * 60)
        for e in result.errors:
            log.info("  %s", e)
        log.error("Validation FAILED — %d error(s)", len(result.errors))
        return 1
    else:
        log.info("Validation PASSED — no errors (%d warning(s))", len(result.warnings))
        return 0


if __name__ == "__main__":
    sys.exit(main())
