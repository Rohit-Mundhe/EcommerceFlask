# ShopZone – Complete Hosting Guide on Anvil (Free)

Anvil is a 100 % free-to-host Python web platform.  
No terminal, no server config, no domain purchase needed.  
Your app gets a public URL like `https://YOURAPPNAME.anvil.app`.

---

## PART 1 – Create Your Free Account & App

### Step 1 – Sign up
1. Open your browser and go to **https://anvil.works**
2. Click **"Get started for free"**
3. Enter your email and choose a password → click **"Create account"**
4. Check your email for a verification link and click it

### Step 2 – Create a new app
1. After logging in you land on the **My Apps** dashboard
2. Click the big **"+ New Blank App"** button
3. A theme picker appears — choose **"Material Design 3"** (best looking, free tier)
4. Your app opens in the Anvil online editor
5. At the very top, click the app name ("App 1") and **rename it** to `ShopZone`

> You are now inside the Anvil editor. The left sidebar has:
> - **Forms** (UI pages)  
> - **Modules** (shared Python code)  
> - **Server Modules** (backend Python)  
> - **Data** (database tables)  
> - **Assets** (images, files)  

---

## PART 2 – Add the Python Dependency

### Step 3 – Add werkzeug package
The server code uses `werkzeug` for password hashing.

1. In the left sidebar click the **gear icon ⚙ "Settings"** (bottom of sidebar)
2. Click the **"Dependencies"** tab
3. Under **"Third‑party packages (PyPI)"** click **"Add package"**
4. Type `werkzeug` and press Enter
5. Click **"Confirm"**

---

## PART 3 – Create the Database Tables

### Step 4 – Open the Data tab
1. In the left sidebar click **"Data"** (cylinder/database icon)
2. You see an empty data section

### Step 5 – Create the `products` table
1. Click **"+ Add table"**
2. Name it exactly `products` → click **"Create"**
3. Click **"+ Add column"** and add these columns one by one:

| Column name | Type to select |
|---|---|
| `name` | Text |
| `price` | Number |
| `description` | Text |
| `image_url` | Text |
| `category` | Text |

> Each column: type the name in the Name field, select the type from the dropdown, click "Add column".

### Step 6 – Create the `users` table
1. Click **"+ Add table"** → name it `users` → **"Create"**
2. Add columns:

| Column name | Type |
|---|---|
| `name` | Text |
| `email` | Text |
| `password_hash` | Text |
| `phone` | Text |
| `created_at` | Date/Time |

### Step 7 – Create the `orders` table
1. Click **"+ Add table"** → name it `orders` → **"Create"**
2. Add columns:

| Column name | Type |
|---|---|
| `user_id` | Text |
| `order_date` | Date/Time |
| `status` | Text |
| `payment_method` | Text |
| `total_amount` | Number |
| `shipping_name` | Text |
| `shipping_phone` | Text |
| `shipping_address` | Text |
| `shipping_city` | Text |
| `shipping_state` | Text |
| `shipping_pincode` | Text |
| `note` | Text |

### Step 8 – Create the `order_items` table
1. Click **"+ Add table"** → name it `order_items` → **"Create"**
2. Add columns:

| Column name | Type |
|---|---|
| `order_id` | Link to single row → select table **orders** |
| `product_id` | Link to single row → select table **products** |
| `quantity` | Number |
| `price` | Number |

> For the two "Link" columns: select type **"Link to single row"**, then a second dropdown appears — select the correct table (`orders` or `products`).

---

## PART 4 – Add the Server Module (Backend)

### Step 9 – Create the server module
1. In the left sidebar, find **"Server Modules"** and click the **"+"** next to it
2. A new file called `ServerModule1` appears and opens in the editor
3. **Select all the default code** in the editor (Ctrl+A) and **delete it**
4. Open the file `anvil_app/server_module.py` from this project in VS Code
5. Select all (Ctrl+A), copy (Ctrl+C)
6. Go back to the Anvil browser tab, click in the editor, and paste (Ctrl+V)
7. Press **Ctrl+S** to save (or Anvil auto-saves)

