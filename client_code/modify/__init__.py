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
    self.editor.font = "Roboto Mono"
    self.editor.text = text

    # Cerca la tonalità e il modo nell'indice e lo inserisce nei DropDown
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
      # Salvataggio del nuovo file e eliminazione del vecchio
      titolo = self.titolo.text.upper()
      folder = app_files.app.get(titolo_vecchio)
      old_file = folder.get(titolo_vecchio+".txt")
      old_file.delete()
      new_file = folder.create_file(titolo+".txt",self.editor.text)

      # Se il titolo è stato cambiato, corregge l'indice e la cartella drive (trasferendo tutti i file)
      if titolo != titolo_vecchio:
        new_folder = app_files.app.create_folder(titolo)
        for file in folder.list_files():
          new_folder.create_file(file["title"].replace(titolo_vecchio,titolo),file)
          file.delete()
        folder.delete()
      
      tonalita = self.tonalita.items.index(self.tonalita.selected_value)
      modo = self.modo.selected_value

      tonalita_nuova = self.tonalita.items.index(self.tonalita.selected_value)
      modo_nuovo = self.modo.selected_value
      anvil.server.call('mod_row_indice',titolo_vecchio,titolo,tonalita_nuova,modo_nuovo)
      
      open_form("editor")
    pass

  def annulla_click(self, **event_args):
    """This method is called when the button is clicked"""
    c = confirm(title="Sicuro di voler uscire? Tutte le modifiche andranno perse",
               buttons=[("Sì",True),("No",False)])
    if c:
      open_form("editor")
    pass

  def home_click(self, **event_args):
    """This method is called when the button is clicked"""
    c = confirm(title="Sicuro di voler uscire? Tutte le modifiche andranno perse",
               buttons=[("Sì",True),("No",False)])
    if c:
      open_form("main")
    pass

  def back_click(self, **event_args):
    """This method is called when the button is clicked"""
    c = confirm(title="Sicuro di voler uscire? Tutte le modifiche andranno perse",
               buttons=[("Sì",True),("No",False)])
    if c:
      open_form("editor")
    pass



