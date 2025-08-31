from dotenv import load_dotenv
import os

load_dotenv()

# API CONFIGURATION
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPEN_ROUTER_API_KEY = os.getenv("OPEN_ROUTER_KEY")


# BASE URL

OPEN_ROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# LLM CONFIGURATION

DEFAULT_GEMINI_MODEL = "gemini-2.5-flash"
DEFAULT_OPENAI_MODEL = "openai/gpt-4o"
