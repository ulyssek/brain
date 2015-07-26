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

class Unique(Model):
  
  def __init__(self,cat_id=1000009411,**kwargs):
    self.cat  = str(cat_id)
    self.name = "ONLY_" + self.cat
    Model.__init__(self,**kwargs)

  def build(self):
    pass

  def compute_category(self,item):
    return self.cat
