#profiling
# python3 -m cProfile -s cumulative main.pyw

#------------------# imports #-------------------#
import tkinter as tk
import random
import math
from copy import deepcopy

# ------------------# VARIABLES #------------------#
shapes = [
    ([[0, 0, 1, 0],
      [0, 0, 1, 0],
      [0, 1, 1, 0],
      [0, 0, 0, 0]], '#0200ee'),

    ([[0, 0, 0, 0],
      [0, 1, 1, 0],
      [0, 1, 1, 0],
      [0, 0, 0, 0]], '#e9e720'),

    ([[0, 1, 0, 0],
      [0, 1, 0, 0],
      [0, 1, 1, 0],
      [0, 0, 0, 0]], '#eda001'),

    ([[0, 0, 0, 0],
      [0, 1, 1, 0],
      [1, 1, 0, 0],
      [0, 0, 0, 0]], '#30e630'),

    ([[0, 0, 0, 0],
      [1, 1, 0, 0],
      [0, 1, 1, 0],
      [0, 0, 0, 0]], '#ed0200'),

    ([[0, 0, 0, 0],
      [1, 1, 1, 0],
      [0, 1, 0, 0],
      [0, 0, 0, 0]], '#9101d6'),

    ([[0, 0, 1, 0],
      [0, 0, 1, 0],
      [0, 0, 1, 0],
      [0, 0, 1, 0]], '#01f0f1'),

    ([[0, 0, 0, 0],
      [0, 1, 1, 0],
      [1, 1, 0, 0],
      [0, 1, 0, 0]], '#ba5abf'),

    ([[0, 0, 0, 0],
      [1, 1, 0, 0],
      [0, 1, 1, 0],
      [0, 1, 0, 0]], '#422500'),

    ([[0, 0, 0, 0],
      [1, 1, 1, 0],
      [0, 1, 0, 0],
      [0, 1, 0, 0]], '#2dad8f'),

    ([[0, 0, 0, 0],
      [1, 1, 1, 0],
      [1, 0, 1, 0],
      [0, 0, 0, 0]], '#191a19'),

    ([[0, 1, 0],
      [1, 1, 1],
      [0, 1, 0]], '#fcffff'),

    ([[0, 0, 0, 0],
      [1, 0, 0, 0],
      [1, 1, 0, 0],
      [0, 1, 1, 0]], '#002c73'),

    ([[1, 0, 0],
      [1, 0, 0],
      [1, 1, 1]], '#023d03'),
]
sf = 18
width = 10
height = 20
extra_shapes = False
tile_background = '#444444'
background_color = '#888888'
current_shape = None  # the current shape that is controlled by the user inputs
global_delay = 800  # time delay for piece falling (ms)
next_shape = random.randint(0, 6) if not extra_shapes else random.randint(0, len(shapes) - 1)
score = 0
multiplier = 1
level = 1
outline_width = 1

# ------------------# WINDOW #------------------#
window = tk.Tk()
window.title('Tetris')
right_sidebar = tk.Canvas(bg=background_color, width=(width * sf) / 4)
right_sidebar.pack(side='left', fill='both', expand=True)
canvas = tk.Canvas(width=sf * width, height=sf * height)
canvas.pack(fill='both', expand=True, side='left')
left_sidebar = tk.Canvas(bg=background_color, width=width * sf * 1.05)
left_sidebar.pack(side='left', fill='both', expand=True)
score_counter = left_sidebar.create_text(int((width * sf) / 3) + int(sf * 2 - int(sf / 3)),
                                         int((height * sf) / 3) - int(sf / 2) - (sf * 2), text='',
                                         font=('Areil', int(sf / 2), 'bold'), anchor='center')


# ------------------# STATIC FUNCTIONS #------------------#
def spawn_new():
    global current_shape
    Piece.instances.append(Piece())  # create the new piece to move
    current_shape = Piece.instances[-1]


def clear_canvas():
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            canvas.itemconfig(grid[y][x], fill=tile_background, outline=tile_background, dash=())


def restart(event):
    global current_shape, next_shape, global_delay, score, multiplier, level, collision_grid
    current_shape = None  # the current shape that is controlled by the user inputs
    global_delay = 300  # time delay for piece falling (ms)
    next_shape = random.randint(0, 6)
    score = 0
    multiplier = 1
    level = 1
    window.unbind('<Key>')
    clear_canvas()
    Piece.instances = []
    collision_grid = make_grid(width, height)
    spawn_new()


window.bind('<r>', restart)

# ------------------# LEVEL FUNCTIONS #------------------#
def make_grid(x, y, char=0):  # create a list of lists (array) of dimensions x (width) by y (height)
    return [[char for i in range(x)] for i in range(y)]


def rotate_left(array):  # rotate a array 90 degrees to the left
    output = deepcopy(array)
    for i, v in enumerate(array):
        v.reverse()
    for y in range(len(array)):
        for x in range(len(array[y])):
            output[y][x] = array[x][y]
    return output


