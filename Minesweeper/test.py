def gather_images(types=['.png','.jpeg'],recursive=True, tkImage=False):
  from PIL import Image, ImageTk
  import glob
  files = []
  images = {}
  for i,extension in enumerate(types):
    files += glob.glob((f'**/**/**{extension}'),recursive=recursive)
  for i,file in enumerate(files):
    if tkImage:
      images.update({str(file):ImageTk.PhotoImage(Image.open(file))})
    else:
      images.update({str(file):Image.open(file)})
  return images

def play(filename, nodisplay=True, autoexit=True, stdout=False):
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

play('mine_explode.wav',nodisplay=False,autoexit=False,stdout=True)