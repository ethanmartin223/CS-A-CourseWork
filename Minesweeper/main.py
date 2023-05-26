import random, sys, time, math
import tkinter as tk
from PIL import ImageTk, Image, ImageDraw
from functools import partial
import threading

sys.setrecursionlimit(2000) #changes recurse limit as the recurse(x,y) function could *theoretically* go over the base limit at higher dificulties

#starting varibles for board layout and options
gamemode = 1
grid = lambda x,y,char=0:[[char for i in range(x)]for i in range(y)]

if gamemode in ['easy',1]:
  (sf, width, height, mines) = (35, 10, 10, 10)
elif gamemode in ['medium',2]:
  (sf, width, height, mines) = (30, 16, 16, 40)
elif gamemode in ['hard',3]:
  (sf, width, height, mines) = (22, 22, 22, 99)
else:
  raise ValueError(f'{gamemode} is not a valid gamemode.')
minesleft = mines
turn = 0  
minelocations = []
for i in range(mines):
  temp = (random.randint(0,width-1),random.randint(0,height-1))
  while temp in minelocations:
    temp = (random.randint(0,width-1),random.randint(0,height-1))
  minelocations.append(temp)
board = grid(width,height)
buttons = grid(width,height,char=None)
displaygrid = grid(width,height,char=2)
for i,v in enumerate(minelocations): 
  if board[v[1]][v[0]] == 0:
    board[v[1]][v[0]] = 1
  else: 
    i-=1
    continue
boardwithnumbers = grid(width,height,char = None)
visited = []
removed = 0
clickedOnMine = False
cur_time = 0
hasWon = False
volume = True
best_time = '---'
endgame_screen = None

#colors
tilebg = '#a2d149'
tilebg1 = '#aad751'
minebg = 'red'
revealedbg = '#d7b899'
revealedbg1 = '#e5c29f'
fgclr = {0: None, 1:'#1976d2', 2:'#388e3c', 3: '#d32f2f', 4:'#8026a2', 5:'#ff8f00', 6:'#433f3e', 7:'#433f3e', 8:'#433f3e'}
scoreboardclr = '#4a752c'

#window init
window = tk.Tk()
window.wm_attributes('-fullscreen', True)

#mine Images
def makeMine(fg,bg):
  imager = Image.new('RGBA', (sf,sf), bg)
  image = ImageDraw.Draw(imager)
  image.ellipse([sf/4,sf/4,sf-sf/4,sf-sf/4], fill=fg)
  return ImageTk.PhotoImage(imager)
colors = [
  ('#008744','#00582c'),
  ('#ed44b5','#9a2c76'),
  ('#48e6f1','#2f969d'),
  ('#4885ed','#2f569a'),
  ('#f4c20d','#9f7e08'),
  ('#db3236','#8e2123'),
  ('#b648f2','#762f9d'),
  ('#f4840d','#9f5608'),
]
mine_images = [makeMine(v[1],v[0]) for i,v in enumerate(colors)]

#images
button_null = tk.PhotoImage(width=1, height=1)
flag_img = ImageTk.PhotoImage(Image.open(fp="images/flag_icon.png").resize((sf,sf),Image.ANTIALIAS))
flag_img_1 = ImageTk.PhotoImage(Image.open(fp="images/flag_icon.png").resize((44,44),Image.ANTIALIAS))
clock_img = ImageTk.PhotoImage(Image.open(fp="images/clock_icon.png").resize((44,44),Image.ANTIALIAS))
clock_img_1 = ImageTk.PhotoImage(Image.open(fp="images/clock_icon.png").resize((70,70),Image.ANTIALIAS))
trophy_img = ImageTk.PhotoImage(Image.open(fp="images/trophy_icon.png").resize((70,70)))
vol_on_img = ImageTk.PhotoImage(Image.open(fp="images/volume_on.png").resize((30,30),Image.ANTIALIAS))
vol_off_img = ImageTk.PhotoImage(Image.open(fp="images/volume_off.png").resize((30,30),Image.ANTIALIAS))
lose_screen_img = ImageTk.PhotoImage(Image.open(fp="images/lose_screen.png").resize((int((width*sf)/2),int((height*sf)/4))))
win_screen_img = ImageTk.PhotoImage(Image.open(fp="images/win_screen.png"))

