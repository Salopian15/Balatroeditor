"""
Editor model — high-level functions to read/manipulate Balatro save data.
"""

import copy
from game_data import (
    JOKER_MAP, ENHANCEMENT_MAP, EDITION_MAP, SEAL_MAP,
    SUIT_CODES, RANK_CODES, SUIT_CODE_REV, RANK_CODE_REV, RANK_NOMINAL,
    ENHANCEMENTS, EDITIONS, SUITS, SUIT_COLOURS,
)


def _game(data):
    """Get the GAME table from save data."""
    return data["GAME"]


def _card_areas(data):
    """cardAreas is a top-level key in the save, not under GAME."""
    return data["cardAreas"]


# ── General ────────────────────────────────────────────────────

def get_dollars(data):
    return _game(data).get("dollars", 0)

def set_dollars(data, val):
    _game(data)["dollars"] = max(0, int(val))

def get_hands(data):
    return _game(data).get("current_round", {}).get("hands_left", 4)

def set_hands(data, val):
    _game(data).setdefault("current_round", {})["hands_left"] = max(1, int(val))

def get_discards(data):
    return _game(data).get("current_round", {}).get("discards_left", 3)

def set_discards(data, val):
    _game(data).setdefault("current_round", {})["discards_left"] = max(0, int(val))

def get_hand_size(data):
    return _card_areas(data).get("hand", {}).get("config", {}).get("card_limit", 8)

def set_hand_size(data, val):
    val = max(1, int(val))
    _card_areas(data)["hand"]["config"]["card_limit"] = val
    _card_areas(data)["hand"]["config"]["temp_limit"] = val

def get_max_jokers(data):
    cfg = _card_areas(data).get("jokers", {}).get("config", {})
    return cfg.get("card_limit", 5)

def set_max_jokers(data, val):
    val = max(0, int(val))
    cfg = _card_areas(data)["jokers"]["config"]
    cfg["card_limit"] = val
    cfg["temp_limit"] = val
    _game(data)["max_jokers"] = val

def get_ante(data):
    return _game(data).get("round_resets", {}).get("ante", 1)

def set_ante(data, val):
    _game(data)["round_resets"]["ante"] = max(1, int(val))

def get_round(data):
    return _game(data).get("round", 1)

def set_round(data, val):
    _game(data)["round"] = max(1, int(val))


# ── Jokers ─────────────────────────────────────────────────────

def get_jokers(data):
    """Return list of joker card objects from the save."""
    cards = _card_areas(data).get("jokers", {}).get("cards", {})
    return _get_joker_list(cards)


def _get_joker_list(cards):
    """Convert joker cards (list or dict) to a plain list."""
    if isinstance(cards, list):
        return cards
    if isinstance(cards, dict):
        return [cards[k] for k in sorted(cards.keys()) if isinstance(k, int)]
    return []


# Card modifier flags supported by the editor
MODIFIER_FLAGS = ("eternal", "rental", "perishable", "pinned")


def get_joker_info(joker):
    """Extract display info from a joker card object."""
    center = joker.get("save_fields", {}).get("center", "")
    name = JOKER_MAP.get(center, center)
    edition = _get_edition_name(joker)
    ability = joker.get("ability", {})
    info = {"id": center, "name": name, "edition": edition, "card": joker}
    for flag in MODIFIER_FLAGS:
        info[flag] = bool(ability.get(flag, False))
    return info


def _get_edition_name(card):
    ed = card.get("edition", {})
    if not ed or not isinstance(ed, dict):
        return "base"
    if ed.get("negative"):
        return "negative"
    if ed.get("polychrome"):
        return "polychrome"
    if ed.get("holo"):
        return "holo"
    if ed.get("foil"):
        return "foil"
    return "base"


def set_joker_modifier(joker, modifier, value):
    """Set or clear a modifier flag (eternal/rental/perishable/pinned) on a joker."""
    ability = joker.setdefault("ability", {})
    if value:
        ability[modifier] = True
    else:
        ability.pop(modifier, None)


def set_joker_edition(joker, edition_key, data=None):
    """Set the edition on a joker card object.

    If *data* is provided, adjusts joker card_limit for negative edition changes.
    """
    was_negative = isinstance(joker.get("edition"), dict) and joker["edition"].get("negative")
    for eid, ename, edesc, ed_dict in EDITIONS:
        if eid == edition_key:
            if ed_dict is None:
                if "edition" in joker:
                    del joker["edition"]
            else:
                joker["edition"] = dict(ed_dict)
            break
    is_negative = isinstance(joker.get("edition"), dict) and joker["edition"].get("negative")
    if data is not None:
        cfg = _card_areas(data)["jokers"]["config"]
        if is_negative and not was_negative:
            cfg["card_limit"] = cfg.get("card_limit", 5) + 1
        elif was_negative and not is_negative:
            cfg["card_limit"] = max(0, cfg.get("card_limit", 5) - 1)


