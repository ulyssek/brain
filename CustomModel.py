import csv
import sys
from IModel   import *
from Globals  import *
from parser   import parser


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
      limit = 10

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
       
        if brand in brands.keys():
          if row[id_position] in brands[brand].keys():
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




 
