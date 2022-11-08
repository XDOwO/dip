from statistics import mode
import tkinter
import PIL
from PIL import ImageTk
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import functions
import file_io
im=""
tk_image=[]
im_list=[]
p=-1
window = tkinter.Tk()


def show_image(im,r=0,c=0):
    global image_canvas,tk_image
    tk_image.append(ImageTk.PhotoImage(im))
    image_canvas=tkinter.Canvas(window,width=im.size[0],height=im.size[1])
    image_canvas.create_image(0,0,anchor=tkinter.NW, image=tk_image[-1])
    image_canvas.grid(row=r,column=c)
    return image_canvas
def remove_display():
    tk_image.clear()
    for child in window.winfo_children(): child.grid_forget()
def show_homepage():
    remove_display()
    global im,canvas
    show_image(im,c=1)
    button_histogram.grid(column=1,rowspan=3,sticky="ew")
    button_bit_plane.grid(column=1,rowspan=3,sticky="ew")
    button_smoothing.grid(column=1,rowspan=3,sticky="ew")
    button_sharpening.grid(column=1,rowspan=3,sticky="ew")
    button_undo.grid(column=1,rowspan=3,sticky="ew")
    button_save_files.grid(column=1,rowspan=3,sticky="ew")
    

def open_file():
    global im,im_list,p
    im=file_io.openfile()
    im_list.append(im)
    p+=1
    show_homepage()

def call_histogram():
    global im,tk_image,im_list,p
    remove_display()
    # foo=tkinter.Canvas(window,width=im.size[0],height=im.size[1])
    # global im_tk
    # im_tk=ImageTk.PhotoImage(im)
    # foo.create_image(0,0,anchor=tkinter.NW, image=im_tk)
    # foo.grid(row=0,column=0)

    data=functions.histogram(im)
    show_image(im,r=0,c=0)
    f = Figure(figsize=(5,4), dpi=100)
    ax = f.add_subplot(111)
    ax.bar(data[0],data[1])
    canvas = FigureCanvasTkAgg(f, master=window)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0,column=1,columnspan=2,sticky="nsew")

    out=functions.histogram_equalization(im,data)
    new_im=out[2]
    show_image(new_im,r=1,c=0)
    f2 = Figure(figsize=(5,4), dpi=100)
    ax2 = f2.add_subplot(111)
    ax2.bar(out[0],out[1])
    canvas2 = FigureCanvasTkAgg(f2, master=window)
    canvas2.draw()
    canvas2.get_tk_widget().grid(row=1,column=1,columnspan=2,sticky="nsew")
    im=new_im
    p,im_list=functions.undo_setup(im,im_list,p)
    
    tkinter.Button(window,text='Back to Homepage',bg='#62806A',font = ('Arial',18),command=show_homepage).grid(row=3,rowspan=1,columnspan=3,sticky="nsew")
def call_bit_plane():
    remove_display()
    show_image(im,c=1)
    tkinter.Label(window,text='Warning:Bit Value must be less than 8 and greater than -1',bg='#62806A',font = ('Arial',12),fg="#ffffff").grid(column=1)
    bit_entry.grid(column=1)
    tkinter.Button(window,text='Get Bit Value',bg='#62806A',font = ('Arial',12),command=get_bit_and_display_bit_plane).grid(column=1)
def get_bit_and_display_bit_plane():
    remove_display()
    i=-1
    if bit_entry.get()!='':
        i = int(bit_entry.get())
    if(int(i)<0 or int(i)>8): show_homepage()
    else:
        new_im=functions.bit_plane(im,i)
        show_outcome(new_im)

def show_outcome(new_im):
    global im,im_list,p
    im=new_im
    p,im_list=functions.undo_setup(im,im_list,p)
    show_image(new_im,c=1)
    # print(type(im))
    tkinter.Button(window,text='Back to Homepage',bg='#62806A',font = ('Arial',18),command=show_homepage).grid(column=1)

def call_smoothing():
    remove_display()
    show_image(im,c=1)
    tkinter.Button(window,text='Averaging Filter',bg='#62806A',font = ('Arial',18),command=lambda:call__filter_get(0)).grid(column=1)
    tkinter.Button(window,text='Gaussian Filter',bg='#62806A',font = ('Arial',18),command=lambda:call__filter_get(1)).grid(column=1)
    tkinter.Button(window,text='Median Filter',bg='#62806A',font = ('Arial',18),command=lambda:call__filter_get(2)).grid(column=1)

