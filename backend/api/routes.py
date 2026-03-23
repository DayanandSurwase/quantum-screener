from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.models.schemas import AnalysisResponse, ChatRequest
from backend.services.finance_service import get_stock_data, get_historical_data, get_market_news
from backend.agents.chat_agent import answer_stock_question
from backend.agents.bull_agent import generate_bull_case
from backend.agents.bear_agent import generate_bear_case
from backend.agents.judge_agent import generate_verdict
from backend.agents.learn_agent import generate_flashcards

router = APIRouter()

class LearnRequest(BaseModel):
    topic: str

@router.get("/analyze/{stock}", response_model=AnalysisResponse)
async def analyze_stock(stock: str):
    ticker = stock.upper()

    try:
        stock_data = get_stock_data(ticker)
        chart_data = get_historical_data(ticker)
        
        bull_case = generate_bull_case(stock_data)
        bear_case = generate_bear_case(stock_data)
        decision = generate_verdict(ticker, bull_case, bear_case)
        
        response_data = AnalysisResponse(
            stock_data=stock_data,
            chart_data=chart_data,
            bull_case=bull_case,
            bear_case=bear_case,
            decision=decision
        )

        return response_data

    except Exception as e:
        if "rate limit" in str(e).lower() or "429" in str(e):
            raise HTTPException(status_code=429, detail="The AI is currently analyzing too many requests. Please take a quick breather and try again in 1 minute.")
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post("/chat")
async def chat_with_ai(request: ChatRequest):
    try:
        answer = answer_stock_question(request.ticker, request.message)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get("/market-news")
async def market_news():
    try:
        data = get_market_news()
        return data
    except Exception as e:
        print("ERROR:", e)
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post("/learn")
async def learn_topic(request: LearnRequest):
    try:
        cards = generate_flashcards(request.topic)
        return {"flashcards": cards}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))