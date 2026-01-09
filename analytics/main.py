import streamlit as st
import plotly.graph_objects as go
from streamlit_plotly_events import plotly_events
import pandas as pd
from load_data import load_profit_data
from utils import y_axis

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

    # Graph unit
    if unit == "€":
        total = df["cum_total"]
        show = df["cum_show"]
        noShow = df["cum_noshow"]
        label = "Profit (€)"
    else:
        total = df["cum_total_bb"]
        show = df["cum_show_bb"]
        noShow = df["cum_noshow_bb"]
        label = "Profit (bb)"

    # Plot
    fig = go.Figure()

    hands_played_list = list(range(len(df) + 1))

    fig.add_trace(go.Scatter(
        x = hands_played_list,
        y = y_axis(total),
        name = "Total",
        mode = "lines+markers",
        customdata = [None] + df["hand_id"].tolist(),
        line = dict(color="green"),
        marker = dict(opacity=0),
    ))

    if show_showdown:
        fig.add_trace(go.Scatter(
            x = hands_played_list,
            y = y_axis(show),
            name = "Showdown",
            line = dict(color="blue"),
        ))
        fig.add_trace(go.Scatter(
            x = hands_played_list,
            y = y_axis(noShow),
            name  = "Non-Showdown",
            line = dict(color="red"),
        ))

    fig.update_xaxes(
        range = [0, len(df)],
        tickformat = ",d"
    )

    fig.update_yaxes(tickformat=",.2f")

    fig.update_layout(
        title = "Profit Over Time",
        xaxis_title = "Hands Played",
        yaxis_title = label,
        template = "plotly_dark"
    )

    # Extra stats
    st.subheader("Summary")
    total_hands = len(df)
    total_profit_bb = df["cum_total_bb"][len(df) - 1]
    bb_per_100 = (total_profit_bb / total_hands) * 100
    total_profit = df["cum_total"][len(df) - 1]

    if unit == "€":
        profit_display = round(total_profit, 2)
        profit_label = "Total Profit (€)"
    else:
        profit_display = round(total_profit_bb, 2)
        profit_label = "Total Profit (bb)"

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Hands", total_hands)
    col2.metric(profit_label, profit_display)
    col3.metric("Winrate (bb/100)", round(bb_per_100, 2))

    # Graph
    selected = plotly_events(fig, click_event=True)
    if selected:
        index = selected[0]["pointIndex"]
        hand_id = df.iloc[index - 1]["hand_id"] if index > 0 else None

        if pd.notna(hand_id):
            st.markdown(
                f"<a href='/hand?hand_id={hand_id}' target='_blank'>Open hand {hand_id}</a>",
                unsafe_allow_html=True,
            )

if __name__ == "__main__":
    main()