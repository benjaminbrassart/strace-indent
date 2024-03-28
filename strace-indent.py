#!/usr/bin/env python3

import sys

assert sys.version_info >= (3, 3), "Please upgrade to Python >= 3.3"

import os

INDENT_STRING = os.environ.get("INDENT_STRING", ">---")

if os.isatty(2):
    COLOR_INDENT = "\N{esc}[2;31m"
    COLOR_RESET = "\N{esc}[0m"
else:
    COLOR_INDENT = ""
    COLOR_RESET = ""

def indent_string(level: int) -> str:
    if level <= 0:
        return ""

    s = COLOR_INDENT + level * INDENT_STRING + COLOR_RESET
    if not INDENT_STRING.endswith(" "):
        s += " "

    return s

def indent_line(line: str) -> str:
    new_line = ""
    indent_level = 0

    if line.startswith("+++") and line.endswith("+++"):
        return line

    it = iter(line)

    while True:
        c = next(it, None)
        if c == None:
            break

        if c in "[{(":
            indent_level += 1
            new_line += c
            new_line += "\n" + indent_string(indent_level)
        elif c in "]})":
            indent_level -= 1
            new_line += "\n" + indent_string(indent_level)
            new_line += c
        elif c == ",":
            new_line += c
            new_line += "\n" + indent_string(indent_level)
        elif c == " ":
            continue
        elif c == "=":
            new_line += " = "
        elif c == "\"":
            new_line += c
            while True:
                c = next(it, "\"")

                new_line += c
                if c == "\"":
                    break
        else:
            new_line += c

    return new_line

def main() -> int:
    import shutil
    import subprocess
    import sys
    import tempfile

    sys.stdout = sys.stderr

    def create_fifo() -> tuple[str, str]:
        tmp_dir = tempfile.mkdtemp(prefix="strace-indent-")
        fifo_path = os.path.join(tmp_dir, "strace-output.fifo")

        os.mkfifo(fifo_path)
        return [fifo_path, tmp_dir]

    (fifo_path, tmp_dir) = create_fifo()
    try:
        args = sys.argv[1:]
        child = subprocess.Popen(["strace", "-o", fifo_path] + args)

        first_line = True
        with open(fifo_path, "r") as fifo:
            while True:
                line = fifo.readline()

                if line is None or len(line) == 0:
                    break

                line = line[:-1]

                if not first_line:
                    print()
                first_line = False

                print(indent_line(line))

        return child.wait()
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)

if __name__ == "__main__":
    exit(main())
