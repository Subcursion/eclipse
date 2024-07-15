from traceback import format_exc

from . import term
from .interface import show_interface

# parse env args and command line flags

# start interface loop
try:
    show_interface()
except Exception as e:
    term.set_cursor_visible(True)
    term.erase_display(term.EraseMode.All)
    term.use_alternate_screen_buffer(False)
    format_exc(e)
