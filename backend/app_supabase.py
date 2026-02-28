import os
import certifi
import httpx
from datetime import timedelta
from supabase import create_client, Client
from supabase.lib.client_options import SyncClientOptions
from flask import (Flask, render_template, jsonify, request,
                   session, redirect, url_for, flash)
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.middleware.proxy_fix import ProxyFix
import logging

os.environ['SSL_CERT_FILE']      = certifi.where()
os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()

# ── Supabase ──────────────────────────────────────────────────────────────────
SUPABASE_URL = os.environ.get('SUPABASE_URL', 'https://khacikjsbltpkqpcjmfn.supabase.co')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY',
    'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.'
    'eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImtoYWNpa2pzYmx0cGtxcGNqbWZuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzIxODcyNzQsImV4cCI6MjA4Nzc2MzI3NH0.'
    'wfpuzdQVckgzy1v9rWD-63f4dC9RgI0MXy3BKL8Kjzg')

_http = httpx.Client(verify=False)
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY,
                                  options=SyncClientOptions(httpx_client=_http))

# ── Flask ─────────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
app = Flask(__name__,
            template_folder=os.path.join(BASE_DIR, 'templates'),
            static_folder=os.path.join(BASE_DIR, 'static'))
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
app.secret_key = os.environ.get('SECRET_KEY', 'shopzone-secret-2026')
app.permanent_session_lifetime = timedelta(minutes=30)
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

@app.before_request
def make_session_permanent():
    session.permanent = True

@app.context_processor
def inject_globals():
    cart  = session.get('cart', {})
    count = sum(cart.values()) if cart else 0
    return dict(cart_count=count, current_user=current_user())

# ── Helpers ───────────────────────────────────────────────────────────────────
def current_user():
    return session.get('user')

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user():
            flash('Please log in to continue.', 'warning')
            return redirect(url_for('login', next=request.path))
        return f(*args, **kwargs)
    return decorated

