# Stock Screener

## **Overview**
A lightweight, interactive stock screener built with Dash and Plotly that allows users to visualize stock price data and related news. 

This application provides basic tooling for analyzing stocks through price charts with customizable time ranges and relevant news articles.

![Stock Screener Screenshot](data/images/current_ui.png)

---
## **Recent Improvements**
- Added news articles
- Deployed using Render
- Added some very basic styling (don't judge the front end)

---
## **TODO / Roadmap**
- [ ] Add technical indicators (Moving averages, MACD, RSI)
- [ ] Implement custom date range selection
- [ ] Add basic metrics (P/E ratio, market cap, etc.)
- [ ] Compare metrics to S&P or sector average
- [ ] Include options data for selected stock
- [ ] Deploy app to webserver
- [ ] Simple financial statement analysis 
- [ ] Add dark mode toggle

---
## **Features**
- **Interactive Stock Search**: Search for any stock using ticker symbols from the S&P 500
- **Candlestick Charts**: Visualize price movements with adjustable time ranges (1D, 1W, 1M, YTD, 1Y, 5Y, MAX)
- **Latest News**: Display recent news articles related to the selected company
- **Responsive Design**: Built with Bootstrap components for a clean, mobile-friendly interface

---
## **Data Sources & APIs**
This project leverages the following data sources:

| **Data Type**      | **Source/API**           |
|--------------------|--------------------------|
| Stock Price Data   | Yahoo Finance API        |
| Company News       | News API                 |
| Company Listings   | Wikipedia (S&P 500 list) |

---
## **Repository Structure**
```
📂 /stock-screener
│── 📜 app.py                   → Main Dash application
│── 📦 requirements.txt         → Python dependencies
│── 📖 README.md                → Project documentation
│── 📄 .env                     → API keys (not committed to Git)
│
├── 📊 data/
│   └── 📈 tickers.csv          → List of available stock tickers
│
├── 📓 fetch_tickers.ipynb      → Notebook for fetching ticker data
│
└── 🔍 utils/
    └── 📡 fetch_data.py        → Functions for data retrieval
```

---
## **Setup & Installation**
### **Prerequisites**
- Python 3.8+
- pip or uv package installer

### **Installation**
```bash
# Clone the repository
git clone https://github.com/dylanmcd0/stock-screener.git
cd stock-screener

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
# Using pip:
pip install -r requirements.txt
# Or using uv (faster):
uv pip install -r requirements.txt
```

### **API Keys**
Create a `.env` file in the root directory and add your News API key:
```
NEWS_API_KEY=your_news_api_key_here
```

You can obtain a free News API key from [newsapi.org](https://newsapi.org/).

---
## **Running the Application**
```bash
python -m app
```

Navigate to http://127.0.0.1:8050/ in your web browser to use the application.

---
## **Deployment Details**

- Deployed with [Render](https://render.com/)
- Using the free tier for now (may upgrade in the future)
- Hosted at [this url](https://stock-screener-app-2iwt.onrender.com)
- May change deployment strategy (Heroku, Docker + ECS, idk)
    - Or at least upgrade to paid tier (free takes so long to spin up)

---
## **Author**
👤 **Dylan R. McDonald**  
💼 **Commodities Technology Associate | Aspiring Investment Analyst**  
📧 **dylmcdona@icloud.com**  
