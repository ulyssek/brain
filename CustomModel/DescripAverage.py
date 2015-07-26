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



class DescripAverage(Model):

  ##################################################################################
   ## INIT FUNCTIONS

  def __init__(self,train=False,limit = None,**kwargs):
    self.name = "DESCIP_AVERAGE"
    Model.__init__(self,**kwargs)
    self.dico = dico_mots_clefs()
    self.l = list_mots_clefs()
    
  ##################################################################################
  ## BUILDING FUNCTIONS

  def build(self):

    print "on verra plus tard pour ameliorer le dico des mots clefs avec la base d'apprentissage"

    
  ##################################################################################
    ## CATEGORY COMPUTING FUNCTIONS

  def compute_category(self,item):
    #Core function, associating an item with a category
    #item is a vector just read from the file
    #if self.train:      
    #else:

    desc_position = DESCRIPTION_POSITION_TEST
    d = item[desc_position]
    d = d.split()
    d = [x for x in d if x in self.l] 

    m=0
    for a in self.dico.keys():
      inter=[c for c in d if c in self.dico[a]]
      if m<len(inter):
        m=len(inter)
        cat=a

    return cat   

 
