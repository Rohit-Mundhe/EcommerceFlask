"""
LoginForm  –  Login page
=========================
Components:
  - email_box     : TextBox  (placeholder "Email")
  - password_box  : TextBox  (hide_text=True)
  - login_btn     : Button   ("Log In")
  - register_link : Link     ("Don't have an account? Register")
  - error_label   : Label    (visible=False, initially)
"""
from ._anvil_designer import LoginFormTemplate
from anvil import *
import anvil.server

from . import Globals


class LoginForm(LoginFormTemplate):
    def __init__(self, next_form=None, **properties):
        self._next_form = next_form or 'HomeForm'
        self.init_components(**properties)
        self.error_label.visible = False

    def login_btn_click(self, **event_args):
        email    = (self.email_box.text or '').strip()
        password = self.password_box.text or ''

        if not email or not password:
            self._show_error("Please enter email and password.")
            return

        user = anvil.server.call('login_user', email, password)
        if user:
            Globals.current_user = user
            Notification(f"Welcome back, {user.get('name', 'User')}!", style="success").show()
            open_form(self._next_form)
        else:
            self._show_error("Invalid email or password.")

    def register_link_click(self, **event_args):
        open_form('RegisterForm')

    def _show_error(self, msg):
        self.error_label.text    = msg
        self.error_label.visible = True
