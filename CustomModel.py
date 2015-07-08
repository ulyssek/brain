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
      limit = 1000

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

    
    def compute_output(self):
      result = [["Id_Produit","Id_Categorie"]]
      id_position = ID_POSITION
      if self.train:
        file_name       = VALIDATION_FILE
        brand_position  = BRAND_POSITION
        file_len        = TRAIN_LEN
      else:
        file_name       = TEST_FILE
        brand_position  = BRAND_POSITION_TEST
        file_len        = TEST_LEN

      spam_reader = parser(file_name)
      count = 0

      next(spam_reader)
      for item in spam_reader:
        cat = self.compute_category(item)
        result.append([item[ID_POSITION]])
        count += 1
        if not(int(count) % int(file_len/10)):
          print "%s%% done" % (100*count/float(file_len),)

      self.result = result
        
    ##################################################################################
    ## PRINTING FUNCTIONS

    def print_output(self):
      print "Writing results in output file"

      output_file = open(self.output_name, 'w')
      a = csv.writer(output_file,delimiter=DELIMITER)
      a.writerows(self.result)
      output_file.close()

    ##################################################################################
    ## RUNNNING FUNCTIONS

    def run(self):
      self.build()
      self.compute_output()
      self.print_output()





 
