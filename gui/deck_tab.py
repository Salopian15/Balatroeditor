"""
Deck editor tab — view and edit all playing cards with visual indicators
for enhancements, editions, and seals.
"""

import tkinter as tk
from tkinter import ttk
from game_data import (
    ENHANCEMENTS, ENHANCEMENT_MAP, ENHANCEMENT_COLOURS,
    EDITIONS, EDITION_MAP, EDITION_COLOURS,
    SEALS, SEAL_MAP, SEAL_COLOURS,
    SUIT_COLOURS,
)
from editor_model import (
    get_playing_cards, set_card_enhancement, set_card_edition, set_card_seal,
)


class DeckTab(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.data = None
        self.cards = []
        self.selected_idx = None
        self._build()

    def _build(self):
        # ── Top: card grid ──
        top = ttk.LabelFrame(self, text="Deck Cards", padding=5)
        top.pack(fill="both", expand=True, padx=10, pady=(10, 5))

        # Area filter
        filter_row = ttk.Frame(top)
        filter_row.pack(fill="x", pady=(0, 5))
        ttk.Label(filter_row, text="Show:").pack(side="left", padx=(0, 5))
        self.area_var = tk.StringVar(value="All")
        for area in ("All", "deck", "hand", "discard"):
            ttk.Radiobutton(filter_row, text=area.capitalize(),
                            variable=self.area_var, value=area,
                            command=self._refresh_cards).pack(side="left", padx=4)

        # Bulk edit
        ttk.Separator(filter_row, orient="vertical").pack(side="left", padx=10, fill="y")
        ttk.Label(filter_row, text="Bulk:").pack(side="left", padx=(0, 5))
        ttk.Button(filter_row, text="Apply to All Visible",
                   command=self._bulk_apply).pack(side="left", padx=4)

        # Card grid (scrollable)
        grid_container = ttk.Frame(top)
        grid_container.pack(fill="both", expand=True)

        self.card_canvas = tk.Canvas(grid_container, bg="#1a1a2e",
                                     highlightthickness=0)
        card_sb = ttk.Scrollbar(grid_container, orient="vertical",
                                command=self.card_canvas.yview)
        self.card_canvas.configure(yscrollcommand=card_sb.set)
        card_sb.pack(side="right", fill="y")
        self.card_canvas.pack(side="left", fill="both", expand=True)

        self.card_inner = tk.Frame(self.card_canvas, bg="#1a1a2e")
        self.card_canvas.create_window((0, 0), window=self.card_inner,
                                       anchor="nw")
        self.card_inner.bind("<Configure>",
                             lambda e: self.card_canvas.configure(
                                 scrollregion=self.card_canvas.bbox("all")))

        self.card_canvas.bind("<Enter>", self._bind_mousewheel)
        self.card_canvas.bind("<Leave>", self._unbind_mousewheel)

        # ── Bottom: edit panel for selected card ──
        bot = ttk.LabelFrame(self, text="Edit Selected Card", padding=10)
        bot.pack(fill="x", padx=10, pady=(5, 10))

        self.sel_label = ttk.Label(bot, text="No card selected",
                                   font=("Helvetica", 13, "bold"))
        self.sel_label.grid(row=0, column=0, columnspan=6, pady=(0, 8), sticky="w")

        # Enhancement
        ttk.Label(bot, text="Enhancement:").grid(row=1, column=0, sticky="w", padx=5)
        self.enh_var = tk.StringVar(value="None")
        enh_combo = ttk.Combobox(bot, textvariable=self.enh_var,
                                 values=[e[1] for e in ENHANCEMENTS],
                                 state="readonly", width=14)
        enh_combo.grid(row=1, column=1, padx=5)
        enh_combo.bind("<<ComboboxSelected>>", self._on_enh_change)

        # Edition
        ttk.Label(bot, text="Edition:").grid(row=1, column=2, sticky="w", padx=5)
        self.ed_var = tk.StringVar(value="None")
        ed_combo = ttk.Combobox(bot, textvariable=self.ed_var,
                                values=[e[1] for e in EDITIONS],
                                state="readonly", width=14)
        ed_combo.grid(row=1, column=3, padx=5)
        ed_combo.bind("<<ComboboxSelected>>", self._on_ed_change)

        # Seal
        ttk.Label(bot, text="Seal:").grid(row=1, column=4, sticky="w", padx=5)
        self.seal_var = tk.StringVar(value="None")
        seal_combo = ttk.Combobox(bot, textvariable=self.seal_var,
                                  values=[s[1] for s in SEALS],
                                  state="readonly", width=14)
        seal_combo.grid(row=1, column=5, padx=5)
        seal_combo.bind("<<ComboboxSelected>>", self._on_seal_change)

    def _bind_mousewheel(self, event):
        self.card_canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbind_mousewheel(self, event):
        self.card_canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        self.card_canvas.yview_scroll(-1 * (event.delta // 120), "units")

    def _on_enh_change(self, event=None):
        if self.selected_idx is None:
            return
        enh_name = self.enh_var.get()
        enh_id = "c_base"
        for eid, ename, *_ in ENHANCEMENTS:
            if ename == enh_name:
                enh_id = eid
                break
        card_obj = self.cards[self.selected_idx]["card"]
        set_card_enhancement(card_obj, enh_id)
        self.cards[self.selected_idx]["enhancement"] = enh_id
        self.app.mark_unsaved()
        self._refresh_cards()

    def _on_ed_change(self, event=None):
        if self.selected_idx is None:
            return
        ed_name = self.ed_var.get()
        ed_key = "base"
        for eid, ename, *_ in EDITIONS:
            if ename == ed_name:
                ed_key = eid
                break
        card_obj = self.cards[self.selected_idx]["card"]
        set_card_edition(card_obj, ed_key)
        self.cards[self.selected_idx]["edition"] = ed_key
        self.app.mark_unsaved()
        self._refresh_cards()

    def _on_seal_change(self, event=None):
        if self.selected_idx is None:
            return
        seal_name = self.seal_var.get()
        seal_val = None
        for sid, sname, *_ in SEALS:
            if sname == seal_name:
                seal_val = sid
                break
        card_obj = self.cards[self.selected_idx]["card"]
        set_card_seal(card_obj, seal_val)
        self.cards[self.selected_idx]["seal"] = seal_val
        self.app.mark_unsaved()
        self._refresh_cards()

    def _bulk_apply(self):
        """Apply current enhancement/edition/seal settings to all visible cards."""
        if self.selected_idx is None:
            return
        enh_name = self.enh_var.get()
        ed_name = self.ed_var.get()
        seal_name = self.seal_var.get()

        enh_id = "c_base"
        for eid, ename, *_ in ENHANCEMENTS:
            if ename == enh_name:
                enh_id = eid
                break
        ed_key = "base"
        for eid, ename, *_ in EDITIONS:
            if ename == ed_name:
                ed_key = eid
                break
        seal_val = None
        for sid, sname, *_ in SEALS:
            if sname == seal_name:
                seal_val = sid
                break

        area_filter = self.area_var.get()
        for i, cinfo in enumerate(self.cards):
            if area_filter != "All" and cinfo["area"] != area_filter:
                continue
            set_card_enhancement(cinfo["card"], enh_id)
            set_card_edition(cinfo["card"], ed_key)
            set_card_seal(cinfo["card"], seal_val)
            cinfo["enhancement"] = enh_id
            cinfo["edition"] = ed_key
            cinfo["seal"] = seal_val

        self.app.mark_unsaved()
        self._refresh_cards()

    def _select_card(self, idx):
        self.selected_idx = idx
        cinfo = self.cards[idx]
        self.sel_label.config(
            text=f"{cinfo['rank']} of {cinfo['suit']}  [{cinfo['area']}]"
        )
        enh_display = ENHANCEMENT_MAP.get(cinfo["enhancement"], "None")
        ed_display = EDITION_MAP.get(cinfo["edition"], "None")
        seal_display = SEAL_MAP.get(cinfo["seal"], "None")
        self.enh_var.set(enh_display)
        self.ed_var.set(ed_display)
        self.seal_var.set(seal_display)
        self._refresh_cards()

    def _refresh_cards(self):
        for w in self.card_inner.winfo_children():
            w.destroy()

        if not self.cards:
            lbl = tk.Label(self.card_inner, text="No cards found",
                           fg="#888", bg="#1a1a2e", font=("Helvetica", 13))
            lbl.grid(row=0, column=0, padx=20, pady=30)
            return

        area_filter = self.area_var.get()
        col = 0
        row = 0
        for i, cinfo in enumerate(self.cards):
            if area_filter != "All" and cinfo["area"] != area_filter:
                continue
            self._create_card_widget(row, col, i, cinfo)
            col += 1
            if col >= 8:
                col = 0
                row += 1

    def _create_card_widget(self, grid_row, grid_col, idx, cinfo):
        """Create a visual playing card widget with effect indicators."""
        selected = (idx == self.selected_idx)
        suit_col = SUIT_COLOURS.get(cinfo["suit"], "#999")
        enh_col = ENHANCEMENT_COLOURS.get(cinfo["enhancement"])
        ed_col = EDITION_COLOURS.get(cinfo["edition"])
        seal_col = SEAL_COLOURS.get(cinfo["seal"])

        # Border colour: selected > edition > default
        if selected:
            border = "#f39c12"
        elif ed_col:
            border = ed_col
        else:
            border = "#333"

        card = tk.Frame(self.card_inner, bg=border, padx=2, pady=2)
        card.grid(row=grid_row, column=grid_col, padx=3, pady=3)

        bg = "#2d2d4e" if not selected else "#3d3d6e"
        inner = tk.Frame(card, bg=bg, width=80, height=110)
        inner.pack_propagate(False)
        inner.pack()

        # Edition strip at top
        if ed_col:
            strip = tk.Frame(inner, bg=ed_col, height=4)
            strip.pack(fill="x")

        # Rank
        rank_text = cinfo["rank"]
        if rank_text == "10":
            rank_text = "10"
        rank_lbl = tk.Label(inner, text=rank_text, bg=bg, fg=suit_col,
                            font=("Helvetica", 16, "bold"))
        rank_lbl.pack(pady=(4, 0))

        # Suit symbol
        suit_sym = {"Hearts": "♥", "Diamonds": "♦", "Clubs": "♣", "Spades": "♠"
                    }.get(cinfo["suit"], "?")
        suit_lbl = tk.Label(inner, text=suit_sym, bg=bg, fg=suit_col,
                            font=("Helvetica", 14))
        suit_lbl.pack()

        # Enhancement badge
        if enh_col:
            enh_name = ENHANCEMENT_MAP.get(cinfo["enhancement"], "")
            enh_badge = tk.Label(inner, text=enh_name, bg=enh_col, fg="white",
                                 font=("Helvetica", 7, "bold"), padx=2)
            enh_badge.pack(pady=(2, 0))

        # Seal indicator (coloured dot at bottom)
        if seal_col:
            seal_name = SEAL_MAP.get(cinfo["seal"], "")
            seal_badge = tk.Label(inner, text=f"● {seal_name}", bg=bg,
                                  fg=seal_col, font=("Helvetica", 8, "bold"))
            seal_badge.pack(pady=(1, 2))

        # Area indicator
        area_text = cinfo["area"][0].upper()
        area_lbl = tk.Label(inner, text=area_text, bg=bg, fg="#555",
                            font=("Helvetica", 7))
        area_lbl.pack(side="bottom")

        # Click to select
        for widget in [card, inner, rank_lbl, suit_lbl, area_lbl]:
            widget.bind("<Button-1>", lambda e, i=idx: self._select_card(i))

    def load_data(self, data):
        self.data = data
        self.selected_idx = None
        self.cards = get_playing_cards(data)
        self._refresh_cards()

    def apply_data(self, data):
        # Card changes are applied in-place
        pass
