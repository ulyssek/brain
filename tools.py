from time import sleep

def f(n):
  results = []
  for i in xrange(6):
    for j in xrange(6-i-1):
      try:
        results.append(n.compare_keeps(i,i+j+1))
      except:
        results.append(0)
  return results



#import matplotlib.pyplot as plt


def up(dico,key):
  if key in dico.keys():
    dico[key] += 1
  else:
    dico[key] = 1

def compute_density(dico):
  density = {}
  for key in dico:
    up(density,dico[key])
  return density




def smart_plot(liste, x_list = None, figure = False, names = None,xlabel=None,ylabel=None,xlim=None,ylim=None, legend=None, legend_position=1):
  color = ("r--", "b--", "g--", "y--", "o--")
  if figure:
    plt.figure(1)
    nb_figure = len(liste)
    for key in xrange(len(liste)):
      plt.subplot(nb_figure, 1, key)
      plt.plot(range(len(liste[key])), liste[key], color[0])
      if names is not None:
        plt.title(names[key])
  else:
    ax = plt.gca()
    if x_list is None:
      args = ()
      kwargs = {}
      label = None
      for key in xrange(len(liste)):
        if legend is not None:
          kwargs = {"label":legend[key]}
        args = (range(len(liste[key])), liste[key], color[key % len(color)])
        plt.plot(*args,**kwargs)
    else:
      args = (x_list, liste, color[0])
      plt.plot(*args)
    if names is not None:
      plt.title(names)
    if xlabel is not None:
      ax.set_xlabel(xlabel)
    if ylabel is not None:
      ax.set_ylabel(ylabel)
    if xlim is not None:
      ax.set_xlim(xlim)
    if ylim is not None:
      ax.set_ylim(ylim)
    if legend is not None:
      if legend_position==1:
        loc = "upper right"
      elif legend_position==2:
        loc = "lower right"
      elif legend_position==3:
        loc = "lower left"
      else:
        loc = "upper left"
      plt.legend(loc=loc)

  plt.show()
  return plt


def smart_in(dico,key):
  try:
    dico[key]
    return True
  except KeyError:
    return False
    
def find_nearest(liste, element):
  #CAREFUL, THE LIST MUST BE SORTED

  if element <= liste[0]:
    return liste[0]
  elif element >= liste[len(liste)-1]:
    return liste[len(liste)-1]
  current_i = len(liste)/2
  step = len(liste)/2
  while True:
    if liste[current_i] == element:
      return liste[current_i]
    elif step == 1:
      m1 = (current_i-1,abs(liste[current_i-1]-element))
      m2 = (current_i,abs(liste[current_i]-element))
      try:
        m3 = (current_i+1,abs(liste[current_i+1]-element))
      except IndexError:
        m3 = m2
      return liste[min([m1,m2,m3],key=lambda x : x[1])[0]]
        
    step = step/2
    if liste[current_i] < element:
      current_i += step
    else:
      current_i -= step