def rotate_right(array):  # rotate a array 90 degrees to the right
    output = deepcopy(array)
    array.reverse()
    for y in range(len(array)):
        for x in range(len(array[y])):
            output[y][x] = array[x][y]
    return output


# ------------------# LEVEL INIT #------------------#
# create collision and display grids
grid = make_grid(width, height)
collision_grid = make_grid(width, height)
next_piece_display = make_grid(4, 4)
for y in range(len(grid)):
    for x in range(len(grid[0])):
        # create the tiles for the gui in range width by height
        grid[y][x] = canvas.create_rectangle(x * sf + outline_width, y * sf + outline_width, x * sf + sf, y * sf + sf,
                                             fill=tile_background,
                                             width=outline_width)

left_sidebar.create_rectangle(int((width * sf) / 3) - int(sf / 2), int((height * sf) / 3) - int(sf / 2),
                              int((width * sf) / 3) + 4 * sf + int(sf / 2),
                              int((height * sf) / 3) + 4 * sf + int(sf / 2), fill='#666666', outline='#666666',
                              width=outline_width)

score_bar_id = left_sidebar.create_rectangle(int((width * sf) / 3) - int(sf/2), int((height * sf) / 3) - int(sf)*3.5,
                              int((height * sf) / 3)+ int(sf),
                              int((height * sf) / 3)- int(sf)*1.5, fill='#666666', outline='#666666',
                              width=outline_width)
left_sidebar.tag_lower(score_bar_id)

for y in range(4):
    for x in range(4):
        next_piece_display[y][x] = left_sidebar.create_rectangle(x * sf + int((width * sf) / 3) + outline_width,
                                                                 y * sf + int((height * sf) / 3) + outline_width,
                                                                 x * sf + int((width * sf) / 3) + sf,
                                                                 y * sf + int((height * sf) / 3) + sf,
                                                                 outline=tile_background, width=0)


