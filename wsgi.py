import sys
import os

# Load .env file if present (local development only)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.app_supabase import app

application = app
