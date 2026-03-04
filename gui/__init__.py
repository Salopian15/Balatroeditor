"""
Cross-platform GUI utilities for the Balatro Save Editor.
"""

import sys

IS_MAC = sys.platform == "darwin"
IS_LINUX = sys.platform.startswith("linux")


def bind_mousewheel(canvas):
    """Bind platform-appropriate mousewheel scrolling to a canvas widget.

    Handles the different event models:
    - macOS: <MouseWheel> with delta ±1
    - Windows: <MouseWheel> with delta ±120
    - Linux: <Button-4> / <Button-5>
    """
    def _on_mousewheel(event):
        if IS_MAC:
            canvas.yview_scroll(-1 * event.delta, "units")
        else:
            canvas.yview_scroll(-1 * (event.delta // 120), "units")

    def _on_linux_scroll_up(event):
        canvas.yview_scroll(-3, "units")

    def _on_linux_scroll_down(event):
        canvas.yview_scroll(3, "units")

    def _bind(event):
        if IS_LINUX:
            canvas.bind_all("<Button-4>", _on_linux_scroll_up)
            canvas.bind_all("<Button-5>", _on_linux_scroll_down)
        else:
            canvas.bind_all("<MouseWheel>", _on_mousewheel)

    def _unbind(event):
        if IS_LINUX:
            canvas.unbind_all("<Button-4>")
            canvas.unbind_all("<Button-5>")
        else:
            canvas.unbind_all("<MouseWheel>")

    canvas.bind("<Enter>", _bind)
    canvas.bind("<Leave>", _unbind)
