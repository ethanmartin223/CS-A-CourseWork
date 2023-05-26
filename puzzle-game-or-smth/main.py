from copy import deepcopy
import tkinter as tk
import time
from PIL import ImageTk, Image, ImageFilter 
from functools import partial
import math

# ----------------- FUNCTIONS FOR LEVEL --------------#
def makeGrid(width, height):
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
    return grid

def playfn(filename, nodisplay=True, autoexit=True, stdout=False):
    from subprocess import call
    import threading
    procces_list = ['ffplay']
    if nodisplay:
      procces_list.append('-nodisp')
    if autoexit:
      procces_list.append('-autoexit')
    if not stdout:
      procces_list.append('-loglevel')
      procces_list.append('quiet')
    procces_list.append(filename)
    process = lambda: call(procces_list)
    th = threading.Thread(target=process, daemon=True)
    th.start()

# ------------------- WINDOW CREATION -----------------#
window = tk.Tk()
window.attributes('-fullscreen', True)
window.configure(background='black')

# ------------------------- VARS ----------------------#
width=height= 8
grid = makeGrid(width, height)
sf = 35 # scalefactor of each pixel -needs to be global for most functions, check when creating new class
mapStuff = []
master = deepcopy(grid)
turn = 0
lastTurn = -1
enemyLastTurn = -1
level = 1
sawframe = 0
sawblade_frames = [f'frame_{i}' for i in range(9)]

# ------------------- PLAYED BEFORE CHECK -------------#
try:
  cookielog = open('cookie_log.py','r')
except FileNotFoundError:
  cookielog = open('cookie_log.py','w')
  cookielog.write('hasplayedbefore = False\nhighestlvl = 1')
finally:
  cookielog.close()
  from cookie_log import hasplayedbefore, highestlvl
  lvlsdone = []
  [lvlsdone.append(v) for v in range(highestlvl+1)]
  hasplayed = hasplayedbefore


#-------------------------IMAGES-----------------------#
PLAYER_IMG_UP = ImageTk.PhotoImage(Image.open(fp='images/player.png')
.resize((sf+1, sf+1), Image.NEAREST))
PLAYER_IMG_LEFT = ImageTk.PhotoImage(Image.open(fp='images/player.png').resize((sf+1, sf+1), Image.NEAREST).rotate(90))
PLAYER_IMG_DOWN = ImageTk.PhotoImage(Image.open(fp='images/player.png').resize((sf+1, sf+1), Image.NEAREST).rotate(180))
PLAYER_IMG_RIGHT = ImageTk.PhotoImage(Image.open(fp='images/player.png').resize((sf+1, sf+1), Image.NEAREST).rotate(270))
PLAYER_IMG_IDLE = ImageTk.PhotoImage(Image.open(fp='images/old_player.png').resize((sf+1, sf+1), Image.NEAREST))
BOX_IMG = ImageTk.PhotoImage(Image.open(fp='images/box.png').resize((sf+1, sf+1), Image.NEAREST))
RED_SWITCH_IMG = ImageTk.PhotoImage(Image.open(fp='images/red_switch.png').resize((sf+1, sf+1), Image.NEAREST))
BLUE_SWITCH_IMG = ImageTk.PhotoImage(Image.open(fp='images/blue_switch.png').resize((sf+1, sf+1), Image.NEAREST))
GREEN_SWITCH_IMG = ImageTk.PhotoImage(Image.open(fp='images/green_switch.png').resize((sf+1, sf+1), Image.NEAREST))
RED_DOOR_IMG = ImageTk.PhotoImage(Image.open(fp='images/red_door.png').resize((sf+1, sf+1), Image.NEAREST))
BLUE_DOOR_IMG = ImageTk.PhotoImage(Image.open(fp='images/blue_door.png').resize((sf+1, sf+1), Image.NEAREST))
GREEN_DOOR_IMG = ImageTk.PhotoImage(Image.open(fp='images/green_door.png').resize((sf+1, sf+1), Image.NEAREST))
SAW_IMG = ImageTk.PhotoImage(Image.open(fp='images/saw-gif/frame_0.png').resize((sf+1, sf+1), Image.NEAREST))
WALL_IMG = ImageTk.PhotoImage(Image.open(fp='images/wall.png').resize((sf+1, sf+1), Image.NEAREST))
WATER_IMG = ImageTk.PhotoImage(Image.open(fp='images/water.png').resize((sf+1, sf+1), Image.NEAREST))
STAIRS_IMG = ImageTk.PhotoImage(Image.open(fp='images/stairs.png').resize((sf+1, sf+1), Image.NEAREST).rotate(90))
SUNK_BOX_IMG = ImageTk.PhotoImage(Image.open(fp='images/submurged_box.png').resize((sf+1, sf+1), Image.NEAREST))
RAFT_IMG = ImageTk.PhotoImage(Image.open(fp='images/raft.png').resize((sf+1, sf+1), Image.NEAREST))
DISABLED_LVL_IMG = ImageTk.PhotoImage(Image.open(fp='images/level_locked.png').resize((sf+1, sf+1), Image.NEAREST))
SUPRISED_PLAYER_IMG = ImageTk.PhotoImage(Image.open(fp='images/suprised_player.png').resize((sf+1, sf+1), Image.NEAREST))
EMITTER_IMG_RIGHT = ImageTk.PhotoImage(Image.open(fp='images/laser_emmiter.png').resize((sf+1, sf+1), Image.NEAREST))
EMITTER_IMG_DOWN = ImageTk.PhotoImage(Image.open(fp='images/laser_emmiter.png').resize((sf+1, sf+1), Image.NEAREST).rotate(-90))
EMITTER_IMG_UP = ImageTk.PhotoImage(Image.open(fp='images/laser_emmiter.png').resize((sf+1, sf+1), Image.NEAREST).rotate(90))
EMITTER_IMG_LEFT = ImageTk.PhotoImage(Image.open(fp='images/laser_emmiter.png').resize((sf+1, sf+1), Image.NEAREST).rotate(180))
ORANGE_PORTAL_IMG = ImageTk.PhotoImage(Image.open(fp='images/orange_portalv1.png').resize((sf+1, sf+1), Image.NEAREST))
METAL_BOX_IMG = ImageTk.PhotoImage(Image.open(fp='images/metal_box.png').resize((sf+1, sf+1), Image.NEAREST))
PLAY_BUTTON_IMG = ImageTk.PhotoImage(Image.open(fp='images/play_button.png').resize((sf*2, sf*2), Image.NEAREST)) 
TITLE_IMG = ImageTk.PhotoImage(Image.open(fp='images/title.png').resize((256,128), Image.NEAREST)) 
SUNK_METAL_BOX_IMG = ImageTk.PhotoImage(Image.open(fp='images/sunken_metal_box.png').resize((sf+1, sf+1), Image.NEAREST))
# --------------------STARTSCREEN -------------------- #
pixel1 = 'Ariel'
continue_start = True

