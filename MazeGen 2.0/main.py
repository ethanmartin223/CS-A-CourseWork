import tkinter as tk
import random
import sys
import time
import math


# start
MAP_HEIGHT = 51
MAP_WIDTH = 51
sf = 10

#window stuff below here
window = tk.Tk()
canvas = tk.Canvas(width=MAP_WIDTH*sf, height=MAP_HEIGHT*sf)
canvas.pack(side='left')
window.wm_attributes('-fullscreen', True)

tilegrid = [[0 for x in range(MAP_WIDTH)] for y in range(MAP_HEIGHT)]
for y in range(MAP_HEIGHT):
    for x in range(MAP_WIDTH):
        tilegrid[y][x] = canvas.create_rectangle(x*sf,y*sf,x*sf+sf,y*sf+sf, fill='black', outline='')


sys.setrecursionlimit(10**6)

class GenerateMaze(object):
    def __init__(self, width, height, starting_point=(1, 1)):
        self.width = width
        self.height = height
        self.grid = [[1 for x in range(width)] for y in range(height)]
        self.starting_point = starting_point
        self.grid[self.starting_point[1]][self.starting_point[0]] = 0
        self.visited_points = [self.starting_point]
        self.path = []
        self.iter_from_last_room = 9
        self.iterations = 0
        self.generate_map()
      
    def generate_map(self):
        self.recurse(*self.starting_point)

    def recurse(self,x,y):
        self.iterations += 1
        possible_directions = [(0,1),(1,0),(0,-1),(-1,0)]
        possible_next_destinations = []
        for i,v in enumerate(possible_directions):
            try:
                if any(map(lambda n: n<0, (x+v[0]*2, y+v[1]*2))) or x+v[0]*2 >= self.width or y+v[1]*2 >= self.height:
                    raise IndexError
                elif (x+v[0], y+v[1]) not in self.visited_points and (x+v[0]*2, y+v[1]*2) not in self.visited_points \
                        and (x+v[0]*3, y+v[1]*3) not in self.visited_points:
                    possible_next_destinations.append(((x+v[0]*2, y+v[1]*2),(x+v[0], y+v[1])))
                else:
                    raise IndexError
            except IndexError:
                pass
          
        if possible_next_destinations:
            next_location = random.choice(possible_next_destinations)
            self.grid[next_location[0][1]][next_location[0][0]] = 0
            self.grid[next_location[1][1]][next_location[1][0]] = 0
            if self.iter_from_last_room > 0:
              self.iter_from_last_room -= 1
            else:
              room_w = random.randrange(4,8,2)
              room_h = random.randrange(4,8,2)
              
              next_room = [[0 for x in range(room_w)] for y in range(room_h)]
              for y in range(room_h):
                for x in range(room_w):
                  if (next_location[0][1]+y > 0) and (next_location[0][0]+x > 0) and (next_location[0][1]+y < self.height) and\
                      (next_location[0][0]+x < self.width):
                    self.grid[next_location[0][1]+y][next_location[0][0]+x] = 0
              self.iter_from_last_room = 29
            self.path.append(next_location[0])
            self.visited_points.append(next_location[0])
            self.recurse(*next_location[0])
          

        else:
            if len(self.path) > 0:
                self.iterations += 1
                backtrack = self.path.pop(-1)
                self.recurse(*backtrack)
            else:
                return


maze_data = GenerateMaze(MAP_WIDTH,MAP_HEIGHT).grid

for y in range(len(maze_data)):
  for x in range(len(maze_data[0])):
    canvas.itemconfig(tilegrid[y][x],fill='black' if maze_data[y][x] else 'white')
  

window.mainloop()