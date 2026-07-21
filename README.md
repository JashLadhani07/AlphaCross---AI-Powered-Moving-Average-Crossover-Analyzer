# AlphaCross: AI-Powered Moving Average Crossover & Market Insight Platform

A full-stack trading analytics platform for the **NSE 500** universe. It combines live YFinance market data, EMA-crossover signal detection, an XGBoost ML predictor, a full-universe screener, a portfolio-level backtester, and a GPT-4-Turbo trading assistant, all wrapped in a React dashboard.

---

## Features

- **NSE 500 Universe Screener** - scans up to all 500 Nifty 500 constituents in parallel and buckets them into Bullish / Bearish / Neutral based on EMA 20 vs EMA 50, with sector tagging and search.
- **Hybrid NSE 500 Data Loader** - automatically downloads the latest official Nifty 500 constituent list with seamless fallback to a bundled local CSV, ensuring reliable production deployments while continuing to use live Yahoo Finance market data.
- **Single-Stock Analysis** - live price, EMA 20/50, RSI, and an XGBoost-based crossover prediction with a confidence score.
- **Single-Stock Backtest** - EMA-crossover strategy backtest with full trade logs (entry/exit price & date, P&L, win rate, risk-reward ratio, profit factor, max drawdown).
- **Universe Backtest** - runs the crossover strategy across a configurable slice of the NSE 500 (max stocks, initial capital, position size %, stop loss %, take profit %) and returns portfolio-level metrics: total return, win rate, best/worst trade, top-performing sectors, and a ranked trade list.
- **Top Movers** - daily gainers/losers across a curated liquid-stock basket.
- **AI Chatbot** - GPT-4-Turbo (with GPT-3.5 and Gemini fallbacks, plus a fully offline rule-based fallback) that explains signals, answers "should I buy/sell" style questions with risk disclaimers, and remembers conversation context.
- **AI Summaries & Sentiment** - auto-generated 2-line stock summaries and a sentiment endpoint (currently simulated, pluggable to a real news API).

---

## Live Demo

- **Frontend (Vercel):** https://alpha-cross-an-ai-powered-moving-av.vercel.app
- **Backend (Render):** https://alphacross-ai-powered-moving-average.onrender.com

---

## Intelligent Data Pipeline

AlphaCross separates **market universe management** from **live market data**.

**Universe Management**
- Attempts to fetch the latest official Nifty 500 constituent list from Nifty Indices.
- Automatically falls back to `backend/data/nifty500.csv` if the online source is unavailable.
- Guarantees uninterrupted screening of all 500 constituents.

**Live Market Data**
- Uses Yahoo Finance (`yfinance`) for live OHLCV prices.
- EMA, RSI, screening, ML predictions, and backtests always operate on current market data.

This hybrid architecture provides production reliability without sacrificing live market data.

---

## Project Structure

```
AlphaCross/
├── backend/
│   ├── main.py                  # FastAPI app — all API endpoints (run from repo root)
│   ├── requirements.txt
│   ├── data/
│   │   └── nifty500.csv         # Local backup of official Nifty 500 constituents
│   ├── ml/
│   │   ├── data_fetch.py        # yfinance fetch with retry logic
│   │   ├── features.py          # EMA 20/50, RSI, slopes, returns, volatility, signal labels
│   │   ├── engine.py            # StrategyEngine — SMA/EMA/WMA, single/double/triple crossover signal generation
│   │   ├── model_xgb.py         # XGBoost training + prediction (handles binary/multi-class edge cases)
│   │   ├── backtest.py          # run_advanced_backtest — single-position engine w/ SL/TP/max-hold/priority exits
│   │   ├── nse500_fetcher.py    # Hybrid loader: online official fetch + automatic local CSV fallback
│   │   ├── stocks_list.py       # Static curated list of popular NSE stocks (used for quick lookups)
│   │   └── universe_screen.py   # Threaded EMA-based bullish/bearish/neutral screener helper
│   └── ai/
│       └── chat.py              # GPT-4-Turbo / GPT-3.5 / Gemini chat, chart explanations, summaries, sentiment
│
└── frontend/
    ├── public/
    │   └── index.html
    ├── src/
    │   ├── api/
    │   │   └── api.js           # Axios client for all backend endpoints
    │   ├── components/
    │   │   ├── ChartDisplay.jsx
    │   │   ├── Chatbot.jsx
    │   │   ├── Loader.jsx
    │   │   ├── PerformanceTable.jsx
    │   │   ├── PredictionCard.jsx
    │   │   ├── StockSelector.jsx
    │   │   ├── SummaryCard.jsx
    │   │   └── TopMovers.jsx
    │   ├── pages/
    │   │   ├── Dashboard.jsx              # Single-stock view
    │   │   ├── ScreeningResults.jsx       # NSE 500 Screener view
    │   │   └── UniverseBacktestDashboard.jsx  # Universe Backtest view
    │   ├── App.jsx
    │   ├── index.js
    │   └── index.css
    └── package.json
```

