from openai import OpenAI
from config import (
    GEMINI_API_KEY,
    OPEN_ROUTER_API_KEY,
    OPEN_ROUTER_BASE_URL,
    DEFAULT_GEMINI_MODEL,
    DEFAULT_OPENAI_MODEL)

client = OpenAI(
    base_url= OPEN_ROUTER_BASE_URL,
    api_key=OPEN_ROUTER_API_KEY
)

def chat(inp:str, role="user"):
    message_history = []
    message_history.append({"role":role,"content":inp})

    completeion = client.responses.create(
        model= DEFAULT_OPENAI_MODEL,
        input = message_history
    )

    response = completeion
    print(response)
    print(inp)
    return "hetlo"
