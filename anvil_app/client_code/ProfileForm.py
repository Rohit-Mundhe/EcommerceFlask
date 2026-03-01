"""
ProfileForm  –  User profile / edit page
==========================================
Components:
  - name_box      : TextBox
  - phone_box     : TextBox
  - email_label   : Label   (read-only)
  - joined_label  : Label   (read-only)
  - save_btn      : Button  ("Save Changes")
  - back_btn      : Button  ("← Home")
  - message_label : Label   (visible=False)
"""
from ._anvil_designer import ProfileFormTemplate
from anvil import *
import anvil.server

from . import Globals


class ProfileForm(ProfileFormTemplate):
    def __init__(self, **properties):
        if not Globals.current_user:
            open_form('LoginForm', next_form='HomeForm')
            return
        self.init_components(**properties)
        self.message_label.visible = False
        self._load()

    def _load(self):
        u = anvil.server.call('get_user_by_id', Globals.current_user['id'])
        if not u:
            return
        self.name_box.text    = u.get('name', '')
        self.phone_box.text   = u.get('phone', '')
        self.email_label.text = u.get('email', '')
        joined = str(u.get('created_at', ''))[:10]
        self.joined_label.text = f"Member since: {joined}"

    def save_btn_click(self, **event_args):
        name  = (self.name_box.text or '').strip()
        phone = (self.phone_box.text or '').strip()
        ok, err = anvil.server.call(
            'update_profile', Globals.current_user['id'], name, phone
        )
        if ok:
            Globals.current_user['name']  = name
            Globals.current_user['phone'] = phone
            self.message_label.text       = "Profile updated successfully."
            self.message_label.foreground = "green"
        else:
            self.message_label.text       = err or "Update failed."
            self.message_label.foreground = "red"
        self.message_label.visible = True

    def back_btn_click(self, **event_args):
        open_form('HomeForm')
