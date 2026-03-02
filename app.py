import os
from datetime import timedelta
from functools import wraps
from supabase import create_client, Client
from flask import (Flask, render_template, request, session,
                   redirect, url_for, flash, jsonify)
from werkzeug.security import generate_password_hash, check_password_hash

# ── Supabase ──────────────────────────────────────────────────────────────────
SUPABASE_URL = os.environ.get('SUPABASE_URL', '').strip()
SUPABASE_KEY = os.environ.get('SUPABASE_KEY', '').strip()
if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError('Set SUPABASE_URL and SUPABASE_KEY environment variables.')
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ── Flask ─────────────────────────────────────────────────────────────────────
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'shopzone-2026')
app.permanent_session_lifetime = timedelta(hours=2)

# ── Helpers ───────────────────────────────────────────────────────────────────
def get_user():
    return session.get('user')

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not get_user():
            flash('Please log in to continue.', 'warning')
            return redirect(url_for('login', next=request.path))
        return f(*args, **kwargs)
    return decorated

@app.before_request
def make_permanent():
    session.permanent = True

@app.context_processor
def inject_globals():
    cart = session.get('cart', {})
    return dict(user=get_user(), cart_count=sum(cart.values()))

# ── Auth ──────────────────────────────────────────────────────────────────────
@app.route('/register', methods=['GET', 'POST'])
def register():
    if get_user():
        return redirect(url_for('index'))
    if request.method == 'POST':
        name     = request.form.get('name', '').strip()
        email    = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm  = request.form.get('confirm', '')
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
        supabase.table('users').insert({
            'name': name, 'email': email,
            'password': generate_password_hash(password), 'phone': phone
        }).execute()
        flash('Account created! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if get_user():
        return redirect(url_for('index'))
    if request.method == 'POST':
        email    = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        result   = supabase.table('users').select('*').eq('email', email).execute()
        if result.data and check_password_hash(result.data[0]['password'], password):
            u = result.data[0]
            session['user'] = {'id': u['id'], 'name': u['name'],
                               'email': u['email'], 'phone': u.get('phone', '')}
            flash(f"Welcome, {u['name']}!", 'success')
            return redirect(request.args.get('next') or url_for('index'))
        flash('Invalid email or password.', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    u = get_user()
    if request.method == 'POST':
        name  = request.form.get('name', '').strip()
        phone = request.form.get('phone', '').strip()
        supabase.table('users').update({'name': name, 'phone': phone}).eq('id', u['id']).execute()
        session['user']['name']  = name
        session['user']['phone'] = phone
        flash('Profile updated.', 'success')
        return redirect(url_for('profile'))
    row = supabase.table('users').select('*').eq('id', u['id']).execute().data
    return render_template('profile.html', u=row[0] if row else u)

# ── Products ──────────────────────────────────────────────────────────────────
@app.route('/')
def index():
    q   = request.args.get('q', '').strip()
    cat = request.args.get('cat', '').strip()
    qb  = supabase.table('products').select('*')
    if q:   qb = qb.ilike('name', f'%{q}%')
    if cat: qb = qb.eq('category', cat)
    products = qb.execute().data or []
    all_cats = supabase.table('products').select('category').execute().data or []
    cats = sorted({r['category'] for r in all_cats if r.get('category')})
    return render_template('index.html', products=products, cats=cats, q=q, cat=cat)

@app.route('/product/<int:pid>')
def product(pid):
    row = supabase.table('products').select('*').eq('id', pid).execute().data
    if not row:
        flash('Product not found.', 'danger')
        return redirect(url_for('index'))
    p       = row[0]
    related = supabase.table('products').select('*')\
        .eq('category', p['category']).neq('id', pid).limit(4).execute().data or []
    return render_template('product.html', p=p, related=related)

# ── Cart ──────────────────────────────────────────────────────────────────────
def get_cart_items():
    cart = session.get('cart', {})
    items, total = [], 0
    for pid, qty in cart.items():
        row = supabase.table('products').select('*').eq('id', int(pid)).execute().data
        if row:
            item = dict(row[0])
            item['qty'] = qty
            item['sub'] = round(item['price'] * qty, 2)
            total += item['sub']
            items.append(item)
    return items, round(total, 2)

@app.route('/cart')
@login_required
def cart():
    items, total = get_cart_items()
    return render_template('cart.html', items=items, total=total)

@app.route('/cart/add/<int:pid>', methods=['POST'])
def cart_add(pid):
    if not get_user():
        flash('Please log in first.', 'warning')
        return redirect(url_for('login'))
    qty = max(1, int(request.form.get('qty', 1)))
    c   = session.get('cart', {})
    c[str(pid)] = c.get(str(pid), 0) + qty
    session['cart'] = c
    flash('Added to cart!', 'success')
    return redirect(request.referrer or url_for('index'))

@app.route('/cart/update', methods=['POST'])
@login_required
def cart_update():
    pid = str(request.form.get('pid'))
    qty = int(request.form.get('qty', 0))
    c   = session.get('cart', {})
    if qty <= 0:
        c.pop(pid, None)
    else:
        c[pid] = qty
    session['cart'] = c
    return redirect(url_for('cart'))

@app.route('/cart/remove/<int:pid>', methods=['POST'])
@login_required
def cart_remove(pid):
    c = session.get('cart', {})
    c.pop(str(pid), None)
    session['cart'] = c
    return redirect(url_for('cart'))

@app.route('/cart/clear', methods=['POST'])
@login_required
def cart_clear():
    session['cart'] = {}
    return redirect(url_for('cart'))

# ── Checkout ──────────────────────────────────────────────────────────────────
@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    items, total = get_cart_items()
    if not items:
        flash('Your cart is empty.', 'warning')
        return redirect(url_for('cart'))
    u = get_user()
    if request.method == 'POST':
        order = supabase.table('orders').insert({
            'user_id':          u['id'],
            'status':           'confirmed',
            'payment_method':   'Cash on Delivery',
            'total_amount':     total,
            'shipping_name':    request.form.get('name', ''),
            'shipping_phone':   request.form.get('phone', ''),
            'shipping_address': request.form.get('address', ''),
            'shipping_city':    request.form.get('city', ''),
            'shipping_state':   request.form.get('state', ''),
            'shipping_pincode': request.form.get('pincode', ''),
            'note':             request.form.get('note', ''),
        }).execute().data[0]
        oid = order['id']
        for item in items:
            supabase.table('order_items').insert({
                'order_id':   oid,
                'product_id': item['id'],
                'quantity':   item['qty'],
                'price':      item['price'],
            }).execute()
        session['cart'] = {}
        flash(f'Order #{oid} placed! Pay on delivery.', 'success')
        return redirect(url_for('order_confirm', oid=oid))
    return render_template('checkout.html', items=items, total=total, u=u)

@app.route('/order/<int:oid>')
@login_required
def order_confirm(oid):
    order = supabase.table('orders').select('*').eq('id', oid).execute().data
    if not order or order[0]['user_id'] != get_user()['id']:
        return redirect(url_for('index'))
    items = supabase.table('order_items')\
        .select('*, products(*)').eq('order_id', oid).execute().data or []
    return render_template('order_confirmation.html', order=order[0], items=items)

@app.route('/orders')
@login_required
def orders():
    uid  = get_user()['id']
    rows = supabase.table('orders').select('*').eq('user_id', uid)\
               .order('order_date', desc=True).execute().data or []
    for o in rows:
        o['items'] = supabase.table('order_items')\
            .select('*, products(*)').eq('order_id', o['id']).execute().data or []
        o['total'] = sum(i['quantity'] * i['price'] for i in o['items'])
    return render_template('orders.html', orders=rows)

if __name__ == '__main__':
    app.run(debug=True)
