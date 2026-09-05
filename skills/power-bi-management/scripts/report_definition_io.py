"""PBIR definition packaging, extraction, and immutable publish staging.

Safety rules (see plans/260905-fabric-resync/appendix-1.md):
- Upload only the documented public definition parts; never local cache or
  Git-integration metadata (``.pbi/**``, ``.platform``, ``.pbip``).
- Rewrite ``byPath`` to ``byConnection`` only in a temporary staging copy so the
  source project is never mutated.
- Reject API-controlled part paths that could escape the chosen output root.
- Decode base64 strictly and write atomically.
"""

from __future__ import annotations

import base64
import hashlib
import json
import os
import shutil
import tempfile
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Optional

# Root files that belong in a public report definition. ``.platform`` is a Fabric
# Git-integration system file and is intentionally excluded from transport.
ALLOWED_ROOT_FILES = {"definition.pbir", "semanticModelDiagramLayout.json"}
ALLOWED_DIRS = ("definition/", "StaticResources/")
REQUIRED_ROOT_FILE = "definition.pbir"

# Local noise that must never be uploaded even if present in the folder.
IGNORED_DIR_NAMES = {".pbi"}
IGNORED_FILE_NAMES = {"thumbs.db", ".ds_store"}
IGNORED_SUFFIXES = (".pbip", ".tmp", ".bak", "~")


class DefinitionError(RuntimeError):
    """Raised for unsafe or malformed report definitions."""


@dataclass
class DefinitionPart:
    path: str  # forward-slash relative path
    abs_path: Path


def _is_ignored(rel_posix: str) -> bool:
    parts = rel_posix.split("/")
    name = parts[-1].lower()
    if any(seg in IGNORED_DIR_NAMES for seg in parts[:-1]):
        return True
    if parts[0] in IGNORED_DIR_NAMES:
        return True
    if name in IGNORED_FILE_NAMES:
        return True
    if any(name.endswith(suffix) for suffix in IGNORED_SUFFIXES):
        return True
    # Dotfiles (including the Fabric ``.platform`` system file) are known local
    # metadata that is deliberately not transported to the report definition.
    if name.startswith("."):
        return True
    return False


def _is_allowed(rel_posix: str) -> bool:
    if rel_posix in ALLOWED_ROOT_FILES:
        return True
    return any(rel_posix.startswith(prefix) for prefix in ALLOWED_DIRS)


def collect_parts(report_dir: str | os.PathLike[str]) -> list[DefinitionPart]:
    """Return the allowlisted definition parts under ``report_dir``.

    Fails closed on symlinks and on unexpected root files rather than silently
    transporting them.
    """
    root = Path(report_dir).resolve()
    if not (root / REQUIRED_ROOT_FILE).is_file():
        raise DefinitionError(f"{REQUIRED_ROOT_FILE} is required but missing in {root}")

    parts: list[DefinitionPart] = []
    unexpected: list[str] = []
    for abs_path in sorted(root.rglob("*")):
        if abs_path.is_symlink():
            raise DefinitionError(f"Refusing symlink in report definition: {abs_path}")
        if not abs_path.is_file():
            continue
        rel_posix = PurePosixPath(abs_path.relative_to(root).as_posix()).as_posix()
        if _is_ignored(rel_posix):
            continue
        if not _is_allowed(rel_posix):
            unexpected.append(rel_posix)
            continue
        parts.append(DefinitionPart(path=rel_posix, abs_path=abs_path))

    if unexpected:
        raise DefinitionError(
            "Unexpected files outside the definition allowlist: "
            + ", ".join(sorted(unexpected))
        )
    if not parts:
        raise DefinitionError(f"No uploadable definition parts found under {root}")
    return parts


def build_upload_payload(report_dir: str | os.PathLike[str]) -> dict[str, Any]:
    """Build the ``{"definition": {"parts": [...]}}`` upload body."""
    parts = collect_parts(report_dir)
    payload_parts = [
        {
            "path": part.path,
            "payload": base64.b64encode(part.abs_path.read_bytes()).decode("ascii"),
            "payloadType": "InlineBase64",
        }
        for part in parts
    ]
    return {"definition": {"parts": payload_parts}}


