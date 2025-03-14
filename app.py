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

app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
    ],
    assets_folder="assets",
)

app._favicon = "assets/favicon.ico"  # Add a favicon reference to ensure assets are loaded


app.layout = html.Div(
    [
        dbc.Container(
            [
                # Header for the page with custom styling
                html.Div(
                    [
                        html.H1(
                            "Stock Screener",
                            className="text-center my-3",
                            style={"color": "#1e88e5", "fontWeight": "700", "marginBottom": "25px"},
                        )
                    ],
                    style={
                        "background": "#f0f8ff",
                        "padding": "20px",
                        "borderRadius": "10px",
                        "marginBottom": "20px",
                    },
                ),
                # Input field for stock ticker and submit button
                dbc.Row(
                    [
                        dbc.Col(
                            dcc.Dropdown(
                                id="ticker-input",
                                options=[
                                    {"label": i, "value": i.split(" - ")[0]}
                                    for i in combined_tickers
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
                ),
                dcc.Loading(
                    id="loading",
                    type="default",
                    children=[
                        html.Div(
                            [
                                html.Div(
                                    dcc.Graph(id="candlestick-chart"),
                                    style={
                                        "border": "1px solid #e0e0e0",
                                        "borderRadius": "10px",
                                        "padding": "5px",
                                        "backgroundColor": "#f8fafc",
                                        "boxShadow": "0 4px 8px rgba(0,0,0,0.08)",
                                    },
                                ),
                                # Date range buttons below the chart
                                html.Div(
                                    dbc.ButtonGroup(
                                        [
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
                                        "marginTop": "10px",
                                        "marginBottom": "10px",
                                    },  # Positioned below chart with proper spacing
                                ),
                            ]
                        ),
                    ],
                ),
                # News section
                html.Div(
                    [
                        html.H3(
                            "Latest News",
                            className="mt-4 mb-3",
                            style={
                                "color": "#1976d2",
                                "fontWeight": "600",
                                "borderBottom": "2px solid #bbdefb",
                                "paddingBottom": "8px",
                                "display": "inline-block",
                            },
                        ),
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
    ]
)


# Fetch stock data only when the ticker is selected
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

    # Find the company name for news search or use ticker
    company_name = ""
    for combined in combined_tickers:
        if combined.startswith(f"{ticker} - "):
            company_name = combined.split(" - ")[1]
            break
    if not company_name:
        company_name = ticker

    data = fetch_stock_data(ticker)
    if data is None or data.empty:
        return {}, []

    news_data = fetch_news(company_name)
    if news_data is None:
        news_data = []

    result_dict = {"ticker": ticker, "data": data.to_dict("records")}

    return result_dict, news_data


# Update chart and filter data
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

    data = pd.DataFrame(stock_data)
    selected_range = "YTD"
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

    data["date"] = pd.to_datetime(data["date"])
    today = pd.Timestamp.today()

    if selected_range == "MAX":
        filtered_data = data
    elif selected_range == "YTD":
        start_of_year = pd.Timestamp(today.year, 1, 1)
        filtered_data = data[data["date"] >= start_of_year]
    else:
        days = date_ranges[selected_range]
        filtered_data = data[data["date"] >= today - pd.Timedelta(days=days)]

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

    enabled_buttons = []
    for label in date_ranges.keys():
        if (f"btn-{label}" == triggered_id) or (
            label == selected_range and triggered_id != f"btn-{label}"
        ):
            button_style = {
                "backgroundColor": "#1e88e5",
                "color": "white",
                "fontWeight": "bold",
                "boxShadow": "0 4px 8px rgba(0,0,0,0.2)",
                "border": "none",
                "borderRadius": "20px",
                "padding": "6px 15px",
                "transform": "scale(1.05)",
            }
            button_color = None
            outline = False
        else:
            button_style = {
                "backgroundColor": "#f1f5f9",
                "color": "#64748b",
                "border": "1px solid #cbd5e1",
                "borderRadius": "20px",
                "padding": "6px 15px",
            }
            button_color = None
            outline = False

        button = dbc.Button(
            label,
            id=f"btn-{label}",
            color=button_color,
            style=button_style,
            size="sm",
            outline=outline,
            className="mx-1 my-2",  # Add spacing between buttons
            disabled=False,
        )
        enabled_buttons.append(button)

    return fig, enabled_buttons


# Update news container based on fetched news data
@app.callback(Output("news-container", "children"), [Input("stored-news-data", "data")])
def update_news(news_data):
    if not news_data:
        return html.Div("No news available for this stock.", className="text-muted")

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
                            style={
                                "backgroundColor": "#e3f2fd",
                                "color": "#1976d2",
                                "fontWeight": "500",
                                "border": "none",
                                "borderRadius": "20px",
                                "boxShadow": "0 2px 4px rgba(0,0,0,0.1)",
                                "padding": "5px 15px",
                                "transition": "all 0.2s ease",
                            },
                        ),
                    ]
                ),
                className="mb-3",
                style={
                    "border": "none",
                    "borderLeft": "4px solid #1e88e5",
                    "borderRadius": "8px",
                    "boxShadow": "0 4px 8px rgba(0,0,0,0.1)",
                    "backgroundColor": "white",
                    "transition": "all 0.3s ease",
                },
            )
        )

    return news_items


if __name__ == "__main__":
    app.run_server(debug=True)
