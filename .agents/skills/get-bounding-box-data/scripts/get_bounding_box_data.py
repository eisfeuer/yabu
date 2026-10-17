#!/usr/bin/env python3
"""Read the bounding box of a Transport Fever 3 model (.mdl) in the current project.

Usage: python get_bounding_box_data.py <model name> [--root <project dir>]

Prints JSON on stdout. Exits with code 1 and a message on stderr on any error.
"""
import argparse
import json
import os
import re
import sys

NUMBER = r"[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?"
VECTOR = r"\{\s*(%s)\s*,\s*(%s)\s*,\s*(%s)\s*,?\s*\}" % (NUMBER, NUMBER, NUMBER)
BOUNDING_INFO = re.compile(r"boundingInfo\s*=\s*\{(.*?)\}\s*,?\s*\}", re.DOTALL)
BB_MAX = re.compile(r"bbMax\s*=\s*" + VECTOR)
BB_MIN = re.compile(r"bbMin\s*=\s*" + VECTOR)
SKIP_DIRS = {".git", "node_modules", ".vscode", "__pycache__"}


def fail(message):
    print(message, file=sys.stderr)
    sys.exit(1)


def to_number(text):
    value = float(text)
    return int(value) if value.is_integer() else value


def find_models(root, filename):
    wanted = filename.lower()
    found = []
    for current, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for name in files:
            if name.lower() == wanted:
                found.append(os.path.join(current, name))
    return sorted(found)


def read_bounding_box(path):
    with open(path, "r", encoding="utf-8", errors="replace") as handle:
        text = handle.read()
    section = BOUNDING_INFO.search(text)
    if not section:
        fail("No boundingInfo section found in %s" % path)
    body = section.group(0)
    max_match = BB_MAX.search(body)
    min_match = BB_MIN.search(body)
    if not max_match or not min_match:
        fail("bbMin/bbMax with three numbers not found in %s" % path)
    min_x, min_y, min_z = (to_number(v) for v in min_match.groups())
    max_x, max_y, max_z = (to_number(v) for v in max_match.groups())
    return {
        "bounding_box": {
            "min": {"x": min_x, "y": min_y, "z": min_z},
            "max": {"x": max_x, "y": max_y, "z": max_z},
        }
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("model", help="model name, with or without .mdl")
    parser.add_argument("--root", default=os.getcwd(), help="project directory")
    args = parser.parse_args()

    name = os.path.basename(args.model.strip())
    if not name.lower().endswith(".mdl"):
        name += ".mdl"

    matches = find_models(os.path.abspath(args.root), name)
    if not matches:
        fail("Model file '%s' was not found in the project." % name)
    if len(matches) > 1:
        fail("Multiple files named '%s' found:\n%s" % (name, "\n".join(matches)))

    print(json.dumps(read_bounding_box(matches[0]), indent=4))


if __name__ == "__main__":
    main()
