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

def profit_over_time():
    query = """
        SELECT h.hand_id, h.profit, h.showdown, s.startdate, s.bigblind
        FROM Hand h
        JOIN Session s ON h.session_id = s.session_id
        ORDER BY s.startdate, h.hand_id
    """
    return query