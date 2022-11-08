
from PIL import Image
from math import pi,e
import numpy as np
import matplotlib.pyplot as plt
import cv2
def histogram(im):
    h=im.size[0]
    v=im.size[1]
    color=np.array(im)
    data=np.zeros(256,dtype=int)
    for y in range(v):
        for x in range(h):
            data[color[y][x]]+=1
    np_coor=np.array([i for i in range(256)])
    return (np_coor,data)
def histogram_equalization(im,data):
    h=im.size[0]
    v=im.size[1]
    np_data=data[1]
    probability=[0 for i in range(256)]
    pixel_nums=im.size[0]*im.size[1]
    for i in range(len(np_data)):
        probability[i]=float(np_data[i]/pixel_nums)
        if i!=0: probability[i]+=probability[i-1]
    equalization_map=[0 for i in range(256)]
    for i in range(256):
        equalization_map[i]=round(probability[i]*255)
    new_im=im.convert('L')
    for y in range(v):
        for x in range(h):
            pixel=im.getpixel((x,y))
            new_im.putpixel((x,y),equalization_map[pixel])
            np_data[pixel]-=1
            np_data[equalization_map[pixel]]+=1
    np_coor=np.array([i for i in range(256)])
    return (np_coor,np_data,new_im)

def bit_plane(im,value):
    h=im.size[0]
    v=im.size[1]
    new_im=im.convert('L')
    i=2**(value+1)
    for y in range(v):
        for x in range(h):
            if(im.getpixel((x,y))%i>=(i/2)):new_im.putpixel((x,y),255)
            else: new_im.putpixel((x,y),0)
    return new_im

# def averging_filter(im,value):
#     cv_image=np.array(im)
#     new_im=cv2.blur(cv_image,(value,value))
#     new_im = Image.fromarray(new_im)
    # return new_im
def averging_filter(im,value):
    h=im.size[0]
    v=im.size[1]
    b=(value-1)//2
    new_im=im.convert('L')
    color=np.array(im)
    color_with_border=np.pad(color,(b),"constant")
    for y in range(b,v+b):
        for x in range(b,h+b):
            average_v=int(np.average(color_with_border[y-b:y+b+1,x-b:x+b+1]))
            new_im.putpixel((x-b,y-b),average_v)
                    
    return new_im
                   
                    
def gaussian_filter(im,value,std):
    h=im.size[0]
    v=im.size[1]
    b=(value-1)//2
    new_im=im.convert('L')
    mask=np.empty([value,value],float)
    color=np.array(im)
    color_with_border=np.pad(color,(b),"constant")
    
    for y in range(-b,b+1):
        for x in range(-b,b+1):
            # print(x,y)
            mask[y+b][x+b]=1/(2*pi*std**2)*e**-((x**2+y**2)/(2*std**2))
    mask=np.divide(mask,np.sum(mask))
    # print(mask)
    for y in range(b,v+b):
        for x in range(b,h+b):
            # print(color_with_border[y-b:y+b+1,x-b:x+b+1])
            average_v=int(np.sum(np.multiply(color_with_border[y-b:y+b+1,x-b:x+b+1],mask)))
            new_im.putpixel((x-b,y-b),average_v)
    return new_im
    
def median_filter(im,value):
    h=im.size[0]
    v=im.size[1]
    b=(value-1)//2
    new_im=im.convert('L')
    color=np.array(im)
    color_with_border=np.pad(color,(b),"constant")
    for y in range(b,v+b):
        for x in range(b,h+b):
            average_v=int(np.median(color_with_border[y-b:y+b+1,x-b:x+b+1]))
            new_im.putpixel((x-b,y-b),average_v)
                    
    return new_im

def sharpening_filter(im,value):
    # print(value,std)
    h=im.size[0]
    v=im.size[1]
    b=(value-1)//2
    new_im=im.convert('L')
    mask=np.ones([value,value],int)
    mask[b][b]=((value**2)-1)*-1
    # print(b)
    color=np.array(im)
    color_with_border=np.pad(color,(b),"constant")
    
    

    # print(mask)
    for y in range(b,v+b):
        for x in range(b,h+b):
            # print(color_with_border[y-b:y+b+1,x-b:x+b+1])
            average_v=int(np.sum(np.multiply(color_with_border[y-b:y+b+1,x-b:x+b+1],mask)))
            new_im.putpixel((x-b,y-b),int(color_with_border[y-b][x-b])-average_v)
    return new_im
def undo_setup(im,im_list,p):
    if(p!=len(im_list)-1):
        im_list=im_list[:p+1]
    p+=1
    im_list.append(im)
    # print(p,len(im_list))
    return (p,im_list)
def undo(im_list,p):
    if(p>0):p-=1
    im=im_list[p]
    # print(im_list)
    
    return (im,p,im_list)
if "__main__"==__name__:
    import file_io
    im=file_io.openfile()  
    im.show()
    sharpening_filter(im,3,1).show()

