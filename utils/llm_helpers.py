from openai import OpenAI
from config import (
    OPEN_ROUTER_API_KEY,
    OPEN_ROUTER_BASE_URL,
    DEFAULT_OPENAI_MODEL)
import json
import os
from datetime import datetime

client = OpenAI(
    base_url= OPEN_ROUTER_BASE_URL,
    api_key=OPEN_ROUTER_API_KEY
)

# Define the 3 required personas for Part 2 of assignment
SYSTEM_PROMPTS = {
    "professional": {
        "name": "Professional Assistant",
        "prompt": "You are a professional business assistant. Provide formal, structured, and business-like responses. Use professional language, be concise, and focus on practical solutions. Always maintain a courteous and authoritative tone."
    },
    "creative": {
        "name": "Creative Companion", 
        "prompt": "You are a creative and imaginative companion. Be artistic, inspiring, and think outside the box. Use vivid language, metaphors, and encourage creative thinking. Help brainstorm ideas and approach problems from unique angles."
    },
    "technical": {
        "name": "Technical Expert",
        "prompt": "You are a technical expert and educator. Provide detailed, accurate technical explanations with step-by-step instructions. Break down complex concepts, use precise terminology, and include examples when helpful. Focus on thorough and educational responses."
    }
}

# Global state
current_persona = "professional"
message_history = []

# Initialize with default persona
def _initialize_conversation():
    global message_history
    message_history = [{"role": "system", "content": SYSTEM_PROMPTS[current_persona]["prompt"]}]

_initialize_conversation()

def chat(user_input):
    """Send user input to LLM and get response"""
    message_history.append({"role": "user", "content": user_input})

    try:
        completion = client.chat.completions.create(
            model=DEFAULT_OPENAI_MODEL,
            messages=message_history,
            max_tokens=500,
            temperature=0.7,
        )
        response = completion.choices[0].message.content
        message_history.append({"role": "assistant", "content": response})
        
        # Keep conversation history manageable (last 20 messages + system prompt)
        if len(message_history) > 21:
            system_msg = message_history[0]
            message_history = [system_msg] + message_history[-20:]
        
        return response
    except Exception as e:
        raise Exception(f"API call failed: {str(e)}")

def set_system_prompt(persona):
    """Change the AI persona"""
    global current_persona, message_history
    
    if persona in SYSTEM_PROMPTS:
        current_persona = persona
        # Reset conversation with new system prompt
        message_history = [{"role": "system", "content": SYSTEM_PROMPTS[persona]["prompt"]}]
        return f"[OK] Switched to {SYSTEM_PROMPTS[persona]['name']} mode"
    else:
        available = ", ".join(SYSTEM_PROMPTS.keys())
        return f"[ERROR] Invalid persona '{persona}'. Available: {available}"

def get_available_personas():
    """Get list of available persona names"""
    return list(SYSTEM_PROMPTS.keys())

def get_current_persona():
    """Get current persona name"""
    return current_persona

def get_current_persona_info():
    """Get current persona full information"""
    return SYSTEM_PROMPTS[current_persona]

def clear_history():
    """Clear conversation history but keep system prompt"""
    global message_history
    message_history = [{"role": "system", "content": SYSTEM_PROMPTS[current_persona]["prompt"]}]

def get_conversation_history():
    """Get current conversation history"""
    return message_history.copy()

# Bonus: Conversation persistence functions
def save_conversation(filename=None):
    """Save current conversation to JSON file"""
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"conversation_{current_persona}_{timestamp}.json"
    
    conversation_data = {
        "timestamp": datetime.now().isoformat(),
        "persona": current_persona,
        "persona_info": SYSTEM_PROMPTS[current_persona],
        "conversation": message_history
    }
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(conversation_data, f, indent=2, ensure_ascii=False)
        return filename
    except Exception as e:
        raise Exception(f"Failed to save conversation: {str(e)}")

def load_conversation(filename):
    """Load conversation from JSON file"""
    global message_history, current_persona
    
    try:
        if not os.path.exists(filename):
            raise FileNotFoundError(f"File not found: {filename}")
        
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Restore conversation state
        current_persona = data.get("persona", "professional")
        message_history = data.get("conversation", [])
        
        # Ensure we have a valid system prompt
        if not message_history or message_history[0]["role"] != "system":
            message_history.insert(0, {"role": "system", "content": SYSTEM_PROMPTS[current_persona]["prompt"]})
        
        return True
    except Exception as e:
        raise Exception(f"Failed to load conversation: {str(e)}")

def get_conversation_stats():
    """Get statistics about current conversation"""
    user_messages = len([msg for msg in message_history if msg["role"] == "user"])
    assistant_messages = len([msg for msg in message_history if msg["role"] == "assistant"])
    return {
        "user_messages": user_messages,
        "assistant_messages": assistant_messages,
        "total_messages": len(message_history) - 1,  # Exclude system message
        "current_persona": SYSTEM_PROMPTS[current_persona]["name"]
    }
