# ShopZone – E-Commerce Web App

A Flask + Supabase e-commerce app. Free hosting on PythonAnywhere.

## Stack
| Layer | Technology |
|---|---|
| Backend | Flask (Python) |
| Database | Supabase (Postgres) |
| Templates | Jinja2 + HTML/CSS |
| Hosting | PythonAnywhere (free) |

## Project structure
```
backend/
  app_supabase.py     ← main Flask app
  supabase_schema.sql ← database schema
static/
  styles.css
  app.js
templates/           ← all HTML pages
wsgi.py              ← PythonAnywhere entry point
requirements.txt
```

## Environment variables required
| Variable | Description |
|---|---|
| `SUPABASE_URL` | Your Supabase project URL |
| `SUPABASE_KEY` | Your Supabase anon/service key |
| `SECRET_KEY` | Flask session secret key |

## Deploy to PythonAnywhere (free)
See the step-by-step instructions below in the Hosting section.
