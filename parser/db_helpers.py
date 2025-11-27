import mysql.connector
import os
from dotenv import load_dotenv
load_dotenv()

def get_connection():
    return mysql.connector.connect(
        host = os.getenv("DB_HOST"),
        user = os.getenv("DB_USER"),
        password = os.getenv("DB_PASS"),
        database = os.getenv("DB_NAME")
    )

def insert_session(cursor, data):
    query = """
        INSERT INTO Session (
            sessioncode, clientversion, mode, gametype, tablename,
            smallblind, bigblind, duration, gamecount, startdate, currency,
            nickname, bets, wins, chipsin, chipsout, tablesize
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE sessioncode = sessioncode
    """
    cursor.execute(query, data)
    return cursor.lastrowid


def get_session_id_by_code(cursor, sessioncode):
    cursor.execute("SELECT session_id FROM Session WHERE sessioncode = %s", (sessioncode,))
    result = cursor.fetchone()
    return result[0] if result else None


def insert_hand(cursor, data):
    query = """
        INSERT INTO Hand (session_id, gamecode, startdate, showdown)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE gamecode = gamecode
    """
    cursor.execute(query, data)
    return cursor.lastrowid


def insert_player(cursor, data):
    query = """
        INSERT INTO Player (hand_id, name, seat, chips, win, bet, dealer, rakeamount)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, data)

def insert_round(cursor, data):
    query = """
        INSERT INTO Round (hand_id, roundnumber)
        VALUES (%s, %s)
    """
    cursor.execute(query, data)
    return cursor.lastrowid

def insert_action(cursor, data):
    query = """
        INSERT INTO Action (round_id, player_id, actiontype_id, amount, actionorder)
        VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query, data)

def insert_pocket_cards(cursor, data):
    query = """
        UPDATE Player SET card1 = %s, card2 = %s
        WHERE player_id = %s
    """
    cursor.execute(query, data)

def insert_board(cursor, hand_id, board_number, cards_data):
    query = """
        INSERT INTO Board (hand_id, boardnumber, flop, turn, river)
        VALUES (%s, %s, %s, %s, %s)
    """
    data = (
        hand_id,
        board_number,
        cards_data.get("flop"),
        cards_data.get("turn"),
        cards_data.get("river"),
    )
    cursor.execute(query, data)

def insert_profit(cursor, profit, hand_id):
    query = """
        UPDATE Hand
        SET profit = %s
        WHERE hand_id = %s
    """
    cursor.execute(query, (profit, hand_id))