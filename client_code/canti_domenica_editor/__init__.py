from ._anvil_designer import canti_domenica_editorTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import module

class canti_domenica_editor(canti_domenica_editorTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    domenica = anvil.server.call("get_domenica")
    indice = anvil.server.call('get_indice')
    indice_titoli = [indice[i]["titolo"] for i in range(len(indice))]
    self.lista.items = indice

    module.domenica.clear()
    for row in domenica:
      if row['titolo'] in indice_titoli:
        module.domenica.append({"titolo": row["titolo"],
                                "tonalita": row["tonalita"],
                                "tonalita_originale": row["tonalita"],
                                "modo": row["modo"],
                                "num": row["num"]})
      else:
        anvil.server.call('del_row_domenica',row["titolo"])

    self.domenica.items = module.domenica
    
    # Any code you write here will run before the form opens.

  def reset_click(self, **event_args):
    """This method is called when the button is clicked"""
    c = confirm(title="Sicuro di voler cancellare tutti i canti della domenica?",
                buttons=[("Sì",True),("No",False)])
    if c:
      anvil.server.call("reset_domenica")
    pass

  def salva_click(self, **event_args):
    """This method is called when the button is clicked"""
    a = module.check_domenica(module.domenica)
    domenica = a[1]
    
    if a[0]:
      anvil.server.call("reset_domenica")
      for canto in domenica:
        print(canto)
        anvil.server.call("new_row_domenica",canto["titolo"],canto["tonalita"],canto["tonalita_originale"],canto["modo"],canto["num"])
      open_form("editor")
    else:
      alert("Ordinare correttamente i canti")
    pass

  def back_click(self, **event_args):
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

  def refresh(self):
    self.refresh_data_bindings()
    self.domenica.items = module.domenica