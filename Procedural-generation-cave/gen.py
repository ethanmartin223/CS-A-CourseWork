def cave_level(width, height, density=40, iterations=5,moore_neighbours=4,gold=1,iron=20,copper=10,silver=5):
  import random
  from copy import deepcopy
  global grid
  
  gold_chance = [5 for i in range(gold)]
  gold_chance = gold_chance+[1 for i in range(100-len(gold_chance))]
  silver_chance = [4 for i in range(silver)]
  silver_chance = silver_chance+[1 for i in range(100-len(silver_chance))]
  iron_chance = [3 for i in range(iron)]
  iron_chance = iron_chance+[1 for i in range(100-len(iron_chance))]
  copper_chance = [2 for i in range(copper)]
  copper_chance = copper_chance+[1 for i in range(100-len(copper_chance))]

  def grid(width, height, density):
      chances = [1 for i in range(density)]
      chances = chances+[0 for i in range(100-len(chances))]
      row = []
      grid = []
      for l in range(height):
          for i in range(width):
              if i == 0:
                  row = [' ']
              else:
                  row.append(' ')
          grid.append(row[:])
      i = 0
      for y in range(height):
          for x in range(width):
              grid[y][x] = random.choice(chances)
      return grid
  grid = grid(width, height, density)
  temp_grid = deepcopy(grid)
  rounds = 0
  alive = lambda x: True if x == 1 else False
  def cellDoTurn(x, y):
      global grid
      surounding_alive = 0
      d = [(1, 1), (1, 0), (0, 1), (-1, 0), (1, -1), (-1, 1), (0, -1), (-1, -1)]
      for i, v in enumerate(d):
          try:
              if alive(grid[y + v[0]][x + v[1]]):
                  surounding_alive += 1
          except IndexError:
              pass
      #CONDITIONS
      if surounding_alive >= moore_neighbours:
          temp_grid[y][x] = 4
      if surounding_alive < moore_neighbours:
          temp_grid[y][x] = 3
      #/CONDITIONS
  for i in range(iterations):
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            cellDoTurn(x, y)
    for y in range(len(temp_grid)):
        for x in range(len(temp_grid[0])):
            if temp_grid[y][x] == 3:
                grid[y][x] = 0
            if temp_grid[y][x] == 4:
                grid[y][x] = 1
            if temp_grid[y][x] == 0:
                grid[y][x] = 0
    rounds += 1
    alive_cells = 0
    temp_grid = deepcopy(grid)

  for y in range(len(grid)):
    for x in range(len(grid[0])):
      if grid[y][x] == 1:
        #gold 5, silver 4, iron 3, copper 2
        ore = random.choice(['copper','gold','iron','silver'])
        if ore =='copper':
          grid[y][x] = random.choice(copper_chance)
        if ore =='gold':
          grid[y][x] = random.choice(gold_chance)
        if ore =='iron':
          grid[y][x] = random.choice(iron_chance)
        if ore =='silver':
          grid[y][x] = random.choice(silver_chance)

        
  return grid


def dungeon_level(width, height, roomCount=7, nullSpace=2, DLA_erosion=0):
  import random
  def grid(width, height):
    row = []
    grid = []
    for l in range(height):
        for i in range(width):
            if i == 0:
                row = [0]
            else:
                row.append(0)
        grid.append(row[:])
    i = 0
    for y in range(height):
        for x in range(width):
            grid[y][x] = 0
    return grid
  rooms = [
    grid(15,15),
    grid(10,10),
    grid(9,9),
    grid(8,8),
    grid(7,7),
    grid(6,6),
    grid(5,5),
    grid(4,4),
  ]
  map_var = grid(width, height)
  for y in range(height):
    for x in range(width):
      map_var[y][x] = 1
  non_valid = []
  iterations = 0
  doorways = []
  passed_iterations = 0
  failed_times = 0
  while True:
    room_of_choice = random.choice(rooms)

    while True:
        try_coords = (random.randint(0, width), random.randint(0, height))
        if width - try_coords[0] > len(room_of_choice) and height - try_coords[1] > len(room_of_choice[0]):
            break

    failed = False
    for y in range(try_coords[1] - nullSpace, (try_coords[1] + len(room_of_choice)) + nullSpace):
        for x in range(try_coords[0] - nullSpace, (try_coords[0] + len(room_of_choice[0])) + nullSpace):
            if (x, y) in non_valid:
                failed = True
                passed_iterations += 1
            else:
                pass
    if passed_iterations >= 50:
        map_var = grid(width, height)
        for y in range(height):
          for x in range(width):
            map_var[y][x] = 1
        non_valid = []
        iterations = 0
        doorways = []
        passed_iterations = 0

    if failed == False:
        iterations += 1
        for y in range(try_coords[1], (try_coords[1] + len(room_of_choice))):
            for x in range(try_coords[0], (try_coords[0] + len(room_of_choice[0]))):
                map_var[y][x] = room_of_choice[y - try_coords[1]][
                    x - try_coords[0]]
                non_valid.append((x, y))
            doorways.append((x-int(len(room_of_choice[0])/2), y-int(len(room_of_choice)/2)))

    if iterations == roomCount:
        break

  def getStepsNeeded(xy1, xy2):
      steps = []
      y1 = xy1[1]
      x1 = xy1[0]
      y2 = xy2[1]
      x2 = xy2[0]
      while x2 > x1:
              x1 += 1
              steps.append((x1, y1))
      while x1 > x2:
              x1 -= 1
              steps.append((x1, y1))
      while y1 < y2:
              y1 += 1
              steps.append((x1, y1))
      while y2 < y1:
              y1 -= 1
              steps.append((x1, y1))
      return steps

  for i,v in enumerate(doorways):
    try:
      steps = getStepsNeeded(v,doorways[i+1])
      for i, v in enumerate(steps):
        map_var[v[1]][v[0]] = 3
    except IndexError:
      pass
  
  for y in range(len(map_var)):
    for x in range(len(map_var[0])):
      if map_var[y][x] == 3:
        surounding_3 = 0
        d = [(1, 0), (0, 1), (-1, 0),(0, -1)]
        for i, v in enumerate(d):
          try:
              if y + v[0] < 0:
                surounding_3 -=1
              elif x + v[1] < 0:
                surounding_3 -=1
              elif map_var[y + v[0]][x + v[1]] == 3:
                  surounding_3 += 1
              elif map_var[y + v[0]][x + v[1]] == 0:
                  surounding_3 += 1
          except IndexError:
              surounding_3 -=1
              pass
        if surounding_3 < 2:
          map_var[y][x] = 1
  return map_var