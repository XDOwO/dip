from PIL import Image,ImageEnhance,ImageStat,ImageTk
from math import log,e
import tkinter
from tkinter import W, filedialog
im=0
img2=0

mode=0
p=0
rp=0
undo_list=[]
act_list=["buffer"]
degree_list=[0]
rotate_degree=0
def canvas_setup():
    global img2,im,canvas
    img2 = ImageTk.PhotoImage(im)
    canvas=tkinter.Canvas(window,width=im.size[0],height=im.size[1])
    canvas.create_image(0,0,anchor=tkinter.NW, image=img2)
def save():
    f = filedialog.asksaveasfile(mode='w', defaultextension="."+extension,filetypes=[('Image file','*.'+extension)])
    if f is None:
        return
    im.save(f.name)
def openfile():
    filename = filedialog.askopenfilename(filetypes=[('Image file','*.jpg .png .tif'), ('All files','*.*')])
    if filename=='':
        return
    global im,button_contrast,extension,original_im,undo_list
    extension=filename[-3:]
    title.pack_forget()
    button.pack_forget()
    im=Image.open(filename)
    original_im=im
    # im.show()
    canvas_setup()
    display_editor_buttons()
    undo_list.append(im)
    return im
def contrast():
    canvas.pack_forget()
    global x,im,filter
    x=ImageStat.Stat(im).rms[0]/256
    # print(x)
    filter="contrast"
    delete_editor_buttons()
    display_method_buttons()
def brightness():
    global x,im,filter
    x=ImageStat.Stat(im).rms[0]/256
    filter="brightness"
    delete_editor_buttons()
    display_method_buttons()
def scale():
    global im,h,w
    h,w=im.size
    delete_editor_buttons()
    display_resize_buttons()
def rotate():
    delete_editor_buttons()
    display_rotate_buttons()
def grey_slicing():
    delete_editor_buttons()
    display_grey_buttons()
def display_editor_buttons():
    global act_list,im_r
    canvas.pack()
    button_contrast.pack(fill='x')
    button_brightness.pack(fill='x')
    button_zoom_in.pack(fill='x')
    button_rotate.pack(fill='x')
    button_grey_slicing.pack(fill='x')
    button_reset.pack(fill='x')
    button_undo.pack(fill='x')
    button_save.pack(fill='x',side='bottom')
    if(act_list[p]!='r'): im_r=im
def delete_editor_buttons():
    canvas.pack_forget()
    button_contrast.pack_forget()
    button_brightness.pack_forget()
    button_save.pack_forget()
    button_zoom_in.pack_forget()
    button_rotate.pack_forget()
    button_grey_slicing.pack_forget()
    button_reset.pack_forget()
    button_undo.pack_forget()
def display_method_buttons():
    canvas.pack()
    button_linear.pack(fill='x')
    button_exp.pack(fill='x')
    button_log.pack(fill='x')
def delete_method_buttons():
    canvas.pack_forget()
    button_linear.pack_forget()
    button_exp.pack_forget()
    button_log.pack_forget()
def display_input_buttons():
    canvas.pack()
    label_a.pack()
    entry_a.pack()
    label_b.pack()
    entry_b.pack()
    button_confirm.pack()
def delete_input_buttons():
    canvas.pack_forget()
    label_a.pack_forget()
    entry_a.pack_forget()
    label_b.pack_forget()
    entry_b.pack_forget()
    button_confirm.pack_forget()
def display_resize_buttons():
    canvas.pack()
    label_s.pack()
    entry_s.pack()
    button_confirm_s.pack()
def delete_resize_buttons():
    canvas.pack_forget()
    label_s.pack_forget()
    entry_s.pack_forget()
    button_confirm_s.pack_forget()
def display_rotate_buttons():
    canvas.pack()
    label_r.pack()
    entry_r.pack()
    button_confirm_r.pack()
def delete_rotate_buttons():
    canvas.pack_forget()
    label_r.pack_forget()
    entry_r.pack_forget()
    button_confirm_r.pack_forget()
def display_grey_buttons():
    canvas.pack()
    label_g1.pack()
    slider_g1.pack()
    label_g2.pack()
    slider_g2.pack()
    button_confirm_g.pack()
def delete_grey_buttons():
    canvas.pack_forget()
    label_g1.pack_forget()
    slider_g1.pack_forget()
    label_g2.pack_forget()
    slider_g2.pack_forget()
    button_confirm_g.pack_forget()
def display_yes_no_g_buttons():
    canvas.pack()
    label_yes_or_no_g.pack()
    button_yes_g.pack()
    button_no_g.pack()
def delete_yes_no_g_buttons():
    canvas.pack_forget()
    label_yes_or_no_g.pack_forget()
    button_yes_g.pack_forget()
    button_no_g.pack_forget()
