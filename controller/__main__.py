from traceback import format_exc

from . import term
from .logging import elog
from .interface import interface
from .term.input import input_thread

# parse env args and command line flags

# start interface loop
try:
    input_thread.start()
    interface.setup_screen()
    interface.render()
except Exception as e:
    elog("There was an error during runtime.")
    elog(format_exc(e))
except KeyboardInterrupt:
    elog("Received ctrl+c")
finally:
    interface.restore_screen()
