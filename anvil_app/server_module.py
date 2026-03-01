"""
ShopZone – Anvil Server Module
================================
All functions decorated with @anvil.server.callable are callable from
client-side Anvil forms via anvil.server.call('function_name', ...).

Data Tables (create these in the Anvil editor under "Data" tab):
  products    – id*, name, price(number), description, image_url, category
  users       – id*, name, email(unique), password_hash, phone, created_at
  orders      – id*, user_email, order_date, status, payment_method,
                total_amount(number), shipping_name, shipping_phone,
                shipping_address, shipping_city, shipping_state,
                shipping_pincode, note
  order_items – id*, order_id(link:orders), product_id(link:products),
                quantity(number), price(number)

  (* id columns are auto-created by Anvil as row IDs)
"""

import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# ── Products ──────────────────────────────────────────────────────────────────

@anvil.server.callable
def get_products(search=None, category=None):
    """Return list of product dicts, optionally filtered."""
    rows = app_tables.products.search()
    results = []
    for row in rows:
        p = dict(row)
        if search and search.lower() not in (p.get('name') or '').lower():
            continue
        if category and p.get('category') != category:
            continue
        p['id'] = row.get_id()
        results.append(p)
    return results


@anvil.server.callable
def get_categories():
    """Return sorted list of unique category names."""
    cats = {row['category'] for row in app_tables.products.search() if row['category']}
    return sorted(cats)


@anvil.server.callable
def get_product(product_id):
    """Return a single product dict by row ID."""
    row = app_tables.products.get_by_id(product_id)
    if not row:
        return None
    p = dict(row)
    p['id'] = row.get_id()
    return p


@anvil.server.callable
def get_related_products(category, exclude_id):
    """Return up to 4 products in the same category, excluding one."""
    results = []
    for row in app_tables.products.search(category=category):
        if row.get_id() == exclude_id:
            continue
        p = dict(row)
        p['id'] = row.get_id()
        results.append(p)
        if len(results) >= 4:
            break
    return results


# ── Auth ──────────────────────────────────────────────────────────────────────

@anvil.server.callable
def register_user(name, email, password, phone=''):
    """Register a new user. Returns (True, None) on success or (False, error_msg)."""
    email = email.strip().lower()
    if not name or not email or not password:
        return False, 'All fields are required.'
    if len(password) < 6:
        return False, 'Password must be at least 6 characters.'
    existing = app_tables.users.get(email=email)
    if existing:
        return False, 'Email already registered.'
    app_tables.users.add_row(
        name=name,
        email=email,
        password_hash=generate_password_hash(password),
        phone=phone,
        created_at=datetime.utcnow()
    )
    return True, None


@anvil.server.callable
def login_user(email, password):
    """
    Validate credentials.
    Returns user dict (id, email, name, phone) on success, or None on failure.
    """
    email = email.strip().lower()
    row = app_tables.users.get(email=email)
    if row and check_password_hash(row['password_hash'], password):
        return {
            'id':    row.get_id(),
            'email': row['email'],
            'name':  row.get('name', ''),
            'phone': row.get('phone', ''),
        }
    return None


@anvil.server.callable
def update_profile(user_id, name, phone):
    """Update name and phone for a user by row ID."""
    row = app_tables.users.get_by_id(user_id)
    if not row:
        return False, 'User not found.'
    row.update(name=name, phone=phone)
    return True, None


@anvil.server.callable
def get_user_by_id(user_id):
    """Return user dict for profile display."""
    row = app_tables.users.get_by_id(user_id)
    if not row:
        return None
    u = dict(row)
    u['id'] = row.get_id()
    u.pop('password_hash', None)   # never expose password hash to client
    return u


# ── Orders ────────────────────────────────────────────────────────────────────

@anvil.server.callable
def place_order(user_id, cart, shipping):
    """
    Place an order.
    cart     – list of dicts: [{product_id, quantity, price}, ...]
    shipping – dict with keys: full_name, phone, address, city, state,
               pincode, note, payment_method
    Returns order row ID on success.
    """
    if not cart:
        raise ValueError('Cart is empty.')

    total = sum(item['price'] * item['quantity'] for item in cart)

    order_row = app_tables.orders.add_row(
        user_id=user_id,
        order_date=datetime.utcnow(),
        status='confirmed',
        payment_method=shipping.get('payment_method', 'Cash on Delivery'),
        total_amount=round(total, 2),
        shipping_name=shipping.get('full_name', ''),
        shipping_phone=shipping.get('phone', ''),
        shipping_address=shipping.get('address', ''),
        shipping_city=shipping.get('city', ''),
        shipping_state=shipping.get('state', ''),
        shipping_pincode=shipping.get('pincode', ''),
        note=shipping.get('note', ''),
    )
    order_id = order_row.get_id()

    for item in cart:
        product_row = app_tables.products.get_by_id(item['product_id'])
        app_tables.order_items.add_row(
            order_id=order_row,
            product_id=product_row,
            quantity=item['quantity'],
            price=item['price'],
        )

    return order_id


@anvil.server.callable
def get_order(order_id, user_id):
    """Return a single order with its items. Only the owning user may view it."""
    order_row = app_tables.orders.get_by_id(order_id)
    if not order_row or order_row['user_id'] != user_id:
        return None
    order = dict(order_row)
    order['id'] = order_row.get_id()
    order['items'] = _get_order_items(order_row)
    return order


@anvil.server.callable
def get_my_orders(user_id):
    """Return all orders for a user, newest first, each with items."""
    order_rows = sorted(
        app_tables.orders.search(user_id=user_id),
        key=lambda r: r['order_date'] or datetime.min,
        reverse=True
    )
    orders = []
    for row in order_rows:
        o = dict(row)
        o['id'] = row.get_id()
        o['items'] = _get_order_items(row)
        o['order_total'] = sum(
            i['price'] * i['quantity'] for i in o['items']
        )
        orders.append(o)
    return orders


# ── Internal helpers ──────────────────────────────────────────────────────────

def _get_order_items(order_row):
    """Return list of item dicts for an order row."""
    items = []
    for item_row in app_tables.order_items.search(order_id=order_row):
        item = {
            'quantity': item_row['quantity'],
            'price':    item_row['price'],
        }
        prod_row = item_row['product_id']
        if prod_row:
            item['product'] = {
                'id':       prod_row.get_id(),
                'name':     prod_row['name'],
                'price':    prod_row['price'],
                'image_url': prod_row.get('image_url'),
                'category': prod_row.get('category'),
            }
        items.append(item)
    return items
