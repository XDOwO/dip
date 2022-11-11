from statistics import mode
import tkinter
import PIL
from PIL import ImageTk,Image
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
    global iscolor
    remove_display()
    global im,canvas
    show_image(im,c=1)
    if not iscolor:
        button_histogram.grid(column=1,rowspan=3,sticky="ew")
        button_bit_plane.grid(column=1,rowspan=3,sticky="ew")
        button_smoothing.grid(column=1,rowspan=3,sticky="ew")
        button_sharpening.grid(column=1,rowspan=3,sticky="ew")
        button_fft_2d.grid(column=1,rowspan=3,sticky="ew")
        button_ifft_2d.grid(column=1,rowspan=3,sticky="ew")
    else:
        button_display_rgb_component.grid(column=1,rowspan=3,sticky="ew")
        button_display_hsi_component.grid(column=1,rowspan=3,sticky="ew")
        button_color_complement.grid(column=1,rowspan=1,sticky="ew")
        button_color_average_smoothing.grid(column=1,rowspan=3,sticky="ew")
        button_color_sharping.grid(column=1,rowspan=3,sticky="ew")
        button_feather.grid(column=1,rowspan=3,sticky="ew")
    button_undo.grid(column=1,rowspan=3,sticky="ew")
    button_save_files.grid(column=1,rowspan=3,sticky="ew")
def rgb_identifier():
    global iscolor,im
    w, h = im.size
    for i in range(w):
        for j in range(h):
            r, g, b = im.getpixel((i,j))
            if r != g != b:
                iscolor=True
                return
    iscolor = False

def open_file():
    global im,im_list,p
    im=file_io.openfile()
    im_list.append(im)
    p+=1
    rgb_identifier()
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

def call__filter_get(filter_mode,color_mode=""):
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
    tkinter.Button(window,text='Get Scale Value',bg='#62806A',font = ('Arial',12),command=lambda:get_filter_scale_and_display(filter_mode,color_mode)).grid(column=1)

def get_filter_scale_and_display(filter_mode,color_mode=""):
    global im,im_list,p
    remove_display()
    i=-1
    sigma=-1
    if filter_entry.get()!='':
        i = int(filter_entry.get())
        if (filter_mode==0 or filter_mode==2 or filter_mode==3 or filter_mode==4 or filter_mode==5):pass
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
    if(filter_mode==4):
        new_im=functions.color_average_filter(im,i,color_mode)
    if(filter_mode==5):
        new_im=functions.color_sharpening(im,i,color_mode)
    show_image(new_im,c=1)
    
    im=new_im
    p,im_list=functions.undo_setup(im,im_list,p)
    tkinter.Button(window,text='Back to Homepage',bg='#62806A',font = ('Arial',18),command=show_homepage).grid(column=1)

def call_undo():
    global im,im_list,p
    if(p>=0):im,p,im_list=functions.undo(im_list,p)
    remove_display()
    show_homepage()

def call_fft_2d():
    remove_display()
    mag=functions.fft_2d(im)
    show_image(mag,c=1)
    functions.label(window,'Magnitude Spectrum Image').grid(column=1,sticky="ew")
    tkinter.Button(window,text='Back to Homepage',bg='#62806A',font = ('Arial',18),command=show_homepage).grid(row=3,column=1)

def call_ifft_2d():
    remove_display()
    mag,pha=functions.ifft_2d(im)
    show_image(mag,c=0)
    show_image(pha,c=2)
    functions.label(window,'Magnitude only Image After IFFT').grid(row=1,column=0,sticky="ew")
    functions.label(window,'Phase only Image After IFFT').grid(row=1,column=2,sticky="ew")
    tkinter.Button(window,text='Back to Homepage',bg='#62806A',font = ('Arial',18),command=show_homepage).grid(row=3,column=1)

