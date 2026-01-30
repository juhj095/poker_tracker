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

def went_to_showdown(game, hero_name):
    players = [p.attrib["name"] for p in game.findall("general/players/player")]
    player_set = set(players)

    # Track who folded at any point
    folded = set()
    for a in game.findall(".//action"):
        if a.attrib.get("type") == "0":  # Fold
            folded.add(a.attrib.get("player"))

    # 1) Hero must not fold
    if hero_name in folded:
        return False

    # 2) At least one OTHER player must not fold
    others = player_set - {hero_name}
    others_not_folded = [p for p in others if p not in folded]

    return len(others_not_folded) >= 1