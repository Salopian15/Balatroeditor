"""
Main application window — tab layout, file loading/saving, backup/restore.
"""

import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import shutil
from datetime import datetime

IS_MAC = sys.platform == "darwin"

from save_io import find_profiles, read_save, write_save, read_jkr, write_jkr, SAVE_DIR
from editor_model import repair_cards, detect_modded_content
from gui.general_tab import GeneralTab
from gui.joker_tab import JokerTab
from gui.deck_tab import DeckTab
<<<<<<< HEAD
import sprites
=======
from gui.consumable_tab import ConsumableTab
>>>>>>> b145c62b9d60c866cbfc705dc5fba4284f83949d


BACKUPS_DIR = os.path.join(SAVE_DIR, ".editor_backups")


def ensure_backups_dir():
    """Ensure the backups directory exists."""
    os.makedirs(BACKUPS_DIR, exist_ok=True)


def create_timestamped_backup(save_path):
    """Create a timestamped backup of the save file."""
    if not os.path.exists(save_path):
        return
    ensure_backups_dir()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.basename(save_path)
    backup_path = os.path.join(BACKUPS_DIR, f"{filename}_{timestamp}.bak")
    shutil.copy2(save_path, backup_path)


def list_backups(save_filename="save.jkr"):
    """Return list of (backup_path, timestamp_str, readable_date) sorted newest first."""
    ensure_backups_dir()
    backups = []
    for fname in os.listdir(BACKUPS_DIR):
        if fname.startswith(save_filename + "_") and fname.endswith(".bak"):
            fpath = os.path.join(BACKUPS_DIR, fname)
            # Extract timestamp: save.jkr_YYYYMMDD_HHMMSS.bak
            timestamp_part = fname[len(save_filename) + 1:-4]  # Remove prefix and .bak
            try:
                dt = datetime.strptime(timestamp_part, "%Y%m%d_%H%M%S")
                readable = dt.strftime("%Y-%m-%d %H:%M:%S")
                backups.append((fpath, timestamp_part, readable))
            except ValueError:
                continue
    backups.sort(reverse=True, key=lambda x: x[1])
    return backups


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.withdraw()  # Hide window while building to prevent jitter

        self.title("Balatro Save Editor")
        self.geometry("960x720")
        self.minsize(800, 600)
        self.configure(bg="#0f0f23")

        self.data = None
        self.save_path = None
        self._unsaved = False

        self._apply_theme()
        self._build_menu()
        self._build_ui()
        self._init_sprites()

        # Centre on screen before showing
        self.update_idletasks()
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw - 960) // 2
        y = (sh - 720) // 2
        self.geometry(f"960x720+{x}+{y}")

        # Load save while still hidden so it appears fully rendered
        self._auto_detect()
        self.deiconify()

    def _apply_theme(self):
        """Configure ttk styles to match the dark colour scheme."""
        style = ttk.Style(self)
        # Use a base theme that is cross-platform
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        bg_dark  = "#0f0f23"
        bg_mid   = "#1a1a2e"
        bg_panel = "#16213e"
        accent   = "#27ae60"
        fg       = "#e0e0e0"
        fg_dim   = "#aaaaaa"
        border   = "#333355"

        style.configure(".",
            background=bg_dark, foreground=fg,
            fieldbackground=bg_mid, troughcolor=bg_mid,
            bordercolor=border, relief="flat",
            font=("Helvetica", 12),
        )
        style.configure("TFrame", background=bg_dark)
        style.configure("TLabel", background=bg_dark, foreground=fg)
        style.configure("TLabelframe",
            background=bg_dark, foreground=fg_dim,
            bordercolor=border, relief="groove",
        )
        style.configure("TLabelframe.Label",
            background=bg_dark, foreground=fg_dim, font=("Helvetica", 11),
        )
        style.configure("TNotebook",
            background=bg_dark, bordercolor=border, tabmargins=[2, 4, 2, 0],
        )
        style.configure("TNotebook.Tab",
            background=bg_mid, foreground=fg_dim,
            padding=[12, 6], font=("Helvetica", 12),
        )
        style.map("TNotebook.Tab",
            background=[("selected", bg_panel)],
            foreground=[("selected", fg)],
        )
        style.configure("TButton",
            background=bg_mid, foreground=fg,
            bordercolor=border, relief="raised", padding=[8, 4],
        )
        style.map("TButton",
            background=[("active", bg_panel)],
        )
        style.configure("TCombobox",
            background=bg_mid, foreground=fg,
            fieldbackground=bg_mid, selectbackground=accent,
        )
        style.configure("TSpinbox",
            background=bg_mid, foreground=fg, fieldbackground=bg_mid,
        )
        style.configure("TEntry",
            background=bg_mid, foreground=fg, fieldbackground=bg_mid,
            insertcolor=fg,
        )
        style.configure("TScrollbar",
            background=bg_mid, troughcolor=bg_dark, bordercolor=border,
        )
        style.configure("TSeparator", background=border)
        style.configure("TRadiobutton", background=bg_dark, foreground=fg)
        style.configure("TCheckbutton", background=bg_dark, foreground=fg)

    def mark_unsaved(self):
        """Call this whenever data is changed to flag unsaved state."""
        if not self._unsaved:
            self._unsaved = True
            self._update_title()

    def _build_menu(self):
        menubar = tk.Menu(self)
        file_menu = tk.Menu(menubar, tearoff=0)
        mod_key = "⌘" if IS_MAC else "Ctrl+"
        bind_key = "Command" if IS_MAC else "Control"

        file_menu.add_command(label="Open Save…", command=self._open_file,
                              accelerator=f"{mod_key}O")
        file_menu.add_separator()
        file_menu.add_command(label="Save", command=self._save_file,
                              accelerator=f"{mod_key}S")
        file_menu.add_command(label="Save As…", command=self._save_as)
        file_menu.add_separator()
        file_menu.add_command(label="View Backups…", command=self._show_backups)
        file_menu.add_separator()
        file_menu.add_command(label="Quit", command=self.quit,
                              accelerator=f"{mod_key}Q")
        menubar.add_cascade(label="File", menu=file_menu)

        settings_menu = tk.Menu(menubar, tearoff=0)
        settings_menu.add_command(label="Set Balatro Game Folder…",
                                  command=self._browse_game_dir)
        menubar.add_cascade(label="Settings", menu=settings_menu)

        self.config(menu=menubar)

        self.bind_all(f"<{bind_key}-o>", lambda e: self._open_file())
        self.bind_all(f"<{bind_key}-s>", lambda e: self._save_file())

    def _build_ui(self):
        # ── Bottom bar: status + save button ──
        bottom = tk.Frame(self, bg="#0d0d1f", pady=0)
        bottom.pack(fill="x", side="bottom")

        # Thin accent line above the bar
        tk.Frame(bottom, bg="#27ae60", height=2).pack(fill="x")

        bar = tk.Frame(bottom, bg="#0d0d1f")
        bar.pack(fill="x")

        self.status_var = tk.StringVar(value="No save loaded — use File > Open Save or place a save.jkr in the Balatro folder")
        status = tk.Label(bar, textvariable=self.status_var,
                          bg="#0d0d1f", fg="#aaaaaa",
                          font=("Helvetica", 11), anchor="w", padx=12, pady=6)
        status.pack(fill="x", side="left", expand=True)

        self.save_btn = tk.Button(
            bar, text="  Save Changes", command=self._save_file,
            bg="#27ae60", fg="white", activebackground="#2ecc71",
            activeforeground="white", font=("Helvetica", 12, "bold"),
            padx=16, pady=6, relief="flat", bd=0, state="disabled",
            cursor="hand2",
        )
        self.save_btn.pack(side="right", padx=10, pady=5)

        # ── Welcome banner (shown when no save is loaded) ──
        self.welcome_frame = tk.Frame(self, bg="#0f0f23")
        self.welcome_frame.pack(fill="both", expand=True)

        inner = tk.Frame(self.welcome_frame, bg="#16213e", padx=40, pady=40)
        inner.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(inner, text="Balatro Save Editor",
                 bg="#16213e", fg="#e0e0e0",
                 font=("Helvetica", 22, "bold")).pack(pady=(0, 6))
        tk.Label(inner, text="No save file loaded",
                 bg="#16213e", fg="#888",
                 font=("Helvetica", 14)).pack(pady=(0, 20))

        tk.Button(inner, text="  Open Save File…",
                  command=self._open_file,
                  bg="#27ae60", fg="white", activebackground="#2ecc71",
                  activeforeground="white", font=("Helvetica", 13, "bold"),
                  padx=20, pady=10, relief="flat", bd=0, cursor="hand2",
                  ).pack(pady=(0, 8))
        tk.Label(inner,
                 text="Or place your save.jkr in the default Balatro folder\n"
                      "and it will be detected automatically on next launch.",
                 bg="#16213e", fg="#666",
                 font=("Helvetica", 11), justify="center").pack()

        # ── Tab notebook (hidden until a save is loaded) ──
        self.notebook = ttk.Notebook(self)

        self.general_tab = GeneralTab(self.notebook, self)
        self.joker_tab = JokerTab(self.notebook, self)
        self.deck_tab = DeckTab(self.notebook, self)
        self.consumable_tab = ConsumableTab(self.notebook, self)

