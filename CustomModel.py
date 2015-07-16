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
    path                = TRAIN_FILE
    train_len           = TRAIN_LEN
    brand_position      = BRAND_POSITION
    id_position         = C3_ID_POSITION
    cdiscount_position  = CDISCOUNT_POSITION
    self.no_brand       = NO_BRAND

    brands  = {}

    spam_reader = parser(path)

    print "computing brands dictionary"

    self.reset_count(train_len)

    spam_reader.next()
    for row in spam_reader:
      brand = self.normalized_brand(row[brand_position])
     
      if self.skip_cdiscount and not(int(row[cdiscount_position])):
        continue
      if smart_in(brands,brand):
        if smart_in(brands[brand],row[id_position]):
          brands[brand][row[id_position]] += 1
        else:
          brands[brand][row[id_position]] = 1
      else:
        brands[brand] = {row[id_position] : 1}

      self.smart_count()
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

  def build(self,skip_cdiscount):
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
      if smart_in(prices,price):
        if smart_in(prices[price],row[self.id_position]):
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
    print prices
    self.p_list = l
    self.build_max_prices()
    print self.build_max_prices()

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
      p_list=self.p_list 
      if price not in p_list:
        p_list.append(price)
        p_list.sort()
        if p_list.index(price)==len(p_list)-1:
          price=p_list[len(p_list)-2]
        elif p_list.index(price)==0:
          price=p_list[1]
        else:
          if price-p_list[p_list.index(price)-1]<p_list[p_list.index(price)+1]-price:
            price=p_list[p_list.index(price)-1]
          else:
            price=p_list[p_list.index(price)+1]
      cat = self.cat_from_price(price)
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

 
