"""
RegisterForm  –  Registration page
====================================
Components:
  - name_box          : TextBox
  - email_box         : TextBox
  - password_box      : TextBox  (hide_text=True)
  - confirm_box       : TextBox  (hide_text=True)
  - phone_box         : TextBox  (optional)
  - register_btn      : Button   ("Create Account")
  - login_link        : Link     ("Already have an account? Log In")
  - error_label       : Label    (visible=False initially)
"""
from ._anvil_designer import RegisterFormTemplate
from anvil import *
import anvil.server

from . import Globals


class RegisterForm(RegisterFormTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
        self.error_label.visible = False

    def register_btn_click(self, **event_args):
        name     = (self.name_box.text or '').strip()
        email    = (self.email_box.text or '').strip()
        password = self.password_box.text or ''
        confirm  = self.confirm_box.text or ''
        phone    = (self.phone_box.text or '').strip()

        if password != confirm:
            self._show_error("Passwords do not match.")
            return

        ok, err = anvil.server.call('register_user', name, email, password, phone)
        if ok:
            Notification("Account created! Please log in.", style="success").show()
            open_form('LoginForm')
        else:
            self._show_error(err or "Registration failed.")

    def login_link_click(self, **event_args):
        open_form('LoginForm')

    def _show_error(self, msg):
        self.error_label.text    = msg
        self.error_label.visible = True
