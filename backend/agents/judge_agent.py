from backend.services.groq_service import generate_ai_response

def generate_verdict(ticker: str, bull_case: str, bear_case: str) -> str:
    system_prompt = (
        "You are the Chief Investment Officer (Judge Agent). "
        "You must review the Bull case and the Bear case for a stock, weigh their arguments, "
        "and provide a final, decisive verdict: BUY, HOLD, or SELL. "
        "Start your response strictly with the word BUY, HOLD, or SELL, followed by a brief 2-sentence justification."
        "Dont use dollar signs this totally indian format so if you need to write some figures use indian rupee"
    )

    
    user_prompt = (
        f"Stock: {ticker}\n\n"
        f"--- BULL CASE ---\n{bull_case}\n\n"
        f"--- BEAR CASE ---\n{bear_case}\n\n"
        "What is your final decision and why?"
    )
    return generate_ai_response(system_prompt, user_prompt)