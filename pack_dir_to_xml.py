#!/usr/bin/env python3

# Run command: python pack_dir_to_xml.py . combined_files.xml
# To include hidden files (like .gitignore), add the flag:
# python pack_dir_to_xml.py . output.xml --include-hidden
# To skip files larger than a threshold (for example, 1 MB):
# python pack_dir_to_xml.py . output.xml --max-bytes 1000000

import argparse
import base64
import os
import sys
import mimetypes
import xml.etree.ElementTree as ET

def is_text_file(path, sniff_bytes=2048):
    mime, _ = mimetypes.guess_type(path)
    if mime:
        if mime.startswith("text/") or mime in {"application/xml", "application/json"}:
            return True
        if any(path.endswith(ext) for ext in (
            ".py", ".js", ".ts", ".tsx", ".jsx", ".java", ".c", ".cpp", ".h", ".hpp",
            ".cs", ".rb", ".go", ".rs", ".php", ".sh", ".ps1", ".sql", ".r", ".m",
            ".yml", ".yaml", ".toml", ".ini", ".cfg", ".md", ".txt", ".csv", ".tsv",
            ".ipynb", ".css", ".scss", ".less"
        )):
            return True
    try:
        with open(path, "rb") as f:
            chunk = f.read(sniff_bytes)
        return b"\x00" not in chunk
    except Exception:
        return False

def read_file_contents(path, text_encoding="utf-8"):
    if is_text_file(path):
        with open(path, "r", encoding=text_encoding, errors="replace") as f:
            return f.read(), "text"
    else:
        with open(path, "rb") as f:
            b = f.read()
        return base64.b64encode(b).decode("ascii"), "base64"

def build_xml(root_dir, output_xml, include_hidden=False, follow_symlinks=False, exclude_globs=None, max_bytes=None):
    root_dir = os.path.abspath(root_dir)
    if exclude_globs is None:
        exclude_globs = []

    root_elem = ET.Element("files")
    root_elem.set("root", root_dir)

    for dirpath, dirnames, filenames in os.walk(root_dir, followlinks=follow_symlinks):
        # Skip unwanted folders
        dirnames[:] = [d for d in dirnames if d not in {"__pycache__", "venv"}]

        # Optionally skip hidden folders
        if not include_hidden:
            dirnames[:] = [d for d in dirnames if not d.startswith(".")]
            filenames = [f for f in filenames if not f.startswith(".")]

        # Exclude by glob patterns
        def excluded(name):
            from fnmatch import fnmatch
            return any(fnmatch(name, pat) for pat in exclude_globs)

        dirnames[:] = [d for d in dirnames if not excluded(d)]
        filenames = [f for f in filenames if not excluded(f)]

        for fn in filenames:
            # Skip .sqlite3 files
            if fn.lower().endswith(".sqlite3"):
                continue

            full_path = os.path.join(dirpath, fn)
            relpath = os.path.relpath(full_path, root_dir).replace("\\", "/")

            # Skip the output file itself
            if os.path.abspath(full_path) == os.path.abspath(output_xml):
                continue

            # Print progress
            print(f"Processing: {relpath}")

            if max_bytes is not None:
                try:
                    if os.path.getsize(full_path) > max_bytes:
                        el = ET.SubElement(root_elem, "file", attrib={
                            "path": relpath,
                            "encoding": "skipped",
                            "reason": f"size_exceeds_{max_bytes}_bytes"
                        })
                        continue
                except OSError:
                    pass

            try:
                content, enc = read_file_contents(full_path)
            except Exception as e:
                el = ET.SubElement(root_elem, "file", attrib={
                    "path": relpath,
                    "encoding": "error"
                })
                el.text = f"Could not read file: {e}"
                continue

            el = ET.SubElement(root_elem, "file", attrib={
                "path": relpath,
                "encoding": enc
            })
            el.text = content

    tree = ET.ElementTree(root_elem)
    indent_xml(root_elem)
    os.makedirs(os.path.dirname(os.path.abspath(output_xml)), exist_ok=True)
    tree.write(output_xml, encoding="utf-8", xml_declaration=True)

def indent_xml(elem, level=0):
    i = "\n" + level * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        for child in elem:
            indent_xml(child, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

def main():
    parser = argparse.ArgumentParser(
        description="Recursively read files and write a single XML where each <file> element contains contents and a relative path attribute."
    )
    parser.add_argument("root", help="Root directory to scan")
    parser.add_argument("output", help="Path to output XML file")
    parser.add_argument("--include-hidden", action="store_true", help="Include hidden files and folders")
    parser.add_argument("--follow-symlinks", action="store_true", help="Follow symlinks")
    parser.add_argument("--exclude", action="append", default=[], help="Glob pattern to exclude, can be used multiple times")
    parser.add_argument("--max-bytes", type=int, default=None, help="Skip files larger than this many bytes")
    args = parser.parse_args()

    try:
        build_xml(
            root_dir=args.root,
            output_xml=args.output,
            include_hidden=args.include_hidden,
            follow_symlinks=args.follow_symlinks,
            exclude_globs=args.exclude,
            max_bytes=args.max_bytes
        )
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
