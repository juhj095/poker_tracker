# Lines start at 0, change numpy.float64 to float due to plotly_events
def y_axis(total):
    return [0.0] + total.astype(float).tolist()

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

def format_card(card):
    suit, rank = card[0], card[1]
    return f"{rank}{SUIT_MAP.get(suit, suit)}"

def format_multiple_cards(cards):
    return " ".join([format_card(c) for c in cards if c])

def extract_cards_from_flop(flop):
    return [flop[i:i+2] for i in range(0, len(flop), 2)]

def community_cards(round_number, board_row):
    def get(attr):
        return getattr(board_row, attr, None)

    cards = []

    flop = get("flop")
    if flop:
        cards.extend(extract_cards_from_flop(flop))

    if round_number >= 3:
        turn = get("turn")
        if turn:
            cards.append(turn)

    if round_number >= 4:
        river = get("river")
        if river:
            cards.append(river)

    return [format_multiple_cards(cards)] if cards and round_number >= 2 else []

def format_amount(amount, bigblind, unit):
    if amount is None:
        return ""
    if unit == "Big Blinds":
        return f"{amount / bigblind:.2f} bb"
    return f"{amount:.2f} €"

def format_pot(pot, bigblind, unit):
    return f"Pot: {format_amount(pot, bigblind, unit)}"