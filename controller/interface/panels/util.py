from controller.types import Rect

from controller import term


def draw_frame(rect: Rect, title: str | None = None):
    title = f" {title} "
    dashes_before = (rect.width - 2) // 8
    dashes_after = (rect.width - 2 - dashes_before) - len(title)

    term.print_raw("┌" + ("─" * dashes_before) + title + ("─" * dashes_after) + "┐")
    for i in range(rect.height - 2):
        term.move_cursor(term.CursorDirection.Down)
        term.set_cursor_column(rect.x)
        term.print_raw("│")
        term.set_cursor_column(rect.x + rect.width - 1)
        term.print_raw("│")
    term.move_cursor(term.CursorDirection.Down)
    term.set_cursor_column(rect.x)
    term.print_raw("└" + ("─" * (rect.width - 2)) + "┘")
    term.set_cursor_position(rect.y + 1, rect.x + 1)
