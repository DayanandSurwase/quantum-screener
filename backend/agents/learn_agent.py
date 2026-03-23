import json
from backend.services.groq_service import generate_ai_response

def generate_flashcards(topic: str) -> list:
    """Generates 20 beginner-friendly financial flashcards."""
    
    system_prompt = (
        "You are Quantum Academy, a world-class financial educator. "
        "The user will give you a topic related to finance, investing, or the stock market. "
        "Generate exactly 20 educational flashcards for a complete beginner. "
        "Use simple, easy-to-understand language (Hinglish/Indian context is great if relevant, but keep it professional). "
        "Keep answers under 3 sentences. "
        "You MUST return the response strictly as a JSON array of objects, with no markdown like ```json. "
        'Format exactly like this: [{"question": "What is Market Cap?", "answer": "It is the total value of all a company\'s shares combined."}]'
    )
    
    user_prompt = f"Topic to teach: {topic}"
    
    raw_response = generate_ai_response(system_prompt, user_prompt)
    
    try:
        clean_response = raw_response.replace('```json', '').replace('```', '').strip()
        parsed_data = json.loads(clean_response)
        return parsed_data
    except json.JSONDecodeError:
        return [{"question": "System Error", "answer": "Could not generate flashcards. Please try a different topic."}]