<<<<<<< HEAD
        self.notebook.add(self.general_tab, text="  General  ")
        self.notebook.add(self.joker_tab, text="  Jokers  ")
        self.notebook.add(self.deck_tab, text="  Deck  ")
=======
        self.notebook.add(self.general_tab, text="  ⚙ General  ")
        self.notebook.add(self.joker_tab, text="  🃏 Jokers  ")
        self.notebook.add(self.consumable_tab, text="  🔮 Consumables  ")
        self.notebook.add(self.deck_tab, text="  🂠 Deck  ")
>>>>>>> b145c62b9d60c866cbfc705dc5fba4284f83949d

    def _update_title(self):
        base = "Balatro Save Editor"
        if self._unsaved:
            self.title(f"\u25cf {base} \u2014 unsaved changes")
            self.save_btn.config(state="normal")
        else:
            self.title(base)
            self.save_btn.config(state="disabled" if not self.data else "normal")

    def _auto_detect(self):
        """Try to auto-detect a save file on launch."""
        profiles = find_profiles()
        if profiles:
            # Load the first profile's save
            path = os.path.join(profiles[0], "save.jkr")
            self._load_save(path)

    def _init_sprites(self):
        """Try to auto-detect the Balatro game directory for card images."""
        love_path = sprites.auto_detect_love_path()
        if love_path:
            sprites.set_love_path(love_path)

    def _browse_game_dir(self):
        """Let the user manually select Balatro.love for card images."""
        path = filedialog.askopenfilename(
            title="Select Balatro.love",
            filetypes=[("LÖVE archive", "*.love"), ("All Files", "*.*")],
        )
        if path:
            sprites.set_love_path(path)
            if sprites.is_available():
                messagebox.showinfo("Success",
                                    "Joker sprites loaded!\n"
                                    "Card images will appear in the Jokers tab.")
                # Refresh the joker list to show images
                if self.data:
                    self.joker_tab._refresh_joker_list()
            else:
                messagebox.showwarning("Warning",
                                       "Could not load sprites from that file.\n"
                                       "Make sure you selected a valid Balatro.love archive.")

    def _show_backups(self):
        """Show a dialog to view and restore from timestamped backups."""
        if not self.save_path:
            messagebox.showwarning("Warning", "No save file loaded.")
            return

        backups = list_backups(os.path.basename(self.save_path))
        if not backups:
            messagebox.showinfo("Backups", "No backups found yet.\n"
                                "Backups are created each time you save.")
            return

        # Create a new window
        bak_win = tk.Toplevel(self)
        bak_win.title("Restore from Backup")
        bak_win.geometry("500x400")
        bak_win.transient(self)
        bak_win.grab_set()

        # Instructions
        instr = ttk.Label(bak_win, text="Select a backup to restore:",
                          font=("Helvetica", 12))
        instr.pack(pady=(10, 5), padx=10)

        # Listbox with backups
        frame = ttk.Frame(bak_win)
        frame.pack(fill="both", expand=True, padx=10, pady=5)

        listbox = tk.Listbox(frame, font=("Helvetica", 11), height=12,
                             bg="#2d2d4e", fg="white", selectmode="single")
        listbox.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=listbox.yview)
        scrollbar.pack(side="right", fill="y")
        listbox.config(yscrollcommand=scrollbar.set)

        for bak_path, ts, readable in backups:
            size_kb = os.path.getsize(bak_path) / 1024
            listbox.insert(tk.END, f"{readable}  ({size_kb:.1f} KB)")

        # Info label
        info_lbl = ttk.Label(bak_win, text="", foreground="green",
                             font=("Helvetica", 10))
        info_lbl.pack(padx=10, pady=5)

        def on_select():
            sel = listbox.curselection()
            if not sel:
                messagebox.showwarning("Warning", "Please select a backup.")
                return
            idx = sel[0]
            bak_path, ts, readable = backups[idx]

            if messagebox.askyesno("Confirm",
                                   f"Restore from {readable}?\n\n"
                                   f"Current save will be backed up first."):
                try:
                    # Backup current state first
                    create_timestamped_backup(self.save_path)
                    # Restore from selected backup
                    shutil.copy2(bak_path, self.save_path)
                    # Reload in editor
                    self._load_save(self.save_path)
                    self.status_var.set(f"Restored from {readable}")
                    messagebox.showinfo("Success",
                                        f"Restored from backup: {readable}\n\n"
                                        f"Your previous state was backed up.")
                    bak_win.destroy()
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to restore:\n{e}")

        # Buttons
        btn_frame = ttk.Frame(bak_win)
        btn_frame.pack(fill="x", padx=10, pady=(0, 10))

        ttk.Button(btn_frame, text="Restore Selected",
                   command=on_select).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Delete Selected",
                   command=lambda: on_delete_backup(listbox, backups, bak_win)
                   ).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Close",
                   command=bak_win.destroy).pack(side="right", padx=5)

        def on_delete_backup(lb, baks, win):
            sel = lb.curselection()
            if not sel:
                messagebox.showwarning("Warning", "Please select a backup.")
                return
            idx = sel[0]
            bak_path, ts, readable = baks[idx]
            if messagebox.askyesno("Confirm", f"Delete {readable}?"):
                try:
                    os.unlink(bak_path)
                    baks.pop(idx)
                    lb.delete(idx)
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to delete:\n{e}")

    def _open_file(self):
        save_dir = SAVE_DIR
        path = filedialog.askopenfilename(
            title="Open Balatro Save",
            initialdir=save_dir if os.path.isdir(save_dir) else "~",
            filetypes=[("Balatro Save", "*.jkr"), ("All Files", "*.*")],
        )
        if path:
            self._load_save(path)

    def _load_save(self, path):
        try:
            self.data = read_jkr(path)
            self.save_path = path
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load save:\n{e}")
            return

