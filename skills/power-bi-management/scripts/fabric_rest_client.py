"""Fabric REST transport for Power BI report management.

Wraps the Azure CLI (``az rest``) against the Fabric API. This module owns the
Tier-2 fallback lane: it is used only when no exact Fabric MCP capability exists
for the requested operation.

Design constraints (see plans/260905-fabric-resync/appendix-1.md):
- Standard library only; the Azure CLI is the sole external dependency.
- ``stdout`` (response body) and ``stderr`` (verbose header log) are captured
  separately so a JSON body never contains verbose header noise.
- Every ambiguous or failed state fails closed with a structured error.
- Long-running operations honour ``Retry-After`` and a monotonic deadline, and
  surface the service error instead of finishing silently.
"""

from __future__ import annotations

import json
import re
import subprocess
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Optional
from urllib.parse import urlparse

FABRIC_RESOURCE = "https://api.fabric.microsoft.com"
FABRIC_HOST = "api.fabric.microsoft.com"
FABRIC_BASE = "https://api.fabric.microsoft.com/v1"

# Terminal LRO states per Fabric long-running-operation contract.
_LRO_RUNNING = {"notstarted", "running"}
_LRO_SUCCESS = {"succeeded"}
_LRO_FAILURE = {"failed", "cancelled", "canceled"}

_DEFAULT_RETRY_AFTER_S = 3
_DEFAULT_DEADLINE_S = 600


class FabricRestError(RuntimeError):
    """Raised for any non-success or ambiguous Fabric REST outcome."""

    def __init__(
        self,
        message: str,
        *,
        status: Optional[int] = None,
        error_code: Optional[str] = None,
        details: Any = None,
        operation_id: Optional[str] = None,
    ) -> None:
        super().__init__(message)
        self.status = status
        self.error_code = error_code
        self.details = details
        self.operation_id = operation_id


@dataclass
class RestResponse:
    """Parsed result of a single ``az rest`` call."""

    status: Optional[int]
    headers: dict[str, str] = field(default_factory=dict)
    body: Any = None
    text: str = ""

    def header(self, name: str) -> Optional[str]:
        """Case-insensitive header lookup."""
        target = name.lower()
        for key, value in self.headers.items():
            if key.lower() == target:
                return value
        return None


