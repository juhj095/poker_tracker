from constants import SUIT_MAP, POSITION_MAP

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

def assign_positions(players):
    rows = [p._asdict() for p in players]

    # Find dealer
    btn_index = next(i for i, p in enumerate(rows) if int(p.get("dealer", 0)) == 1)

    # Rotate so BTN is first
    rotated = rows[btn_index:] + rows[:btn_index]

    player_count = len(rotated)
    if player_count not in POSITION_MAP:
        raise ValueError(f"Unsupported table size: {player_count}")

    positions = POSITION_MAP[player_count]

    # Assign positions
    for player, pos in zip(rotated, positions):
        player["position"] = pos

    return rotated

def format_player_label(
    name: str,
    position: str,
    hero_name: str,
    hide_names: bool
):
    if hide_names:
        label = position
    else:
        label = f"{name} [{position}]"

    if name == hero_name:
        label += " (Hero)"

    return label

def select_profit_series(df, unit):
    if unit == "€":
        return {
            "total": df["cum_total"],
            "show": df["cum_show"],
            "noshow": df["cum_noshow"],
            "label": "Profit (€)",
        }

    return {
        "total": df["cum_total_bb"],
        "show": df["cum_show_bb"],
        "noshow": df["cum_noshow_bb"],
        "label": "Profit (bb)",
    }

def compute_summary_stats(df):
    total_hands = len(df)

    total_profit = df["cum_total"].iloc[-1]
    total_profit_bb = df["cum_total_bb"].iloc[-1]

    bb_per_100 = (total_profit_bb / total_hands) * 100 if total_hands else 0

    return {
        "hands": total_hands,
        "profit": total_profit,
        "profit_bb": total_profit_bb,
        "bb_per_100": bb_per_100,
    }

def stake_label(bb, ante):
    stake = int(round(bb * 100))
    return f"NL{stake} ANTE" if ante else f"NL{stake}"