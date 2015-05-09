#!/usr/bin/env python3
# -*- coding:utf8 -*-
from tkinter import *
from PIL import Image, ImageTk
from bs4 import BeautifulSoup
import requests as rq
import time

IMAGE_HASH = ''
COOKIE = ''
def login(username,password,hashcode):
    # print('login with:' + username + ':' + password)
    '''
    username:hansnow
    password:***
    imagestring:72b6c3
    imagehash:70534bea566661cdc83a86785ba48090
    '''
    payload = {"username": username,
    "password": password,
    "imagestring": hashcode,
    "imagehash": IMAGE_HASH}

    r = rq.post('http://bt.byr.cn/takelogin.php',params=payload)
    # soup = BeautifulSoup(r.text)
    # name = soup.select('#info_block a[href^="userdetails"]')[0].get_text()
    # print(name)
    print(r.text)
    print(r.history)



def refresh():
    html = rq.get('http://bt.byr.cn/login.php').text
    soup = BeautifulSoup(html)
    IMAGE_HASH = soup.select('input[name="imagehash"]')[0]['value']
    with  open('image.png','wb') as f:
        r = rq.get('http://bt.byr.cn/image.php?action=regimage&imagehash='+IMAGE_HASH)
        # f.write(io.StringIO(r.content))
        f.write(r.content)
        print(IMAGE_HASH)




    
class App:

    def __init__(self,master):
        refresh()
        frame = Frame(master)
        frame.pack()
        # frame.title = 'BYRBT TOOL'
        self.UserLabel = Label(frame,
            text="Username")
        self.PassLabel = Label(frame,
            text="Password")
        self.HashLabel = Label(frame,
            text="HashCode")
        self.UserLabel.grid(row=0,column=0,sticky=W)
        self.PassLabel.grid(row=1,column=0,sticky=W)
        self.HashLabel.grid(row=2,column=0,sticky=W)

        self.UserEntry = Entry(frame)
        self.PassEntry = Entry(frame,show='*')
        self.HashEntry = Entry(frame)
        self.UserEntry.grid(row=0,column=1)
        self.PassEntry.grid(row=1,column=1)
        self.HashEntry.grid(row=2,column=1)

        self.ImgBox = ImageTk.PhotoImage(file='image.png')
        self.ImgLabel = Label(frame, image=self.ImgBox)
        self.ImgLabel.image = self.ImgBox
        self.ImgLabel.grid(row=3,column=0,columnspan=2)
        
        self.RefreshBtn = Button(frame, text="Refresh",command=self.refresh)
        self.RefreshBtn.grid(row=4,column=0)

        self.LoginBtn = Button(frame,text='Login',command=self.login)
        self.LoginBtn.grid(row=4,column=1,sticky=W+E)

    def refresh(self):
        refresh()
        self.ImgBox = ImageTk.PhotoImage(file='image.png')
        self.ImgLabel.config(image=self.ImgBox)
    def login(self):
        username = self.UserEntry.get()
        password = self.PassEntry.get()
        hashcode = self.HashEntry.get()
        login(username,password,hashcode)



root = Tk()
root.title('BYRBT TOOL')
app = App(root)

root.mainloop()



