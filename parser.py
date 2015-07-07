#!/usr/bin/env python
#-*-coding:utf-8-*-

import csv

def parser(file_name, quotechar='\\'):
  csv_file = open(file_name, "rb")
  spam_reader = csv.reader(csv_file, delimiter=';',
    quotechar=quotechar, quoting=csv.QUOTE_MINIMAL)
  return spam_reader
