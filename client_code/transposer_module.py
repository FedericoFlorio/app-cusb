import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

ton_orig = 0
ton = 0
mode = ""
testo_base = ""
testo = ""

def newTon(ton,mode):
  tonalita = {"M" : ["DO","REb","RE","MIb","MI","FA","FA#","SOL","LAb","LA","SIb","SI"],
              "m" : ["DO","DO#","RE","MIb","MI","FA","FA#","SOL","SOL#","LA","SIb","SI"]}
  return tonalita[mode][ton]

class Transposer():
  def __init__(self, ton_old, modo):
    self.ton_old = ton_old
    self.modo = modo
    self.shift = 0
    self.ton_new = (self.ton_old + self.shift) % 12
    self.encode = ["\intro", "\outro", "\c"]
    self.join = ["/", "_"]
    self.text_new = ""
    self.tonalita = {"M" : ["DO","REb","RE","MIb","MI","FA","FA#","SOL","LAb","LA","SIb","SI"],
                     "m" : ["DO","DO#","RE","MIb","MI","FA","FA#","SOL","SOL#","LA","SIb","SI"]}
    self.tonalita_cast = {"M" : [0,1,0,1,0,1,0,0,1,0,1,0], "m" : [1,0,1,1,0,1,0,1,0,0,1,0]}  # 0=#, 1=b
    self.diesis = ["DO","DO#","RE","RE#","MI","FA","FA#","SOL","SOL#","LA","LA#","SI"]
    self.bemolle = ["DO","REb","RE","MIb","MI","FA","SOLb","SOL","LAb","LA","SIb","SI"]
    self.ACC = ["DO", "RE", "MI", "FA", "SOL", "LA", "SI", "#", "b"]
    self.CHAR = ["-","sdim","dim","maj","sus","/","add","m","+","o","_"]   # , "2", "4", "5", "6", "7", "9", "11", "13"

  def isIntro(self, s):
    is_in = (s.split()[0] == "\intro")
    if is_in == True:
      self.text_new += "\intro "
    return is_in

  def isOutro(self, s):
    is_out = (s.split()[0] == "\outro")
    if is_out == True:
      self.text_new += "\outro "
    return is_out

  def isChords(self, s):
    is_c = (s.split()[0] == "\c")
    if is_c == 1:
      self.text_new += "\c "
    return is_c

  def ton2num(self, str):
    if str in self.diesis:
      num = self.diesis.index(str)
    elif str in self.bemolle:
      num = self.bemolle.index(str)
    else:
      num = -1
    return num

  def num2ton(self, num, cast):
    if cast == 0:
      ton = self.diesis[num]
    elif cast == 1:
      ton = self.bemolle[num]
    else:
      ton = "nn"
    return ton
  
  def delete_parentheses(self,line):
    newline = ''
    skip1c = 0
    skip2c = 0
    for c in line:
      if c == '[':
        skip1c += 1
      elif c == '(':
        skip2c += 1
      elif c == ']' and skip1c > 0:
        skip1c -= 1
      elif c == ')'and skip2c > 0:
        skip2c -= 1
      elif skip1c == 0 and skip2c == 0:
        newline += c
    return newline
    
  def scrivi_parentesi(self, line_old, pos):
    while line_old[pos] != ')' and line_old[pos] != ']':
      self.text_new += line_old[pos]
      pos += 1
    self.text_new += line_old[pos]
    return pos + 1

  def check_n_transpose(self,line):
    line = str(line).strip('\n')
    if self.isIntro(line) or self.isChords(line) or self.isOutro(line):
      for c in self.encode:
        line = line.replace(c,"")   # line = 
      return self.transpose(line)
    else:
      return line + "\n"

  def convert(self, text_in, shift):
    text_out = ""
    self.shift = shift
    self.ton_new = (self.ton_old + self.shift) % 12
    lines = text_in.split("\n")
    text_out = ""
    for line in lines:
      self.text_new = ""
      text_out += self.check_n_transpose(line)
    return text_out.strip("\n")
    
  def rebuild(self, line_old, line_new):   # RIAGGIUNGO PARENTESI

    debito = 0   # conta gli spazi di cui sono in debito
    pos = 0   # posizione nella riga vecchia
    index_old = 0   # indice accordo index_new-esimo
    index_new = 0
    line_old_split = self.delete_parentheses(line_old).split()

    while pos < len(line_old)-1:
      spazi = 0
      if line_old[pos] == '(' or line_old[pos] == '[':
        pos = self.scrivi_parentesi(line_old, pos)
      else:
        l_old = len(line_old_split[index_old])
        l_new = len(line_new[index_new])
        if pos == 0:
          self.text_new += " "*max(len(line_old) - len(line_old.lstrip()) - 1, 0)
          pos += (len(line_old) - len(line_old.lstrip()))
        pos += l_old

        self.text_new += line_new[index_new]
        index_new += 1
        if line_old_split[index_old].find('/') != -1:
          self.text_new = self.text_new + "/" + line_new[index_new]
          l_new = l_new + len(line_new[index_new]) + 1   # il +1 è per il '/'
          index_new += 1
        if line_old_split[index_old].find('_') != -1:
          self.text_new = self.text_new + "_" + line_new[index_new]
          l_new = l_new + len(line_new[index_new]) + 1   # il +1 è per il '/'
          index_new += 1
        index_old += 1
        diff = l_old - l_new
        spazi += diff
  
        # calcolo spazi successivi
  
      while pos < len(line_old)-1 and line_old[pos] == " ":
        spazi += 1
        pos += 1

      spazi -= debito

      # spazi deve essere >= 1
      if pos >= len(line_old)-1:
        debito = debito   ######## continue ?
      elif spazi < 1:
        self.text_new += " "
        debito = abs(spazi) + 1
      else:
        self.text_new += " "*spazi
        debito = 0

    return self.text_new + "\n"

  def transpose(self, line):
    accordi = []
#    line_strip = " ".join(line.split())
    line_split = self.delete_parentheses(line)
    for c in self.join:
      line_split = line_split.replace(c,' ')
    line_split = line_split.split()
    for word in line_split:
      extra = []
      base = word
      for c in self.CHAR:
        base = base.replace(c, "")   # base è un singolo accordo
      base = ''.join(c for c in base if not c.isdigit())   # elimina i numeri

      extra = word
      for c in self.ACC:
        extra = extra.replace(c, "")   # extra contiene tutte le variazioni di ogni accordo

      if base in self.diesis or base in self.bemolle:
        chord_old = self.ton2num(base)
        chord_new = (chord_old + self.shift) % 12
        if self.tonalita_cast[self.modo][self.ton_new] == 0:
          base_new = self.diesis[chord_new]
        elif self.tonalita_cast[self.modo][self.ton_new] == 1:
          base_new = self.bemolle[chord_new]
      else:
        base_new = base

      base_new += extra
      accordi.append(base_new)
    return self.rebuild(line,accordi)