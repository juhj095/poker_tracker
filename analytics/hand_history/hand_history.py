import streamlit as st
from hand_history.render_hand import render_hand_history
from data.handle_data import load_actions, load_boards, load_players, load_hand_info, mark_hand_favourite, unmark_hand_favourite, load_favourite_hands
from utils import format_multiple_cards
def hand(update_url: bool=False):
    bet_unit = st.sidebar.radio("Bet display:", ["Big Blinds", "€"], horizontal=True)
    hide_names = st.sidebar.checkbox("Hide names", value=False)

    st.sidebar.header("Hand Tags")

    fav_df = load_favourite_hands()

    with st.sidebar.expander("Favourites", expanded=True):
        fav_df = load_favourite_hands()
        if fav_df.empty:
            st.info("No favourite hands yet.")
        else:
            for row in fav_df.itertuples(index=False):
                if st.button(f"{row.gamecode} ({format_multiple_cards([row.hero_cards[:2], row.hero_cards[2:]])})", key=f"fav_{row.gamecode}"):
                    st.session_state.selected_gamecode = row.gamecode
                    if update_url:
                        st.query_params["hand"] = str(row.gamecode)

    gamecode = st.session_state.get("selected_gamecode")
    if not gamecode:
        st.warning("No hand selected.")
        st.stop()

    hand_df = load_hand_info(gamecode)
    hand_id = int(hand_df["hand_id"].iloc[0])
    actions = load_actions(hand_id)
    boards = load_boards(hand_id)
    players = load_players(hand_id)

    hand_text = render_hand_history(actions, boards, players, hand_df, bet_unit, hide_names)

    # TODO handle multiple tags
    tag_ids = hand_df.iloc[0]["tag_ids"]
    is_favourite = tag_ids is not None and "1" in tag_ids.split(",")

    if is_favourite:
        if st.button("Unmark as Favourite"):
            unmark_hand_favourite(hand_id)
    else:
        if st.button("Mark as Favourite"):
            mark_hand_favourite(hand_id)

    st.code(hand_text, language="text")