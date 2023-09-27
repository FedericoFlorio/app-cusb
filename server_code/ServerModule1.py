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


@anvil.server.callable
def get_indice():
  return app_tables.indice.search()

@anvil.server.callable
def new_row_indice(titolo,tonalita,modo):
  return app_tables.indice.add_row(titolo=titolo,tonalita=tonalita,modo=modo)

@anvil.server.callable
def create_text_file(file_name, file_content):
    with open(file_name, 'w') as file:
        file.write(file_content)

# @anvil.server.callable
# def editor()
#   return anvil.assets.editor.call("editor.html")