def showEndGame(c,b):
  global endgame_screen
  endgame_screen = tk.LabelFrame(master=canvas,width=int((width*sf)/2),height=int((height*sf)/2),bd=0,highlightbackground=None,bg='#4ac0fd')
  end_frame = tk.Label(master=endgame_screen,image=lose_screen_img,bd=0)
  end_frame.pack(side='bottom')
  info_box = tk.LabelFrame(master=endgame_screen,bd=0)
  clock_container = tk.LabelFrame(bg='#4ac0fd',master=info_box,bd=0,pady=10,padx=10)
  best_clock_container = tk.LabelFrame(bg='#4ac0fd',master=info_box,bd=0,pady=10,padx=10)
  this_run_time = tk.Label(master=clock_container,image=clock_img_1,bg='#4ac0fd',bd=0)
  best_run_time = tk.Label(master=best_clock_container,image=trophy_img,bg='#4ac0fd',bd=0)
  if type(b) == float:
    b = int(b)
  if type(c) == float:
    c = int(c)   
  round_time = tk.Label(master=clock_container,text=c,bg='#4ac0fd',bd=0,padx=20,font=('ariel',18,'bold'),fg='white')
  best_time = tk.Label(master=best_clock_container,text=b,bg='#4ac0fd',bd=0,padx=20,font=('ariel',18,'bold'),fg='white')
  endgame_screen.place(x=int((width*sf)/2),y=int((height*sf)/3)+sf,anchor='center')
  info_box.pack()
  round_time.pack(side='bottom')
  clock_container.pack(side='left')
  this_run_time.pack(side='left')
  best_run_time.pack()
  best_clock_container.pack(side='right')
  best_time.pack()

#volume
def volume_onOff():
  global volume
  if volume:
    volume=False
    volume_button.configure(image=vol_off_img)
  elif not volume:
    volume=True
    volume_button.configure(image=vol_on_img)

#w- (m)idget managment
    
container = tk.LabelFrame(bg=scoreboardclr,bd=0,highlightthickness=0)
scoreboard = tk.LabelFrame(master=container,bg=scoreboardclr,bd=0,highlightthickness=0,highlightbackground='white')
mineAndTime = tk.LabelFrame(master=scoreboard,bg=scoreboardclr,bd=0,highlightthickness=0)
time_counter_bundle =tk.LabelFrame(master=mineAndTime,bg=scoreboardclr,bd=0,highlightthickness=0,highlightbackground='white') 
mines_left_bundle = tk.LabelFrame(master=mineAndTime,bg=scoreboardclr,bd=0,highlightthickness=0,highlightbackground='white')
flag_icon = tk.Label(master=mines_left_bundle,image=flag_img_1,bg=scoreboardclr)
clock_icon = tk.Label(master=time_counter_bundle,image=clock_img,bg=scoreboardclr)
mines_left_counter = tk.Label(master=mines_left_bundle,text=f'{minesleft}',bg=scoreboardclr,fg='#ffffff',font=('ariel',18,'bold'))
seconds_counter = tk.Label(master=time_counter_bundle,text=f'{cur_time}',bg=scoreboardclr,fg='#ffffff',font=('ariel',18,'bold'))
volume_button = tk.Button(master=scoreboard,image=vol_on_img,bd=0,highlightthickness=0,bg=scoreboardclr,fg=scoreboardclr,activebackground=scoreboardclr,relief='flat',command=volume_onOff)
canvas = tk.Canvas(master=container, bg='black',width=width*sf-2,height=height*sf-2)
container.pack(expand=True)
volume_button.pack(side='right',padx=(0,20))
canvas.pack(side='bottom')
scoreboard.pack(side='top',expand=True,fill='both')
mines_left_bundle.pack(side='left',padx=(0,20))
mines_left_counter.pack(side='right')
flag_icon.pack(side='left')
time_counter_bundle.pack(side='right')
seconds_counter.pack(side='right')
clock_icon.pack()
mineAndTime.pack(anchor='center')

def squaresLeft(master):
  squaresLeft = 0
  for y in range(len(master)):
    for x in range(len(master[y])):
      if master[y][x] in [2,5]:
        squaresLeft += 1
  return squaresLeft
        
