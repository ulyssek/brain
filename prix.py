#!/usr/bin/env python
#-*-coding:utf-8-*-



import csv
import sys
from parser     import parser
from tools      import smart_plot
from math_tools import distribution
from tools      import up
from tools      import compute_density

file_name = "../data/training.csv"

csv.field_size_limit(sys.maxsize)


spam_reader = parser(file_name)

limit = 5000000
pas_interval = 0.5
spam_reader = parser(file_name)
cat='1000003437'

## le prix max
prix_max=0
count=0
for row in spam_reader:
  if row[3] == cat:
    if float(row[8])>prix_max:
      prix_max=float(row[8])
  count+=1
  if count == limit:
    break



spam_reader = parser(file_name)

leng=int(prix_max/pas_interval)+int(bool(prix_max/pas_interval-int(prix_max/pas_interval)))+1
l=[0]*leng
#print prix_max
##remplir la liste l avec le nombre d'objet de categorie cat pour chaque intervalle
count = 0
for row in spam_reader:
  if row[3] == cat:
    #print int(float(row[8])/pas_interval)
    l[int(float(row[8])/pas_interval)]+=1
  count += 1
  if count == limit:
    break

##tracer la densité empirique pour la categorie cat

g=range(leng)

def foo(x):
  return x*pas_interval

g=map(foo,g)
 


smart_plot(l,g)










