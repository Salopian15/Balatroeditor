"""
Balatro game data constants — joker IDs, enhancements, editions, seals, suits, ranks.
"""

# All jokers: (internal_id, display_name, description, rarity)
# Rarity: "Common", "Uncommon", "Rare", "Legendary"
JOKERS = [
    ("j_joker", "Joker", "+4 Mult", "Common"),
    ("j_greedy_joker", "Greedy Joker", "+3 Mult for each played Diamond", "Common"),
    ("j_lusty_joker", "Lusty Joker", "+3 Mult for each played Heart", "Common"),
    ("j_wrathful_joker", "Wrathful Joker", "+3 Mult for each played Spade", "Common"),
    ("j_gluttenous_joker", "Gluttonous Joker", "+3 Mult for each played Club", "Common"),
    ("j_jolly", "Jolly Joker", "+8 Mult if hand contains a Pair", "Common"),
    ("j_zany", "Zany Joker", "+12 Mult if hand contains a Three of a Kind", "Common"),
    ("j_mad", "Mad Joker", "+10 Mult if hand contains a Two Pair", "Common"),
    ("j_crazy", "Crazy Joker", "+12 Mult if hand contains a Straight", "Common"),
    ("j_droll", "Droll Joker", "+10 Mult if hand contains a Flush", "Common"),
    ("j_sly", "Sly Joker", "+50 Chips if hand contains a Pair", "Common"),
    ("j_wily", "Wily Joker", "+100 Chips if hand contains a Three of a Kind", "Common"),
    ("j_clever", "Clever Joker", "+80 Chips if hand contains a Two Pair", "Common"),
    ("j_devious", "Devious Joker", "+100 Chips if hand contains a Straight", "Common"),
    ("j_crafty", "Crafty Joker", "+80 Chips if hand contains a Flush", "Common"),
    ("j_half", "Half Joker", "+20 Mult if hand has 3 or fewer cards", "Common"),
    ("j_stencil", "Joker Stencil", "x1 Mult for each empty Joker slot", "Common"),
    ("j_four_fingers", "Four Fingers", "Flushes and Straights can be made with 4 cards", "Uncommon"),
    ("j_mime", "Mime", "Retrigger all card held in hand abilities", "Uncommon"),
    ("j_credit_card", "Credit Card", "Go up to -$20 in debt", "Common"),
    ("j_ceremonial", "Ceremonial Dagger", "When Blind is selected, destroy Joker to the right and add double its sell value as permanent +Mult", "Uncommon"),
    ("j_banner", "Banner", "+30 Chips for each remaining discard", "Common"),
    ("j_mystic_summit", "Mystic Summit", "+15 Mult when 0 discards remaining", "Common"),
    ("j_marble", "Marble Joker", "Adds a Stone card to your deck when Blind is selected", "Uncommon"),
    ("j_loyalty_card", "Loyalty Card", "x4 Mult every 5 hands played", "Uncommon"),
    ("j_8_ball", "8 Ball", "1 in 4 chance for each played 8 to create a Tarot card", "Common"),
    ("j_misprint", "Misprint", "+? Mult (random between 0 and 23)", "Common"),
    ("j_dusk", "Dusk", "Retrigger all played cards on final hand of round", "Uncommon"),
    ("j_raised_fist", "Raised Fist", "Adds double the rank of lowest held card as Mult", "Common"),
    ("j_chaos", "Chaos the Clown", "1 free reroll per shop visit", "Common"),
    ("j_fibonacci", "Fibonacci", "+8 Mult for each played Ace, 2, 3, 5, or 8", "Uncommon"),
    ("j_steel_joker", "Steel Joker", "+0.2x Mult for each Steel Card in full deck", "Uncommon"),
    ("j_scary_face", "Scary Face", "+30 Chips if played card is a face card", "Common"),
    ("j_abstract", "Abstract Joker", "+3 Mult for each Joker you own", "Common"),
    ("j_delayed_grat", "Delayed Gratification", "Earn $2 per discard if no discards used by end of round", "Common"),
    ("j_hack", "Hack", "Retrigger each played 2, 3, 4, or 5", "Uncommon"),
    ("j_pareidolia", "Pareidolia", "All cards are considered face cards", "Uncommon"),
    ("j_gros_michel", "Gros Michel", "+15 Mult. 1 in 6 chance to be destroyed at end of round", "Common"),
    ("j_even_steven", "Even Steven", "+4 Mult if played card has even rank (10, 8, 6, 4, 2)", "Common"),
    ("j_odd_todd", "Odd Todd", "+31 Chips if played card has odd rank (A, 9, 7, 5, 3)", "Common"),
    ("j_scholar", "Scholar", "+20 Chips and +4 Mult if played card is an Ace", "Common"),
    ("j_business", "Business Card", "1 in 2 chance to earn $2 when face card is played", "Common"),
    ("j_supernova", "Supernova", "Adds the number of times poker hand has been played as Mult", "Common"),
    ("j_ride_the_bus", "Ride the Bus", "+1 Mult per consecutive hand without a face card", "Common"),
    ("j_space", "Space Joker", "1 in 4 chance to upgrade played hand level", "Uncommon"),
    ("j_egg", "Egg", "Gains $3 of sell value at end of round", "Common"),
    ("j_burglar", "Burglar", "+3 Hands when Blind is selected, lose all discards", "Uncommon"),
    ("j_blackboard", "Blackboard", "x3 Mult if all held cards are Spades or Clubs", "Uncommon"),
    ("j_runner", "Runner", "+15 Chips if played hand contains a Straight, gains +15 Chips", "Common"),
    ("j_ice_cream", "Ice Cream", "+100 Chips. -5 Chips for each hand played", "Common"),
    ("j_dna", "DNA", "First played card is permanently copied to hand on first hand of round", "Rare"),
    ("j_splash", "Splash", "Every played card counts in scoring", "Uncommon"),
    ("j_blue_joker", "Blue Joker", "+2 Chips for each remaining card in deck", "Common"),
    ("j_sixth_sense", "Sixth Sense", "Destroy played 6 on first hand, create a Spectral card", "Uncommon"),
    ("j_constellation", "Constellation", "+0.1x Mult every time a Planet card is used", "Uncommon"),
    ("j_hiker", "Hiker", "Every played card permanently gains +5 Chips", "Uncommon"),
    ("j_faceless", "Faceless Joker", "Earn $5 if 3+ face cards are discarded at the same time", "Common"),
    ("j_green_joker", "Green Joker", "+1 Mult per hand played, -1 Mult per discard", "Common"),
    ("j_superposition", "Superposition", "Create a Tarot card if hand contains an Ace and a Straight", "Common"),
    ("j_todo_list", "To Do List", "Earn $4 if poker hand is a listed type", "Common"),
    ("j_cavendish", "Cavendish", "x3 Mult. 1 in 1000 chance to be destroyed at end of round", "Common"),
    ("j_card_sharp", "Card Sharp", "x3 Mult if played poker hand was already played this round", "Uncommon"),
    ("j_red_card", "Red Card", "+3 Mult when any Booster Pack is skipped", "Common"),
    ("j_madness", "Madness", "x0.5 Mult when Blind is selected; destroy a random Joker. x1 Mult when Boss Blind is selected", "Uncommon"),
    ("j_square", "Square Joker", "+4 Chips if played hand has exactly 4 cards, gains +4 Chips", "Common"),
    ("j_seance", "Séance", "Create a Spectral card if poker hand is a Straight Flush", "Uncommon"),
    ("j_riff_raff", "Riff-Raff", "Create 2 Common Jokers when Blind is selected (must have room)", "Common"),
    ("j_vampire", "Vampire", "x0.1 Mult per enhanced card played; removes enhancement", "Uncommon"),
    ("j_shortcut", "Shortcut", "Straights can have gaps of 1 rank (e.g. 2 4 6 8 10)", "Uncommon"),
    ("j_hologram", "Hologram", "+0.25x Mult per card added to deck", "Uncommon"),
    ("j_vagabond", "Vagabond", "Create a Tarot card when hand is played with $4 or less", "Uncommon"),
    ("j_baron", "Baron", "x1.5 Mult for each King held in hand", "Rare"),
    ("j_cloud_9", "Cloud 9", "Earn $1 per 9 in your full deck at end of round", "Common"),
    ("j_rocket", "Rocket", "Earn $1 at end of round. Payout increases by $2 when Boss Blind is defeated", "Uncommon"),
    ("j_obelisk", "Obelisk", "x0.2 Mult per consecutive hand played not being your most played hand", "Rare"),
    ("j_midas_mask", "Midas Mask", "All played face cards become Gold cards", "Uncommon"),
    ("j_luchador", "Luchador", "Sell to disable current Boss Blind effect", "Uncommon"),
    ("j_photograph", "Photograph", "x2 Mult for first played face card", "Common"),
    ("j_gift", "Gift Card", "+1 to sell value of all Jokers and Consumables at end of round", "Uncommon"),
    ("j_turtle_bean", "Turtle Bean", "+5 hand size, reduces by 1 each round", "Uncommon"),
    ("j_erosion", "Erosion", "+4 Mult for each card below the starting deck size", "Uncommon"),
    ("j_reserved_parking", "Reserved Parking", "1 in 2 chance for each face card held to earn $1", "Common"),
    ("j_mail", "Mail-In Rebate", "Earn $5 if discarded hand has a designated rank", "Common"),
    ("j_to_the_moon", "To the Moon", "Earn extra $1 of interest for every $5, max $20", "Uncommon"),
    ("j_hallucination", "Hallucination", "1 in 2 chance to create a Tarot card after opening a Booster Pack", "Common"),
    ("j_fortune_teller", "Fortune Teller", "+1 Mult per Tarot card used this run", "Common"),
    ("j_juggler", "Juggler", "+1 hand size", "Common"),
    ("j_drunkard", "Drunkard", "+1 discard per round", "Common"),
    ("j_stone", "Stone Joker", "+25 Chips for each Stone Card in full deck", "Uncommon"),
    ("j_golden", "Golden Joker", "Earn $4 at end of round", "Common"),
    ("j_lucky_cat", "Lucky Cat", "+0.25x Mult each time a Lucky card triggers", "Uncommon"),
    ("j_baseball", "Baseball Card", "Uncommon Jokers give x1.5 Mult", "Rare"),
    ("j_bull", "Bull", "+2 Chips per $1 you have", "Uncommon"),
    ("j_diet_cola", "Diet Cola", "Sell to create a free Double Tag", "Uncommon"),
    ("j_trading", "Trading Card", "Discard 1 card, if first discard, create a random Tarot card and destroy it", "Uncommon"),
    ("j_flash", "Flash Card", "+2 Mult per reroll in the shop", "Uncommon"),
    ("j_popcorn", "Popcorn", "+20 Mult, -4 Mult per round played", "Common"),
    ("j_trousers", "Spare Trousers", "+2 Mult if played hand contains a Two Pair", "Common"),
    ("j_ancient", "Ancient Joker", "Each played card of a random suit gives x1.5 Mult", "Rare"),
    ("j_ramen", "Ramen", "x2 Mult, lose x0.01 Mult per card discarded", "Uncommon"),
    ("j_walkie_talkie", "Walkie Talkie", "+10 Chips and +4 Mult if played card is a 10 or 4", "Common"),
    ("j_selzer", "Seltzer", "Retrigger all played cards for the next 10 hands", "Uncommon"),
    ("j_castle", "Castle", "+3 Chips per discarded card, suit changes each round", "Uncommon"),
    ("j_smiley", "Smiley Face", "+5 Mult if played card is a face card", "Common"),
    ("j_campfire", "Campfire", "x0.25 Mult for each card sold, resets when Boss Blind is defeated", "Rare"),
    ("j_ticket", "Golden Ticket", "Earn $4 when a Gold card is played", "Common"),
    ("j_mr_bones", "Mr. Bones", "Prevents death if chips scored are at least 25% of required. Self-destructs", "Uncommon"),
    ("j_acrobat", "Acrobat", "x3 Mult on final hand of round", "Uncommon"),
    ("j_sock_and_buskin", "Sock and Buskin", "Retrigger all played face cards", "Uncommon"),
    ("j_swashbuckler", "Swashbuckler", "Adds sell value of all owned Jokers as Mult", "Common"),
    ("j_troubadour", "Troubadour", "+2 hand size, -1 hand per round", "Uncommon"),
    ("j_certificate", "Certificate", "First card dealt each round gets a random seal", "Uncommon"),
    ("j_smeared", "Smeared Joker", "Hearts and Diamonds count as the same suit. Spades and Clubs count as the same suit", "Uncommon"),
    ("j_throwback", "Throwback", "x0.25 Mult for each Blind skipped this run", "Uncommon"),
    ("j_hanging_chad", "Hanging Chad", "Retrigger first played card 2 additional times", "Common"),
    ("j_rough_gem", "Rough Gem", "Played Diamonds earn $1", "Uncommon"),
    ("j_bloodstone", "Bloodstone", "1 in 2 chance for played Hearts to give x1.5 Mult", "Uncommon"),
    ("j_arrowhead", "Arrowhead", "+50 Chips for each played Spade", "Uncommon"),
    ("j_onyx_agate", "Onyx Agate", "+7 Mult for each played Club", "Uncommon"),
    ("j_glass", "Glass Joker", "x0.75 Mult for every Glass Card that is destroyed", "Uncommon"),
    ("j_ring_master", "Showman", "Joker, Tarot, Planet, and Spectral cards may appear multiple times", "Uncommon"),
    ("j_flower_pot", "Flower Pot", "x3 Mult if hand has a Diamond, Club, Heart, and Spade card", "Uncommon"),
    ("j_blueprint", "Blueprint", "Copies ability of Joker to the right", "Rare"),
    ("j_wee", "Wee Joker", "+8 Chips when each played 2 is scored, gains +8 Chips", "Common"),
    ("j_merry_andy", "Merry Andy", "+3 discards per round, -1 hand size", "Uncommon"),
    ("j_oops", "Oops! All 6s", "Doubles all listed probabilities (1 in 3 → 2 in 3)", "Uncommon"),
    ("j_idol", "The Idol", "x2 Mult for each played card of a random rank and suit", "Uncommon"),
    ("j_seeing_double", "Seeing Double", "x2 Mult if hand has a Club card and a card of any other suit", "Uncommon"),
    ("j_matador", "Matador", "Earn $8 when Boss Blind ability is triggered", "Uncommon"),
    ("j_hit_the_road", "Hit the Road", "x0.5 Mult for each Jack discarded this round", "Rare"),
    ("j_duo", "The Duo", "x2 Mult if hand contains a Pair", "Rare"),
    ("j_trio", "The Trio", "x3 Mult if hand contains a Three of a Kind", "Rare"),
    ("j_family", "The Family", "x4 Mult if hand contains a Four of a Kind", "Rare"),
    ("j_order", "The Order", "x3 Mult if hand contains a Straight", "Rare"),
    ("j_tribe", "The Tribe", "x2 Mult if hand contains a Flush", "Rare"),
    ("j_stuntman", "Stuntman", "+250 Chips, -2 hand size", "Uncommon"),
    ("j_invisible", "Invisible Joker", "After 2 rounds, sell to duplicate a random Joker", "Rare"),
    ("j_brainstorm", "Brainstorm", "Copies the ability of the leftmost Joker", "Rare"),
    ("j_satellite", "Satellite", "Earn $1 per unique Planet card used this run at end of round", "Uncommon"),
    ("j_shoot_the_moon", "Shoot the Moon", "+13 Mult for each Queen held in hand", "Uncommon"),
    ("j_drivers_license", "Driver's License", "x3 Mult if you have 16+ Enhanced cards in your full deck", "Rare"),
    ("j_cartomancer", "Cartomancer", "Creates a Tarot card when Blind is selected", "Uncommon"),
    ("j_astronomer", "Astronomer", "All Planet cards and Celestial Packs in shop are free", "Uncommon"),
    ("j_burnt", "Burnt Joker", "Upgrade level of first discarded poker hand each round", "Uncommon"),
    ("j_bootstraps", "Bootstraps", "+2 Mult for every $5 you have", "Uncommon"),
    ("j_caino", "Caino", "x1 Mult. Gains x1 Mult when a face card is destroyed", "Legendary"),
    ("j_triboulet", "Triboulet", "x2 Mult for played Kings and Queens", "Legendary"),
    ("j_yorick", "Yorick", "x1 Mult. Gains x1 Mult every 23 cards discarded", "Legendary"),
    ("j_chicot", "Chicot", "Disables effect of every Boss Blind", "Legendary"),
    ("j_perkeo", "Perkeo", "Creates a Negative copy of 1 random consumable card at end of shop", "Legendary"),
]

