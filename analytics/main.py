import streamlit as st
from streamlit_plotly_events import plotly_events
from data.handle_data import load_profit_data, load_stakes
from utils import select_profit_series, compute_summary_stats, stake_label
from plots.profit_plot import build_profit_figure
from hand_history.hand_history import hand

def main():
    st.set_page_config(page_title="Poker Tracker", layout="wide")
    st.title("Poker Tracker 📈")

    # Filters
    st.sidebar.header("Filters")
    unit = st.sidebar.radio("Display unit:", ["Big Blinds", "€"], horizontal=True)
    show_showdown = st.sidebar.checkbox("Showdown/Non SD Winnings", False)

    start_date = st.sidebar.date_input("Start date", value=None)
    end_date = st.sidebar.date_input("End date", value=None)

    stake_df = load_stakes()

    stake_options = {
        stake_label(row.bigblind, row.ante): (row.bigblind, row.ante)
        for row in stake_df.itertuples(index=False)
    }

    selected_labels = st.sidebar.multiselect(
        "Stakes",
        options=list(stake_options.keys())
    )

    stakes = [
        stake_options[label] for label in selected_labels
    ]

    df = load_profit_data(start_date, end_date, stakes)

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

    if "selected_gamecode" not in st.session_state:
        st.session_state.selected_gamecode = None

    # Graph
    selected = plotly_events(fig, click_event=True)
    if selected:
        index = selected[0]["pointIndex"]
        if index > 0:
            st.session_state.selected_gamecode = df.iloc[index - 1]["gamecode"]

    if st.session_state.selected_gamecode:
        with st.expander(
            f"Hand {st.session_state.selected_gamecode}",
            expanded=True,
        ):
            st.markdown(
                f"<a href='/hand?hand={st.session_state.selected_gamecode}' target='_blank'>Open hand in a new tab</a>",
                unsafe_allow_html=True,
            )
            hand()

if __name__ == "__main__":
    main()