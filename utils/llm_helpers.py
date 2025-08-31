from openai import OpenAI
from config import (
    OPEN_ROUTER_API_KEY,
    OPEN_ROUTER_BASE_URL,
    DEFAULT_OPENAI_MODEL)

client = OpenAI(
    base_url= OPEN_ROUTER_BASE_URL,
    api_key=OPEN_ROUTER_API_KEY
)

message_history = []

def chat(user_input):
    message_history.append({"role":"user","content":user_input})

    completeion = client.chat.completions.create(
        model= DEFAULT_OPENAI_MODEL,
        messages = message_history,
        max_tokens=500,
        temperature=0.7,

    )
    response = completeion.choices[0].message.content
    message_history.append({"role":"assistant","content":response})
    print(message_history)
    return response