def exitStart():
  global continue_start
  continue_start = False

startscreen = tk.Canvas(window, width=sf * width + (sf * 2), height=sf * width + (sf * 2), bg='#2B2A2A', bd=0, highlightthickness=0)
startscreen.place(relx=.5,rely=.5,anchor='center')
play = tk.Button(startscreen,relief='flat',image=PLAY_BUTTON_IMG, bd=0, command=exitStart, activebackground='#2e332f', bg='#2e332f')
play.config(highlightbackground='#2B2A2A')
i = 0
down = False
while continue_start:
  PLAY_BUTTON_IMG = ImageTk.PhotoImage(Image.open(fp='images/play_button.png').resize((sf*2+i, sf*2+i), Image.NEAREST)) 
  play.config(image=PLAY_BUTTON_IMG)
  startscreen.create_rectangle(0,0,sf*width+sf*2,sf*height+sf*2,fill='#2B2A2A')
  startscreen.create_image(40,40,image=TITLE_IMG,anchor='nw')
  play.place(relx=.5,rely=.8,anchor='center')
  play.update()
  time.sleep(.001)
  window.update()

play.destroy()

for i in range(int((width*sf+sf*2)/2)):
  startscreen.create_rectangle(0,0,i,sf*height+sf*2,fill='black')
  startscreen.create_rectangle(width*sf+sf*2,0,width*sf+sf*2-i,sf*height+sf*2,fill='black')
  window.update()
  #time.sleep(.0001)
  startscreen.delete('all')

startscreen.delete('all')
play.destroy()

for i in range(int((width*sf+sf*2)/2)):
  startscreen.create_rectangle(0,0,((width*sf+sf*2)/2)-i,sf*height+sf*2,fill='black')
  startscreen.create_rectangle(((width*sf+sf*2)/2)+i,0,((width*sf+sf*2)),sf*height+sf*2,fill='black')
  window.update()
  #time.sleep(.0001)
  startscreen.delete('all')

startscreen.create_text(150,20,text=f'Levels',font=(pixel1, 20))
continue_start = True


def selectLevel(lvl):
  global continue_start, level
  level = lvl
  continue_start = False

lvlid = 1
pix = tk.PhotoImage(width=sf, height=sf)
buttons = []
locate = []
for y in range(5):
  for x in range(5):
    temp = partial(selectLevel, lvlid)
    if (lvlid in lvlsdone) or (lvlsdone==[] and lvlid==1):
      buttons.append(tk.Button(startscreen, activebackground='#515c54', bg='#2e332f', padx=0, pady=0, text=lvlid, command=temp,image=pix, compound='c',highlightbackground='#515c54',relief='solid',state='normal'))
      locate.append((x*60+30,y*60+50))
    else:
      tk.Button(startscreen, activebackground='#515c54', bg='#2e332f',state='disabled',image=DISABLED_LVL_IMG,relief='solid',highlightbackground='#515c54').place(x=x*60+30,y=y*60+50)
    lvlid += 1

for i,v in enumerate(buttons):
  v.place(x=locate[i][0], y=locate[i][1])
  v['state']= 'normal'

while continue_start:
  window.update()
