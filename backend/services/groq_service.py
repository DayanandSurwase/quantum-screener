from groq import Groq
from backend.config.settings import settings

client = Groq(api_key=settings.groq_api_key)

def generate_ai_response(system_prompt: str, user_prompt: str) -> str:
    """Standardized method to call the Groq API."""
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        model=settings.model_name,
        temperature=0.7,
        max_tokens=1024,
    )
    return chat_completion.choices[0].message.content