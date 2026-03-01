"""
ProductForm  –  Single product detail page
============================================
Anvil Form: ProductForm
Components:
  - product_image     : Image
  - category_label    : Label
  - product_name      : Label
  - product_price     : Label
  - product_desc      : Label
  - quantity_box      : NumberBox  (min=1, value=1)
  - add_cart_btn      : Button  ("🛒 Add to Cart")
  - back_btn          : Button  ("← Back")
  - related_panel     : ColumnPanel  (related products)
"""
from ._anvil_designer import ProductFormTemplate
from anvil import *
import anvil.server

from . import Globals
from .ProductCard import ProductCard


class ProductForm(ProductFormTemplate):
    def __init__(self, product_id=None, **properties):
        self._product_id = product_id
        self.init_components(**properties)
        self._load()

    def _load(self):
        p = anvil.server.call('get_product', self._product_id)
        if not p:
            Notification("Product not found.", style="danger").show()
            open_form('HomeForm')
            return
        self._product = p
        self.product_name.text    = p.get('name', '')
        self.product_price.text   = f"₹{p.get('price', 0):.2f}"
        self.category_label.text  = p.get('category', '')
        self.product_desc.text    = p.get('description', '')
        self.product_image.source = (
            p.get('image_url') or 'https://placehold.co/400x300?text=No+Image'
        )
        # Related products
        self.related_panel.clear()
        related = anvil.server.call(
            'get_related_products', p.get('category', ''), self._product_id
        )
        for rp in related:
            card = ProductCard(product=rp)
            card.set_event_handler('add_to_cart', self._on_add_to_cart)
            card.set_event_handler('view_product', lambda product, **e:
                open_form('ProductForm', product_id=product['id']))
            self.related_panel.add_component(card)

    def add_cart_btn_click(self, **event_args):
        if Globals.current_user is None:
            Notification("Please log in to add items to your cart.", style="warning").show()
            open_form('LoginForm')
            return
        qty = int(self.quantity_box.text or 1)
        qty = max(1, qty)
        pid = self._product['id']
        Globals.cart[pid] = Globals.cart.get(pid, 0) + qty
        Notification(f"Added {qty}× '{self._product['name']}' to cart!", style="success").show()

    def _on_add_to_cart(self, product, **event_args):
        if Globals.current_user is None:
            Notification("Please log in.", style="warning").show()
            return
        pid = product['id']
        Globals.cart[pid] = Globals.cart.get(pid, 0) + 1
        Notification(f"'{product['name']}' added to cart!", style="success").show()

    def back_btn_click(self, **event_args):
        open_form('HomeForm')
