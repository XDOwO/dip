
from PIL import Image
import tkinter
from math import pi,e,cos,sin,sqrt,acos,radians,degrees
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

def convert_array_to_img(arr,color='L'):
    return Image.fromarray(np.uint8(arr) , color)
def button(window,text_,command_):
    return tkinter.Button(window,text=text_,bg='#62806A',font = ('Arial',18),command=command_)
def label(window,text_):
    return tkinter.Label(window,text=text_,bg='#62806A',font = ('Arial',15),fg="#ffffff",border=34)
def fft_2d(im):
    arr=np.fft.fftshift(np.fft.fft2(im))
    mag_im=convert_array_to_img(np.multiply(np.log(np.abs(arr)),256/np.max(np.log(np.abs(arr)))))
    # mag_im=convert_array_to_img(20*np.log(np.abs(arr)))
    # pha_im=convert_array_to_img(np.multiply(np.log(np.abs(np.angle(arr))),256/np.max(np.log(np.abs(np.angle(arr))))))
    
    # pha_im=convert_array_to_img(20*np.log(np.abs(np.angle(arr))))
    return mag_im

def ifft_2d(im):
    arr = np.fft.fftshift(np.fft.fft2(im))
    mag = np.abs(arr)
    pha = arr / np.abs(arr)
    mag_arr = np.fft.ifft2(np.fft.ifftshift(mag))
    pha_arr = np.fft.ifft2(np.fft.ifftshift(pha))
    mag_im=convert_array_to_img(np.multiply(np.log(mag_arr),20))
    pha_im=convert_array_to_img(np.multiply(np.log(pha_arr),20))
    # mag_im=convert_array_to_img(np.multiply(np.log(mag_arr),256/np.max(np.log(mag_arr))))
    # pha_im=convert_array_to_img(np.multiply(np.log(np.abs(pha_arr)),256/np.max(np.log(np.abs(pha_arr)))))
    
    # test_im=convert_array_to_img(np.add(np.multiply(np.log(mag_arr),20),np.multiply(np.log(pha_arr),20)))
    # test_im.show()
    return mag_im,pha_im
def d_i_p_step_1(im):
    arr=np.array(im)
    h=im.size[0]
    v=im.size[1]
    for y in range(v):
        for x in range(h):
            # im.putpixel((x,y),im.getpixel((x,y)*(-1)**(x+y)))
            arr[y][x]=arr[y][x]*((-1)**(x+y))
    return convert_array_to_img(arr)
def d_i_p_step_2(im):
    show_im=fft_2d(im)
    im_data=np.fft.fftshift(np.fft.fft2(im))
    return show_im,im_data

def d_i_p_step_3(data):
    data=np.conj(data)
    show_im=convert_array_to_img(np.multiply(np.log(np.abs(data)),256/np.max(np.log(np.abs(data)))))
    return show_im,data

def d_i_p_step_4(data):
    data = np.fft.ifft2(np.fft.ifftshift(data))
    show_im=convert_array_to_img(np.multiply(np.log(data),20))
    return show_im,data

def d_i_p_step_5(arr):
    for y in range(len(arr)):
        for x in range(len(arr[0])):
            arr[y][x]=arr[y][x].real*(-1)**(x+y)+arr[y][x].imag*1j
    return convert_array_to_img(arr)



def rgb_component(im,channel):
    # (r,g,b) in channel =(0,1,2)
    im = im.split()[channel].convert('RGB')
    h,v=im.size
    arr = np.array(im)
    mul = [0,0,0]
    mul[channel] = 1
    for i in range(v):
        for j in range(h):
            arr[i][j] = np.multiply(arr[i][j],mul)
    return convert_array_to_img(arr,"RGB")
