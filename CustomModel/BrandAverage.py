# -*- coding:utf-8 -*-

import csv
import sys
import math
import string
import gc
from time     import sleep
from IModel   import *
from Globals  import *
from parser   import parser
from tools    import smart_in, find_nearest
from dico     import *
from WordDic  import WordDic
#from sklearn.feature_extraction.text import TfidfVectorizer
#from sklearn.neighbors import KNeighborsClassifier as nei_classifier

from timer import Timer


csv.field_size_limit(sys.maxsize)








class BrandAverage(Model):

  ##################################################################################
  ## INIT FUNCTIONS

  def __init__(self,**kwargs):
    self.name = "BRAND_AVERAGE"
    Model.__init__(self,**kwargs)

  ##################################################################################
  ## BUILDING FUNCTIONS

  def build(self):

    brands  = {}

    spam_reader = parser(self.path)

    print "computing brands dictionary"

    self.reset_count(self.train_len)

    spam_reader.next()
    for row in spam_reader:
      self.smart_count()
      brand = self.normalized_brand(row[self.brand_position])
     
      if self.skip_cdiscount_function(row):
        continue
      if smart_in(brands,brand):
        if smart_in(brands[brand],row[self.c3_position]):
          brands[brand][row[self.c3_position]] += 1
        else:
          brands[brand][row[self.c3_position]] = 1
        brands[brand]['total']+=1
      else:
        brands[brand] = {row[self.c3_position] : 1,'total' : 1}
        

      
      if self.loop_break:
        break



    self.brands = brands
    self.build_max_brands()
    

  def normalized_brand(self,brand):
    if brand == '':
      return self.no_brand
    else:
      return brand

  def build_max_brands(self):
    self.max_brand = {}
    self.proba = {}
    for brand in self.brands.keys():

      brand_dict = self.brands[brand]
      total=brand_dict.pop('total')
      self.max_brand[brand] = max(brand_dict.keys(),key=lambda x : brand_dict[x])
      self.proba[brand] = float(brand_dict[self.max_brand[brand]])/float(total)
      #if float(brand_dict[self.max_brand[brand]])!=float(total):
      # print "proba plus petit que 1"
      #print float(brand_dict[self.max_brand[brand]])
      

      


  ##################################################################################
  ## CATEGORY COMPUTING FUNCTIONS

  def compute_category(self,item):
    #Core function, associating an item with a category
    #item is a vector just read from the file
    if self.train:
      brand_position = self.brand_position
    else:
      brand_position = self.brand_position_test
    no_brand = NO_BRAND
    if not smart_in(self.brands,item[brand_position]):
      brand = no_brand
    else:
      brand = item[brand_position]
    cat = self.cat_from_brand(brand)
    return cat

  def cat_from_brand(self,brand):
    return self.max_brand[brand]
    brand_dict = self.brands[brand]
    return max(brand_dict.keys(),key=lambda x : brand_dict[x])




