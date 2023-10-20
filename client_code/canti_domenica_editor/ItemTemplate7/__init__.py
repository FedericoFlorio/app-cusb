from ._anvil_designer import ItemTemplate7Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import module

class ItemTemplate7(ItemTemplate7Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    self.tonalita.items = ["DO","REb","RE","MIb","MI","FA","FA#","SOL","LAb","LA","SIb","SI"]
    self.tonalita.selected_value = self.tonalita.items[self.item["tonalita"]]
    self.num.items = [str(i) for i in range(len(module.domenica)+1)]
    self.num.selected_value = str(self.item["num"])
    
    # Any code you write here will run before the form opens.

  def tonalita_change(self, **event_args):
    """This method is called when an item is selected"""
    for i in range(len(module.domenica)):
      if self.titolo.text == module.domenica[i]["titolo"]:
        module.domenica[i]["tonalita"] = self.tonalita.items.index(self.tonalita.selected_value)
        get_open_form().refresh()
        break
    pass

  def num_change(self, **event_args):
    """This method is called when an item is selected"""
    for i in range(len(module.domenica)):
      if self.titolo.text == module.domenica[i]["titolo"]:
        titolo = module.domenica[i]["titolo"]
        tonalita = module.domenica[i]["tonalita"]
        tonalita_originale = module.domenica[i]["tonalita_originale"]
        modo = module.domenica[i]["modo"]
        num = int(self.num.selected_value)
        module.domenica[i] = {"titolo": titolo,
                              "tonalita": tonalita,
                              "tonalita_originale": tonalita_originale,
                              "modo": modo,
                              "num": num}
        break
    get_open_form().refresh()
    pass