# Injection seam: tests replace this with a fake that returns canned output.
def _run_subprocess(args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(  # noqa: S603 - args are a fixed list, never shell=True
        args,
        capture_output=True,
        text=True,
        check=False,
    )


_run: Callable[[list[str]], subprocess.CompletedProcess] = _run_subprocess


_STATUS_RE = re.compile(r"response status[^0-9]*(\d{3})", re.IGNORECASE)
_INTERESTING_HEADERS = (
    "x-ms-operation-id",
    "location",
    "retry-after",
    "x-ms-error-code",
)
# One matcher per known header: tolerant of quoting and log prefixes because it
# anchors on the header name itself rather than on line structure.
_HEADER_RES = {
    name: re.compile(
        r"['\"]?" + re.escape(name) + r"['\"]?\s*[:=]\s*['\"]?([^'\"\r\n]+?)['\"]?\s*$",
        re.IGNORECASE,
    )
    for name in _INTERESTING_HEADERS
}


def parse_verbose(stderr: str) -> tuple[Optional[int], dict[str, str]]:
    """Extract HTTP status and interesting headers from az ``--verbose`` output.

    The az CLI verbose format is not a stable contract, so this parser is
    deliberately tolerant and fails closed: if no status line is found the
    caller treats the response as unusable rather than guessing success.
    """
    status: Optional[int] = None
    headers: dict[str, str] = {}
    for line in stderr.splitlines():
        if status is None:
            status_match = _STATUS_RE.search(line)
            if status_match:
                status = int(status_match.group(1))
                continue
        for name, matcher in _HEADER_RES.items():
            if name in headers:
                continue
            found = matcher.search(line)
            if found:
                headers[name] = found.group(1).strip()
    return status, headers


def _validate_fabric_url(url: str) -> None:
    parsed = urlparse(url)
    if parsed.scheme != "https":
        raise FabricRestError(f"Refusing non-HTTPS Fabric URL: {url!r}")
    if parsed.hostname != FABRIC_HOST:
        raise FabricRestError(
            f"Refusing URL outside {FABRIC_HOST}: {url!r}. "
            "The Azure token must not be sent to another host."
        )


def az_rest(
    method: str,
    url: str,
    *,
    body_file: Optional[str] = None,
    extra_headers: Optional[dict[str, str]] = None,
    resource: str = FABRIC_RESOURCE,
    verbose: bool = True,
) -> RestResponse:
    """Invoke ``az rest`` and return a parsed :class:`RestResponse`.

    Raises :class:`FabricRestError` on transport failure or an unparseable
    verbose stream. HTTP-level success/failure is decided by the caller from
    ``response.status`` so that ``202`` is handled explicitly rather than being
    mistaken for a completed result.
    """
    _validate_fabric_url(url)
    args = [
        "az",
        "rest",
        "--method",
        method.lower(),
        "--url",
        url,
        "--resource",
        resource,
    ]
    for name, value in (extra_headers or {}).items():
        args += ["--headers", f"{name}={value}"]
    if body_file:
        args += ["--body", f"@{body_file}"]
    if verbose:
        args.append("--verbose")

    completed = _run(args)
    status, headers = parse_verbose(completed.stderr or "")
    body = _parse_json(completed.stdout)

    if completed.returncode != 0 and status is None:
        raise FabricRestError(
            f"az rest failed for {method} {url}",
            details=(completed.stderr or completed.stdout or "").strip(),
        )
    return RestResponse(
        status=status,
        headers=headers,
        body=body,
        text=completed.stdout or "",
    )


def _parse_json(text: Optional[str]) -> Any:
    if not text:
        return None
    stripped = text.strip()
    if not stripped:
        return None
    try:
        return json.loads(stripped)
    except json.JSONDecodeError:
        return None


def _require_success(response: RestResponse, context: str) -> None:
    if response.status is None:
        raise FabricRestError(
            f"Could not determine HTTP status for {context}; treating as failure.",
        )
    if response.status >= 400:
        error_code, message = _extract_error(response.body)
        raise FabricRestError(
            f"{context} returned HTTP {response.status}: {message or 'unknown error'}",
            status=response.status,
            error_code=error_code,
            details=response.body,
        )


def _extract_error(body: Any) -> tuple[Optional[str], Optional[str]]:
    if isinstance(body, dict):
        code = body.get("errorCode") or body.get("code")
        message = body.get("message")
        error = body.get("error")
        if isinstance(error, dict):
            code = code or error.get("code")
            message = message or error.get("message")
        return code, message
    return None, None


def paginate(url: str, *, extra_headers: Optional[dict[str, str]] = None) -> list[Any]:
    """Follow ``continuationUri`` and accumulate every ``value[]`` entry."""
    items: list[Any] = []
    next_url: Optional[str] = url
    seen: set[str] = set()
    while next_url:
        if next_url in seen:
            raise FabricRestError(f"Pagination loop detected at {next_url!r}")
        seen.add(next_url)
        _validate_fabric_url(next_url)
        response = az_rest("get", next_url, extra_headers=extra_headers)
        _require_success(response, f"GET {next_url}")
        body = response.body or {}
        items.extend(body.get("value", []) if isinstance(body, dict) else [])
        next_url = body.get("continuationUri") if isinstance(body, dict) else None
    return items


def _resolve_unique(
    items: list[dict[str, Any]],
    display_name: str,
    kind: str,
) -> str:
    matches = [
        item
        for item in items
        if item.get("displayName") == display_name and item.get("id")
    ]
    if not matches:
        raise FabricRestError(f"No {kind} named {display_name!r} was found.")
    if len(matches) > 1:
        ids = ", ".join(sorted(str(m.get("id")) for m in matches))
        raise FabricRestError(
            f"{len(matches)} {kind}s named {display_name!r} exist ({ids}); "
            "pass an explicit id to disambiguate."
        )
    return str(matches[0]["id"])


def resolve_workspace_id(name: str) -> str:
    """Return the single workspace id for ``name`` or fail closed."""
    items = paginate(f"{FABRIC_BASE}/workspaces")
    return _resolve_unique(items, name, "workspace")


def resolve_report_id(workspace_id: str, name: str) -> str:
    """Return the single report id for ``name`` in a workspace or fail closed."""
    items = paginate(f"{FABRIC_BASE}/workspaces/{workspace_id}/reports")
    return _resolve_unique(items, name, "report")


def poll_operation(
    operation_id: str,
    *,
    get_result: bool = False,
    initial_retry_after: Optional[int] = None,
    deadline_s: int = _DEFAULT_DEADLINE_S,
    sleep: Callable[[float], None] = time.sleep,
    now: Callable[[], float] = time.monotonic,
) -> Any:
    """Poll a Fabric LRO to a terminal state.

    Honours ``Retry-After``, enforces a monotonic deadline, and raises
    :class:`FabricRestError` for failed/cancelled/timeout/unknown states rather
    than returning silently. Fetches the result only when ``get_result`` is set.
    """
    if not operation_id:
        raise FabricRestError("Missing operation id; cannot poll a 202 response.")

    state_url = f"{FABRIC_BASE}/operations/{operation_id}"
    deadline = now() + deadline_s
    retry_after = initial_retry_after or _DEFAULT_RETRY_AFTER_S

    while True:
        if now() >= deadline:
            raise FabricRestError(
                f"Operation {operation_id} did not finish within {deadline_s}s; "
                "the operation id is preserved for manual recovery.",
                operation_id=operation_id,
            )
        sleep(min(retry_after, max(0, deadline - now())))
        response = az_rest("get", state_url)
        _require_success(response, f"operation {operation_id} status")
        body = response.body or {}
        status = str(body.get("status", "")).lower()
        header_retry = response.header("retry-after")
        if header_retry and header_retry.isdigit():
            retry_after = int(header_retry)

        if status in _LRO_RUNNING:
            continue
        if status in _LRO_FAILURE:
            error = body.get("error") if isinstance(body, dict) else None
            code, message = _extract_error({"error": error} if error else body)
            raise FabricRestError(
                f"Operation {operation_id} ended in state {status!r}: "
                f"{message or 'no error detail'}",
                error_code=code,
                details=error,
                operation_id=operation_id,
            )
        if status in _LRO_SUCCESS:
            if not get_result:
                return body
            result = az_rest("get", f"{state_url}/result")
            _require_success(result, f"operation {operation_id} result")
            return result.body
        raise FabricRestError(
            f"Operation {operation_id} returned unknown state {status!r}.",
            operation_id=operation_id,
        )


def send_definition_request(
    method: str,
    url: str,
    *,
    body_file: Optional[str] = None,
    extra_headers: Optional[dict[str, str]] = None,
    get_result: bool = False,
    **poll_kwargs: Any,
) -> Any:
    """Run a create/get/update call and resolve both 200/201 and 202 paths.

    Returns the parsed definition/result body regardless of whether the service
    answered synchronously (200/201) or asynchronously (202 + LRO), so callers
    never depend on a fixed temp-file path.
    """
    response = az_rest(
        method,
        url,
        body_file=body_file,
        extra_headers=extra_headers,
    )
    if response.status in (200, 201):
        return response.body
    if response.status == 202:
        operation_id = response.header("x-ms-operation-id")
        location = response.header("location")
        if not operation_id and location:
            operation_id = location.rstrip("/").rsplit("/", 1)[-1]
        retry_after = response.header("retry-after")
        return poll_operation(
            operation_id or "",
            get_result=get_result,
            initial_retry_after=int(retry_after) if retry_after and retry_after.isdigit() else None,
            **poll_kwargs,
        )
    _require_success(response, f"{method} {url}")
    return response.body
