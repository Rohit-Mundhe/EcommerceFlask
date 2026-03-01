"""
OrderConfirmationForm  –  Order placed success page
=====================================================
Components:
  - order_id_label   : Label
  - status_label     : Label
  - items_panel      : ColumnPanel
  - total_label      : Label
  - shipping_label   : Label  (multiline)
  - home_btn         : Button ("Continue Shopping")
  - orders_btn       : Button ("View My Orders")
"""
from ._anvil_designer import OrderConfirmationFormTemplate
from anvil import *
import anvil.server

from . import Globals


class OrderConfirmationForm(OrderConfirmationFormTemplate):
    def __init__(self, order_id=None, **properties):
        self._order_id = order_id
        self.init_components(**properties)
        self._load()

    def _load(self):
        if not Globals.current_user:
            open_form('HomeForm')
            return
        order = anvil.server.call('get_order', self._order_id, Globals.current_user['id'])
        if not order:
            open_form('HomeForm')
            return

        self.order_id_label.text = f"Order #{order['id']}"
        self.status_label.text   = f"Status: {order.get('status', 'confirmed').title()}"
        self.total_label.text    = f"Total: ₹{order.get('total_amount', 0):.2f}"
        self.shipping_label.text = (
            f"{order.get('shipping_name','')} | {order.get('shipping_phone','')}\n"
            f"{order.get('shipping_address','')}, {order.get('shipping_city','')}, "
            f"{order.get('shipping_state','')} – {order.get('shipping_pincode','')}"
        )

        self.items_panel.clear()
        for item in order.get('items', []):
            prod = item.get('product', {})
            self.items_panel.add_component(
                Label(text=f"{prod.get('name','?')}  ×{item['quantity']}  ₹{item['price'] * item['quantity']:.2f}")
            )

    def home_btn_click(self, **event_args):
        open_form('HomeForm')

    def orders_btn_click(self, **event_args):
        open_form('OrdersForm')
