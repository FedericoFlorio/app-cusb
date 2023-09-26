from ._anvil_designer import editorTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class editor(editorTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    ind = anvil.server.call('get_indice')
    self.lista.items = ind
    anvil.users.login_with_form()
    self.modo.items = ["M","m"]
    self.modo.selected_value = None
    self.tonalita.items = ["DO","REb","RE","MIb","MI","FA","FA#","SOL","LAb","LA","SIb","SI"]
    self.tonalita.selected_value = None

    # Any code you write here will run before the form opens.

  def get_title(self):
    f = self.carica.file
    if f != None:
      titolo = f.name
      titolo = titolo.upper().replace(".TXT","")
      return titolo
  
  def nuovo_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.nuovo.visible = False
    self.crea.visible = True
    self.carica.visible = True
    pass

  def crea_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.crea.visible = False
    self.carica.visible = False
    self.nuovo_titolo.visible = True
    self.crea_OK.visible = True
    pass

  def carica_change(self, file, **event_args):
    """This method is called when a new file is loaded into this FileLoader"""
    titolo = self.get_title()
    
    rows = anvil.server.call('get_indice')
    es = False
    for canto in rows:
      if canto["titolo"] == titolo:
        es = True
        alert("Nome canto non valido: il canto esiste già")

    if es == False:
      self.label_1.visible = True
      self.label_tonalita.visible = True
      self.label_modo.visible = True
      self.tonalita.visible = True
      self.modo.visible = True
      self.carica_OK.visible = True
    else:
      open_form("editor")

    pass

  def carica_OK_click(self, **event_args):
    """This method is called when the button is clicked"""
    titolo = self.get_title()
    tonalita = self.tonalita.items.index(self.tonalita.selected_value)
    modo = self.modo.selected_value
    
    app_files.app.create_folder(titolo)
    folder = app_files.app.get(titolo)
    nuovo_file = folder.create_file(titolo+".txt",self.carica.file)
    nr = anvil.server.call('new_row_indice',titolo,tonalita,modo)

    open_form("editor")
    pass

  def crea_OK_click(self, **event_args):
    """This method is called when the button is clicked"""
    titolo = self.nuovo_titolo.text.upper()
    rows = anvil.server.call('get_indice')
    es = False
    for canto in rows:
      if canto["titolo"] == titolo:
        es = True
        alert("Nome canto non valido: il canto esiste già")

    if es == False:
      open_form("new_song",titolo=titolo)
    else:
      open_form("editor")
    pass
