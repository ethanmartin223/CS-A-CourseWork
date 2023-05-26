import tkinter as tk
import random, time
from copy import deepcopy


window=tk.Tk()
window.wm_attributes('-fullscreen', True)
window.configure(background='#faf8ef')
canvas = tk.Canvas(width=650,height=420,bg='#faf8ef',relief='flat',highlightthickness=0)
canvas.place(relx=0.5, rely=0.5, anchor='center')
turn = 0
last_turn = -1
sf= 100
score = 0
bestscore = 0
gameover=False
run_by_self = True

def copyclass(class_,newname):
  return type(f'{newname}', class_.__bases__, dict(class_.__dict__))

def round_rectangle(master,x1, y1, x2, y2, r=25, **kwargs):   
  points = (x1+r, y1, x1+r, y1, x2-r, y1, x2-r, y1, x2, y1, x2, y1+r, x2, y1+r, x2, y2-r, x2, y2-r, x2, y2, x2-r, y2, x2-r, y2, x1+r, y2, x1+r, y2, x1, y2, x1, y2-r, x1, y2-r, x1, y1+r, x1, y1+r, x1, y1)
  return master.create_polygon(points, **kwargs, smooth=True)


colors = {
  2:'#eee4da',
  4: '#ede0c8',
  8: '#f2b179',
  16: '#f59563',
  32: '#f67c5f',
  64: '#f65e3b',
  128: '#edcf72',
  256: '#edcc61',
  512: '#edc850',
  1024: '#edc53f',
  2048: '#edc22e',
  4096: '#3e3933',
}

class Tile:
  instances = []
  def __init__(self):
    global score
    self.value = random.choice([2,4])
    self.color = colors[self.value]
    score+= self.value
    while True:
      self.x = random.randint(0,len(board.grid)-1)
      self.y = random.randint(0,len(board.grid)-1)
      if board.grid[self.y][self.x] == 0:
        break
    self.__class__.instances.append(self)
  def place(self):
    board.grid[self.y][self.x] = self

class Board:
  def __init__(self):
    self.master = [
      [0,0,0,0],
      [0,0,0,0],
      [0,0,0,0],
      [0,0,0,0],
    ]
    self.grid=deepcopy(self.master)

  def move_all_up(self):
    global turn
    for i in range(4):
      for i,v in enumerate(Tile.instances):
        while True:
          try:
            if self.grid[v.y-1][v.x].__class__ == int and v.y-1 >=0:
              v.y-=1
            elif self.grid[v.y-1][v.x].__class__ == Tile and v.y-1 >=0 and self.grid[v.y-1][v.x].value == v.value:
              Tile.instances.remove(v)
              self.grid[v.y-1][v.x].value *= 2
              self.grid[v.y-1][v.x].color = colors[self.grid[v.y-1][v.x].value]
            else:
              break
          except IndexError: 
            break
      board.grid=deepcopy(board.master)
      [v.place() for i,v in enumerate(Tile.instances)]
    turn+=1
  
  def move_all_down(self):
    global turn
    for i in range(4):
      for i,v in enumerate(Tile.instances):
        while True:
          try:
            if self.grid[v.y+1][v.x].__class__ == int and v.y+1 <=len(self.grid):
              v.y+=1
            elif self.grid[v.y+1][v.x].__class__ == Tile and v.y+1 <=len(self.grid) and self.grid[v.y+1][v.x].value == v.value:
              Tile.instances.remove(v)
              self.grid[v.y+1][v.x].value *= 2
              self.grid[v.y+1][v.x].color = colors[self.grid[v.y+1][v.x].value]
            else:
              break
          except IndexError:
            break
      board.grid=deepcopy(board.master)
      [v.place() for i,v in enumerate(Tile.instances)]
    turn+=1

  def move_all_right(self):
    global turn
    for i in range(4):
      for i,v in enumerate(Tile.instances):
        while True:
          try:
            if self.grid[v.y][v.x+1].__class__ == int and v.x+1 <=len(self.grid):
              v.x+=1
            elif self.grid[v.y][v.x+1].__class__ == Tile and v.x+1 <=len(self.grid) and self.grid[v.y][v.x+1].value == v.value:
              Tile.instances.remove(v)
              self.grid[v.y][v.x+1].value *= 2
              self.grid[v.y][v.x+1].color = colors[self.grid[v.y][v.x+1].value]
            else:
              break
          except IndexError:
            break
      board.grid=deepcopy(board.master)
      [v.place() for i,v in enumerate(Tile.instances)]
    turn+=1

  def move_all_left(self):
    global turn
    for i in range(4):
      for i,v in enumerate(Tile.instances):
        while True:
          try:
            if self.grid[v.y][v.x-1].__class__ == int and v.x-1 >=0:
              v.x-=1
            elif self.grid[v.y][v.x-1].__class__ == Tile and v.x-1 >=0 and self.grid[v.y][v.x-1].value == v.value:
              Tile.instances.remove(v)
              self.grid[v.y][v.x-1].value *= 2
              self.grid[v.y][v.x-1].color = colors[self.grid[v.y][v.x-1].value]
            else:
              break
          except IndexError:
            break
        board.grid=deepcopy(board.master)
        [v.place() for i,v in enumerate(Tile.instances)]
    
  def move(self,event):
    key = event.keysym
    if key in ['w','Up']:
      self.move_all_up()
    elif key in ['s','Down']:
      self.move_all_down()
    elif key in ['d','Right']:
      self.move_all_right()
    elif key in ['a','Left']:
      self.move_all_left()
    else:
      pass