def call_d_i_p(step=1,data=''):
    global im
    im = Image.open("DIP_image.tif")
    remove_display()
    if(step==1):
        functions.label(window,"Multiplying -1**(x+y)").grid(row=1,column=1)
        im=functions.d_i_p_step_1(im)
    elif(step==2):
        functions.label(window,"DFT").grid(row=1,column=1)
        im,data=functions.d_i_p_step_2(im)
    elif(step==3):
        functions.label(window,"Conjugation").grid(row=1,column=1)
        im,data=functions.d_i_p_step_3(data)
    elif(step==4):
        functions.label(window,"Inverse DFT").grid(row=1,column=1)
        im,data=functions.d_i_p_step_4(data)
    elif(step==5):
        functions.label(window,"Real part Multiplying -1**(x+y)").grid(row=1,column=1)
        im=functions.d_i_p_step_5(data)
    else:
        title.grid(row=0,column=1)
        button.grid(row=1,column=1)
        button_d_i_p.grid(row=2,column=1)
        functions.button(window,"hw3-4(e)",call_hw_3_4_e_page1).grid(row=3,column=1)
        return
    show_image(im,r=2,c=1)
    tkinter.Button(window,text='Next',bg='#62806A',font = ('Arial',18),command=lambda:call_d_i_p(step+1,data)).grid(row=3,column=1)

def call_rgb_component():
    remove_display()
    show_image(functions.rgb_component(im,0),c=0)
    show_image(functions.rgb_component(im,1),c=1)
    show_image(functions.rgb_component(im,2),c=2)
    functions.label(window,"Red").grid(column=0,row=1)
    functions.label(window,"Green").grid(column=1,row=1)
    functions.label(window,"Blue").grid(column=2,row=1)
    button_homepage.grid(column=1,row=2)

def call_hsi_component():
    remove_display()
    show_image(functions.hsi_component(im,0),c=0)
    show_image(functions.hsi_component(im,1),c=1)
    show_image(functions.hsi_component(im,2),c=2)
    functions.label(window,"Hue").grid(column=0,row=1)
    functions.label(window,"Saturation").grid(column=1,row=1)
    functions.label(window,"Intensity").grid(column=2,row=1)
    button_homepage.grid(column=1,row=2)

def call_color_complement():
    global im
    remove_display()
    show_image(im:=functions.color_complement(im),c=1)
    button_homepage.grid(column=1,row=2)

def call_color_sharp_or_smooth(mode):
    remove_display()
    show_image(im,r=0,c=1)
    if mode == 'smooth':
        functions.button(window,"RGB",lambda:call__filter_get(4,"RGB")).grid(row=1,columnspan=3,sticky="ew")
        functions.button(window,"HSI",lambda:call__filter_get(4,"HSI")).grid(row=2,columnspan=3,sticky="ew")
        functions.button(window,"HSV",lambda:call__filter_get(4,"HSV")).grid(row=3,columnspan=3,sticky="ew")
    if mode == "sharp":
        functions.button(window,"RGB",lambda:call__filter_get(5,"RGB")).grid(row=1,columnspan=3,sticky="ew")
        functions.button(window,"HSI",lambda:call__filter_get(5,"HSI")).grid(row=2,columnspan=3,sticky="ew")
        functions.button(window,"HSV",lambda:call__filter_get(5,"HSV")).grid(row=3,columnspan=3,sticky="ew")
    
def call_hw_3_4_e_page1():
    def show_image_hw(im,f,r=0,c=0):
        global im_o,im_a_r,im_s_r,im_a_h,im_s_h
        global f1,f2,f3,f4,f5
        global image_canvas,tk_image
        tk_image.append(ImageTk.PhotoImage(im))
        image_canvas=tkinter.Canvas(f,width=im.size[0],height=im.size[1])
        image_canvas.create_image(0,0,anchor=tkinter.NW, image=tk_image[-1])
        image_canvas.grid(row=r,column=c)
        return image_canvas

    remove_display()
    im_o=Image.open("Lenna_512_color.tif")
    im_a_r=Image.open(".\\q4\\averag_filter_5x5_rgb_lenna.tif")
    im_s_r=Image.open(".\\q4\\sharpening_after_averag_filter_5x5_rgb_lenna.tif")
    f1=tkinter.Frame(window,bg='#62806A')
    f2=tkinter.Frame(window,bg='#62806A')
    f3=tkinter.Frame(window,bg='#62806A')
    show_image_hw(im_o,f1,r=0,c=1)
    tkinter.Label(f1,text='Original Image',bg='#62806A',font = ('Arial',12),fg="#ffffff",border=34).grid(column=1,row=1)
    show_image_hw(im_a_r,f2,r=0,c=1)
    tkinter.Label(f2,text='Average Filter 5x5 RGB',bg='#62806A',font = ('Arial',12),fg="#ffffff",border=34).grid(column=1,row=1)
    show_image_hw(im_s_r,f3,r=0,c=1)
    tkinter.Label(f3,text='Laplacian Sharping Average Filter 5x5 RGB',bg='#62806A',font = ('Arial',12),fg="#ffffff",border=34).grid(column=1,row=1)
    f1.grid(row=0,column=0)
    f2.grid(row=0,column=1)
    f3.grid(row=0,column=2)
    functions.button(window,"next",lambda:call_hw_3_4_e_page2()).grid(row=2,column=1)