def get_a_and_b():
    global a,b
    a=1
    b=0
    if entry_a.get()!='':
        a= entry_a.get()
    if entry_b.get()!='':
        b= entry_b.get()
    delete_input_buttons()
    outcome()
def get_s():
    global s
    s=100
    if entry_s.get()!='':
        s = float(entry_s.get())
    delete_resize_buttons()
    im_resize()
def get_r():
    global r,rotate_degree
    r=0
    if entry_r.get()!='':
        r = float(entry_r.get())
    rotate_degree+=r
    delete_rotate_buttons()
    im_rotate()
def get_g():
    global g1,g2
    g1=0
    g2=0
    if slider_g1.get()!='':
        g1 = float(slider_g1.get())
    if slider_g2.get()!='':
        g2 = float(slider_g2.get())
    delete_grey_buttons()
    display_yes_no_g_buttons()
def yes_g():
    global g_mode
    g_mode=1
    delete_yes_no_g_buttons()
    im_grey_slicing()
def no_g():
    global g_mode
    g_mode=0
    delete_yes_no_g_buttons()
    im_grey_slicing()
def im_resize():
    global im,w,h,s,canvas
    size=(int(w*s/100),int(h*s/100))
    # print(h,w,size)
    im=im.resize(size)
    undo_setup(im,'s')
    canvas_setup()
    display_editor_buttons()
    
def im_rotate():
    global im,rotate_degree,im_r
    im=im_r.rotate(rotate_degree)
    undo_setup(im,'r')
    canvas_setup()
    display_editor_buttons()
    
def im_grey_slicing():
    pixel_grey_slicing()
    canvas_setup()
    display_editor_buttons()
def pixel_grey_slicing():
    global g1,g2,im,g_mode
    grey_im=im.convert('L')
    for i in range(grey_im.size[0]):
        for j in range(grey_im.size[1]):
            if not g1<=grey_im.getpixel((i,j))<=g2:
                grey_im.putpixel((i,j),255)
            elif g_mode==1:
                grey_im.putpixel((i,j),0)
    im=grey_im
    undo_setup(im,'g')
def reset():
    global im,original_im,undo_list,p,rotate_degree
    im=original_im
    rotate_degree=0
    undo_setup(im,'re')
    delete_editor_buttons()
    canvas_setup()   
    display_editor_buttons()
def undo():
    global p,undo_list,im,rotate_degree,rp
    if p>=1 and (act_list[p]=='r' or act_list[p]=='re'):
        rp-=1
        degree_list.pop(-1)
        rotate_degree=degree_list[rp]
       # print(degree_list)
    if(p>0):p-=1
    im=undo_list[p]
    delete_editor_buttons()
    canvas_setup()   
    display_editor_buttons()
def linear():
    global mode
    delete_method_buttons()
    display_input_buttons()
    mode=0
def exponential():
    delete_method_buttons()
    display_input_buttons()
    global mode
    mode=1
def logarithmical():
    delete_method_buttons()
    display_input_buttons()
    global mode
    mode=2
def outcome():

    global im,a,b,filter
    a=float(a)
    b=float(b)
    grey_im=im.convert('L')
    if filter=="brightness":
        for i in range(grey_im.size[0]):
            for j in range(grey_im.size[1]):
                x=grey_im.getpixel((i,j))
                value=(a*x+b)
                if(mode==0):
                    pass
                elif mode==1:
                    value=e**value
                    if(value>2**32): value=255
                else:
                    value=log(value)
                grey_im.putpixel((i,j),int(value))
    else:
        max=0
        min=256
        
        for i in range(grey_im.size[0]):
            for j in range(grey_im.size[1]):
                if grey_im.getpixel((i,j))>max:max=grey_im.getpixel((i,j))
                if grey_im.getpixel((i,j))<min:min=grey_im.getpixel((i,j))
        # print(max,min)
        contrast=(max-min)/256
        for i in range(grey_im.size[0]):
            for j in range(grey_im.size[1]):
                pixel=grey_im.getpixel((i,j))-128
                value=(a*contrast+b)
                if(mode==0):
                    pass
                elif mode==1:
                    value=e**value
                    if(value>2**32): value=255
                else:
                    value=log(value)
                value=value/contrast
                grey_im.putpixel((i,j),int(value*pixel+128))
    im=grey_im
    undo_setup(im,'b and c')
    canvas_setup()
    display_editor_buttons()
    
