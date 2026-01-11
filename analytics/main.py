import streamlit as st
from streamlit_plotly_events import plotly_events
from data.load_data import load_profit_data
from utils import select_profit_series, compute_summary_stats
from plots.profit_plot import build_profit_figure
from hand_history.hand import hand

def main():
    st.set_page_config(page_title="Poker Tracker", layout="wide")
    st.title("Poker Tracker 📈")

    # Filters
    st.sidebar.header("Filters")
    unit = st.sidebar.radio("Display unit:", ["Big Blinds", "€"])
    show_showdown = st.sidebar.checkbox("Showdown/Non SD Winnings", False)

    start_date = st.sidebar.date_input("Start date", value=None)
    end_date = st.sidebar.date_input("End date", value=None)

    df = load_profit_data(start_date, end_date)

    if df.empty:
        st.warning("No data found — check your database or filters.")
        return

    series = select_profit_series(df, unit)

    fig = build_profit_figure(
        df=df,
        total=series["total"],
        show=series["show"],
        noshow=series["noshow"],
        label=series["label"],
        show_showdown=show_showdown
    )

    stats = compute_summary_stats(df)

    st.subheader("Summary")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Hands", stats["hands"])

    if unit == "€":
        col2.metric("Total Profit (€)", round(stats["profit"], 2))
    else:
        col2.metric("Total Profit (bb)", round(stats["profit_bb"], 2))

    col3.metric("Winrate (bb/100)", round(stats["bb_per_100"], 2))

    if "selected_hand_id" not in st.session_state:
        st.session_state.selected_hand_id = None
        st.session_state.selected_hand_gamecode = None

    # Graph
    selected = plotly_events(fig, click_event=True)
    if selected:
        index = selected[0]["pointIndex"]
        if index > 0:
            st.session_state.selected_hand_id = df.iloc[index - 1]["hand_id"]
            st.session_state.selected_hand_gamecode = df.iloc[index - 1]["gamecode"]

    if st.session_state.selected_hand_id:
        with st.expander(
            f"Hand {st.session_state.selected_hand_gamecode}",
            expanded=True,
        ):
            hand(int(st.session_state.selected_hand_id))

if __name__ == "__main__":
    main()