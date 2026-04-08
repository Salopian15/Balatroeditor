"""

Joker editor tab â€” list, add, remove jokers with edition control and visual indicators.

"""



import tkinter as tk

from tkinter import ttk

from game_data import (

    JOKERS, JOKER_MAP, JOKER_DESC, EDITIONS, EDITION_COLOURS, EDITION_MAP,

)

from editor_model import (

    get_jokers, get_joker_info, set_joker_edition, set_joker_modifier,
<<<<<<< HEAD
    add_joker, remove_joker, MODIFIER_FLAGS, get_max_jokers,
)
from gui import bind_mousewheel, bind_mousewheel_horizontal
from sprites import get_joker_tk_image, is_available as sprites_available
=======

    add_joker, remove_joker, MODIFIER_FLAGS,

)

from gui import bind_mousewheel
>>>>>>> b145c62b9d60c866cbfc705dc5fba4284f83949d





# Rarity groupings for the joker picker

JOKER_GROUPS = {

    "Common": [j for j in JOKERS[:50]],

    "Uncommon": [j for j in JOKERS[50:100]],

    "Rare": [j for j in JOKERS[100:130]],

    "Legendary": [j for j in JOKERS[130:]],

}



RARITY_COLOURS = {

    "Common": "#3498db",

    "Uncommon": "#2ecc71",

    "Rare": "#e74c3c",

    "Legendary": "#8e44ad",

}





class Tooltip:

    """Simple hover tooltip for a widget."""

    def __init__(self, widget, text):

        self.widget = widget

        self.text = text

        self.tip_window = None

        widget.bind("<Enter>", self._show)

        widget.bind("<Leave>", self._hide)



    def _show(self, event=None):

        if self.tip_window:

            return

        x = self.widget.winfo_rootx() + 20

        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 4

        self.tip_window = tw = tk.Toplevel(self.widget)

        tw.wm_overrideredirect(True)

        tw.wm_geometry(f"+{x}+{y}")

        label = tk.Label(tw, text=self.text, justify="left",

                         bg="#1a1a2e", fg="#ddd", relief="solid", bd=1,

                         font=("Helvetica", 11), padx=8, pady=4,

                         wraplength=300)

        label.pack()



    def _hide(self, event=None):

        if self.tip_window:

            self.tip_window.destroy()

            self.tip_window = None





class JokerTab(ttk.Frame):

    def __init__(self, parent, app):

        super().__init__(parent)

        self.app = app

        self.data = None

        self._build()



    def _build(self):
<<<<<<< HEAD
        # ── Top: current jokers list ──
        top = ttk.LabelFrame(self, text="  Current Jokers", padding=10)
        top.pack(fill="both", expand=True, padx=10, pady=(10, 5))

        # Scrollable frame for joker cards (horizontal)
        canvas_frame = ttk.Frame(top)
        canvas_frame.pack(fill="both", expand=True)

        self.joker_canvas = tk.Canvas(canvas_frame, height=200, bg="#1a1a2e",
                                      highlightthickness=0)
        joker_hscroll = ttk.Scrollbar(canvas_frame, orient="horizontal",
                                      command=self.joker_canvas.xview)
        self.joker_canvas.configure(xscrollcommand=joker_hscroll.set)
        self.joker_canvas.pack(fill="both", expand=True)
        joker_hscroll.pack(fill="x")
=======

        # â”€â”€ Top: current jokers list â”€â”€

        top = ttk.LabelFrame(self, text="Current Jokers", padding=10)

        top.pack(fill="both", expand=True, padx=10, pady=(10, 5))



        # Scrollable frame for joker cards

        self.joker_canvas = tk.Canvas(top, height=180, bg="#1a1a2e",

                                      highlightthickness=0)

        self.joker_xscroll = ttk.Scrollbar(top, orient="horizontal",

                           command=self.joker_canvas.xview)

        self.joker_canvas.configure(xscrollcommand=self.joker_xscroll.set,

                        xscrollincrement=16)

        self.joker_canvas.pack(fill="both", expand=True)

        self.joker_xscroll.pack(fill="x", pady=(4, 0))
>>>>>>> b145c62b9d60c866cbfc705dc5fba4284f83949d

        self.joker_inner = tk.Frame(self.joker_canvas, bg="#1a1a2e")

        self.joker_canvas.create_window((0, 0), window=self.joker_inner,

                                        anchor="nw")

        self.joker_inner.bind("<Configure>",

                              lambda e: self._update_joker_scrollregion())



        # Horizontal wheel support lets users browse long joker rows.

        bind_mousewheel(self.joker_canvas, horizontal=True)



