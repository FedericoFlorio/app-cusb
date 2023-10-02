from ._anvil_designer import ItemTemplate7Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class ItemTemplate7(ItemTemplate7Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    dom = anvil.server.call("get_domenica")
    self.num.items = [str(i) for i in range(len(dom)+1)]
    self.num.selected_value = 0
    self.tonalita.items = ["DO","REb","RE","MIb","MI","FA","FA#","SOL","LAb","LA","SIb","SI"]
    ton = app_tables.canti_domenica.search(titolo=self.titolo.text)
    ind = anvil.server.call('get_indice')
    for row in ind:
      if row["titolo"] == self.titolo.text:
        self.tonalita.selected_value = row["tonalita"]
        for i in ton:
          i["tonalita"] = row["tonalita"]
    
    # Any code you write here will run before the form opens.
