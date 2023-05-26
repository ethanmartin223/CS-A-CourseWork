#----------------# Imports #----------------#
import random
from csvreader import CSVfile
import tkinter as tk
from functools import partial
import time
import requests
import link_extractor as le
import io
from PIL import Image, ImageTk

# You can change the time delay here; under TIMER_DURATION. If you want it disabled, set it to
# float("inf")

#----------------# Settings/constents #---------------#
TIMER_DURATION = 20  #sec
SHOW_ANSWER_DELAY = 3  #sec

#----------------# colors #----------------#
YELLOW_TEXT = '#f7cb93'
WHITE_TEXT = '#ffffff'
BLUE_BACKGROUND = '#051472'
MONEY_TEXT = ('Ariel', 30, 'bold')
QUESTION_TEXT = ('Ariel', 20, 'bold')
CATAGORY_TEXT = ('Ariel', 15, 'bold')

#----------------# vars #----------------#
timer_running = False

#----------------# load and clean CSVfile #----------------#
csv = CSVfile('jeopardy.csv'
              )  #custom csvreader just cleans data and has extra functionality


#----------------# category class #----------------#
class Category:
    instances = {}

    def __init__(self, cat_name, date) -> None:
        self.__class__.instances.update({cat_name: self})
        self.name = cat_name
        self.questions = {}
        self.date_taped = date


#----------------# load data and create instances #----------------#
data = csv.read()
for i, v in enumerate(data):
    if v[3] in Category.instances.keys():
        Category.instances[v[3]].questions.update({v[4]: {v[5]: (v[6])}})
    else:
        Category(v[3], v[1])
        Category.instances[v[3]].questions.update({v[4]: {v[5]: (v[6])}})
current_game_catagories = []
for i in range(5):
    while True:
        cat_choosen = Category.instances[random.choice(
            list(Category.instances.keys()))]
        if len(cat_choosen.questions) == 5:
            current_game_catagories.append(cat_choosen)
            break

#code above just returns current_game_catagories as a list of 5 catagory objects, each of which contain
# a dictionary of 5 questions and answers under self.questions

#----------------# window init #----------------#
window = tk.Tk()
window.wm_attributes('-fullscreen', True)  #set the window to fullscreen

buttons_menu = tk.LabelFrame(
    bd=0, highlightcolor=None,
    bg=BLUE_BACKGROUND)  #add a container for the buttons and headers
buttons_menu.pack(fill='both', expand=True)

question_container = tk.LabelFrame(
    bd=0, highlightcolor=None, bg=BLUE_BACKGROUND,
    fg=WHITE_TEXT)  #add a container for wigets used in the question screen
current_question = tk.Label(question_container,
                            text='',
                            font=QUESTION_TEXT,
                            wrap=window.winfo_screenwidth() - 100,
                            bd=0,
                            highlightcolor=None,
                            bg=BLUE_BACKGROUND,
                            fg=WHITE_TEXT)  #question label

#----------------# add all the headers for the coulmns #----------------#
for i, v in enumerate(current_game_catagories):
    tk.Label(buttons_menu,
             text=v.name,
             bg=BLUE_BACKGROUND,
             fg=WHITE_TEXT,
             wrap=166,
             width=10,
             height=4,
             font=CATAGORY_TEXT).grid(row=0, column=i)

#----------------# create question matrix #----------------#
questions = [[(*list(v.questions.items()), )[x][1] for x in range(5)]
             for i, v in enumerate(current_game_catagories)]


#----------------# create button callback #----------------#
def on_button_press(x, y) -> None:
    global submit_clicked, current_player, timer_running
    buttons_menu.pack_forget()  #hide button main screen

    #-------------# Show question screen #--------------#
    question_container.pack(fill='both', expand=True)  #show question container
    q, links = le.extract_html_links(list(questions[x][y])[0])
    '''if links:
      if len(links) == 1:
        for i,v in enumerate(links):
          try:
            imagedata = io.BytesIO(requests.get(v).content)
            image_from_link = ImageTk.PhotoImage(Image.open(imagedata))
            current_question.config(image=image_from_link)
          except:
            pass'''

    current_question.config(text=q)
    current_question.pack(side='top', fill='both',
                          expand=True)  #show the question

    #-------------# start timer #---------------#
    timer_start = time.time()
    timer_running = True  #start timer

    #-------------# SKIP Button #---------------#
    def skip_question(event):
        global timer_running
        if event.keysym == 'space':
            timer_running = False

    window.bind('<Key>', skip_question)

    while timer_running:
        if (time.time() - timer_start >= TIMER_DURATION):
            timer_running = False
        window.update()

    current_question.config(
        text=
        f'The Correct Answer is:\n\n{list(questions[x][y].items())[0][1].lower().title()}'
    )
    window.update()
    time.sleep(SHOW_ANSWER_DELAY)
    window.unbind('<Key>')

    #-------------# Re-show main screen and hide answer screen #-------------#
    buttons[y][x]["state"] = "disabled"  #disable button
    buttons[y][x].config(text='')  #set button text to clear
    question_container.pack_forget()  #hide question container
    buttons_menu.pack(fill='both', expand=True)  #re-show main screen
    current_question.config(image=None)


#----------------# create button matrix #----------------#
buttons = [[
    tk.Button(buttons_menu,
              text=f'${200*(y+1)}',
              width=5,
              height=2,
              command=partial(on_button_press, x, y),
              font=MONEY_TEXT,
              bg=BLUE_BACKGROUND,
              fg=YELLOW_TEXT,
              highlightbackground='#000000') for x in range(5)
] for y in range(5)]

#----------------# Add all buttons to LabelFrame #----------------#
for y in range(len(buttons)):
    for x in range(len(buttons[y])):
        buttons[y][x].grid(
            row=y + 1, column=x, sticky="nswe"
        )  #use grid manager to add button to row y and column x
buttons_menu.columnconfigure(tuple(range(5)), weight=2)
buttons_menu.rowconfigure(tuple(range(6)), weight=2)

#----------------# Run Mainloop #----------------#
window.mainloop()
