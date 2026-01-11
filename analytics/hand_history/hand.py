import streamlit as st
from hand_history.render_hand import render_hand_history
from data.load_data import load_actions, load_boards, load_players, load_hand_info

def hand(hand_id):
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

    actions = load_actions(hand_id)
    boards = load_boards(hand_id)
    players = load_players(hand_id)
    hand = load_hand_info(hand_id)

    hand_text = render_hand_history(actions, boards, players, hand, bet_unit, hide_names)

    st.code(hand_text, language="text")