<<<<<<< HEAD
        # Horizontal mousewheel / trackpad scrolling
        bind_mousewheel_horizontal(self.joker_canvas)

        # Keep references to PhotoImages so they aren't garbage-collected
        self._card_images = []

        # Joker count + description panel
        info_row = ttk.Frame(top)
        info_row.pack(fill="x", pady=(5, 0))

        self.joker_count_var = tk.StringVar(value="")
        tk.Label(info_row, textvariable=self.joker_count_var,
                 bg="#16213e", fg="#aaaaaa", font=("Helvetica", 10),
                 padx=10, pady=4).pack(side="left")

        self.desc_var = tk.StringVar(value="Click a joker above to see its effect")
        self.desc_label = tk.Label(info_row, textvariable=self.desc_var,
                                   bg="#16213e", fg="#dddddd", anchor="w",
                                   font=("Helvetica", 12), padx=10, pady=6,
                                   wraplength=650, justify="left")
        self.desc_label.pack(side="left", fill="x", expand=True)
=======
        # Description panel for selected joker

        self.desc_var = tk.StringVar(value="Click a joker above to see its effect")

        desc_frame = ttk.Frame(top)

        desc_frame.pack(fill="x", pady=(5, 0))

        self.desc_label = tk.Label(desc_frame, textvariable=self.desc_var,

                                   bg="#16213e", fg="#ddd", anchor="w",

                                   font=("Helvetica", 12), padx=10, pady=6,

                                   wraplength=700, justify="left")

        self.desc_label.pack(fill="x")
>>>>>>> b145c62b9d60c866cbfc705dc5fba4284f83949d



        # â”€â”€ Middle: edition selector + remove button â”€â”€

        mid = ttk.Frame(self)

        mid.pack(fill="x", padx=10, pady=5)



        ttk.Label(mid, text="Selected Joker Edition:").pack(side="left", padx=5)

        self.edition_var = tk.StringVar(value="base")

        ed_combo = ttk.Combobox(mid, textvariable=self.edition_var,

                                values=[e[1] for e in EDITIONS],

                                state="readonly", width=15)

        ed_combo.pack(side="left", padx=5)

        ed_combo.bind("<<ComboboxSelected>>", self._on_edition_change)



        # Modifier checkboxes (eternal / rental / perishable / pinned)

        sep = ttk.Separator(mid, orient="vertical")

        sep.pack(side="left", fill="y", padx=10, pady=2)

        self._modifier_vars = {}

        self._modifier_cbs = {}

        for flag in MODIFIER_FLAGS:

            var = tk.BooleanVar(value=False)

            cb = ttk.Checkbutton(

                mid, text=flag.capitalize(), variable=var,

                command=lambda f=flag: self._on_modifier_toggle(f),

            )

            cb.pack(side="left", padx=4)

            self._modifier_vars[flag] = var

            self._modifier_cbs[flag] = cb



        ttk.Button(mid, text="Remove Selected", command=self._remove_selected

                   ).pack(side="right", padx=5)

<<<<<<< HEAD
        # ── Bottom: joker picker ──
        bot = ttk.LabelFrame(self, text="  Add Joker", padding=10)
=======


        # â”€â”€ Bottom: joker picker â”€â”€

        bot = ttk.LabelFrame(self, text="Add Joker", padding=10)

