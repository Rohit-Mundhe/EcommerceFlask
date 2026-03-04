# ─────────────────────────────────────────────────────────────────────────────
# PythonAnywhere WSGI configuration file
#
# HOW TO USE:
#   1. On PythonAnywhere → Web tab → click the WSGI file link
#   2. Delete ALL existing content in that file
#   3. Paste the contents of THIS file
#   4. Replace YOURUSERNAME with your PythonAnywhere username (line 16)
#   5. Save → Reload
# ─────────────────────────────────────────────────────────────────────────────

import sys
import os

# ── CHANGE THIS ───────────────────────────────────────────────────────────────
USERNAME = 'Indianwomanengineer'

sys.path.insert(0, f'/home/{USERNAME}/EcommerceFlask')

os.environ['SUPABASE_URL'] = 'https://khacikjsbltpkqpcjmfn.supabase.co'
os.environ['SUPABASE_KEY'] = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImtoYWNpa2pzYmx0cGtxcGNqbWZuIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MjE4NzI3NCwiZXhwIjoyMDg3NzYzMjc0fQ.Yc6FhGGKaXEcd9j2aTie-mTnzmd7v-t-FeFOql0GE1c'
os.environ['SECRET_KEY']   = 'shopzone-2026'
# SSL_VERIFY is NOT set here — PythonAnywhere has no proxy, SSL works fine

from app import app
application = app

