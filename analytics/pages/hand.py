import streamlit as st
from render_hand import render_hand_history
from load_data import load_hand, load_board, load_players, load_hero_name

st.set_page_config(page_title="Hand History", layout="wide")

st.title("Hand History")

hand_id = st.query_params.get("hand_id")

if not hand_id:
    st.warning("No hand selected.")
    st.stop()

try:
    hand_id = int(hand_id)
except ValueError:
    st.error("Invalid hand_id.")
    st.stop()

actions = load_hand(hand_id)
board = load_board(hand_id)
players = load_players(hand_id)
hero = load_hero_name(hand_id)
hero_name = hero["nickname"][0]

if actions.empty:
    st.warning("No actions found for this hand.")
    st.stop()

hand_text = render_hand_history(actions, board, players, hero_name)

st.code(hand_text, language="text")