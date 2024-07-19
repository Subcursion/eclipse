import select
import signal
import sys
import termios
import tty


def getch():
    c = sys.stdin.read(1)
    return c


def getch_select():
    c = None
    rlist, _, xlist = select.select([sys.stdin], [], [sys.stdin])
    for fd in rlist:
        print(fd, "is ready for reading")
        c = fd.read(1)
    for fd in xlist:
        print(fd, "had an error")
    return c


def getch_poll():
    c = None
    p = select.poll()
    p.register(sys.stdin.fileno(), select.POLLIN)

    res = p.poll()
    for fd, event in res:
        print(fd, "had event", event)
        c = sys.stdin.read(1)
        print("read", c, ord(c), "from", fd)
    return c


def getch_epoll():
    c = None
    ep = select.epoll()
    ep.register(sys.stdin.fileno(), select.EPOLLIN)

    res = ep.poll()
    for fd, event in res:
        print(fd, "had event", event)
        c = sys.stdin.read(1)
        print("read", c, ord(c), "from", fd)
    return c


def handle_sigwinc(signum, frame):
    ws_row, ws_col = termios.tcgetwinsize(sys.stdin.fileno())
    print("signal: rows", ws_row, "cols", ws_col)


old_settings = termios.tcgetattr(sys.stdin.fileno())
tty.setcbreak(sys.stdin.fileno(), when=termios.TCSANOW)

signal.signal(signal.SIGWINCH, handle_sigwinc)

print("Signal registered; getting cursor position")

print(chr(0x1B), "[6n", end="", sep="", flush=True)

print("Requested, setting c break")

ws_row, ws_col = termios.tcgetwinsize(sys.stdin.fileno())

print("rows", ws_row, "cols", ws_col)

termios.tcsetwinsize(sys.stdin.fileno(), (30, 30))

print("entering main c loop")
while True:
    try:
        c = getch_select()
        print(f"{c} ({ord(c)}) was pressed!", flush=True)
    except KeyboardInterrupt:
        break

termios.tcsetattr(sys.stdin.fileno(), termios.TCSANOW, old_settings)
