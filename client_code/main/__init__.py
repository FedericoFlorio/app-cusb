from ._anvil_designer import mainTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users

class main(mainTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  # def button_login_click(self, **event_args):
  #   """This method is called when the button is clicked"""
  #   anvil.users.login_with_form()
  #   pass

  def button_editor_click(self, **event_args):
    """This method is called when the button is clicked"""
    if anvil.users.login_with_form(allow_cancel=True) is not None:
      open_form("editor")
    pass

  def button_libretto_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("libretto")
    pass

  def button_canti_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("canti_domenica")
    pass




