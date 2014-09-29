#  coding: utf8

from importarFile0 import *
from importarFile1 import *
#from importarFile2 import *

# we have the old database and it has to be converted to the new structure.
# first will be imported de UsersCES file
# second the Socis CIC file
# and finally Transversal file to complet the database.

############################
## Main call of functions ##
############################

ZeroFile('Transversal.csv')
FirstFile('usersCES.csv')
#SecondFile('Socis_CIC-21_7_2014.csv')

print("bye!")
