from PIL import Image
import numpy as np
from tkinter import W, filedialog
extension=""
def openfile():
    global im,extension
    filename = filedialog.askopenfilename(filetypes=[('Image file','*.jpg .png .tif .raw'), ('All files','*.*')])
    if filename=='':
        return
    extension=filename[-3:]
    if extension=='raw' : return openfile_raw(filename)
    im=Image.open(filename)
    return im
def save(im):
    f = filedialog.asksaveasfile(mode='w', defaultextension="."+extension,filetypes=[('Image file','*.'+extension)])
    if f is None:
        return
    im.save(f.name)
def openfile_raw(filename):
    global im,extension
    file=open(filename,'rb')
    rawData = file.read()
    file.close()
    if file=='':
        return
    extension='raw'
    im=Image.frombytes('L',(512,512),rawData,'raw')
    return im
if __name__ == "__main__":
    openfile_raw()
    im.show()




