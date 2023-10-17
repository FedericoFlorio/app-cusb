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
    # Visualizzazione indice
    ind = anvil.server.call('get_indice')
    self.lista.items = ind
    
    # Creazione tasti
    self.modo.items = ["M","m"]
    self.modo.selected_value = None
    self.tonalita.items = ["DO","REb","RE","MIb","MI","FA","FA#","SOL","LAb","LA","SIb","SI"]
    self.tonalita.selected_value = None
  
      # Any code you write here will run before the form opens.

  def get_title(self):  # Estrae il titolo di un file caricato
    f = self.carica.file
    if f != None:
      titolo = f.name
      titolo = titolo.upper().replace(".TXT","")
      return titolo
  
  def nuovo_click(self, **event_args):  # Rivela i pulsanti per un nuovo file
    """This method is called when the button is clicked"""
    self.nuovo.visible = False
    self.crea.visible = True
    self.carica.visible = True
    pass

  def crea_click(self, **event_args): # Rivela le opzioni per creare un nuovo file
    """This method is called when the button is clicked"""
    self.crea.visible = False
    self.carica.visible = False
    self.nuovo_titolo.visible = True
    self.crea_OK.visible = True
    pass

  def carica_change(self, file, **event_args): # Rivela le opzioni per caricare un nuovo file e controlla il file caricato
    """This method is called when a new file is loaded into this FileLoader"""
    if self.carica.file is not None:
      titolo = self.get_title()
      # Controllo sull'esistenza del canto
      rows = anvil.server.call('get_indice')
      es = False
      for canto in rows:
        if canto["titolo"] == titolo:
          es = True
          alert("Nome canto non valido: il canto esiste già")
  
      # Controllo sul formato del file
      file_content = self.carica.file.get_bytes()
      text = file_content.decode('utf-8').split("\n")
      # with open(titolo+".txt","r") as file:
      #   text = file.readlines()
      err = anvil.server.call('check_format',text)
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
  
      # Mostra le opzioni per tonalità e modo
      if es==False and err==0:
        self.label_1.visible = True
        self.label_tonalita.visible = True
        self.label_modo.visible = True
        self.tonalita.visible = True
        self.modo.visible = True
        self.carica_OK.visible = True
      else:
        open_form("editor")

    pass

  def carica_OK_click(self, **event_args): # Carica il nuovo file
    """This method is called when the button is clicked"""
    titolo = self.get_title()
    tonalita = self.tonalita.items.index(self.tonalita.selected_value)
    modo = self.modo.selected_value

    # Creazione nuova cartella Drive e caricamento file
    app_files.app.create_folder(titolo)
    folder = app_files.app.get(titolo)
    nuovo_file = folder.create_file(titolo+".txt",self.carica.file)
    nr = anvil.server.call('new_row_indice',titolo,tonalita,modo)

    open_form("editor")
    pass

  def crea_OK_click(self, **event_args): # Apre l'editor per un nuovo canto
    """This method is called when the button is clicked"""
    titolo = self.nuovo_titolo.text.upper()

    # Controllo esistenza canto
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

  def home_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("main")
    pass

  def canti_domenica_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("canti_domenica_editor")
    pass