startscreen.delete('all')
startscreen.destroy()
startscreen = tk.Canvas(window, width=sf * width + (sf * 2), height=sf * width + (sf * 2), bg='#2B2A2A', bd=0, highlightthickness=0)
startscreen.place(relx=.5,rely=.5,anchor='center')

for i in range(int((width*sf+sf*2)/2)):
  startscreen.create_rectangle(0,0,i,sf*height+sf*2,fill='black')
  startscreen.create_rectangle(width*sf+sf*2,0,width*sf+sf*2-i,sf*height+sf*2,fill='black')
  window.update()
  #time.sleep(.0001)
  startscreen.delete('all')

for i in range(int((width*sf+sf*2)/2)):
  startscreen.create_rectangle(0,0,((width*sf+sf*2)/2)-i,sf*height+sf*2,fill='black')
  startscreen.create_rectangle(((width*sf+sf*2)/2)+i,0,((width*sf+sf*2)),sf*height+sf*2,fill='black')
  window.update()
  #time.sleep(.0001)
  startscreen.delete('all')
startscreen.destroy()
# ----------------TK GAME CONTAINERS ------------------#
frame = tk.LabelFrame(width=sf * width + (sf * 2), height=sf * width + (sf * 2), bg='#3D3D3D', bd=0)
[[tk.Label(frame,image=WALL_IMG, bd=0).place(x=x*sf,y=y*sf) for x in range(len(grid[0])+2)] for y in range(len(grid)+2)]
frame.place(relx=.5,rely=.5,anchor='center')
screen = tk.Canvas(frame, bg='black', width=sf * width, height=sf * height, highlightthickness=0)
screen.place(x=sf, y=sf)

# ----------------------- OBJECTS ---------------------#
class Wall:
  def __init__(self, xy, multiassign=False):
    self.multiassign = multiassign
    if not self.multiassign:
      self.x = xy[0]
      self.y = xy[1]
    else: 
      self.locations = xy
  def place(self):
    if self.multiassign:
      for i,v in enumerate(self.locations):
        grid[v[1]][v[0]] = self
    else:
      grid[self.y][self.x] = self

class Box:
  instances = []
  def __init__(self, xy):
    self.destroyed = False
    self.x = xy[0]
    self.y = xy[1]
    self.__class__.instances.append(self)
  def place(self):
    if not self.destroyed:
      grid[self.y][self.x] = self

class MetalBox:
  instances = []
  def __init__(self, xy):
    self.destroyed = False
    self.x = xy[0]
    self.y = xy[1]
    self.__class__.instances.append(self)
  def place(self):
    if not self.destroyed:
      grid[self.y][self.x] = self

class Floor:
  def __init__(self, x, y):
    self.x = x
    self.y = y
  def place(self):
    grid[self.y][self.x] = self


class Water:
  def __init__(self, xy, multiassign=False):
    self.multiassign = multiassign
    if not self.multiassign:
      self.x = xy[0]
      self.y = xy[1]
    else: 
      self.locations = xy
  def place(self):
    if self.multiassign:
      for i,v in enumerate(self.locations):
        grid[v[1]][v[0]] = self
    else:
      grid[self.y][self.x] = self

class SunkenBox:
  instances = []
  def __init__(self, xy):
    self.__class__.instances.append(self)
    self.x = xy[0]
    self.y = xy[1]
  def place(self):
    grid[self.y][self.x] = self

class SunkenMetalBox:
  instances = []
  def __init__(self, xy):
    self.__class__.instances.append(self)
    self.x = xy[0]
    self.y = xy[1]
  def place(self):
    grid[self.y][self.x] = self

