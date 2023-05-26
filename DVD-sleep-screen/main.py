import random
import time
import tkinter as tk
from PIL import Image,ImageTk

window = tk.Tk()
window.geometry(f'{window.winfo_screenwidth()}x{window.winfo_screenheight()}')
window.overrideredirect(1)
window.wm_attributes('-topmost', 'true')
black_bg = tk.Frame(width=window.winfo_screenwidth(),height=window.winfo_screenheight(),bg='black').place(x=0,y=0)

width = 100
height = 50

dvd_blue = ImageTk.PhotoImage(Image.open("dvd_blue.png").resize((width,height),Image.ANTIALIAS))
dvd_brown = ImageTk.PhotoImage(Image.open("dvd_brown.png").resize((width,height),Image.ANTIALIAS))
dvd_green = ImageTk.PhotoImage(Image.open("dvd_green.png").resize((width,height),Image.ANTIALIAS))
dvd_grey = ImageTk.PhotoImage(Image.open("dvd_grey.png").resize((width,height),Image.ANTIALIAS))
dvd_light_blue = ImageTk.PhotoImage(Image.open("dvd_light_blue.png").resize((width,height),Image.ANTIALIAS))
dvd_light_green = ImageTk.PhotoImage(Image.open("dvd_light_green.png").resize((width,height),Image.ANTIALIAS))
dvd_orange = ImageTk.PhotoImage(Image.open("dvd_orange.png").resize((width,height),Image.ANTIALIAS))
dvd_pink = ImageTk.PhotoImage(Image.open("dvd_pink.png").resize((width,height),Image.ANTIALIAS))
dvd_purple = ImageTk.PhotoImage(Image.open("dvd_purple.png").resize((width,height),Image.ANTIALIAS))
dvd_red = ImageTk.PhotoImage(Image.open("dvd_red.png").resize((width,height),Image.ANTIALIAS))
dvd_white = ImageTk.PhotoImage(Image.open("dvd_white.png").resize((width,height),Image.ANTIALIAS))
dvd_yellow = ImageTk.PhotoImage(Image.open("dvd_yellow.png").resize((width,height),Image.ANTIALIAS))

current_x = 3
current_y = 3
location = (window.winfo_screenwidth()//2-(width/2),window.winfo_screenheight()//2-(height/2))
dr_corner = (location[0]+width,location[1]+height)
d_corner = (location[0],location[1]+height)
r_corner = (location[0]+width,location[1])

dvd_image = random.sample((dvd_blue,dvd_brown,dvd_green,dvd_grey,dvd_light_blue,dvd_light_green,dvd_orange,dvd_pink,dvd_purple,dvd_red,dvd_white,dvd_yellow),1)

text = tk.Label(width=width,height=height,bd=0,image=dvd_image)

while True:
  if (location[0] >= window.winfo_screenwidth()-width):
    current_x=random.randint(-5,0)
    current_y=random.randint(-5,5)
    dvd_image = random.sample((dvd_blue,dvd_brown,dvd_green,dvd_grey,dvd_light_blue,dvd_light_green,dvd_orange,dvd_pink,dvd_purple,dvd_red,dvd_white,dvd_yellow),1)
  elif location[0] <= 0:
    current_x=random.randint(0,5)
    current_y=random.randint(-5,5)
    dvd_image = random.sample((dvd_blue,dvd_brown,dvd_green,dvd_grey,dvd_light_blue,dvd_light_green,dvd_orange,dvd_pink,dvd_purple,dvd_red,dvd_white,dvd_yellow),1)
  elif location[1] >= window.winfo_screenheight()-height:
    current_x=random.randint(-5,5)
    current_y=random.randint(-5,0)
    dvd_image = random.sample((dvd_blue,dvd_brown,dvd_green,dvd_grey,dvd_light_blue,dvd_light_green,dvd_orange,dvd_pink,dvd_purple,dvd_red,dvd_white,dvd_yellow),1)
  elif location[1] <= 0:
    current_x=random.randint(-5,5)
    current_y=random.randint(0,5)
    dvd_image = random.sample((dvd_blue,dvd_brown,dvd_green,dvd_grey,dvd_light_blue,dvd_light_green,dvd_orange,dvd_pink,dvd_purple,dvd_red,dvd_white,dvd_yellow),1)
  if location == (0,0):
    break
  if r_corner == (window.winfo_screenwidth(),0):
    break
  if dr_corner == (window.winfo_screenwidth(),window.winfo_screenheight()):
    break
  if d_corner == (0,window.winfo_screenheight()):
    break
  text = tk.Label(width=width,height=height,image=dvd_image)
  text.place(x=location[0], y=location[1])
  window.update()
  speed = abs(current_x) + abs(current_y)
  time.sleep(.004*speed)
  location =(location[0]+current_x,location[1]+current_y)
  dr_corner = (location[0]+100,location[1]+50)
  text.destroy()
