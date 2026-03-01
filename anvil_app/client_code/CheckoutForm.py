"""
CheckoutForm  –  Checkout / shipping details page
===================================================
Components:
  - full_name_box    : TextBox
  - phone_box        : TextBox
  - address_box      : TextBox  (multiline)
  - city_box         : TextBox
  - state_box        : TextBox
  - pincode_box      : TextBox
  - note_box         : TextBox  (optional)
  - payment_label    : Label    ("Cash on Delivery")
  - order_summary    : ColumnPanel
  - total_label      : Label
  - place_order_btn  : Button   ("Place Order")
  - back_btn         : Button   ("← Back to Cart")
  - error_label      : Label    (visible=False)
"""
from ._anvil_designer import CheckoutFormTemplate
from anvil import *
import anvil.server

from . import Globals


class CheckoutForm(CheckoutFormTemplate):
    def __init__(self, **properties):
        if not Globals.current_user:
            open_form('LoginForm', next_form='CartForm')
            return
        self.init_components(**properties)
        self.error_label.visible = False
        self._render_summary()
        # Pre-fill user details
        u = Globals.current_user
        self.full_name_box.text = u.get('name', '')
        self.phone_box.text     = u.get('phone', '')

    def _render_summary(self):
        self.order_summary.clear()
        cart  = Globals.cart
        total = 0
        self._cart_items = []
        for pid, qty in cart.items():
            p = anvil.server.call('get_product', pid)
            if not p:
                continue
            subtotal = p['price'] * qty
            total   += subtotal
            self._cart_items.append({'product_id': pid, 'quantity': qty, 'price': p['price']})
            self.order_summary.add_component(
                Label(text=f"{p['name']}  ×{qty}  ₹{subtotal:.2f}")
            )
        self.total_label.text = f"Total: ₹{total:.2f}"

    def place_order_btn_click(self, **event_args):
        shipping = {
            'full_name':       (self.full_name_box.text or '').strip(),
            'phone':           (self.phone_box.text or '').strip(),
            'address':         (self.address_box.text or '').strip(),
            'city':            (self.city_box.text or '').strip(),
            'state':           (self.state_box.text or '').strip(),
            'pincode':         (self.pincode_box.text or '').strip(),
            'note':            (self.note_box.text or '').strip(),
            'payment_method':  'Cash on Delivery',
        }
        if not shipping['full_name'] or not shipping['address'] or not shipping['city']:
            self._show_error("Please fill in all required shipping fields.")
            return

        try:
            order_id = anvil.server.call(
                'place_order',
                Globals.current_user['id'],
                self._cart_items,
                shipping
            )
        except Exception as ex:
            self._show_error(f"Could not place order: {ex}")
            return

        Globals.cart = {}
        Notification(f"Order #{order_id} placed! You will pay on delivery.", style="success").show()
        open_form('OrderConfirmationForm', order_id=order_id)

    def back_btn_click(self, **event_args):
        open_form('CartForm')

    def _show_error(self, msg):
        self.error_label.text    = msg
        self.error_label.visible = True
