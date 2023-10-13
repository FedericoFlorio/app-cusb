import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

ton = 0
mode = ""
testo = ""

def newTon(ton,mode,shift):
  tonalita = {"M" : ["DO","REb","RE","MIb","MI","FA","FA#","SOL","LAb","LA","SIb","SI"],
              "m" : ["DO","DO#","RE","MIb","MI","FA","FA#","SOL","SOL#","LA","SIb","SI"]}
  ton_new = tonalita[mode][(ton+shift)%12]
  return ton_new

def transpose(lines,ton_old,mode,shift):
  if mode == "m":
    ton_old = (ton_old + 3)%12
  ton_new = (ton_old + shift)%12

  tonalita = {"M" : ["DO","REb","RE","MIb","MI","FA","FA#","SOL","LAb","LA","SIb","SI"],
                "m" : ["DO","DO#","RE","MIb","MI","FA","FA#","SOL","SOL#","LA","SIb","SI"]}
  tonalita_cast = {"M" : [0,1,0,1,0,1,0,0,1,0,1,0], "m" : [1,0,1,1,0,1,0,1,0,0,1,0]}  # 0=#, 1=b
  diesis = ["DO","DO#","RE","RE#","MI","FA","FA#","SOL","SOL#","LA","LA#","SI"]
  bemolle = ["DO","REb","RE","MIb","MI","FA","SOLb","SOL","LAb","LA","SIb","SI"]
  char = ["m", "dim", "-", "maj", "+", "sdim", "sus", "2", "4", "6", "7", "9", "11", "13", "/"]

  def isIntro(s):
    return (s.split()[0] == "\intro")

  def isChords(s):
    return (s.split()[0] == "\c")

  def ton2num(str):
    if str in diesis:
      num = diesis.index(str)
    elif str in bemolle:
      num = bemolle.index(str)
    else:
      num = -1
    return num

  def num2ton(num,cast):
    if cast == 0:
      ton = diesis[num]
    elif cast == 1:
      ton = bemolle[num]
    else:
      ton = "nn"
    return ton

  text_new = ""

  for line in lines:
    line = line.strip("\n")
    pos = -1
    if isIntro(line) or isChords(line):
      line_new = line
      cnt = 0
      for word in line.split():
        if word == "\intro" or word == "\c":
          word_new = word
        else:
          extra = []
          word_mod = word
          for c in char:
            if word.find(c) > -1:
              word_mod = word.replace(c," ")
              extra.append(c)
          
          if word_mod.find(" ") != -1:
            basi = word_mod.split()
          else:
            basi = [word_mod]
  
          basi_new = [""] * len(basi)
  
          for i,base in enumerate(basi):
            if base in diesis or base in bemolle:
              chord = ton2num(base)
              chord_new = (chord + shift) % 12
              if tonalita_cast[mode][ton_new] == 0:
                basi_new[i] = diesis[chord_new]
              elif tonalita_cast[mode][ton_new] == 1:
                basi_new[i] = bemolle[chord_new]
            else:
              basi_new[i] = base
  
          word_new = basi_new[0]
          for e in extra:
            word_new += e
          if len(basi) == 2:
            word_new += basi_new[1]
    
        l = len(word)
        l_new = len(word_new)
        pos = line[pos+1:].find(word) + pos+1
  
        if l_new+cnt <= l:
          line_new = line_new[0:pos] + word_new + " "*(l-l_new-cnt) + line_new[pos+l:]
        else:
          for j in range(l_new+cnt-l):
            if line_new[pos+l] == " " and line_new[pos+l+1] == " ":
              line_new = line[:pos] + word_new + line[pos+l+1:]
            elif pos > 1 and line_new[pos-1] == " " and line_new[pos-2] == " ":
              line = line[:pos-1] + word_new + line[pos+l:]
            elif pos == 1 and line[pos-1] == " ":
              line = word_new + line[pos+l:]
            else:
              line_new = line_new[0:pos] + word_new + line_new[pos+l:]
              cnt += 1
    else:
      line_new = line

    text_new += (line_new + "\n")

  return text_new.strip("\n")