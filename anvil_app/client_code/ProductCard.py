"""
ProductCard  –  Reusable product card component
================================================
Anvil Custom Component.
Add these components in the designer:
  - product_image    : Image
  - category_label   : Label  (small badge)
  - product_name     : Label  (heading)
  - product_price    : Label
  - product_desc     : Label  (2-3 lines)
  - add_cart_btn     : Button ("🛒 Add to Cart")
  - view_btn         : Button ("View Details")

Custom events raised: 'add_to_cart', 'view_product'
  Both pass `product=self._product` as event data.
"""
from ._anvil_designer import ProductCardTemplate
from anvil import *


class ProductCard(ProductCardTemplate):
    def __init__(self, product=None, **properties):
        self._product = product or {}
        self.init_components(**properties)
        self._render()

    def _render(self):
        p = self._product
        self.product_name.text    = p.get('name', '')
        self.product_price.text   = f"₹{p.get('price', 0):.2f}"
        self.category_label.text  = p.get('category', '')
        desc = p.get('description', '')
        self.product_desc.text    = (desc[:80] + '…') if len(desc) > 80 else desc
        img_url = p.get('image_url') or 'https://placehold.co/300x220?text=No+Image'
        self.product_image.source = img_url

    def add_cart_btn_click(self, **event_args):
        self.raise_event('add_to_cart', product=self._product)

    def view_btn_click(self, **event_args):
        self.raise_event('view_product', product=self._product)
