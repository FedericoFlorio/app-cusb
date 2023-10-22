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
from .. import transposer_module as tr

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
      module.domenica = []
      for i in self.lista.get_components():
        i.update()
      self.refresh_data_bindings()
      self.domenica.items = module.domenica
    pass

  def salva_click(self, **event_args):
    """This method is called when the button is clicked"""
    a = module.check_domenica(module.domenica)
    domenica = a[1]
    text = ""
    chords = ""
    if a[0]:
      anvil.server.call("reset_domenica")
      domenica_table = anvil.server.call("get_domenica")
      print("entrato if a[0]")
      
      for canto in domenica:
        print("entrato for canto in domenica")
        anvil.server.call("new_row_domenica",canto["titolo"],canto["tonalita"],canto["tonalita_originale"],canto["modo"],canto["num"])
        titolo = canto['titolo']
        tonalita = canto['tonalita']
        tonalita_0 = canto['tonalita_originale']
        modo = canto['modo']
        folder = app_files.app.get(titolo)
        f = folder.get(titolo+".txt")
        f_content = f.get_bytes()
        song = f_content.decode('utf-8')
        print("aaa" + song)

        if tonalita != tonalita_0:
          transposer = tr.Transposer(tonalita_0,modo)
          encoded = transposer.convert(song,(tonalita-tonalita_0)%12)
        else:
          encoded = song
        
        output = module.display(encoded)
        testo = output[0]
        accordi = output[1]
        text += testo + "&nbsp;\n&nbsp;\n&nbsp;\n"
        chords += accordi + "&nbsp;\n&nbsp;\n&nbsp;\n"

      print(text)
      print("\n\n\n")
      print(chords)
      folder = app_files.app.get("00_CANTI_DOMENICA")
      f_testo = folder.get("TESTI.txt")
      f_accordi = folder.get("ACCORDI.txt")
      f_testo.delete()
      f_accordi.delete()
      nuovo_testi = folder.create_file("TESTI.txt",text)
      nuovo_accordi = folder.create_file("ACCORDI.txt",chords)
      
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