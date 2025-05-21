from ._anvil_designer import mainTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
### NUOVO
import anvil.js
###

class main(mainTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    ### NUOVO
    # Ritarda il binding dei pulsanti di 100 ms per assicurarsi che il DOM sia pronto
    anvil.js.window.setTimeout(self.setup_event_handlers, 100)
    ###

    # Any code you write here will run before the form opens.

  # def button_login_click(self, **event_args):
  #   """This method is called when the button is clicked"""
  #   anvil.users.login_with_form()
  #   pass

  ### NUOVO
  def setup_event_handlers(self, *args):
    # Ora il DOM è pronto, questi funzionano
    anvil.js.window.document.querySelector('[anvil-id="button_libretto"]').addEventListener(
      "click", lambda e: self.button_libretto_click()
    )
    anvil.js.window.document.querySelector('[anvil-id="button_canti"]').addEventListener(
      "click", lambda e: self.button_canti_click()
    )
    anvil.js.window.document.querySelector('[anvil-id="button_editor"]').addEventListener(
      "click", lambda e: self.button_editor_click()
    )
    ###

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

