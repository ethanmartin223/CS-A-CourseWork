import random,time
from gen import *
from copy import deepcopy
import math

width = 70
height = 100
rwidth = 40
rheight =20

#Level gen
map_var = cave_level(width, height,density=60,iterations=5,moore_neighbours=5,gold=1,iron=20,copper=10,silver=5)

for y in range(0, len(map_var)):
  for x in range(0, len(map_var[y])):
    print(str(map_var[y][x])+str(map_var[y][x]), end="")
  print()