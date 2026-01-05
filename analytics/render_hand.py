from utils import ROUND_NAMES, format_multiple_cards, extract_cards_from_flop, community_cards

def render_run_boards(board_rows, street_is_shared):
    lines = []

    # Detect shared streets
    shared_streets = {r for r in range(2, 5) if street_is_shared(r)}

    # Shared streets exist
    if shared_streets:
        first_board = board_rows.iloc[0]

        # Build base cards for shared streets
        base_cards = []
        if 2 in shared_streets and first_board.flop:
            base_cards.extend(extract_cards_from_flop(first_board.flop))
        if 3 in shared_streets and first_board.turn:
            base_cards.append(first_board.turn)

        # Append per-run streets
        for run_index, board in enumerate(board_rows.itertuples(), start=1):
            lines.append("")
            lines.append(f"=== Run {run_index} ===")

            # Start with the shared cards (flop/turn if shared)
            run_cards = list(base_cards)  

            # Add any remaining cards for this run
            if 2 not in shared_streets and board.flop:
                run_cards.extend(extract_cards_from_flop(board.flop))
            if 3 not in shared_streets and board.turn:
                run_cards.append(board.turn)
            if 4 not in shared_streets and board.river:
                run_cards.append(board.river)

            lines.append(f"*** River ***")
            lines.append(format_multiple_cards(run_cards))

    # All-in preflop
    else:
        for run_index, board in enumerate(board_rows.itertuples(), start=1):
            lines.append("")
            lines.append(f"=== Run {run_index} ===")

            run_cards = []
            if board.flop:
                run_cards.extend(extract_cards_from_flop(board.flop))
            if board.turn:
                run_cards.append(board.turn)
            if board.river:
                run_cards.append(board.river)

            lines.append("*** River ***")
            lines.append(format_multiple_cards(run_cards))

    return lines

def render_hand_history(actions, board_rows, players, hero):
    lines = []

    hero_row = players.loc[players["name"] == hero]
    if not hero_row.empty:
        row = hero_row.iloc[0]
        cards = format_multiple_cards([row.card1, row.card2])
        lines.append(f"{hero} (Hero) has {cards}")

    rounds = dict(tuple(actions.groupby("roundnumber")))
    last_action_round = actions["roundnumber"].max()
    number_of_runs = len(board_rows)
    is_multi_run = number_of_runs > 1
    print(rounds)
    def street_is_shared(r):
        return r <= last_action_round
    
    pot = 0
    folds = 0

    # Render shared streets first
    for r in [0, 1, 2, 3, 4]:
        if not folds + 1 < len(players) or (is_multi_run and not street_is_shared(r)):
            lines.append(f"Pot: {pot:.2f}") # TODO correct final pot size
            break
        lines.append("")
        lines.append(f"*** {ROUND_NAMES[r]} ***")
        if r >= 2:
            lines.extend(community_cards(r, board_rows.iloc[0]))
        if pot:
            lines.append(f"Pot: {pot:.2f}")
            lines.append("")
        
        if r not in rounds:
            continue
        for row in rounds[r].itertuples():
            if row.action == "Fold":
                folds += 1
            if row.amount:
                pot += row.amount
                lines.append(f"{row.name}: {row.action} {row.amount}")
            else:
                lines.append(f"{row.name}: {row.action}")

    # Run-it-twice
    if is_multi_run:
        lines.extend(render_run_boards(board_rows, street_is_shared))

    if lines[-1] != "":
        lines.append("")

    for player in players.itertuples():
        if (player.card1 or player.card2) and player.name != hero:
            cards = format_multiple_cards([player.card1, player.card2])
            lines.append(f"{player.name} shows {cards}")

    if lines[-1] != "":
        lines.append("")

    for player in players.itertuples():
        if player.win and float(player.win) > 0:
            lines.append(f"{player.name} wins {player.win}")

    return "\n".join(lines)