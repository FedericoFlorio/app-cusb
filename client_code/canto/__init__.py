from ._anvil_designer import cantoTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class canto(cantoTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    if "titolo" in properties:
      global titolo
      titolo = properties["titolo"]

    self.titolo.text = titolo

    ton = ["DO","REb","RE","MIb","MI","FA","FA#","SOL","LAb","LA","SIb","SI"]
    mod = {"M":"maggiore", "m":"minore"}
    ind = anvil.server.call('get_indice')
    for row in ind:
      if row['titolo'] == titolo:
        tonalita = ton[row['tonalita']]
        modo = mod[row['modo']]
    self.tonalita.text = tonalita
    self.modo.text = modo
    
    folder = app_files.app.get(titolo)
    f = folder.get(titolo+".txt")
    f_content = f.get_bytes()
    global text
    text = f_content.decode('utf-8')

    lines = text.split("\n")
    global testo
    global accordi
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

    self.testo.font = "Arial"
    self.testo.font_size = 18
    self.testo.content = testo

    # Any code you write here will run before the form opens.

  def accordi_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    if self.accordi.checked:
      self.tonalita.visible = True
      self.modo.visible = True
      self.plus.visible = True
      self.minus.visible = True
      self.testo.font = "Roboto Mono"
      self.testo.font_size = 14
      self.testo.content = accordi
    else:
      self.tonalita.visible = False
      self.modo.visible = False
      self.plus.visible = False
      self.minus.visible = False
      self.testo.font = "Arial"
      self.testo.font_size = 18
      self.testo.content = testo
    pass

  def home_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("main")
    pass

  def back_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("libretto")
    pass

  def font_minus_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.testo.font_size -= 1
    pass

  def font_plus_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.testo.font_size += 1
    pass





