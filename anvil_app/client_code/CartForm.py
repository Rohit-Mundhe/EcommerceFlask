"""
CartForm  –  Shopping cart page
=================================
Components:
  - cart_panel      : ColumnPanel  (cart rows)
  - total_label     : Label
  - checkout_btn    : Button  ("Proceed to Checkout")
  - clear_btn       : Button  ("Clear Cart")
  - continue_btn    : Button  ("← Continue Shopping")
  - empty_label     : Label   ("Your cart is empty", visible=False)
"""
from ._anvil_designer import CartFormTemplate
from anvil import *
import anvil.server

from . import Globals


class CartForm(CartFormTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
        self._render()

    def _render(self):
        self.cart_panel.clear()
        cart = Globals.cart  # {product_id: quantity}

        if not cart:
            self.empty_label.visible  = True
            self.checkout_btn.enabled = False
            self.total_label.text     = "Total: ₹0.00"
            return

        self.empty_label.visible = False
        total = 0

        for pid, qty in list(cart.items()):
            p = anvil.server.call('get_product', pid)
            if not p:
                continue
            subtotal = p['price'] * qty
            total   += subtotal

            row = ColumnPanel()
            row.add_component(Label(text=p['name'], bold=True))
            row.add_component(Label(text=f"₹{p['price']:.2f} × {qty} = ₹{subtotal:.2f}"))

            minus_btn = Button(text="−", role="outlined-button")
            plus_btn  = Button(text="+", role="outlined-button")
            del_btn   = Button(text="Remove", role="outlined-button")
            minus_btn.set_event_handler('click', lambda **e, p=pid: self._change_qty(p, -1))
            plus_btn.set_event_handler('click',  lambda **e, p=pid: self._change_qty(p, +1))
            del_btn.set_event_handler('click',   lambda **e, p=pid: self._remove(p))

            btn_row = GridPanel()
            btn_row.add_component(minus_btn)
            btn_row.add_component(plus_btn)
            btn_row.add_component(del_btn)
            row.add_component(btn_row)
            self.cart_panel.add_component(row)

        self.total_label.text = f"Total: ₹{total:.2f}"
        self.checkout_btn.enabled = True

    def _change_qty(self, product_id, delta):
        cart = Globals.cart
        new_qty = cart.get(product_id, 0) + delta
        if new_qty <= 0:
            cart.pop(product_id, None)
        else:
            cart[product_id] = new_qty
        Globals.cart = cart
        self._render()

    def _remove(self, product_id):
        Globals.cart.pop(product_id, None)
        self._render()

    def checkout_btn_click(self, **event_args):
        if not Globals.current_user:
            Notification("Please log in to checkout.", style="warning").show()
            open_form('LoginForm', next_form='CartForm')
            return
        open_form('CheckoutForm')

    def clear_btn_click(self, **event_args):
        Globals.cart = {}
        self._render()

    def continue_btn_click(self, **event_args):
        open_form('HomeForm')
