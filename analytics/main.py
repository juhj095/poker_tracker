import streamlit as st
import plotly.graph_objects as go
from db_helpers import get_connection, profit_over_time
import pandas as pd

def main():
    st.set_page_config(page_title="Poker Tracker", layout="wide")
    st.title("Poker Tracker 📈")

    # Filters
    st.sidebar.header("Filters")
    show_showdown = st.sidebar.checkbox("Showdown/Non SD Winnings", False)

    # DB Query
    connection = get_connection()
    query = profit_over_time()
    df = pd.read_sql(query, connection)
    connection.close()

    if df.empty:
        st.warning("No data found — check your database or date filters.")
    else:
        df["startdate"] = pd.to_datetime(df["startdate"])

        # ✅ Sort and compute cumulative lines
        df = df.sort_values(["startdate", "hand_id"]).reset_index(drop=True)
        df["show_profit"] = df["profit"].where(df["showdown"] == 1, 0.0)
        df["noshow_profit"] = df["profit"].where(df["showdown"] == 0, 0.0)
        df["cum_total"] = df["profit"].cumsum()
        df["cum_show"] = df["show_profit"].cumsum()
        df["cum_noshow"] = df["noshow_profit"].cumsum()

        # Calculate profit in big blinds and bb/100
        df["profit_bb"] = df["profit"] / df["bigblind"]

        total_hands = len(df) - 1  # exclude the initial 0 row
        total_profit_bb = df["profit_bb"].sum()
        bb_per_100 = (total_profit_bb / total_hands) * 100 if total_hands > 0 else 0

        # Start all lines from 0
        df = pd.concat([
            pd.DataFrame([{"hand_id": 0, "cum_total": 0, "cum_show": 0, "cum_noshow": 0}]),
            df
        ], ignore_index=True)

        # Plot
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df.index, y=df["cum_total"], name="Total", line=dict(color="green")))
        if show_showdown:
            fig.add_trace(go.Scatter(x=df.index, y=df["cum_show"], name="Showdown", line=dict(color="blue")))
            fig.add_trace(go.Scatter(x=df.index, y=df["cum_noshow"], name="Non-Showdown", line=dict(color="red")))

        fig.update_layout(
            title="Profit Over Time",
            xaxis_title="Hands Played",
            yaxis_title="Profit (€)",
            template="plotly_white"
        )

        st.plotly_chart(fig, width="stretch")

        # Extra stats
        st.subheader("Summary")
        total_hands = len(df)
        total_profit = df["profit"].sum()

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Hands", total_hands)
        col2.metric("Total Profit (€)", round(total_profit, 2))
        col3.metric("Winrate (bb/100)", round(bb_per_100, 2))

if __name__ == "__main__":
    main()