#!/usr/bin/env python3
"""Keep XNU CI errors readable; tee retains the complete log separately.

This filter never classifies build success. The shell's pipefail preserves the
actual build exit status, and the unfiltered log is uploaded even on failure.
"""
from collections import deque
import re
import sys

ANSI = re.compile(r'\x1b\[[0-?]*[ -/]*[@-~]')
ERROR = re.compile(r'\berror:|\bfatal error:|Undefined symbols|undefined reference|^ld:|^make(?:\[\d+\])?: \*\*\*|^clang(?:\+\+)?: error:')
PROGRESS = re.compile(r'\[info\]|\[warning\]|Applying patch:|Staged |^===|^Building |^XNU build|^Patch.*failed')


def main():
    before = deque(maxlen=4)
    following = errors = lines = 0
    for original in sys.stdin:
        line = ANSI.sub('',original.rstrip('\n'))
        lines += 1
        if ERROR.search(line):
            if not following:
                for previous in before:print(previous,flush=True)
            print(line,flush=True)
            errors += 1;following = 6;before.clear()
        elif following:
            print(line,flush=True);following -= 1
        elif PROGRESS.search(line):
            print(line,flush=True);before.clear()
        else:
            before.append(line)
    print(f'Build log: {lines} lines, {errors} diagnostic matches. See xnu-build-log artifact for complete output.',flush=True)


if __name__ == '__main__':main()
