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
      else:
        brands[brand] = {row[self.c3_position] : 1}

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
    for brand in self.brands.keys():
      brand_dict = self.brands[brand]
      self.max_brand[brand] = max(brand_dict.keys(),key=lambda x : brand_dict[x])
      


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




class PriceAverage(Model):

  ##################################################################################
   ## INIT FUNCTIONS

  def __init__(self,**kwargs):
    self.name = "PRICE_AVERAGE"
    Model.__init__(self,**kwargs)
    self.prix_max = 0
    self.pas = 0.5


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
      l.append(price)
      if smart_in(prices,price):
        if smart_in(prices[price],row[self.c3_position]):
          prices[price][row[self.c3_position]] += 1
        else:
          prices[price][row[self.c3_position]] = 1
      else:
        prices[price] = {row[self.c3_position] : 1}
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
    return p
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
    for price in self.prices.keys():
      price_dict = self.prices[price]
      self.max_price[price] = max(price_dict.keys(),key=lambda x : price_dict[x])


  def cat_from_price(self,price):
    return self.max_price[price]
    

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


class DescCentroid(Model):


 
  ##################################################################################
  ## INIT FUNCTIONS

  def __init__(self,**kwargs):
    self.name = "DESC_CENTROID_IDF"
    Model.__init__(self,**kwargs)

  ##################################################################################
  ## BUILDING FUNCTIONS

  def build(self):

    self.word_cats_dict = {}
    cats  = {} 

    spam_reader = parser(self.path)

    print "computing category dictionary"

    self.reset_count(self.train_len)

    spam_reader.next()
    for row in spam_reader:
      self.smart_count()
      cat   = row[self.c3_position]

      voc = self.voc_from_item(row,train=True)
     
      if self.skip_cdiscount_function(row):
        continue

      for word in voc:
        if smart_in(self.word_cats_dict,word):
          if cat not in self.word_cats_dict[word]:
            self.word_cats_dict[word].add(cat)
        else:
          self.word_cats_dict[word] = set([cat])
        if smart_in(cats,cat):
          cats[cat].add_word(word)
        else:
          cats[cat] = WordDic()
          cats[cat].add_word(word)

      if self.loop_break:
        break

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
      "et",
      "les",
      "des",
      "À",
      "…",
      "voir",
      "présentation",
      "en",
      "avec",
      "a",
      "ce",
      "par",
      #"sur",
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
      #"mm",
      "cm",
      "dm",
      "m",
      "d",
      "plus",
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
          idf_factor = len(self.word_cats_dict[word])
        else:
          idf_factor = 1
        self.centroids[cat][word] = self.cats[cat].dic[word]/(word_count*idf_factor)
        
  def compute_category(self,item):
    t = Timer()
    t.pick("debut")
    voc = self.voc_from_item(item)
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
        pass
    #print "total : %s " % (len(cat_set) ,)
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
      

class Unique(Model):
  
  def __init__(self,cat_id=1000009411,**kwargs):
    self.cat  = str(cat_id)
    self.name = "ONLY_" + self.cat
    Model.__init__(self,**kwargs)

  def build(self):
    pass

  def compute_category(self,item):
    return self.cat