def undo_setup(im,c):
    global undo_list,p,act_list,degree_list,rotate_degree,rp
    if(p==len(undo_list)-1):
        undo_list.append(im)
        act_list.append(c)
        if c=='r':
            degree_list.append(rotate_degree)
            rp+=1
        if c=='re':
            degree_list.append(0)
            rp+=1
        p+=1
    else:
        undo_list=undo_list[0:p+1]
        undo_list.append(im)
        act_list=act_list[0:p+1]
        act_list.append(c)
        if c=='r':
            degree_list=degree_list[0:rp+1]
            degree_list.append(rotate_degree)
            rp+=1
        if c=='re':
            degree_list=degree_list[0:rp+1]
            degree_list.append(0)
            rp+=1
        p+=1
    #print(act_list)
window = tkinter.Tk()
window.geometry("1920x1080")
window.title("Hw1")
window.config(bg='#F4FEEC')
title=tkinter.Label(window,text='Welcome to Homework 1',bg='#62806A',font = ('Arial',18),fg="#ffffff",border=34)
button=tkinter.Button(window,text='Open File',bg='#62806A',font = ('Arial',18),command=openfile)
button_contrast=tkinter.Button(window,text='Change contrast',bg='#62806A',font = ('Arial',18),command=contrast)
button_brightness=tkinter.Button(window,text='Change brightness',bg='#62806A',font = ('Arial',18),command=brightness)
button_zoom_in=tkinter.Button(window,text='Zoom In/Out',bg='#62806A',font = ('Arial',18),command=scale)
button_rotate=tkinter.Button(window,text='Rotate',bg='#62806A',font = ('Arial',18),command=rotate)
button_grey_slicing=tkinter.Button(window,text='Grey Level Slicing',bg='#62806A',font = ('Arial',18),command=grey_slicing)
button_reset=tkinter.Button(window,text='Reset',bg='#62806A',font = ('Arial',18),command=reset)
button_undo=tkinter.Button(window,text='Undo',bg='#62806A',font = ('Arial',18),command=undo)
#-----------------
button_linear=tkinter.Button(window,text='linear',bg='#62806A',font = ('Arial',18),command=linear)
button_exp=tkinter.Button(window,text='exponential',bg='#62806A',font = ('Arial',18),command=exponential)
button_log=tkinter.Button(window,text='logarithmical',bg='#62806A',font = ('Arial',18),command=logarithmical)
canvas_for_input=tkinter.Canvas(window,width=400,height=400)
label_a=tkinter.Label(window,text='Input a',bg='#62806A',font = ('Arial',10),fg="#ffffff")
label_b=tkinter.Label(window,text='Input b',bg='#62806A',font = ('Arial',10),fg="#ffffff")
entry_a=tkinter.Entry(window,width=5)
entry_b=tkinter.Entry(window,width=5)
label_s=tkinter.Label(window,text='Input scale(unit:%)',bg='#62806A',font = ('Arial',10),fg="#ffffff")
entry_s=tkinter.Entry(window,width=5)
label_r=tkinter.Label(window,text='Input angle(unit:degree)',bg='#62806A',font = ('Arial',10),fg="#ffffff")
entry_r=tkinter.Entry(window,width=5)
label_g1=tkinter.Label(window,text='The lower limit',bg='#62806A',font = ('Arial',10),fg="#ffffff")
slider_g1 = tkinter.Scale(window, from_=0, to=255, orient='horizontal')
label_g2=tkinter.Label(window,text='The upper limit',bg='#62806A',font = ('Arial',10),fg="#ffffff")
slider_g2 = tkinter.Scale(window, from_=0, to=255, orient='horizontal')
button_confirm=tkinter.Button(window,text='confirm',bg='#62806A',font = ('Arial',10),command=get_a_and_b)
button_confirm_s=tkinter.Button(window,text='confirm',bg='#62806A',font = ('Arial',10),command=get_s)
button_confirm_r=tkinter.Button(window,text='confirm',bg='#62806A',font = ('Arial',10),command=get_r)
button_confirm_g=tkinter.Button(window,text='confirm',bg='#62806A',font = ('Arial',10),command=get_g)
label_yes_or_no_g=tkinter.Label(window,text='Do you want to change the unselectedd area to black?',bg='#62806A',font = ('Arial',10),fg="#ffffff")
button_yes_g=tkinter.Button(window,text='Yes!',bg='#62806A',font = ('Arial',10),command=yes_g)
button_no_g=tkinter.Button(window,text='No:(',bg='#62806A',font = ('Arial',10),command=no_g)
button_save=tkinter.Button(window,text='Save Files',bg='#62806A',font = ('Arial',10),command=save)

title.pack(pady=100)
button.pack()
window.mainloop()


# s=input("Please enter the name of image:")
# with Image.open(s,"r") as image:
#     display(image)
#     image=contrast(image,3,5)
#     display(image)
#     image=brightness(image,3,5)
#     save(image)