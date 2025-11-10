#AlphaCross — AI-Driven MA Crossover Analyzer

AlphaCross is a full-stack trading signal analyzer that uses machine learning (XGBoost) and AI insights to detect and backtest moving average crossovers on NSE 500 stocks.

Key Features
Real-Time Data: Fetches 3-month EOD prices (3:30 PM) for NSE 500 via yfinance
ML Predictions: XGBoost predicts bullish/bearish crossovers (3-day horizon)
Backtesting: Detailed trade logs, profit metrics, and performance summary
AI Chatbot: GPT/Gemini-powered Q&A for strategy and market insights
Interactive Dashboard: ReactJS + Tailwind dark-mode interface with charts

Architecture
alphacross/
├── backend/     # FastAPI + ML + Chatbot
│   ├── ml/      # data_fetch.py | features.py | model_xgb.py | backtest.py
│   └── ai/      # chat.py (GenAI integration)
└── frontend/    # ReactJS Dashboard
    ├── src/components | pages | api
    └── public/

Quick Start

Backend

cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload


Frontend

cd frontend
npm install
npm start


Backend: http://localhost:8000

Frontend: http://localhost:3000

Core Endpoints
Endpoint	Description
/data/{symbol}	Fetch EMA/RSI & price data
/predict/{symbol}	ML prediction (Bullish/Bearish + confidence)
/backtest/{symbol}	Run MA crossover backtest
/chat	AI chatbot for trading explanations

Model & Strategy

Features: EMA 20/50, RSI 14, slopes, returns, volatility
Model: XGBoost (50 trees, depth 3, lr 0.1)
Labeling: +1 = Bullish, −1 = Bearish
Backtest Metrics: Win %, Profit %, Max DD %, Risk-Reward, Profit Factor

Tech Stack

Backend: FastAPI · XGBoost · Pandas · yfinance · TA-Lib · OpenAI/Gemini
Frontend: React 18 · TailwindCSS · Chart.js · Axios · Lucide
