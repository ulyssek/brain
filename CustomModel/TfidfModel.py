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




class TfIdfModel(Model):


  def __init__(self,**kwargs):
    self.name = "TfIdefModel"
    Model.__init__(self,**kwargs)


  def build(self):


    spam_reader = parser(self.path)

    data = {}

    print "computing brands dictionary"

    self.reset_count(self.train_len)

    spam_reader.next()
    for row in spam_reader:
      self.smart_count()
      desc = row[self.desc_position]

      if self.skip_cdiscount_function(row):
        continue
      if smart_in(data,row[self.c3_position]):
        data[row[self.c3_position]].append(desc)
      else:
        data[row[self.c3_position]] = [desc]

      if self.loop_break:
        break

    final_data = {}
    print len(data["1000015309"])

    for cat_id in data.keys():
      final_text = ''
      for text in data[cat_id]:
        final_text += text
      final_data[cat_id] = final_text
      print final_text

    vectorizer = TfidfVectorizer()
    vectorizer.fit_transform(map(lambda x : final_data[x], final_data.keys()))
    return vectorizer



