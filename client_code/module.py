import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

# This is a module.
# You can define variables and functions here, and use them from any form. For example, in a top-level form:
#
#    from . import Module1
#
#    Module1.say_hello()
#

domenica = []
# {"titolo": row["titolo"],
#  "tonalita": row["tonalita"],
#  "modo": row["modo"],
#  "num": row["num"]})

def check_domenica(lista):
  ordine = [lista[i]["num"] for i in range(len(lista))]
  ordine.sort()
  for i in range(len(ordine)-1):
    if ordine[i] == 0 or ordine[i] == ordine[i+1] or ordine[i] not in list(range(len(ordine)+1)):
      return (False,0)

  sorted = [0 for i in range(len(lista))]
  for i in lista:
    sorted[i["num"]-1] = i
  return (True, sorted)