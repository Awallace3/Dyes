import os

filename = open('benchmarks.json','r')
data = filename.readlines()
for i in data:
    if 'name' in i:
        print(i)
    if 'exp' in i:
        print(i)
  #  print(i)