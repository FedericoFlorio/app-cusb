import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
@anvil.server.callable
def say_hello(name):
  print("Hello, " + name + "!")
  return 42


@anvil.server.callable  # Cerca un canto nella tabella indice
def get_indice():
  return app_tables.indice.search(tables.order_by("titolo"),
                                  tables.order_by("tonalita"))

@anvil.server.callable  # Aggiunge una riga alla tabella indice
def new_row_indice(titolo,tonalita,modo):
  return app_tables.indice.add_row(titolo=titolo,tonalita=tonalita,modo=modo)

@anvil.server.callable  # Crea un file di testo dato nome e contenuto
def create_text_file(file_name, file_content):
    with open(file_name, 'w') as file:
        file.write(file_content)

@anvil.server.callable  # Controlla la correttezza del formato di un testo sorgente
def check_format(s):
  err = 0
  title = s[0]
  intro = s[1]
  if title.split()[0] != "\head":
    err = 1
  if intro.split()[0] == "\intro":
    end = s[len(s)-1]
    body = s[3:len(s)-1]
    beg = s[2]
  else:
    if intro.split()[0] == "\start":
      end = s[len(s)-1]
      body = s[2:len(s)-1]
      beg = s[1]
    else:
      err = 2

  if beg.split()[0] != "\start":
    print(beg.split()[0])
    err = 3
  if end.split()[0] != "\end":
    err = 4
  for line in body:
    w = line.split()[0]
    if w != "\l" and w != "\c" and w != "$" and w != "$$" and w != "\outro" and w != "\cmt":
      err = 5
  return err

@anvil.server.callable
def mod_row_indice(old,new,ton,mod):
  ind = get_indice()
  for row in ind:
    if row['titolo'] == old:
      row['tonalita'] = ton
      row['modo'] = mod
      row['titolo'] = new

@anvil.server.callable
def mod_row_indice(old,new,ton,mod):
  ind = get_indice()
  for row in ind:
    if row['titolo'] == old:
      row['tonalita'] = ton
      row['modo'] = mod
      row['titolo'] = new

@anvil.server.callable  # Cancella una riga della tabella indice
def del_row_indice(titolo):
  ind = get_indice()
  for row in ind:
    if row["titolo"] == titolo:
      row.delete()

@anvil.server.callable  # Restituisce i canti della domenica dalla tabella canti_domenica
def get_domenica():
  return app_tables.canti_domenica.search(tables.order_by("num"))

@anvil.server.callable  # Aggiunge una riga alla tabella canti_domenica
def new_row_domenica(titolo,tonalita,tonalita_originale,modo,num):
  return app_tables.canti_domenica.add_row(titolo=titolo, tonalita=tonalita, tonalita_originale=tonalita_originale, modo=modo, num=num)

@anvil.server.callable  #cancella una riga della tabella canti_domenica
def del_row_domenica(titolo):
  dom = get_domenica()
  for row in dom:
    if row["titolo"] == titolo:
      row.delete()

@anvil.server.callable  # Cancella le righe della tabella canti_domenica
def reset_domenica():
  app_tables.canti_domenica.delete_all_rows()

@anvil.server.callable  # Imposta l'ordine dei canti della domenica
def num_domenica(titolo,num):
  dom = get_domenica()
  for row in dom:
    if row["titolo"] == titolo:
      row["num"] = num

@anvil.server.callable
def check_domenica(lista):
  ordine = [lista["num"] for i in range(len(lista))]
  ordine.sort()
  for i in range(len(ordine)-1):
    if ordine[i] == 0 or ordine[i] == ordine[i+1]:
      return False
  return True