JOKER_MAP = {jid: name for jid, name, *_ in JOKERS}
JOKER_NAME_MAP = {name: jid for jid, name, *_ in JOKERS}
JOKER_DESC = {jid: desc for jid, name, desc, *_ in JOKERS}
JOKER_RARITY = {jid: rarity for jid, name, desc, rarity in JOKERS}

# Card enhancements: (center_id, display_name, ability_effect, description)
ENHANCEMENTS = [
    ("c_base", "None", "Base", "No enhancement"),
    ("m_bonus", "Bonus", "Bonus Card", "+30 Chips"),
    ("m_mult", "Mult", "Mult Card", "+4 Mult"),
    ("m_wild", "Wild", "Wild Card", "Any suit"),
    ("m_glass", "Glass", "Glass Card", "x2 Mult, chance to break"),
    ("m_steel", "Steel", "Steel Card", "x1.5 Mult while in hand"),
    ("m_stone", "Stone", "Stone Card", "+50 Chips, no rank/suit"),
    ("m_gold", "Gold", "Gold Card", "+$3 at end of round"),
    ("m_lucky", "Lucky", "Lucky Card", "1 in 5 chance +20 Mult, 1 in 15 chance +$20"),
]

ENHANCEMENT_MAP = {eid: name for eid, name, *_ in ENHANCEMENTS}
ENHANCEMENT_NAME_MAP = {name: eid for eid, name, *_ in ENHANCEMENTS}