def call_hw_3_4_e_page2():
    def show_image_hw(im,f,r=0,c=0):
        global im_o,im_a_r,im_s_r,im_a_h,im_s_h
        global f1,f2,f3,f4,f5
        global image_canvas,tk_image
        tk_image.append(ImageTk.PhotoImage(im))
        image_canvas=tkinter.Canvas(f,width=im.size[0],height=im.size[1])
        image_canvas.create_image(0,0,anchor=tkinter.NW, image=tk_image[-1])
        image_canvas.grid(row=r,column=c)
        return image_canvas

    remove_display()
    im_o=Image.open("Lenna_512_color.tif")
    im_a_h=Image.open(".\\q4\\averag_filter_5x5_hsi_lenna.tif")
    im_s_h=Image.open(".\\q4\\sharpening_after_averag_filter_5x5_hsi_lenna.tif")
    f1=tkinter.Frame(window,bg='#62806A')
    f4=tkinter.Frame(window,bg='#62806A')
    f5=tkinter.Frame(window,bg='#62806A')
    show_image_hw(im_o,f1,r=0,c=1)
    tkinter.Label(f1,text='Original Image',bg='#62806A',font = ('Arial',12),fg="#ffffff",border=34).grid(column=1,row=1)
    show_image_hw(im_a_h,f4,r=0,c=1)
    tkinter.Label(f4,text='Average Filter 5x5 HSI',bg='#62806A',font = ('Arial',12),fg="#ffffff",border=34).grid(column=1,row=1)
    show_image_hw(im_s_h,f5,r=0,c=1)
    tkinter.Label(f5,text='Laplacian Sharping Average Filter 5x5 HSI',font = ('Arial',12),fg="#ffffff",border=34).grid(column=1,row=1)
    f1.grid(row=0,column=0)
    f4.grid(row=0,column=1)
    f5.grid(row=0,column=2)
    functions.button(window,"next",lambda:call_hw_3_4_e_page3()).grid(row=2,column=1)
def call_hw_3_4_e_page3():
    def show_image_hw(im,f,r=0,c=0):
        global im_o,im_a_r,im_s_r,im_a_h,im_s_h
        global f1,f2,f3,f4,f5
        global image_canvas,tk_image
        tk_image.append(ImageTk.PhotoImage(im))
        image_canvas=tkinter.Canvas(f,width=im.size[0],height=im.size[1])
        image_canvas.create_image(0,0,anchor=tkinter.NW, image=tk_image[-1])
        image_canvas.grid(row=r,column=c)
        return image_canvas
    def back():
        global button,title,button_d_i_p
        remove_display()
        title.grid(row=0,column=1)
        button.grid(row=1,column=1)
        button_d_i_p.grid(row=2,column=1)
        functions.button(window,"hw3-4(e)",call_hw_3_4_e_page1).grid(row=3,column=1)
    remove_display()
    im_a_r=Image.open(".\\q4\\averag_filter_5x5_rgb_lenna.tif")
    im_s_r=Image.open(".\\q4\\sharpening_after_averag_filter_5x5_rgb_lenna.tif")
    im_a_h=Image.open(".\\q4\\averag_filter_5x5_hsi_lenna.tif")
    im_s_h=Image.open(".\\q4\\sharpening_after_averag_filter_5x5_hsi_lenna.tif")
    f2=tkinter.Frame(window,bg='#62806A')
    f3=tkinter.Frame(window,bg='#62806A')
    show_image_hw(im_a_r,f2,r=0,c=1)
    tkinter.Label(f2,text='Average Filter 5x5 RGB',bg='#62806A',font = ('Arial',8),fg="#ffffff",border=5).grid(column=1,row=1)
    show_image_hw(im_s_r,f3,r=0,c=1)
    tkinter.Label(f3,text='Laplacian Sharping Average Filter 5x5 RGB',bg='#62806A',font = ('Arial',8),fg="#ffffff",border=5).grid(column=1,row=1)
    f4=tkinter.Frame(window,bg='#62806A')
    f5=tkinter.Frame(window,bg='#62806A')
    show_image_hw(im_a_h,f4,r=0,c=1)
    tkinter.Label(f4,text='Average Filter 5x5 HSI',bg='#62806A',font = ('Arial',8),fg="#ffffff",border=5).grid(column=1,row=1)
    show_image_hw(im_s_h,f5,r=0,c=1)
    tkinter.Label(f5,text='Laplacian Sharping Average Filter 5x5 HSI',font = ('Arial',8),fg="#ffffff",border=5).grid(column=1,row=1)
    f2.grid(row=0,column=0)
    f3.grid(row=0,column=2)
    f4.grid(row=1,column=0)
    f5.grid(row=1,column=2)
    functions.button(window,"back",lambda:back()).grid(row=1,column=1,columnspan=1,sticky="ew")

