"""
Consumable editor tab — view, add, and remove Tarot, Planet, and Spectral cards.
Supports edition selection and live search filtering.
"""

import tkinter as tk
from tkinter import ttk
from editor_model import get_consumables, remove_consumable, add_consumable
from game_data import EDITIONS, EDITION_COLOURS, edition_name_to_id
from gui import bind_mousewheel

TAROTS = [
    ("c_fool", "The Fool"), ("c_magician", "The Magician"), ("c_high_priestess", "The High Priestess"),
    ("c_empress", "The Empress"), ("c_emperor", "The Emperor"), ("c_heirophant", "The Hierophant"),
    ("c_lovers", "The Lovers"), ("c_chariot", "The Chariot"), ("c_justice", "Justice"),
    ("c_hermit", "The Hermit"), ("c_wheel_of_fortune", "The Wheel of Fortune"), ("c_strength", "Strength"),
    ("c_hanged_man", "The Hanged Man"), ("c_death", "Death"), ("c_temperance", "Temperance"),
    ("c_devil", "The Devil"), ("c_tower", "The Tower"), ("c_star", "The Star"),
    ("c_moon", "The Moon"), ("c_sun", "The Sun"), ("c_judgement", "Judgement"), ("c_world", "The World")
]

PLANETS = [
    ("c_mercury", "Mercury"), ("c_venus", "Venus"), ("c_earth", "Earth"),
    ("c_mars", "Mars"), ("c_jupiter", "Jupiter"), ("c_saturn", "Saturn"),
    ("c_uranus", "Uranus"), ("c_neptune", "Neptune"), ("c_pluto", "Pluto"),
    ("c_planet_x", "Planet X"), ("c_ceres", "Ceres"), ("c_eris", "Eris")
]

SPECTRALS = [
    ("c_familiar", "Familiar"), ("c_grim", "Grim"), ("c_incantation", "Incantation"),
    ("c_talisman", "Talisman"), ("c_aura", "Aura"), ("c_wraith", "Wraith"),
    ("c_sigil", "Sigil"), ("c_ouija", "Ouija"), ("c_ectoplasm", "Ectoplasm"),
    ("c_immolate", "Immolate"), ("c_ankh", "Ankh"), ("c_deja_vu", "Deja Vu"),
    ("c_hex", "Hex"), ("c_trance", "Trance"), ("c_medium", "Medium"),
    ("c_cryptid", "Cryptid"), ("c_soul", "The Soul"), ("c_black_hole", "Black Hole")
]

# All consumable groups in display order: (header_label, bg_colour, items_list)
CONSUMABLE_GROUPS = [
    ("  Tarot Cards  ",   "#8e44ad", TAROTS),
    ("  Planet Cards  ",  "#2980b9", PLANETS),
    ("  Spectral Cards  ","#c0392b", SPECTRALS),
]

# Flat lookup: center_id → display_name
_ALL_CONSUMABLES = {cid: cname for _, _, items in CONSUMABLE_GROUPS for cid, cname in items}


