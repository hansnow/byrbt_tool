#!/usr/bin/env python3
# -*- coding:utf8 -*-
from tkinter import *
from PIL import Image, ImageTk
from bs4 import BeautifulSoup
import requests as rq
import json

IMAGE_HASH = ''
COOKIES = {}
def login(username,password,hashcode,keeplogin):
    global IMAGE_HASH
    global COOKIES
    '''
    The login form-data are here:

    username:hansnow
    password:***
    imagestring:72b6c3
    imagehash:70534bea566661cdc83a86785ba48090
    '''
    payload = {"username": username,
    "password": password,
    "imagestring": hashcode,
    "imagehash": IMAGE_HASH}

    r = rq.post('http://bt.byr.cn/takelogin.php',data=payload,allow_redirects=False)
    if not ('图片代码无效' in r.text):
        COOKIES = rq.utils.dict_from_cookiejar(r.cookies)
        if keeplogin.get():
            with open('cookies.txt','w') as f:
                f.write(json.dumps(COOKIES))
        
        print('login success')
    else:
        print('login failed')
        



def refresh():
    global IMAGE_HASH
    html = rq.get('http://bt.byr.cn/login.php').text
    soup = BeautifulSoup(html)
    IMAGE_HASH = soup.select('input[name="imagehash"]')[0]['value']
    with  open('image.png','wb') as f:
        r = rq.get('http://bt.byr.cn/image.php?action=regimage&imagehash='+IMAGE_HASH)
        # f.write(io.StringIO(r.content))
        f.write(r.content)
        print(IMAGE_HASH)




    
class makeLoginPanel:

    def __init__(self,master):
        self.master = master
        refresh()
        frame = Frame(master)
        frame.pack()
        
        # variable to store checkbox value
        self.keeplogin = IntVar()

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
        self.UserEntry.grid(row=0,column=1,columnspan=2)
        self.PassEntry.grid(row=1,column=1,columnspan=2)
        self.HashEntry.grid(row=2,column=1,columnspan=2)

        self.ImgBox = ImageTk.PhotoImage(file='image.png')
        self.ImgLabel = Label(frame, image=self.ImgBox)
        self.ImgLabel.image = self.ImgBox
        self.ImgLabel.grid(row=3,column=0,columnspan=2)
        
        self.RefreshBtn = Button(frame, text="Refresh",command=self.refresh)
        self.RefreshBtn.grid(row=3,column=2,sticky=W+E)

        self.KeepLoginChkBtn = Checkbutton(frame,text='KeepLogin',variable=self.keeplogin)
        self.KeepLoginChkBtn.grid(row=4,column=0)

        self.LoginBtn = Button(frame,text='Login',command=self.login)
        self.LoginBtn.grid(row=4,column=1,columnspan=2,sticky=W+E)

    def refresh(self):
        global IMAGE_HASH
        html = rq.get('http://bt.byr.cn/login.php').text
        soup = BeautifulSoup(html)
        IMAGE_HASH = soup.select('input[name="imagehash"]')[0]['value']
        with  open('image.png','wb') as f:
            r = rq.get('http://bt.byr.cn/image.php?action=regimage&imagehash='+IMAGE_HASH)
            # f.write(io.StringIO(r.content))
            f.write(r.content)
            print(IMAGE_HASH)
        self.ImgBox = ImageTk.PhotoImage(file='image.png')
        self.ImgLabel.config(image=self.ImgBox)
    def login(self):
        global IMAGE_HASH
        global COOKIES
        username = self.UserEntry.get()
        password = self.PassEntry.get()
        hashcode = self.HashEntry.get()
        # login(username,password,hashcode,self.keeplogin)
        # # login('hansnow','woshixh4291221',hashcode)
        '''
        The login form-data are here:

        username:hansnow
        password:***
        imagestring:72b6c3
        imagehash:70534bea566661cdc83a86785ba48090
        '''
        payload = {"username": username,
        "password": password,
        "imagestring": hashcode,
        "imagehash": IMAGE_HASH}

        r = rq.post('http://bt.byr.cn/takelogin.php',data=payload,allow_redirects=False)
        if not ('图片代码无效' in r.text):
            COOKIES = rq.utils.dict_from_cookiejar(r.cookies)
            if self.keeplogin.get():
                with open('cookies.txt','w') as f:
                    f.write(json.dumps(COOKIES))
            print(r.text)
            print('login success')
            self.master.destroy()


        else:
            print(r.text)
            print('login failed')

