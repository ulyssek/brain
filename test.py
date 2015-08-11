#!/usr/bin/env python








from CustomModel import BrandAverage


m = BrandAverage(train=True,limit=pow(10,3),talkative=True)

m.build()
m.compute_output()
m.build_max_brands()

if m.score==0.0188557944754317974813147:
  print "It's Working ! "
else:
  dif = float(m.score) - 0.0188557944754317974813147
  print "Huston, we got a situation here (difference : %s)" % (dif,)