def call_feather():
    global im,p,im_list
    remove_display()
    new_im = functions.feather(im)
    show_image(new_im,c=1)
    p,im_list=functions.undo_setup(im,im_list,p)
    im = new_im
    button_homepage.grid(column=1)
    
   
    
window.geometry("1920x1080")
window.title("Hw2")
window.config(bg='#F4FEEC')
# grayscale image function in hw2
title=tkinter.Label(window,text='Welcome to Homework 2',bg='#62806A',font = ('Arial',18),fg="#ffffff",border=34)
button=tkinter.Button(window,text='Open File',bg='#62806A',font = ('Arial',18),command=open_file)
button_histogram=tkinter.Button(window,text='Histogram',bg='#62806A',font = ('Arial',18),command=call_histogram)
button_bit_plane=tkinter.Button(window,text='Bit Plane',bg='#62806A',font = ('Arial',18),command=call_bit_plane)
button_smoothing=tkinter.Button(window,text='Smoothing',bg='#62806A',font = ('Arial',18),command=call_smoothing)
button_sharpening=tkinter.Button(window,text='Sharpening',bg='#62806A',font = ('Arial',18),command=lambda:call__filter_get(3))
# grayscale image function in hw3
button_fft_2d=functions.button(window,'Display FFT',call_fft_2d)
button_ifft_2d=functions.button(window,'Display After FFT Invert',call_ifft_2d)
button_d_i_p=functions.button(window,'Hw3-3',call_d_i_p)
bit_entry=tkinter.Entry(window,width=5)
# color image
button_display_rgb_component = functions.button(window,"Display Component in RGB",call_rgb_component)
button_display_hsi_component = functions.button(window,"Display Component in HSI",call_hsi_component)
button_color_complement = functions.button(window,"Color Complement",call_color_complement)
button_color_average_smoothing = functions.button(window,"Average Smoothing",lambda:call_color_sharp_or_smooth("smooth"))
button_color_sharping = functions.button(window,"Laplacian Sharping",lambda:call_color_sharp_or_smooth("sharp"))
button_feather = functions.button(window,"Feahter",call_feather)
# undo and save (for rgb and grayscale)
button_undo=tkinter.Button(window,text='undo',bg='#62806A',font = ('Arial',18),command=call_undo)
button_save_files=tkinter.Button(window,text='Save Files',bg='#62806A',font = ('Arial',18),command=lambda:file_io.save(im))
#Back to homepage
button_homepage=tkinter.Button(window,text='Back to Homepage',bg='#62806A',font = ('Arial',18),command=show_homepage)

# delete_button=tkinter.Button(window,text='D',bg='#62806A',font = ('Arial',18),command=remove_display)
window.columnconfigure(0,weight=1)
window.columnconfigure(1,weight=1)
window.columnconfigure(2,weight=1)
title.grid(row=0,column=1)
button.grid(row=1,column=1)
button_d_i_p.grid(row=2,column=1)
functions.button(window,"hw3-4(e)",call_hw_3_4_e_page1).grid(row=3,column=1)
# delete_button.grid()
window.mainloop()
