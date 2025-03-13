import pandas as pd
import yfinance as yf
import requests
import datetime
import json

def fetch_sp500_tickers():
    """
    Fetches the current S&P 500 tickers and company names from Wikipedia and saves them to a CSV.
    """

    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    tables = pd.read_html(requests.get(url).text)
    df = tables[0]  # First table contains the S&P 500 tickers and company names

    tickers = df["Symbol"].tolist()
    company_names = df["Security"].tolist()
    combined = df["Symbol"] + " - " + df["Security"]

    pd.DataFrame({'Ticker': tickers, 'Company Name': company_names, 'Combined': combined}).to_csv("data/tickers.csv", index=False)
    print("S&P 500 tickers and company names saved to tickers.csv")

def fetch_stock_data(ticker):
    """Fetches historical stock data for the given ticker from Yahoo Finance API"""
    try:
        today = datetime.date.today().strftime("%Y-%m-%d")
        data = yf.download(ticker, start="1900-01-01", end=today, group_by="ticker")
        if data.empty:
            raise Exception("No data available for the given ticker.")
        else:
            data.columns = data.columns.droplevel(0)
            data.index = data.index.date
            data.columns = ["Open", "High", "Low", "Close", "Volume"]
            return data
    except Exception as e:
        print(f"Error fetching stock data for {ticker}: {str(e)}")
        return None
    
def fetch_income_statement(ticker):
    """
    Fetches the income statement for the given ticker from Yahoo Finance API
    """
    try:
        data = yf.Ticker(ticker)
        return data.financials
    except Exception as e:
        print(f"Error fetching income statement for {ticker}: {str(e)}")
        return None

def fetch_balance_sheet(ticker):
    """
    Fetches the balance sheet for the given ticker from Yahoo Finance API
    """
    try:
        data = yf.Ticker(ticker)
        return data.balance_sheet
    except Exception as e:
        print(f"Error fetching balance sheet for {ticker}: {str(e)}")
        return None

def fetch_cash_flow(ticker):
    """
    Fetches the cash flow statement for the given ticker from Yahoo Finance API
    """
    try:
        data = yf.Ticker(ticker)
        return data.cashflow
    except Exception as e:
        print(f"Error fetching cash flow statement for {ticker}: {str(e)}")
        return None