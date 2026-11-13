# File integrity utility

A small Python command-line tool for calculating and checking SHA-256 digests.

## Requirements

- Python 3.10 or newer
- No third-party dependencies

## Create a manifest

```bash
python tools/file_integrity.py create README.md research/README.md -o sha256-manifest.json
```

## Verify a manifest

```bash
python tools/file_integrity.py verify sha256-manifest.json
```

A matching digest indicates that the file contents match the contents recorded when the manifest was created. Keep the manifest somewhere trustworthy; an attacker able to replace both a file and its manifest can replace both digests too.

## Limitations

This is an integrity-checking demonstration, not a digital-signature system or a complete forensic evidence-management solution. SHA-256 does not establish who created a file or when it was created.
