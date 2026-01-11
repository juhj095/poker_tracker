ROUND_NAMES = {
    0: "Blinds",
    1: "Preflop",
    2: "Flop",
    3: "Turn",
    4: "River",
}

SUIT_MAP = {
    "S": "♠",
    "H": "♥",
    "D": "♦",
    "C": "♣",
}

POSITION_MAP = {
    2: ["BTN", "SB"],
    3: ["BTN", "SB", "BB"],
    4: ["BTN", "SB", "BB", "UTG"],
    5: ["BTN", "SB", "BB", "UTG", "CO"],
    6: ["BTN", "SB", "BB", "UTG", "MP", "CO"],
    7: ["BTN", "SB", "BB", "UTG", "HJ", "LJ", "CO"],
    8: ["BTN", "SB", "BB", "UTG", "UTG+1", "LJ", "HJ", "CO"],
    9: ["BTN", "SB", "BB", "UTG", "UTG+1", "UTG+2", "LJ", "HJ", "CO"],
}