import csv
import sys
import math
import gc
from IModel   import *
from Globals  import *
from parser   import parser
from tools    import smart_in, find_nearest
from dico     import *
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import KNeighborsClassifier as nei_classifier


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
    brand_position      = BRAND_POSITION
    id_position         = C3_ID_POSITION
    cdiscount_position  = CDISCOUNT_POSITION
    self.no_brand       = NO_BRAND

    brands  = {}

    spam_reader = parser(self.path)

    print "computing brands dictionary"

    self.reset_count(self.train_len)

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

  def __init__(self,**kwargs):
    self.name = "PRICE_AVERAGE"
    Model.__init__(self,**kwargs)
    self.price_position = PRICE_POSITION
    self.id_position = C3_ID_POSITION
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
        if smart_in(prices[price],row[self.id_position]):
          prices[price][row[self.id_position]] += 1
        else:
          prices[price][row[self.id_position]] = 1
      else:
        prices[price] = {row[self.id_position] : 1}
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
      price_position = PRICE_POSITION
    else:
      price_position = PRICE_POSITION_TEST
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

  def build(self):
    text_position       = DESCRIPTION_POSITION
    id_position         = C3_ID_POSITION
    cdiscount_position  = CDISCOUNT_POSITION


    spam_reader = parser(self.path)

    data = {}

    print "computing brands dictionary"

    self.reset_count(self.train_len)

    spam_reader.next()
    for row in spam_reader:
      desc = row[text_position]

      if self.skip_cdiscount and not(int(row[cdiscount_position])):
        continue
      if smart_in(data,row[id_position]):
        data[row[id_position]].append(desc)
      else:
        data[row[id_position]] = [desc]

      self.smart_count()
      if self.loop_break:
        break

    final_data = {}

    for cat_id in data.keys():
      final_text = ''
      for text in data[cat_id]:
        final_text += text
      final_data[cat_id] = final_text

    vectorizer = TfidfVectorizer()
    vectorizer.fit_transform(map(lambda x : final_data[x], final_data.keys()))
    return vectorizer



class PriceNeighbors(Model):
 
  def __init__(self,neighbors_number=10,price=True,brand=True,**kwargs):
    self.name = "PRICE_AVERAGE"
    Model.__init__(self,**kwargs)
    self.price_position   = PRICE_POSITION
    self.brand_position   = BRAND_POSITION
    self.id_position      = C3_ID_POSITION
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
      cat   = row[self.id_position]
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
      price_position = PRICE_POSITION
    else:
      price_position = PRICE_POSITION_TEST
    cat = self.cat_from_price(price)
    return cat

  def cat_from_price(self,price):
    return self.classifier.predict([[price]])

  def pre_build_item(self,item):
    if self.train:
      price_position = PRICE_POSITION
    else:
      price_position = PRICE_POSITION_TEST
    return item[price_position]


  def compute_batch_category(self,items):
    X = map(lambda (x1,x2) : [x1], items)
    del(items)
    return self.classifier.predict(X)

  

 
