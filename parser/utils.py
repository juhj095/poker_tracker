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