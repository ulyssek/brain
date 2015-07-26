from Globals import * 
from parser import *
from timer import Timer






class Model:
  
  def __init__(self,
                  limit=None,
                  talkative=True,
                  skip_cdiscount=False,
                  batch=False,
                  train=False,
                  **kwargs):
    self.skip_cdiscount = skip_cdiscount
    self.limit          = limit
    self.talkative      = talkative
    self.batch          = batch
    self.train          = train
    self.score          = 0
    self.path           = TRAIN_FILE
    self.train_len      = TRAIN_LEN
    self.cdiscount_position = CDISCOUNT_POSITION
    self.output_name    = RESULT_PATH + self.name + ".csv"
    self.no_brand       = NO_BRAND

    self.id_position          = ID_POSITION
    self.brand_position       = BRAND_POSITION
    self.price_position       = PRICE_POSITION
    self.c3_position          = C3_ID_POSITION
    self.cdiscount_position   = CDISCOUNT_POSITION
    self.desc_position        = DESCRIPTION_POSITION
    self.libelle_position     = LIBELLE_POSITION
    self.desc_position_test   = DESCRIPTION_POSITION_TEST
    self.brand_position_test  = BRAND_POSITION_TEST
    self.price_position_test  = PRICE_POSITION_TEST
    self.libelle_position_test = LIBELLE_POSITION_TEST
    self.counting_timer       = Timer()

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
    self.counting_timer.clean()
    self.counting_timer.pick()
    
  def smart_count(self,so_far=False):
    self.count += 1
    try:
      boule = not(self.count % int(self.local_limit/10)) and self.talkative 
    except ZeroDivisionError:
      boule = False
    if self.limit is not None and self.count == self.local_limit:
      self.loop_break = True
      if self.talkative:
        print "100% done"
    elif boule: 
      self.counting_timer.pick()
      print "%s%% done (%s s)" % (int(100*self.count/float(self.local_limit)),self.counting_timer.last_dif())
      if so_far:
        print "score so far : %s " % (self.temp_score/float(self.count)*100)

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
      price_positin       = PRICE_POSITION
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
    self.temp_score = 0

    self.reset_count(file_len)

    print "computing output"
    next(spam_reader)

    if not self.batch:
      for item in spam_reader:
        self.smart_count(so_far=True)
        cat = self.compute_category(item)
        if self.train:
          if self.skip_cdiscount_function(item):
            continue
          real_cat = item[cat_position]
          self.temp_score += int(real_cat == cat)
        else:  
          result.append([item[id_position],cat])

        if self.loop_break:
          break
    else:
      print "batch"
      items = []
      real_cats = []
      for item in spam_reader:
        self.smart_count()
        it = self.pre_build_item(item)
        cat = item[cat_position]
        if self.train:
          if self.skip_cdiscount_function(item):
            continue
          real_cats.append(cat)
          items.append((it,cat))
        else:
          items.append(it)
        if self.loop_break:
          break
      prediction = self.compute_batch_category(items)
      print "prediction done, computing score"
      for i in xrange(len(items)):
        self.temp_score += int(str(prediction[i]) == str(items[i][1]))
      print self.temp_score
          



    if self.train:
      self.score = self.temp_score/float(validation_len)*100
      print "score : %s " % (self.score,)
    else:
      self.result = result

  def skip_cdiscount_function(self, item):
    return self.skip_cdiscount and not bool(int(item[self.cdiscount_position]))

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