class ConsumableTab(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.data = None
        self.selected_indices = set()
        self._build()

    def _build(self):
        # ── Current consumables ──
        top = ttk.LabelFrame(self, text="  Current Consumables", padding=10)
        top.pack(fill="both", expand=True, padx=10, pady=(10, 5))

        self.canvas = tk.Canvas(top, height=140, bg="#1a1a2e", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.inner = tk.Frame(self.canvas, bg="#1a1a2e")
        self.canvas.create_window((0, 0), window=self.inner, anchor="nw")
        self.inner.bind("<Configure>", lambda e: self.canvas.configure(
            scrollregion=self.canvas.bbox("all")))
        bind_mousewheel(self.canvas)

        # ── Controls row: remove button ──
        mid = ttk.Frame(self)
        mid.pack(fill="x", padx=10, pady=5)
        ttk.Button(mid, text="Remove Selected", command=self._remove_selected).pack(side="right", padx=5)

        # ── Add consumables picker ──
        bot = ttk.LabelFrame(self, text="  Add Consumable", padding=10)
        bot.pack(fill="both", expand=True, padx=10, pady=(5, 10))

        # Search + edition row
        search_row = ttk.Frame(bot)
        search_row.pack(fill="x", pady=(0, 5))

        ttk.Label(search_row, text="Search:").pack(side="left", padx=(0, 5))
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self._filter_picker)
        ttk.Entry(search_row, textvariable=self.search_var, width=25).pack(side="left")

        ttk.Label(search_row, text="  Edition:").pack(side="left", padx=(10, 5))
        self.new_edition_var = tk.StringVar(value="None")
        ttk.Combobox(
            search_row, textvariable=self.new_edition_var,
            values=[e[1] for e in EDITIONS], state="readonly", width=15,
        ).pack(side="left", padx=5)

        # Scrollable picker grid
        picker_container = ttk.Frame(bot)
        picker_container.pack(fill="both", expand=True)

        self.picker_canvas = tk.Canvas(picker_container, bg="#16213e", highlightthickness=0)
        picker_sb = ttk.Scrollbar(picker_container, orient="vertical",
                                  command=self.picker_canvas.yview)
        self.picker_canvas.configure(yscrollcommand=picker_sb.set)
        picker_sb.pack(side="right", fill="y")
        self.picker_canvas.pack(side="left", fill="both", expand=True)

        self.picker_inner = tk.Frame(self.picker_canvas, bg="#16213e")
        self.picker_canvas.create_window((0, 0), window=self.picker_inner, anchor="nw")
        self.picker_inner.bind("<Configure>", lambda e: self.picker_canvas.configure(
            scrollregion=self.picker_canvas.bbox("all")))
        bind_mousewheel(self.picker_canvas)

        self._populate_picker()

    def _populate_picker(self, filter_text=""):
        """Rebuild the picker grid, optionally filtering by text."""
        for w in self.picker_inner.winfo_children():
            w.destroy()

        filter_text = filter_text.lower()
        current_row = 0

        for header, hdr_bg, items in CONSUMABLE_GROUPS:
            filtered = [(cid, cname) for cid, cname in items
                        if filter_text in cname.lower() or filter_text in cid.lower()]
            if not filtered:
                continue

            hdr = tk.Label(self.picker_inner, text=header, bg=hdr_bg, fg="white",
                           font=("Helvetica", 11, "bold"), padx=6, pady=2)
            hdr.grid(row=current_row, column=0, columnspan=6, sticky="w",
                     pady=(8, 4), padx=4)
            current_row += 1

            col = 0
            for cid, cname in filtered:
                btn = tk.Button(
                    self.picker_inner, text=cname,
                    bg="#0f3460", fg="white", activebackground="#1a508b",
                    activeforeground="white", relief="raised", bd=1,
                    font=("Helvetica", 10), padx=8, pady=4, width=16,
                    cursor="hand2",
                    command=lambda c=cid: self._add_consumable(c),
                )
                btn.grid(row=current_row, column=col, padx=3, pady=2, sticky="w")
                col += 1
                if col >= 4:
                    col = 0
                    current_row += 1
            if col > 0:
                current_row += 1

    def _filter_picker(self, *args):
        self._populate_picker(self.search_var.get())

    def load_data(self, data):
        self.data = data
        self.selected_indices = set()
        self._refresh()

    def apply_data(self, data):
        pass

    def _refresh(self):
        for w in self.inner.winfo_children():
            w.destroy()

        if not self.data:
            return

        cons = get_consumables(self.data)
        for i, c in enumerate(cons):
            sf = c.get("save_fields", {})
            center = sf.get("center", "unknown")
            edition_key = sf.get("edition", {}).get("type", "base") if isinstance(sf.get("edition"), dict) else "base"

            is_selected = i in getattr(self, "selected_indices", set())
            ed_colour = EDITION_COLOURS.get(edition_key)
            border_color = "#f39c12" if is_selected else (ed_colour or "#333")
            bg_color = "#3d3d6e" if is_selected else "#2d2d4e"

            card = tk.Frame(self.inner, bg=border_color, padx=2, pady=2)
            card.pack(side="left", padx=5, pady=5)

            inner_c = tk.Frame(card, bg=bg_color, width=80, height=110)
            inner_c.pack_propagate(False)
            inner_c.pack()

            # Edition strip at top
            if ed_colour:
                tk.Frame(inner_c, bg=ed_colour, height=4).pack(fill="x")

            display_name = _ALL_CONSUMABLES.get(center, center.replace("c_", "").capitalize())

            lbl = tk.Label(inner_c, text=display_name, bg=bg_color, fg="white",
                           font=("Helvetica", 10, "bold"), wraplength=70)
            lbl.pack(expand=True)

            # Edition badge
            if edition_key != "base":
                from game_data import EDITION_MAP
                ed_display = EDITION_MAP.get(edition_key, "")
                badge_fg = "white" if edition_key != "foil" else "#1a1a2e"
                tk.Label(inner_c, text=ed_display, bg=ed_colour or "#555",
                         fg=badge_fg, font=("Helvetica", 8, "bold"),
                         padx=3, pady=0).pack(pady=(0, 2))

            for w in [card, inner_c, lbl]:
                w.bind("<Button-1>", lambda e, idx=i: self._toggle_selection(idx, e))

    def _remove_selected(self):
        if not self.data or not getattr(self, "selected_indices", None):
            return
        indices = sorted(list(self.selected_indices), reverse=True)
        for idx in indices:
            remove_consumable(self.data, idx)
        self.app.mark_unsaved()
        self.selected_indices.clear()
        self._refresh()

    def _toggle_selection(self, idx, event=None):
        if event and (event.state & 0x0004 or event.state & 0x0001):
            if idx in self.selected_indices:
                self.selected_indices.remove(idx)
            else:
                self.selected_indices.add(idx)
        else:
            if idx in self.selected_indices and len(self.selected_indices) == 1:
                self.selected_indices.clear()
            else:
                self.selected_indices = {idx}
        self._refresh()

    def _add_consumable(self, cid):
        if not self.data:
            return
        ed_key = edition_name_to_id(self.new_edition_var.get())
        add_consumable(self.data, cid, edition=ed_key)
        self.app.mark_unsaved()
        self._refresh()
