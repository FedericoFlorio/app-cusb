from ._anvil_designer import canti_domenica_editorTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class canti_domenica_editor(canti_domenica_editorTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    domenica = anvil.server.call("get_domenica")
    ind = anvil.server.call('get_indice')
    self.lista.items = ind
    
    # Any code you write here will run before the form opens.

  def reset_click(self, **event_args):
    """This method is called when the button is clicked"""
    c = confirm(title="Sicuro di voler cancellare tutti i canti della domenica?",
                buttons=[("Sì",True),("No",False)])
    if c:
      anvil.server.call("reset_domenica")
    pass

  def avanti_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.ins.visible = True
    self.domenica.visible = True
    self.salva.visible = True
    dom = anvil.server.call("get_domenica")
    for i in dom:
      anvil.server.call("num_domenica",i["titolo"],0)
    self.domenica.items = dom
    pass

  def salva_click(self, **event_args):
    """This method is called when the button is clicked"""
    lista = []
    items = self.domenica.items
    for item in items:
      tit = item["titolo"]
      ton = item["ton"]
      num = item["num"]
      lista.append([tit.text,ton.selected_value,num.selected_value])
    if anvil.server.call("check_domenica",lista):
      alert("Check OK")
      # anvil.server.call("reset_domenica")
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



  

