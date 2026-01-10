import streamlit as st
from render_hand import render_hand_history
from load_data import load_actions, load_boards, load_players, load_hand_info

st.set_page_config(page_title="Hand History", layout="wide")

st.title("Hand History")

hand_id = st.query_params.get("hand_id")

bet_unit = st.sidebar.radio(
    "Bet display:",
    ["Big Blinds", "€"],
    horizontal=True
)

hide_names = st.sidebar.checkbox(
    "Hide names",
    value=False
)

if not hand_id:
    st.warning("No hand selected.")
    st.stop()

try:
    hand_id = int(hand_id)
except ValueError:
    st.error("Invalid hand_id.")
    st.stop()

actions = load_actions(hand_id)
boards = load_boards(hand_id)
players = load_players(hand_id)
hand = load_hand_info(hand_id)

if actions.empty:
    st.warning("No actions found for this hand.")
    st.stop()

hand_text = render_hand_history(actions, boards, players, hand, bet_unit, hide_names)

st.code(hand_text, language="text")