






class Model:
  
  def __init__(self,**kwargs):
    for key in kwargs.keys():
      setattr(self, key, kwargs[key])

    print "Model initialized !"

  def build(self):
    print "running model !"
