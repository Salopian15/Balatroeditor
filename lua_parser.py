"""
Lua table literal parser and serializer.

Parses the Balatro save format (Lua 'return { ... }' table literals)
into Python dicts/lists, and serializes back.
"""

import re


class LuaParseError(Exception):
    pass


class LuaParser:
    """Parse a Lua table literal string into Python objects."""

    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.length = len(text)

    def _skip_ws(self):
        while self.pos < self.length and self.text[self.pos] in ' \t\r\n':
            self.pos += 1

    def _peek(self):
        if self.pos < self.length:
            return self.text[self.pos]
        return None

    def _expect(self, ch):
        self._skip_ws()
        if self.pos >= self.length or self.text[self.pos] != ch:
            got = self.text[self.pos] if self.pos < self.length else 'EOF'
            raise LuaParseError(
                f"Expected '{ch}' at pos {self.pos}, got '{got}'"
            )
        self.pos += 1

    def _match_str(self, s):
        self._skip_ws()
        if self.text[self.pos:self.pos + len(s)] == s:
            self.pos += len(s)
            return True
        return False

    def parse(self):
        self._skip_ws()
        # Strip optional 'return' keyword
        if self.text[self.pos:self.pos + 6] == 'return':
            self.pos += 6
        self._skip_ws()
        result = self._parse_value()
        return result

    def _parse_value(self):
        self._skip_ws()
        ch = self._peek()
        if ch is None:
            raise LuaParseError("Unexpected end of input")
        if ch == '{':
            return self._parse_table()
        if ch == '"':
            return self._parse_string()
        if ch == '-' or ch.isdigit():
            return self._parse_number()
        # Keywords
        if self.text[self.pos:self.pos + 4] == 'true':
            self.pos += 4
            return True
        if self.text[self.pos:self.pos + 5] == 'false':
            self.pos += 5
            return False
        if self.text[self.pos:self.pos + 3] == 'nil':
            self.pos += 3
            return None
        # Try to read as unquoted identifier (shouldn't normally happen in saves)
        raise LuaParseError(
            f"Unexpected char '{ch}' at pos {self.pos}: "
            f"...{self.text[max(0,self.pos-20):self.pos+20]}..."
        )

    def _parse_string(self):
        self._expect('"')
        parts = []
        while self.pos < self.length:
            ch = self.text[self.pos]
            if ch == '\\':
                self.pos += 1
                esc = self.text[self.pos]
                if esc == 'n':
                    parts.append('\n')
                elif esc == 't':
                    parts.append('\t')
                elif esc == '\\':
                    parts.append('\\')
                elif esc == '"':
                    parts.append('"')
                else:
                    parts.append(esc)
                self.pos += 1
            elif ch == '"':
                self.pos += 1
                return ''.join(parts)
            else:
                parts.append(ch)
                self.pos += 1
        raise LuaParseError("Unterminated string")

    def _parse_number(self):
        self._skip_ws()
        start = self.pos
        if self.text[self.pos] == '-':
            self.pos += 1
        while self.pos < self.length and (self.text[self.pos].isdigit() or self.text[self.pos] == '.'):
            self.pos += 1
        # Scientific notation
        if self.pos < self.length and self.text[self.pos] in ('e', 'E'):
            self.pos += 1
            if self.pos < self.length and self.text[self.pos] in ('+', '-'):
                self.pos += 1
            while self.pos < self.length and self.text[self.pos].isdigit():
                self.pos += 1
        num_str = self.text[start:self.pos]
        if '.' in num_str or 'e' in num_str or 'E' in num_str:
            return float(num_str)
        return int(num_str)

    def _parse_table(self):
        self._expect('{')
        self._skip_ws()

        entries = []
        has_string_keys = False
        has_int_keys = False
        max_int_key = 0

        while self._peek() != '}':
            self._skip_ws()
            if self._peek() == '}':
                break

            # Check for keyed entry: ["key"]= or [N]=
            if self._peek() == '[':
                saved_pos = self.pos
                self.pos += 1
                self._skip_ws()
                if self._peek() == '"':
                    # String key: ["key"]=value
                    key = self._parse_string()
                    self._expect(']')
                    self._expect('=')
                    val = self._parse_value()
                    entries.append((key, val))
                    has_string_keys = True
                else:
                    # Numeric key: [N]=value
                    key = self._parse_number()
                    self._expect(']')
                    self._expect('=')
                    val = self._parse_value()
                    entries.append((int(key), val))
                    has_int_keys = True
                    max_int_key = max(max_int_key, int(key))
            else:
                # Bare value (positional)
                val = self._parse_value()
                has_int_keys = True
                max_int_key += 1
                entries.append((max_int_key, val))

            self._skip_ws()
            if self._peek() == ',':
                self.pos += 1

        self._expect('}')

        # If all keys are sequential ints 1..N, return a list
        if has_int_keys and not has_string_keys:
            int_keys = sorted([k for k, v in entries])
            if int_keys == list(range(1, len(int_keys) + 1)):
                result = [None] * len(entries)
                for k, v in entries:
                    result[k - 1] = v
                return result

        # Otherwise return a dict (preserving int keys as-is for mixed tables)
        result = {}
        for k, v in entries:
            result[k] = v
        return result


def parse_lua(text):
    """Parse a Lua table literal string into Python objects."""
    parser = LuaParser(text)
    return parser.parse()


def serialize_lua(obj, indent=0):
    """Serialize a Python object back to a Lua table literal string."""
    if obj is None:
        return "nil"
    if isinstance(obj, bool):
        return "true" if obj else "false"
    if isinstance(obj, int):
        return str(obj)
    if isinstance(obj, float):
        # Preserve Lua's number formatting
        if obj == int(obj) and abs(obj) < 1e15:
            # Check if original had decimal — keep as float representation
            s = repr(obj)
            return s
        return repr(obj)
    if isinstance(obj, str):
        escaped = obj.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n').replace('\t', '\\t')
        return f'"{escaped}"'
    if isinstance(obj, list):
        if not obj:
            return "{}"
        parts = []
        for i, v in enumerate(obj):
            parts.append(f"[{i + 1}]={serialize_lua(v, indent + 1)},")
        return "{" + "".join(parts) + "}"
    if isinstance(obj, dict):
        if not obj:
            return "{}"
        parts = []
        for k, v in obj.items():
            if isinstance(k, int):
                parts.append(f"[{k}]={serialize_lua(v, indent + 1)},")
            else:
                parts.append(f'["{k}"]={serialize_lua(v, indent + 1)},')
        return "{" + "".join(parts) + "}"
    raise TypeError(f"Cannot serialize type {type(obj)}")


def serialize_save(obj):
    """Serialize a save data object with the 'return' prefix."""
    return "return " + serialize_lua(obj)