# Editions
EDITIONS = [
    ("base", "None", "No edition", None),
    ("foil", "Foil", "+50 Chips", {"type": "foil", "foil": True, "chips": 50}),
    ("holo", "Holographic", "+10 Mult", {"type": "holo", "holo": True, "mult": 10}),
    ("polychrome", "Polychrome", "x1.5 Mult", {"type": "polychrome", "polychrome": True, "x_mult": 1.5}),
    ("negative", "Negative", "+1 Joker slot", {"type": "negative", "negative": True}),
]

EDITION_MAP = {eid: name for eid, name, *_ in EDITIONS}
EDITION_NAME_MAP = {name: eid for eid, name, *_ in EDITIONS}

# Seals
SEALS = [
    (None, "None", "No seal"),
    ("Gold", "Gold", "Earn $3 when played"),
    ("Red", "Red", "Retrigger card"),
    ("Blue", "Blue", "Planet card on final hand"),
    ("Purple", "Purple", "Tarot card on discard"),
]

SEAL_MAP = {sid: name for sid, name, *_ in SEALS}
SEAL_NAME_MAP = {name: sid for sid, name, *_ in SEALS}

# Suits
SUITS = ["Hearts", "Diamonds", "Clubs", "Spades"]
SUIT_CODES = {"H": "Hearts", "D": "Diamonds", "C": "Clubs", "S": "Spades"}
SUIT_CODE_REV = {v: k for k, v in SUIT_CODES.items()}