def hsi_component(im,channel):
    # (h,s,i) in channel =(0,1,2)
    hsv_im = im.convert('HSV')
    lim = im.convert('L')
    h,v=im.size
    hsv_im_arr = np.array(hsv_im)
    if channel==0 :
        for i in range(v):
            for j in range(h):
                r,g,b=im.getpixel((j,i))
                lim.putpixel((j,i),rgb_to_hue(r,g,b))
        return lim
    elif channel==1:
        for i in range(v):
            for j in range(h):
                r,g,b=im.getpixel((j,i))
                lim.putpixel((j,i),rgb_to_saturity(r,g,b))
        # print(convert_array_to_img(arr))
        return lim
    else:
        for i in range(v):
            for j in range(h):
                r,g,b=im.getpixel((j,i))
                lim.putpixel((j,i),rgb_to_intensity(r,g,b))
        return lim
    # print(hsv_im_arr)
    # return im

def color_complement(im):
    arr = np.array(im)
    h,v=im.size
    for i in range(v):
        for j in range(h):
            arr[i][j][0] = 255 - arr[i][j][0]
            arr[i][j][1] = 255 - arr[i][j][1]
            arr[i][j][2] = 255 - arr[i][j][2]
    return convert_array_to_img(arr,"RGB")

# def convert_to_H_in_HSI(im):
#     # l_arr = np.array(im.convert('L'))
#     rgb_arr= np.array(im.convert('RGB'))
#     rgb_arr=rgb_arr/255
#     h,v=im.size
#     arr=np.array(im.convert('L'))
#     # rgb_arr[0][0] = (160,164,36)
#     for i in range(v):
#         for j in range(h):
#             arr[i][j] = rgb_to_hue(*rgb_arr[i][j])*255+0.5
#     return convert_array_to_img(arr)

# def convert_to_S_in_HSI(im):
#     # l_arr = np.array(im.convert('L'))
#     rgb_arr= np.array(im.convert('RGB'))
#     rgb_arr=rgb_arr/255
#     h,v=im.size
#     arr=np.array(im.convert('L'))
#     # rgb_arr[0][0] = (160,164,36)
#     for i in range(v):
#         for j in range(h):
#             arr[i][j] = rgb_to_saturity(*rgb_arr[i][j])*255+0.5
#     # print(arr[0][0])
#     return convert_array_to_img(arr)

# def convert_to_I_in_HSI(im):
#     # l_arr = np.array(im.convert('L'))
#     rgb_arr= np.array(im.convert('RGB'))
#     rgb_arr=rgb_arr/255
#     h,v=im.size
#     arr=np.array(im.convert('L'))
#     # rgb_arr[0][0] = (160,164,36)
#     for i in range(v):
#         for j in range(h):
#             arr[i][j] = rgb_to_intensity(*rgb_arr[i][j])*255+0.5
#     # print(arr[0][0])
#     return convert_array_to_img(arr)

