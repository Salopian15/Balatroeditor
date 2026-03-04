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


class GeneralTab(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.fields = {}
        self._loading = False
        self._build()

    def _build(self):
        header = ttk.Label(self, text="General Settings", font=("Helvetica", 16, "bold"))
        header.pack(pady=(15, 10))

        container = ttk.Frame(self)
        container.pack(padx=30, pady=10, fill="x")

        field_defs = [
            ("Money ($)", "dollars", 0, 999999),
            ("Hands Left", "hands", 1, 99),
            ("Discards Left", "discards", 0, 99),
            ("Max Joker Slots", "max_jokers", 0, 99),
            ("Hand Size", "hand_size", 1, 20),
            ("Ante", "ante", 1, 39),
            ("Round", "round", 1, 999),
        ]

        for i, (label, key, lo, hi) in enumerate(field_defs):
            row = ttk.Frame(container)
            row.pack(fill="x", pady=4)

            lbl = ttk.Label(row, text=label, width=20, anchor="w",
                            font=("Helvetica", 13))
            lbl.pack(side="left", padx=(0, 10))

            var = tk.IntVar(value=0)
            var.trace_add("write", lambda *a: self._on_field_change())
            spin = ttk.Spinbox(row, from_=lo, to=hi, textvariable=var,
                               width=10, font=("Helvetica", 13))
            spin.pack(side="left")

            self.fields[key] = var

    def _on_field_change(self):
        if not self._loading:
            self.app.mark_unsaved()

    def load_data(self, data):
        self._loading = True
        getters = {
            "dollars": get_dollars,
            "hands": get_hands,
            "discards": get_discards,
            "max_jokers": get_max_jokers,
            "hand_size": get_hand_size,
            "ante": get_ante,
            "round": get_round,
        }
        for key, getter in getters.items():
            try:
                self.fields[key].set(getter(data))
            except (KeyError, TypeError):
                pass
        self._loading = False

    def apply_data(self, data):
        setters = {
            "dollars": set_dollars,
            "hands": set_hands,
            "discards": set_discards,
            "max_jokers": set_max_jokers,
            "hand_size": set_hand_size,
            "ante": set_ante,
            "round": set_round,
        }
        for key, setter in setters.items():
            try:
                setter(data, self.fields[key].get())
            except (KeyError, TypeError):
                pass