#check around each tile for a mine; returns the number of mines to display on tile
def mines_around(x,y):
  m = 0
  d = [(0,1),(1,0),(1,1),(-1,0),(0,-1),(-1,-1),(-1,1),(1,-1)]
  for i,v in enumerate(d): 
    try: 
      if y+v[1] >-1 and x+v[0] > -1: 
        if board[y+v[1]][x+v[0]]: m+=1
    except IndexError:
      pass
  return m

#board init
for y in range(height):
  for x in range(width):
    if board[y][x] != 1:
      boardwithnumbers[y][x] = mines_around(x,y)
    else:
      boardwithnumbers[y][x] = 'X'

#end mainloop
def gameover():
  global clickedOnMine,cur_time,best_time
  window.unbind('<r>')
  clickedOnMine = True
  for i,v in enumerate(minelocations):
    buttons[v[1]][v[0]].configure(image=random.choice(mine_images),anchor='center')
    window.update()
    time.sleep(.3 if gamemode == 1 else .2 if gamemode == 2 else .1)
  #time.sleep(2)
  #showEndGame('---',best_time)
  window.bind('<r>',restart)
  
# for tiles that are clicked on that have sourounding non-bomb tiles, iterate through and reveal all that are not touching a bomb
def recurse(x,y):
  global grid, displaygrid, visited, boardwithnumbers, removed
  if boardwithnumbers[y][x] == 0:
    for i,v in enumerate([(0,1),(1,0),(1,1),(-1,0),(0,-1),(-1,-1),(-1,1),(1,-1)]):
      try:
        if mines_around(x+v[0],y+v[1]) == 0 and (x+v[0],y+v[1]) not in visited and y+v[1]>-1 and x+v[0]>-1 and boardwithnumbers[y+v[1]][x+v[0]] == 0:
            displaygrid[y+v[1]][x+v[0]]=n= board[y+v[1]][x+v[0]]
            if n == 0:
              clr = revealedbg if ((x+v[0])+(y+v[1])) % 2 == 0 else revealedbg1
            elif n == 1:
              clr = minebg
            a = mines_around(x+v[0],y+v[1])
            buttons[y+v[1]][x+v[0]].configure(bg=clr,anchor='center',text=a if a != 0 else '',fg=fgclr[a])
            buttons[y+v[1]][x+v[0]].update()
            visited.append((x+v[0],y+v[1]))
            if board[y+v[1]][x+v[0]] == 0 and x+v[0] <= width and y+v[1] <= height:
              recurse(x+v[0],y+v[1])          
        elif mines_around(x+v[0],y+v[1]) > 0 and (x+v[0],y+v[1]) not in visited and y+v[1]>-1 and x+v[0]>-1 and boardwithnumbers[y+v[1]][x+v[0]] != 'X':
            displaygrid[y+v[1]][x+v[0]]=n= board[y+v[1]][x+v[0]]
            if n == 0:
              clr = revealedbg if ((x+v[0])+(y+v[1])) % 2 == 0 else revealedbg1
            elif n == 1:
              clr = minebg
            a = mines_around(x+v[0],y+v[1])
            buttons[y+v[1]][x+v[0]].configure(bg=clr,anchor='center',text=a if a != 0 else '',fg=fgclr[a])
            buttons[y+v[1]][x+v[0]].update()
            visited.append((x+v[0],y+v[1]))
      except IndexError:
        pass

#reveal clicked tile
def reveal(x,y):
  global board, displaygrid, visited, boardwithnumbers, turn, minelocations, removed
  if turn == 0:
    turn += 1
    while boardwithnumbers[y][x] != 0:
      restart(None) #One hell of a bottleneck
  if displaygrid[y][x] not in [5]:
    displaygrid[y][x]= board[y][x] 
    if displaygrid[y][x] == 0:
      recurse(x,y)
    a = mines_around(x,y)
    if board[y][x] == 0:
      buttons[y][x].configure(bg=revealedbg if (x+y) % 2 == 0 else revealedbg1,anchor='center',text=a if a != 0 else '',fg=fgclr[a])
    elif board[y][x] == 1:
      buttons[y][x].configure(image=random.choice(mine_images),anchor='center',fg=fgclr[a])
    if displaygrid[y][x] == 1:
      gameover()
  turn+= 1

