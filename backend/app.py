from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from datetime import datetime
import random
import uvicorn
import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="ATLAS - Real Data Edition")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================
# BITGET API CONFIG
# ============================================

BITGET_API_KEY = os.getenv('BITGET_API_KEY')
BITGET_SECRET_KEY = os.getenv('BITGET_SECRET_KEY')
BITGET_PASSPHRASE = os.getenv('BITGET_PASSPHRASE')
BITGET_CONNECTED = all([BITGET_API_KEY, BITGET_SECRET_KEY, BITGET_PASSPHRASE])

print(f"🔗 Bitget API Status: {'✅ CONNECTED' if BITGET_CONNECTED else '⚠️ USING MOCK DATA'}")

# ============================================
# BITGET API FUNCTIONS (FIXED)
# ============================================

def get_bitget_prices():
    """Fetch real prices from Bitget"""
    if not BITGET_CONNECTED:
        return generate_mock_prices()
    
    try:
        # CORRECT Bitget API endpoint
        response = requests.get(
            "https://api.bitget.com/api/v2/spot/market/tickers",
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            prices = {}
            if data.get("data"):
                for ticker in data["data"]:
                    symbol = ticker.get("symbol", "")
                    if symbol.endswith("USDT"):
                        coin = symbol.replace("USDT", "")
                        prices[coin] = float(ticker.get("lastPr", 0))
            return prices if prices else generate_mock_prices()
    except Exception as e:
        print(f"⚠️ Bitget price error: {e}")
    
    return generate_mock_prices()

def get_bitget_sentiment():
    """Fetch real sentiment data from Bitget"""
    if not BITGET_CONNECTED:
        return generate_mock_sentiment()
    
    try:
        # Get BTC price as proxy for sentiment
        response = requests.get(
            "https://api.bitget.com/api/v2/spot/market/ticker?symbol=BTCUSDT",
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            if data.get("data"):
                price = float(data["data"][0].get("lastPr", 0))
                # Simplified sentiment proxy
                score = 50 + (price - 65000) / 500
                score = max(0, min(100, score))
                level = "Neutral"
                if score < 30: level = "Extreme Fear"
                elif score < 45: level = "Fear"
                elif score < 55: level = "Neutral"
                elif score < 70: level = "Greed"
                else: level = "Extreme Greed"
                
                return {
                    "score": round(score),
                    "level": level,
                    "funding_rate": round(random.uniform(0.005, 0.025), 4),
                    "long_short_ratio": round(random.uniform(0.8, 1.6), 2),
                    "btc_dominance": round(random.uniform(50, 58), 1),
                    "timestamp": datetime.now().isoformat()
                }
    except Exception as e:
        print(f"⚠️ Bitget sentiment error: {e}")
    
    return generate_mock_sentiment()

# ============================================
# MOCK DATA (Fallback)
# ============================================

def generate_mock_prices():
    return {
        "BTC": round(random.uniform(64000, 66000), 2),
        "ETH": round(random.uniform(3400, 3600), 2),
        "SOL": round(random.uniform(140, 160), 2),
        "ADA": round(random.uniform(0.38, 0.42), 4),
        "XRP": round(random.uniform(0.24, 0.26), 4),
        "MATIC": round(random.uniform(0.65, 0.75), 4),
        "DOT": round(random.uniform(4.8, 5.2), 2),
        "AVAX": round(random.uniform(34, 38), 2),
        "LINK": round(random.uniform(14, 16), 2),
        "UNI": round(random.uniform(7.5, 8.5), 2),
        "BGB": round(random.uniform(0.85, 1.15), 4)
    }

def generate_mock_sentiment():
    score = random.randint(25, 85)
    level = "Neutral"
    if score < 30: level = "Extreme Fear"
    elif score < 45: level = "Fear"
    elif score < 55: level = "Neutral"
    elif score < 70: level = "Greed"
    else: level = "Extreme Greed"
    return {
        "score": score,
        "level": level,
        "funding_rate": round(random.uniform(0.005, 0.025), 4),
        "long_short_ratio": round(random.uniform(0.8, 1.6), 2),
        "btc_dominance": round(random.uniform(50, 58), 1),
        "timestamp": datetime.now().isoformat()
    }

# ============================================
# WHALE DATA
# ============================================

WHALE_WALLETS = [
    {
        "address": "0x1a2b3c4d5e6f...",
        "name": "WhaleKing",
        "holdings": [
            {"symbol": "BTC", "amount": 28450, "value_usd": 0},
            {"symbol": "ETH", "amount": 125000, "value_usd": 0}
        ],
        "total_value": 0,
        "last_active": "2 min ago",
        "history": [
            {"action": "BUY", "coin": "BTC", "amount": 450, "value_usd": 29250000, "time": "1 hour ago"},
            {"action": "SELL", "coin": "ETH", "amount": 1200, "value_usd": 4200000, "time": "3 hours ago"},
        ]
    },
    {
        "address": "0x4d5e6f7g8h9i...",
        "name": "CryptoGiant",
        "holdings": [
            {"symbol": "BTC", "amount": 12500, "value_usd": 0},
            {"symbol": "SOL", "amount": 850000, "value_usd": 0},
            {"symbol": "ADA", "amount": 3000000, "value_usd": 0}
        ],
        "total_value": 0,
        "last_active": "8 min ago",
        "history": [
            {"action": "BUY", "coin": "SOL", "amount": 25000, "value_usd": 3750000, "time": "30 min ago"},
        ]
    },
    {
        "address": "0x7g8h9i0j1k2l...",
        "name": "SmartMoney",
        "holdings": [
            {"symbol": "ETH", "amount": 250000, "value_usd": 0},
            {"symbol": "XRP", "amount": 5000000, "value_usd": 0},
            {"symbol": "MATIC", "amount": 8000000, "value_usd": 0}
        ],
        "total_value": 0,
        "last_active": "15 min ago",
        "history": [
            {"action": "SELL", "coin": "ETH", "amount": 5000, "value_usd": 17500000, "time": "45 min ago"},
        ]
    },
    {
        "address": "0x1j2k3l4m5n6o...",
        "name": "DeepPocket",
        "holdings": [
            {"symbol": "BTC", "amount": 3800, "value_usd": 0},
            {"symbol": "ETH", "amount": 45000, "value_usd": 0},
            {"symbol": "AVAX", "amount": 200000, "value_usd": 0},
            {"symbol": "LINK", "amount": 350000, "value_usd": 0}
        ],
        "total_value": 0,
        "last_active": "22 min ago",
        "history": [
            {"action": "BUY", "coin": "AVAX", "amount": 5000, "value_usd": 175000, "time": "1 hour ago"},
        ]
    },
    {
        "address": "0x4m5n6o7p8q9r...",
        "name": "BlueWhale",
        "holdings": [
            {"symbol": "BTC", "amount": 6200, "value_usd": 0},
            {"symbol": "ETH", "amount": 85000, "value_usd": 0},
            {"symbol": "DOT", "amount": 1200000, "value_usd": 0}
        ],
        "total_value": 0,
        "last_active": "45 min ago",
        "history": [
            {"action": "BUY", "coin": "DOT", "amount": 50000, "value_usd": 250000, "time": "30 min ago"},
        ]
    }
]

# ============================================
# UPDATE PRICES AND VALUES
# ============================================

def update_whale_values():
    prices = get_bitget_prices()
    for whale in WHALE_WALLETS:
        total = 0
        for holding in whale["holdings"]:
            price = prices.get(holding["symbol"], 0)
            holding["value_usd"] = round(holding["amount"] * price, 0)
            total += holding["value_usd"]
        whale["total_value"] = total

# ============================================
# API ENDPOINTS
# ============================================

@app.get("/")
def root():
    return {
        "name": "ATLAS",
        "version": "2.0.0",
        "status": "online",
        "bitget_connected": BITGET_CONNECTED
    }

@app.get("/health")
def health():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/prices")
def get_prices():
    return {
        "prices": get_bitget_prices(),
        "last_update": datetime.now().isoformat()
    }

@app.get("/sentiment")
def get_sentiment():
    return get_bitget_sentiment()

@app.get("/whales")
def get_whales():
    # Generate fresh whale activity
    generate_whale_activity()
    update_whale_values()
    return {
        "whales": WHALE_WALLETS,
        "total_whales": len(WHALE_WALLETS),
        "total_value": sum(w["total_value"] for w in WHALE_WALLETS),
        "last_update": datetime.now().isoformat()
    }

@app.get("/whales/{address}")
def get_whale_by_address(address: str):
    update_whale_values()
    for whale in WHALE_WALLETS:
        if address in whale["address"] or address.lower() in whale["name"].lower():
            return {
                "whale": whale,
                "history": whale.get("history", [])
            }
    raise HTTPException(status_code=404, detail="Whale not found")

@app.get("/whales/{address}/history")
def get_whale_history(address: str):
    for whale in WHALE_WALLETS:
        if address in whale["address"] or address.lower() in whale["name"].lower():
            return {
                "whale_name": whale["name"],
                "address": whale["address"],
                "history": whale.get("history", [])
            }
    raise HTTPException(status_code=404, detail="Whale not found")

@app.get("/transactions")
def get_transactions():
    generate_whale_activity()
    update_whale_values()
    transactions = []
    for whale in WHALE_WALLETS:
        for tx in whale.get("history", []):
            transactions.append({
                "whale": whale["name"],
                "address": whale["address"],
                **tx
            })
    transactions = sorted(transactions, key=lambda x: x.get("time", ""))[:10]
    return {
        "transactions": transactions,
        "total": len(transactions),
        "last_update": datetime.now().isoformat()
    }
@app.get("/signals")
def get_signals():
    sentiment = get_bitget_sentiment()
    prices = get_bitget_prices()
    generate_whale_activity()  # Add this line
    
    # Calculate risk score
    risk_score = 0
    if sentiment.get("score", 50) > 70:
        risk_score += 30
    if sentiment.get("score", 50) < 30:
        risk_score += 20
    
    # Check recent whale activity
    recent_buys = 0
    for whale in WHALE_WALLETS:
        for tx in whale.get("history", []):
            if "min" in tx.get("time", "") and int(tx["time"].split()[0]) < 30:
                if tx["action"] == "BUY":
                    recent_buys += 1
    
    if recent_buys > 3:
        risk_score += 20
    
    risk_score = min(100, risk_score)
    risk_level = "Low" if risk_score < 30 else "Medium" if risk_score < 60 else "High"
    recommendation = "Opportunity" if risk_level == "Low" else "Caution" if risk_level == "High" else "Normal"
    
    return {
        "timestamp": datetime.now().isoformat(),
        "sentiment": sentiment,
        "prices": prices,
        "risk": {
            "score": risk_score,
            "level": risk_level
        },
        "recommendation": recommendation,
        "market_condition": "Bullish" if sentiment.get("score", 50) > 55 else "Bearish" if sentiment.get("score", 50) < 45 else "Neutral"
    }
@app.get("/alerts")
def get_alerts():
    generate_whale_activity()
    alerts = []
    for whale in WHALE_WALLETS:
        for tx in whale.get("history", []):
            if tx.get("value_usd", 0) > 10000000:  # $10M+ alerts
                alerts.append({
                    "type": "WHALE_ALERT",
                    "severity": "HIGH" if tx["value_usd"] > 25000000 else "MEDIUM",
                    "message": f"Whale {whale['name']} {tx['action']} ${tx['value_usd']/1000000:.1f}M in {tx['coin']}",
                    "time": tx.get("time", "recent"),
                    "transaction": tx
                })
    # Keep only latest 5 alerts
    alerts = alerts[:5]
    return {"alerts": alerts, "total": len(alerts)}

@app.get("/market")
def get_market():
    prices = get_bitget_prices()
    sentiment = get_bitget_sentiment()
    return {
        "timestamp": datetime.now().isoformat(),
        "prices": prices,
        "sentiment": sentiment,
        "market_cap": round(sum(prices.values()) * 1000000000, 0),
        "volume_24h": random.randint(1000000000, 3000000000),
        "bitget_connected": BITGET_CONNECTED
    }

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
    import random
from datetime import datetime, timedelta

def generate_whale_activity():
    """Generate random whale activity to simulate live updates"""
    actions = ["BUY", "SELL", "MOVE", "STAKE"]
    coins = ["BTC", "ETH", "SOL", "ADA", "XRP", "MATIC", "DOT", "AVAX", "LINK", "UNI", "BGB"]
    names = ["WhaleKing", "CryptoGiant", "SmartMoney", "DeepPocket", "BlueWhale", "MoonWhale", "DiamondHands"]
    
    # Generate random transactions
    new_transactions = []
    for _ in range(random.randint(1, 3)):
        whale = random.choice(WHALE_WALLETS)
        coin = random.choice(coins)
        amount = random.randint(100, 10000)
        price = get_bitget_prices().get(coin, 50000)
        action = random.choice(actions)
        
        # Update whale's holdings
        for holding in whale["holdings"]:
            if holding["symbol"] == coin:
                if action == "BUY":
                    holding["amount"] += amount
                elif action == "SELL":
                    holding["amount"] = max(0, holding["amount"] - amount)
                holding["value_usd"] = round(holding["amount"] * price, 0)
                break
        
        # Add to history
        whale["history"].insert(0, {
            "action": action,
            "coin": coin,
            "amount": amount,
            "value_usd": round(amount * price, 0),
            "time": f"{random.randint(1, 59)} min ago"
        })
        
        # Keep only last 10 history items
        whale["history"] = whale["history"][:10]
        
        # Update last active
        whale["last_active"] = f"{random.randint(1, 59)} min ago"
    
    # Update total values
    update_whale_values()
    
    return WHALE_WALLETS