>>>>>>> b145c62b9d60c866cbfc705dc5fba4284f83949d
        bot.pack(fill="both", expand=True, padx=10, pady=(5, 10))



        # Search

        search_row = ttk.Frame(bot)

        search_row.pack(fill="x", pady=(0, 5))

        ttk.Label(search_row, text="Search:").pack(side="left", padx=(0, 5))

        self.search_var = tk.StringVar()

        self.search_var.trace_add("write", self._filter_picker)

        search_entry = ttk.Entry(search_row, textvariable=self.search_var,

                                 width=25)

        search_entry.pack(side="left")



        # Edition for new joker

        ttk.Label(search_row, text="  Edition:").pack(side="left", padx=(10, 5))

        self.new_edition_var = tk.StringVar(value="None")

        new_ed = ttk.Combobox(search_row, textvariable=self.new_edition_var,

                              values=[e[1] for e in EDITIONS],

                              state="readonly", width=15)

        new_ed.pack(side="left", padx=5)



        # Joker picker grid (scrollable)

        picker_container = ttk.Frame(bot)

        picker_container.pack(fill="both", expand=True)



        self.picker_canvas = tk.Canvas(picker_container, bg="#16213e",

                                       highlightthickness=0)

        picker_sb = ttk.Scrollbar(picker_container, orient="vertical",

                                  command=self.picker_canvas.yview)

        self.picker_canvas.configure(yscrollcommand=picker_sb.set)

        picker_sb.pack(side="right", fill="y")

        self.picker_canvas.pack(side="left", fill="both", expand=True)



        self.picker_inner = tk.Frame(self.picker_canvas, bg="#16213e")

        self.picker_canvas.create_window((0, 0), window=self.picker_inner,

                                        anchor="nw")

        self.picker_inner.bind("<Configure>",

                               lambda e: self.picker_canvas.configure(

                                   scrollregion=self.picker_canvas.bbox("all")))



        # Bind mousewheel scrolling (cross-platform)

        bind_mousewheel(self.picker_canvas)



        self.selected_indices = set()

        self._populate_picker()



    def _populate_picker(self, filter_text=""):

        for w in self.picker_inner.winfo_children():

            w.destroy()



        filter_text = filter_text.lower()

        col = 0

        row_widget = None

        current_row = 0



        for group_name, jokers in JOKER_GROUPS.items():

            filtered = [(jid, jname) for jid, jname, *_ in jokers

                        if filter_text in jname.lower() or filter_text in jid.lower()]

            if not filtered:

                continue



            # Group header

            hdr = tk.Label(self.picker_inner, text=f"  {group_name}  ",

                           bg=RARITY_COLOURS.get(group_name, "#555"),

                           fg="white", font=("Helvetica", 11, "bold"),

                           padx=6, pady=2)

            hdr.grid(row=current_row, column=0, columnspan=6, sticky="w",

                     pady=(8, 4), padx=4)

            current_row += 1

            col = 0



            for jid, jname, *_ in filtered:

                desc = JOKER_DESC.get(jid, "")

                btn = tk.Button(

                    self.picker_inner, text=jname,

                    bg="#0f3460", fg="white", activebackground="#1a508b",

                    activeforeground="white", relief="raised", bd=1,

                    font=("Helvetica", 11), padx=8, pady=4, width=18,

                    cursor="hand2",

                    command=lambda j=jid: self._add_joker(j),

                )

                btn.grid(row=current_row, column=col, padx=3, pady=2, sticky="w")

                Tooltip(btn, f"{jname}\n{desc}")

                col += 1

                if col >= 4:

                    col = 0

                    current_row += 1



            if col > 0:

                current_row += 1



    def _filter_picker(self, *args):

        self._populate_picker(self.search_var.get())



    def _add_joker(self, joker_id):

        if not self.data:

            return

        # Map edition display name to key

        ed_name = self.new_edition_var.get()

        ed_key = "base"

        for eid, ename, *_ in EDITIONS:

            if ename == ed_name:

                ed_key = eid

                break

        add_joker(self.data, joker_id, ed_key)

        self.app.mark_unsaved()
<<<<<<< HEAD
        self._sync_max_jokers()
=======

>>>>>>> b145c62b9d60c866cbfc705dc5fba4284f83949d
        self._refresh_joker_list()



    def _remove_selected(self):
<<<<<<< HEAD
        if self.selected_idx is not None and self.data:
            remove_joker(self.data, self.selected_idx)
            self.selected_idx = None
            self.app.mark_unsaved()
            self._sync_max_jokers()
            self._refresh_joker_list()
=======

        if not getattr(self, "selected_indices", None) or not self.data:

            return

        indices = sorted(list(self.selected_indices), reverse=True)

        for idx in indices:

            remove_joker(self.data, idx)

        self.selected_indices.clear()

        self.app.mark_unsaved()

        self._refresh_joker_list()


>>>>>>> b145c62b9d60c866cbfc705dc5fba4284f83949d

    def _on_edition_change(self, event=None):

        if not getattr(self, "selected_indices", None) or not self.data:

            return

        jokers = get_jokers(self.data)

        ed_name = self.edition_var.get()

        ed_key = "base"

        for eid, ename, *_ in EDITIONS:

            if ename == ed_name:

                ed_key = eid

                break

        for idx in self.selected_indices:

            if 0 <= idx < len(jokers):

                set_joker_edition(jokers[idx], ed_key, data=self.data)

        self.app.mark_unsaved()

        self._refresh_joker_list()



    def _on_modifier_toggle(self, flag):

        if not getattr(self, "selected_indices", None) or not self.data:

            # Reset the checkbox since no joker is selected

            self._modifier_vars[flag].set(False)

            return

        jokers = get_jokers(self.data)

        for idx in self.selected_indices:

            if 0 <= idx < len(jokers):

                set_joker_modifier(jokers[idx], flag, self._modifier_vars[flag].get())

        self.app.mark_unsaved()

        self._refresh_joker_list()