# Joker config data extracted from game source (game.lua).
# Maps joker_id -> {order, effect, cost, config} where config
# contains the fields that get merged into the ability table.
_JOKER_CONFIGS = {
    "j_joker": {"order": 1, "effect": "Mult", "cost": 2, "config": {"mult": 4}},
    "j_greedy_joker": {"order": 2, "effect": "Suit Mult", "cost": 5, "config": {"extra": {"s_mult": 3, "suit": "Diamonds"}}},
    "j_lusty_joker": {"order": 3, "effect": "Suit Mult", "cost": 5, "config": {"extra": {"s_mult": 3, "suit": "Hearts"}}},
    "j_wrathful_joker": {"order": 4, "effect": "Suit Mult", "cost": 5, "config": {"extra": {"s_mult": 3, "suit": "Spades"}}},
    "j_gluttenous_joker": {"order": 5, "effect": "Suit Mult", "cost": 5, "config": {"extra": {"s_mult": 3, "suit": "Clubs"}}},
    "j_jolly": {"order": 6, "effect": "Type Mult", "cost": 3, "config": {"t_mult": 8, "type": "Pair"}},
    "j_zany": {"order": 7, "effect": "Type Mult", "cost": 4, "config": {"t_mult": 12, "type": "Three of a Kind"}},
    "j_mad": {"order": 8, "effect": "Type Mult", "cost": 4, "config": {"t_mult": 10, "type": "Two Pair"}},
    "j_crazy": {"order": 9, "effect": "Type Mult", "cost": 4, "config": {"t_mult": 12, "type": "Straight"}},
    "j_droll": {"order": 10, "effect": "Type Mult", "cost": 4, "config": {"t_mult": 10, "type": "Flush"}},
    "j_sly": {"order": 11, "effect": "", "cost": 3, "config": {"t_chips": 50, "type": "Pair"}},
    "j_wily": {"order": 12, "effect": "", "cost": 4, "config": {"t_chips": 100, "type": "Three of a Kind"}},
    "j_clever": {"order": 13, "effect": "", "cost": 4, "config": {"t_chips": 80, "type": "Two Pair"}},
    "j_devious": {"order": 14, "effect": "", "cost": 4, "config": {"t_chips": 100, "type": "Straight"}},
    "j_crafty": {"order": 15, "effect": "", "cost": 4, "config": {"t_chips": 80, "type": "Flush"}},
    "j_half": {"order": 16, "effect": "Hand Size Mult", "cost": 5, "config": {"extra": {"mult": 20, "size": 3}}},
    "j_stencil": {"order": 17, "effect": "Hand Size Mult", "cost": 8, "config": {}},
    "j_four_fingers": {"order": 18, "effect": "", "cost": 7, "config": {}},
    "j_mime": {"order": 19, "effect": "Hand card double", "cost": 5, "config": {"extra": 1}},
    "j_credit_card": {"order": 20, "effect": "Credit", "cost": 1, "config": {"extra": 20}},
    "j_ceremonial": {"order": 21, "effect": "", "cost": 6, "config": {"mult": 0}},
    "j_banner": {"order": 22, "effect": "Discard Chips", "cost": 5, "config": {"extra": 30}},
    "j_mystic_summit": {"order": 23, "effect": "No Discard Mult", "cost": 5, "config": {"extra": {"mult": 15, "d_remaining": 0}}},
    "j_marble": {"order": 24, "effect": "Stone card hands", "cost": 6, "config": {"extra": 1}},
    "j_loyalty_card": {"order": 25, "effect": "1 in 10 mult", "cost": 5, "config": {"extra": {"Xmult": 4, "every": 5, "remaining": "5 remaining"}}},
    "j_8_ball": {"order": 26, "effect": "Spawn Tarot", "cost": 5, "config": {"extra": 4}},
    "j_misprint": {"order": 27, "effect": "Random Mult", "cost": 4, "config": {"extra": {"max": 23, "min": 0}}},
    "j_dusk": {"order": 28, "effect": "", "cost": 5, "config": {"extra": 1}},
    "j_raised_fist": {"order": 29, "effect": "Socialized Mult", "cost": 5, "config": {}},
    "j_chaos": {"order": 30, "effect": "Bonus Rerolls", "cost": 4, "config": {"extra": 1}},
    "j_fibonacci": {"order": 31, "effect": "Card Mult", "cost": 8, "config": {"extra": 8}},
    "j_steel_joker": {"order": 32, "effect": "Steel Card Buff", "cost": 7, "config": {"extra": 0.2}},
    "j_scary_face": {"order": 33, "effect": "Scary Face Cards", "cost": 4, "config": {"extra": 30}},
    "j_abstract": {"order": 34, "effect": "Joker Mult", "cost": 4, "config": {"extra": 3}},
    "j_delayed_grat": {"order": 35, "effect": "Discard dollars", "cost": 4, "config": {"extra": 2}},
    "j_hack": {"order": 36, "effect": "Low Card double", "cost": 6, "config": {"extra": 1}},
    "j_pareidolia": {"order": 37, "effect": "All face cards", "cost": 5, "config": {}},
    "j_gros_michel": {"order": 38, "effect": "", "cost": 5, "config": {"extra": {"odds": 6, "mult": 15}}},
    "j_even_steven": {"order": 39, "effect": "Even Card Buff", "cost": 4, "config": {"extra": 4}},
    "j_odd_todd": {"order": 40, "effect": "Odd Card Buff", "cost": 4, "config": {"extra": 31}},
    "j_scholar": {"order": 41, "effect": "Ace Buff", "cost": 4, "config": {"extra": {"mult": 4, "chips": 20}}},
    "j_business": {"order": 42, "effect": "Face Card dollar Chance", "cost": 4, "config": {"extra": 2}},
    "j_supernova": {"order": 43, "effect": "Hand played mult", "cost": 5, "config": {"extra": 1}},
    "j_ride_the_bus": {"order": 44, "effect": "", "cost": 6, "config": {"extra": 1}},
    "j_space": {"order": 45, "effect": "Upgrade Hand chance", "cost": 5, "config": {"extra": 4}},
    "j_egg": {"order": 46, "effect": "", "cost": 4, "config": {"extra": 3}},
    "j_burglar": {"order": 47, "effect": "", "cost": 6, "config": {"extra": 3}},
    "j_blackboard": {"order": 48, "effect": "", "cost": 6, "config": {"extra": 3}},
    "j_runner": {"order": 49, "effect": "", "cost": 5, "config": {"extra": {"chips": 0, "chip_mod": 15}}},
    "j_ice_cream": {"order": 50, "effect": "", "cost": 5, "config": {"extra": {"chips": 100, "chip_mod": 5}}},
    "j_dna": {"order": 51, "effect": "", "cost": 8, "config": {}},
    "j_splash": {"order": 52, "effect": "", "cost": 3, "config": {}},
    "j_blue_joker": {"order": 53, "effect": "", "cost": 5, "config": {"extra": 2}},
    "j_sixth_sense": {"order": 54, "effect": "", "cost": 6, "config": {}},
    "j_constellation": {"order": 55, "effect": "", "cost": 6, "config": {"extra": 0.1, "Xmult": 1}},
    "j_hiker": {"order": 56, "effect": "", "cost": 5, "config": {"extra": 5}},
    "j_faceless": {"order": 57, "effect": "", "cost": 4, "config": {"extra": {"dollars": 5, "faces": 3}}},
    "j_green_joker": {"order": 58, "effect": "", "cost": 4, "config": {"extra": {"hand_add": 1, "discard_sub": 1}}},
    "j_superposition": {"order": 59, "effect": "", "cost": 4, "config": {}},
    "j_todo_list": {"order": 60, "effect": "", "cost": 4, "config": {"extra": {"dollars": 4, "poker_hand": "High Card"}}},
    "j_cavendish": {"order": 61, "effect": "", "cost": 4, "config": {"extra": {"odds": 1000, "Xmult": 3}}},
    "j_card_sharp": {"order": 62, "effect": "", "cost": 6, "config": {"extra": {"Xmult": 3}}},
    "j_red_card": {"order": 63, "effect": "", "cost": 5, "config": {"extra": 3}},
    "j_madness": {"order": 64, "effect": "", "cost": 7, "config": {"extra": 0.5}},
    "j_square": {"order": 65, "effect": "", "cost": 4, "config": {"extra": {"chips": 0, "chip_mod": 4}}},
    "j_seance": {"order": 66, "effect": "", "cost": 6, "config": {"extra": {"poker_hand": "Straight Flush"}}},
    "j_riff_raff": {"order": 67, "effect": "", "cost": 6, "config": {"extra": 2}},
    "j_vampire": {"order": 68, "effect": "", "cost": 7, "config": {"extra": 0.1, "Xmult": 1}},
    "j_shortcut": {"order": 69, "effect": "", "cost": 7, "config": {}},
    "j_hologram": {"order": 70, "effect": "", "cost": 7, "config": {"extra": 0.25, "Xmult": 1}},
    "j_vagabond": {"order": 71, "effect": "", "cost": 8, "config": {"extra": 4}},
    "j_baron": {"order": 72, "effect": "", "cost": 8, "config": {"extra": 1.5}},
    "j_cloud_9": {"order": 73, "effect": "", "cost": 7, "config": {"extra": 1}},
    "j_rocket": {"order": 74, "effect": "", "cost": 6, "config": {"extra": {"dollars": 1, "increase": 2}}},
    "j_obelisk": {"order": 75, "effect": "", "cost": 8, "config": {"extra": 0.2, "Xmult": 1}},
    "j_midas_mask": {"order": 76, "effect": "", "cost": 7, "config": {}},
    "j_luchador": {"order": 77, "effect": "", "cost": 5, "config": {}},
    "j_photograph": {"order": 78, "effect": "", "cost": 5, "config": {"extra": 2}},
    "j_gift": {"order": 79, "effect": "", "cost": 6, "config": {"extra": 1}},
    "j_turtle_bean": {"order": 80, "effect": "", "cost": 6, "config": {"extra": {"h_size": 5, "h_mod": 1}}},
    "j_erosion": {"order": 81, "effect": "", "cost": 6, "config": {"extra": 4}},
    "j_reserved_parking": {"order": 82, "effect": "", "cost": 6, "config": {"extra": {"odds": 2, "dollars": 1}}},
    "j_mail": {"order": 83, "effect": "", "cost": 4, "config": {"extra": 5}},
    "j_to_the_moon": {"order": 84, "effect": "", "cost": 5, "config": {"extra": 1}},
    "j_hallucination": {"order": 85, "effect": "", "cost": 4, "config": {"extra": 2}},
    "j_fortune_teller": {"order": 86, "effect": "", "cost": 6, "config": {"extra": 1}},
    "j_juggler": {"order": 87, "effect": "Hand Size", "cost": 4, "config": {"h_size": 1}},
    "j_drunkard": {"order": 88, "effect": "Discard Size", "cost": 4, "config": {"d_size": 1}},
    "j_stone": {"order": 89, "effect": "Stone Card Buff", "cost": 6, "config": {"extra": 25}},
    "j_golden": {"order": 90, "effect": "Bonus dollars", "cost": 6, "config": {"extra": 4}},
    "j_lucky_cat": {"order": 91, "effect": "", "cost": 6, "config": {"Xmult": 1, "extra": 0.25}},
    "j_baseball": {"order": 92, "effect": "", "cost": 8, "config": {"extra": 1.5}},
    "j_bull": {"order": 93, "effect": "", "cost": 6, "config": {"extra": 2}},
    "j_diet_cola": {"order": 94, "effect": "", "cost": 6, "config": {}},
    "j_trading": {"order": 95, "effect": "", "cost": 6, "config": {"extra": 3}},
    "j_flash": {"order": 96, "effect": "", "cost": 5, "config": {"extra": 2, "mult": 0}},
    "j_popcorn": {"order": 97, "effect": "", "cost": 5, "config": {"mult": 20, "extra": 4}},
    "j_trousers": {"order": 98, "effect": "", "cost": 6, "config": {"extra": 2}},
    "j_ancient": {"order": 99, "effect": "", "cost": 8, "config": {"extra": 1.5}},
    "j_ramen": {"order": 100, "effect": "", "cost": 6, "config": {"Xmult": 2, "extra": 0.01}},
    "j_walkie_talkie": {"order": 101, "effect": "", "cost": 4, "config": {"extra": {"chips": 10, "mult": 4}}},
    "j_selzer": {"order": 102, "effect": "", "cost": 6, "config": {"extra": 10}},
    "j_castle": {"order": 103, "effect": "", "cost": 6, "config": {"extra": {"chips": 0, "chip_mod": 3}}},
    "j_smiley": {"order": 104, "effect": "", "cost": 4, "config": {"extra": 5}},
    "j_campfire": {"order": 105, "effect": "", "cost": 9, "config": {"extra": 0.25}},
    "j_ticket": {"order": 106, "effect": "dollars for Gold cards", "cost": 5, "config": {"extra": 4}},
    "j_mr_bones": {"order": 107, "effect": "Prevent Death", "cost": 5, "config": {}},
    "j_acrobat": {"order": 108, "effect": "Shop size", "cost": 6, "config": {"extra": 3}},
    "j_sock_and_buskin": {"order": 109, "effect": "Face card double", "cost": 6, "config": {"extra": 1}},
    "j_swashbuckler": {"order": 110, "effect": "Set Mult", "cost": 4, "config": {"mult": 1}},
    "j_troubadour": {"order": 111, "effect": "Hand Size, Plays", "cost": 6, "config": {"extra": {"h_size": 2, "h_plays": -1}}},
    "j_certificate": {"order": 112, "effect": "", "cost": 6, "config": {}},
    "j_smeared": {"order": 113, "effect": "", "cost": 7, "config": {}},
    "j_throwback": {"order": 114, "effect": "", "cost": 6, "config": {"extra": 0.25}},
    "j_hanging_chad": {"order": 115, "effect": "", "cost": 4, "config": {"extra": 2}},
    "j_rough_gem": {"order": 116, "effect": "", "cost": 7, "config": {"extra": 1}},
    "j_bloodstone": {"order": 117, "effect": "", "cost": 7, "config": {"extra": {"odds": 2, "Xmult": 1.5}}},
    "j_arrowhead": {"order": 118, "effect": "", "cost": 7, "config": {"extra": 50}},
    "j_onyx_agate": {"order": 119, "effect": "", "cost": 7, "config": {"extra": 7}},
    "j_glass": {"order": 120, "effect": "Glass Card", "cost": 6, "config": {"extra": 0.75, "Xmult": 1}},
    "j_ring_master": {"order": 121, "effect": "", "cost": 5, "config": {}},
    "j_flower_pot": {"order": 122, "effect": "", "cost": 6, "config": {"extra": 3}},
    "j_blueprint": {"order": 123, "effect": "Copycat", "cost": 10, "config": {}},
    "j_wee": {"order": 124, "effect": "", "cost": 8, "config": {"extra": {"chips": 0, "chip_mod": 8}}},
    "j_merry_andy": {"order": 125, "effect": "", "cost": 7, "config": {"d_size": 3, "h_size": -1}},
    "j_oops": {"order": 126, "effect": "", "cost": 4, "config": {}},
    "j_idol": {"order": 127, "effect": "", "cost": 6, "config": {"extra": 2}},
    "j_seeing_double": {"order": 128, "effect": "X1.5 Mult club 7", "cost": 6, "config": {"extra": 2}},
    "j_matador": {"order": 129, "effect": "", "cost": 7, "config": {"extra": 8}},
    "j_hit_the_road": {"order": 130, "effect": "Jack Discard Effect", "cost": 8, "config": {"extra": 0.5}},
    "j_duo": {"order": 131, "effect": "X1.5 Mult", "cost": 8, "config": {"Xmult": 2, "type": "Pair"}},
    "j_trio": {"order": 132, "effect": "X2 Mult", "cost": 8, "config": {"Xmult": 3, "type": "Three of a Kind"}},
    "j_family": {"order": 133, "effect": "X3 Mult", "cost": 8, "config": {"Xmult": 4, "type": "Four of a Kind"}},
    "j_order": {"order": 134, "effect": "X3 Mult", "cost": 8, "config": {"Xmult": 3, "type": "Straight"}},
    "j_tribe": {"order": 135, "effect": "X3 Mult", "cost": 8, "config": {"Xmult": 2, "type": "Flush"}},
    "j_stuntman": {"order": 136, "effect": "", "cost": 7, "config": {"extra": {"h_size": 2, "chip_mod": 250}}},
    "j_invisible": {"order": 137, "effect": "", "cost": 8, "config": {"extra": 2}},
    "j_brainstorm": {"order": 138, "effect": "Copycat", "cost": 10, "config": {}},
    "j_satellite": {"order": 139, "effect": "", "cost": 6, "config": {"extra": 1}},
    "j_shoot_the_moon": {"order": 140, "effect": "", "cost": 5, "config": {"extra": 13}},
    "j_drivers_license": {"order": 141, "effect": "", "cost": 7, "config": {"extra": 3}},
    "j_cartomancer": {"order": 142, "effect": "Tarot Buff", "cost": 6, "config": {}},
    "j_astronomer": {"order": 143, "effect": "", "cost": 8, "config": {}},
    "j_burnt": {"order": 144, "effect": "", "cost": 8, "config": {"h_size": 0, "extra": 4}},
    "j_bootstraps": {"order": 145, "effect": "", "cost": 7, "config": {"extra": {"mult": 2, "dollars": 5}}},
    "j_caino": {"order": 146, "effect": "", "cost": 20, "config": {"extra": 1}},
    "j_triboulet": {"order": 147, "effect": "", "cost": 20, "config": {"extra": 2}},
    "j_yorick": {"order": 148, "effect": "", "cost": 20, "config": {"extra": {"xmult": 1, "discards": 23}}},
    "j_chicot": {"order": 149, "effect": "", "cost": 20, "config": {}},
    "j_perkeo": {"order": 150, "effect": "", "cost": 20, "config": {}},
}


