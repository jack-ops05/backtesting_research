#STD
#TP
import plotly.graph_objects as go
#LCL

def _plotEquity(x, y):
    #Purpose of function: To plot equity curve using Plotly.

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Equity Curve'))
    fig.update_layout(title='Equity Curve', xaxis_title='Timestamp', yaxis_title='Equity', template='plotly_dark')
    fig.show()