class Player:
    def __init__(self):
        self.direction = None
        self.x = 6
        self.y = 6
        self.dead = False
        self.last_move = None
    
    #move player
    def move(self, event):
      global turn
      stepable = (Floor, Switch, OpenDoor, SawBlade, Goal, SunkenBox, Raft, Portal)
      pushable = (Box, MetalBox)

      #lazy pass out of bounds movment 
      try: 
        #get keysym (key pressed details)
        if event.keysym in ['Up', 'Down', 'Left', 'Right','w','a','s','d']:
          self.direction = event.keysym
          #move up
          if self.direction in ['Up','w']:
            self.last_move = 'Up'
            #Move just player
            if grid[self.y-1][self.x].__class__ in stepable and self.y-1 > -1:
              self.y -= 1
              turn += 1
            #move player and box
            elif grid[self.y-1][self.x].__class__ in pushable and grid[self.y - 2][self.x].__class__ in stepable and self.y-2 > -1:
              grid[self.y-1][self.x].y -= 1 
              self.y -= 1
              turn += 1
            #push box onto water
            elif grid[self.y-1][self.x].__class__ is Box and grid[self.y - 2][self.x].__class__ is (Water) and self.y-2 > -1:
              grid[self.y-1][self.x].destroyed = True
              grid[self.y-2][self.x] = SunkenBox((grid[self.y-2][self.x].x,grid[self.y-2][self.x].y))
              self.y -= 1
              turn += 1   
            elif grid[self.y-1][self.x].__class__ is MetalBox and grid[self.y - 2][self.x].__class__ is (Water) and self.y-2 > -1:
              grid[self.y-1][self.x].destroyed = True
              grid[self.y-2][self.x] = SunkenMetalBox((grid[self.y-2][self.x].x,grid[self.y-2][self.x].y))
              self.y -= 1
              turn += 1   
        
          #move down
          if self.direction in ['Down','s']:
            self.last_move = 'Down'
            if grid[self.y + 1][self.x].__class__ in stepable:
              self.y += 1
              turn += 1
            elif grid[self.y + 1][self.x].__class__ in pushable and grid[self.y + 2][self.x].__class__ in stepable:
              grid[self.y+1][self.x].y += 1 
              self.y += 1
              turn += 1
            elif grid[self.y+1][self.x].__class__ is Box and grid[self.y + 2][self.x].__class__ is (Water):
              grid[self.y+1][self.x].destroyed = True
              grid[self.y+2][self.x] = SunkenBox((grid[self.y+2][self.x].x,grid[self.y+2][self.x].y))
              self.y += 1
              turn += 1
            elif grid[self.y+1][self.x].__class__ is MetalBox and grid[self.y + 2][self.x].__class__ is (Water):
              grid[self.y+1][self.x].destroyed = True
              grid[self.y+2][self.x] = SunkenMetalBox((grid[self.y+2][self.x].x,grid[self.y+2][self.x].y))
              self.y += 1
              turn += 1
          
          #move right
          if self.direction in ['Right','d']:
            self.last_move = 'Right'
            if grid[self.y][self.x + 1].__class__ in stepable:
              self.x += 1
              turn += 1
            elif grid[self.y][self.x + 1].__class__ in pushable and grid[self.y][self.x + 2].__class__ in stepable:
              grid[self.y][self.x + 1].x += 1 
              self.x += 1
              turn += 1
            elif grid[self.y][self.x+1].__class__ is Box and grid[self.y][self.x+2].__class__ is (Water):
              grid[self.y][self.x+1].destroyed = True
              grid[self.y][self.x+2] = SunkenBox((grid[self.y][self.x+2].x,grid[self.y][self.x+2].y))
              self.x += 1
              turn += 1
            elif grid[self.y][self.x+1].__class__ is MetalBox and grid[self.y][self.x+2].__class__ is (Water):
              grid[self.y][self.x+1].destroyed = True
              grid[self.y][self.x+2] = SunkenMetalBox((grid[self.y][self.x+2].x,grid[self.y][self.x+2].y))
              self.x += 1
              turn += 1
          
          #move left
          if self.direction in ['Left','a']:
            self.last_move = 'Left'
            if grid[self.y][self.x - 1].__class__ in stepable and self.x-1 > -1:
              self.x -= 1
              turn += 1
            elif grid[self.y][self.x - 1].__class__ in pushable and grid[self.y][self.x - 2].__class__ in stepable and self.x-2 > -1:
              grid[self.y][self.x - 1].x -= 1 
              self.x -= 1
              turn += 1
            elif grid[self.y][self.x-1].__class__ is Box and grid[self.y][self.x-2].__class__ is (Water):
                grid[self.y][self.x-1].destroyed = True
                grid[self.y][self.x-2] = SunkenBox((grid[self.y][self.x-2].x,grid[self.y][self.x-2].y))
                self.x -= 1
                turn += 1
            elif grid[self.y][self.x-1].__class__ is MetalBox and grid[self.y][self.x-2].__class__ is (Water):
                grid[self.y][self.x-1].destroyed = True
                grid[self.y][self.x-2] = SunkenMetalBox((grid[self.y][self.x-2].x,grid[self.y][self.x-2].y))
                self.x -= 1
                turn += 1

        #space to skip turn
        elif event.keysym == 'space':
          turn += 1
          self.direction = None
          self.last_move = None
        
        #r to restart
        elif event.keysym == 'r':
          player.dead = True

      #lazy catch-all
      except IndexError:
        pass
        
class Switch:
  instances = [] 
  def __init__(self, xy, id, switchtype):
    self.__class__.instances.append(self)
    self.x = xy[0]
    self.y = xy[1]
    self.paired_id = id
    self.state = False
    self.switchtype = switchtype.lower() 
    if self.switchtype == 'red':
      self.switchtype = RED_SWITCH_IMG
    elif self.switchtype == 'green':
      self.switchtype = GREEN_SWITCH_IMG
    elif self.switchtype == 'blue':
      self.switchtype = BLUE_SWITCH_IMG
  def place(self):
    grid[self.y][self.x] = self
  def is_activated(self):
    if grid[self.y][self.x].__class__ not in (Box, MetalBox) and grid[self.y][self.x] != 1:
      return True
    else:
      return False
  def activated_command(self):
    self.paired_id

class Door:
  def __init__(self, xy, id, doortype):
    self.x = xy[0]
    self.y = xy[1]
    self.is_open = False
    self.id = id
    self.doortype = doortype.lower() 
    if self.doortype == 'red':
      self.doortype = RED_DOOR_IMG
    elif self.doortype == 'green':
      self.doortype = GREEN_DOOR_IMG
    elif self.doortype == 'blue':
      self.doortype = BLUE_DOOR_IMG
  def place(self):
    grid[self.y][self.x] = self

