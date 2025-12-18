# ₿ Bitcoin Price Tracker (Desktop + API)

A real-time **Bitcoin price tracking system** consisting of a **FastAPI backend** and a **modern PyQt5 desktop application**.  
The project fetches live BTC data from **CoinGecko**, applies intelligent caching, and displays prices, trends, and alerts in a clean, responsive GUI.

---

## ✨ Features

### 🖥️ Desktop Application (PyQt5)
- Live BTC / USDT price display
- Color-coded price movement (green ↑ / red ↓)
- 24h percentage change indicator
- 24h High & Low visualization
- Real-time interactive price chart (PyQtGraph)
- Time-based X-axis with human-readable clock
- Price alert system with popup notifications
- Automatic timezone display (UTC offset)
- Graceful handling of connection failures

---

### ⚙️ Backend API (FastAPI)
- Fetches live Bitcoin data from CoinGecko
- Separate endpoints for price and market details
- Smart in-memory caching:
  - Price & change refreshed every ~1.5s
  - High/Low refreshed every 30s
- Async HTTP requests using `httpx`
- CORS enabled for desktop access
- Lightweight & fast response time

---

## 🧠 Architecture Overview
bitcoin-tracker/
│
├── backend/
│ ├── main.py # FastAPI application
│ └── requirements.txt
│
├── desktop/
│ ├── btc_tracker.py # PyQt5 application
│ └── requirements.txt
│
└── README.md



Desktop app communicates with the backend API:
PyQt5 GUI → FastAPI → CoinGecko API




---

## 🖼️ Screenshot

![Bitcoin Price Tracker Screenshot](https://github.com/iphosein/BTC-Price-Tracker/blob/0ae9d35394bf73189fd0a70f5a7c8f79121164ea/BTC-Price.JPG)

> Shows live BTC price, 24h stats, interactive chart, and alert input.

---

## 🚀 Getting Started

### 1️⃣ Backend Setup (FastAPI)

```bash
pip install fastapi uvicorn httpx
uvicorn main:app --host 127.0.0.1 --port 8080
http://127.0.0.1:8080/bitcoin-price

pip install pyqt5 pyqtgraph requests pytz
python btc_tracker.py


🛠️ Tech Stack
Backend

FastAPI

httpx (async HTTP client)

CoinGecko API

Frontend

PyQt5

PyQtGraph

Requests

pytz

