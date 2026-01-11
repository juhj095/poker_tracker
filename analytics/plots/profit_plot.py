import plotly.graph_objects as go

# Lines start at 0, change numpy.float64 to float due to plotly_events
def y_axis(total):
    return [0.0] + total.astype(float).tolist()

def build_profit_figure(
    df,
    total,
    show,
    noshow,
    label,
    show_showdown
):
    fig = go.Figure()

    hands_played = list(range(len(df) + 1))

    fig.add_trace(
        go.Scatter(
            x=hands_played,
            y=y_axis(total),
            name="Total",
            mode="lines+markers",
            customdata=[None] + df["hand_id"].tolist(),
            line=dict(color="green"),
            marker=dict(opacity=0),
        )
    )

    if show_showdown:
        fig.add_trace(
            go.Scatter(
                x=hands_played,
                y=y_axis(show),
                name="Showdown",
                line=dict(color="blue"),
            )
        )
        fig.add_trace(
            go.Scatter(
                x=hands_played,
                y=y_axis(noshow),
                name="Non-Showdown",
                line=dict(color="red"),
            )
        )

    fig.update_xaxes(range=[0, len(df)], tickformat=",d")
    fig.update_yaxes(tickformat=",.2f")

    fig.update_layout(
        title="Profit Over Time",
        xaxis_title="Hands Played",
        yaxis_title=label,
        template="plotly_dark",
        autosize=True,
        margin=dict(l=40, r=40, t=40, b=40),
    )

    return fig