class OpenDoor:
  def __init__(self, xy, id):
    self.x = xy[0]
    self.y = xy[1]
    self.is_open = False
    self.id = id
  def place(self):
    grid[self.y][self.x] = self

class SawBlade:
  instances = []
  def __init__(self, steps, loop=True):
    self.x = steps[0][0]
    self.y = steps[0][1]
    self.steps = steps
    self.i=0
    self.loop = loop
    self.__class__.instances.append(self)
    if self.loop:
      temp = deepcopy(steps)
      temp.pop(-1)
      temp.pop(0)
      temp.reverse()
      [self.steps.append(v) for i,v in enumerate(temp)]
  def place(self):
    grid[self.y][self.x] = self
    global turn,lastTurn
    if turn > lastTurn:
      self.i += 1
      if self.i >= len(self.steps):
        self.i = 0
  def move(self):
    v = self.steps[self.i]
    if grid[v[1]][v[0]].__class__ == Box:
      grid[v[1]][v[0]].destroyed = True
    self.x = v[0]
    self.y = v[1]
  
class Goal:
  def __init__(self, x, y):
    self.x = x
    self.y = y
  def place(self):
    grid[self.y][self.x] = self

class Raft:
  instances = []
  def __init__(self, steps):
    self.x = steps[0][0]
    self.y = steps[0][1]
    self.steps = steps
    self.i=0
    self.__class__.instances.append(self)
    temp = deepcopy(steps)
    temp.pop(-1)
    temp.pop(0)
    temp.reverse()
    [self.steps.append(v) for i,v in enumerate(temp)]
  def place(self):
    grid[self.y][self.x] = self
    global turn, lastTurn
    if turn > lastTurn:
      self.i += 1
      if self.i >= len(self.steps):
        self.i = 0
  def move(self):
    v = self.steps[self.i]
    self.x = v[0]
    self.y = v[1]

class Portal:
  instances = []
  def __init__(self,xy,id,color):
    self.x = xy[0]
    self.y = xy[1]
    self.color = color
    self.is_open = False
    self.id = id
    self.__class__.instances.append(self)
  def place(self):
    grid[self.y][self.x] = self

class Emitter:
  instances = []
  def __init__(self, xy,direction):
    self.x = xy[0]
    self.y = xy[1]
    self.__class__.instances.append(self)
    self.direction = direction.upper()
  def place(self):
    global player
    passable = [Floor, Water, OpenDoor,Raft]
    grid[self.y][self.x] = self
    for i in range(len(grid)):
      if self.direction == 'UP': #The +1 in [self.y-1-i] is so it does not include the emmiter in checking
        if (self.y-i,self.x) == (player.y,player.x):
          player.dead = True
        elif grid[self.y-1-i][self.x].__class__ == Box :
          grid[self.y-1-i][self.x].destroyed = True
        elif grid[self.y-1-i][self.x].__class__ not in passable:
          screen.create_line((self.x)*sf+int(sf/2),(self.y)*sf,(self.x)*sf+int(sf/2),(self.y-1-i)*sf+sf,fill='red',width=5)
          break     
      elif self.direction == 'LEFT':
        if (self.y,self.x-i) == (player.y,player.x):
          player.dead = True
        elif grid[self.y][self.x-1-i].__class__ == Box :
          grid[self.y][self.x-1-i].destroyed = True
        elif grid[self.y][self.x-1-i].__class__ not in passable:
          screen.create_line((self.x)*sf,(self.y)*sf+int(sf/2),(self.x-i)*sf,self.y*sf+int(sf/2),fill='red',width=5)
          break   
      elif self.direction == 'DOWN':
          try:
            if (self.y+i,self.x) == (player.y,player.x):
              player.dead = True
            elif grid[self.y+i+1][self.x].__class__ == Box :
              grid[self.y+i+1][self.x].destroyed = True
            elif grid[self.y+i+1][self.x].__class__ not in passable:
              screen.create_line((self.x)*sf+int(sf/2),(self.y+1)*sf,(self.x)*sf+int(sf/2),(self.y+i)*sf+sf,fill='red',width=5)
              break
          except IndexError:
            screen.create_line((self.x)*sf+int(sf/2),(self.y+1)*sf,(self.x)*sf+int(sf/2),(self.y+i)*sf+sf,fill='red',width=5)
            break
      elif self.direction == 'RIGHT':
        try:
          if (self.y,self.x+i) == (player.y,player.x):
            player.dead = True
          elif grid[self.y][self.x+i+1].__class__ == Box :
            grid[self.y][self.x+i+1].destroyed = True
          elif grid[self.y][self.x+i+1].__class__ not in passable:
            screen.create_line((self.x+1)*sf,(self.y)*sf+int(sf/2),(self.x+i+1)*sf,(self.y)*sf+int(sf/2),fill='red',width=5)
            break
        except IndexError:
          screen.create_line((self.x+1)*sf,(self.y)*sf+int(sf/2),(self.x+i+1)*sf,(self.y)*sf+int(sf/2),fill='red',width=5)
          break
          
