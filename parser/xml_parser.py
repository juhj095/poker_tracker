import os
from lxml import etree

from db_helpers import get_session_id_by_code, insert_session, insert_hand, insert_player, insert_round, insert_action, insert_pocket_cards, insert_board, insert_profit
from parsers import parse_session, parse_hand, parse_player, parse_action, parse_boards
from utils import normalize_cards, calculate_profit

def xml_parser(cursor, xml_path):
    tree = etree.parse(xml_path)
    root = tree.getroot()

    sessioncode = root.attrib.get("sessioncode")
    gametype = root.find("general").findtext("gametype")
    existing_session_id = get_session_id_by_code(cursor, sessioncode)

    if existing_session_id:
        print(f"Session already exists in the database. Skipping import for {os.path.basename(xml_path)}\n")

    # TODO better way to check if cash game for more currencies
    elif "€" not in gametype:
        print(f"Cash games only. Skipping import for {os.path.basename(xml_path)}\n")

    else:
        # Insert session
        session_data = parse_session(root)

        session_id = insert_session(cursor, (
            sessioncode,
            session_data["clientversion"],
            session_data["mode"],
            session_data["gametype"],
            session_data["tablename"],
            session_data["smallblind"],
            session_data["bigblind"],
            session_data["duration"],
            session_data["gamecount"],
            session_data["startdate"],
            session_data["currency"],
            session_data["nickname"],
            session_data["bets"],
            session_data["wins"],
            session_data["chipsin"],
            session_data["chipsout"],
            session_data["tablesize"]
        ))
        
        for game in root.findall("game"):
            hero_in_hand = any(
                player.attrib.get("name") == session_data["nickname"]
                for player in game.findall("general/players/player")
            )
            if not hero_in_hand:
                continue

            # Insert hands
            hand_data = parse_hand(game)
            
            hand_id = insert_hand(cursor, (
                session_id,
                hand_data["gamecode"],
                hand_data["startdate"],
                hand_data["showdown"]
            ))

            player_id_map = {}
            boards = {}
            players_data = []

            # Insert players
            for player in game.findall("general/players/player"):
                player_data = parse_player(player)

                insert_player(cursor, (
                    hand_id,
                    player_data["name"],
                    player_data["seat"],
                    player_data["chips"],
                    player_data["win"],
                    player_data["bet"],
                    player_data["dealer"],
                    player_data["rakeamount"]
                ))

                player_id_map[player_data["name"]] = cursor.lastrowid
                players_data.append(player_data)


            # Insert profit
            hero_name = session_data["nickname"]
            hero_profit = calculate_profit(hero_name, players_data)
            insert_profit(cursor, hero_profit, hand_id)
        
            # Insert rounds
            for round in game.findall("round"):
                round_number = int(round.attrib.get("no"))
                round_id = insert_round(cursor, (
                    hand_id, round_number
                ))

                # Insert pocket cards
                if round_number == 1:
                    for cards in round.findall("cards"):
                        pocket_cards = normalize_cards(cards.text)
                        if (pocket_cards != "XX"):
                            player_name = cards.attrib.get("player")
                            # If one card is shown
                            if len(pocket_cards) == 3:
                                pocket_cards = pocket_cards.replace("X", "")
                                insert_pocket_cards(cursor, (
                                    pocket_cards,
                                    None,
                                    player_id_map[player_name]
                                ))
                            else:
                                insert_pocket_cards(cursor, (
                                    pocket_cards[:2],
                                    pocket_cards[2:],
                                    player_id_map[player_name]
                                ))

                if round_number in (2, 3, 4):
                    parse_boards(round, boards)

                # Insert actions
                for action in round.findall("action"):
                    action_data = parse_action(action)

                    insert_action(cursor, (
                        round_id,
                        player_id_map[action_data["player_name"]],
                        action_data["action_type"],
                        action_data["amount"],
                        action_data["action_number"]
                    ))
            
            # Insert community cards
            for board_number, cards_data in boards.items():
                insert_board(cursor, hand_id, board_number, cards_data)

        print(f"✅ Done: {os.path.basename(xml_path)}\n")