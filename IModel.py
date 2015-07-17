from Globals import * 
from parser import *






class Model:
  
  def __init__(self,limit=None,talkative=True,skip_cdiscount=False,**kwargs):
    self.skip_cdiscount = skip_cdiscount
    self.limit          = limit
    self.talkative      = talkative
    for key in kwargs.keys():
      setattr(self, key, kwargs[key])

    print "Model initialized !"

  def build(self,skip_cdiscount):
    raise Exception("Not Implemented yet")

  ##################################################################################
  ## COUNTING FUNCTIONS

  def reset_count(self,count_len):
    self.count = 0
    self.loop_break = False
    if self.limit is not None:
      self.local_limit = min(count_len,self.limit)
    else:
      self.local_limit = count_len
    print self.local_limit
    print self.limit
    
  def smart_count(self):
    self.count += 1
    if self.limit is not None and self.count == self.limit:
      self.loop_break = True
      if self.talkative:
        print "100% done"
    elif not(self.count % int(self.local_limit/10)) and self.talkative:
      print "%s%% done" % (100*self.count/float(self.local_limit),)

  ##################################################################################
  ## CATEGORY COMPUTING FUNCTIONS

  def compute_category(self,item):
    raise Exception("Not Implemented yet")
 
  def compute_output(self):
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
    score = 0

    self.reset_count(file_len)

    print "computing output"
    next(spam_reader)
    for item in spam_reader:
      cat = self.compute_category(item)
      if self.train:
        if self.skip_cdiscount and bool(int(item[cdiscount_position])):
          continue
        real_cat = item[cat_position]
        score += int(real_cat == cat)
      else:  
        result.append([item[ID_POSITION],cat])

      self.smart_count()
      if self.loop_break:
        break

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

  def run(self):
    self.build()
    self.compute_output()
    if not self.train:
      self.print_output()

