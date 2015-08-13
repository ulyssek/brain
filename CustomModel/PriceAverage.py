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





class PriceAverage(Model):

  ##################################################################################
   ## INIT FUNCTIONS

  def __init__(self,**kwargs):
    self.name = "PRICE_AVERAGE"
    Model.__init__(self,**kwargs)
    self.prix_max = 0
    self.pas = 10


  ##################################################################################
  ## BUILDING FUNCTIONS

  def build(self,skip_cdiscount=False):
    prices={}
    l=[]
    spam_reader = parser(self.path)
    spam_reader.next()
    self.reset_count(self.train_len)
    
    print "computing prices dictionary and prices list"

    for row in spam_reader:
      if float(row[self.price_position])<=0:
        continue
      price = self.transform(float(row[self.price_position]))
      if smart_in(prices,price):
        if smart_in(prices[price],row[self.c3_position]):
          prices[price][row[self.c3_position]] += 1
        else:
          prices[price][row[self.c3_position]] = 1
        prices[price]['total']+=1
      else:
        l.append(price)
        prices[price] = {row[self.c3_position] : 1,'total' : 1}
      self.smart_count()
      if self.loop_break:
        break

    l.sort() 
    self.prices = prices
    self.p_list = l
    self.build_max_prices()
    
    #print self.max_price
    #print l[len(l)-1]
    
  ###A UN PRIX ASSOCIER LA BORNE INF DE L'INTERVALLE ECHELLE LOGARITHMIQUE
  def transform(self, p):
  #  inf=int(math.log(p)/self.pas)*self.pas
  #  return p
    inf = int(p/self.pas)*self.pas
    return inf


  ###### DEFINIR LE PRIX MAX
  def define_price_max(self):
    spam_reader = parser(self.path)
    count=0
    for row in spam_reader:
      if float(row[self.price_position])>self.prix_max:
        self.prix_max=float(row[self.price_position])
      count+=1
      if count == self.train_len:
        break



  ##################################################################################
    ## CATEGORY COMPUTING FUNCTIONS

  def compute_category(self,item):
    #Core function, associating an item with a category
    #item is a vector just read from the file
    if self.train:
      price_position = self.price_position
    else:
      price_position = self.price_position_test
    price = float(item[price_position])
    if price <= 0:
      cat = '1000015309'
    else:
      price = self.transform(price)
      p = None 
      p = find_nearest(self.p_list,price)
      cat = self.cat_from_price(p)
    return cat

  def build_max_prices(self):
    self.max_price = {}
    self.proba = {}
    for price in self.prices.keys():
      price_dict = self.prices[price]
      t=price_dict.pop('total')
      self.proba[price]={'total':t}
      self.max_price[price] = max(price_dict.keys(),key=lambda x : price_dict[x])
      self.proba[price]['proba']=float(price_dict[self.max_price[price]])/float(t)



  def cat_from_price(self,price):
    return self.max_price[price]
 
