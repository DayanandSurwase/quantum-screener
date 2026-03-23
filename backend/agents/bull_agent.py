from backend.services.groq_service import generate_ai_response
from backend.models.schemas import StockData

def generate_bull_case(stock_data: StockData) -> str:
    system_prompt = (
        "You are an optimistic Wall Street Bull Analyst. "
        "Your job is to look at the financial data provided and argue passionately "
        "why this stock is a fantastic investment. Focus on growth potential, market dominance, and positive metrics."
        "Dont write to much thesis yess but write that needed to be write but not so much max 2 paragraphs."
    )
    user_prompt = (
        f"Analyze {stock_data.company_name} ({stock_data.ticker}).\n"
        f"Price: ${stock_data.price}\n"
        f"Market Cap: ${stock_data.market_cap}\n"
        f"Revenue: ${stock_data.revenue}\n"
        f"P/E Ratio: {stock_data.pe_ratio}\n"
        "Provide a concise, 2-3 paragraph bull case."
    )
    return generate_ai_response(system_prompt, user_prompt)