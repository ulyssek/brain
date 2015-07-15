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
count = 0
limit = 100000000000
brand_position = 3
ratio = 0


##################################################################################
## COMPTER LE NOMBRE DE PRODUITS CDISCOUNT


for row in spam_reader: 
  if row[7] == "1":
    ratio += 1
  count+=1
  if count == limit:
    break

ratio = ratio/float(count)

print "ratio de produit cdiscount : %s" % (ratio)



