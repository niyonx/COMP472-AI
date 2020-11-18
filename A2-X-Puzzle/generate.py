import random

l = ['1','2','3','4','5','6','7','0']

for i in range(50):
  random.shuffle(l)
  print(" ".join(l))