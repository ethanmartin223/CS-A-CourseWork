def isPrime(num, c=0, i=1):
    if num > i:
      if num % i == 0:
        c = c+1
        if c > 1:
          return False
      return isPrime(num, i=i+1, c=c)
    else:
      return True if c == 1 else False

def factorial(n):
  return n * factorial(n-1) if n > 0 else 1

def permutations(n, r):
  return int(factorial(n) / factorial(n - r))

def leastCommon(iterable_):
  dct = {}
  presences_list = []
  for i in iterable_:
    presence = iterable_.count(i)
    presences_list.append(presence)
    if i not in dct:
      dct[presence] = i
    else:
      dct.update({presence : i})
  mode_amount = min(presences_list)
  mode = dct[min(dct)]
  return mode,mode_amount

def mostCommon(iterable_):
  dct = {}
  presences_list = []
  for i in iterable_:
    presence = iterable_.count(i)
    presences_list.append(presence)
    if i not in dct:
      dct[presence] = i
    else:
      dct.update({presence : i})
  mode_amount = max(presences_list)
  mode = dct[max(dct)]
  return mode,mode_amount

def mean(numberset):
  while type(numberset[0]) == tuple:
    numberset = numberset[0]
  total = 0
  for i,v in enumerate(numberset):
    total += v
  return total / len(numberset)

def median(numberset):
  numset = sorted(list(numberset))
  if len(numset)%2 != 0:
    return numset[int(len(numset)/2)]
  else:
    return numset[int((len(numset)-1)/2)], numset[int((len(numset)-1)/2)+1]

def mode(numberset):
  num = dict()
  no_mode = True
  for i,v in enumerate(numberset):
    if v in num.keys():
      no_mode = False
    num.setdefault(v, 0)
    num[v] += 1
  if no_mode:
    return None
  greatest = (0,0)
  for i,v in enumerate(num.items()):
    v = list(v)
    if v[1] == greatest[1]:
      greatest[0] = [greatest[0]]+v
    elif v[1] > greatest[1]:
      greatest = v
  if type(greatest[0]) == int:
    return greatest[0] 
  alr =  []
  for i,v in enumerate(greatest[0]):
    if v not in alr:
      alr.append(v)
  return alr

def sdeviation(numberset):
  while type(numberset[0]) == tuple:
    numberset = numberset[0]
  m = mean(numberset)
  out = 0
  for i,v in enumerate(numberset):
    out += abs(m-v)**2
  out /= len(numberset)
  return (out)**(1/2)

def variance(numberset):
  while type(numberset[0]) == tuple:
    numberset = numberset[0]
  return sdeviation(numberset)**2

def percentile(numberset,percent):
  n = 0
  for i,v in enumerate(numberset):
    if v < percent:
      n += 1
  return (n / len(numberset))*100

