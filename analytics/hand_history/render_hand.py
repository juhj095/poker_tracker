from utils import format_multiple_cards, community_cards, format_amount, format_pot, assign_positions, format_player_label
from constants import ROUND_NAMES
from hand_history.render_multiple_runs import render_run_boards

def render_hand_history(actions, board_rows, players, hand, bet_unit, hide_names):
    lines = []
    hero = hand["nickname"].iloc[0]
    bigblind = hand["bigblind"].iloc[0]
    hero_row = players.loc[players["name"] == hero]

    positioned_players = assign_positions(players.itertuples())
    player_meta = {
        p["name"]: {
            "position": p["position"],
        }
        for p in positioned_players
    }

    lines.append("*** Players ***")
    for p in positioned_players:
        stack = p.get("chips")
        pos = p.get("position")
        name = p.get("name")

        label = format_player_label(
            name=name,
            position=pos,
            hero_name=hero,
            hide_names=hide_names,
        )

        lines.append(f"{label} ({format_amount(stack, bigblind, bet_unit)})")
    lines.append("")

    if not hero_row.empty:
        row = hero_row.iloc[0]
        cards = format_multiple_cards([row.card1, row.card2])
        label = format_player_label(
            name=hero,
            position=player_meta[hero]["position"],
            hero_name=hero,
            hide_names=hide_names
        )
        lines.append(f"{label} has {cards}")

    rounds = dict(tuple(actions.groupby("roundnumber")))
    last_action_round = actions["roundnumber"].max()
    number_of_runs = len(board_rows)
    is_multi_run = number_of_runs > 1

    def street_is_shared(r):
        return r <= last_action_round
    
    pot = 0
    folds = 0

    # Render shared streets first
    for r in [0, 1, 2, 3, 4]:
        if not folds + 1 < len(players) or (is_multi_run and not street_is_shared(r)):
            lines.append(format_pot(pot, bigblind, bet_unit)) # TODO correct final pot size
            break
        lines.append("")
        lines.append(f"*** {ROUND_NAMES[r]} ***")
        if r >= 2:
            lines.extend(community_cards(r, board_rows.iloc[0]))
        if pot:
            lines.append(format_pot(pot, bigblind, bet_unit))
            lines.append("")
        
        if r not in rounds:
            continue
        for row in rounds[r].itertuples():
            meta = player_meta.get(row.name)
            label = format_player_label(
                name=row.name,
                position=meta["position"],
                hero_name=hero,
                hide_names=hide_names,
            )

            if row.action == "Fold":
                folds += 1
            if row.amount:
                pot += row.amount
                formatted = format_amount(row.amount, bigblind, bet_unit)
                lines.append(f"{label}: {row.action} {formatted}")
            else:
                lines.append(f"{label}: {row.action}")

    # Run-it-twice
    if is_multi_run:
        lines.extend(render_run_boards(board_rows, street_is_shared))

    if lines[-1] != "":
        lines.append("")

    for player in players.itertuples():
        if (player.card1 or player.card2) and player.name != hero:
            cards = format_multiple_cards([player.card1, player.card2])
            meta = player_meta[player.name]
            label = format_player_label(
                name=player.name,
                position=meta["position"],
                hero_name=hero,
                hide_names=hide_names,
            )
            lines.append(f"{label} shows {cards}")

    if lines[-1] != "":
        lines.append("")

    for player in players.itertuples():
        if player.win and float(player.win) > 0:
            meta = player_meta[player.name]
            label = format_player_label(
                name=player.name,
                position=meta["position"],
                hero_name=hero,
                hide_names=hide_names,
            )
            lines.append(f"{label} wins {format_amount(player.win, bigblind, bet_unit)}")

    return "\n".join(lines)