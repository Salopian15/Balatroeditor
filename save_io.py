"""
Save file I/O for Balatro .jkr files.

Handles DEFLATE decompression/compression and Lua parsing/serialization.
"""

import zlib
import shutil
import os
from lua_parser import parse_lua, serialize_save


SAVE_DIR = os.path.expanduser("~/Library/Application Support/Balatro")


def find_profiles():
    """Return list of profile directory paths found under the Balatro save dir."""
    profiles = []
    if not os.path.isdir(SAVE_DIR):
        return profiles
    for entry in sorted(os.listdir(SAVE_DIR)):
        path = os.path.join(SAVE_DIR, entry)
        if os.path.isdir(path) and os.path.exists(os.path.join(path, "save.jkr")):
            profiles.append(path)
    return profiles


def read_jkr(filepath):
    """Read a .jkr file → decompress → parse → return Python dict."""
    with open(filepath, 'rb') as f:
        compressed = f.read()
    try:
        text = zlib.decompress(compressed, -15).decode('utf-8')
    except zlib.error as e:
        raise IOError(f"Failed to decompress {filepath}: {e}")
    return parse_lua(text)


def write_jkr(filepath, data, backup=True):
    """Serialize Python dict → compress → write to .jkr file."""
    if backup and os.path.exists(filepath):
        bak = filepath + ".bak"
        shutil.copy2(filepath, bak)

    text = serialize_save(data)
    compressed = zlib.compress(text.encode('utf-8'), 9)[2:-4]  # Strip zlib header/trailer for raw deflate
    with open(filepath, 'wb') as f:
        f.write(compressed)


def read_save(profile_path):
    """Read save.jkr from a profile directory."""
    return read_jkr(os.path.join(profile_path, "save.jkr"))


def write_save(profile_path, data, backup=True):
    """Write save.jkr to a profile directory."""
    write_jkr(os.path.join(profile_path, "save.jkr"), data, backup=backup)
