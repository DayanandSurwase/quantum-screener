import yfinance as yf
from curl_cffi import requests
from backend.models.schemas import StockData

session = requests.Session(impersonate="chrome110")

def get_exchange_rate(from_currency: str, to_currency: str = "INR") -> float:
    if from_currency == to_currency:
        return 1.0
    try:
        ticker = f"{from_currency}{to_currency}=X"
        rate_info = yf.Ticker(ticker, session=session).info
        return rate_info.get("regularMarketPrice", rate_info.get("currentPrice", 83.0))
    except:
        return 83.0 

def get_stock_data(ticker: str) -> StockData:
    stock = yf.Ticker(ticker, session=session)
    try:
        info = stock.info
    except Exception as e:
        raise ValueError(f"Failed to fetch data for {ticker}. Details: {str(e)}")
    
    native_currency = info.get("currency", "INR").upper()
    exchange_rate = get_exchange_rate(native_currency, "INR")

    raw_price = info.get("currentPrice", info.get("regularMarketPrice"))
    raw_mcap = info.get("marketCap")
    raw_rev = info.get("totalRevenue")

    price = raw_price * exchange_rate if raw_price else None
    market_cap = raw_mcap * exchange_rate if raw_mcap else None
    revenue = raw_rev * exchange_rate if raw_rev else None

    return StockData(
        ticker=ticker.upper(),
        company_name=info.get("shortName", ticker),
        price=price,
        market_cap=market_cap,
        revenue=revenue,
        pe_ratio=info.get("trailingPE", info.get("forwardPE")),
        currency="INR" 
    )

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
    """Fetches live daily changes for top stocks to populate the Market Panel."""
    watchlist = ["NVDA", "TTE.PA", "RELIANCE.NS"]
    
    trending = []
    try:
        data = yf.download(watchlist, period="2d", group_by="ticker", progress=False, session=session)
        
        for ticker in watchlist:
            if ticker in data:
                closes = data[ticker]['Close'].dropna().values
                if len(closes) >= 2:
                    prev_close = closes[-2]
                    current = closes[-1]
                    pct_change = ((current - prev_close) / prev_close) * 100
                    
                    display_ticker = ticker.split(".")[0]
                    
                    trending.append({
                        "ticker": display_ticker,
                        "change": round(pct_change, 2)
                    })
        
        trending = sorted(trending, key=lambda x: abs(x["change"]), reverse=True)[:3]
    except Exception as e:
        trending = [{"ticker": "NIFTY50", "change": 0.0}]

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