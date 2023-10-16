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
    text = ""
    global chords
    chords = ""
    domenica = anvil.server.call("get_domenica")

    for canto in domenica:
      titolo = canto['titolo']
      tonalita = canto['tonalita']
      tonalita_0 = canto['tonalita_originale']
      modo = canto['modo']
      folder = app_files.app.get(titolo)
      f = folder.get(titolo+".txt")
      f_content = f.get_bytes()
      
      song = f_content.decode('utf-8')

      if tonalita != tonalita_0:
        transposer = tr.Transposer(tonalita_0,modo)
        encoded = transposer.convert(song,(tonalita-tonalita_0)%12)
      else:
        encoded = song
      
      output = self.display(encoded)
      testo = output[0]
      accordi = output[1]
      text += testo + "&nbsp;\n&nbsp;\n&nbsp;\n"
      chords += accordi + "&nbsp;\n&nbsp;\n&nbsp;\n"

    self.testo.font = "Arial"
    self.testo.font_size = 14
    self.testo.content = text

    # Any code you write here will run before the form opens.

  def display(self,text):
    lines = text.split("\n")
    testo = ""
    accordi = ""
    flag = False
    for line in lines:
      s = line.split()[0]
      if s == "\head":
        testo += ("## " + line.replace("\head ","") + "\n\n")
        accordi += ("## " + line.replace("\head ","") + "\n\n")
      elif s == "\intro":
        accordi += ("Intro:  **" + line.replace("\intro ","") + "**" + "\n")
      elif s == "\start":
        accordi += "\n"
      elif s == "\c":
        if flag:
          accordi += "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        accordi += ("**" + line.replace("\c ","").replace(" ","&nbsp;") + "**\n")
      elif s == "\l":
        if flag:
          testo += "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
          accordi += "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        testo += (line.replace("\l ","") + "\n")
        accordi += (line.replace("\l ","") + "\n")
      elif s == "$":
        testo += "&nbsp;\n"
        accordi += "&nbsp;\n"
      elif s == "$$":
        flag = not flag
        testo += "&nbsp;\n"
        accordi += "&nbsp;\n"

    return (testo, accordi)
  
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
