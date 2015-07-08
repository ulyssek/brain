#!/usr/bin/env python
#-*-coding:utf-8-*-



import csv
import sys
from time       import sleep
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
limit = None
brand_position = 6
id_position = 3
no_brand = "AUCUNE"

if limit is not None:
  train_len = min(15786886,limit)
else:
  train_len = 15786886
  
test_len = 35066


##################################################################################
## EXTRACTING BRANDS FROM FILE


print "computing brands dictionary"

result = {}

for row in spam_reader:
  brand = row[brand_position]
  if brand == '':
    brand = no_brand
 
  if brand in brands.keys():
    if row[id_position] in brands[brand].keys():
      brands[brand][row[id_position]] += 1
    else:
      brands[brand][row[id_position]] = 1
  else:
    brands[brand] = {row[id_position] : 1}
  count += 1
  if limit is not None and count == limit:
    break
  if not(int(count) % int(train_len/10)):
    print "%s%% done" % (100*count/float(train_len),)


##################################################################################
## DEFINING CATEGORY FUNCTION

def cat_from_brand(brands,brand):
  brand_dict = brands[brand]
  return max(brand_dict.keys(),key=lambda x : brand_dict[x])

##################################################################################
## COMPUTING SCORE ON TEST FILE

print "computing category for test file"
  
test_file = "../data/test.csv"
output_file_name = "../results/brandy.csv"

spam_reader = parser(test_file)
brand_position_test = 3
count = 0

result = [["Id_Produit","Id_Categorie"]]

next(spam_reader)
for row in spam_reader:
  if row[brand_position_test] not in brands.keys():
    brand = no_brand
  else:
    brand = row[brand_position_test]
  cat = cat_from_brand(brands,brand)
  result.append([row[0],cat])
  count += 1
  if not(int(count) % int(test_len/10)):
    print "%s%% done" % (100*count/float(test_len),)


##################################################################################
## WRITING DOWN RESULTS IN THE OUTPUT FILE

print "Writing results in output file"

output_file = open(output_file_name, 'w')
a = csv.writer(output_file,delimiter=';')
a.writerows(result)
output_file.close()



