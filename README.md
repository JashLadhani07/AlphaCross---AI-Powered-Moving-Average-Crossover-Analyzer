Perfect — here’s your **final, polished, professional README.md** version, ready for GitHub or portfolio use, including the **deployment links (Vercel + Render)** and clean formatting (no emojis):

---

# **AlphaCross — AI-Driven MA Crossover Analyzer**

**AlphaCross** is a full-stack trading signal analyzer that uses **machine learning (XGBoost)** and **AI insights** to detect and backtest **moving average crossovers** on **NSE 500 stocks**.
It provides real-time analytics, ML-based signal predictions, an AI trading chatbot, and an interactive dashboard for backtesting performance.

**Live Demo:** [https://alpha-cross-an-ai-powered-moving-av.vercel.app/](https://alpha-cross-an-ai-powered-moving-av.vercel.app/)
**Backend API (Render):** *(example)* `https://alpha-cross-backend.onrender.com`

---

## **Key Features**

* **Real-Time Data:** Fetches 3-month end-of-day (EOD) prices for NSE 500 via *yfinance*
* **ML Predictions:** XGBoost model predicts bullish or bearish crossovers (3-day horizon)
* **Backtesting:** Comprehensive trade logs, profit metrics, and portfolio summaries
* **AI Chatbot:** GPT/Gemini-powered Q&A assistant for trading insights
* **Interactive Dashboard:** ReactJS + TailwindCSS dark UI with dynamic charts

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

**Backend:** [http://localhost:8000](http://localhost:8000)
**Frontend:** [http://localhost:3000](http://localhost:3000)

---

## **Core Endpoints**

| Endpoint             | Description                                      |
| -------------------- | ------------------------------------------------ |
| `/data/{symbol}`     | Fetch EMA, RSI, and price data                   |
| `/predict/{symbol}`  | Get ML prediction (Bullish/Bearish + confidence) |
| `/backtest/{symbol}` | Run MA crossover backtest with trade logs        |
| `/chat`              | AI chatbot for trading explanations              |

---

## **Model & Strategy**

* **Features:** EMA 20/50, RSI 14, EMA slopes, returns, and volatility
* **Model:** XGBoost Classifier (50 estimators, max_depth=3, learning_rate=0.1)
* **Labeling:** +1 = Bullish, −1 = Bearish
* **Backtest Metrics:** Win %, Profit %, Max Drawdown %, Risk-Reward Ratio, Profit Factor

---

## **Tech Stack**

**Backend:** FastAPI · XGBoost · Pandas · yfinance · TA-Lib · OpenAI/Gemini
**Frontend:** React 18 · TailwindCSS · Chart.js · Axios · Lucide

**Deployment:**

* **Frontend:** [Vercel](https://alpha-cross-an-ai-powered-moving-av.vercel.app/)
* **Backend:** Render (Uvicorn + FastAPI)

---

## **Example Usage**

```bash
curl http://localhost:8000/predict/TCS
```

**Response:**

```json
{
  "symbol": "TCS",
  "prediction": "Bullish",
  "confidence": 0.87
}
```

---

## **Maintainer**

Developed by **Jash Ladhani**
For project/demo purposes — not for live trading use.
