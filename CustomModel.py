import csv
import sys
import math
from IModel   import *
from Globals  import *
from parser   import parser
from tools    import smart_in


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

  def build(self,skip_cdiscount=False):
    path                = TRAIN_FILE
    train_len           = TRAIN_LEN
    brand_position      = BRAND_POSITION
    id_position         = C3_ID_POSITION
    no_brand            = NO_BRAND
    cdiscount_position  = CDISCOUNT_POSITION

    count   = 0
    brands  = {}
    limit   = None

    if limit is not None:
      train_len = min(TRAIN_LEN,limit)
    else:
      train_len = TRAIN_LEN

    spam_reader = parser(path)

    print "computing brands dictionary"

    spam_reader.next()
    for row in spam_reader:
      brand = row[brand_position]
      if brand == '':
        brand = no_brand
     
      if skip_cdiscount and not(int(row[cdiscount_position])):
        continue
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


"""


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
 
      spam_reader = parser(self.path)

      print "computing prices dictionary"

      for row in spam_reader:
        price = self.transform(row[self.price_position])
        if price in prices.keys():
          if row[id_position] in prices[price].keys():
            prices[price][row[id_position]] += 1
          else:
            prices[price][row[id_position]] = 1
        else:
          prices[price] = {row[id_position] : 1}
        count += 1
        if count == self.train_len:
          break
        
      self.prices = prices

  ###A UN PRIX ASSOCIER LA BORNE INF DE L'INTERVALLE ECHELLE LOGARITHMIQUE
  def transform(self, prix):
    inf=int(math.exp(prix)/self.pas)*self.pas
    inf=math.log(inf)
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
        brand_position = BRAND_POSITION
      else:
        brand_position = BRAND_POSITION_TEST
      no_brand = NO_BRAND
      if item[brand_position] not in self.brands.keys():
        brand = no_brand
      else:
        brand = item[brand_position]
      cat = self.cat_from_brand(brand)
      return cat



    def cat_from_brand(self,brand):
      brand_dict = self.brands[brand]
      return max(brand_dict.keys(),key=lambda x : brand_dict[x])

    
    def compute_output(self):
      result = [["Id_Produit","Id_Categorie"]]
      id_position = ID_POSITION
      if self.train:
        file_name       = VALIDATION_FILE
        brand_position  = BRAND_POSITION
        file_len        = TRAIN_LEN
        validation_len  = VALIDATION_LEN
        cat_position    = C3_ID_POSITION
      else:
        file_name       = TEST_FILE
        brand_position  = BRAND_POSITION_TEST
        file_len        = TEST_LEN

      spam_reader = parser(file_name)
      count = 0
      score = 0
      limit = None

      if limit is not None:
        file_len = min(file_len,limit)
      else:
        file_len = file_len
 

      print "computing output"
      next(spam_reader)
      for item in spam_reader:
        cat = self.compute_category(item)
        if self.train:
          real_cat = item[cat_position]
          score += int(real_cat == cat)
        else:  
          result.append([item[ID_POSITION]])
        count += 1
        if not(int(count) % int(file_len/10)):
          print "%s%% done" % (100*count/float(file_len),)
        if (limit is not None) & (count == limit):
          break
      print "100% done"
      if self.train:
        self.score = score/float(validation_len)*100
        print "score : %s " % (self.score,)
      else:
        self.result = result

"""



 
