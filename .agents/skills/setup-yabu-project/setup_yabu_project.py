#!/usr/bin/env python3
"""Set up a Yabu project template (bridge or tunnel) in game_data."""
import argparse
import json
import re
import sys
from pathlib import Path

TEXT_EXTENSIONS = {".lua", ".tl", ".json", ".html", ".txt", ".md"}
MOD_ID_TEMPLATE = "yourname_new_bridge"
NAME_KEY_TEMPLATE = "NEW_BRIDGE_NAME"
FILE_TEMPLATE = "new_bridge"
DISPLAY_TEMPLATE = "New Bridge"


def json_escape(value):
    return json.dumps(value, ensure_ascii=False)[1:-1]


def read(path):
    return path.read_text(encoding="utf-8", newline="")


def write(path, text):
    path.write_text(text, encoding="utf-8", newline="")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", default="game_data", help="path to game_data folder")
    p.add_argument("--mod-id", required=True)
    p.add_argument("--file-name", required=True, help="base file name, without extension")
    p.add_argument("--display-name", required=True)
    p.add_argument("--type", choices=["bridge", "tunnel"], required=True)
    a = p.parse_args()

    root = Path(a.root)
    if not root.is_dir():
        sys.exit(f"game_data folder not found: {root}")
    if not re.fullmatch(r"[a-z0-9_]+", a.mod_id):
        sys.exit("mod id must contain only lowercase letters, digits and underscores")
    if not re.fullmatch(r"[A-Za-z0-9_]+", a.file_name):
        sys.exit("file name must contain only letters, digits and underscores")

    infra = root / "content" / "infrastructure"
    folder = infra / "bridge"
    if not folder.is_dir():
        sys.exit(f"template folder not found: {folder}")

    upper = a.file_name.upper()
    files = [f for f in root.rglob("*") if f.is_file() and f.suffix.lower() in TEXT_EXTENSIONS]

    # Single pass per file so replacements never feed each other.
    for f in files:
        original = read(f)
        tokens = {MOD_ID_TEMPLATE: a.mod_id}
        name = f.name.lower()
        if name.endswith(".bridge.lua") or name == "strings.json":
            tokens[NAME_KEY_TEMPLATE] = upper + "_NAME"
        if name.endswith(".bridge.lua"):
            tokens[FILE_TEMPLATE] = a.file_name
        if name in ("strings.json", "modinfo.json"):
            tokens[DISPLAY_TEMPLATE] = json_escape(a.display_name)
        pattern = re.compile("|".join(re.escape(k) for k in sorted(tokens, key=len, reverse=True)))
        text = pattern.sub(lambda m: tokens[m.group(0)], original)
        if a.type == "tunnel":
            text = text.replace("/infrastructure/bridge", "/infrastructure/tunnel")
        if text != original:
            write(f, text)

    for suffix in (".bridge.lua", ".script.lua"):
        src = folder / (FILE_TEMPLATE + suffix)
        if src.exists():
            src.rename(folder / (a.file_name + suffix))

    if a.type == "tunnel":
        (folder / (a.file_name + ".bridge.lua")).rename(folder / (a.file_name + ".tunnel.lua"))
        folder.rename(infra / "tunnel")

    print(f"Yabu {a.type} project set up: mod id '{a.mod_id}', file '{a.file_name}', name '{a.display_name}'.")


if __name__ == "__main__":
    main()
