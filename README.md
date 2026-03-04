# Balatro Save Editor

A desktop GUI application for editing [Balatro](https://www.playbalatro.com/) save files (`.jkr`). Built with Python and Tkinter, it lets you modify money, jokers, deck cards, and other run statistics without touching the raw save format.

> **⚠ Warning — always back up your saves before editing.**  
> The editor creates automatic backups before every write, but keeping your own copy is never a bad idea.

---

## Features

| Area | What you can edit |
|---|---|
| **General** | Money, hands left, discards left, max joker slots, hand size, ante, round |
| **Jokers** | Add / remove jokers, change edition (Foil / Holo / Polychrome / Negative), toggle Eternal / Rental / Perishable / Pinned modifiers |
| **Deck** | Enhancement, edition, and seal on any playing card; bulk-apply to all visible cards; filter by area (deck / hand / discard) |
| **Backups** | Timestamped automatic backups before every save; view, restore, or delete old backups from inside the app |

---

## Requirements

| Dependency | Version |
|---|---|
| Python | 3.8 or later |
| Tkinter | Bundled with most Python installations |

No third-party packages are required.

### Checking Tkinter

```bash
python3 -m tkinter
```

A small test window should appear. If it does not, install the `python3-tk` package for your OS (e.g. `sudo apt install python3-tk` on Debian/Ubuntu).

---

## Installation

```bash
git clone https://github.com/Salopian15/Balatroeditor.git
cd Balatroeditor
```

That is all — there are no extra dependencies to install.

---

## Running the Editor

```bash
python3 main.py
```

On **macOS** the editor automatically looks for Balatro saves in:

```
~/Library/Application Support/Balatro/<profile>/save.jkr
```

If a save is found it is loaded on startup. On other platforms (Windows / Linux) use **File → Open Save…** to browse to your save file manually.

### Typical save locations

| Platform | Path |
|---|---|
| macOS | `~/Library/Application Support/Balatro/` |
| Windows | `%AppData%\Balatro\` |
| Linux (Steam) | `~/.local/share/Steam/steamapps/compatdata/<appid>/pfx/…` |

---

## User Guide

### Opening a Save

1. Launch the editor with `python3 main.py`.
2. On macOS a save file is loaded automatically if one is found.
3. On any platform, use **File → Open Save…** (or **⌘O**) to pick a `.jkr` file manually.

The status bar at the bottom shows the path of the currently loaded save. If the editor detects and repairs any malformed card fields it will report the count there too.

---

### General Tab

The **General** tab contains the core run statistics.

| Field | Description | Range |
|---|---|---|
| Money ($) | Current dollars | 0 – 999 999 |
| Hands Left | Hands remaining in the current round | 1 – 99 |
| Discards Left | Discards remaining in the current round | 0 – 99 |
| Max Joker Slots | How many jokers can be held at once | 0 – 99 |
| Hand Size | Cards drawn each turn | 1 – 20 |
| Ante | Current ante level | 1 – 39 |
| Round | Current round number | 1 – 999 |

Use the spinbox controls to change any value. The title bar gains a **●** indicator and the **💾 Save Changes** button becomes active as soon as you make a change.

---

### Joker Tab

#### Current jokers list

The top panel shows your active jokers as visual cards. Each card displays:

- **Name** and **internal ID**
- A coloured strip at the top indicating the edition
- An edition badge (e.g. *Foil*, *Holo*, *Polychrome*, *Negative*) below the name
- Small modifier badges for active flags (*ETER*, *RENT*, *PERI*, *PINE*)

**Click a joker card** to select it (highlighted in gold). The description panel below the list shows the joker's effect text.

#### Changing an edition

1. Click a joker card to select it.
2. Use the **Selected Joker Edition** dropdown (middle bar) to pick an edition.

Available editions:

| Edition | Effect |
|---|---|
| None | No edition bonus |
| Foil | +50 Chips |
| Holographic | +10 Mult |
| Polychrome | x1.5 Mult |
| Negative | +1 Joker slot (does not count against the slot limit) |

#### Toggling modifiers

With a joker selected, check or uncheck the modifier checkboxes:

- **Eternal** — cannot be sold or destroyed
- **Rental** — costs $1 at end of each round
- **Perishable** — loses its Perishable sticker after 5 hands played and reverts to a normal joker
- **Pinned** — cannot be reordered in the joker bar

#### Removing a joker

Click the joker to select it, then click **Remove Selected**.

#### Adding a joker

The bottom panel is the **Add Joker** picker:

1. Optionally type in the **Search** box to filter by name.
2. Optionally choose an **Edition** for the new joker.
3. Click the joker button to add it.

Jokers are grouped by rarity with colour-coded headers:
- 🔵 **Common**
- 🟢 **Uncommon**
- 🔴 **Rare**
- 🟣 **Legendary**

Hover over any joker button to see its effect description in a tooltip.

---

### Deck Tab

The **Deck** tab shows every playing card in the run (deck, hand, and discard pile).

#### Filtering by area

Use the radio buttons at the top to display only cards from a specific area:

- **All** — show every card
- **Deck** — cards currently in the draw pile
- **Hand** — cards currently held in hand
- **Discard** — cards in the discard pile

The area of each card is indicated by a small letter in the bottom-right corner of its widget: `D` for deck, `H` for hand, and `D` for discard (both deck and discard share the same initial letter).

#### Editing a single card

1. Click a card to select it (highlighted in gold).  
   The label in the **Edit Selected Card** panel shows the rank, suit, and area.
2. Use the three dropdowns to set:

| Dropdown | Options |
|---|---|
| **Enhancement** | None, Bonus, Mult, Wild, Glass, Steel, Stone, Gold, Lucky |
| **Edition** | None, Foil, Holographic, Polychrome, Negative |
| **Seal** | None, Gold, Red, Blue, Purple |

Changes take effect immediately and are reflected in the card grid.

#### Bulk applying to all visible cards

1. Select any card and choose the enhancement / edition / seal you want.
2. Click **Apply to All Visible** (in the filter bar).

This applies the **currently selected** enhancement, edition, and seal settings to every card shown by the active area filter.

---

### Saving Changes

- Click **💾 Save Changes** (bottom-right) or use **File → Save** (**⌘S**).
- To write to a different file use **File → Save As…**.

Before writing, the editor **always** creates a timestamped backup of the existing file:

```
~/Library/Application Support/Balatro/.editor_backups/save.jkr_YYYYMMDD_HHMMSS.bak
```

A success dialog confirms the save and shows the backup location.

---

### Backup and Restore

Use **File → View Backups…** to open the backup manager.

- The list shows all backups for the currently loaded save file, newest first, with their timestamp and file size.
- **Restore Selected** — copies the selected backup over the live save and reloads it in the editor. Your current state is backed up first.
- **Delete Selected** — permanently removes the selected backup file.

---

## Project Structure

```
Balatroeditor/
├── main.py          # Entry point — creates and runs the App window
├── gui/
│   ├── app.py       # Main window: tabs, file menu, backup/restore logic
│   ├── general_tab.py   # General settings tab
│   ├── joker_tab.py     # Joker editor tab
│   └── deck_tab.py      # Deck card editor tab
├── editor_model.py  # High-level read/write functions for save data
├── game_data.py     # Joker list, editions, enhancements, seals, suits, ranks
├── save_io.py       # .jkr file I/O (DEFLATE compress/decompress)
└── lua_parser.py    # Lua table ↔ Python dict serialiser
```

---

## Disclaimer

This tool is a fan-made project and is not affiliated with or endorsed by Localthunk or the Balatro development team. Use at your own risk. Editing save files may affect game balance or cause unexpected behaviour. Always keep a backup of your original save.
