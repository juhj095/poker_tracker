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
        SELECT h.hand_id,
               h.profit,
               h.showdown,
               s.startdate,
               s.bigblind
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
    query += " ORDER BY s.startdate, h.hand_id"

    return query, params