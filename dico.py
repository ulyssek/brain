import csv
import sys
import math
from IModel   import *
from Globals  import *
from parser   import parser
from tools    import smart_in
def dico_mots_clefs():
  spam_reader = parser("../data/rayon.csv")
  spam_reader.next()

  dictionnaire={}
  position_id=4
  name_cat1=1
  name_cat2=3
  name_cat3=5

  for row in spam_reader:
    x=row[name_cat1].lower()
    y=row[name_cat2].lower()
    z=row[name_cat3].lower()
    x=x.split()
    y=y.split()
    z=z.split()
    x=x+y+z
    non=['de', 'la', 'les', 'le', 'du', 'des', 'a', 'pour', '-', 'et']
    dictionnaire[row[position_id]]=[c for c in x if c not in non]

  return dictionnaire

def list_mots_clefs():
  d=dico_mots_clefs()
  l=[]
  for i in d.values():
    if i not in l:
      l.append(i)
  return l
  
  

