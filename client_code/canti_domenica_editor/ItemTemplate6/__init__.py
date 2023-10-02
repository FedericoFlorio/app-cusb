from ._anvil_designer import ItemTemplate6Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class ItemTemplate6(ItemTemplate6Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    domenica = anvil.server.call("get_domenica")
    dom = [i["titolo"] for i in domenica]
    if self.titolo.text in dom:
      self.titolo.background = "theme:Primary Container"
      self.background = "theme:Primary Container"
      self.add.icon = "fa:minus"

    # Any code you write here will run before the form opens.

  def add_click(self, **event_args):
    """This method is called when the button is clicked"""
    if self.add.icon == "fa:plus":
      self.titolo.background = "theme:Primary Container"
      self.background = "theme:Primary Container"
      self.add.icon = "fa:minus"
      anvil.server.call("new_row_domenica",self.titolo.text,0)
    else:
      self.titolo.background = "theme:On Primary"
      self.background = "theme:On Primary"
      self.add.icon = "fa:plus"
      anvil.server.call("del_row_domenica",self.titolo.text)
    pass