# def convert_hsi_to_rgb(h,s,i,img):
    
    
#     h=h*360.0/255
#     i=i/255
#     img = np.array(img)
#     s = s/255
#     im = np.empty([len(h),len(h[0]),3],dtype=int)
#     for y in range(len(h)):
#         for x in range(len(h[0])):
#             im[y][x] = np.array(HSI_to_rgb(h[y][x],s[y][x],i[y][x]))*255+0.5
            # rgb=[0,0,0]
            # hp=h[y][x]/60
            # z = 1 - abs(int(hp+0.5)%2-1)
            # c = (3*i[y][x]*s[y][x]) / (1 + z)
            # xx = c*z
            # if img[y][x][0]==img[y][x][1]==img[y][x][2]:
            #     rgb=[0,0,0]
            # elif 0 <= hp <= 1:
            #     rgb=[c,xx,0]
            # elif 1 <= hp <= 2:
            #     rgb=[xx,c,0]
            # elif 2 <= hp <= 3:
            #     rgb=[0,c,xx]
            # elif 3 <= hp <= 4:
            #     rgb=[0,xx,c]
            # elif 4 <= hp <= 5:
            #     rgb=[xx,0,c]
            # elif 5 <= hp < 6:
            #     rgb=[c,0,xx]
            # m = i[y][x] * (1-s[y][x])
            # im[y][x]=(np.array(rgb)+m)*255+0.5

            # H = h[y][x]
            # H = H / 180 * pi 
            # r,g,b=0.0,0.0,0.0
            # if h[y][x] <=120:
            #     b,r=i[y][x]*(1-s[y][x]),i[y][x]*(1+(s[y][x]*cos(H))/cos(pi/3 - H))
            #     g = 3*i[y][x] - (b + r)
            # elif h[y][x] <= 240:
            #     r,g=i[y][x]*(1-s[y][x]),i[y][x]*(1+(s[y][x]*cos(H - 2/3*pi))/cos(pi - H))
            #     b = 3*i[y][x] - (r + g)
            # else:
            #     g,b=i[y][x]*(1-s[y][x]),i[y][x]*(1+(s[y][x]*cos(H - 4/3*pi))/cos(5/3*pi - H))
            #     r = 3*i[y][x] - (b + g)
            # im[y][x]=np.array((r,g,b))*255+0.5

            # H=h[y][x]
            # I=i[y][x]
            # S=s[y][x]
            # if(H==0):
            #     r,g,b= I + 2*I*S ,I - I*S ,I-I*S
            # elif 0 < H < 120:
            #     r,g,b=I+I*S*cos(H/pi)/cos( 60 / pi - H / pi) , I + I*S*(1-cos(H/pi)/cos( 60 / pi - H / pi)),I-I*S
            # elif H == 120 :
            #     r,g,b = I - I*S ,I + 2*I*S , I-I*S
            # elif 120 < H < 240:
            #     r,g,b = I-I*S,I+I*S*cos(H/pi-120/pi)/cos( 180 / pi - H / pi),I+I*S*(1-cos(H/pi-120/pi)/cos( 180 / pi - H / pi))
            # elif H == 240:
            #     r,g,b  = I -I*S,I-I*S,I+2*I*S
            # else:
            #     r,g,b = I + I*S*(1-(cos(H/pi - 240 /pi)/cos(300 / pi - H / pi))) , I - I*S , I + I*S*cos(H/pi - 240 /pi)/cos(300 / pi - H / pi)
            # im[y][x]=np.array((r,g,b))*255+0.5

            # H = degrees(h[y][x])
            # I = i[y][x]
            # S = s[y][x]
            # if 0 <= H <= 120 :
            #     b = I * (1 - S)
            #     r = I * (1 + (S * cos(radians(H)) / cos(radians(60) - radians(H))))
            #     g = I * 3 - (r + b)
            # elif 120 < H <= 240:
            #     H -= 120
            #     r = I * (1 - S)
            #     g = I * (1 + (S * cos(radians(H)) / cos(radians(60) - radians(H))))
            #     b = 3 * I - (r + g)
            # elif 0 < H <= 360:
            #     H -= 240
            #     g = I * (1 - S)
            #     b = I * (1 + (S * cos(radians(H)) / cos(radians(60) - radians(H))))
            #     r = I * 3 - (g + b)
            # im[y][x]=np.array((r,g,b))*255+0.5

    # return convert_array_to_img(im,"RGB")

def convert_hsv_to_rgb(h,s,v,img):
    h=h*360.0/255
    s=s/255
    v=v/255
    img = np.array(img)
    im = np.empty([len(h),len(h[0]),3],dtype=int)
    for y in range(len(h)):
        for x in range(len(h[0])):
            rgb=[0,0,0]
            hp=h[y][x]/60
            c = v[y][x]*s[y][x]
            xx = c*(1-abs(int(hp+0.5)%2-1))
            if 0 <= hp < 1:
                rgb=[c,xx,0]
            elif 1 <= hp < 2:
                rgb=[xx,c,0]
            elif 2 <= hp < 3:
                rgb=[0,c,xx]
            elif 3 <= hp < 4:
                rgb=[0,xx,c]
            elif 4 <= hp < 5:
                rgb=[xx,0,c]
            elif 5 <= hp < 6:
                rgb=[c,0,xx]
            m = v[y][x] - c
            # print(rgb,m)
            im[y][x]=(np.array(rgb)+m)*255+0.5
    return convert_array_to_img(im,"RGB")

