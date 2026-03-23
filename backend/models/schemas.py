from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class StockData(BaseModel):
    ticker: str
    price: Optional[float] = None
    market_cap: Optional[float] = None
    revenue: Optional[float] = None
    pe_ratio: Optional[float] = None
    company_name: Optional[str] = "Unknown"
    currency: Optional[str] = "INR"


class AnalysisResponse(BaseModel):
    stock_data: StockData
    chart_data: List[Dict[str, Any]]
    bull_case: str
    bear_case: str
    decision: str


class ChatRequest(BaseModel):
    ticker: str
    message: str