"""
Joker sprite loader — extracts individual joker images from the Balatro spritesheet.

The game stores joker art in a single spritesheet (Jokers.png) inside the
Balatro.love archive.  This module locates the archive, extracts the sheet,
and crops individual sprites keyed by joker_id.

Requires Pillow.  If Pillow is unavailable or the game files cannot be found,
all public functions degrade gracefully (return None).
"""

import os
import sys
import zipfile

try:
    from PIL import Image, ImageTk
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

from editor_model import _JOKER_CONFIGS

# Spritesheet grid constants (2x resolution)
_COLS = 10
_CELL_W = 142
_CELL_H = 190
_SHEET_PATH = "resources/textures/2x/Jokers.png"

# Cached data
_sprite_cache: dict = {}          # joker_id -> PIL.Image
_tk_image_cache: dict = {}        # (joker_id, width, height) -> ImageTk.PhotoImage
_sheet_image: "Image.Image | None" = None
_love_path: str | None = None


# ── Locating the game archive ──────────────────────────────────

def _default_love_paths() -> list[str]:
    """Return candidate paths for Balatro.love in priority order."""
    paths = []
    if sys.platform == "darwin":
        base = os.path.expanduser(
            "~/Library/Application Support/Steam/steamapps/common/Balatro"
        )
        paths.append(os.path.join(base, "Balatro.app", "Contents", "Resources", "Balatro.love"))
    elif sys.platform == "win32":
        for drive in ("C", "D", "E"):
            paths.append(
                os.path.join(f"{drive}:\\", "Program Files (x86)", "Steam",
                             "steamapps", "common", "Balatro", "Balatro.love")
            )
            paths.append(
                os.path.join(f"{drive}:\\", "Program Files", "Steam",
                             "steamapps", "common", "Balatro", "Balatro.love")
            )
    else:  # Linux
        home = os.path.expanduser("~")
        paths.append(os.path.join(home, ".steam", "steam", "steamapps", "common",
                                  "Balatro", "Balatro.love"))
        paths.append(os.path.join(home, ".local", "share", "Steam", "steamapps",
                                  "common", "Balatro", "Balatro.love"))
    return paths


def auto_detect_love_path() -> str | None:
    """Try to find Balatro.love automatically. Returns path or None."""
    for p in _default_love_paths():
        if os.path.isfile(p):
            return p
    return None


def set_love_path(path: str | None):
    """Manually set (or clear) the path to Balatro.love and reset caches."""
    global _love_path, _sheet_image
    _love_path = path
    _sheet_image = None
    _sprite_cache.clear()
    _tk_image_cache.clear()


def get_love_path() -> str | None:
    return _love_path


# ── Spritesheet loading ────────────────────────────────────────

def _load_sheet() -> "Image.Image | None":
    """Load the Jokers spritesheet from the .love archive. Cached."""
    global _sheet_image
    if _sheet_image is not None:
        return _sheet_image
    if not HAS_PIL or not _love_path or not os.path.isfile(_love_path):
        return None
    try:
        with zipfile.ZipFile(_love_path, "r") as zf:
            with zf.open(_SHEET_PATH) as f:
                _sheet_image = Image.open(f).copy()
        return _sheet_image
    except (KeyError, zipfile.BadZipFile, OSError):
        return None


def _get_sprite(joker_id: str) -> "Image.Image | None":
    """Crop a single joker sprite from the sheet. Cached by joker_id."""
    if joker_id in _sprite_cache:
        return _sprite_cache[joker_id]
    cfg = _JOKER_CONFIGS.get(joker_id)
    if cfg is None:
        return None
    sheet = _load_sheet()
    if sheet is None:
        return None
    order = cfg["order"]  # 1-indexed
    idx = order - 1
    col = idx % _COLS
    row = idx // _COLS
    x0 = col * _CELL_W
    y0 = row * _CELL_H
    sprite = sheet.crop((x0, y0, x0 + _CELL_W, y0 + _CELL_H))
    _sprite_cache[joker_id] = sprite
    return sprite


# ── Public API for tkinter ─────────────────────────────────────

def get_joker_tk_image(joker_id: str, width: int = 80, height: int = 107):
    """Return a tkinter-compatible PhotoImage for the given joker, or None.

    Results are cached; safe to call repeatedly for the same id+size.
    The caller must keep a reference to the returned object to prevent GC.
    """
    if not HAS_PIL:
        return None
    key = (joker_id, width, height)
    if key in _tk_image_cache:
        return _tk_image_cache[key]
    sprite = _get_sprite(joker_id)
    if sprite is None:
        return None
    resized = sprite.resize((width, height), Image.LANCZOS)
    tk_img = ImageTk.PhotoImage(resized)
    _tk_image_cache[key] = tk_img
    return tk_img


def is_available() -> bool:
    """Return True if sprites can be loaded (Pillow installed + love path set + sheet exists)."""
    return HAS_PIL and _love_path is not None and _load_sheet() is not None
