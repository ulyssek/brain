from tools import smart_in



class WordDic():


  def __init__(self):
      self.total  = 0
      self.dic    = {}


  def add_word(self,word,n=1):
      if smart_in(self.dic,word):
        self.dic[word] += n
      else:
        self.dic[word] = n
      self.total += n

  def word_list(self):
    return self.dic.keys()
      
