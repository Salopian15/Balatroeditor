"""
Balatro game data constants — joker IDs, enhancements, editions, seals, suits, ranks.
"""

# All jokers: (internal_id, display_name, description)
JOKERS = [
    ("j_joker", "Joker", "+4 Mult"),
    ("j_greedy_joker", "Greedy Joker", "+3 Mult for each played Diamond"),
    ("j_lusty_joker", "Lusty Joker", "+3 Mult for each played Heart"),
    ("j_wrathful_joker", "Wrathful Joker", "+3 Mult for each played Spade"),
    ("j_gluttenous_joker", "Gluttonous Joker", "+3 Mult for each played Club"),
    ("j_jolly", "Jolly Joker", "+8 Mult if hand contains a Pair"),
    ("j_zany", "Zany Joker", "+12 Mult if hand contains a Three of a Kind"),
    ("j_mad", "Mad Joker", "+10 Mult if hand contains a Two Pair"),
    ("j_crazy", "Crazy Joker", "+12 Mult if hand contains a Straight"),
    ("j_droll", "Droll Joker", "+10 Mult if hand contains a Flush"),
    ("j_sly", "Sly Joker", "+50 Chips if hand contains a Pair"),
    ("j_wily", "Wily Joker", "+100 Chips if hand contains a Three of a Kind"),
    ("j_clever", "Clever Joker", "+80 Chips if hand contains a Two Pair"),
    ("j_devious", "Devious Joker", "+100 Chips if hand contains a Straight"),
    ("j_crafty", "Crafty Joker", "+80 Chips if hand contains a Flush"),
    ("j_half", "Half Joker", "+20 Mult if hand has 3 or fewer cards"),
    ("j_stencil", "Joker Stencil", "x1 Mult for each empty Joker slot"),
    ("j_four_fingers", "Four Fingers", "Flushes and Straights can be made with 4 cards"),
    ("j_mime", "Mime", "Retrigger all card held in hand abilities"),
    ("j_credit_card", "Credit Card", "Go up to -$20 in debt"),
    ("j_ceremonial", "Ceremonial Dagger", "When Blind is selected, destroy Joker to the right and add double its sell value as permanent +Mult"),
    ("j_banner", "Banner", "+30 Chips for each remaining discard"),
    ("j_mystic_summit", "Mystic Summit", "+15 Mult when 0 discards remaining"),
    ("j_marble", "Marble Joker", "Adds a Stone card to your deck when Blind is selected"),
    ("j_loyalty_card", "Loyalty Card", "x4 Mult every 5 hands played"),
    ("j_8_ball", "8 Ball", "1 in 4 chance for each played 8 to create a Tarot card"),
    ("j_misprint", "Misprint", "+? Mult (random between 0 and 23)"),
    ("j_dusk", "Dusk", "Retrigger all played cards on final hand of round"),
    ("j_raised_fist", "Raised Fist", "Adds double the rank of lowest held card as Mult"),
    ("j_chaos", "Chaos the Clown", "1 free reroll per shop visit"),
    ("j_fibonacci", "Fibonacci", "+8 Mult for each played Ace, 2, 3, 5, or 8"),
    ("j_steel_joker", "Steel Joker", "+0.2x Mult for each Steel Card in full deck"),
    ("j_scary_face", "Scary Face", "+30 Chips if played card is a face card"),
    ("j_abstract", "Abstract Joker", "+3 Mult for each Joker you own"),
    ("j_delayed_grat", "Delayed Gratification", "Earn $2 per discard if no discards used by end of round"),
    ("j_hack", "Hack", "Retrigger each played 2, 3, 4, or 5"),
    ("j_pareidolia", "Pareidolia", "All cards are considered face cards"),
    ("j_gros_michel", "Gros Michel", "+15 Mult. 1 in 6 chance to be destroyed at end of round"),
    ("j_even_steven", "Even Steven", "+4 Mult if played card has even rank (10, 8, 6, 4, 2)"),
    ("j_odd_todd", "Odd Todd", "+31 Chips if played card has odd rank (A, 9, 7, 5, 3)"),
    ("j_scholar", "Scholar", "+20 Chips and +4 Mult if played card is an Ace"),
    ("j_business", "Business Card", "1 in 2 chance to earn $2 when face card is played"),
    ("j_supernova", "Supernova", "Adds the number of times poker hand has been played as Mult"),
    ("j_ride_the_bus", "Ride the Bus", "+1 Mult per consecutive hand without a face card"),
    ("j_space", "Space Joker", "1 in 4 chance to upgrade played hand level"),
    ("j_egg", "Egg", "Gains $3 of sell value at end of round"),
    ("j_burglar", "Burglar", "+3 Hands when Blind is selected, lose all discards"),
    ("j_blackboard", "Blackboard", "x3 Mult if all held cards are Spades or Clubs"),
    ("j_runner", "Runner", "+15 Chips if played hand contains a Straight, gains +15 Chips"),
    ("j_ice_cream", "Ice Cream", "+100 Chips. -5 Chips for each hand played"),
    ("j_dna", "DNA", "First played card is permanently copied to hand on first hand of round"),
    ("j_splash", "Splash", "Every played card counts in scoring"),
    ("j_blue_joker", "Blue Joker", "+2 Chips for each remaining card in deck"),
    ("j_sixth_sense", "Sixth Sense", "Destroy played 6 on first hand, create a Spectral card"),
    ("j_constellation", "Constellation", "+0.1x Mult every time a Planet card is used"),
    ("j_hiker", "Hiker", "Every played card permanently gains +5 Chips"),
    ("j_faceless", "Faceless Joker", "Earn $5 if 3+ face cards are discarded at the same time"),
    ("j_green_joker", "Green Joker", "+1 Mult per hand played, -1 Mult per discard"),
    ("j_superposition", "Superposition", "Create a Tarot card if hand contains an Ace and a Straight"),
    ("j_todo_list", "To Do List", "Earn $4 if poker hand is a listed type"),
    ("j_cavendish", "Cavendish", "x3 Mult. 1 in 1000 chance to be destroyed at end of round"),
    ("j_card_sharp", "Card Sharp", "x3 Mult if played poker hand was already played this round"),
    ("j_red_card", "Red Card", "+3 Mult when any Booster Pack is skipped"),
    ("j_madness", "Madness", "x0.5 Mult when Blind is selected; destroy a random Joker. x1 Mult when Boss Blind is selected"),
    ("j_square", "Square Joker", "+4 Chips if played hand has exactly 4 cards, gains +4 Chips"),
    ("j_seance", "Séance", "Create a Spectral card if poker hand is a Straight Flush"),
    ("j_riff_raff", "Riff-Raff", "Create 2 Common Jokers when Blind is selected (must have room)"),
    ("j_vampire", "Vampire", "x0.1 Mult per enhanced card played; removes enhancement"),
    ("j_shortcut", "Shortcut", "Straights can have gaps of 1 rank (e.g. 2 4 6 8 10)"),
    ("j_hologram", "Hologram", "+0.25x Mult per card added to deck"),
    ("j_vagabond", "Vagabond", "Create a Tarot card when hand is played with $4 or less"),
    ("j_baron", "Baron", "x1.5 Mult for each King held in hand"),
    ("j_cloud_9", "Cloud 9", "Earn $1 per 9 in your full deck at end of round"),
    ("j_rocket", "Rocket", "Earn $1 at end of round. Payout increases by $2 when Boss Blind is defeated"),
    ("j_obelisk", "Obelisk", "x0.2 Mult per consecutive hand played not being your most played hand"),
    ("j_midas_mask", "Midas Mask", "All played face cards become Gold cards"),
    ("j_luchador", "Luchador", "Sell to disable current Boss Blind effect"),
    ("j_photograph", "Photograph", "x2 Mult for first played face card"),
    ("j_gift", "Gift Card", "+1 to sell value of all Jokers and Consumables at end of round"),
    ("j_turtle_bean", "Turtle Bean", "+5 hand size, reduces by 1 each round"),
    ("j_erosion", "Erosion", "+4 Mult for each card below the starting deck size"),
    ("j_reserved_parking", "Reserved Parking", "1 in 2 chance for each face card held to earn $1"),
    ("j_mail", "Mail-In Rebate", "Earn $5 if discarded hand has a designated rank"),
    ("j_to_the_moon", "To the Moon", "Earn extra $1 of interest for every $5, max $20"),
    ("j_hallucination", "Hallucination", "1 in 2 chance to create a Tarot card after opening a Booster Pack"),
    ("j_fortune_teller", "Fortune Teller", "+1 Mult per Tarot card used this run"),
    ("j_juggler", "Juggler", "+1 hand size"),
    ("j_drunkard", "Drunkard", "+1 discard per round"),
    ("j_stone", "Stone Joker", "+25 Chips for each Stone Card in full deck"),
    ("j_golden", "Golden Joker", "Earn $4 at end of round"),
    ("j_lucky_cat", "Lucky Cat", "+0.25x Mult each time a Lucky card triggers"),
    ("j_baseball", "Baseball Card", "Uncommon Jokers give x1.5 Mult"),
    ("j_bull", "Bull", "+2 Chips per $1 you have"),
    ("j_diet_cola", "Diet Cola", "Sell to create a free Double Tag"),
    ("j_trading", "Trading Card", "Discard 1 card, if first discard, create a random Tarot card and destroy it"),
    ("j_flash", "Flash Card", "+2 Mult per reroll in the shop"),
    ("j_popcorn", "Popcorn", "+20 Mult, -4 Mult per round played"),
    ("j_trousers", "Spare Trousers", "+2 Mult if played hand contains a Two Pair"),
    ("j_ancient", "Ancient Joker", "Each played card of a random suit gives x1.5 Mult"),
    ("j_ramen", "Ramen", "x2 Mult, lose x0.01 Mult per card discarded"),
    ("j_walkie_talkie", "Walkie Talkie", "+10 Chips and +4 Mult if played card is a 10 or 4"),
    ("j_selzer", "Seltzer", "Retrigger all played cards for the next 10 hands"),
    ("j_castle", "Castle", "+3 Chips per discarded card, suit changes each round"),
    ("j_smiley", "Smiley Face", "+5 Mult if played card is a face card"),
    ("j_campfire", "Campfire", "x0.25 Mult for each card sold, resets when Boss Blind is defeated"),
    ("j_ticket", "Golden Ticket", "Earn $4 when a Gold card is played"),
    ("j_mr_bones", "Mr. Bones", "Prevents death if chips scored are at least 25% of required. Self-destructs"),
    ("j_acrobat", "Acrobat", "x3 Mult on final hand of round"),
    ("j_sock_and_buskin", "Sock and Buskin", "Retrigger all played face cards"),
    ("j_swashbuckler", "Swashbuckler", "Adds sell value of all owned Jokers as Mult"),
    ("j_troubadour", "Troubadour", "+2 hand size, -1 hand per round"),
    ("j_certificate", "Certificate", "First card dealt each round gets a random seal"),
    ("j_smeared", "Smeared Joker", "Hearts and Diamonds count as the same suit. Spades and Clubs count as the same suit"),
    ("j_throwback", "Throwback", "x0.25 Mult for each Blind skipped this run"),
    ("j_hanging_chad", "Hanging Chad", "Retrigger first played card 2 additional times"),
    ("j_rough_gem", "Rough Gem", "Played Diamonds earn $1"),
    ("j_bloodstone", "Bloodstone", "1 in 2 chance for played Hearts to give x1.5 Mult"),
    ("j_arrowhead", "Arrowhead", "+50 Chips for each played Spade"),
    ("j_onyx_agate", "Onyx Agate", "+7 Mult for each played Club"),
    ("j_glass", "Glass Joker", "x0.75 Mult for every Glass Card that is destroyed"),
    ("j_ring_master", "Showman", "Joker, Tarot, Planet, and Spectral cards may appear multiple times"),
    ("j_flower_pot", "Flower Pot", "x3 Mult if hand has a Diamond, Club, Heart, and Spade card"),
    ("j_blueprint", "Blueprint", "Copies ability of Joker to the right"),
    ("j_wee", "Wee Joker", "+8 Chips when each played 2 is scored, gains +8 Chips"),
    ("j_merry_andy", "Merry Andy", "+3 discards per round, -1 hand size"),
    ("j_oops", "Oops! All 6s", "Doubles all listed probabilities (1 in 3 → 2 in 3)"),
    ("j_idol", "The Idol", "x2 Mult for each played card of a random rank and suit"),
    ("j_seeing_double", "Seeing Double", "x2 Mult if hand has a Club card and a card of any other suit"),
    ("j_matador", "Matador", "Earn $8 when Boss Blind ability is triggered"),
    ("j_hit_the_road", "Hit the Road", "x0.5 Mult for each Jack discarded this round"),
    ("j_duo", "The Duo", "x2 Mult if hand contains a Pair"),
    ("j_trio", "The Trio", "x3 Mult if hand contains a Three of a Kind"),
    ("j_family", "The Family", "x4 Mult if hand contains a Four of a Kind"),
    ("j_order", "The Order", "x3 Mult if hand contains a Straight"),
    ("j_tribe", "The Tribe", "x2 Mult if hand contains a Flush"),
    ("j_stuntman", "Stuntman", "+250 Chips, -2 hand size"),
    ("j_invisible", "Invisible Joker", "After 2 rounds, sell to duplicate a random Joker"),
    ("j_brainstorm", "Brainstorm", "Copies the ability of the leftmost Joker"),
    ("j_satellite", "Satellite", "Earn $1 per unique Planet card used this run at end of round"),
    ("j_shoot_the_moon", "Shoot the Moon", "+13 Mult for each Queen held in hand"),
    ("j_drivers_license", "Driver's License", "x3 Mult if you have 16+ Enhanced cards in your full deck"),
    ("j_cartomancer", "Cartomancer", "Creates a Tarot card when Blind is selected"),
    ("j_astronomer", "Astronomer", "All Planet cards and Celestial Packs in shop are free"),
    ("j_burnt", "Burnt Joker", "Upgrade level of first discarded poker hand each round"),
    ("j_bootstraps", "Bootstraps", "+2 Mult for every $5 you have"),
    ("j_caino", "Caino", "x1 Mult. Gains x1 Mult when a face card is destroyed"),
    ("j_triboulet", "Triboulet", "x2 Mult for played Kings and Queens"),
    ("j_yorick", "Yorick", "x1 Mult. Gains x1 Mult every 23 cards discarded"),
    ("j_chicot", "Chicot", "Disables effect of every Boss Blind"),
    ("j_perkeo", "Perkeo", "Creates a Negative copy of 1 random consumable card at end of shop"),
]

JOKER_MAP = {jid: name for jid, name, *_ in JOKERS}
JOKER_NAME_MAP = {name: jid for jid, name, *_ in JOKERS}
JOKER_DESC = {jid: desc for jid, name, desc in JOKERS}

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

# Seals
SEALS = [
    (None, "None", "No seal"),
    ("Gold", "Gold", "Earn $3 when played"),
    ("Red", "Red", "Retrigger card"),
    ("Blue", "Blue", "Planet card on final hand"),
    ("Purple", "Purple", "Tarot card on discard"),
]

SEAL_MAP = {sid: name for sid, name, *_ in SEALS}

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
