# Stock Screener

## **Overview**
A lightweight, interactive stock screener built with Dash and Plotly that allows users to visualize stock price data and related news. 

This application provides essential tools for analyzing stocks through candlestick charts with customizable time ranges and relevant news articles.

I will be adding more things in the future

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
## **Current Development**
- Implementing caching to reduce API requests
- Adding fundamental financial metrics
- Improving the news integration with better filtering

---
## **Future Improvements**
- Implement portfolio tracking functionality
- Add financial statements visualization
- Include options data for selected stocks
- Basic financial modeling
- Deployment (hopefully soon)


---
## **Author**
👤 **Dylan R. McDonald**  
💼 **Commodities Technology Associate | Aspiring Investment Analyst**  
📧 **dylmcdona@icloud.com**  
