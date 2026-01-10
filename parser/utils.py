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
    max_other_bet = max((p["bet"] for p in players if p["name"] != hero_name))
    if hero_win > 0:
        winners = [p for p in players if (p.get("win") or 0) > 0]
        if len(winners) > 1:
            if hero_bet > max_other_bet:
                profit = hero_win - hero_bet + (hero_bet - max_other_bet)
            else:
                profit = hero_win - hero_bet
        else:
            profit = sum(min(p["bet"], hero_bet) for p in players if p["name"] != hero_name) - (hero["rakeamount"] or 0)
    else:
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