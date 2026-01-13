import streamlit as st
from hand_history.hand_history import hand

st.set_page_config(page_title="Hand History", layout="wide")
st.title("Hand History")

st.session_state.selected_gamecode = st.query_params.get("hand")

hand(update_url=True)