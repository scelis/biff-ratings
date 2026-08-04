#!/usr/bin/env python3
"""Validate ratings.json.

Checks that the file parses, that each episode has the expected shape, and
that every rating name used by an episode is defined in rating_definitions.

Reports every problem it finds rather than stopping at the first one.
Exits 0 when the file is valid, 1 otherwise.
"""

import json
import re
import sys
from pathlib import Path

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def validate(path):
    errors = []

    try:
        raw = path.read_text()
    except OSError as e:
        return [f"could not read {path}: {e}"]

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        return [f"{path}: invalid JSON on line {e.lineno}, column {e.colno}: {e.msg}"]

    if not isinstance(data, dict):
        return [f"{path}: top level must be an object"]

    definitions = data.get("rating_definitions")
    if not isinstance(definitions, dict):
        errors.append("rating_definitions must be an object mapping rating name to number")
        definitions = {}
    else:
        for name, value in definitions.items():
            if not isinstance(value, (int, float)) or isinstance(value, bool):
                errors.append(f'rating_definitions["{name}"] must be a number, got {value!r}')

    episodes = data.get("ratings")
    if not isinstance(episodes, list):
        errors.append("ratings must be an array of episodes")
        return errors

    unknown = {}
    for i, ep in enumerate(episodes):
        where = f"ratings[{i}]"
        if not isinstance(ep, dict):
            errors.append(f"{where} must be an object")
            continue

        label = ep.get("media") if isinstance(ep.get("media"), str) else where

        if not isinstance(ep.get("episode"), int) or isinstance(ep.get("episode"), bool):
            errors.append(f"{where} ({label}): episode must be an integer")
        if not isinstance(ep.get("media"), str) or not ep.get("media"):
            errors.append(f"{where}: media must be a non-empty string")

        date = ep.get("date")
        if not isinstance(date, str) or not DATE_RE.match(date):
            errors.append(f"{where} ({label}): date must be a YYYY-MM-DD string, got {date!r}")

        host_ratings = ep.get("ratings")
        if not isinstance(host_ratings, dict):
            errors.append(f"{where} ({label}): ratings must be an object")
            continue

        for host, name in host_ratings.items():
            if name is None:
                continue
            if not isinstance(name, str):
                errors.append(f'{where} ({label}): ratings["{host}"] must be a string or null, got {name!r}')
            elif name not in definitions:
                unknown.setdefault(name, []).append(f"{label} ({host})")

    for name in sorted(unknown):
        users = ", ".join(unknown[name])
        errors.append(f'undefined rating "{name}" used by: {users}')

    return errors


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / "ratings.json"

    errors = validate(path)
    if errors:
        print(f"{path}: {len(errors)} problem(s) found\n", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    print(f"{path} is valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
