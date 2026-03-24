import yfinance as yf
import time
from datetime import datetime, timedelta
from backend.models.schemas import StockData

market_intel_cache = {"data": None, "last_updated": datetime.min}

def get_exchange_rate(from_currency: str, to_currency: str = "INR") -> float:
    if from_currency == to_currency:
        return 1.0
    try:
        ticker = yf.Ticker(f"{from_currency}{to_currency}=X")
        return float(ticker.fast_info.last_price)
    except:
        return 83.0

def get_stock_data(ticker: str) -> StockData:
    stock = yf.Ticker(ticker)
    
    try:
        hist = stock.history(period="5d")
        if hist.empty:
            raise ValueError(f"Yahoo Finance rejected the live data request for {ticker}.")
        raw_price = float(hist["Close"].iloc[-1])
    except Exception as e:
        raise ValueError(f"Failed to fetch live price for {ticker}. Details: {str(e)}")

    raw_mcap = None
    native_currency = "INR"
    pe_ratio = None
    revenue = None

    try:
        f_info = stock.fast_info
        raw_mcap = getattr(f_info, 'market_cap', None)
        native_currency = getattr(f_info, 'currency', "INR").upper()
    except:
        pass
        
    try:
        info = stock.info
        pe_ratio = info.get("trailingPE", info.get("forwardPE"))
        revenue = info.get("totalRevenue")
    except:
        pass

    exchange_rate = get_exchange_rate(native_currency, "INR")

    return StockData(
        ticker=ticker.upper(),
        company_name=ticker.upper(), 
        price=raw_price * exchange_rate if raw_price else None,
        market_cap=raw_mcap * exchange_rate if raw_mcap else None,
        revenue=revenue * exchange_rate if revenue else None,
        pe_ratio=pe_ratio,
        currency="INR" 
    )

def get_historical_data(ticker: str):
    stock = yf.Ticker(ticker)
    
    native_currency = "INR"
    try:
        native_currency = getattr(stock.fast_info, 'currency', "INR").upper()
    except:
        pass
        
    exchange_rate = get_exchange_rate(native_currency, "INR")

    hist = stock.history(period="3mo")
    hist_40 = hist.tail(40)
    
    chart_data = []
    for date, row in hist_40.iterrows():
        converted_price = row["Close"] * exchange_rate
        chart_data.append({
            "date": date.strftime("%b %d"), 
            "price": round(converted_price, 2)
        })
        
    return chart_data

def get_market_news():
    global market_intel_cache
    
    if datetime.now() - market_intel_cache["last_updated"] < timedelta(minutes=5):
        if market_intel_cache["data"] is not None:
            return market_intel_cache["data"]

    watchlist = ["RELIANCE.NS", "HDFCBANK.NS", "TCS.NS", "NVDA", "AAPL"]
    trending = []
    
    for t in watchlist:
        try:
            stock = yf.Ticker(t)
            hist = stock.history(period="5d")
            if len(hist) >= 2:
                prev_close = float(hist["Close"].iloc[-2])
                current = float(hist["Close"].iloc[-1])
                pct_change = ((current - prev_close) / prev_close) * 100
                
                trending.append({
                    "ticker": t.replace(".NS", ""),
                    "change": round(pct_change, 2)
                })
            time.sleep(1.5)
        except:
            continue
            
    trending = sorted(trending, key=lambda x: abs(x["change"]), reverse=True)[:3]

    result = {
        "trending": trending,
        "scans": [
            "Undervalued Tech (P/E < 20)",
            "High Momentum Breakouts",
            "NIFTY 50 Volume Spikes"
        ],
        "alerts": [
            {"type": "Live", "text": "Global market sentiment tracking active."},
            {"type": "Macro", "text": "AI Multi-Agent system fully operational."}
        ]
    }
    
    if trending:
        market_intel_cache["data"] = result
        market_intel_cache["last_updated"] = datetime.now()

    return result