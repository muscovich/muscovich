#!/usr/bin/env python3
"""Calculate SHA-256 digests for files and verify a saved digest manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_manifest(paths: list[Path]) -> dict[str, str]:
    manifest = {}
    for path in paths:
        if not path.is_file():
            raise FileNotFoundError(f"Not a file: {path}")
        manifest[str(path)] = sha256_file(path)
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create or verify SHA-256 file integrity manifests."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    create_parser = subparsers.add_parser("create", help="Create a JSON manifest.")
    create_parser.add_argument("files", nargs="+", type=Path)
    create_parser.add_argument("-o", "--output", type=Path, default=Path("sha256-manifest.json"))

    verify_parser = subparsers.add_parser("verify", help="Verify files against a manifest.")
    verify_parser.add_argument("manifest", type=Path)

    args = parser.parse_args()

    try:
        if args.command == "create":
            manifest = build_manifest(args.files)
            args.output.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
            print(f"Wrote {len(manifest)} digest(s) to {args.output}")
            return 0

        manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
        failures = 0
        for filename, expected in manifest.items():
            path = Path(filename)
            if not path.is_file():
                print(f"MISSING  {filename}")
                failures += 1
                continue
            actual = sha256_file(path)
            if actual == expected:
                print(f"OK       {filename}")
            else:
                print(f"MISMATCH {filename}")
                failures += 1
        print(f"\nChecked {len(manifest)} file(s); {failures} issue(s).")
        return 1 if failures else 0

    except (OSError, json.JSONDecodeError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    raise SystemExit(main())