<<<<<<< HEAD
        # Auto-repair any cards with broken enhancement configs
        repaired = repair_cards(self.data)

        # Show a short display name instead of full path
        short = os.path.basename(os.path.dirname(path)) + "/" + os.path.basename(path)
        if repaired:
            self.status_var.set(f"Loaded: {short}  \u2014  repaired {repaired} card field(s)")
        else:
            self.status_var.set(f"Loaded: {short}")
=======
        # Auto-repair can overwrite values that some mods intentionally set.
        mod_info = detect_modded_content(self.data)
        if mod_info["is_modded"]:
            reason = ", ".join(mod_info["reasons"])
            self.status_var.set(
                f"Loaded: {path}  (modded content detected; skipped auto-repair: {reason})"
            )
            repaired = 0
        else:
            repaired = repair_cards(self.data)
            if repaired:
                self.status_var.set(f"Loaded: {path}  (repaired {repaired} card field(s))")
            else:
                self.status_var.set(f"Loaded: {path}")
>>>>>>> b145c62b9d60c866cbfc705dc5fba4284f83949d

        self._unsaved = repaired > 0
        self._update_title()
        self.general_tab.load_data(self.data)
        self.joker_tab.load_data(self.data)
        self.deck_tab.load_data(self.data)
        self.consumable_tab.load_data(self.data)

        # Switch from welcome screen to tab view
        self.welcome_frame.pack_forget()
        self.notebook.pack(fill="both", expand=True, padx=5, pady=5)

    def _save_file(self):
        if not self.data or not self.save_path:
            self._save_as()
            return
        self._do_save(self.save_path)

    def _save_as(self):
        if not self.data:
            messagebox.showwarning("Warning", "No save data loaded.")
            return
        path = filedialog.asksaveasfilename(
            title="Save Balatro Save",
            defaultextension=".jkr",
            filetypes=[("Balatro Save", "*.jkr"), ("All Files", "*.*")],
        )
        if path:
            self._do_save(path)

    def _do_save(self, path):
        try:
            self.general_tab.apply_data(self.data)
            self.joker_tab.apply_data(self.data)
            self.deck_tab.apply_data(self.data)
            # Create timestamped backup before writing
            create_timestamped_backup(path)
            write_jkr(path, self.data, backup=True)
            self.save_path = path
            self._unsaved = False
            self._update_title()
            short = os.path.basename(os.path.dirname(path)) + "/" + os.path.basename(path)
            self.status_var.set(f"Saved: {short}")
            messagebox.showinfo("Saved", "Save written successfully!\n"
                                "A timestamped backup was created automatically.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save:\n{e}")
