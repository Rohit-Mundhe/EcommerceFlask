"""
Globals  –  Shared client-side state
======================================
Import this module in every Form to access shared state:
  from . import Globals

  Globals.current_user   – dict or None
  Globals.cart           – {product_id: quantity}
"""

current_user = None   # dict: {id, email, name, phone}  or  None
cart = {}             # {product_id (str/row-id): quantity (int)}
