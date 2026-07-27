#!/usr/bin/env python3
"""Validate ZIJIN AI Memory cases using only the Python standard library."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Iterable

REQUIRED_CASE_FILES = {
    "manifest.json",
    "conversation_memory.md",
    "people_memory.md",
    "insight_memory.md",
    "opportunity_memory.md",
    "case_card.md",
}
RELATIONSHIP_TYPES = {
    "client",
    "prospective_client",
    "partner",
    "channel",
    "expert",
    "project_owner",
    "mixed",
}
EVIDENCE_LEVELS = {"confirmed", "inferred", "hypothesis"}
SOURCE_TYPES = {"interview", "conversation", "meeting", "course_feedback", "idea", "mixed"}
PRIVACY_LEVELS = {"public_safe", "private", "restricted"}
STATUS_VALUES = {"template", "draft", "validated", "archived"}
PLACEHOLDER_PATTERNS = [
    re.compile(r"\{\{[^{}]+\}\}"),
    re.compile(r"CASE-XXX"),
    re.compile(r"<[^>]{2,80}>")
]
FRONT_MATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def parse_front_matter(text: str) -> dict[str, str]:
    match = FRONT_MATTER_RE.search(text)
    if not match:
        return {}
    data: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip()
    return data


def validate_manifest(manifest: dict, case_dir: Path) -> list[str]:
    errors: list[str] = []
    required = {
        "case_id",
        "title",
        "date",
        "source_type",
        "relationship_types",
        "evidence_levels",
        "privacy",
        "status",
        "tags",
    }
    missing = sorted(required - manifest.keys())
    if missing:
        errors.append(f"{case_dir}: manifest missing keys: {', '.join(missing)}")
        return errors

    if not re.fullmatch(r"CASE-\d{3}", str(manifest["case_id"])):
        errors.append(f"{case_dir}: invalid case_id {manifest['case_id']!r}")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(manifest["date"])):
        errors.append(f"{case_dir}: invalid date {manifest['date']!r}")
    if manifest["source_type"] not in SOURCE_TYPES:
        errors.append(f"{case_dir}: invalid source_type")
    if manifest["privacy"] not in PRIVACY_LEVELS:
        errors.append(f"{case_dir}: invalid privacy")
    if manifest["status"] not in STATUS_VALUES:
        errors.append(f"{case_dir}: invalid status")

    relationships = set(manifest.get("relationship_types", []))
    if not relationships or not relationships <= RELATIONSHIP_TYPES:
        errors.append(f"{case_dir}: invalid relationship_types {sorted(relationships)}")
    evidence = set(manifest.get("evidence_levels", []))
    if not evidence or not evidence <= EVIDENCE_LEVELS:
        errors.append(f"{case_dir}: invalid evidence_levels {sorted(evidence)}")
    if not isinstance(manifest.get("tags"), list):
        errors.append(f"{case_dir}: tags must be an array")
    return errors


def validate_case(case_dir: Path) -> list[str]:
    errors: list[str] = []
    manifest_path = case_dir / "manifest.json"
    if not manifest_path.exists():
        return [f"{case_dir}: missing manifest.json"]

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        return [f"{case_dir}: cannot read manifest.json: {exc}"]

    errors.extend(validate_manifest(manifest, case_dir))
    status = manifest.get("status")
    if status == "template":
        return errors

    present = {path.name for path in case_dir.iterdir() if path.is_file()}
    missing_files = sorted(REQUIRED_CASE_FILES - present)
    if missing_files:
        errors.append(f"{case_dir}: missing files: {', '.join(missing_files)}")
        return errors

    case_id = str(manifest.get("case_id", ""))
    privacy = str(manifest.get("privacy", ""))
    for filename in sorted(REQUIRED_CASE_FILES - {"manifest.json"}):
        path = case_dir / filename
        text = path.read_text(encoding="utf-8")
        front = parse_front_matter(text)
        if front.get("case_id") != case_id:
            errors.append(f"{path}: front matter case_id must be {case_id}")
        if front.get("privacy") != privacy:
            errors.append(f"{path}: front matter privacy must be {privacy}")
        if not front.get("asset_type"):
            errors.append(f"{path}: missing asset_type in front matter")
        for pattern in PLACEHOLDER_PATTERNS:
            if pattern.search(text):
                errors.append(f"{path}: unresolved placeholder matching {pattern.pattern!r}")

    if privacy == "public_safe":
        forbidden_names = {"transcript.md", "full_transcript.md", "raw_chat.md", "contacts.md"}
        found_forbidden = forbidden_names & present
        if found_forbidden:
            errors.append(f"{case_dir}: public case includes sensitive raw files: {sorted(found_forbidden)}")
    return errors


def iter_case_dirs(examples_dir: Path) -> Iterable[Path]:
    if not examples_dir.exists():
        return []
    return sorted(path for path in examples_dir.iterdir() if path.is_dir() and path.name.startswith("case_"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("case_dir", nargs="?", type=Path)
    parser.add_argument("--all", action="store_true", help="validate every case under examples/")
    args = parser.parse_args()

    skill_root = Path(__file__).resolve().parents[1]
    if args.all:
        case_dirs = list(iter_case_dirs(skill_root / "examples"))
    elif args.case_dir:
        case_dirs = [args.case_dir]
    else:
        parser.error("provide case_dir or --all")

    errors: list[str] = []
    for case_dir in case_dirs:
        errors.extend(validate_case(case_dir))
    if errors:
        print("VALIDATION FAILED")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"VALIDATION PASSED: {len(case_dirs)} case directorie(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
