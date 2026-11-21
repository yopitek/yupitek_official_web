#!/usr/bin/env python3
"""Fail if `hugo` reports an ERROR, even when it still exits 0.

A malformed file under data/ makes Hugo log
  ERROR error building site: failed to load data: ...
and then carry on with an empty data map, so every page that reads site data silently loses
content while the build "succeeds". `--quiet` hides the line entirely. This check runs the real
build command and fails on any ERROR line.
Usage (repo root): python3 scripts/qa/hugo_build_check.py [extra hugo args]
"""
import subprocess
import sys
import tempfile

IGNORED = ("deprecated:",)


def main() -> int:
    with tempfile.TemporaryDirectory() as out:
        proc = subprocess.run(
            ["hugo", "--minify", "--gc", "--cleanDestinationDir", "--buildFuture", "-d", out, *sys.argv[1:]],
            capture_output=True, text=True,
        )
    lines = (proc.stdout + proc.stderr).splitlines()
    errors = [l for l in lines if "ERROR" in l and not any(i in l for i in IGNORED)]
    for line in errors:
        print(line.strip())
    print(f"hugo exit={proc.returncode}, {len(errors)} ERROR line(s)")
    return 1 if errors or proc.returncode != 0 else 0


if __name__ == "__main__":
    sys.exit(main())
