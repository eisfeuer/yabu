#!/usr/bin/env python3
"""Build a Yabu.addPartModel(...) function call from bounding box JSON.

Usage:
    python create_addpartmodel_call.py <model name> [--repo repo] [--json '<json>']

The bounding box JSON (output of the get-bounding-box-data skill) is read from
--json or, if omitted, from stdin. Prints the Lua call on stdout. Exits with
code 1 and a message on stderr on any error.
"""
import argparse
import json
import os
import sys


def fail(message):
    print(message, file=sys.stderr)
    sys.exit(1)


def format_number(value):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        fail("Bounding box value is not a number: %r" % (value,))
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return repr(value)


def read_vector(box, key):
    try:
        vector = box[key]
        return [format_number(vector[axis]) for axis in ("x", "y", "z")]
    except (KeyError, TypeError):
        fail("Missing or invalid '%s' (x, y, z) in bounding_box." % key)


def build_call(repo, model_file, json_text):
    try:
        box = json.loads(json_text)["bounding_box"]
    except (ValueError, KeyError, TypeError):
        fail("Input is not valid bounding box JSON with a 'bounding_box' object.")
    min_values = ", ".join(read_vector(box, "min"))
    max_values = ", ".join(read_vector(box, "max"))
    return (
        "Yabu.addPartModel(\n"
        "    %s,\n"
        '    "%s",\n'
        "    { { %s, }, { %s, } }\n"
        ")"
    ) % (repo, model_file, min_values, max_values)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("model", help="model name, with or without .mdl")
    parser.add_argument("--repo", default="repo", help="repository variable name")
    parser.add_argument("--json", dest="json_text", help="bounding box JSON")
    args = parser.parse_args()

    json_text = args.json_text if args.json_text is not None else sys.stdin.read()
    if not json_text.strip():
        fail("No bounding box JSON provided.")

    name = os.path.basename(args.model.strip())
    if not name.lower().endswith(".mdl"):
        name += ".mdl"

    print(build_call(args.repo, name, json_text))


if __name__ == "__main__":
    main()
