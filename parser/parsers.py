from datetime import datetime
from utils import normalize_cards

# TODO: other currencies

def parse_session(root):
    general = root.find("general")
    clientversion = general.findtext("client_version")
    mode = general.findtext("mode")
    gametype = general.findtext("gametype")
    tablename = general.findtext("tablename")
    smallblind = float(general.findtext("smallblind").replace("€", "") or 0)
    bigblind = float(general.findtext("bigblind").replace("€", "") or 0)
    duration = general.findtext("duration")
    gamecount = int(general.findtext("gamecount") or 0)
    startdate = datetime.strptime(general.findtext("startdate"), "%d.%m.%Y %H:%M:%S")
    currency = general.findtext("currency")
    nickname = general.findtext("nickname")
    bets = float(general.findtext("bets").replace("€", "") or 0)
    wins = float(general.findtext("wins").replace("€", "") or 0)
    chipsin = float(general.findtext("chipsin").replace("€", "") or 0)
    chipsout = float(general.findtext("chipsout").replace("€", "") or 0)
    tablesize = int(general.findtext("tablesize") or 0)

    return {
        "clientversion": clientversion,
        "mode": mode,
        "gametype": gametype,
        "tablename": tablename,
        "smallblind": smallblind,
        "bigblind": bigblind,
        "duration": duration,
        "gamecount": gamecount,
        "startdate": startdate,
        "currency": currency,
        "nickname": nickname,
        "bets": bets,
        "wins": wins,
        "chipsin": chipsin,
        "chipsout": chipsout,
        "tablesize": tablesize
    }

def parse_hand(game):
    gamecode = game.attrib.get("gamecode")
    startdate = datetime.strptime(game.findtext("general/startdate"),  "%d.%m.%Y %H:%M:%S")

    return {
        "gamecode": gamecode,
        "startdate": startdate
    }

def parse_player(player):
    name = player.attrib.get("name")
    seat = int(player.attrib.get("seat") or 0)
    chips = float(player.attrib.get("chips").replace("€", "") or 0)
    win = float(player.attrib.get("win").replace("€", "") or 0)
    bet = float(player.attrib.get("bet").replace("€", "") or 0)
    dealer = int(player.attrib.get("dealer") or 0)
    rakeamount = None
    if "rakeamount" in player.attrib:
        rakeamount = float(player.attrib.get("rakeamount").replace("€", ""))

    return {
        "name": name,
        "seat": seat,
        "chips": chips,
        "win": win,
        "bet": bet,
        "dealer": dealer,
        "rakeamount": rakeamount
    }

def parse_action(action):
    player_name = action.attrib.get("player")
    action_type = int(action.attrib.get("type"))
    amount = float(action.attrib.get("sum").replace("€", "")) or 0.0
    action_number = int(action.attrib.get("no"))

    return {
        "player_name": player_name,
        "action_type": action_type,
        "amount": amount,
        "action_number": action_number
    }

def parse_boards(round, boards):
    for cards in round.findall("cards"):
        board_attr = cards.attrib.get("board")  # None, "board1", "board2"
        board_number = 1
        if board_attr:
            board_number = int(board_attr.replace("board", ""))

        card_type = cards.attrib.get("type")  # "Flop", "Turn", "River"
        card_string = normalize_cards(cards.text)

        if board_number not in boards:
            boards[board_number] = {"flop": None, "turn": None, "river": None}
        boards[board_number][card_type.lower()] = card_string

    return boards