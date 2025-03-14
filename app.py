import dash
from dash import dcc, html, Input, Output, State, callback_context
import dash_bootstrap_components as dbc
import datetime
import plotly.graph_objects as go
import pandas as pd
from utils.fetch_data import fetch_stock_data, fetch_news  # Import stock data and news functions


# Utils
df = pd.read_csv("data/tickers.csv")
combined_tickers = df["Combined"].tolist() if "Combined" in df.columns else df["Ticker"].tolist()
date_ranges = {
    "1D": 1,
    "1W": 7,
    "1M": 30,
    "YTD": "YTD",
    "1Y": 365,
    "5Y": 1825,
    "MAX": "MAX",
}

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout
app.layout = dbc.Container(
    [
        # Header for the page
        html.H1("Stock Screener", className="text-center my-3"),
        # Input field for stock ticker and submit button
        dbc.Row(
            [
                dbc.Col(
                    dcc.Dropdown(
                        id="ticker-input",
                        options=[
                            {"label": i, "value": i.split(" - ")[0]} for i in combined_tickers
                        ],  # Extract ticker from combined format
                        placeholder="Enter or select a ticker...",
                    ),
                    width=9,
                ),
                dbc.Col(
                    dbc.Button(
                        "Submit",
                        id="submit-button",
                        color="primary",
                        className="btn-block",
                    ),
                    width=3,
                ),
            ],
            className="mb-3 align-items-center",
        ),  # Align items vertically
        # Chart with integrated date range buttons
        dcc.Loading(
            id="loading",
            type="default",
            children=[
                html.Div(
                    [
                        # Chart itself
                        dcc.Graph(id="candlestick-chart"),
                        # Date range buttons below the chart
                        html.Div(
                            dbc.ButtonGroup(
                                [
                                    # Date range buttons with new styling
                                    dbc.Button(
                                        label,
                                        id=f"btn-{label}",
                                        color="secondary",
                                        disabled=True,
                                        size="sm",  # Smaller buttons
                                        outline=True,  # Outlined style
                                        className="mx-1",  # Add spacing between buttons
                                    )
                                    for label in date_ranges.keys()
                                ],
                                id="date-buttons",
                                className="mb-3",
                            ),
                            style={
                                "textAlign": "center",
                                "marginTop": "-20px",
                            },  # Position closer to chart
                        ),
                    ]
                ),
            ],
        ),
        # News section
        html.Div(
            [
                html.H3("Latest News", className="mt-4 mb-3"),
                dcc.Loading(
                    id="news-loading",
                    type="default",
                    children=[html.Div(id="news-container", className="news-articles")],
                ),
            ]
        ),
        # Store components for data
        dcc.Store(id="stored-stock-data", data={}),
        dcc.Store(id="stored-news-data", data=[]),
    ],
    fluid=True,
)


# **New Callback**: Fetch stock data only when the ticker is selected
@app.callback(
    [
        Output("stored-stock-data", "data"),  # Store stock data
        Output("stored-news-data", "data"),  # Store news data
    ],
    [Input("submit-button", "n_clicks")],  # Trigger when submit button is clicked
    [State("ticker-input", "value")],  # Get the selected ticker
)
def fetch_and_store_data(n_clicks, ticker):
    if not n_clicks or not ticker:
        return {}, []  # Return empty if no ticker selected

    # Find the company name for news search
    company_name = ""
    for combined in combined_tickers:
        if combined.startswith(f"{ticker} - "):
            company_name = combined.split(" - ")[1]
            break

    # Use ticker if company name not found
    if not company_name:
        company_name = ticker

    # Fetch stock data once when the ticker is selected
    data = fetch_stock_data(ticker)
    if data is None or data.empty:
        return {}, []

    # Fetch news data
    news_data = fetch_news(company_name)
    if news_data is None:
        news_data = []

    # Add ticker information to the data
    result_dict = {"ticker": ticker, "data": data.to_dict("records")}

    # Return both stock data and news data
    return result_dict, news_data


