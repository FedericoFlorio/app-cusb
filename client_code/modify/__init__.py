from ._anvil_designer import modifyTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class modify(modifyTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    if "titolo" in properties:
      titolo = properties["titolo"]

    self.titolo.text = titolo
    self.modo.items = ["M","m"]
    self.modo.selected_value = None
    self.tonalita.items = ["DO","REb","RE","MIb","MI","FA","FA#","SOL","LAb","LA","SIb","SI"]
    self.tonalita.selected_value = None

    # Any code you write here will run before the form opens.

  def salva_click(self, **event_args): # Controlla tutto e salva il file
    """This method is called when the button is clicked"""
    # Controllo formato del file
    err = anvil.server.call('check_format',self.editor.text)
    if err==1:
      alert("Errore nel titolo")
    elif err==2:
      alert("Errore nell'intro")
    elif err==3:
      alert("Errore nel begin")
    elif err==4:
      alert("Errore nell'end")
    elif err==5:
      alert("Errore nel corpo")

    # Controllo tonalità e modo
    if self.tonalita.selected_value == None or self.modo.selected_value == None:
      alert("Inserire tonalità e modo")

    # Creazione nuovo file
    if err==0:
      titolo = self.titolo.text
      app_files.app.create_folder(titolo)
      folder = app_files.app.get(titolo)
      nuovo_file = folder.create_file(titolo+".txt",self.editor.text)
      tonalita = self.tonalita.items.index(self.tonalita.selected_value)
      modo = self.modo.selected_value
      nr = anvil.server.call('new_row_indice',titolo,tonalita,modo)
      open_form("editor")
    pass
