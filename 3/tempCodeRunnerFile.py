gb=[0,0,0]
            hp=h[y][x]/60
            z = 1 - abs(int(hp+0.5)%2-1)
            c = (3*i[y][x]*s[y][x]) / (1 + z)
            xx = c*z
            if img[y][x][0]==img[y][x][1]==img[y][x][2]:
                rgb=[0,0,0]
            elif 0 <= hp <= 1:
                rgb=[c,xx,0]
            elif 1 <= hp <= 2:
                rgb=[xx,c,0]
            elif 2 <= hp <= 3:
                rgb=[0,c,xx]
            elif 3 <= hp <= 4:
                rgb=[0,xx,c]
            elif 4 <= hp <= 5:
                rgb=[xx,0,c]
            elif 5 <= hp <= 6:
                rgb=[c,0,xx]
            m = i[y][x] * (1-s[y][x])
            im[y][x]=(np.array(rgb)+m)*255+0.5