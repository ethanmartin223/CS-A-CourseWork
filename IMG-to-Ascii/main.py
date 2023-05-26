def luminace(rgb: tuple):
  r,g,b = rgb
  return (0.2126*r + 0.7152*g + 0.0722*b)**(1/2)


def toASCII(fp=None, image_object=None, transparent_background=False, char_shading=True, output_dim=None, scalefactor=0, null_char=' ', char_height_correction=True, rgb_color=False, background=None):
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
              output_text[y][x] = f'\033[38;2;{r};{g};{b}m{luminace_map[v] if char_shading else "█"}\033[0m' if rgb_color else luminace_map[v]
            break

    output = ''
    for y in range(filtered_image.height):
      for i,v in enumerate(output_text[y]):
        output += ''.join(str(v))
      output += '\n'
      
  return output

import time
data = toASCII('gabe.png', scalefactor=.6, rgb_color=True, char_shading=True)
for i,v in enumerate(data):
  print(v, end='', flush=True)
with open('output_file.txt', 'w') as output:
  output.write(data)
  output.close()
  