def toASCII(fp=None, image_object=None, transparent_background=False, output_dim=None, scalefactor=0, null_char=' ', char_height_correction=True, rgb_color=False, background=None):
  from PIL import Image, ImageOps
  import math, random
  
  with Image.open(fp=fp) if fp != None else image_object as input_image:
    if output_dim is not None:
      input_image = input_image.resize(output_dim)
    if scalefactor != 0:
      input_image = input_image.resize((math.floor(input_image.width*scalefactor), math.floor(input_image.height*scalefactor)))
    if char_height_correction:
      input_image = input_image.resize((input_image.width,round(input_image.height/2)))
    
    filtered_image = ImageOps.grayscale(input_image)
    input_image = input_image.convert('RGB')
    output_text = [[' ' for x in range(input_image.width)] for y in range(input_image.height)]
    comp_data = [[(filtered_image.getpixel((x_,y_))) for x_ in range(filtered_image.width)] for y_ in range(filtered_image.height)]
    
    char_set = '''$@B%8&WM#*oahkbdpqwmZ0OQLCJXcvxrjft/\|(){}[]?-_+~<>i!lI;:,"^`'. '''
    luminace_map = {}
    index = 0
    for i in range(1,257,256//len(char_set)):
      luminace_map.update({tuple([r for r in range(i, i+(256//len(char_set)))]) : char_set[index]})
      index += 1
    
    for y in range(filtered_image.height):
      for x in range(filtered_image.width):
        for i,v in enumerate(luminace_map.keys()):
          if comp_data[y][x] == 0 and transparent_background:
            if background is not None:
              output_text[y][x] = f'\033[48;2;{background[0]};{background[1]};{background[2]}m{null_char}\033[0m' if rgb_color else luminace_map[v]
            else:
              output_text[y][x] = null_char
            break
          if comp_data[y][x] in v:
            r,g,b = input_image.getpixel((x,y))
            if background is not None:
              output_text[y][x] = f'\033[48;2;{background[0]};{background[1]};{background[2]}m\033[38;2;{r};{g};{b}m{luminace_map[v]}\033[0m' if rgb_color else luminace_map[v]
            else:
              output_text[y][x] = f'\033[38;2;{r};{g};{b}m{luminace_map[v]}\033[0m' if rgb_color else luminace_map[v]
            break

    output = ''
    for y in range(filtered_image.height):
      for i,v in enumerate(output_text[y]):
        output += ''.join(str(v))
      output += '\n'
      
  return output

def luminace(rgb: tuple):
  r,g,b = rgb
  return (0.2126*r + 0.7152*g + 0.0722*b)**(1/2)

def rgb_to_hex(red, green, blue):
  red = hex(int(red))
  green = hex(int(green))
  blue = hex(int(blue))
  hex_code = '#' + red + green + blue
  hex_code = hex_code.replace('0x', '')
  return hex_code

def hex_to_rgb(value):
  value = value.replace('#', '')
  length = len(value)
  rgb_code = tuple(int(value[i:i + length // 3], 16) for i in range(0, length, length // 3))
  return rgb_code

def array(width,height):
  return [[0 for x_ in range(width)] for y_ in range(height)]

def playsound(filename, nodisplay=True, autoexit=True, stdout=False):
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

def spritesheet(imagename: str, tile_dim: tuple, spacer=0, sf=1):
  from PIL import Image
  spritesheet_image = Image.open(imagename)
  width = spritesheet_image.width
  height = spritesheet_image.height
  tile_height = tile_dim[1]
  tile_width = tile_dim[0]
  sprites = []
  for y in range(height // tile_height):
      for x in range(width // tile_width):
          cords = (
              x * tile_width + x, y * tile_height + y, x * tile_width + x + tile_width,
              y * tile_height + y + tile_height)
          sprites.append(spritesheet_image.crop(cords).resize((sf, sf), Image.NEAREST))
  return sprites

def padArray(array: list, padxy: (tuple or list)):
  padx, pady = padxy
  output = [[1 for x_ in range(len(array) + padx * 2)] for y_ in range(len(array[0]) + pady * 2)]
  for y in range(len(array)):
      for x in range(len(array[0])):
          output[y + pady][x + padx] = array[y][x]
  return output

def rotate_right(array): 
  from copy import deepcopy
  output = deepcopy(array)
  array.reverse()
  for y in range(len(array)):
      for x in range(len(array[y])):
          output[y][x] = array[x][y]
  return output

def rotate_left(array): 
  from copy import deepcopy
  output = deepcopy(array)
  for i, v in enumerate(array):
      v.reverse()
  for y in range(len(array)):
      for x in range(len(array[y])):
          output[y][x] = array[x][y]
  return output

def isGeometricSeq(seq):
  flg = True
  common = seq[1] / seq[0]
  for i,v in enumerate(seq):
    if i != 0:
      if v / seq[i-1] != common:
        flg = False
  return (flg,common if flg==True else None)

def isArithmicSeq(seq):
  flg = True
  common = seq[1] - seq[0]
  for i,v in enumerate(seq):
    if i != 0:
      if v - seq[i-1] != common:
        flg = False
  return (flg,common if flg==True else None)

def generalTermOf(seq):
  if isGeometricSeq(seq)[0]:
    r = seq[1] / seq[0]
    return f'{seq[0]}*({r})**(n-1)'
  elif isArithmicSeq(seq)[0]:
    r = seq[1] - seq[0]
    return f'{seq[0]-r}+({r})*n'
  else:
    return None

def summination(ceil,formula,n=1):
  '''
   ceil\n
     ∑(formula)\n
   n=0
  '''
  total = []
  for n in range(n,ceil+1):
    total.append(eval(formula, locals()))
  return sum(total)

