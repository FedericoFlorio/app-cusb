from ._anvil_designer import ItemTemplate4Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class ItemTemplate4(ItemTemplate4Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def button_1_click(self, **event_args):  # Apre la pagina di modifica del canto
    """This method is called when the button is clicked"""
    open_form("modify",titolo=self.label_1.text)
    pass

  def delete_click(self, **event_args):  # Elimina un canto (dopo opportune conferme)
    """This method is called when the button is clicked"""
    titolo = self.label_1.text
    t = TextBox(placeholder="Inserire il titolo del canto")
    c = alert(content = t,
             title = "Conferma l'eliminazione del canto e tutti i file associati",
             buttons = [("Sì",True),("No",False)])
    if c and t.text == titolo:
      anvil.server.call("del_row_indice",titolo)
      anvil.server.call("del_row_domenica",titolo)
      folder = app_files.app.get(titolo)
      folder.delete()
      open_form("editor")
    elif c:
      alert("Scrivere correttamente il nome del canto (in MAIUSCOLO)")
    pass


