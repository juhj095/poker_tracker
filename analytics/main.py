import streamlit as st
import plotly.graph_objects as go
from db_helpers import get_connection, profit_over_time
import pandas as pd

def main():
    st.set_page_config(page_title="Poker Tracker", layout="wide")
    st.title("Poker Tracker 📈")

    # Filters
    st.sidebar.header("Filters")
    unit = st.sidebar.radio("Display unit:", ["€", "Big Blinds"])
    show_showdown = st.sidebar.checkbox("Showdown/Non SD Winnings", False)

    start_date = st.sidebar.date_input("Start date", value=None)
    end_date = st.sidebar.date_input("End date", value=None)

    # DB Query
    connection = get_connection()
    query= profit_over_time( # TODO params
        start_date=start_date,
        end_date=end_date
    )
    df = pd.read_sql(query, connection) # TODO params=params
    connection.close()

    if df.empty:
        st.warning("No data found — check your database or date filters.")
    else:
        df["startdate"] = pd.to_datetime(df["startdate"])

        # Sort and compute cumulative lines
        df = df.sort_values(["startdate", "hand_id"]).reset_index(drop=True)
        df["show_profit"] = df["profit"].where(df["showdown"] == 1, 0.0)
        df["noshow_profit"] = df["profit"].where(df["showdown"] == 0, 0.0)
        df["cum_total"] = df["profit"].cumsum()
        df["cum_show"] = df["show_profit"].cumsum()
        df["cum_noshow"] = df["noshow_profit"].cumsum()

         # BB equivalents
        df["profit_bb"] = df["profit"] / df["bigblind"]
        df["show_profit_bb"] = df["show_profit"] / df["bigblind"]
        df["noshow_profit_bb"] = df["noshow_profit"] / df["bigblind"]

        df["cum_total_bb"] = df["profit_bb"].cumsum()
        df["cum_show_bb"] = df["show_profit_bb"].cumsum()
        df["cum_noshow_bb"] = df["noshow_profit_bb"].cumsum()

        # Start all lines from 0
        df_plot = pd.concat([
            pd.DataFrame([{
                "cum_total": 0,
                "cum_show": 0,
                "cum_noshow": 0,
                "cum_total_bb": 0,
                "cum_show_bb": 0,
                "cum_noshow_bb": 0
            }]),
            df
        ], ignore_index=True)

        # Graph unit
        if unit == "€":
            y_total = df_plot["cum_total"]
            y_show = df_plot["cum_show"]
            y_noShow = df_plot["cum_noshow"]
            y_label = "Profit (€)"
        else:
            y_total = df_plot["cum_total_bb"]
            y_show = df_plot["cum_show_bb"]
            y_noShow = df_plot["cum_noshow_bb"]
            y_label = "Profit (bb)"

        # Plot
        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=df_plot.index,
                y=y_total,
                name="Total",
                line=dict(color="green"),
            )
        )

        if show_showdown:
            fig.add_trace(
                go.Scatter(
                    x=df_plot.index,
                    y=y_show,
                    name="Showdown",
                    line=dict(color="blue"),
                )
            )
            fig.add_trace(
                go.Scatter(
                    x=df_plot.index,
                    y=y_noShow,
                    name="Non-Showdown",
                    line=dict(color="red"),
                )
            )

        fig.update_layout(
            title="Profit Over Time",
            xaxis_title="Hands Played",
            yaxis_title=y_label,
            template="plotly_white",
        )

        st.plotly_chart(fig, width="stretch")

        # Extra stats
        st.subheader("Summary")
        total_hands = len(df_plot) - 1 # exclude the initial 0 row
        total_profit_bb = df["profit_bb"].sum()
        bb_per_100 = (total_profit_bb / total_hands) * 100 if total_hands > 0 else 0
        total_profit = df_plot["profit"].sum()

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

if __name__ == "__main__":
    main()