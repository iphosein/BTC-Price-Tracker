from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx
import time

app = FastAPI(title="BTC Price API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

PRICE_URL = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd&include_24hr_change=true"

DETAIL_URL = "https://api.coingecko.com/api/v3/coins/bitcoin?localization=false&tickers=false&market_data=true&community_data=false&developer_data=false&sparkline=false"

cache = {}
last_price_fetch = 0
last_detail_fetch = 0

async def get_btc_data():
    global cache, last_price_fetch, last_detail_fetch
    now = time.time()

    if not cache or now - last_price_fetch > 1.5:
        async with httpx.AsyncClient(timeout=6.0) as client:
            try:
                r = await client.get(PRICE_URL)
                r.raise_for_status()
                data = r.json()["bitcoin"]

                cache["price"] = float(data["usd"])
                cache["change_24h"] = round(float(data["usd_24h_change"]), 2)
                last_price_fetch = now
            except:
                pass

    if "high_24h" not in cache or now - last_detail_fetch > 30:
        async with httpx.AsyncClient(timeout=8.0) as client:
            try:
                r = await client.get(DETAIL_URL)
                r.raise_for_status()
                market = r.json()["market_data"]
                cache["high_24h"] = float(market["high_24h"]["usd"])
                cache["low_24h"] = float(market["low_24h"]["usd"])
                last_detail_fetch = now
            except:
                pass

    if not cache:
        raise HTTPException(503, "CoinGecko unavailable")

    cache["updated_at"] = int(now)
    return cache


@app.get("/bitcoin-price")
async def bitcoin_price():
    return await get_btc_data()