# Ranks (display name → card code suffix, nominal value)
RANKS = [
    ("2", "2", 2),
    ("3", "3", 3),
    ("4", "4", 4),
    ("5", "5", 5),
    ("6", "6", 6),
    ("7", "7", 7),
    ("8", "8", 8),
    ("9", "9", 9),
    ("10", "T", 10),
    ("Jack", "J", 11),
    ("Queen", "Q", 12),
    ("King", "K", 13),
    ("Ace", "A", 14),
]

RANK_CODES = {code: name for name, code, _ in RANKS}
RANK_CODE_REV = {name: code for name, code, _ in RANKS}
RANK_NOMINAL = {name: nom for name, _, nom in RANKS}

# Suit colours for GUI
SUIT_COLOURS = {
    "Hearts": "#e74c3c",
    "Diamonds": "#e67e22",
    "Clubs": "#27ae60",
    "Spades": "#2c3e50",
}

# Edition colours for GUI indicators
EDITION_COLOURS = {
    "base": None,
    "foil": "#a8d8ea",
    "holo": "#c39bd3",
    "polychrome": "#f39c12",
    "negative": "#2c3e50",
}

# Seal colours for GUI indicators
SEAL_COLOURS = {
    None: None,
    "Gold": "#f1c40f",
    "Red": "#e74c3c",
    "Blue": "#3498db",
    "Purple": "#8e44ad",
}

