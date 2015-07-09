#!/usr/bin/env python
#-*-coding:utf-8-*-


from Globals import *

import csv
import sys
from time       import sleep
from parser     import parser
from tools      import smart_plot
from math_tools import distribution
from tools      import up
from tools      import compute_density

file_name = "../data/training.csv"

csv.field_size_limit(sys.maxsize)


spam_reader = parser(file_name)

train_name = "../data/training_set.csv"
validation = "../data/validation_set.csv"

train_len = 13*pow(10,6)

training_result = []
validation_result = []
count = 0

training_file = open(train_name, 'w')
training_a = csv.writer(training_file,delimiter=';')

valiation_file = open(validation, 'w')
validation_a = csv.writer(valiation_file,delimiter=';')


for row in spam_reader:
  if count < train_len:
    training_a.writerows([row])
  else:
    validation_a.writerows([row])
  count += 1
  if not(int(count) % int(TRAIN_LEN/10)):
    print "%s%% done" % (100*count/float(TRAIN_LEN),)



