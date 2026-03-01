"""
OrdersForm  –  My Orders page
================================
Components:
  - orders_panel : ColumnPanel
  - back_btn     : Button  ("← Home")
"""
from ._anvil_designer import OrdersFormTemplate
from anvil import *
import anvil.server

from . import Globals


class OrdersForm(OrdersFormTemplate):
    def __init__(self, **properties):
        if not Globals.current_user:
            open_form('LoginForm', next_form='HomeForm')
            return
        self.init_components(**properties)
        self._load()

    def _load(self):
        orders = anvil.server.call('get_my_orders', Globals.current_user['id'])
        self.orders_panel.clear()
        if not orders:
            self.orders_panel.add_component(Label(text="You have no orders yet."))
            return

        for o in orders:
            panel = ColumnPanel()
            date_str = str(o.get('order_date', ''))[:10]
            panel.add_component(Label(
                text=f"Order #{o['id']}  |  {date_str}  |  {o.get('status','').title()}",
                bold=True
            ))
            panel.add_component(Label(text=f"Total: ₹{o.get('order_total', 0):.2f}"))
            for item in o.get('items', []):
                prod = item.get('product', {})
                panel.add_component(Label(
                    text=f"  • {prod.get('name','?')}  ×{item['quantity']}  @ ₹{item['price']:.2f}"
                ))
            panel.add_component(Spacer(height=12))
            self.orders_panel.add_component(panel)

    def back_btn_click(self, **event_args):
        open_form('HomeForm')
