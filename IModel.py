from Globals import * 
from parser import *






class Model:
  
  def __init__(self,**kwargs):
    for key in kwargs.keys():
      setattr(self, key, kwargs[key])

    print "Model initialized !"

  def build(self):
    raise Exception("Not Implemented yet")

    ##################################################################################
    ## CATEGORY COMPUTING FUNCTIONS
  def compute_category(self,item):
    raise Exception("Not Implemented yet")
 
  def compute_output(self,skip_cdiscount=False):
    result = [["Id_Produit","Id_Categorie"]]
    id_position = ID_POSITION
    if self.train:
      file_name           = VALIDATION_FILE
      brand_position      = BRAND_POSITION
      file_len            = TRAIN_LEN
      validation_len      = VALIDATION_LEN
      cat_position        = C3_ID_POSITION
      cdiscount_position  = CDISCOUNT_POSITION
    else:
      file_name           = TEST_FILE
      brand_position      = BRAND_POSITION_TEST
      file_len            = TEST_LEN
      cdiscount_position  = 1

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
        if skip_cdiscount and bool(int(item[cdiscount_position])):
          continue
        real_cat = item[cat_position]
        score += int(real_cat == cat)
      else:  
        result.append([item[ID_POSITION],cat])
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

  ##################################################################################
  ## PRINTING FUNCTIONS

  def print_output(self):
    print "Writing results in output file"

    output_file = open(self.output_name, 'w')
    a = csv.writer(output_file,delimiter=DELIMITER)
    a.writerows(self.result)
    output_file.close()

  ##################################################################################
  ## RUNNING FUNCTIONS

  def run(self,skip_cdiscount=False):
    self.build(skip_cdiscount)
    self.compute_output(skip_cdiscount)
    if not self.train:
      self.print_output()

