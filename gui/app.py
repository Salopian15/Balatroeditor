"""
Main application window — tab layout, file loading/saving, backup/restore.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import shutil
from datetime import datetime

from save_io import find_profiles, read_save, write_save, read_jkr, write_jkr
from editor_model import repair_cards
from gui.general_tab import GeneralTab
from gui.joker_tab import JokerTab
from gui.deck_tab import DeckTab


BACKUPS_DIR = os.path.expanduser("~/Library/Application Support/Balatro/.editor_backups")


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
        self.title("Balatro Save Editor")
        self.geometry("960x720")
        self.minsize(800, 600)
        self.configure(bg="#0f0f23")

        self.data = None
        self.save_path = None
        self._unsaved = False

        self._build_menu()
        self._build_ui()
        self._auto_detect()

    def mark_unsaved(self):
        """Call this whenever data is changed to flag unsaved state."""
        if not self._unsaved:
            self._unsaved = True
            self._update_title()

    def _build_menu(self):
        menubar = tk.Menu(self)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Open Save…", command=self._open_file,
                              accelerator="⌘O")
        file_menu.add_separator()
        file_menu.add_command(label="Save", command=self._save_file,
                              accelerator="⌘S")
        file_menu.add_command(label="Save As…", command=self._save_as)
        file_menu.add_separator()
        file_menu.add_command(label="View Backups…", command=self._show_backups)
        file_menu.add_separator()
        file_menu.add_command(label="Quit", command=self.quit,
                              accelerator="⌘Q")
        menubar.add_cascade(label="File", menu=file_menu)
        self.config(menu=menubar)

        self.bind_all("<Command-o>", lambda e: self._open_file())
        self.bind_all("<Command-s>", lambda e: self._save_file())

    def _build_ui(self):
        # ── Bottom bar: status + save button ──
        bottom = ttk.Frame(self)
        bottom.pack(fill="x", side="bottom")

        self.status_var = tk.StringVar(value="No save loaded")
        status = ttk.Label(bottom, textvariable=self.status_var,
                           font=("Helvetica", 11), anchor="w", padding=(10, 4))
        status.pack(fill="x", side="left", expand=True)

        self.save_btn = tk.Button(
            bottom, text="💾  Save Changes", command=self._save_file,
            bg="#27ae60", fg="white", activebackground="#2ecc71",
            activeforeground="white", font=("Helvetica", 12, "bold"),
            padx=16, pady=6, relief="raised", bd=1, state="disabled",
        )
        self.save_btn.pack(side="right", padx=10, pady=6)

        # Tab notebook
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=5, pady=5)

        self.general_tab = GeneralTab(self.notebook, self)
        self.joker_tab = JokerTab(self.notebook, self)
        self.deck_tab = DeckTab(self.notebook, self)

        self.notebook.add(self.general_tab, text="  ⚙ General  ")
        self.notebook.add(self.joker_tab, text="  🃏 Jokers  ")
        self.notebook.add(self.deck_tab, text="  🂠 Deck  ")

    def _update_title(self):
        base = "Balatro Save Editor"
        if self._unsaved:
            self.title(f"● {base} — unsaved changes")
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
        save_dir = os.path.expanduser("~/Library/Application Support/Balatro")
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

        # Auto-repair any cards with broken enhancement configs
        repaired = repair_cards(self.data)
        if repaired:
            self.status_var.set(f"Loaded: {path}  (repaired {repaired} card field(s))")
        else:
            self.status_var.set(f"Loaded: {path}")

        self._unsaved = repaired > 0
        self._update_title()
        self.general_tab.load_data(self.data)
        self.joker_tab.load_data(self.data)
        self.deck_tab.load_data(self.data)

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
            self.status_var.set(f"Saved: {path}")
            messagebox.showinfo("Success", "Save written successfully!\n"
                                "A timestamped backup was created in\n"
                                f"{BACKUPS_DIR}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save:\n{e}")