<<<<<<< HEAD
    def _sync_max_jokers(self):
        """Keep the General tab spinner in sync with the model's card_limit."""
        if not self.data:
            return
        try:
            cur = get_max_jokers(self.data)
            self.app.general_tab.fields["max_jokers"].set(cur)
        except (AttributeError, KeyError):
            pass

    def _refresh_joker_list(self):
        self._card_images = []  # reset image references
=======


    def _select_joker(self, idx, event=None):

        if not hasattr(self, 'selected_indices'):

            self.selected_indices = set()

            

        if event and (event.state & 0x0004 or event.state & 0x0001): # Ctrl or Shift

            if idx in self.selected_indices:

                self.selected_indices.remove(idx)

            else:

                self.selected_indices.add(idx)

        else:

            self.selected_indices = {idx}



        jokers = get_jokers(self.data)

        if len(self.selected_indices) == 1:

            actual_idx = list(self.selected_indices)[0]

            if 0 <= actual_idx < len(jokers):

                info = get_joker_info(jokers[actual_idx])

                ed_display = EDITION_MAP.get(info["edition"], "None")

                self.edition_var.set(ed_display)

                for flag in MODIFIER_FLAGS:

                    self._modifier_vars[flag].set(info.get(flag, False))

                desc = JOKER_DESC.get(info["id"], "")

                self.desc_var.set(f'{info["name"]}  —  {desc}')

        else:

            for flag in MODIFIER_FLAGS:

                self._modifier_vars[flag].set(False)

            self.desc_var.set(f'{len(self.selected_indices)} jokers selected')

        self._refresh_joker_list()



    def _refresh_joker_list(self):

>>>>>>> b145c62b9d60c866cbfc705dc5fba4284f83949d
        for w in self.joker_inner.winfo_children():

            w.destroy()



        self._update_joker_scrollregion()



        if not self.data:
<<<<<<< HEAD
            self.joker_count_var.set("")
=======

>>>>>>> b145c62b9d60c866cbfc705dc5fba4284f83949d
            return



        jokers = get_jokers(self.data)
