from tkinter import *
import pystray
from PIL import Image, ImageDraw
import psutil
import time
import ctypes #,win32con
import win32.lib.win32con as win32con
import cv2
import requests
import threading
from datetime import datetime
import os
ctypes.windll.shcore.SetProcessDpiAwareness(1)

w = 1920
h = 1080
x,y0=1500,100
# global stop_clock 
stop_clock = False
dy=50
thickness = 2
clock_is_set = True
#clock colour
r=255
g=0
b=0

def create_image(width, height, color1, color2):
    image = Image.new('RGB', (width, height), color1)
    dc = ImageDraw.Draw(image)
    dc.rectangle(
        (width // 2, 0, width, height // 2),
        fill=color2)
    dc.rectangle(
        (0, height // 2, width // 2, height),
        fill=color2)

    return image


def download_random_img():
    global w,h
    path =  f'https://unsplash.it/{w}/{h}/?random'
    # mainframe.pack_forget()
    # loading.pack(fill=tk.BOTH,expand=True)
    # pb.start()
    if os.path.isdir('data'):
        pass
    else:
        os.makedirs('data')
    try:
        r = requests.get(path)
        open('data/img.png', 'wb').write(r.content)
        abspath = os.path.abspath('data/img.png')
        ctypes.windll.user32.SystemParametersInfoW(20, 0,abspath, 0)
        # root.title('Personalisation Tool')
    except:
        pass
    #     root.title('Personalisation Tool:No internet')
    # pb.stop()
    # loading.pack_forget()
    # mainframe.pack(fill=tk.BOTH,expand=True)

def getWallpaper():
    ubuf = ctypes.create_unicode_buffer(512)
    ctypes.windll.user32.SystemParametersInfoW(win32con.SPI_GETDESKWALLPAPER,len(ubuf),ubuf,0)
    return ubuf.value

try:
    with open('app_config.txt','rb') as f:
        l = f.readlines()
    for i in l:
        i = i.decode()
        if i[0]=='#':
            pass
        elif i[0]=='x':
            x = int(i[2:])
        elif i[0]=='y':
            y0 = int(i[2:])
        elif i[0]=='c' and i[1]=='r':
            r = int(i[3:])
            if 0<=r<=255:
                pass
            else:
                r = 255
        elif i[0]=='c' and i[1]=='g':
            g = int(i[3:])
            if 0<=g<=255:
                pass
            else:
                g = 255
        elif i[0]=='c' and i[1]=='b':
            b = int(i[3:])
            if 0<=b<=255:
                pass
            else:
                b = 255
except:
    pass

def clock():
    if os.path.isdir('data') and os.path.isfile('data/img.png'):
        org_wall_abs_path = getWallpaper()
    else:
        # download_random_img()
        os.mkdir('data')
        org_wall_abs_path = getWallpaper()
        cwd = os.getcwd()
        os.system(f'copy {org_wall_abs_path} {cwd}\\data\\img.png')
        abspath = os.path.abspath('data/img.png')
        ctypes.windll.user32.SystemParametersInfoW(20, 0,abspath, 0)
        org_wall_abs_path = getWallpaper()
    main_wallpaper = cv2.imread(org_wall_abs_path)
    while True:
        if stop_clock:
            break
        wallpaper_with_clk = cv2.imread('data/img.png')
        battery = psutil.sensors_battery()
        now = datetime.now()
        current_time = now.strftime("%I:%M")
        for  i , line in  enumerate (current_time.split ( ':' )):
            y = y0 + i*dy
            wallpaper_with_clk = cv2.putText(wallpaper_with_clk, line+'|',(x, y),cv2.FONT_HERSHEY_SIMPLEX,2, (b,g,r), thickness, cv2.LINE_AA)
        wallpaper_with_clk = cv2.putText(wallpaper_with_clk, str(datetime.today().strftime('%A')),(x+100, y-70),cv2.FONT_HERSHEY_SIMPLEX,1,(b,g,r), thickness, cv2.LINE_AA)
        wallpaper_with_clk = cv2.putText(wallpaper_with_clk, str(battery.percent)+"%",(x+100, y-35),cv2.FONT_HERSHEY_SIMPLEX,1, (b,g,r), thickness, cv2.LINE_AA)
        cv2.imwrite('data/img_clk.png',wallpaper_with_clk)
        path = os.path.abspath('data/img_clk.png')
        ctypes.windll.user32.SystemParametersInfoW(20, 0,str(path), 0)
        time.sleep(5)
        var=2

def set_clocl():
    if not stop_clock:
        global  t
        t = threading.Thread(target=clock,daemon=True)
        t.start()

def remove_clock():
    abspath = os.path.abspath('data/img.png')
    ctypes.windll.user32.SystemParametersInfoW(20, 0,abspath, 0)

def about_fun():
    global root
    root = Tk()
    root.title("About")
    root.resizable(0,0)
    # root.attributes('-alpha',0.9)
    root.config(bg='#202020')
    about = '''
    -works well for display size w = 1920 h = 1080
    -Clock refresh in every 5 seconds
    -to change clock position create a app_config.txt
        in same directory as of python file inside app_config file write these three lines
    -#default position
    -x=1500
    -y=800
    -x and y are coordinates of display
    -to change clock colour
    -write in app_config file
    -cr=255
    -cg=255
    -cb=255
    cr,cg,cb holds colour value 0-255
    -Refresh wallpaper dependent on internet speed
    -Let me know if you encountered any bug\n
    -source code avaliable at\n
    -https://github.com/Lakshit-Karsoliya\n
    '''
    l = Label(root,text=about,fg='#ffffff',bg='#202020',font=('Helvetica 12'), justify= LEFT)
    l.pack(padx=20,pady=20,anchor="w")
    root.mainloop()

def function_handler(icon,item):
    global stop_clock , clock_is_set , root
    if str(item)=='About':
        about_fun()
    elif str(item)=='clock_stop':
        pass
    elif str(item)=='Random Wallpaper':
        download_random_img()
    elif str(item)=='Start Clock':
        stop_clock = False
        # clock_is_set = True
        if not clock_is_set:
            set_clocl()
    elif str(item)=='Stop Clock':
        stop_clock = True
        clock_is_set = False
        remove_clock()
    elif str(item)=='exit':
        remove_clock()
        try:
            root.destroy()
        except:#root already destroyed
            pass
        icon.stop()


image = create_image(64,64,'black','white')

icon = pystray.Icon('AppTitle',image,menu = pystray.Menu(
    pystray.MenuItem('Random Wallpaper',function_handler),
    pystray.MenuItem('Start Clock',function_handler),
    pystray.MenuItem('Stop Clock',function_handler),
    pystray.MenuItem('About',function_handler),
    pystray.MenuItem('exit',function_handler),
))

set_clocl()
icon.run()
