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
    edition_name_to_id, enhancement_name_to_id, seal_name_to_id,
)
from editor_model import (
    get_playing_cards, set_card_enhancement, set_card_edition, set_card_seal,
)
from gui import bind_mousewheel


class DeckTab(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.data = None
        self.cards = []
        self.selected_indices = set()
        self._build()

    def _build(self):
        # ── Top: card grid ──
        top = ttk.LabelFrame(self, text="  Deck Cards", padding=5)
        top.pack(fill="both", expand=True, padx=10, pady=(10, 5))

        # Area filter + card count
        filter_row = ttk.Frame(top)
        filter_row.pack(fill="x", pady=(0, 5))
        ttk.Label(filter_row, text="Show:").pack(side="left", padx=(0, 5))
        self.area_var = tk.StringVar(value="All")
        for area in ("All", "deck", "hand", "discard"):
            ttk.Radiobutton(filter_row, text=area.capitalize(),
                            variable=self.area_var, value=area,
                            command=self._refresh_cards).pack(side="left", padx=4)

        self.count_var = tk.StringVar(value="")
        ttk.Label(filter_row, textvariable=self.count_var,
                  foreground="#aaaaaa", font=("Helvetica", 10)).pack(side="left", padx=10)

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

        bind_mousewheel(self.card_canvas)

        # ── Bottom: edit panel for selected card ──
        bot = ttk.LabelFrame(self, text="  Edit Card", padding=10)
        bot.pack(fill="x", padx=10, pady=(5, 10))

        self.sel_label = ttk.Label(bot, text="Select a card above to edit it",
                                   font=("Helvetica", 12), foreground="#aaaaaa")
        self.sel_label.grid(row=0, column=0, columnspan=7, pady=(0, 8), sticky="w")

        # Enhancement
        ttk.Label(bot, text="Enhancement:").grid(row=1, column=0, sticky="w", padx=(0, 4))
        self.enh_var = tk.StringVar(value="None")
        enh_combo = ttk.Combobox(bot, textvariable=self.enh_var,
                                 values=[e[1] for e in ENHANCEMENTS],
                                 state="readonly", width=14)
        enh_combo.grid(row=1, column=1, padx=(0, 12))
        enh_combo.bind("<<ComboboxSelected>>", self._on_enh_change)

        # Edition
        ttk.Label(bot, text="Edition:").grid(row=1, column=2, sticky="w", padx=(0, 4))
        self.ed_var = tk.StringVar(value="None")
        ed_combo = ttk.Combobox(bot, textvariable=self.ed_var,
                                values=[e[1] for e in EDITIONS],
                                state="readonly", width=14)
        ed_combo.grid(row=1, column=3, padx=(0, 12))
        ed_combo.bind("<<ComboboxSelected>>", self._on_ed_change)

        # Seal
        ttk.Label(bot, text="Seal:").grid(row=1, column=4, sticky="w", padx=(0, 4))
        self.seal_var = tk.StringVar(value="None")
        seal_combo = ttk.Combobox(bot, textvariable=self.seal_var,
                                  values=[s[1] for s in SEALS],
                                  state="readonly", width=14)
        seal_combo.grid(row=1, column=5, padx=(0, 16))
        seal_combo.bind("<<ComboboxSelected>>", self._on_seal_change)

        # Bulk apply sits in the same row, right-aligned
        ttk.Button(bot, text="Apply to All Visible",
                   command=self._bulk_apply).grid(row=1, column=6, padx=(4, 0))
        ttk.Label(bot, text="(applies current settings to all visible cards)",
                  foreground="#666677", font=("Helvetica", 9)
                  ).grid(row=2, column=0, columnspan=7, sticky="w", pady=(4, 0))

        btn_container = ttk.Frame(bot)
        btn_container.grid(row=3, column=0, columnspan=7, pady=(8, 0), sticky="w")
        ttk.Button(btn_container, text="Remove Selected", command=self._remove_card).pack(side="left", padx=5)
        ttk.Button(btn_container, text="Add Card to Deck", command=self._show_add_card).pack(side="left", padx=5)

    def _remove_card(self):
        if not getattr(self, 'selected_indices', None):
            return
        from editor_model import remove_playing_card
        cards_to_remove = [self.cards[i] for i in self.selected_indices]
        for cinfo in cards_to_remove:
            remove_playing_card(self.data, cinfo["card"], area=cinfo["area"])
        self.app.mark_unsaved()
        self.selected_indices.clear()
        self.cards = get_playing_cards(self.data)
        self._refresh_cards()

    def _show_add_card(self):
        from game_data import SUITS, RANKS
        dlg = tk.Toplevel(self)
        dlg.title("Add Card")
        dlg.geometry("300x200")
        dlg.transient(self)
        dlg.grab_set()

        ttk.Label(dlg, text="Suit:").pack(pady=(15, 0))
        suit_var = tk.StringVar(value="Spades")
        ttk.Combobox(dlg, textvariable=suit_var, values=SUITS, state="readonly").pack()

        ttk.Label(dlg, text="Rank:").pack(pady=(15, 0))
        rank_var = tk.StringVar(value="Ace")
        ranks = [r[0] for r in RANKS]
        ttk.Combobox(dlg, textvariable=rank_var, values=ranks, state="readonly").pack()

        def do_add():
            from editor_model import add_playing_card
            add_playing_card(self.data, suit_var.get(), rank_var.get(), area="deck")
            self.app.mark_unsaved()
            self.cards = get_playing_cards(self.data)
            self._refresh_cards()
            dlg.destroy()

        ttk.Button(dlg, text="Add to Deck", command=do_add).pack(pady=20)

    def _on_enh_change(self, event=None):
        if not getattr(self, 'selected_indices', None):
            return
        enh_id = enhancement_name_to_id(self.enh_var.get())
        for idx in self.selected_indices:
            card_obj = self.cards[idx]["card"]
            set_card_enhancement(card_obj, enh_id)
            self.cards[idx]["enhancement"] = enh_id
        self.app.mark_unsaved()
        self._refresh_cards()

    def _on_ed_change(self, event=None):
        if not getattr(self, 'selected_indices', None):
            return
        ed_key = edition_name_to_id(self.ed_var.get())
        for idx in self.selected_indices:
            card_obj = self.cards[idx]["card"]
            set_card_edition(card_obj, ed_key)
            self.cards[idx]["edition"] = ed_key
        self.app.mark_unsaved()
        self._refresh_cards()

    def _on_seal_change(self, event=None):
        if not getattr(self, 'selected_indices', None):
            return
        seal_val = seal_name_to_id(self.seal_var.get())
        for idx in self.selected_indices:
            card_obj = self.cards[idx]["card"]
            set_card_seal(card_obj, seal_val)
            self.cards[idx]["seal"] = seal_val
        self.app.mark_unsaved()
        self._refresh_cards()

    def _bulk_apply(self):
        """Apply current enhancement/edition/seal settings to all visible cards."""
        if not self.cards:
            return
        enh_id = enhancement_name_to_id(self.enh_var.get())
        ed_key = edition_name_to_id(self.ed_var.get())
        seal_val = seal_name_to_id(self.seal_var.get())

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

    def _select_card(self, idx, event=None):
        if event and (event.state & 0x0004 or event.state & 0x0001): # Ctrl or Shift
            if idx in self.selected_indices:
                self.selected_indices.remove(idx)
            else:
                self.selected_indices.add(idx)
        else:
            self.selected_indices = {idx}

        if not self.selected_indices:
            self.sel_label.config(text="No card selected")
            self._refresh_cards()
            return
            
        cinfo = self.cards[idx]
        if len(self.selected_indices) == 1:
            self.sel_label.config(
                text=f"{cinfo['rank']} of {cinfo['suit']}  \u2014  {cinfo['area']}",
                foreground="#e0e0e0",
            )
        else:
            self.sel_label.config(
                text=f"{len(self.selected_indices)} cards selected",
                foreground="#e0e0e0",
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
            self.count_var.set("")
            return

        area_filter = self.area_var.get()
        col = 0
        row = 0
        visible = 0
        for i, cinfo in enumerate(self.cards):
            if area_filter != "All" and cinfo["area"] != area_filter:
                continue
            self._create_card_widget(row, col, i, cinfo)
            visible += 1
            col += 1
            if col >= 8:
                col = 0
                row += 1

        total = len(self.cards)
        if visible == total:
            self.count_var.set(f"{total} cards")
        else:
            self.count_var.set(f"{visible} of {total} cards")

    def _create_card_widget(self, grid_row, grid_col, idx, cinfo):
        """Create a visual playing card widget with effect indicators."""
        selected = (idx in getattr(self, 'selected_indices', set()))
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
        rank_name = cinfo["rank"]
        from game_data import RANK_CODE_REV
        if rank_name == "10":
            rank_text = "10"
        else:
            rank_text = RANK_CODE_REV.get(rank_name, rank_name)
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
            widget.bind("<Button-1>", lambda e, i=idx: self._select_card(i, e))

    def load_data(self, data):
        self.data = data
        self.selected_indices = set()
        self.cards = get_playing_cards(data)
        self._refresh_cards()

    def apply_data(self, data):
        # Card changes are applied in-place
        pass
