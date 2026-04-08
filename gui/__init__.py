"""
Cross-platform GUI utilities for the Balatro Save Editor.
"""

import sys

IS_MAC = sys.platform == "darwin"
IS_LINUX = sys.platform.startswith("linux")


def bind_mousewheel(canvas, horizontal=False):
    """Bind platform-appropriate mousewheel scrolling to a canvas widget.

    Handles the different event models:
    - macOS: <MouseWheel> with delta ±1
    - Windows: <MouseWheel> with delta ±120
    - Linux: <Button-4> / <Button-5> (vertical), <Button-6> / <Button-7> (horizontal)

    Args:
        canvas: Canvas-like widget exposing xview_scroll/yview_scroll.
        horizontal: If True, bind horizontal scrolling gestures.
    """
    def _on_mousewheel(event):
        view = canvas.xview_scroll if horizontal else canvas.yview_scroll
        if IS_MAC:
            view(-1 * event.delta, "units")
        else:
            view(-1 * (event.delta // 120), "units")

    def _on_linux_scroll_up(event):
        view = canvas.xview_scroll if horizontal else canvas.yview_scroll
        view(-3, "units")

    def _on_linux_scroll_down(event):
        view = canvas.xview_scroll if horizontal else canvas.yview_scroll
        view(3, "units")

    def _bind(event):
        if IS_LINUX:
            up_event = "<Button-6>" if horizontal else "<Button-4>"
            down_event = "<Button-7>" if horizontal else "<Button-5>"
            canvas.bind_all(up_event, _on_linux_scroll_up)
            canvas.bind_all(down_event, _on_linux_scroll_down)
        else:
            event_name = "<Shift-MouseWheel>" if horizontal else "<MouseWheel>"
            canvas.bind_all(event_name, _on_mousewheel)

    def _unbind(event):
        if IS_LINUX:
            up_event = "<Button-6>" if horizontal else "<Button-4>"
            down_event = "<Button-7>" if horizontal else "<Button-5>"
            canvas.unbind_all(up_event)
            canvas.unbind_all(down_event)
        else:
            event_name = "<Shift-MouseWheel>" if horizontal else "<MouseWheel>"
            canvas.unbind_all(event_name)

    canvas.bind("<Enter>", _bind)
    canvas.bind("<Leave>", _unbind)


def bind_mousewheel_horizontal(canvas):
    """Bind platform-appropriate horizontal mousewheel scrolling to a canvas.

    Triggers on Shift+scroll (macOS/Windows) or Shift+Button-4/5 (Linux).
    On macOS, trackpad horizontal swipes also send <Shift-MouseWheel>.
    """
    def _on_shift_mousewheel(event):
        if IS_MAC:
            canvas.xview_scroll(-1 * event.delta, "units")
        else:
            canvas.xview_scroll(-1 * (event.delta // 120), "units")

    def _on_linux_scroll_left(event):
        canvas.xview_scroll(-3, "units")

    def _on_linux_scroll_right(event):
        canvas.xview_scroll(3, "units")

    def _bind(event):
        if IS_LINUX:
            canvas.bind_all("<Shift-Button-4>", _on_linux_scroll_left)
            canvas.bind_all("<Shift-Button-5>", _on_linux_scroll_right)
        else:
            canvas.bind_all("<Shift-MouseWheel>", _on_shift_mousewheel)

    def _unbind(event):
        if IS_LINUX:
            canvas.unbind_all("<Shift-Button-4>")
            canvas.unbind_all("<Shift-Button-5>")
        else:
            canvas.unbind_all("<Shift-MouseWheel>")

    canvas.bind("<Enter>", _bind)
    canvas.bind("<Leave>", _unbind)
