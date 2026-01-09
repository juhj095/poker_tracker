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

def profit_over_time(start_date=None, end_date=None): # TODO stakes=None
    query = """
        SELECT
            h.hand_id,
            h.profit,
            h.startdate,
            s.bigblind,
            SUM(h.profit) OVER (ORDER BY h.startdate, h.hand_id) AS cum_total,
            SUM(CASE WHEN h.showdown = 1 THEN h.profit ELSE 0 END)
                OVER (ORDER BY h.startdate, h.hand_id) AS cum_show,
            SUM(CASE WHEN h.showdown = 0 THEN h.profit ELSE 0 END)
                OVER (ORDER BY h.startdate, h.hand_id) AS cum_noshow,
            SUM(h.profit / s.bigblind) OVER (ORDER BY h.startdate, h.hand_id) AS cum_total_bb,
            SUM(CASE WHEN h.showdown = 1 THEN h.profit / s.bigblind ELSE 0 END)
                OVER (ORDER BY h.startdate, h.hand_id) AS cum_show_bb,
            SUM(CASE WHEN h.showdown = 0 THEN h.profit / s.bigblind ELSE 0 END)
                OVER (ORDER BY h.startdate, h.hand_id) AS cum_noshow_bb
        FROM Hand h
        JOIN Session s ON h.session_id = s.session_id
        WHERE 1 = 1
    """

    params = []

    if start_date:
        query += " AND s.startdate >= %s"
        params.append(start_date)

    if end_date:
        query += " AND s.startdate <= %s"
        params.append(end_date)
    
    # TODO stakes
    """
    if stakes:
        placeholders = ", ".join(["%s"] * len(stakes))
        query += f" AND s.bigblind IN ({placeholders})"
        params.extend(stakes)
    """

    return query, params

def actions_info():
    query = """
        SELECT
            r.roundnumber,
            a.actionorder,
            p.name,
            at.description AS action,
            a.amount
        FROM Action a
        JOIN ActionType at ON a.actiontype_id = at.actiontype_id
        JOIN Player p ON a.player_id = p.player_id
        JOIN Round r ON a.round_id = r.round_id
        WHERE r.hand_id = %s
        ORDER BY r.roundnumber, a.actionorder
    """
    return query

def boards_info():
    query = """
        SELECT flop, turn, river
        FROM Board
        WHERE hand_id = %s
        ORDER BY boardnumber
    """
    return query

def players_info():
    query = """
        SELECT name, seat, chips, win, dealer, card1, card2
        FROM Player
        WHERE hand_id = %s
    """
    return query

def hand_info():
    query = """
        SELECT s.nickname, s.bigblind
        FROM Session s
        JOIN Hand h ON s.session_id = h.session_id
        WHERE hand_id = %s
    """
    return query