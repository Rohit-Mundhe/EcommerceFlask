-- Products table
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    price NUMERIC(10,2) NOT NULL,
    description TEXT,
    image_url TEXT,
    category TEXT
);

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    phone TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Orders table
CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    order_date TIMESTAMP DEFAULT NOW(),
    status TEXT DEFAULT 'pending',
    payment_method TEXT DEFAULT 'Cash on Delivery',
    total_amount NUMERIC(10,2),
    shipping_name TEXT,
    shipping_phone TEXT,
    shipping_address TEXT,
    shipping_city TEXT,
    shipping_state TEXT,
    shipping_pincode TEXT,
    note TEXT
);

-- Order Items table (multiple products per order)
CREATE TABLE IF NOT EXISTS order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(id) ON DELETE CASCADE,
    product_id INTEGER REFERENCES products(id) ON DELETE SET NULL,
    quantity INTEGER NOT NULL,
    price NUMERIC(10,2)
);

-- ─────────────────────────────────────────────────────────
-- ALTER statements: run these if tables were created earlier
-- without the new columns (safe to run multiple times)
-- ─────────────────────────────────────────────────────────
ALTER TABLE products    ADD COLUMN IF NOT EXISTS category TEXT;
ALTER TABLE users       ADD COLUMN IF NOT EXISTS phone TEXT;
ALTER TABLE orders      ADD COLUMN IF NOT EXISTS payment_method TEXT DEFAULT 'Cash on Delivery';
ALTER TABLE orders      ADD COLUMN IF NOT EXISTS total_amount NUMERIC(10,2);
ALTER TABLE orders      ADD COLUMN IF NOT EXISTS shipping_name TEXT;
ALTER TABLE orders      ADD COLUMN IF NOT EXISTS shipping_phone TEXT;
ALTER TABLE orders      ADD COLUMN IF NOT EXISTS shipping_address TEXT;
ALTER TABLE orders      ADD COLUMN IF NOT EXISTS shipping_city TEXT;
ALTER TABLE orders      ADD COLUMN IF NOT EXISTS shipping_state TEXT;
ALTER TABLE orders      ADD COLUMN IF NOT EXISTS shipping_pincode TEXT;
ALTER TABLE orders      ADD COLUMN IF NOT EXISTS note TEXT;
ALTER TABLE order_items ADD COLUMN IF NOT EXISTS price NUMERIC(10,2);

-- ─────────────────────────────────────────────────────────
-- SAMPLE DATA: Run ONLY once to seed products for testing
-- Skip if products table already has data
-- ─────────────────────────────────────────────────────────
INSERT INTO products (name, price, description, image_url, category)
SELECT * FROM (VALUES
  ('Wireless Headphones', 49.99, 'High quality wireless headphones with noise cancellation.', 'https://placehold.co/300x200?text=Headphones', 'Electronics'),
  ('Running Shoes',       89.99, 'Lightweight and comfortable running shoes.',                'https://placehold.co/300x200?text=Shoes',       'Footwear'),
  ('Backpack',            34.99, 'Durable 30L backpack for everyday use.',                   'https://placehold.co/300x200?text=Backpack',     'Bags'),
  ('Smartwatch',         129.99, 'Fitness smartwatch with heart rate monitor.',              'https://placehold.co/300x200?text=Smartwatch',   'Electronics'),
  ('Sunglasses',          19.99, 'UV400 protection sunglasses.',                             'https://placehold.co/300x200?text=Sunglasses',   'Accessories'),
  ('Water Bottle',        14.99, 'Stainless steel insulated water bottle.',                  'https://placehold.co/300x200?text=Bottle',       'Accessories')
) AS v(name, price, description, image_url, category)
WHERE NOT EXISTS (SELECT 1 FROM products LIMIT 1);