<<<<<<< HEAD
        max_j = get_max_jokers(self.data)

        if not jokers:
            self.joker_count_var.set("0 jokers")
            lbl = tk.Label(self.joker_inner, text="No jokers \u2014 add one below!",
=======

        if not jokers:

            lbl = tk.Label(self.joker_inner, text="No jokers â€” add one below!",

>>>>>>> b145c62b9d60c866cbfc705dc5fba4284f83949d
                           fg="#888", bg="#1a1a2e", font=("Helvetica", 13))

            lbl.pack(padx=20, pady=30)

            self._update_joker_scrollregion()

            return

<<<<<<< HEAD
        count = len(jokers)
        self.joker_count_var.set(f"{count}/{max_j} jokers")
=======

>>>>>>> b145c62b9d60c866cbfc705dc5fba4284f83949d

        for i, joker in enumerate(jokers):

            info = get_joker_info(joker)

            is_selected = (i in getattr(self, "selected_indices", set()))

            self._create_joker_card(i, info, is_selected)



        # Ensure horizontal bounds match the current card strip.

        self._update_joker_scrollregion()



    def _update_joker_scrollregion(self):

        self.joker_inner.update_idletasks()

        bounds = self.joker_canvas.bbox("all")

        self.joker_canvas.configure(scrollregion=(bounds or (0, 0, 0, 0)))



    def _create_joker_card(self, idx, info, selected):
<<<<<<< HEAD
        """Create a visual joker card widget with edition indicator and optional image."""
=======

        """Create a visual joker card widget with edition indicator."""

>>>>>>> b145c62b9d60c866cbfc705dc5fba4284f83949d
        ed_key = info["edition"]

        ed_colour = EDITION_COLOURS.get(ed_key)
        has_image = sprites_available()



        # Card frame

        border_col = "#f39c12" if selected else (ed_colour or "#333")

        bg = "#2d2d4e" if not selected else "#3d3d6e"



        card = tk.Frame(self.joker_inner, bg=border_col, padx=3, pady=3)

        card.pack(side="left", padx=6, pady=8)

<<<<<<< HEAD
        card_w = 100 if has_image else 120
        card_h = 170 if has_image else 140
        inner = tk.Frame(card, bg=bg, width=card_w, height=card_h)
=======


        inner = tk.Frame(card, bg=bg, width=120, height=140)

>>>>>>> b145c62b9d60c866cbfc705dc5fba4284f83949d
        inner.pack_propagate(False)

        inner.pack()



        # Edition indicator strip at top

        if ed_colour:
<<<<<<< HEAD
            strip = tk.Frame(inner, bg=ed_colour, height=4)
            strip.pack(fill="x")

        clickables = [card, inner]

        # Joker sprite image
        if has_image:
            tk_img = get_joker_tk_image(info["id"], width=80, height=107)
            if tk_img:
                self._card_images.append(tk_img)
                img_lbl = tk.Label(inner, image=tk_img, bg=bg, bd=0)
                img_lbl.pack(pady=(4, 0))
                clickables.append(img_lbl)

        # Joker name (smaller when image is present)
        name_font = ("Helvetica", 9, "bold") if has_image else ("Helvetica", 11, "bold")
        name_lbl = tk.Label(inner, text=info["name"], bg=bg, fg="white",
                            font=name_font, wraplength=card_w - 10,
                            justify="center")
        name_lbl.pack(padx=4, pady=(2 if has_image else 8, 0))
        clickables.append(name_lbl)
=======

            strip = tk.Frame(inner, bg=ed_colour, height=6)

            strip.pack(fill="x")



        # Joker name

        name_lbl = tk.Label(inner, text=info["name"], bg=bg, fg="white",

                            font=("Helvetica", 11, "bold"), wraplength=110,

                            justify="center")

        name_lbl.pack(expand=True, padx=4, pady=(8, 2))
>>>>>>> b145c62b9d60c866cbfc705dc5fba4284f83949d



        # Edition badge

        if ed_key != "base":

            ed_display = EDITION_MAP.get(ed_key, "")

            badge_bg = ed_colour or "#555"
<<<<<<< HEAD
=======

            # Choose contrasting text color

>>>>>>> b145c62b9d60c866cbfc705dc5fba4284f83949d
            badge_fg = "white" if ed_key != "foil" else "#1a1a2e"

            badge = tk.Label(inner, text=ed_display, bg=badge_bg, fg=badge_fg,
<<<<<<< HEAD
                             font=("Helvetica", 8, "bold"), padx=3, pady=0)
            badge.pack(pady=(0, 2))
            clickables.append(badge)
=======

                             font=("Helvetica", 9, "bold"), padx=4, pady=1)

            badge.pack(pady=(0, 4))
>>>>>>> b145c62b9d60c866cbfc705dc5fba4284f83949d



        # Modifier badges

        _mod_colours = {

            "eternal": "#e6b800", "rental": "#e67300",

            "perishable": "#9b59b6", "pinned": "#2980b9",

        }

        active_mods = [f for f in MODIFIER_FLAGS if info.get(f)]

        if active_mods:

            mod_frame = tk.Frame(inner, bg=bg)
<<<<<<< HEAD
            mod_frame.pack(pady=(0, 1))
=======

            mod_frame.pack(pady=(0, 2))

>>>>>>> b145c62b9d60c866cbfc705dc5fba4284f83949d
            for mod in active_mods:

                mlbl = tk.Label(mod_frame, text=mod[:4].upper(),

                                bg=_mod_colours.get(mod, "#555"), fg="white",

                                font=("Helvetica", 7, "bold"), padx=2, pady=0)

                mlbl.pack(side="left", padx=1)
<<<<<<< HEAD
                clickables.append(mlbl)

        # Click to select — bind all child widgets
        for widget in clickables:
            widget.bind("<Button-1>", lambda e, i=idx: self._select_joker(i))
=======

                mlbl.bind("<Button-1>", lambda e, i=idx: self._select_joker(i, event=e))



        # ID label

        id_lbl = tk.Label(inner, text=info["id"], bg=bg, fg="#666",

                          font=("Helvetica", 8))

        id_lbl.pack(pady=(0, 4))



        # Click to select

        for widget in [card, inner, name_lbl, id_lbl]:

            widget.bind("<Button-1>", lambda e, i=idx: self._select_joker(i, event=e))

        if ed_key != "base":

            badge.bind("<Button-1>", lambda e, i=idx: self._select_joker(i, event=e))


>>>>>>> b145c62b9d60c866cbfc705dc5fba4284f83949d

    def load_data(self, data):

        self.data = data

        self.selected_indices = set()

        self._refresh_joker_list()



    def apply_data(self, data):

        # Joker changes are applied in-place, nothing extra needed

        pass

