from tools import smart_in



class WordDic():


  def __init__(self):
      self.total    = 0
      self.dic      = {}
      self.product  = False


  def add_word(self,word,n=1):
      if smart_in(self.dic,word):
        self.dic[word] += n
      else:
        self.dic[word] = n
      self.total += n

  def word_list(self):
    return self.dic.keys()

  def get_occurence(self,word):
    return self.dic[word]
      
  def build_product(self):
    if self.product:
      raise Exception("Products already built")
    word_list = self.word_list()
    for i in xrange(len(word_list)):
      for j in xrange(i):
        self.add_word(word_list[i] + "_" + word_list[j],max(self.get_occurence(word_list[i]),self.get_occurence(word_list[j])))
    self.product = True
