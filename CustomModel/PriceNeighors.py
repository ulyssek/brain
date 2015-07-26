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


class PriceNeighbors(Model):
 
  def __init__(self,neighbors_number=10,price=True,brand=True,**kwargs):
    self.name = "PRICE_AVERAGE"
    Model.__init__(self,**kwargs)
    self.neighbors_number = neighbors_number
    self.price            = price
    self.brand            = brand



  def extract_from_item(self,item):
    result = {}
    if self.price:
      result["price"] = float(item[self.price_position])
    if self.brand:
      result["brand"] = float(item[self.brand_position])
    return result
 
  def build(self,skip_cdiscount=False):
    prices=[]
    spam_reader = parser(self.path)
    spam_reader.next()

    self.reset_count(self.train_len)
    
    print "computing prices dictionary and prices list"

    for row in spam_reader:
      price = float(row[self.price_position])
      self.smart_count()
      if price < 0:
        continue
      cat   = row[self.c3_position]
      prices.append((price,cat))
      if self.loop_break:
        break

    self.prices = prices
    self.build_classifier()

  def build_classifier(self):
    self.classifier = nei_classifier(n_neighbors=self.neighbors_number)
    X = map(lambda (x1,x2) : [x1], self.prices)
    y = map(lambda (x1, x2) : x2, self.prices)
    del(self.prices)
    self.classifier.fit(X,y)

  def compute_category(self,item):
    #Core function, associating an item with a category
    #item is a vector just read from the file
    if self.train:
      price_position = self.price_position
    else:
      price_position = self.price_position_test
    cat = self.cat_from_price(price)
    return cat

  def cat_from_price(self,price):
    return self.classifier.predict([[price]])

  def pre_build_item(self,item):
    if self.train:
      price_position = self.price_position
    else:
      price_position = self.price_position_test
    return item[price_position]


  def compute_batch_category(self,items):
    X = map(lambda (x1,x2) : [x1], items)
    del(items)
    return self.classifier.predict(X)