c = 0
while True:
  board = Board()
  Tile()
  window.bind('<Key>', board.move)
  while True:
    [v.place() for i,v in enumerate(Tile.instances)]
    round_rectangle(canvas,0,0,420,420,fill='#bbada0',width=12,r=20)
    for y in range(len(board.grid)):
      for x in range(len(board.grid[0])):
        round_rectangle(canvas,x*sf+10,y*sf+10,x*sf+sf+10,y*sf+sf+10,fill='#cdc1b4',outline='#bbada0',width=12,r=20)
    for y in range(len(board.grid)):
      for x in range(len(board.grid[0])):
        if board.grid[y][x].__class__ != int:
          round_rectangle(canvas,x*sf+10,y*sf+10,x*sf+sf+10,y*sf+sf+10,fill=board.grid[y][x].color,outline='#bbada0',r=20,width=12)
          if board.grid[y][x].value in [2,4]:
            canvas.create_text(x*sf+(sf/2)+10,y*sf+(sf/2)+10,text=str(board.grid[y][x].value),font=('Rod', 30,'bold'),fill='#776e65')
          else:
            if len(str(board.grid[y][x].value)) in [1,2]:
              size = 30
            elif len(str(board.grid[y][x].value)) in [3]:
              size = 20
            elif len(str(board.grid[y][x].value)) in [4]:
              size = 10
              
            canvas.create_text(x*sf+(sf/2)+10,y*sf+(sf/2)+10,text=str(board.grid[y][x].value),font=('Rod', size,'bold'),fill='#f9f6f2')
    canvas.create_text(545,25,text=str(2048),font=('Rod', 30,'bold'),fill='#776e65')
    canvas.create_text(545,250,text=str('\nHOW TO PLAY: Use your arrow\nkeys or AWSD keys to move the \ntiles. Tiles with the same number\nmerge into one when they touch.\nAdd them up to reach 2048!\n\n\n\n\n\n\n\n\n\n\n\nOrginal game created by Gabriele\nCirulli.'),font=('Rod', 8),fill='#776e65')
    round_rectangle(canvas,445,60,540,100,outline='#bbada0',fill='#bbada0',r=20)
    round_rectangle(canvas,550,60,645,100,outline='#bbada0',
    fill='#bbada0',r=20)
    canvas.create_text(492,70,text=str('SCORE'),font=('Rod', 8,'bold'),fill='#eee3d3')
    canvas.create_text(597,70,text=str('BEST'),font=('Rod', 8,'bold'),fill='#eee3d3')
    canvas.create_text(493,87,text=str(score),font=('Rod', 10,'bold'),fill='#fbffff')
    canvas.create_text(597,87,text=str(bestscore),font=('Rod', 10,'bold'),fill='#fbffff')
    try:
      flag = False
      for i,v in enumerate(board.grid):
        if 0 in v:
          flag = True
          break
        if i == len(board.grid)-1 and flag == False:
          gameover = True
    except AttributeError:
      pass
    time.sleep(.001)
    window.update()
    if turn>last_turn:
      Tile()
      last_turn = turn
    board.grid=deepcopy(board.master)
    if gameover:
      break
    canvas.delete('all')

  def playagain():
    global gameover,score,turn,last_turn,play_again
    gameover = False
    score = 0
    turn = 0
    last_turn = -1
    for i,v in enumerate(Tile.instances):
      del Tile.instances[i]
    Tile.instances.clear()
    play_again.destroy()

  canvas.create_text(210,150,text='Game Over',font=('Rod', 30,'bold'),fill='#fbffff')
  play_again = tk.Button(canvas,text='PLAY AGAIN',font=('Rod', 8,'bold'),fg='#eee3d3',bg='#786f67',height=2, relief='flat',highlightthickness=0,activebackground='#786f67',activeforeground='#eee3d3',command=playagain)
  round_rectangle(canvas,145,200,265,252,fill='#786f67',r=20)
  play_again.place(x=148,y=205)
  def flat(event): 
      if event.widget is play_again: 
          event.widget.config(relief='flat') 
  window.bind('<Button-1>', flat)

  while gameover:
    window.update()
