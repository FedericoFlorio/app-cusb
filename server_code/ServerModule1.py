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
  return app_tables.indice.search()

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
  beg = s[2]
  end = s[len(s)-1]
  body = s[3:len(s)-1]
  if title.split("")[0] != "\title":
    err = 1
  if intro.split("")[0] != "\intro":
    err = 2
  if beg.split("")[0] != "\begin":
    err = 3
  if end.split("")[0] != "\end":
    err = 4
  for line in body:
    w = line.split("")[0]
    if w != "\t" or w != "\a" or w != "$" or w != "$$":
      err = 5
  return err