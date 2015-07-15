import csv
import sys
import math
from IModel   import *
from Globals  import *
from parser   import parser
from tools    import smart_in
from dico     import *


csv.field_size_limit(sys.maxsize)





class BrandAverage(Model):

  ##################################################################################
  ## INIT FUNCTIONS

  def __init__(self,train=False,**kwargs):
    self.train = train
    self.score = 0
    Model.__init__(self,**kwargs)
    self.name = "BRAND_AVERAGE"
    self.output_name = RESULT_PATH + self.name + ".csv"

  ##################################################################################
  ## BUILDING FUNCTIONS

  def build(self):
    path = TRAIN_FILE
    train_len = TRAIN_LEN
    brand_position = BRAND_POSITION
    id_position = C3_ID_POSITION
    no_brand = NO_BRAND

    count = 0
    brands = {}
    limit = None

    if limit is not None:
      train_len = min(TRAIN_LEN,limit)
    else:
      train_len = TRAIN_LEN

    spam_reader = parser(path)

    print "computing brands dictionary"

    for row in spam_reader:
      brand = row[brand_position]
      if brand == '':
        brand = no_brand
     
      if smart_in(brands,brand):
        if smart_in(brands[brand],row[id_position]):
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
    print "100% done"

    self.brands = brands
    self.build_max_brands()
    

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
      brand_position = BRAND_POSITION
    else:
      brand_position = BRAND_POSITION_TEST
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

  def __init__(self,train=False,limit = None,**kwargs):
    self.train = train
    self.score = 0
    Model.__init__(self,**kwargs)
    self.name = "PRICE_AVERAGE"
    self.output_name = RESULT_PATH + self.name + ".csv"
    self.path = TRAIN_FILE
    self.train_len = TRAIN_LEN
    self.price_position = PRICE_POSITION
    self.id_position = C3_ID_POSITION
    self.prix_max = 0
    if limit is not None:
      self.train_len = min(TRAIN_LEN,limit)
    self.pas = 0.5


  ##################################################################################
  ## BUILDING FUNCTIONS

  def build(self):
    prices={}
    l=[]
    spam_reader = parser(self.path)
    spam_reader.next()
    count=0

    print "computing prices dictionary and prices list"

    for row in spam_reader:
      if float(row[self.price_position])<=0:
        continue
      price = self.transform(float(row[self.price_position]))
      l.append(price)
      if price in prices.keys():
        if row[self.id_position] in prices[price].keys():
          prices[price][row[self.id_position]] += 1
        else:
          prices[price][row[self.id_position]] = 1
      else:
        prices[price] = {row[self.id_position] : 1}
      count += 1
      if count == self.train_len:
        sort(l)
        break
        
    self.prices = prices
    self.p_list = l

  ###A UN PRIX ASSOCIER LA BORNE INF DE L'INTERVALLE ECHELLE LOGARITHMIQUE
  def transform(self, p):
  #  inf=int(math.log(p)/self.pas)*self.pas
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
      price_position = PRICE_POSITION
    else:
      price_position = PRICE_POSITION_TEST
    price = float(item[price_position])
    if price <= 0:
      cat = 1000015309
    else:
      price = self.transform(price) 
      if price not in self.p_list:
        self.p_list.append(price)
        if price-self.p_list[self.p_list.index(price)-1]<self.p_list[self.p_list.index(price)+1]-price:
          price=self.p_list[self.p_list.index(price)-1]
        else:
          price=self.p_list[self.p_list.index(price)+1]
      cat = self.cat_from_price(price)
      return cat



  def cat_from_price(self,price):
    price_dict = self.prices[price]
    return max(price_dict.keys(),key=lambda x : price_dict[x])


class DescripAverage(Model):

  ##################################################################################
   ## INIT FUNCTIONS

  def __init__(self,train=False,limit = None,**kwargs):
    self.score = 0
    Model.__init__(self,**kwargs)
    self.name = "DESCIP_AVERAGE"
    self.output_name = RESULT_PATH + self.name + ".csv"
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

 
