from ._anvil_designer import cantoTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import transposer_module as tr

class canto(cantoTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    if "titolo" in properties:
      global titolo
      titolo = properties["titolo"]

    self.titolo.text = titolo

    global ton
    ton = {"M" : ["DO","REb","RE","MIb","MI","FA","FA#","SOL","LAb","LA","SIb","SI"],
           "m" : ["DO","DO#","RE","MIb","MI","FA","FA#","SOL","SOL#","LA","SIb","SI"]}
    mod = {"M":"maggiore", "m":"minore"}
    ind = anvil.server.call('get_indice')
    for row in ind:
      if row['titolo'] == titolo:
        tr.ton_orig = row['tonalita']
        tr.ton = tr.ton_orig
        tr.mode = row['modo']
        
    self.tonalita.text = ton[tr.mode][tr.ton]
    self.modo.text = mod[tr.mode]
    
    folder = app_files.app.get(titolo)
    f = folder.get(titolo+".txt")
    f_content = f.get_bytes()
    global text
    tr.testo_base = f_content.decode('utf-8')
    tr.testo = tr.testo_base
    
    disp = self.display(tr.testo)
    testo = disp[0]
    accordi = disp[1]

    self.testo.font = "Arial"
    self.testo.font_size = 18
    self.testo.content = testo

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
      self.tonalita.visible = True
      self.modo.visible = True
      self.plus.visible = True
      self.minus.visible = True
      self.testo.font = "Roboto Mono"
      self.testo.font_size = 14
      self.testo.content = self.display(tr.testo)[1]
    else:
      self.tonalita.visible = False
      self.modo.visible = False
      self.plus.visible = False
      self.minus.visible = False
      self.testo.font = "Arial"
      self.testo.font_size = 18
      self.testo.content = self.display(tr.testo)[0]
    pass

  def font_minus_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.testo.font_size -= 1
    pass

  def font_plus_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.testo.font_size += 1
    pass

  def plus_click(self, **event_args):
    """This method is called when the button is clicked"""
    tr.ton = (tr.ton + 1)%12
    shift = (tr.ton-tr.ton_orig)%12
    transposer = tr.Transposer(tr.ton_orig,tr.mode)
    tr.testo = transposer.convert(tr.testo_base,shift)
    self.tonalita.text = tr.newTon(tr.ton,tr.mode)
    self.testo.content = self.display(tr.testo)[1]
    pass

  def minus_click(self, **event_args):
    """This method is called when the button is clicked"""
    tr.ton = (tr.ton - 1)%12
    shift = (tr.ton-tr.ton_orig)%12
    transposer = tr.Transposer(tr.ton_orig,tr.mode)
    tr.testo = transposer.convert(tr.testo_base,shift)
    self.tonalita.text = tr.newTon(tr.ton,tr.mode)
    self.testo.content = self.display(tr.testo)[1]
    pass

  def home_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("main")
    pass

  def back_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("libretto")
    pass