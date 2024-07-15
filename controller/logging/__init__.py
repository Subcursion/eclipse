from .. import term


def log_to_main_term(*args, **kargs):
    term.save_cursor_position()
    term.use_alternate_screen_buffer(False)
    print(*args, **kargs)
    term.use_alternate_screen_buffer()
    term.restore_cursor_position()
