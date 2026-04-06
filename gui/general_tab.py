"""
General settings tab — money, hands, discards, max jokers, hand size, ante, round.
"""

import tkinter as tk
from tkinter import ttk
from editor_model import (
    get_dollars, set_dollars, get_hands, set_hands,
    get_discards, set_discards, get_max_jokers, set_max_jokers,
    get_hand_size, set_hand_size, get_ante, set_ante, get_round, set_round,
)

BG = "#0f0f23"
BG_PANEL = "#16213e"
FG = "#e0e0e0"
FG_DIM = "#aaaaaa"
ACCENT = "#27ae60"


class GeneralTab(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.fields = {}
        self._loading = False
        self._build()

    def _build(self):
        # Outer padding
        outer = ttk.Frame(self)
        outer.pack(fill="both", expand=True, padx=20, pady=15)

        # ── Run Resources ──
        res_frame = ttk.LabelFrame(outer, text="  Run Resources", padding=(20, 12))
        res_frame.pack(fill="x", pady=(0, 12))

        resource_fields = [
            ("Money ($)",      "dollars",   0, 999999, "Current gold — how much you have to spend at the shop"),
            ("Hands Left",     "hands",     1, 99,     "Hands remaining to play this round"),
            ("Discards Left",  "discards",  0, 99,     "Discards remaining this round"),
            ("Max Joker Slots","max_jokers", 0, 99,    "How many jokers you can carry at once"),
            ("Hand Size",      "hand_size", 1, 20,     "Cards dealt to your hand each round"),
        ]
        self._build_fields(res_frame, resource_fields)

        # ── Game Progress ──
        prog_frame = ttk.LabelFrame(outer, text="  Game Progress", padding=(20, 12))
        prog_frame.pack(fill="x")

        progress_fields = [
            ("Ante",  "ante",  1, 39,  "Current ante — higher antes have harder blinds"),
            ("Round", "round", 1, 999, "Round number within the current ante"),
        ]
        self._build_fields(prog_frame, progress_fields)

        # ── Hint ──
        hint = tk.Label(outer,
                        text="Changes are applied when you click  Save Changes  in the toolbar.",
                        bg=BG, fg="#555566", font=("Helvetica", 10), anchor="w")
        hint.pack(fill="x", pady=(14, 0))

    def _build_fields(self, parent, field_defs):
        for i, (label, key, lo, hi, tip) in enumerate(field_defs):
            row = tk.Frame(parent, bg=BG_PANEL if i % 2 == 0 else BG,
                           padx=10, pady=6)
            row.pack(fill="x")

            lbl = tk.Label(row, text=label, bg=row["bg"], fg=FG,
                           font=("Helvetica", 13), width=20, anchor="w")
            lbl.pack(side="left")

            var = tk.IntVar(value=0)
            var.trace_add("write", lambda *a: self._on_field_change())
            spin = ttk.Spinbox(row, from_=lo, to=hi, textvariable=var,
                               width=10, font=("Helvetica", 13))
            spin.pack(side="left", padx=(0, 12))

            tip_lbl = tk.Label(row, text=tip, bg=row["bg"], fg=FG_DIM,
                               font=("Helvetica", 10), anchor="w")
            tip_lbl.pack(side="left", fill="x", expand=True)

            self.fields[key] = var

    def _on_field_change(self):
        if not self._loading:
            self.app.mark_unsaved()

    def load_data(self, data):
        self._loading = True
        getters = {
            "dollars":    get_dollars,
            "hands":      get_hands,
            "discards":   get_discards,
            "max_jokers": get_max_jokers,
            "hand_size":  get_hand_size,
            "ante":       get_ante,
            "round":      get_round,
        }
        for key, getter in getters.items():
            try:
                self.fields[key].set(getter(data))
            except (KeyError, TypeError):
                pass
        self._loading = False

    def apply_data(self, data):
        setters = {
            "dollars":    set_dollars,
            "hands":      set_hands,
            "discards":   set_discards,
            "max_jokers": set_max_jokers,
            "hand_size":  set_hand_size,
            "ante":       set_ante,
            "round":      set_round,
        }
        for key, setter in setters.items():
            try:
                setter(data, self.fields[key].get())
            except (KeyError, TypeError):
                pass