class makeMainPanel:
    def __init__(self,master):
        UserInfo = self.getUserInfo()
        frame = Frame(master)
        frame.pack()
        # Info Label
        self.usernameLabel = Label(frame,text="Username:")
        self.usernameLabel.grid(row=0,column=0,sticky=W)

        self.rankLabel = Label(frame,text="Rank:")
        self.rankLabel.grid(row=1,column=0,sticky=W)

        self.bonusLabel = Label(frame,text="Bonus:")
        self.bonusLabel.grid(row=2,column=0,sticky=W)

        self.ratioLabel = Label(frame,text="Ratio:")
        self.ratioLabel.grid(row=3,column=0,sticky=W)

        self.uploadLabel = Label(frame,text="Uploaded:")
        self.uploadLabel.grid(row=4,column=0,sticky=W)

        self.downloadLabel = Label(frame,text="Downloaded:")
        self.downloadLabel.grid(row=5,column=0,sticky=W)

        self.inviteLabel = Label(frame,text="Invite:")
        self.inviteLabel.grid(row=6,column=0,sticky=W)

        # Real info
        self.UsernameLabel = Label(frame,text=UserInfo['username'])
        self.UsernameLabel.grid(row=0,column=1,sticky=E)

        self.RankLabel = Label(frame,text=UserInfo['rank'])
        self.RankLabel.grid(row=1,column=1,sticky=E)

        self.BonusLabel = Label(frame,text=UserInfo['bonus'])
        self.BonusLabel.grid(row=2,column=1,sticky=E)

        self.RatioLabel = Label(frame,text=UserInfo['ratio'])
        self.RatioLabel.grid(row=3,column=1,sticky=E)

        self.UploadLabel = Label(frame,text=UserInfo['upload'])
        self.UploadLabel.grid(row=4,column=1,sticky=E)

        self.DownloadLabel = Label(frame,text=UserInfo['download'])
        self.DownloadLabel.grid(row=5,column=1,sticky=E)

        self.InviteLabel = Label(frame,text=UserInfo['invite'])
        self.InviteLabel.grid(row=6,column=1,sticky=E)


    def getUserInfo(self):
        global COOKIES
        html = rq.get('http://bt.byr.cn/index.php',cookies=COOKIES).text
        soup = BeautifulSoup(html)
        username =  soup.select('#info_block a[href^="userdetails"]')[0].get_text()
        rank = soup.select('#info_block a[href^="userdetails"]')[0]['class'][0].split('_')[0]
        bonus = soup.select('#info_block a[href^="mybonus"]')[0].next_sibling[3:-1]
        invite = soup.select('#info_block a[href^="invite"]')[0].next_sibling[3:]
        ratio = soup.select('#info_block font.color_ratio')[0].next_sibling.strip()
        upload = soup.select('#info_block font.color_uploaded')[0].next_sibling.strip()
        download = soup.select('#info_block font.color_downloaded')[0].next_sibling.strip()

        return {
        'username': username,
        'rank': rank,
        'bonus': bonus,
        'invite': invite,
        'ratio': ratio,
        'upload': upload,
        'download': download
        }




root = Tk()
root.title('BYRBT TOOL')
# makeMainPanel(root)
LoginPanel = Toplevel()
LoginPanel.title('LoginPanel')
makeLoginPanel(LoginPanel)
root.withdraw()
def callback(event):
    print('ready to deiconify')
    root.deiconify()
    print('root has deiconifyed')
    makeMainPanel(root)
    LoginPanel.unbind("<Destroy>", funcid)
funcid = LoginPanel.bind("<Destroy>", callback)

root.mainloop()



