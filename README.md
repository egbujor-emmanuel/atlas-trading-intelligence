# 🏛️ ATLAS — AI-Powered Trading Intelligence

[![Bitget Hackathon](https://img.shields.io/badge/Bitget-Builder%20Base%20Camp-f7b731)](https://bitget.com)
[![Track 2](https://img.shields.io/badge/Track-Trading%20Infrastructure-blue)](https://bitget-ai.gitbook.io/hackathon)

## 📊 Overview

ATLAS is a real-time cryptocurrency market intelligence platform that helps AI trading agents and human traders make smarter decisions by tracking whale movements, market sentiment, and live prices.

### Key Features

- 🐋 **Whale Tracking** — Monitor large holders and their transactions
- 📊 **Market Sentiment** — Fear & Greed index, funding rates, long/short ratios
- 💰 **Live Prices** — Real-time prices for 10+ cryptocurrencies
- 📡 **AI Signals** — Actionable trading recommendations
- 🔔 **Real-time Alerts** — Notifications for high-value whale movements
- 🔌 **Agent API** — REST endpoints for AI agents

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js (for Bitget Agent Hub)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/attrito/atlas.git
cd atlas

# 2. Install backend dependencies
cd backend
pip install fastapi uvicorn pydantic python-dotenv requests

# 3. (Optional) Connect to Bitget API
# Create .env file with your Bitget API keys
echo "BITGET_API_KEY=your_key" > .env
echo "BITGET_SECRET_KEY=your_secret" >> .env
echo "BITGET_PASSPHRASE=your_passphrase" >> .env

# 4. Start the backend
python app.py

# 5. Open the frontend
# Double-click frontend/index.html or use Live Server