# Fundamental Long/Short Equity Strategy with Data-Driven Insights

## **Overview**
This project implements a fundamental long/short equity strategy for the Technology, Media, & Telecommunications (TMT) sector. The strategy ranks stocks based on key **fundamental factors**, **valuation metrics**, and **earnings sentiment analysis**, constructing a sector-neutral portfolio that is backtested against a benchmark.

By integrating data-driven insights with traditional fundamental investing, this project demonstrates a structured approach to hedge fund-style equity selection.

---
## **In Progress**

**Current Tasks:**
- Gathering and cleaning data

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
/stock-screener
│── app.py                     # Main entry point for the Dash app
│── requirements.txt            # Dependencies (e.g., dash, yfinance, plotly)
│── README.md                   # Project documentation
│── .gitignore                   # Ignore unnecessary files (e.g., __pycache__)
│
├── assets/                     # Static files (CSS, JS, images)
│   ├── styles.css              # Custom styles for the dashboard (optional)
│
├── components/                 # Reusable UI components
│   ├── layout.py               # Layout definition (separate UI from logic)
│   ├── callbacks.py            # Dash callbacks for interactivity
│
├── data/                       # Any local data files (optional, if needed)
│
└── utils/                      # Helper functions (e.g., API requests)
    ├── fetch_data.py           # API functions for stock data, news, etc.
    ├── calculations.py         # Any financial calculations (DCF, ratios)
```

---
## **7. How to Run This Project**
### **Installation**
```bash
# Clone the repository
git clone https://github.com/yourgithub/long-short-equity-tmt.git
cd long-short-equity-tmt

# Install dependencies
pip install -r requirements.txt
```

### **Run Data Processing & Backtest**
```bash
python main.py
```

---
## **8. Future Improvements**
🔹 **Enhance Sentiment Analysis:** Use deep-learning models (BERT) for better transcript analysis  
🔹 **Expand Universe:** Apply to **other sectors** or **global markets**  
🔹 **Alternative Data Signals:** Incorporate **Google Trends, web traffic, credit card data**  
🔹 **Leverage Machine Learning:** Predict earnings surprises based on fundamental patterns  

---
## **9. Conclusion**
This project showcases a basic fundamental long/short equity strategy that combines:
✅ **Traditional valuation and fundamental analysis**
✅ **Earnings call sentiment analysis & alternative data**
✅ **Systematic portfolio construction & backtesting**

---
## **Author & Contact**
👤 **Dylan R. McDonald**  
💼 **Commodities Technology Associate | Aspiring Investment Analyst**  
📧 **dylmcdona@icloud.com**  
🔗 **[]**  
📂 **[]**  

---