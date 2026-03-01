"""
HomeForm  –  Main product listing page
=========================================
Anvil Form: HomeForm
Layout components (add in the Anvil designer):
  - search_box        : TextBox  (placeholder "Search products…")
  - search_btn        : Button   ("Search")
  - category_panel    : ColumnPanel  (for category chips)
  - products_panel    : ColumnPanel  (for product cards)
  - cart_badge        : Label        (shows cart item count)
  - nav_login_btn     : Button  ("Log In")
  - nav_logout_btn    : Button  ("Log Out")
  - nav_orders_btn    : Button  ("My Orders")
  - nav_cart_btn      : Button  ("Cart")
"""
from ._anvil_designer import HomeFormTemplate
from anvil import *
import anvil.server

from . import Globals          # shared cart & user state
from .ProductCard import ProductCard


class HomeForm(HomeFormTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
        self._current_category = None
        self._refresh_nav()
        self._load_products()

    # ── Navigation ────────────────────────────────────────────────────────────

    def _refresh_nav(self):
        logged_in = Globals.current_user is not None
        self.nav_login_btn.visible  = not logged_in
        self.nav_logout_btn.visible = logged_in
        self.nav_orders_btn.visible = logged_in
        self._update_cart_badge()

    def _update_cart_badge(self):
        count = sum(Globals.cart.values())
        self.cart_badge.text = f"🛒 Cart ({count})"

    def nav_login_btn_click(self, **event_args):
        open_form('LoginForm')

    def nav_logout_btn_click(self, **event_args):
        Globals.current_user = None
        Globals.cart = {}
        Notification("You have been logged out.", style="info").show()
        self._refresh_nav()

    def nav_orders_btn_click(self, **event_args):
        open_form('OrdersForm')

    def nav_cart_btn_click(self, **event_args):
        open_form('CartForm')

    # ── Products ──────────────────────────────────────────────────────────────

    def _load_products(self, search=None):
        self.products_panel.clear()
        self.category_panel.clear()

        cats = anvil.server.call('get_categories')
        # "All" chip
        all_btn = Button(text="All", role="outlined-button")
        all_btn.set_event_handler('click', lambda **e: self._filter_category(None))
        self.category_panel.add_component(all_btn)
        for cat in cats:
            btn = Button(text=cat, role="outlined-button")
            btn.set_event_handler('click', lambda **e, c=cat: self._filter_category(c))
            self.category_panel.add_component(btn)

        products = anvil.server.call(
            'get_products',
            search=search,
            category=self._current_category
        )
        if not products:
            self.products_panel.add_component(Label(text="No products found."))
            return
        for p in products:
            card = ProductCard(product=p)
            card.set_event_handler('add_to_cart', self._on_add_to_cart)
            card.set_event_handler('view_product', self._on_view_product)
            self.products_panel.add_component(card)

    def _filter_category(self, category):
        self._current_category = category
        self._load_products(search=self.search_box.text.strip() or None)

    def search_btn_click(self, **event_args):
        self._load_products(search=self.search_box.text.strip() or None)

    def _on_add_to_cart(self, product, **event_args):
        if Globals.current_user is None:
            Notification("Please log in to add items to your cart.", style="warning").show()
            open_form('LoginForm')
            return
        pid = product['id']
        Globals.cart[pid] = Globals.cart.get(pid, 0) + 1
        Notification(f"'{product['name']}' added to cart!", style="success").show()
        self._update_cart_badge()

    def _on_view_product(self, product, **event_args):
        open_form('ProductForm', product_id=product['id'])