---

## PART 5 – Add the Shared Client Module

### Step 10 – Create the Globals module
1. In the left sidebar, find **"Modules"** (under the Forms section) and click **"+"**
2. A dialog asks for a name — type `Globals` (capital G, exactly) → click **"OK"**
3. Delete all default content in the editor
4. Open `anvil_app/client_code/Globals.py` in VS Code, copy all, paste into Anvil
5. Save (Ctrl+S)

---

## PART 6 – Create the Custom Component

### Step 11 – Create ProductCard custom component
1. In the left sidebar, find **"Custom Components"** and click **"+"**
2. Name it `ProductCard` (exact spelling, capital P and C) → click **"OK"**
3. The designer opens. Switch to the **"Code"** tab (top of the editor area)
4. Delete all default code
5. Open `anvil_app/client_code/ProductCard.py` in VS Code, copy all, paste into Anvil
6. Now switch back to the **"Design"** tab and add these components:
   - Drag an **Image** component onto the form → in the right panel set its name to `product_image`
   - Drag a **Label** → name it `category_label`
   - Drag a **Label** → name it `product_name`
   - Drag a **Label** → name it `product_price`
   - Drag a **Label** → name it `product_desc`
   - Drag a **Button** → name it `add_cart_btn`, set text to `🛒 Add to Cart`
   - Drag a **Button** → name it `view_btn`, set text to `View Details`

> **How to rename a component:** Click the component in the designer → in the right properties panel find the **"name"** field at the top → type the exact name listed above.

---

## PART 7 – Create All the Forms

> **How to create a form:**  
> Left sidebar → click **"+"** next to **"Forms"** → choose **"Blank Panel"** → type the form name → click **"OK"**.  
> Then click the **"Code"** tab, select all default code, delete it, paste in the code from the corresponding file.  
> Then go to the **"Design"** tab and add the components listed at the top of each code file.

---

### Step 12 – HomeForm (Startup Form)
**Create form named:** `HomeForm`

After pasting the code, add these components in the Design tab:

| Component type | Name to set | Extra properties |
|---|---|---|
| TextBox | `search_box` | placeholder = `Search products…` |
| Button | `search_btn` | text = `Search` |
| ColumnPanel | `category_panel` | — |
| ColumnPanel | `products_panel` | — |
| Label | `cart_badge` | text = `🛒 Cart (0)` |
| Button | `nav_login_btn` | text = `Log In` |
| Button | `nav_logout_btn` | text = `Log Out` |
| Button | `nav_orders_btn` | text = `My Orders` |
| Button | `nav_cart_btn` | text = `Cart` |

**Set as Startup Form:**
1. Right-click `HomeForm` in the left sidebar
2. Click **"Set as startup form"**
3. A rocket 🚀 icon appears next to it confirming it's the startup form

---

### Step 13 – ProductForm
**Create form named:** `ProductForm`

Components to add:

| Component type | Name | Extra |
|---|---|---|
| Image | `product_image` | — |
| Label | `category_label` | — |
| Label | `product_name` | — |
| Label | `product_price` | — |
| Label | `product_desc` | — |
| NumberBox | `quantity_box` | minimum = `1`, value = `1` |
| Button | `add_cart_btn` | text = `🛒 Add to Cart` |
| Button | `back_btn` | text = `← Back` |
| ColumnPanel | `related_panel` | — |

---

### Step 14 – LoginForm
**Create form named:** `LoginForm`

Components:

| Component type | Name | Extra |
|---|---|---|
| TextBox | `email_box` | placeholder = `Email` |
| TextBox | `password_box` | hide_text = ✔ (tick the checkbox) |
| Button | `login_btn` | text = `Log In` |
| Link | `register_link` | text = `Don't have an account? Register` |
| Label | `error_label` | visible = ✗ (untick visible) |