def HSI_to_rgb(h, s, i):
    if h==0:
        r = i + 2*i*s
        g = i - i*s
        b = i - i*s
    elif 0 < h < 120 :
        b = i * (1 - s)
        r = i * (1 + (s * cos(radians(h)) / cos(radians(60) - radians(h))))
        g = i * 3 - (r + b)
    elif h == 120:
        r = i - i*s
        g = i + 2*i*s
        b = i- i*s
    elif 120 < h <= 240:
        h -= 120
        r = i * (1 - s)
        g = i * (1 + (s * cos(radians(h)) / cos(radians(60) - radians(h))))
        b = 3 * i - (r + g)
    elif h==240:
        r = i - i*s
        g = i - i*s
        b = i + 2*i*s
    else:
        h -= 240
        g = i * (1 - s)
        b = i * (1 + (s * cos(radians(h)) / cos(radians(60) - radians(h))))
        r = i * 3 - (g + b)
    # print(r,g,b)
    return [i if 0 <= i <=255 else 255 for i in [r, g, b]]


def rgb_to_hue(r, g, b):
    # 0 <= h < 360
    if(r==g==b):
        # print("h")
        return 0
    if g>=b:
        try:
            val=degrees(acos((r-g/2-b/2)/sqrt(r**2+g**2+b**2-g*b-r*g-r*b)))
        except:
            val = 0
        return val
    else:
        try:
            val = 360 - degrees(acos((r-g/2-b/2)/sqrt(r**2+g**2+b**2-g*b-r*g-r*b)))
        except:
            val = 359
        return val


def rgb_to_intensity(r, g, b):
    # 0 <= i <= 255
    return (r+g+b)/3


def rgb_to_saturity(r, g, b):
    #0.0 <= s <= 1.0
    if rgb_to_intensity(r,g,b) > 0:
        return 1 - np.min([r, g, b]) / rgb_to_intensity(r,g,b)
    else:
        return 0

def color_average_filter(im,i,color_mode):
    if color_mode == "RGB":
        r,g,b=im.split()
        r=averging_filter(r,i)
        g=averging_filter(g,i)
        b=averging_filter(b,i)
        return Image.merge("RGB",(r,g,b))
    elif color_mode == "HSI":
        imgh,imgv=im.size
        h=np.empty((imgv,imgh))
        s=np.empty((imgv,imgh))
        ii=np.empty((imgv,imgh))
        for y in range(imgv):
            for x in range(imgh):
                r,g,b = np.array(im.getpixel((x,y)))
                h[y][x] = rgb_to_hue(r,g,b)
                s[y][x] = rgb_to_saturity(r,g,b)
                ii[y][x] = rgb_to_intensity(r,g,b)
        
        # print(h,s,ii)
        # h=np.array(averging_filter(convert_array_to_img(h),i))
        # s=np.array(averging_filter(convert_array_to_img(s),i))
        ii=np.array(averging_filter(convert_array_to_img(ii),i))
        # h=np.array(h,dtype=float)
        # s=np.array(s,dtype=float)
        # ii=np.array(ii,dtype=float)
        # print(h[0][0],s[0][0],ii[0][0])
        arr=np.empty((imgv,imgh,3),dtype=int)
        for y in range(imgv):
            for x in range(imgh):
                arr[y][x]=np.array(HSI_to_rgb(h[y][x],s[y][x],ii[y][x]))
        return convert_array_to_img(arr,"RGB")
    elif color_mode=="HSV":
        h,s,v=im.convert("HSV").split()
        h=np.array(h)
        s=np.array(s)
        v=im.convert("HSV").split()[2]
        # h=averging_filter(h,i)
        # s=averging_filter(s,i)
        # v=averging_filter(v,i)
        # return Image.merge("HSV",(h,s,v))

        # h=np.array(averging_filter(h,i))
        # s=np.array(averging_filter(s,i))
        v=np.array(averging_filter(v,i))
        return convert_hsv_to_rgb(h,s,v,im)

