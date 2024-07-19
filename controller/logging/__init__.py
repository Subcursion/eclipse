import sys


def elog(*args, **kargs):
    file = kargs.pop("file", sys.stderr)
    print(*args, **kargs, file=file)
