import yfinance as yf
from curl_cffi import requests
import random
from backend.models.schemas import StockData


session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
})

def get_exchange_rate(from_currency: str, to_currency: str = "INR") -> float:
    if from_currency == to_currency:
        return 1.0
    try:
        ticker = yf.Ticker(f"{from_currency}{to_currency}=X", session=session)
        return float(ticker.fast_info.last_price)
    except:
        return 83.0

def get_stock_data(ticker: str) -> StockData:
    stock = yf.Ticker(ticker, session=session)
    try:
        f_info = stock.fast_info
        hist = stock.history(period="5d")
        
        if hist.empty:
            raise ValueError(f"Yahoo Finance rejected the live data request for {ticker}.")
            
        raw_price = float(hist["Close"].iloc[-1])
        raw_mcap = f_info.market_cap
        native_currency = f_info.currency.upper() if hasattr(f_info, 'currency') else "INR"
        
        pe_ratio = None
        revenue = None
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
    except Exception as e:
        raise ValueError(f"Failed to fetch live data for {ticker}. Details: {str(e)}")
    
    
def get_historical_data(ticker: str):
    stock = yf.Ticker(ticker, session=session)
    
    native_currency = stock.info.get("currency", "INR").upper()
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
    """Fetches live daily changes individually to avoid bulk-download blocks."""
    watchlist = ["RELIANCE.NS", "HDFCBANK.NS", "TCS.NS", "NVDA", "AAPL"]
    trending = []
    
    for t in watchlist:
        try:
            stock = yf.Ticker(t, session=session)
            hist = stock.history(period="5d")
            if len(hist) >= 2:
                prev_close = float(hist["Close"].iloc[-2])
                current = float(hist["Close"].iloc[-1])
                pct_change = ((current - prev_close) / prev_close) * 100
                
                trending.append({
                    "ticker": t.replace(".NS", ""),
                    "change": round(pct_change, 2)
                })
        except:
            continue
            
    trending = sorted(trending, key=lambda x: abs(x["change"]), reverse=True)[:3]

    return {
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