# **Modified Callback**: Update chart and filter data based on selected date range
@app.callback(
    [
        Output("candlestick-chart", "figure"),
        Output("date-buttons", "children"),
    ],
    [Input("stored-stock-data", "data")]
    + [Input(f"btn-{label}", "n_clicks") for label in date_ranges.keys()],
)
def update_chart(stored_data, *args):
    ctx = callback_context

    # Handles the initial state
    if not stored_data or len(stored_data) == 0:
        return go.Figure(
            layout={
                "annotations": [
                    {
                        "text": "No data available",
                        "xref": "paper",
                        "yref": "paper",
                        "showarrow": False,
                    }
                ]
            }
        ), [
            dbc.Button(label, id=f"btn-{label}", color="secondary", disabled=True)
            for label in date_ranges.keys()
        ]

    # Get ticker from stored data
    ticker = stored_data.get("ticker", "")
    stock_data = stored_data.get("data", [])

    # Convert to DataFrame
    data = pd.DataFrame(stock_data)

    # Determine selected date range (default to YTD)
    selected_range = "YTD"
    # Check what triggered the callback
    if ctx.triggered:
        triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]
        # Only update selected range if a date button was clicked
        if any(f"btn-{label}" == triggered_id for label in date_ranges.keys()):
            for label in date_ranges.keys():
                if f"btn-{label}" == triggered_id:
                    selected_range = label
                    break
    else:
        triggered_id = None

    # Convert the date column to datetime
    data["date"] = pd.to_datetime(data["date"])

    # Get today's date as a Pandas Timestamp
    today = pd.Timestamp.today()

    # Apply date filtering
    if selected_range == "MAX":
        filtered_data = data  # No filtering, return all data
    elif selected_range == "YTD":
        start_of_year = pd.Timestamp(today.year, 1, 1)  # First day of the year
        filtered_data = data[data["date"] >= start_of_year]
    else:
        days = date_ranges[selected_range]
        filtered_data = data[data["date"] >= today - pd.Timedelta(days=days)]

    # Create Candlestick chart
    fig = go.Figure(
        data=[
            go.Candlestick(
                x=filtered_data["date"],
                open=filtered_data["open"],
                high=filtered_data["high"],
                low=filtered_data["low"],
                close=filtered_data["close"],
            )
        ]
    )

    fig.update_layout(
        title=f"{ticker.upper() if ticker else 'Stock'} Candlestick Chart",
        xaxis_title="Date",
        yaxis_title="Price",
        xaxis_rangeslider_visible=False,
    )

    # Enable date range buttons with improved styling
    enabled_buttons = []
    for label in date_ranges.keys():
        # Determine button color based on selected range
        if (f"btn-{label}" == triggered_id) or (
            label == selected_range and triggered_id != f"btn-{label}"
        ):
            button_color = "info"  # This button is selected - using info color for better contrast
            outline = False  # Solid button for selected
        else:
            button_color = "secondary"  # This button is not selected
            outline = True  # Outline style for unselected

        # Create button with appropriate styling
        button = dbc.Button(
            label,
            id=f"btn-{label}",
            color=button_color,
            size="sm",  # Smaller buttons
            outline=outline,  # Outlined style for unselected
            className="mx-1",  # Add spacing between buttons
            disabled=False,
        )
        enabled_buttons.append(button)

    return fig, enabled_buttons


# **New Callback**: Update news container based on fetched news data
@app.callback(Output("news-container", "children"), [Input("stored-news-data", "data")])
def update_news(news_data):
    if not news_data:
        return html.Div("No news available for this stock.", className="text-muted")

    # Limit to 5 news articles
    max_articles = min(5, len(news_data))
    news_items = []

    for i in range(max_articles):
        article = news_data[i]
        news_items.append(
            dbc.Card(
                dbc.CardBody(
                    [
                        html.Div(article["date"], className="text-muted small mb-1"),
                        html.H5(article["title"], className="card-title"),
                        html.A(
                            "Read Article",
                            href=article["url"],
                            target="_blank",
                            className="btn btn-outline-primary btn-sm",
                        ),
                    ]
                ),
                className="mb-3",
            )
        )

    return news_items


# Run app
if __name__ == "__main__":
    app.run_server(debug=True)
