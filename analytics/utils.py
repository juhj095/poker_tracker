# Lines start at 0, change numpy.float64 to float due to plotly_events
def y_axis(total):
    return [0.0] + total.astype(float).tolist()