# ── Auth ──────────────────────────────────────────────────────────────────────
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user():
        return redirect(url_for('home'))
    if request.method == 'POST':
        name     = request.form.get('name', '').strip()
        email    = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm  = request.form.get('confirm_password', '')
        phone    = request.form.get('phone', '').strip()
        if not name or not email or not password:
            flash('All fields are required.', 'danger')
            return render_template('register.html')
        if password != confirm:
            flash('Passwords do not match.', 'danger')
            return render_template('register.html')
        if len(password) < 6:
            flash('Password must be at least 6 characters.', 'danger')
            return render_template('register.html')
        if supabase.table('users').select('id').eq('email', email).execute().data:
            flash('Email already registered.', 'danger')
            return render_template('register.html')
        hashed = generate_password_hash(password)
        supabase.table('users').insert(
            {'name': name, 'email': email, 'password': hashed, 'phone': phone}).execute()
        flash('Account created! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user():
        return redirect(url_for('home'))
    if request.method == 'POST':
        email    = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        result   = supabase.table('users').select('*').eq('email', email).execute()
        if result.data and check_password_hash(result.data[0]['password'], password):
            u = result.data[0]
            session['user'] = {'id': u['id'], 'email': u['email'],
                               'name': u.get('name', ''), 'phone': u.get('phone', '')}
            flash(f"Welcome back, {u.get('name', 'User')}!", 'success')
            next_url = request.args.get('next', '')
            if next_url and next_url.startswith('/'):
                return redirect(next_url)
            return redirect(url_for('home'))
        flash('Invalid email or password.', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    u = current_user()
    if request.method == 'POST':
        name  = request.form.get('name', '').strip()
        phone = request.form.get('phone', '').strip()
        supabase.table('users').update({'name': name, 'phone': phone}).eq('id', u['id']).execute()
        session['user']['name']  = name
        session['user']['phone'] = phone
        flash('Profile updated successfully.', 'success')
        return redirect(url_for('profile'))
    db_user = supabase.table('users').select('id,name,email,phone,created_at').eq('id', u['id']).execute().data
    return render_template('profile.html', user=db_user[0] if db_user else u)

# ── Products ──────────────────────────────────────────────────────────────────
@app.route('/')
def home():
    query    = request.args.get('q', '').strip()
    category = request.args.get('category', '').strip()
    q = supabase.table('products').select('*')
    if query:
        q = q.ilike('name', f'%{query}%')
    if category:
        q = q.eq('category', category)
    products = q.execute().data or []
    cats = supabase.table('products').select('category').execute().data or []
    category_list = sorted({c['category'] for c in cats if c.get('category')})
    return render_template('index.html', products=products, category_list=category_list,
                           query=query, selected_category=category)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    result = supabase.table('products').select('*').eq('id', product_id).execute()
    if not result.data:
        flash('Product not found.', 'danger')
        return redirect(url_for('home'))
    p = result.data[0]
    related = supabase.table('products').select('*')\
        .eq('category', p.get('category', '')).neq('id', product_id).limit(4).execute().data or []
    return render_template('product.html', product=p, related=related)

@app.route('/api/products')
def api_products():
    return jsonify(supabase.table('products').select('*').execute().data or [])

# ── Cart ──────────────────────────────────────────────────────────────────────
def _get_cart_items():
    cart  = session.get('cart', {})
    items, total = [], 0
    for pid, qty in cart.items():
        res = supabase.table('products').select('*').eq('id', int(pid)).execute()
        if res.data:
            item = res.data[0]
            item['quantity'] = qty
            item['subtotal'] = round(item['price'] * qty, 2)
            total += item['subtotal']
            items.append(item)
    return items, round(total, 2)

@app.route('/cart')
@login_required
def cart():
    items, total = _get_cart_items()
    return render_template('cart.html', cart_items=items, total=total)

@app.route('/cart/add/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    if not current_user():
        flash('Please log in to add items to your cart.', 'warning')
        return redirect(url_for('login', next=url_for('product_detail', product_id=product_id)))
    qty  = max(1, int(request.form.get('quantity', 1)))
    cart = session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + qty
    session['cart'] = cart
    flash('Item added to cart!', 'success')
    return redirect(request.referrer or url_for('home'))

@app.route('/cart/remove/<int:product_id>', methods=['POST'])
@login_required
def remove_from_cart(product_id):
    cart = session.get('cart', {})
    cart.pop(str(product_id), None)
    session['cart'] = cart
    flash('Item removed.', 'info')
    return redirect(url_for('cart'))

@app.route('/cart/update/<int:product_id>', methods=['POST'])
@login_required
def update_cart(product_id):
    qty  = int(request.form.get('quantity', 1))
    cart = session.get('cart', {})
    if qty <= 0:
        cart.pop(str(product_id), None)
    else:
        cart[str(product_id)] = qty
    session['cart'] = cart
    return redirect(url_for('cart'))

@app.route('/cart/clear', methods=['POST'])
@login_required
def clear_cart():
    session['cart'] = {}
    return redirect(url_for('cart'))

# ── Checkout & Orders ─────────────────────────────────────────────────────────
@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    items, total = _get_cart_items()
    if not items:
        flash('Your cart is empty.', 'warning')
        return redirect(url_for('cart'))
    if request.method == 'POST':
        uid = current_user()['id']
        order_res = supabase.table('orders').insert({
            'user_id':          uid,
            'status':           'confirmed',
            'payment_method':   'Cash on Delivery',
            'total_amount':     total,
            'shipping_name':    request.form.get('full_name', ''),
            'shipping_phone':   request.form.get('phone', ''),
            'shipping_address': request.form.get('address', ''),
            'shipping_city':    request.form.get('city', ''),
            'shipping_state':   request.form.get('state', ''),
            'shipping_pincode': request.form.get('pincode', ''),
            'note':             request.form.get('note', ''),
        }).execute()
        order_id = order_res.data[0]['id']
        for item in items:
            supabase.table('order_items').insert({
                'order_id':   order_id,
                'product_id': item['id'],
                'quantity':   item['quantity'],
                'price':      item['price'],
            }).execute()
        session['cart'] = {}
        flash(f'Order #{order_id} placed! You will pay on delivery.', 'success')
        return redirect(url_for('order_confirmation', order_id=order_id))
    u = current_user()
    return render_template('checkout.html', cart_items=items, total=total, user=u)

@app.route('/order/confirmation/<int:order_id>')
@login_required
def order_confirmation(order_id):
    order = supabase.table('orders').select('*').eq('id', order_id).execute().data
    if not order or order[0]['user_id'] != current_user()['id']:
        return redirect(url_for('home'))
    items = supabase.table('order_items').select('*, products(*)').eq('order_id', order_id).execute().data or []
    return render_template('order_confirmation.html', order=order[0], items=items)

@app.route('/orders')
@login_required
def my_orders():
    uid    = current_user()['id']
    orders = supabase.table('orders').select('*').eq('user_id', uid)\
                     .order('order_date', desc=True).execute().data or []
    for o in orders:
        o['items'] = supabase.table('order_items')\
                             .select('*, products(*)')\
                             .eq('order_id', o['id']).execute().data or []
        o['order_total'] = sum(
            i['products']['price'] * i['quantity']
            for i in o['items'] if i.get('products')
        )
    return render_template('orders.html', orders=orders)

if __name__ == '__main__':
    import os
    app.run(debug=os.environ.get('FLASK_DEBUG', 'false').lower() == 'true',
            host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
