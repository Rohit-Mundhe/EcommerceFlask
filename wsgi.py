import sys
import os

# Add the backend folder to the Python path
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app_supabase import app as application
