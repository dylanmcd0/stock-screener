import dash
from dash import dcc, html, Input, Output, State, callback_context
import dash_bootstrap_components as dbc
import datetime
import plotly.graph_objects as go
import pandas as pd
from utils.fetch_data import fetch_stock_data  # Import only stock data function for now


date_ranges = {
    "1D": 1, "1W": 7, "1M": 30, "YTD": "YTD", "1Y": 365, "5Y": 1825, "MAX": "MAX"
}

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout
app.layout = dbc.Container([
    html.H1("Stock Candlestick Chart", className="text-center my-3"),
    
    # Input field for stock ticker
    dbc.Row([
        dbc.Col(dcc.Input(id="ticker-input", type="text", placeholder="Enter Ticker", className="form-control")),
        dbc.Col(dbc.Button("Submit", id="submit-button", color="primary", className="btn-block"))
    ], className="mb-3"),
    
    # Date range selection buttons (disabled initially)
    dbc.Row([
        dbc.Col([
            dbc.ButtonGroup(
                [dbc.Button(label, id=f"btn-{label}", color="secondary", disabled=True) for label in date_ranges.keys()],
                id="date-buttons",
                className="mb-3"
            )
        ])
    ]),
    
    # Candlestick chart (initially empty)
    dcc.Graph(id="candlestick-chart"),

], fluid=True)


# Callback to enable buttons and update chart
@app.callback(
    [Output("candlestick-chart", "figure"),
     Output("date-buttons", "children")],  # Enable buttons after fetching data
    [Input("submit-button", "n_clicks")] + [Input(f"btn-{label}", "n_clicks") for label in date_ranges.keys()],
    [State("ticker-input", "value")]
)
def update_chart(n_clicks, *args):
    ctx = callback_context

    if not ctx.triggered:
        return go.Figure(), [dbc.Button(label, id=f"btn-{label}", color="secondary", disabled=True) for label in date_ranges.keys()]
    
    triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]

    # Extract ticker
    ticker = args[-1].upper() if args[-1] else None
    if not ticker:
        return go.Figure(), [dbc.Button(label, id=f"btn-{label}", color="secondary", disabled=True) for label in date_ranges.keys()]

    # Fetch stock data
    data = fetch_stock_data(ticker)
    if data is None:
        return go.Figure(), [dbc.Button(label, id=f"btn-{label}", color="secondary", disabled=True) for label in date_ranges.keys()]

    # Default to YTD when ticker is selected
    selected_range = "YTD"
    for label in date_ranges.keys():
        if f"btn-{label}" == triggered_id:
            selected_range = label
            break

    # Filter data based on selected range
    today = datetime.date.today()
    if selected_range == "MAX":
        filtered_data = data
    elif selected_range == "YTD":
        filtered_data = data[data.index >= f"{today.year}-01-01"]
    else:
        days = date_ranges[selected_range]
        filtered_data = data[data.index >= today - datetime.timedelta(days=days)]

    # Create Candlestick chart
    fig = go.Figure(data=[go.Candlestick(
        x=filtered_data.index,
        open=filtered_data["Open"],
        high=filtered_data["High"],
        low=filtered_data["Low"],
        close=filtered_data["Close"]
    )])

    fig.update_layout(
        title=f"{ticker} Candlestick Chart ({selected_range})",
        xaxis_title="Date",
        yaxis_title="Price",
        xaxis_rangeslider_visible=False
    )

    # Enable date range buttons
    enabled_buttons = [dbc.Button(label, id=f"btn-{label}", color="primary", disabled=False) for label in date_ranges.keys()]

    return fig, enabled_buttons


# Run app
if __name__ == "__main__":
    app.run_server(debug=True)
