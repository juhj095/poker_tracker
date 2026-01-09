import streamlit as st
import pandas as pd
from db_helpers import get_connection, profit_over_time, actions_info, boards_info, players_info, hand_info

# TODO load currency and big blind data seperately, saves time
@st.cache_data(show_spinner="Loading hands…")
def load_profit_data(start_date, end_date):
    connection = get_connection()
    query, params = profit_over_time(
        start_date=start_date,
        end_date=end_date
    )
    df = pd.read_sql(query, connection, params=params)
    connection.close()
    df = df.sort_values(["startdate", "hand_id"]).reset_index(drop=True)
    return df

def load_actions(hand_id):
    connection = get_connection()
    query = actions_info()
    df = pd.read_sql(query, connection, params=[hand_id])
    connection.close()
    return df

def load_boards(hand_id):
    connection = get_connection()
    query = boards_info()
    df = pd.read_sql(query, connection, params=[hand_id])
    connection.close()
    return df

def load_players(hand_id):
    connection = get_connection()
    query = players_info()
    df = pd.read_sql(query, connection, params=[hand_id])
    connection.close()
    return df

def load_hand_info(hand_id):
    connection = get_connection()
    query = hand_info()
    df = pd.read_sql(query, connection, params=[hand_id])
    connection.close()
    return df