#add a flag to selected tile on rclick
def flag(x,y,event):
  global displaygrid,board,minesleft
  if displaygrid[y][x] not in [0,1,5] and minesleft >= 1:
    displaygrid[y][x] = 5
    buttons[y][x].configure(anchor='center',image=flag_img)
    buttons[y][x].update()
    minesleft -= 1
    mines_left_counter.configure(text=f'{minesleft}')
  elif displaygrid[y][x] == 5:
    displaygrid[y][x] = 2
    buttons[y][x].configure(anchor='center',image=button_null)
    buttons[y][x].update()
    minesleft+= 1
    mines_left_counter.configure(text=f'{minesleft}')

#development stuff
def reveal_all(event):
  global width,height, board, displaygrid, visited, boardwithnumbers, turn, minelocations
  for y in range(height):
    for x in range(width):
      if displaygrid[y][x] != 5:
        displaygrid[y][x]= board[y][x] 
        a = mines_around(x,y)
        if board[y][x] == 0:
          buttons[y][x].configure(bg=revealedbg if (x+y) % 2 == 0 else revealedbg1,anchor='center',text=a if a != 0 else '',fg=fgclr[a])
        elif board[y][x] == 1:
          buttons[y][x].configure(image=random.choice(mine_images),anchor='center',fg=fgclr[a])
window.bind('<space>',reveal_all)

def restart(event):
  global minelocations, board, buttons, displaygrid, boardwithnumbers, visited, minesleft, removed,cur_time,clickedOnMine,runtimer, turn,endgame_screen
  try:endgame_screen.place_forget()
  except AttributeError: pass
  cur_time=0
  turn=0
  runtimer=True
  minelocations = []
  removed = 0
  clickedOnMine = False
  for i in range(mines):
    temp = (random.randint(0,width-1),random.randint(0,height-1))
    while temp in minelocations:
      temp = (random.randint(0,width-1),random.randint(0,height-1))
    minelocations.append(temp)
  board = grid(width,height)
  displaygrid = grid(width,height,char=2)
  for i,v in enumerate(minelocations): 
    if board[v[1]][v[0]] == 0:
      board[v[1]][v[0]] = 1
    else:
      i-=1
      continue
  boardwithnumbers = grid(width,height,char = None)
  visited = []
  for y in range(height):
    for x in range(width):
      buttons[y][x].configure(bg=tilebg if (x+y) % 2 == 0 else tilebg1,command=partial(reveal,x,y),bd=0,borderwidth=0,highlightthickness=0,highlightbackground='black',image=button_null,compound='right',width=sf-2,height=sf-2,padx=1,pady=1,text='',font=('ariel', int(sf/2), 'bold'))
      p = partial(flag,x,y)
    buttons[y][x].bind('<Button-3>',p)
  for y in range(height):
    for x in range(width):
      if board[y][x] != 1:
        boardwithnumbers[y][x] = mines_around(x,y)
      else:
        boardwithnumbers[y][x] = 'X'
  minesleft=mines
  mines_left_counter.configure(text=f'{minesleft}')
window.bind('<r>',restart)
  
#create each tile (clickable)
for y in range(height):
  for x in range(width):
    p = partial(reveal,x,y)
    buttons[y][x] = tk.Button(canvas,bg=tilebg if (x+y) % 2 == 0 else tilebg1,command=p,bd=0,borderwidth=0,highlightthickness=0,highlightbackground='black',image=button_null,compound='right',width=sf-2,height=sf-2,padx=1,pady=1,font=('ariel', int(sf/2), 'bold'))
    buttons[y][x].place(x=x*sf,y=y*sf)
    p = partial(flag,x,y)
    buttons[y][x].bind('<Button-3>',p)

def checkForWin():
  global displaygrid, mines,cur_time,clickedOnMine,hasWon,runtimer,best_time
  runtimer = True
  while True:
    if clickedOnMine:
      runtimer = False
    if squaresLeft(displaygrid) == mines and not clickedOnMine:
      hasWon = True
      runtimer = False
      showEndGame(cur_time,best_time)
      clickedOnMine = True
    time.sleep(.01)
    cur_time += .01 if cur_time <= 999 and runtimer else 0
    seconds_counter.config(text=f'{str(math.floor(cur_time)) if len(str(math.floor(cur_time))) == 3 else "0"+str(math.floor(cur_time)) if len(str(math.floor(cur_time))) == 2 else "00"+str(math.floor(cur_time))}')
threading.Thread(target=checkForWin).start()

#run gui
window.mainloop()