# ------------------# CLASSES #------------------#
class Piece:
    instances = []  # all instances of this class

    def __init__(self):
        global current_shape, next_shape
        self.shape = deepcopy(shapes[next_shape][0])
        self.color = shapes[next_shape][1]
        next_shape = random.randint(0, 6) if not extra_shapes else random.randint(0, len(shapes) - 1)
        self.width = len(self.shape[0])
        self.height = len(self.shape)
        self.x = math.ceil(width / 2) - int(self.width / 2)
        self.y = 0
        current_shape = self
        window.bind('<Key>', self.move)
        window.after(global_delay, self.do_gravity)

    # Check valid moves and handle key presses
    def move(self, event):
        global collision_grid

        # add all peices are on the collision_grid
        collision_grid = make_grid(width, height)
        for i, v in enumerate(Piece.instances):
            v.do_collison()

        can_move = True
        if current_shape == self:
            # rotate left on e key
            if event.keysym == 'e':
                array = deepcopy(self.shape)
                output = deepcopy(array)
                for i, v in enumerate(array):
                    v.reverse()
                for y in range(len(array)):
                    for x in range(len(array[y])):
                        output[y][x] = array[x][y]
                for y, v in enumerate(output):
                    for x, k in enumerate(v):
                        if k == 1:
                            try:
                                if (isinstance(collision_grid[self.y + y][self.x + x], Piece) and
                                    collision_grid[self.y + y][
                                        self.x + x] != self) or self.x + x > width or self.x + x < 0:
                                    can_move = False
                            except:
                                can_move = False
                if can_move:
                    self.shape = output

            # rotate right on q key
            elif event.keysym == 'q':
                array = deepcopy(self.shape)
                output = deepcopy(array)
                array.reverse()
                for y in range(len(array)):
                    for x in range(len(array[y])):
                        output[y][x] = array[x][y]
                for y, v in enumerate(output):
                    for x, k in enumerate(v):
                        if k == 1:
                            try:
                                if (isinstance(collision_grid[self.y + y][self.x + x], Piece) and
                                    collision_grid[self.y + y][
                                        self.x + x] != self) or self.x + x < 0 or self.x + x > width:
                                    can_move = False
                            except IndexError:
                                can_move = False
                if can_move:
                    self.shape = output

            # move left on a key
            elif event.keysym == 'a':
                for y, v in enumerate(self.shape):
                    for x, k in enumerate(v):
                        if k == 1:
                            if (isinstance(collision_grid[self.y + y][self.x + x - 1], Piece) and
                                collision_grid[self.y + y][self.x + x - 1] != self) or self.x + x - 1 < 0:
                                can_move = False
                if can_move:
                    self.x -= 1

            # move right on d key
            elif event.keysym == 'd':
                for y, v in enumerate(self.shape):
                    for x, k in enumerate(v):
                        if k == 1:
                            try:
                                if (isinstance(collision_grid[self.y + y][self.x + x + 1], Piece) and
                                    collision_grid[self.y + y][self.x + x + 1] != self) or self.x + x + 1 >= width:
                                    can_move = False
                            except IndexError:
                                can_move = False
                if can_move:
                    self.x += 1

            # send peices to bottom on space
            elif event.keysym in ['space']:
                while can_move:
                    for y, v in enumerate(self.shape):
                        for x, k in enumerate(v):
                            if k == 1:
                                try:
                                    if (isinstance(collision_grid[self.y + y + 1][self.x + x], Piece) and
                                        collision_grid[self.y + y + 1][self.x + x] != self) or self.y + y + 1 >= height:
                                        can_move = False
                                except IndexError:
                                    can_move = False

                    if can_move:
                        self.y += 1

            # move piece down on s key
            elif event.keysym in ['s']:
                for y, v in enumerate(self.shape):
                    for x, k in enumerate(v):
                        if k == 1:
                            try:
                                if (isinstance(collision_grid[self.y + y + 1][self.x + x], Piece) and
                                    collision_grid[self.y + y + 1][self.x + x] != self) or self.y + y + 1 >= height:
                                    can_move = False
                            except IndexError:
                                can_move = False

                if can_move:
                    self.y += 1

    # draw self to gui
    def place(self):
        self.draw_shadow()
        for y, v in enumerate(self.shape):
            for x, k in enumerate(v):
                if k == 1:
                    try:
                        canvas.itemconfig(grid[self.y + y][self.x + x], fill=self.color, outline='black', dash=())
                    except:
                        pass

    # add self to the global collision grid
    def do_collison(self):
        global collision_grid
        for y, v in enumerate(self.shape):
            for x, k in enumerate(v):
                if k == 1:
                    try:
                        collision_grid[self.y + y][self.x + x] = self
                    except IndexError:
                        pass

    # make pieces fall if there is no piece beneath them
    def do_gravity(self):
        global current_shape, collision_grid, score

        collision_grid = make_grid(width, height)
        for i, v in enumerate(Piece.instances):
            v.do_collison()
        can_move = True
        for y, v in enumerate(self.shape):
            for x, k in enumerate(v):
                if k == 1:
                    try:
                        if (isinstance(collision_grid[self.y + y + 1][self.x + x], Piece) and
                            collision_grid[self.y + y + 1][self.x + x] != self) or self.y + y + 1 >= height:
                            can_move = False
                    except IndexError:
                        can_move = False

        if can_move:
            self.y += 1
        elif not can_move and current_shape == self:
            score += 20
            window.unbind('<Key>')
            spawn_new()
            return
        if current_shape == self:
            window.after(global_delay, self.do_gravity)

    def draw_shadow(self):
        if self == current_shape:
            can_move = True
            shadow_x = self.x
            shadow_y = self.y
            while can_move:
                for y, v in enumerate(self.shape):
                    for x, k in enumerate(v):
                        if k == 1:
                            try:
                                if (isinstance(collision_grid[shadow_y + y + 1][shadow_x + x], Piece) and
                                    collision_grid[shadow_y + y + 1][
                                        shadow_x + x] != self) or shadow_y + y + 1 >= height:
                                    can_move = False
                            except IndexError:
                                can_move = False

                if can_move:
                    shadow_y += 1
            for y, v in enumerate(self.shape):
                for x, k in enumerate(v):
                    if k == 1:
                        try:
                            canvas.itemconfig(grid[shadow_y + y][shadow_x + x], fill=tile_background,
                                              outline=self.color, dash=())
                        except:
                            pass


# ------------------# BOARD TICK #------------------#
def place_all():
    global collision_grid, grid, global_delay, score
    clear_canvas()
    # draw all pieces to the board
    for i, v in enumerate(Piece.instances):
        v.place()
    for i, v in enumerate(collision_grid):
        flg = True
        for j, c in enumerate(v):
            if not isinstance(c, Piece) or c == current_shape:
                flg = False
        if flg:
            score += 150 * multiplier
            for b, n in enumerate(v):
                try:
                    n.shape.pop(i - n.y)
                except IndexError:
                    pass
            for i in range(2):
                for i, v in enumerate(Piece.instances):
                    v.do_gravity()
    window.after(1, place_all)


def update_gui():
    # score bar
    left_sidebar.itemconfig(score_counter, text=f'Score: {score}')

    # draw next shape
    for y in range(4):
        for x in range(4):
            left_sidebar.itemconfig(next_piece_display[y][x], fill=tile_background, outline=tile_background,
                                    width=outline_width)
    for y in range(4):
        for x in range(4):
            try:
                if shapes[next_shape][0][y][x] == 1:
                    left_sidebar.itemconfig(next_piece_display[y][x], fill=shapes[next_shape][1], width=outline_width,
                                            outline='black')
            except IndexError:
                pass
    window.after(1, update_gui)


# start the recursive place all and spawn the first piece
spawn_new()
place_all()
update_gui()

# ------------------# MAINLOOP #------------------#
window.mainloop()