# Enhancement colours for GUI indicators
ENHANCEMENT_COLOURS = {
    "c_base": None,
    "m_bonus": "#3498db",
    "m_mult": "#e74c3c",
    "m_wild": "#27ae60",
    "m_glass": "#85c1e9",
    "m_steel": "#95a5a6",
    "m_stone": "#7f8c8d",
    "m_gold": "#f1c40f",
    "m_lucky": "#2ecc71",
}

# ── Lookup helpers ─────────────────────────────────────────────────────────────
# Use these instead of manually looping through lists to convert display names
# to internal IDs.  Each returns a default if the name is not found.

def edition_name_to_id(name: str, default: str = "base") -> str:
    """Convert an edition display name (e.g. 'Holographic') to its internal key."""
    return EDITION_NAME_MAP.get(name, default)

def enhancement_name_to_id(name: str, default: str = "c_base") -> str:
    """Convert an enhancement display name (e.g. 'Glass') to its internal key."""
    return ENHANCEMENT_NAME_MAP.get(name, default)

def seal_name_to_id(name: str, default=None):
    """Convert a seal display name (e.g. 'Gold') to its internal value (or None)."""
    return SEAL_NAME_MAP.get(name, default)

def jokers_by_rarity() -> dict:
    """Return a dict mapping rarity → list of (jid, name, desc) tuples, order preserved."""
    groups: dict = {}
    for jid, name, desc, rarity in JOKERS:
        groups.setdefault(rarity, []).append((jid, name, desc))
    return groups
