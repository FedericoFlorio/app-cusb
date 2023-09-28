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
      global titolo_vecchio
      titolo_vecchio = properties["titolo"]

    self.titolo.text = titolo_vecchio
    self.modo.items = ["M","m"]
    self.modo.selected_value = None
    self.tonalita.items = ["DO","REb","RE","MIb","MI","FA","FA#","SOL","LAb","LA","SIb","SI"]
    self.tonalita.selected_value = None

    # Cerca il testo nel drive e lo inserisce nell'editor
    folder = app_files.app.get(titolo_vecchio)
    f = folder.get(titolo_vecchio+".txt")
    f_content = f.get_bytes()
    text = f_content.decode('utf-8')
    self.editor.text = text

    ind = anvil.server.call('get_indice')
    for row in ind:
      if row['titolo'] == titolo_vecchio:
        self.tonalita.selected_value = self.tonalita.items[row['tonalita']]
        self.modo.selected_value = row['modo']
    

    # Any code you write here will run before the form opens.

  def salva_click(self, **event_args): # Controlla tutto e salva il file
    """This method is called when the button is clicked"""
    # Controllo formato del file
    err = anvil.server.call('check_format',self.editor.text.split("\n"))
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

    # Salvataggio file
    if err==0:
      titolo = self.titolo.text
      folder = app_files.app.get(titolo_vecchio)
      # print(titolo_vecchio)
      f = folder.get(titolo_vecchio+".txt")
      f.delete()
      nuovo_file = folder.create_file(titolo+".txt",self.editor.text)
      new_folder = app_files.app.create_folder(titolo)
      # folder.move(new_folder)
      for file in folder.files:
        file.move(new_folder)
      folder.delete()
      
      tonalita = self.tonalita.items.index(self.tonalita.selected_value)
      modo = self.modo.selected_value
      
      ind = anvil.server.call('get_indice')
      for row in ind:
        if row['titolo'] == titolo_vecchio:
          row['tonalita'] = self.tonalita.items.index(self.tonalita.selected_value)
          row['modo'] = self.modo.selected_value
          row['titolo'] = self.titolo.text
      open_form("editor")
    pass
