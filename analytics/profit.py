import matplotlib.pyplot as plt
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
    connection = get_connection()
    cursor = connection.cursor()

    # Get profits for each hand
    cursor.execute("""
        SELECT h.hand_id, h.profit
        FROM Hand h
        JOIN Session s ON h.session_id = s.session_id
        ORDER BY s.startdate, h.hand_id
    """)

    hands = cursor.fetchall()
    connection.close()

    x = list(range(1, len(hands) + 1))
    profits = [float(row[1]) if row[1] is not None else 0.0 for row in hands]
    cumulative = [sum(profits[:i+1]) for i in range(len(profits))]

    # Plot
    plt.figure(figsize=(10, 5))
    plt.plot(x, cumulative, label="Cumulative Profit", linewidth=2)
    plt.xlabel("Hands Played")
    plt.ylabel("Profit (€)")
    plt.title("Poker Profit Over Time")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    profit_over_time()