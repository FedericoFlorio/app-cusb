from ._anvil_designer import canti_domenicaTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import transposer_module as tr

class canti_domenica(canti_domenicaTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    global text
    global chords
    # domenica = anvil.server.call("get_domenica")

    # for canto in domenica:
    #   titolo = canto['titolo']
    #   tonalita = canto['tonalita']
    #   tonalita_0 = canto['tonalita_originale']
    #   modo = canto['modo']
    #   folder = app_files.app.get(titolo)
    #   f = folder.get(titolo+".txt")
    #   f_content = f.get_bytes()
      
    #   song = f_content.decode('utf-8')

    #   if tonalita != tonalita_0:
    #     transposer = tr.Transposer(tonalita_0,modo)
    #     encoded = transposer.convert(song,(tonalita-tonalita_0)%12)
    #   else:
    #     encoded = song
      
    #   output = self.display(encoded)
    #   testo = output[0]
    #   accordi = output[1]
    #   text += testo + "&nbsp;\n&nbsp;\n&nbsp;\n"
    #   chords += accordi + "&nbsp;\n&nbsp;\n&nbsp;\n"

    folder = app_files.app.get("00_CANTI_DOMENICA")
    f_testi = folder.get("TESTI.txt")
    f_accordi = folder.get("ACCORDI.txt")
    testi_content = f_testi.get_bytes()
    accordi_content = f_accordi.get_bytes()
    text = testi_content.decode('utf-8')
    chords = accordi_content.decode('utf-8')
    
    self.testo.font = "Arial"
    self.testo.font_size = 14
    self.testo.content = text

    # Any code you write here will run before the form opens.
  
  def accordi_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    if self.accordi.checked:
      self.testo.font = "Roboto Mono"
      self.testo.font_size = 12
      self.testo.content = chords
    else:
      self.testo.font = "Arial"
      self.testo.font_size = 14
      self.testo.content = text
    pass

  def home_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("main")
    pass

  def font_minus_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.testo.font_size -= 1
    pass

  def font_plus_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.testo.font_size += 1
    pass