class Enemy:
  instances = []
  def __init__(self, xy,direction):
    self.x = xy[0]
    self.y = xy[1]
    self.direction = None
    self.dead = False
    self.__class__.instances.append(self)
  def move(self):
    global player
    stepable = (Floor, Switch, OpenDoor, SawBlade, Goal, SunkenBox, Raft, Portal,int)
    if player.x> self.x and grid[self.y][self.x+1].__class__ in stepable: 
      self.x += 1
    elif player.x < self.x and grid[self.y][self.x-1].__class__ in stepable:
      self.x -= 1
    elif player.y > self.y and grid[self.y+1][self.x].__class__ in stepable:
      self.y += 1
    elif player.y < self.y and grid[self.y-1][self.x].__class__ in stepable:
      self.y -= 1
    if (player.x,player.y) == (self.x,self.y):
      player.dead = True
  def place(self):
    grid[self.y][self.x] = self
  
# ----------------------- LEVEL CREATOR -------------------------#
def createLevel(dgrid):
  dmapstuff = []
  for y in range(len(grid)):
    for x in range(len(grid[0])):
      if dgrid[y][x].__class__ != Raft:
        if dgrid[y][x] == 1:
          dmapstuff.append(Wall((x,y)))
        elif dgrid[y][x] == 2:
          dmapstuff.append(Water((x,y)))
        elif dgrid[y][x] == 3:
          dmapstuff.append(Box((x,y)))
  return dmapstuff