---

### Step 15 – RegisterForm
**Create form named:** `RegisterForm`

Components:

| Component type | Name | Extra |
|---|---|---|
| TextBox | `name_box` | placeholder = `Full Name` |
| TextBox | `email_box` | placeholder = `Email` |
| TextBox | `password_box` | hide_text = ✔ |
| TextBox | `confirm_box` | hide_text = ✔, placeholder = `Confirm Password` |
| TextBox | `phone_box` | placeholder = `Phone (optional)` |
| Button | `register_btn` | text = `Create Account` |
| Link | `login_link` | text = `Already have an account? Log In` |
| Label | `error_label` | visible = ✗ |

---

### Step 16 – CartForm
**Create form named:** `CartForm`

Components:

| Component type | Name | Extra |
|---|---|---|
| ColumnPanel | `cart_panel` | — |
| Label | `total_label` | text = `Total: ₹0.00` |
| Button | `checkout_btn` | text = `Proceed to Checkout` |
| Button | `clear_btn` | text = `Clear Cart` |
| Button | `continue_btn` | text = `← Continue Shopping` |
| Label | `empty_label` | text = `Your cart is empty.`, visible = ✗ |

---

### Step 17 – CheckoutForm
**Create form named:** `CheckoutForm`

Components:

| Component type | Name | Extra |
|---|---|---|
| TextBox | `full_name_box` | placeholder = `Full Name *` |
| TextBox | `phone_box` | placeholder = `Phone *` |
| TextBox | `address_box` | placeholder = `Address *`, multiline = ✔ |
| TextBox | `city_box` | placeholder = `City *` |
| TextBox | `state_box` | placeholder = `State *` |
| TextBox | `pincode_box` | placeholder = `PIN Code *` |
| TextBox | `note_box` | placeholder = `Delivery note (optional)` |
| Label | `payment_label` | text = `Payment: Cash on Delivery` |
| ColumnPanel | `order_summary` | — |
| Label | `total_label` | text = `Total: ₹0.00` |
| Button | `place_order_btn` | text = `Place Order` |
| Button | `back_btn` | text = `← Back to Cart` |
| Label | `error_label` | visible = ✗ |

---

### Step 18 – OrderConfirmationForm
**Create form named:** `OrderConfirmationForm`

Components:

| Component type | Name | Extra |
|---|---|---|
| Label | `order_id_label` | text = `Order #` |
| Label | `status_label` | text = `Status:` |
| ColumnPanel | `items_panel` | — |
| Label | `total_label` | text = `Total:` |
| Label | `shipping_label` | — |
| Button | `home_btn` | text = `Continue Shopping` |
| Button | `orders_btn` | text = `View My Orders` |

---

### Step 19 – OrdersForm
**Create form named:** `OrdersForm`

Components:

| Component type | Name | Extra |
|---|---|---|
| ColumnPanel | `orders_panel` | — |
| Button | `back_btn` | text = `← Home` |

---

### Step 20 – ProfileForm
**Create form named:** `ProfileForm`

Components:

| Component type | Name | Extra |
|---|---|---|
| TextBox | `name_box` | placeholder = `Full Name` |
| TextBox | `phone_box` | placeholder = `Phone` |
| Label | `email_label` | — |
| Label | `joined_label` | — |
| Button | `save_btn` | text = `Save Changes` |
| Button | `back_btn` | text = `← Home` |
| Label | `message_label` | visible = ✗ |

---

## PART 8 – Seed Sample Products

### Step 21 – Add sample products to the database
1. In the left sidebar click **"Data"**
2. Click on the **`products`** table
3. Click **"+ Add row"** and manually add rows, OR use the faster method below:

**Faster: use a temporary server function**
1. Open your server module (`ServerModule1`)
2. At the bottom of the file add this temporary function:

