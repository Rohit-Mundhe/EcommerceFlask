# ShopZone – Anvil E-Commerce App

A fully Python e-commerce web app hosted for free on [Anvil](https://anvil.works).  
No Flask. No Supabase. No servers to manage.

## Stack
| Layer | Technology |
|---|---|
| UI (frontend) | Anvil Forms (Python) |
| Backend logic | Anvil Server Modules (Python) |
| Database | Anvil Data Tables (built-in) |
| Hosting | Anvil Cloud (free, `yourapp.anvil.app`) |

## Features
- Product listing with search and category filter
- Product detail page with related items
- User registration and login (password hashed with werkzeug)
- Shopping cart (session-based)
- Checkout with shipping details (Cash on Delivery)
- Order confirmation and order history
- User profile editor

## Project structure
```
anvil_app/
  server_module.py              ← All backend functions (@anvil.server.callable)
  SETUP.md                      ← Full step-by-step hosting guide
  client_code/
    Globals.py                  ← Shared cart & user state
    ProductCard.py              ← Reusable product card component
    HomeForm.py                 ← Home / product listing (Startup Form)
    ProductForm.py              ← Single product detail
    LoginForm.py
    RegisterForm.py
    CartForm.py
    CheckoutForm.py
    OrderConfirmationForm.py
    OrdersForm.py
    ProfileForm.py
```

## How to deploy
See the full guide: [anvil_app/SETUP.md](anvil_app/SETUP.md)

Quick summary:
1. Sign up at **https://anvil.works** (free)
2. Create a blank Material Design 3 app
3. Add `werkzeug` under Settings → Dependencies
4. Create 4 Data Tables (`products`, `users`, `orders`, `order_items`)
5. Paste each file from `anvil_app/` into the corresponding Anvil editor section
6. Click **Publish** → live URL instantly
