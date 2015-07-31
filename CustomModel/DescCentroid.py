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




class DescCentroid(Model):


 
  ##################################################################################
  ## INIT FUNCTIONS

  def __init__(self,product=False,**kwargs):
    self.name = "DESC_CENTROID_IDF"
    self.product = product
    Model.__init__(self,**kwargs)

  ##################################################################################
  ## BUILDING FUNCTIONS

  def build(self):

    self.word_cats_dict = {}
    cats  = {} 
    cat_count = {}

    spam_reader = parser(self.path)

    print "computing category dictionary"

    self.reset_count(self.train_len)

    spam_reader.next()
    for row in spam_reader:

      cat   = row[self.c3_position]

      if self.skip_cdiscount_function(row):
        continue
      if self.skip_book_function(row):
        continue
      if self.cat_count is not None:
        if not smart_in(cat_count,cat):
          cat_count[cat] = 1
        else:
          if cat_count[cat] > self.cat_count:
            continue
          else:
            cat_count[cat] += 1

      self.smart_count()

      if self.loop_break:
        break


      voc = self.voc_from_item(row,train=True)

      for word in voc:
        if smart_in(self.word_cats_dict,word):
          if cat not in self.word_cats_dict[word]:
            self.word_cats_dict[word].add(cat)
        else:
          self.word_cats_dict[word] = set([cat])
      if self.product:
        voc = self.word_product(voc)
      for word in voc:
        if smart_in(cats,cat):
          cats[cat].add_word(word)
        else:
          cats[cat] = WordDic()
          cats[cat].add_word(word)

      del(voc)

    new_dict = {}
    for word in self.word_cats_dict:
      if not len(self.word_cats_dict[word])==1:
        new_dict[word] = self.word_cats_dict[word]
      else:
        if cats[next(iter(self.word_cats_dict[word]))].del_word(word):
          new_dict[word] = self.word_cats_dict[word]

    self.word_cats_dict = new_dict

    self.cats = cats
    self.build_centroids()


  def word_dic_from_list(self,word_list):
    dic = {"dic":{}, "total" : 0 }
    for word in word_list:
      if smart_in(dic["dic"],word):
        dic["dic"][word] += 1
        dic["total"] += 1
      else:
        dic["dic"][word] = 1
        dic["total"] += 1
    return dic

   
  def voc_from_item(self,item,train=None):
    if train is None:
      train = self.train
    if train:
      desc_position     = self.desc_position
      brand_position    = self.brand_position
      libelle_position  = self.libelle_position
    else:
      desc_position     = self.desc_position_test
      brand_position    = self.brand_position_test
      libelle_position  = self.libelle_position_test
    brand = self.normalized_brand(item[brand_position])
    desc  = self.normalized_desc(item[desc_position])
    libel = self.normalized_desc(item[libelle_position])
    desc  = desc.lower()
    desc += " " + libel.lower()
    voc = desc.split(" ")
    voc = self.remove_stop_words(voc)
    voc.append(brand)
    return voc


  def word_product(self,word_list):
    for i in xrange(len(word_list)):
      for j in xrange(i):
        word_list.append(word_list[i] + "_" + word_list[j])
    return word_list


     

  def normalized_brand(self,brand):
    if brand == '':
      return self.no_brand
    else:
      return brand

  def remove_ponctuation(self,text):
    table = string.maketrans("","")
    return text.translate(table, string.punctuation)

  def remove_stop_words(self,text):
    s_words = [
      "",
      "de",
      "la",
      "le",
      "un",
      "une",
      "pour",
      "au",
      "Le",
      "à",
      "aux",
      "ou",
      "et",
      "les",
      "des",
      "du",
      "À",
      "…",
      "voir",
      "présentation",
      "en",
      "avec",
      "a",
      "ce",
      "par",
      "sur",
      "est",
      "pas",
      "très",
      "rouge",
      "blanche",
      "blanc",
      "rose",
      "noir",
      "gris",
      "grise",
      "bleue",
      "bleu",
      "noire",
      "mm",
      "cm",
      "dm",
      "m",
      "d",
      "plus",
      "AUCUNE",
    ]
    text[:] = [x for x in text if (x not in s_words and not x.isdigit())]
    return text

  def normalized_desc(self,desc):
    return self.remove_ponctuation(desc)

  def build_centroids(self,idf=True):
    self.centroids = {}
    for cat in self.cats.keys():
      self.centroids[cat] = {}
      word_count = float(self.cats[cat].total)
      for word in self.cats[cat].word_list():
        if idf:
          # word est soit de la forme %mot, auxquel cas il sera trouvé dans word_cats_dict, soit de 
          # la forme mot1_mot2, auxquel cas il ne sera pas dans word_cats_dict, et sa valeur de idf 
          # sera une formule de mot1 et mot2
          # Le try permet de n'executer les splits que pour les mots composés
          try:
            idf_factor = len(self.word_cats_dict[word])
          except KeyError:
            #word1, word2 = word.split("_")
            #idf_factor = max(len(self.word_cats_dict[word1]),len(self.word_cats_dict[word2]))
            idf_factor = 1
        else:
          idf_factor = 1
        self.centroids[cat][word] = self.cats[cat].dic[word]/(word_count*idf_factor)
        
  def compute_category(self,item):
    t = Timer()
    t.pick("debut")
    voc = self.voc_from_item(item)
    if self.product:
      voc = self.word_product(voc)
    voc_dic = self.word_dic_from_list(voc)
    best_score = 0
    best_cat = 1000009411
    t.pick("vocabulaire construit")
    cat_set = set()

    for word in voc_dic["dic"].keys():
      try:
        cat_set = cat_set.union(self.word_cats_dict[word])
        #print 'word : "%s", count : %s ' % (word,len(self.word_cats_dict[word]))
      except KeyError:
        #Si on ne peut pas trouver de catégorie pour ce mot, c'est qu'il n'a jamais été trouvé 
        # dans le set train
        pass
    #print "total : %s " % (len(cat_set) ,)
    #print len(voc_dic["dic"])
    for cat in cat_set:
      score = 0
      for word in voc_dic["dic"].keys():
        if smart_in(self.centroids[cat],word):
          score += self.centroids[cat][word]*voc_dic["dic"][word]
      if score > best_score:
        best_score = score
        best_cat = cat
    if best_score == 0:
      #print "nothing found"
      pass
    t.pick("best_cat chope")
    return best_cat
      