> **Note on imports:** `backend/main.py` imports its ML modules as `from backend.ml.data_fetch import ...` (i.e. as the `backend` package). This means the server must be started from the **repository root**, not from inside `backend/` - see run instructions below.

---

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 16+
- npm

### Backend Setup

1. From the **repository root** (the folder that contains `backend/`), install dependencies:
```bash
pip install -r backend/requirements.txt
```

2. (Optional) Set environment variables for the AI chatbot — either export them or put them in a `.env` file loaded by your shell/process manager:
```bash
OPENAI_API_KEY=your_openai_key      # enables GPT-4-Turbo (falls back to GPT-3.5 automatically)
GEMINI_API_KEY=your_gemini_key      # used only if OPENAI_API_KEY is not set
```
If neither key is set, the chatbot automatically falls back to rule-based responses — no API key is required to run the app.

3. Run the server **from the repository root** (important, due to the `backend.ml.*` import style):
```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`, with interactive docs at `http://localhost:8000/docs`.

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
npm install
```

2. Point the frontend at your backend (create `frontend/.env` if it doesn't exist):
```bash
REACT_APP_API_URL=http://localhost:8000
```

3. Start the dev server:
```bash
npm start
```

The app opens at `http://localhost:3000`.

---

## API Reference

All endpoints are served from `backend/main.py`.

| Endpoint | Method | Description |
|---|---|---|
| `/` | GET | Health check |
| `/ping` | GET | Simple liveness probe |
| `/data/{symbol}` | GET | Latest close, EMA 20, EMA 50, RSI for a symbol |
| `/chart/{symbol}` | GET | 6-month historical series (close, EMA 20/50, RSI, volume) for charting |
| `/predict/{symbol}` | GET | Rule-based Bullish/Bearish/Neutral signal with a confidence score derived from EMA slope |
| `/backtest/{symbol}` | GET | Single-stock EMA-crossover backtest (1-year lookback) with trade logs and summary stats |
| `/stocks` | GET | First 50 symbols from the NSE 500 list |
| `/stocks/search?q=` | GET | Search NSE 500 symbols by ticker or industry |
| `/summary/{symbol}` | GET | Plain-language trend/RSI summary for a symbol |
| `/sentiment/{symbol}` | GET | Sentiment placeholder (simulated; swap in a real news API) |
| `/top-movers` | GET | Top 5 gainers and losers from a curated liquid-stock basket (threaded, 5-day window) |
| `/chat` | POST | AI chatbot — body: `{ symbol, query, context }` |
| `/nse500/status` | GET | Metadata about the currently loaded Nifty 500 list (source, count, sample) |
| `/nse500/list` | GET | Full Nifty 500 symbol + industry list |
| `/screen/universe` | POST | Screen the NSE 500 (or a subset via `max_stocks`) into bullish/bearish/neutral buckets |
| `/backtest/universe` | POST | Portfolio-level backtest across the NSE 500 with configurable capital, position sizing, stop loss, and take profit |

### `POST /screen/universe` — request body
```json
{ "max_stocks": 500 }
```

### `POST /backtest/universe` — request body
```json
{
  "max_stocks": 50,
  "initial_capital": 100000,
  "position_size": 0.1,
  "stop_loss": 0.05,
  "take_profit": 0.15
}
```

**Response (abridged):**
```json
{
  "status": "success",
  "total_trades": 49,
  "win_rate": 28.57,
  "total_return": 2.28,
  "final_capital": 102280.45,
  "stocks_tested": 50,
  "best_trade": { "symbol": "ADANIENT", "profit_pct": 21.68 },
  "worst_trade": { "symbol": "ANANTRAJ", "profit_pct": -9.74 },
  "top_sectors": [
    { "sector": "Consumer Durables", "avg_return": 20.66, "trades": 3 }
  ],
  "trade_details": [ { "symbol": "ADANIENT", "entry_date": "2026-04-20", "exit_date": "2026-05-14", "profit_pct": 21.68 } ]
}
```

### `POST /chat` — request body
```json
{
  "symbol": "INFY",
  "query": "Why is INFY predicted bullish?",
  "context": {
    "prediction": "BULLISH",
    "confidence": 0.85,
    "ema20": 1445.20,
    "ema50": 1430.80,
    "rsi": 62.4
  }
}
```

---

## AI Chatbot

Located in `backend/ai/chat.py`. Provider priority:

