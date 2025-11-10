# **AlphaCross — AI-Driven MA Crossover Analyzer**

**AlphaCross** is a full-stack trading signal analyzer that uses **machine learning (XGBoost)** and **AI insights** to detect and backtest **moving average crossovers** on **NSE 500 stocks**.

---

## **Key Features**

* **Real-Time Data:** Fetches 3-month end-of-day (EOD) prices (3:30 PM) for NSE 500 via *yfinance*
* **ML Predictions:** XGBoost predicts bullish or bearish crossovers (3-day horizon)
* **Backtesting:** Generates detailed trade logs, profit metrics, and performance summaries
* **AI Chatbot:** GPT/Gemini-powered Q&A for strategy and market insights
* **Interactive Dashboard:** ReactJS + TailwindCSS dark-mode interface with dynamic charts

---

## **Architecture**

```
alphacross/
├── backend/     # FastAPI + ML + Chatbot
│   ├── ml/      # data_fetch.py | features.py | model_xgb.py | backtest.py
│   └── ai/      # chat.py (GenAI integration)
└── frontend/    # ReactJS Dashboard
    ├── src/components | pages | api
    └── public/
```

---

## **Quick Start**

### **Backend Setup**

```bash
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### **Frontend Setup**

```bash
cd frontend
npm install
npm start
```

**Backend URL:** [http://localhost:8000](http://localhost:8000)
**Frontend URL:** [http://localhost:3000](http://localhost:3000)

---

## **Core Endpoints**

/data/{symbol} - Fetch EMA, RSI, and price data
/predict/{symbol} - Get ML prediction (Bullish/Bearish + confidence)
/backtest/{symbol} - Run MA crossover backtest
/chat - Chatbot for trading explanations

---

## **Model & Strategy**

* **Features:** EMA 20/50, RSI 14, EMA slopes, returns, volatility
* **Model:** XGBoost Classifier (50 estimators, max depth 3, learning rate 0.1)
* **Labeling:** +1 = Bullish, −1 = Bearish
* **Backtest Metrics:** Win %, Profit %, Max Drawdown %, Risk-Reward Ratio, Profit Factor

---

## **Tech Stack**

**Backend:** FastAPI · XGBoost · Pandas · yfinance · TA-Lib · OpenAI/Gemini
**Frontend:** React 18 · TailwindCSS · Chart.js · Axios · Lucide