#img assigning
imgs = {
  Wall:WALL_IMG,
  Box:BOX_IMG,
  Water:WATER_IMG,
  Goal:STAIRS_IMG,
  Raft:RAFT_IMG,
  SunkenBox:SUNK_BOX_IMG,
  MetalBox:METAL_BOX_IMG,
  SunkenMetalBox:SUNK_METAL_BOX_IMG
}
while True:        
  # ------------------- SAVE PROGRESS -------------------#
  if level > highestlvl:
    cookielog = open('cookie_log.py','w')
    cookielog.write(f'hasplayedbefore = True\nhighestlvl = {level}')
    cookielog.close()

  # ----------------------- MAP -------------------------#
  #SWITCHES HAVE TO BE FIRST!!!
  player = Player()
  screen.bind('<Key>', player.move)
  screen.focus_set()

  #level 1
  if level == 1:
    goal = Goal(6,5) 
    player.x, player.y = (0,0)
    mapstuff = createLevel([
      [0,1,1,0,0,0,0,0],
      [0,1,0,0,1,0,1,1],
      [0,1,1,0,1,0,0,0],
      [0,0,0,0,1,0,1,0],
      [0,1,1,0,1,1,1,0],
      [1,1,0,0,0,1,0,0],
      [0,1,0,1,0,1,1,1],
      [0,0,0,1,0,0,0,0],
    ])
  

  #level 2
  if level == 2:
    goal = Goal(1,1)
    player.x, player.y = (6,5)
    mapstuff = createLevel([
      [1,1,1,1,1,1,1,1],
      [1,0,1,0,0,3,0,1],
      [0,0,1,1,0,1,0,1],
      [0,0,0,1,0,1,0,1],
      [3,0,0,1,0,1,0,1],
      [3,3,3,1,3,1,0,1],
      [0,0,0,0,0,1,1,1],
      [1,1,1,1,0,1,1,1],
    ])
    
  
  #level 3
  if level == 3:
    goal = Goal(6,6)
    player.x, player.y = (1,1)
    mapstuff = createLevel([
      [1,0,0,0,0,1,1,1],
      [1,0,1,1,0,1,1,1],
      [1,1,1,1,0,0,1,1],
      [0,0,3,1,3,0,1,1],    
      [3,0,0,0,3,0,1,1],
      [0,3,0,1,3,1,1,1],
      [1,0,1,1,0,1,0,1],
      [0,0,0,0,0,0,0,0],
    ])
    mapstuff = [
      Switch((4,7),'id','red'),
      Door((1,6),'id','red')
    ]+mapstuff


  #level 4
  if level == 4:
    goal = Goal(0,0)
    player.x, player.y = (6,6)
    mapstuff = createLevel([
      [0,1,1,0,0,0,1,1],
      [0,1,1,0,1,3,1,1],
      [0,1,0,0,0,0,0,0],
      [0,0,0,3,0,0,0,0],
      [1,0,1,1,1,0,1,1],
      [0,0,1,1,0,0,0,0],
      [0,0,3,0,0,0,0,0],
      [0,0,1,1,0,0,0,0],
    ])
    mapstuff = [
      Switch((7,3),'id1','red'),
      Switch((5,6),'id','blue'),
      Switch((1,6),'id2','green'),
      Door((0,1),'id2','green'),
      Door((0,3),'id1','red'),
      Door((1,4),'id','blue'),
      Door((3,1),'id','blue'),
      Door((3,6),'id1','red'),
      Door((0,2),'id','blue'),
    ]+mapstuff


  #level 5
  if level == 5:
    goal = Goal(5,7)
    player.x, player.y = (0,0)
    mapstuff = createLevel([
      [0,0,0,1,1,1,1,1],
      [1,1,0,1,1,1,1,1],
      [0,0,0,0,0,0,0,0],
      [1,1,1,1,1,0,1,1],
      [0,0,0,0,0,0,0,0],
      [1,1,0,1,1,1,1,1],
      [0,0,0,0,0,0,0,0],
      [1,1,1,1,1,0,1,1],
    ])
    mapstuff = [
      SawBlade([(0,2),(1,2),(2,2),(3,2),(4,2),(5,2),(6,2),(7,2)]),
      SawBlade([(7,4),(6,4),(5,4),(4,4),(3,4),(2,4),(1,4),(0,4)]),
      SawBlade([(0,6),(1,6),(2,6),(3,6),(4,6),(5,6),(6,6),(7,6)])
    ]+mapstuff


  #level 6
  if level == 6:
    goal = Goal(6,0)
    player.x, player.y = (5,7)
    mapstuff = createLevel([
      [0,0,0,0,0,0,0,2],
      [2,2,0,0,0,2,2,2],
      [2,2,2,2,2,2,2,2],
      [2,2,2,2,2,2,2,2],
      [2,2,2,2,2,2,2,2],
      [2,2,0,0,3,2,2,2],
      [2,0,3,3,0,0,0,2],
      [0,0,0,0,0,0,0,2],
    ])
    mapstuff = [
    ]+mapstuff
  

  #level 7 
  if level == 7:
    goal = Goal(0,0)
    player.x, player.y = (6,0)
    mapstuff = createLevel([
      [0,0,0,0,0,0,0,1],
      [1,1,1,0,1,1,1,1],
      [2,2,1,0,1,2,2,0],
      [2,1,1,0,1,1,2,3],
      [2,1,0,0,0,1,2,3],
      [2,1,1,0,1,1,2,0],
      [2,2,1,1,1,2,2,3],
      [3,2,2,2,2,2,3,3],
    ])
    mapstuff = [
      Switch((3,4), 'minetrap', 'red'),
      OpenDoor((4,4), 'minetrap'),
      OpenDoor((2,4), 'minetrap'),
      OpenDoor((3,3), 'minetrap'),
      OpenDoor((3,5), 'minetrap'),
      ]+mapstuff
  
  
  #level 8  
  if level == 8:
    goal = Goal(7,7)
    player.x, player.y = (0,0)
    mapstuff = createLevel([
      [0,0,0,0,0,0,2,2],
      [0,0,0,0,0,0,2,2],
      [0,2,0,0,0,0,0,0],
      [0,0,0,0,0,0,0,0],
      [0,0,0,0,0,0,0,0],
      [0,0,0,0,0,0,2,0],
      [0,0,0,0,0,0,0,0],
      [0,0,0,0,0,0,0,0],
    ])
    mapstuff = [
      Switch((3,4), 'minetrap', 'red'),
      Door((3,7), 'minetrap', 'red'),
      MetalBox((3,3)),
      Box((3,0)),
      Box((4,4)),
      Emitter((2,4),'down'),
    ]+mapstuff

  #level 9 
  if level == 9:
    goal = Goal(6,3)
    player.x, player.y = (7,7)
    mapstuff = createLevel([
      [1,0,0,0,0,0,0,1,0],
      [0,0,1,0,1,1,0,0,0],
      [0,1,1,1,1,1,1,0,0],
      [0,1,1,2,2,1,4,0,0],
      [0,0,1,2,2,1,1,0,0],
      [0,1,1,1,1,1,1,3,0],
      [0,0,1,1,0,1,0,0,0],
      [1,0,0,0,0,0,0,0,0],
      [1,0,0,0,0,0,0,1,0],
    ])
    mapstuff = [
     
     ]+mapstuff
    
  # ------------------- GAME MAINLOOP -------------------#
  while True:
    [[Floor(x,y).place() for x in range(width)] for y in range(height)]    
    goal.place()
    [x.place() if x.__class__ != (Raft) else 0 for x in mapstuff]
    grid[player.y][player.x] = 1
      
    
    #check if switches are pressed
    for i,v in enumerate(Switch.instances):
      if v.is_activated():
        pass
      else:
        for g,j in enumerate(mapstuff):
          try:
            if j.id == v.paired_id:
              if j.__class__ == Door:
                  grid[j.y][j.x] = OpenDoor((v.y,v.x),j.id) 
              elif j.__class__ == OpenDoor:
                if v.switchtype == RED_SWITCH_IMG:
                  grid[j.y][j.x] = Door((v.y,v.x),j.id,'red') 
                elif v.switchtype == GREEN_SWITCH_IMG:
                  grid[j.y][j.x] = Door((v.y,v.x),j.id, 'green') 
                elif v.switchtype == BLUE_SWITCH_IMG:
                  grid[j.y][j.x] = Door((v.y,v.x),j.id, 'blue') 
            else: pass
          except AttributeError:
            pass

    #portalcheck
    if turn > lastTurn:
      done = False
      for i,v in enumerate(Portal.instances):
        if done:
          break
        for g,j in enumerate(mapstuff):
          if done:
            break
          if j.__class__ == Portal and j != v:
            if j.id == v.id and player.x==v.x and player.y==v.y:
              player.x = j.x
              player.y = j.y
              done = True

    for i,v in enumerate(SunkenBox.instances):
      v.place()
    for i,v in enumerate(SunkenMetalBox.instances):
      v.place()
    for i,v in enumerate(Box.instances):
      v.place()
    for i,v in enumerate(Raft.instances):
      v.place()


    #move objects
    if turn > lastTurn:
      lastTurn = turn
      for i,v in enumerate(SawBlade.instances):
        v.move()
        if v.x == player.x and v.y == player.y:
          player.dead = True
      for i,v in enumerate(Raft.instances):
        if v.x == player.x and v.y == player.y:
          v.move()
          player.x = v.x
          player.y = v.y
        else:
          v.move()
      for i,v in enumerate(Enemy.instances):
        v.move()

    #player - Must be last
    grid[player.y][player.x] = 1

    if player.x == goal.x and player.y == goal.y:
      level += 1
      Box.instances = []
      SunkenBox.instances = []
      Switch.instances = []
      SawBlade.instances = []
      Raft.instances = []
      Emitter.instances = []
      Portal.instances = []
      Enemy.instances = []
      break

    #ani Frame saw
    sawframe += .2 #speed of animation
    if sawframe>8:
      sawframe = 0
    SAW_IMG = ImageTk.PhotoImage(Image.open(fp=f'images/saw-gif/{sawblade_frames[math.floor(sawframe)]}.png').resize((sf+1, sf+1), Image.NEAREST))

    #draw level
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            #main catch
            if grid[y][x].__class__ in imgs.keys():
              screen.create_image(x * sf, y * sf, image=imgs[grid[y][x].__class__], anchor='nw')
            #special tiles
            elif grid[y][x].__class__ == Floor:
                screen.create_rectangle(x * sf, y * sf, (x * sf) + sf, (y * sf) + sf, fill='#494646',width=0)
            elif grid[y][x] == 1:
                if player.direction in ['Up','w']:
                  screen.create_image(x * sf, y * sf, image=PLAYER_IMG_UP, anchor='nw')
                elif player.direction in ['Down','s']:
                  screen.create_image(x * sf, y * sf, image=PLAYER_IMG_DOWN, anchor='nw')
                elif player.direction in ['Right','d']:
                  screen.create_image(x * sf, y * sf, image=PLAYER_IMG_RIGHT, anchor='nw')
                elif player.direction in ['Left','a']:
                  screen.create_image(x * sf, y * sf, image=PLAYER_IMG_LEFT, anchor='nw')
                elif player.direction == None:
                  screen.create_image(x * sf, y * sf, image=PLAYER_IMG_IDLE, anchor='nw')
            elif grid[y][x].__class__ == Switch:
                screen.create_image(x * sf, y * sf, image=grid[y][x].switchtype, anchor='nw')
            elif grid[y][x].__class__ == Door:
                screen.create_image(x * sf, y * sf, image=grid[y][x].doortype, anchor='nw')
            elif grid[y][x].__class__ == OpenDoor:
                screen.create_rectangle(x * sf, y * sf, (x * sf) + sf, (y * sf) + sf, fill='#494646',width=0)
            elif grid[y][x].__class__ == SawBlade:
                screen.create_image(x * sf, y * sf, image=SAW_IMG, anchor='nw')
            elif grid[y][x].__class__ == Emitter:
                if grid[y][x].direction == 'UP':
                  screen.create_image(x * sf, y * sf, image=EMITTER_IMG_UP, anchor='nw')
                elif grid[y][x].direction == 'DOWN':
                  screen.create_image(x * sf, y * sf, image=EMITTER_IMG_DOWN, anchor='nw')
                elif grid[y][x].direction == 'RIGHT':
                  screen.create_image(x * sf, y * sf, image=EMITTER_IMG_RIGHT, anchor='nw')
                elif grid[y][x].direction == 'LEFT':
                  screen.create_image(x * sf, y * sf, image=EMITTER_IMG_LEFT, anchor='nw')
            elif grid[y][x].__class__ == Portal:
                if grid[y][x].color == 'orange': 
                  screen.create_image(x * sf, y * sf, image=ORANGE_PORTAL_IMG, anchor='nw')

    for i,v in enumerate(Emitter.instances):
      v.place()

    if player.dead:
      Box.instances = []
      SawBlade.instances = []
      SunkenBox.instances = []
      SunkenMetalBox.instances = []
      Switch.instances = []
      Raft.instances = []
      Emitter.instances = []
      Portal.instances = []
      Enemy.instances = []
      break
    
    if (level == 7) and ((player.x, player.y) == (3,4)):
      screen.create_image(3 * sf, 4 * sf, image=SUPRISED_PLAYER_IMG, anchor='nw')
      playfn('music/easter-egg.mp3')
      dumbass = tk.Label(window,text='"idiot"   -@gabegolem',fg='#FFFFFF',bg='#000000',font=40)
      dumbass.pack()
      while True:
        window.update()
        

    window.update()
    time.sleep(.0001)
    window.update()
    screen.delete('all')
    grid = deepcopy(master)