def color_sharpening(im,i,color_mode):
    if color_mode == "RGB":
        r,g,b=im.split()
        r=sharpening_filter(r,i)
        g=sharpening_filter(g,i)
        b=sharpening_filter(b,i)
        return Image.merge("RGB",(r,g,b))
    elif color_mode == "HSI":
        imgh,imgv=im.size
        h=np.empty((imgv,imgh),dtype=float)
        s=np.empty((imgv,imgh),dtype=float)
        ii=np.empty((imgv,imgh),dtype=float)
        for y in range(imgv):
            for x in range(imgh):
                r,g,b = np.array(im.getpixel((x,y)))
                h[y][x] = rgb_to_hue(r,g,b)
                s[y][x] = rgb_to_saturity(r,g,b)
                ii[y][x] = rgb_to_intensity(r,g,b)
        
        ii=np.array(sharpening_filter(convert_array_to_img(ii),i))
        # convert_array_to_img(ii).show()
        # print(h[0][0],s[0][0],ii[0][0])
        # print(h[171][126],s[171][126],ii[171][126])
        arr=np.empty((imgv,imgh,3),dtype=int)
        for y in range(imgv):
            for x in range(imgh):
                arr[y][x]=np.array(HSI_to_rgb(h[y][x],s[y][x],ii[y][x]))
        # print(arr[171][126])
        return convert_array_to_img(arr,"RGB")
        pass
    elif color_mode=="HSV":
        h,s,v=im.convert("HSV").split()
        h=np.array(h)
        s=np.array(s)
        # h=sharpening_filter(h,i)
        # s=sharpening_filter(s,i)
        # v=sharpening_filter(v,i)
        # return Image.merge("HSV",(h,s,v))

        # h=np.array(sharpening_filter(h,i))
        # s=np.array(sharpening_filter(s,i))
        v=np.array(sharpening_filter(v,i))
        return convert_hsv_to_rgb(h,s,v,im)

def feather(im):
    new_im = im.convert("RGB")
    h,v=im.size
    H=np.array(im.convert("HSV").split()[0])/255*360
    S=np.array(im.convert("HSV").split()[0])/255*100
    for y in range(v):
        for x in range(h):
            # print(H[y][x])
            if not ( 260 < H[y][x] < 320 and 56 < x <  294 and S[y][x] >= 60 ) and not ( x<136 and y > 378 and y < 511 and x > 61 and 260 < H[y][x] < 335):
                new_im.putpixel((x,y),(0,0,0))
    return new_im
if "__main__"==__name__:
    import file_io
    im=file_io.openfile()  
    # h,v=im.size
    # H=np.array(im.convert("HSV").split()[0])/255*360
    # S=np.array(im.convert("HSV").split()[0])/255*100
    # for y in range(v):
    #     for x in range(h):
    #         # print(H[y][x])
    #         if not ( 260 < H[y][x] < 320 and 56 < x <  294 and S[y][x] >= 60 ) and not ( x<136 and y > 378 and y < 511 and x > 61 and 260 < H[y][x] < 335):
    #             im.putpixel((x,y),(0,0,0))
    # im.show()
    # new_im = im
    # h,s,v=im.convert("HSV").split()
    # h.show()
    # s.show()
    # v.show()
    # hsi_component(im,0).show()
    # new_im = im
    # hsi_component(im,1).show()
    # new_im = im
    # hsi_component(im,2).show()
    # print(np.array(im.convert("HSV")))
    # h,v = im.size
    # for i in range(v):
    #     for j in range(h):
    #         print(im.getpixel((j,i)),end="")
    #     print()
    # vim=color_average_filter(im,5,"HSV")
    # vim.show()
    # color_sharpening(vim,5,"HSV").show()
    iim=color_average_filter(im,5,"HSI")
    iim.show()
    color_sharpening(iim,5,"HSI").show()

    

