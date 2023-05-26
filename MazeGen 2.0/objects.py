import tkinter as tk
import random
import sys
import time
import math

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

class Array2D(object):
  def __init__(self, data):
    self.array = data

  def get_space_score(self, start_coordnate, end_coordnate, final_destination_coordnate):
    sx,sy = start_coordnate
    ex,ey = end_coordnate
    fx,fy = final_destination_coordnate
    h_score = self.get_distance_between(start_coordnate, final_destination_coordnate)*10
    g_score = self.get_distance_between(final_destination_coordnate, end_coordnate)*10
    f_score = g_score + h_score
    return f_score

  def get_distance_between(self, start_coordnate, end_coordnate):
    sx,sy = start_coordnate
    ex,ey = end_coordnate
    return math.sqrt((ex - sx)**2 + (ey - sx)**2)
  
  def a_star_get_path(self, start_coordnate, end_coordnate, can_move_diagonal=True):
    sx,sy = start_coordnate
    ex,ey = end_coordnate
    if can_move_diagonal:
      valid_moves = [(-1,-1),(0,-1),(1,-1),(1,0),(1,1),(0,1),(-1,1),(-1,0)]
    else:
      valid_moves = [(0,-1),(1,0),(0,1),(-1,0)]
    path = [(sy,sx)]
    visited = [(sy,sx)]
    current_x, current_y = sx,sy
    while (current_x,current_y) != (ex,ey):
      current_scores = {}
      for direction in valid_moves:
        current_evaluating = (current_x+direction[0],current_y+direction[1])
        if current_evaluating == (ex,ey):
          path.append(current_evaluating)
          return path
        if ((current_y+direction[1]) > -1) and ((current_x+direction[0])>-1)\
              and ((current_y+direction[1]) < len(self.array)) and ((current_x+direction[0])<len(self.array[0]))\
              and not self.array[current_y+direction[1]][current_x+direction[0]]\
              and current_evaluating not in visited:
          current_scores.update({self.get_space_score((current_x,current_y),current_evaluating,(ex,ey)):current_evaluating})
      if current_scores:
        new_space = current_scores[min(list(current_scores.keys()))]
        current_x, current_y = new_space 
        visited.append((current_x,current_y))
        path.append((current_x,current_y))
      else:
        path.pop(-1)
        current_x,current_y = path[-1]
      