def rewrite_binding(pbir: dict[str, Any], semantic_model_id: str) -> dict[str, Any]:
    """Return a copy of ``definition.pbir`` bound ``byConnection`` for the API."""
    if not semantic_model_id:
        raise DefinitionError("A concrete semanticModelId is required to rebind.")
    updated = json.loads(json.dumps(pbir))  # deep copy without external deps
    updated["datasetReference"] = {
        "byConnection": {"connectionString": f"semanticmodelid={semantic_model_id}"}
    }
    return updated


def stage_publish_copy(
    report_dir: str | os.PathLike[str],
    semantic_model_id: str,
) -> str:
    """Copy the allowlisted definition to a temp dir and rebind ``byConnection``.

    The source project is never modified. Returns the staging directory path;
    the caller owns cleanup (see :func:`cleanup`).
    """
    parts = collect_parts(report_dir)
    staging = Path(tempfile.mkdtemp(prefix="pbi-publish-"))
    for part in parts:
        dest = staging / part.path
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(part.abs_path, dest)

    staged_pbir = staging / REQUIRED_ROOT_FILE
    pbir = json.loads(staged_pbir.read_text(encoding="utf-8"))
    staged_pbir.write_text(
        json.dumps(rewrite_binding(pbir, semantic_model_id), indent=2),
        encoding="utf-8",
    )
    return str(staging)


def content_digest(report_dir: str | os.PathLike[str]) -> str:
    """Stable digest of every file under ``report_dir`` (order-independent)."""
    root = Path(report_dir).resolve()
    hasher = hashlib.sha256()
    for abs_path in sorted(root.rglob("*")):
        if abs_path.is_file() and not abs_path.is_symlink():
            rel = abs_path.relative_to(root).as_posix()
            hasher.update(rel.encode("utf-8"))
            hasher.update(b"\0")
            hasher.update(abs_path.read_bytes())
            hasher.update(b"\0")
    return hasher.hexdigest()


def _safe_relative(part_path: str, out_root: Path) -> Path:
    if not part_path or part_path.strip() == "":
        raise DefinitionError("Empty definition part path.")
    if "\0" in part_path:
        raise DefinitionError("NUL byte in definition part path.")
    if "\\" in part_path:
        raise DefinitionError(f"Backslash in part path is not allowed: {part_path!r}")
    pure = PurePosixPath(part_path)
    if pure.is_absolute() or (len(part_path) >= 2 and part_path[1] == ":"):
        raise DefinitionError(f"Absolute part path is not allowed: {part_path!r}")
    if any(segment in ("", ".", "..") for segment in pure.parts):
        raise DefinitionError(f"Path traversal in part path: {part_path!r}")
    resolved = (out_root / pure).resolve()
    if out_root not in resolved.parents and resolved != out_root:
        raise DefinitionError(f"Part path escapes output root: {part_path!r}")
    return resolved


def safe_extract(definition: dict[str, Any], out_dir: str | os.PathLike[str]) -> list[str]:
    """Decode and write definition parts under ``out_dir`` atomically.

    Validates every API-controlled path before any write, rejects duplicates and
    case collisions, and only promotes the staging directory to ``out_dir`` once
    every part has been written successfully.
    """
    parts = (definition or {}).get("definition", {}).get("parts")
    if not isinstance(parts, list) or not parts:
        raise DefinitionError("Definition contains no parts to extract.")

    out_root = Path(out_dir).resolve()
    staging = Path(tempfile.mkdtemp(prefix="pbi-download-"))
    written: list[str] = []
    seen_lower: set[str] = set()
    try:
        for part in parts:
            rel = part.get("path", "")
            lower = rel.lower()
            if lower in seen_lower:
                raise DefinitionError(f"Duplicate or case-colliding part: {rel!r}")
            seen_lower.add(lower)
            dest = _safe_relative(rel, staging)
            try:
                raw = base64.b64decode(part.get("payload", ""), validate=True)
            except (ValueError, TypeError) as exc:
                raise DefinitionError(f"Invalid base64 for part {rel!r}: {exc}") from exc
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(raw)
            written.append(rel)

        if out_root.exists():
            shutil.rmtree(out_root)
        out_root.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(staging), str(out_root))
    finally:
        if staging.exists():
            shutil.rmtree(staging, ignore_errors=True)
    return written


def cleanup(path: Optional[str]) -> None:
    """Remove a staging directory, ignoring errors."""
    if path and os.path.isdir(path):
        shutil.rmtree(path, ignore_errors=True)