def call__filter_get(filter_mode):
    global filter_entry,sigma_entry
    remove_display()
    show_image(im,c=1)
    frame1=tkinter.Frame(window)
    tkinter.Label(window,text='Warning:Mask size must be an odd number,which 1 is not included.',bg='#62806A',font = ('Arial',12),fg="#ffffff").grid(column=1)
    tkinter.Label(frame1,text='Mask Size:',bg='#62806A',font = ('Arial',12),fg="#ffffff").grid(column=0,row=1,sticky="e")
    filter_entry=tkinter.Entry(frame1,width=5)
    filter_entry.grid(column=1,row=1)
    frame1.grid(column=1)
    if filter_mode==1:
        frame2=tkinter.Frame(window)
        tkinter.Label(frame2,text='Sigma:',bg='#62806A',font = ('Arial',12),fg="#ffffff").grid(column=0,row=2,sticky="e")
        sigma_entry=tkinter.Entry(frame2,width=5)
        sigma_entry.grid(column=1,row=2)
        frame2.grid(column=1)
    tkinter.Button(window,text='Get Scale Value',bg='#62806A',font = ('Arial',12),command=lambda:get_filter_scale_and_display(filter_mode)).grid(column=1)

def get_filter_scale_and_display(filter_mode):
    global im,im_list,p
    remove_display()
    i=-1
    sigma=-1
    if filter_entry.get()!='':
        i = int(filter_entry.get())
        if (filter_mode==0 or filter_mode==2 or filter_mode==3):pass
        elif filter_mode==1 and sigma_entry.get()!='':
            sigma=float(sigma_entry.get())
        else:
            show_homepage()
            return
    # print(i,sigma)
    if i%2==0 or i<0 or i>256 or (sigma==-1 and filter_mode==1): 
        show_homepage()
        return
    if(filter_mode==0):
        new_im=functions.averging_filter(im,i)
    if(filter_mode==1):
        new_im=functions.gaussian_filter(im,i,sigma)
    if(filter_mode==2):
        new_im=functions.median_filter(im,i)
    if(filter_mode==3):
        new_im=functions.sharpening_filter(im,i)
    show_image(new_im,c=1)
    
    im=new_im
    p,im_list=functions.undo_setup(im,im_list,p)
    tkinter.Button(window,text='Back to Homepage',bg='#62806A',font = ('Arial',18),command=show_homepage).grid(column=1)

def call_undo():
    global im,im_list,p
    if(p>=0):im,p,im_list=functions.undo(im_list,p)
    remove_display()
    show_homepage()


window.geometry("1920x1080")
window.title("Hw2")
window.config(bg='#F4FEEC')
title=tkinter.Label(window,text='Welcome to Homework 2',bg='#62806A',font = ('Arial',18),fg="#ffffff",border=34)
button=tkinter.Button(window,text='Open File',bg='#62806A',font = ('Arial',18),command=open_file)
button_histogram=tkinter.Button(window,text='Histogram',bg='#62806A',font = ('Arial',18),command=call_histogram)
button_bit_plane=tkinter.Button(window,text='Bit Plane',bg='#62806A',font = ('Arial',18),command=call_bit_plane)
button_smoothing=tkinter.Button(window,text='Smoothing',bg='#62806A',font = ('Arial',18),command=call_smoothing)
button_sharpening=tkinter.Button(window,text='Sharpening',bg='#62806A',font = ('Arial',18),command=lambda:call__filter_get(3))
button_undo=tkinter.Button(window,text='undo',bg='#62806A',font = ('Arial',18),command=call_undo)

#-----------bit plane entry
bit_entry=tkinter.Entry(window,width=5)
#-----------savefiles
button_save_files=tkinter.Button(window,text='Save Files',bg='#62806A',font = ('Arial',18),command=lambda:file_io.save(im))


# delete_button=tkinter.Button(window,text='D',bg='#62806A',font = ('Arial',18),command=remove_display)
window.columnconfigure(0,weight=1)
window.columnconfigure(1,weight=1)
window.columnconfigure(2,weight=1)
title.grid(row=0,column=1)
button.grid(row=1,column=1)

# delete_button.grid()
window.mainloop()
