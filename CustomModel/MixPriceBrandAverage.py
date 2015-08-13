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
from BrandAverage import *
from PriceAverage import *

csv.field_size_limit(sys.maxsize)





class MixPriceBrandAverage(Model):

##################################################################################
## INIT FUNCTIONS

  def __init__(self,**kwargs):
    self.name = "MIX_BRAND_PRICE_AVERAGE"
    Model.__init__(self,**kwargs)
    self.model_brand=BrandAverage(**kwargs)
    self.model_price=PriceAverage(**kwargs)
  
    


  ##################################################################################
  ## BUILDING FUNCTIONS

  def build(self,skip_cdiscount=False):
    self.model_price.build()
    self.model_brand.build()

  def compute_category(self,item):
    b=self.model_brand
    p=self.model_price
    if self.train:
      brand_position = self.brand_position
      price_position = self.price_position
    else:
      brand_position = self.brand_position_test
      price_position = self.price_position_test
    no_brand = NO_BRAND
    if not smart_in(b.brands,item[brand_position]):
      brand = no_brand
    else:
      brand = item[brand_position]
    
    price = float(item[price_position])

    if price<0: 
      cat=b.cat_from_brand(brand)
    else:
      price = p.transform(price)
      prix = None 
      prix = find_nearest(p.p_list,price)
      price=prix
      if b.proba[brand]['proba']>p.proba[price]['proba'] and brand!=no_brand:
        cat=b.cat_from_brand(brand)
      else:
        cat=p.cat_from_price(price)
    return cat 
