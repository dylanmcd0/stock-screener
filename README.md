# Stock Screener

## **Overview**
This project is designed to be a tool for initial stock screening for an analyst just beginning his or her research into a specific company.
It offers very surface-level analysis of company information, moreso designed for me to work on my Plotly Dash skills, as well as practice
some basic financial modeling and anlaysis. 

---
## **In Progress**
**Current Tasks:**
- Caching data to prevent repetiive API requests
- Adding company metrics
- Incorporating company news articles

---
## **1. Investment Thesis**
Equity long/short strategies rely on identifying **high-quality, undervalued stocks** for long positions and **low-quality, overvalued stocks** for short positions.

This model incorporates fundamental analysis alongside machine learning-driven sentiment analysis to enhance decision-making:

- **Longs:** Companies with **strong revenue growth, profitability, and favorable sentiment**.
- **Shorts:** Companies with **declining earnings, high debt, and negative sentiment**.

**Sector Focus:** The **TMT sector** is ideal due to:
- **High dispersion** in fundamentals (growth vs. declining companies)
- **Frequent earnings surprises** affecting stock prices
- **Hedge fund interest** in relative valuation plays

---
## **2. Data Sources & APIs**
This project collects **fundamental, price, and sentiment data** using:

| **Data Type**          | **Source/API**                 |
|------------------------|--------------------------------|
| Earnings Transcripts  | Webscrapping |
| Stock Prices          | Yahoo Finance, Quandl          |
| Sentiment Analysis    | FinBERT, OpenAI API (ChatGPT)  |

---
## **3. Stock Ranking Model**
Each stock is ranked based on a **multi-factor scoring system**:

| **Factor**             | **Metric**                     | **Weight (%)** |
|------------------------|--------------------------------|---------------|
| **Growth**             | 5Y Revenue CAGR, EPS CAGR     | 20%           |
| **Profitability**      | ROIC, Gross Margins, FCF Yield | 20%           |
| **Valuation**          | P/E, P/B, EV/EBITDA vs. Sector | 20%           |
| **Financial Health**   | Debt/Equity, Interest Coverage | 20%           |
| **Sentiment Analysis** | Earnings Call Sentiment, Insider Buying | 20% |

📌 **Top 10% of stocks = Longs**  
📌 **Bottom 10% of stocks = Shorts**  

---
## **4. Portfolio Construction & Risk Management**
- **Sector-Neutral:** Equal exposure to long & short positions within TMT
- **Position Sizing:** Equal-weighted or volatility-adjusted allocations
- **Risk Controls:** Stop-loss, max drawdown limits, and liquidity screening
- **Rebalancing:** Monthly or quarterly portfolio updates

---
## **5. Backtesting Methodology**
The strategy is backtested using **historical stock prices and fundamental data**:

- **Backtesting Framework:** Backtrader, QuantConnect
- **Benchmark:** S&P 500 (SPY) or TMT sector ETF (XLK)
- **Performance Metrics:**
  ✅ **Annualized Return & Alpha**  
  ✅ **Sharpe Ratio** (Risk-adjusted performance)  
  ✅ **Max Drawdown** (Risk exposure)  
  ✅ **Factor Contribution Analysis**  

---
## **6. Repository Structure**
```
📂 /stock-screener
│── 📜 **app.py**                     → Main entry point for the Dash app   
│── 📦 **requirements.txt**            → Dependencies (e.g., dash, yfinance, plotly)  
│── 📖 **README.md**                   → Project documentation
│── 🚫 **.gitignore**                  → Ignore unnecessary files (e.g., __pycache__)  
│
├── 🎨 **assets/**                     → Static files (CSS, JS, images)
│   ├── 🎨 **styles.css**              → Custom styles for the dashboard
│
├── 📦 **components/**                 → Reusable UI components
│   ├── 🏗️ **layout.py**               → Layout definition (separate UI from logic)  
│   ├── 🔄 **callbacks.py**            → Dash callbacks for interactivity
│
├── 📊 **data/**                       → Any local data files (optional, if needed) 
│
└── 🔍 **utils/**                      → Helper functions (e.g., API requests)
    ├── 📡 **fetch_data.py**           → API functions for stock data, news, etc.
    ├── 🧮 **calculations.py**         → Any financial calculations (DCF, ratios)

```

---
## **7. How to Run Locally**
### **Installation**
I want to productionize this, but might not get to. 
If you want to use this just follow along.
```bash
# Clone the repository
git clone https://github.com/dylanmcd0/stock-screener.git
cd stock-screener

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies (I use uv, it's much faster)
uv pip install -r requirements.txt
```

### **Run App**
```bash
python -m app.py
```

---
## **8. Future Improvements**
🔹 **Enhance Sentiment Analysis:** Use deep-learning models (BERT) for better transcript analysis  
🔹 **Expand Universe:** Apply to **other sectors** or **global markets**  
🔹 **Alternative Data Signals:** Incorporate **Google Trends, web traffic, credit card data**  
🔹 **Leverage Machine Learning:** Predict earnings surprises based on fundamental patterns  

---
## **Author & Contact**
👤 **Dylan R. McDonald**  
💼 **Commodities Technology Associate | Aspiring Investment Analyst**  
📧 **dylmcdona@icloud.com**  
🔗 **[]**  
📂 **[]**  

---