```python
@anvil.server.callable
def seed_products():
    from anvil.tables import app_tables
    data = [
        ("Wireless Headphones", 49.99, "High quality wireless headphones with noise cancellation.", "https://placehold.co/300x200?text=Headphones", "Electronics"),
        ("Running Shoes",       89.99, "Lightweight and comfortable running shoes.",               "https://placehold.co/300x200?text=Shoes",       "Footwear"),
        ("Backpack",            34.99, "Durable 30L backpack for everyday use.",                  "https://placehold.co/300x200?text=Backpack",     "Bags"),
        ("Smartwatch",         129.99, "Fitness smartwatch with heart rate monitor.",             "https://placehold.co/300x200?text=Smartwatch",   "Electronics"),
        ("Sunglasses",          19.99, "UV400 protection sunglasses.",                            "https://placehold.co/300x200?text=Sunglasses",   "Accessories"),
        ("Water Bottle",        14.99, "Stainless steel insulated water bottle.",                 "https://placehold.co/300x200?text=Bottle",       "Accessories"),
    ]
    for name, price, desc, img, cat in data:
        app_tables.products.add_row(name=name, price=price, description=desc, image_url=img, category=cat)
```

3. Save. Then open any Form's code tab and in the Anvil interactive Python console (bottom of editor) run:
   ```python
   import anvil.server
   anvil.server.call('seed_products')
   ```
4. Go back to the **Data → products** table to confirm 6 rows appeared
5. Delete the `seed_products` function from the server module (it was one-time use)

---

## PART 9 – Test in the Editor

### Step 22 – Run the app locally in the editor
1. Click the **▶ Run** button at the top of the Anvil editor
2. A preview window opens inside the browser
3. Test the following flows:
   - Home page loads and shows product cards
   - Search and category filter work
   - Register a new account
   - Log in with that account
   - Add items to cart
   - Checkout with shipping details
   - Confirm the order appears in "My Orders"

---

## PART 10 – Publish (Go Live)

### Step 23 – Publish your app for free
1. Click the **"Publish"** button at the top-right of the Anvil editor
2. A dialog appears — choose **"Publish to web"**
3. Anvil gives you a URL like: `https://shopzone.anvil.app`  
   (you can customize the subdomain if available)
4. Click **"Publish"**
5. Your app is now **live on the internet** — share the URL with anyone

> **Free tier limits:** unlimited usage, always-on, custom subdomain on `anvil.app`.  
> Upgrading is only needed for custom domains (e.g. `shopzone.com`).

---

## PART 11 – Quick Reference File Map

```
anvil_app/
  server_module.py              → Paste into: Server Modules → ServerModule1
  client_code/
    Globals.py                  → Paste into: Modules → Globals
    ProductCard.py              → Paste into: Custom Components → ProductCard
    HomeForm.py                 → Paste into: Forms → HomeForm  (Startup Form ✔)
    ProductForm.py              → Paste into: Forms → ProductForm
    LoginForm.py                → Paste into: Forms → LoginForm
    RegisterForm.py             → Paste into: Forms → RegisterForm
    CartForm.py                 → Paste into: Forms → CartForm
    CheckoutForm.py             → Paste into: Forms → CheckoutForm
    OrderConfirmationForm.py    → Paste into: Forms → OrderConfirmationForm
    OrdersForm.py               → Paste into: Forms → OrdersForm
    ProfileForm.py              → Paste into: Forms → ProfileForm
```

---

## Common Mistakes to Avoid

| Mistake | Fix |
|---|---|
| Component name typo (e.g. `searchbox` instead of `search_box`) | Names must match the code exactly — copy from the table above |
| HomeForm not set as Startup Form | Right-click HomeForm → "Set as startup form" |
| `werkzeug` not added | Settings → Dependencies → add `werkzeug` |
| `order_items.order_id` set as Text instead of Link | Must be "Link to single row → orders" |
| `order_items.product_id` set as Text | Must be "Link to single row → products" |
| Globals module created under Server Modules | Must be under **Modules** (client-side), not Server Modules |
```
