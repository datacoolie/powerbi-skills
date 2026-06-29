# Power BI Desktop Verification

> Read this when you need to open Power BI Desktop, reload a PBIP/PBIR report,
> capture screenshots, choose a Desktop PID, or interpret `powerbi-desktop` CLI
> output. This file is the detailed runbook for the visual verification loop.

## Core Rule

For PBIR edits that affect rendered output, do not rely on JSON validation alone.
Power BI Desktop can reject or visually misrender definitions that are
structurally valid. Use this loop:

1. Edit PBIR files.
2. Run `powerbi-report-author validate "<path-to-.Report-dir>"`.
3. Run `powerbi-desktop status`.
4. Select the intended Desktop instance by PID.
5. Run `powerbi-desktop reload --pid <pid>`.
6. Capture screenshots from the same PID.
7. Review screenshots; if anything is wrong, fix PBIR and restart at step 2.

## Setup

Install the Desktop Bridge CLI globally:

```bash
npm install -g @microsoft/powerbi-desktop-bridge-cli
powerbi-desktop --version
```

Prerequisite: Node.js 20+. If missing, install via:
- Windows: `winget install OpenJS.NodeJS.LTS`
- macOS: `brew install node`
- Linux: distro package or [nodesource](https://github.com/nodesource/distributions)

## Command Reference

| Command | Purpose | When to use |
|---------|---------|-------------|
| `open "<path.pbip>"` | Launch Power BI Desktop for a PBIP/PBIX | Starting Desktop or opening the target report |
| `status` | List Desktop Bridge instances, current files, report dirs, bridge state | Before reload/screenshot; choose the correct PID |
| `manifest --pid <pid>` | Show detailed manifest for a specific instance | Debugging bridge issues |
| `reload --pid <pid>` | Reload the selected instance's current PBIP report files | After validated PBIR edits |
| `screenshot <page-id> --pid <pid> --output <file>` | Capture one page by PBIR page ID | Isolated page changes |
| `screenshot-all --pid <pid> --output-dir <dir>` | Capture every report page | Theme, navigation, or report-wide changes |

### Important Notes

- `open <path>` is the only command that accepts a PBIP/PBIX path. Other commands
  target a running Desktop Bridge instance by PID.
- If exactly one instance is available, `--pid` may be omitted, but passing the
  PID is safer and should always be preferred.
- No command accepts `--report`. The same PBIP can be open in multiple Desktop
  processes, so use `status` and choose by PID.
- `screenshot <page-id>` takes the PBIR page ID (folder name in `pages/`),
  not the display name shown in Desktop tabs.
- Screenshots default to scale `2` for readable visual review. Pass `--scale 1`
  for smaller files; `--scale 3` for extra detail.
- Run reload and screenshot operations **serially** per PID — never in parallel
  against the same PID.

## Status and PID Selection

```bash
powerbi-desktop status
```

Choose the PID where:
- `bridgeStatus` is `connected`
- `currentFilePath` matches the target PBIP/PBIX
- `reportDir` resolves to the expected `.Report` folder
- `diagnostics` is empty or only contains non-blocking warnings

If multiple instances are present, never guess. Choose the PID from `status`.

## Open and Reload

To start Desktop:
```bash
powerbi-desktop open "C:\Reports\Sales\Sales.pbip"
powerbi-desktop status
```

After editing PBIR files:
```bash
powerbi-report-author validate "C:\Reports\Sales\Sales.Report"
powerbi-desktop reload --pid <bridge-pid-from-status>
```

### Reload Limitations

- `reload` is for report-definition changes only. For semantic model/TMDL
  changes, use the semantic-model skill and reopen the PBIP.
- `reload` is supported only for PBIP-backed reports. If the PID has only a
  `.pbix` open, reload returns `REPORT_DIR_REQUIRED`.
- **Theme cache:** When editing an existing theme JSON, Desktop may not pick up
  the change on reload (cache-keyed by file name). Either rename the theme file
  with a random suffix and update `report.json`, or close and reopen Desktop.
- Fix all validation errors before reloading. Reloading invalid PBIR leaves the
  report in a broken visual state.

## Screenshots

> **Capture scope:** Each screenshot captures the report page **AND** the
> right-hand filter pane when enabled and expanded.

Capture one page when the change is isolated:
```bash
powerbi-desktop screenshot <page-id> --pid <pid> --output screenshots/page.png
```

Capture all pages for theme, formatting, navigation, or report-wide changes:
```bash
powerbi-desktop screenshot-all --pid <pid> --output-dir screenshots
```

## Common Outcomes

| Output/error | Meaning | Action |
|---|---|---|
| `"status": "not_connected"` | No Desktop Bridge discoverable | Run `powerbi-desktop open "<path.pbip>"` or ask user to start Desktop |
| `NO_BRIDGE` / `connect ENOENT \\.\pipe\pbi-desktop-bridge-<pid>` | Desktop running but bridge pipe unavailable | Enable preview feature: File → Options → Preview features → "Enable external tool access…", restart Desktop |
| `AMBIGUOUS_DESKTOP_INSTANCE` | Multiple bridge instances available | Run `status`, choose intended PID, retry with `--pid` |
| `METHOD_NOT_AVAILABLE` | Desktop build lacks required bridge method | Desktop is stale/unsupported — see [docs](https://aka.ms/Report_Authoring_skill_LearnDocs) |
| `HostNotReady` / retryable error | Desktop up but report host not ready | CLI auto-retries; rerun once if it surfaces |
| `Timeout` | Reload/screenshot exceeded retry budget | Confirm `status` shows `connected`, retry once. Persist → use `--wait-seconds 120` |
| `Cancelled` | Concurrent reload/screenshot on same PID | Serialize operations per PID, wait for `connected`, retry |
| `ReportDefinitionValidationFailed` | Desktop rejected PBIR | Fix PBIR, validate, then reload again |
| `REPORT_DIR_REQUIRED` | PID has no PBIP/PBIR current file | Select correct PID from `status` or open target PBIP |
| Page not found / empty screenshot | Wrong page ID (used display name?) | Read `pages/pages.json`, use the PBIR folder name |

## Fix-Retry Pattern

When Desktop reports a load or render error:

1. Read the CLI error and Desktop diagnostic details.
2. Open the referenced PBIR JSON file and fix the offending property.
3. Run `powerbi-report-author validate <path-to-.Report-dir>`.
4. Run `powerbi-desktop reload --pid <same-pid>`.
5. Capture screenshots again from the same PID.

Do not switch PIDs mid-loop unless `status` shows the original instance closed.

## Enabling Desktop Bridge

If `powerbi-desktop status` returns `not_connected` even though Desktop is running:

1. In Desktop: **File → Options and settings → Options → Preview features**
2. Enable **"Enable external tool access to Power BI Desktop through secure local APIs"**
3. Restart Power BI Desktop
4. Retry: `powerbi-desktop status --wait-seconds 30`

Reference: [Power BI report authoring docs](https://aka.ms/Report_Authoring_skill_LearnDocs)
