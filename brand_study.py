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
brands = {}
limit = 1000000
brand_position = 3


##################################################################################
## EXTRACTING BRANDS FROM FILE


print "computing brands dictionary"

for row in spam_reader:
  b = row[brand_position]
  if row[7] == 0:
    continue
  if b == '':
    b = "AUCUNE"
  up(brands,b)
  count += 1
  if count == limit:
    break



try:
  none_number = brands.pop("AUCUNE")
except:
  none_number = 0
  print "no AUCUNE"

try:
  non_number += brands.pop('')
except:
  print "no ''"


print brands

##################################################################################
## BUILDING UP DENSITY

print "computing density"

maxi = 0
for key in brands.keys():
  if brands[key] > maxi:
    maxi = brands[key]
    n_key = key


print "key : %s, number : %s" % (n_key,brands[n_key])
density = compute_density(brands)



##################################################################################
## PRINTING STUFF

for i in xrange(1,15):
  try:
    print "number of items : %s, number of brands : %s" % (i, density[i])
  except:
    pass
print "number of brands : %s" % (len(brands.keys()),)
print "number of items : %s" % (count)
print "ratio items/brands : %s" % ((count-none_number)/float(len(brands.keys())))
print "number of un_brand items : %s" % (none_number,)
smart_plot(map(lambda x : density[x],density.keys()),x_list=sorted(density.keys()))

