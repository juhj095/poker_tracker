def normalize_cards(card_string):
    return card_string.replace("10", "T").replace(" ", "")

def calculate_profit(hero_name, players):
    hero = next((p for p in players if p["name"] == hero_name), None)
    if not hero:
        return None

    hero_bet = hero["bet"]
    if hero_bet == 0:
        return 0.0

    hero_win = hero["win"]
    if hero_win > 0:
        other_wins = sum(   # Chopped pots/side pots
            (p.get("win") or 0.0)
            for p in players
            if p["name"] != hero_name and (p.get("win") or 0.0) > 0
        )
        rake = sum((p.get("rakeamount") or 0.0 for p in players), 0.0)
        profit = sum(min(p["bet"], hero_bet) for p in players if p["name"] != hero_name) - rake - other_wins
    else:
        max_other_bet = max((p["bet"] for p in players if p["name"] != hero_name))
        profit = -(min(hero_bet, max_other_bet))

    return profit

def went_to_showdown(game):
    # All players that were dealt in this hand
    all_players = {p.attrib["name"] for p in game.findall("general/players/player")}
    total_players = len(all_players)

    # All players who folded
    folded_players = {
        a.attrib["player"]
        for a in game.findall(".//action")
        if a.attrib.get("type") == "0"  # type 0 = fold
    }

    # Count how many are left
    remaining_players = total_players - len(folded_players)

    # If everyone except one folded → no showdown
    if remaining_players <= 1:
        return False
    else:
        return True