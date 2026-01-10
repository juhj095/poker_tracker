from utils import extract_cards_from_flop, format_multiple_cards

def render_run_boards(board_rows, street_is_shared):
    lines = []

    # Detect shared streets
    shared_streets = {r for r in range(2, 5) if street_is_shared(r)}

    # Shared streets exist
    if shared_streets:
        first_board = board_rows.iloc[0]

        # Build base cards for shared streets
        base_cards = []
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
            if 3 not in shared_streets:
                run_cards.append(board.turn)
            run_cards.append(board.river)

            lines.append(f"*** River ***")
            lines.append(format_multiple_cards(run_cards))

    # All-in preflop
    else:
        for run_index, board in enumerate(board_rows.itertuples(), start=1):
            lines.append("")
            lines.append(f"=== Run {run_index} ===")

            run_cards = []
            run_cards.extend(extract_cards_from_flop(board.flop))
            run_cards.append(board.turn)
            run_cards.append(board.river)

            lines.append("*** River ***")
            lines.append(format_multiple_cards(run_cards))

    return lines