1. **OpenAI GPT-4-Turbo** (falls back to `gpt-4-1106-preview`, then GPT-3.5, on error) — remembers conversation history, gives context-aware answers, and includes risk disclaimers for buy/sell questions.
2. **Google Gemini** (`gemini-pro`) used if no OpenAI key is present.
3. **Rule-based fallback** — pattern-matches greetings, "why", "what is", "should I buy/sell", and prediction questions using live EMA/RSI context. Requires no API key.

Also included: `explain_chart()` for natural-language chart trend summaries and `generate_stock_summary()` for 2-line daily summaries, both with the same GPT → fallback pattern.

---

## Signal & Model Details

### Screening / Prediction Signal
- **Bullish**: EMA 20 > EMA 50
- **Bearish**: EMA 20 < EMA 50
- **Neutral**: EMAs equal (rare)

`/predict/{symbol}` additionally checks the EMA 20 slope direction to assign a confidence score (capped at 0.85).

### Backtest Strategy (single-stock and universe)
- **Entry**: EMA 20 crosses above EMA 50
- **Exit**: EMA 20 crosses below EMA 50, OR stop loss / take profit hit (universe backtest only)
- Universe backtest simulates fixed **position sizing** (% of capital per trade) rather than full capital per trade.

### Features Used (`ml/features.py`)
- `EMA_20`, `EMA_50`
- `EMA_20_slope`, `EMA_50_slope` (3-day rate of change)
- `RSI` (14-period)
- `Returns` (daily % change)
- `Volatility` (10-day rolling std dev)

### ML Model (`ml/model_xgb.py`)
- **Algorithm**: XGBoost Classifier (50 estimators, max_depth=3, learning_rate=0.1)
- Automatically detects class imbalance/insufficient diversity in training labels and falls back to using the current `Signal` column, or a simple EMA-comparison rule, to avoid training failures on short histories.
- Handles both 2-class and 3-class (Bullish/Neutral/Bearish) scenarios with correct label remapping.

### Data Sources

**Live Market Data**
- Yahoo Finance (`yfinance`)
- Automatic retry logic (3 attempts) on transient failures or missing OHLCV columns, with `.NS` suffix auto-appended
- Live OHLCV prices power indicators, screening, predictions, and backtesting

**NSE 500 Constituents**
- Primary source: Official Nifty Indices CSV (fetched live from `niftyindices.com`)
- Cached in memory (`ml/nse500_fetcher.py`)
- Automatic fallback to `backend/data/nifty500.csv` if the online source is unavailable
- Emergency 4-stock fallback only if both online and local sources fail

---

## Frontend Views

| View | File | Description |
|---|---|---|
| Single Stock | `pages/Dashboard.jsx` | Stock selector, prediction card, chart, performance table, AI summary, chatbot |
| NSE 500 Screener | `pages/ScreeningResults.jsx` | Full-universe bullish/bearish/neutral scan with sector tags, filters, and search |
| Universe Backtest | `pages/UniverseBacktestDashboard.jsx` | Configurable portfolio backtest across the NSE 500 with sector and trade-level breakdowns |

Shared components live in `frontend/src/components/`: `ChartDisplay`, `Chatbot`, `Loader`, `PerformanceTable`, `PredictionCard`, `StockSelector`, `SummaryCard`, `TopMovers`.

All API calls are centralized in `frontend/src/api/api.js`.

---

## Deployment

### Backend (Render / Railway / HuggingFace Spaces)
- **Build command**: `pip install -r backend/requirements.txt`
- **Start command** (must run from repo root so `backend.*` imports resolve):
```bash
uvicorn backend.main:app --host 0.0.0.0 --port $PORT
```
- Set `OPENAI_API_KEY` and/or `GEMINI_API_KEY` as environment variables if you want the AI chatbot beyond rule-based fallback.

#### Production Reliability

The backend first attempts to download the latest official Nifty 500 constituent list. If that fails, it transparently loads the bundled `backend/data/nifty500.csv`, ensuring Render deployments continue to screen the full NSE 500 universe. Live market prices are still fetched in real time from Yahoo Finance.

### Frontend (Vercel / Netlify)
- **Build command**: `npm install && npm run build`
- Set `REACT_APP_API_URL` to your deployed backend URL.

---

## Tech Stack

**Backend:** FastAPI, XGBoost, scikit-learn, pandas, numpy, yfinance, `ta`, OpenAI SDK, `google-generativeai`, `requests`, `python-dotenv`

**Frontend:** React 18, React Router, TailwindCSS, Chart.js / react-chartjs-2, Axios, lucide-react

---

## Disclaimer

This tool is for educational and research purposes only. It does not constitute financial advice. Always do your own research before making trading decisions.

---

## License

MIT License — free to use and modify.
