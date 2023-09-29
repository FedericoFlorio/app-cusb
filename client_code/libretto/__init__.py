from ._anvil_designer import librettoTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class libretto(librettoTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    ind = anvil.server.call('get_indice')
    self.lista.items = ind

    # Any code you write here will run before the form opens.

  def home_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("main")
    pass