def remove_joker(data, index):
    """Remove joker at given index (0-based)."""
    cards = _card_areas(data)["jokers"]["cards"]
    joker_list = _get_joker_list(cards)
    # Check if the joker being removed is negative
    if 0 <= index < len(joker_list):
        joker = joker_list[index]
        is_negative = isinstance(joker.get("edition"), dict) and joker["edition"].get("negative")
        if is_negative:
            cfg = _card_areas(data)["jokers"]["config"]
            cfg["card_limit"] = max(0, cfg.get("card_limit", 5) - 1)
    if isinstance(cards, list):
        if 0 <= index < len(cards):
            cards.pop(index)
    elif isinstance(cards, dict):
        int_keys = sorted([k for k in cards if isinstance(k, int)])
        if 0 <= index < len(int_keys):
            del cards[int_keys[index]]
            _reindex_dict(cards)
    _card_areas(data)["jokers"]["config"]["card_count"] = len(get_jokers(data))


def add_joker(data, joker_id, edition_key="base"):
    """Add a new joker to the active jokers with proper ability config from game source."""
    name = JOKER_MAP.get(joker_id, joker_id)
    jcfg = _JOKER_CONFIGS.get(joker_id, {"order": 1, "effect": "", "cost": 1, "config": {}})
    config = copy.deepcopy(jcfg["config"])

    ability = {
        "type": config.pop("type", ""),
        "hands_played_at_create": 0,
        "name": name,
        "effect": jcfg["effect"],
        "set": "Joker",
        "order": jcfg["order"],
        "h_mult": 0,
        "t_mult": config.pop("t_mult", 0),
        "t_chips": config.pop("t_chips", 0),
        "bonus": 0,
        "d_size": config.pop("d_size", 0),
        "p_dollars": 0,
        "mult": config.pop("mult", 0),
        "h_size": config.pop("h_size", 0),
        "x_mult": config.pop("Xmult", 1),
        "h_dollars": 0,
        "extra_value": 0,
        "perma_bonus": 0,
        "h_x_mult": 0,
    }
    # Remaining config fields (extra, etc.) go directly into ability
    for k, v in config.items():
        ability[k] = copy.deepcopy(v)

    # Special joker initializations (from Card:set_ability, card.lua lines 318-333)
    if name == "Invisible Joker":
        ability["invis_rounds"] = 0
    elif name == "Caino":
        ability["caino_xmult"] = 1
    elif name == "Yorick" and isinstance(ability.get("extra"), dict):
        ability["yorick_discards"] = ability["extra"].get("discards", 23)
    elif name == "Loyalty Card" and isinstance(ability.get("extra"), dict):
        ability["burnt_hand"] = 0
        ability["loyalty_remaining"] = ability["extra"].get("every", 5)
    elif name == "To Do List" and isinstance(ability.get("extra"), dict):
        ability["to_do_poker_hand"] = ability["extra"].get("poker_hand", "High Card")

    joker = {
        "save_fields": {"center": joker_id},
        "ability": ability,
        "facing": "front",
        "base": {
            "face_nominal": 0,
            "times_played": 0,
            "nominal": 0,
            "suit_nominal": 0,
        },
        "sell_cost": max(1, jcfg["cost"] // 2),
        "base_cost": jcfg["cost"],
        "extra_cost": 0,
        "params": {},
        "label": name,
        "cost": jcfg["cost"],
        "sort_id": 1,
        "debuff": False,
        "sprite_facing": "front",
        "rank": 1,
    }

    if edition_key != "base":
        set_joker_edition(joker, edition_key)
        # Update cost for edition (matches Card:set_cost from game source)
        ed = joker.get("edition", {})
        ed_cost = ((ed.get("foil") and 2) or 0) + ((ed.get("holo") and 3) or 0) + \
                  ((ed.get("polychrome") and 5) or 0) + ((ed.get("negative") and 5) or 0)
        joker["extra_cost"] = ed_cost
        joker["cost"] = max(1, int((jcfg["cost"] + ed_cost + 0.5)))
        joker["sell_cost"] = max(1, joker["cost"] // 2)

    cards = _card_areas(data)["jokers"]["cards"]
    if isinstance(cards, list):
        cards.append(joker)
    elif isinstance(cards, dict):
        next_key = max([k for k in cards if isinstance(k, int)], default=0) + 1
        cards[next_key] = joker
    _card_areas(data)["jokers"]["config"]["card_count"] = len(get_jokers(data))

    # Negative edition: +1 joker slot (matches Card:set_edition from game source)
    if edition_key == "negative":
        cfg = _card_areas(data)["jokers"]["config"]
        cfg["card_limit"] = cfg.get("card_limit", 5) + 1

    return joker


# ── Deck / Playing Cards ──────────────────────────────────────

def _all_playing_cards(data):
    """Return all playing cards across deck, hand, and discard areas."""
    areas = _card_areas(data)
    result = []
    for area_name in ("deck", "hand", "discard"):
        area = areas.get(area_name, {})
        cards = area.get("cards", {})
        if isinstance(cards, list):
            for c in cards:
                result.append((area_name, c))
        elif isinstance(cards, dict):
            for k in sorted(cards.keys()):
                if isinstance(k, int):
                    result.append((area_name, cards[k]))
    return result


def get_playing_cards(data):
    """Return list of (area_name, card_info_dict) for all playing cards."""
    results = []
    for area_name, card in _all_playing_cards(data):
        base = card.get("base", {})
        sf = card.get("save_fields", {})
        card_code = sf.get("card", "")
        suit_code = card_code.split("_")[0] if "_" in card_code else ""
        rank_code = card_code.split("_")[1] if "_" in card_code else ""
        suit = SUIT_CODES.get(suit_code, base.get("suit", "?"))
        rank = RANK_CODES.get(rank_code, base.get("value", "?"))
        enhancement = sf.get("center", "c_base")
        edition = _get_edition_name(card)
        seal = card.get("seal", None)
        results.append({
            "area": area_name,
            "suit": suit,
            "rank": rank,
            "card_code": card_code,
            "enhancement": enhancement,
            "edition": edition,
            "seal": seal,
            "card": card,
        })
    return results


# Enhancement config data extracted from game source (game.lua lines 648-655).
# Maps center_id → the config dict that Card:set_ability uses to build ability fields.
# In set_ability:
#   mult = config.mult or 0
#   h_mult = config.h_mult or 0
#   h_x_mult = config.h_x_mult or 0
#   h_dollars = config.h_dollars or 0
#   p_dollars = config.p_dollars or 0
#   t_mult = config.t_mult or 0
#   t_chips = config.t_chips or 0
#   x_mult = config.Xmult or 1          ← note: Xmult in config → x_mult in ability
#   extra = copy_table(config.extra) or nil
#   bonus is ADDITIVE onto any existing: (self.ability.bonus or 0) + (config.bonus or 0)
_ENHANCEMENT_CONFIGS = {
    "c_base":   {},
    "m_bonus":  {"bonus": 30},
    "m_mult":   {"mult": 4},
    "m_wild":   {},
    "m_glass":  {"Xmult": 2, "extra": 4},
    "m_steel":  {"h_x_mult": 1.5},
    "m_stone":  {"bonus": 50},
    "m_gold":   {"h_dollars": 3},
    "m_lucky":  {"mult": 20, "p_dollars": 20},
}


def set_card_enhancement(card_obj, enhancement_id):
    """Set enhancement on a playing card, exactly mirroring Card:set_ability from game source.

    Rebuilds the ability table the same way the game does, preserving persistent
    fields (perma_bonus, hands_played_at_create, forced_selection, set) while
    resetting all enhancement-driven fields from the new center's config.
    """
    card_obj["save_fields"]["center"] = enhancement_id
    ability = card_obj.setdefault("ability", {})
    cfg = _ENHANCEMENT_CONFIGS.get(enhancement_id, {})

    # Look up effect/name from ENHANCEMENTS list
    effect = "Base"
    name = "Default Base"
    order = None
    for eid, ename, eff, desc in ENHANCEMENTS:
        if eid == enhancement_id:
            effect = eff
            name = "Default Base" if eid == "c_base" else eff
            break
    # Get order from game source config list
    _enh_orders = {
        "m_bonus": 2, "m_mult": 3, "m_wild": 4, "m_glass": 5,
        "m_steel": 6, "m_stone": 7, "m_gold": 8, "m_lucky": 9,
    }
    order = _enh_orders.get(enhancement_id)

    # Preserve persistent fields that survive enhancement changes
    perma_bonus = ability.get("perma_bonus", 0)
    hands_played = ability.get("hands_played_at_create", 0)
    forced_sel = ability.get("forced_selection")
    extra_value = ability.get("extra_value", 0)

    # Rebuild ability exactly as Card:set_ability does (card.lua lines 289-310)
    ability["name"] = name
    ability["effect"] = effect
    ability["set"] = ability.get("set", "Default")
    ability["mult"] = cfg.get("mult", 0)
    ability["h_mult"] = cfg.get("h_mult", 0)
    ability["h_x_mult"] = cfg.get("h_x_mult", 0)
    ability["h_dollars"] = cfg.get("h_dollars", 0)
    ability["p_dollars"] = cfg.get("p_dollars", 0)
    ability["t_mult"] = cfg.get("t_mult", 0)
    ability["t_chips"] = cfg.get("t_chips", 0)
    ability["x_mult"] = cfg.get("Xmult", 1)
    ability["h_size"] = cfg.get("h_size", 0)
    ability["d_size"] = cfg.get("d_size", 0)
    ability["type"] = cfg.get("type", "")
    ability["extra_value"] = extra_value
    ability["perma_bonus"] = perma_bonus
    ability["hands_played_at_create"] = hands_played
    if forced_sel is not None:
        ability["forced_selection"] = forced_sel
    elif "forced_selection" in ability:
        del ability["forced_selection"]
    if order is not None:
        ability["order"] = order
    elif "order" in ability:
        del ability["order"]

    # extra: deep copy from config, or remove if not present
    if "extra" in cfg:
        ability["extra"] = copy.deepcopy(cfg["extra"])
    elif "extra" in ability:
        del ability["extra"]

    # bonus is additive in the game, but since we're setting from scratch
    # on a playing card, just set it directly from config
    ability["bonus"] = cfg.get("bonus", 0)

    # Update label
    if enhancement_id == "c_base":
        card_obj["label"] = "Base Card"
    else:
        card_obj["label"] = name


def repair_cards(data):
    """Fix any playing cards with broken enhancement/edition configs.

    Checks every playing card in deck, hand, and discard for:
    1. Missing or wrong ability fields for the card's enhancement
    2. Incomplete edition dicts (missing type, stat fields)
    3. Mismatched effect/name vs center
    """
    repaired = 0
    for area_name, card in _all_playing_cards(data):
        center = card.get("save_fields", {}).get("center", "c_base")
        cfg = _ENHANCEMENT_CONFIGS.get(center, {})
        ability = card.get("ability", {})

        # --- Enhancement ability field repairs ---

        # Check x_mult (Xmult in config → x_mult in ability)
        expected_x_mult = cfg.get("Xmult", 1)
        if ability.get("x_mult") != expected_x_mult:
            ability["x_mult"] = expected_x_mult
            repaired += 1

        # Check extra
        if "extra" in cfg:
            if "extra" not in ability or ability["extra"] != cfg["extra"]:
                ability["extra"] = copy.deepcopy(cfg["extra"])
                repaired += 1
        # Don't remove extra if not in config — it might be from a valid prior state

        # Check all simple numeric config fields
        for field in ("mult", "h_mult", "h_x_mult", "h_dollars", "p_dollars",
                       "t_mult", "t_chips", "h_size", "d_size"):
            expected = cfg.get(field, 0)
            if field in cfg and ability.get(field) != expected:
                ability[field] = expected
                repaired += 1

        # Check bonus
        if "bonus" in cfg:
            if ability.get("bonus") != cfg["bonus"]:
                ability["bonus"] = cfg["bonus"]
                repaired += 1

        # Check effect/name match center
        if center != "c_base":
            for eid, ename, effect, desc in ENHANCEMENTS:
                if eid == center:
                    if ability.get("effect") != effect:
                        ability["effect"] = effect
                        repaired += 1
                    if ability.get("name") != effect:
                        ability["name"] = effect
                        repaired += 1
                    break

        # Ensure all base ability fields exist
        for field, default in (("bonus", 0), ("mult", 0), ("h_mult", 0),
                                ("h_x_mult", 0), ("h_dollars", 0), ("p_dollars", 0),
                                ("t_mult", 0), ("t_chips", 0), ("x_mult", 1),
                                ("h_size", 0), ("d_size", 0), ("type", ""),
                                ("extra_value", 0), ("perma_bonus", 0),
                                ("set", "Default"), ("effect", "Base"),
                                ("name", "Default Base")):
            if field not in ability:
                ability[field] = default
                repaired += 1

        # --- Edition repairs ---
        ed = card.get("edition")
        if isinstance(ed, dict) and ed:
            ed_key = _get_edition_name(card)
            if ed_key != "base":
                for eid, ename, edesc, ed_dict in EDITIONS:
                    if eid == ed_key:
                        for k, v in ed_dict.items():
                            if k not in ed:
                                ed[k] = v
                                repaired += 1
                        break

    # --- Joker card_limit repair: account for negative jokers ---
    joker_cards = _card_areas(data).get("jokers", {}).get("cards", {})
    joker_list = _get_joker_list(joker_cards)
    neg_count = sum(
        1 for j in joker_list
        if isinstance(j.get("edition"), dict) and j["edition"].get("negative")
    )
    cfg = _card_areas(data).get("jokers", {}).get("config", {})
    current_limit = cfg.get("card_limit", 5)
    # Each negative joker should add +1 to card_limit.
    # If card_limit doesn't already include negatives, add them.
    # Heuristic: if current_limit + neg_count would fit all jokers, assume
    # the negatives weren't counted and fix it.
    expected_min = current_limit + neg_count
    if neg_count > 0 and current_limit < expected_min:
        cfg["card_limit"] = expected_min
        repaired += 1

    # Also repair joker edition dicts
    for j in joker_list:
        ed = j.get("edition")
        if isinstance(ed, dict) and ed:
            ed_key = _get_edition_name(j)
            if ed_key != "base":
                for eid, ename, edesc, ed_dict in EDITIONS:
                    if eid == ed_key:
                        for k, v in ed_dict.items():
                            if k not in ed:
                                ed[k] = v
                                repaired += 1
                        break

    return repaired


def set_card_edition(card_obj, edition_key):
    """Set edition on a playing card."""
    for eid, ename, edesc, ed_dict in EDITIONS:
        if eid == edition_key:
            if ed_dict is None:
                if "edition" in card_obj:
                    del card_obj["edition"]
            else:
                card_obj["edition"] = dict(ed_dict)
            return


def set_card_seal(card_obj, seal_value):
    """Set seal on a playing card. None removes seal."""
    if seal_value is None:
        if "seal" in card_obj:
            del card_obj["seal"]
    else:
        card_obj["seal"] = seal_value


def _reindex_dict(d):
    """Re-index integer keys in a dict to be sequential from 1."""
    int_items = [(k, d[k]) for k in sorted(d.keys()) if isinstance(k, int)]
    for k, _ in int_items:
        del d[k]
    for i, (_, v) in enumerate(int_items):
        d[i + 1] = v
