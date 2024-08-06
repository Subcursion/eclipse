import threading
import socket
import time
import logging

logger = logging.getLogger(__name__)


class __Connection(threading.Thread):
    def __init__(self, sock: socket.socket):
        super().__init__(daemon=False)

        self._socket = sock

    def run(self):
        logger.debug("Connection started")
        try:
            while True:
                data = self._socket.recv(1024)
                logger.debug("RECV: %s", data.decode())
        except:
            pass
        finally:
            self._socket.close()
            logger.debug("Connection closed")


def connectv4TCP(ip: str, port: int) -> __Connection:

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))

    conn = __Connection(sock)
    conn.start()
    return conn
