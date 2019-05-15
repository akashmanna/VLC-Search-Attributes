import time
import os
import numpy as np
import cv2
from tkinter import *

from vlc import VLC
from darknet.darknet import detect
from tracker import tracker

class GUI:

    def __init__(self):
    
        self.idx = 0
        self.oldDrawnIdx = 0
        self.cap = None
        self.FPS = 0
        self.FILENAME = ""
        self.SEARCHTERM = b''
        self.locs = []


        self.vlc = VLC()
        #time.sleep(1)

        self.GUIapp = Tk()
        self.GUIapp.geometry("640x480")
        self.GUIapp.title("VLC Search by attributes")
        self.currPlayingStr = StringVar()
        label = Label( self.GUIapp, textvariable=self.currPlayingStr, relief=RAISED )
        label.pack()

        self.textBox=Text(self.GUIapp, height=2, width=10)
        self.textBox.pack()

        Button(self.GUIapp, text="SEARCH", command=self.searchInit).pack()

        self.GUIapp.after(500, self.loopfunction)
        self.GUIapp.mainloop()

    def searchInit(self):
        print("Search INIT")
        self.SEARCHTERM=self.textBox.get("1.0","end-1c").encode()
            
    
    def loopfunction(self):
        currPlaying = self.vlc.getCurrPlaying().decode('utf-8')[2:].strip()
        if(self.FILENAME!=currPlaying):
            self.FILENAME = currPlaying
            print(currPlaying)
            if not os.path.isfile(currPlaying):
                #time.sleep(1)
                self.GUIapp.after(1, self.loopfunction)
                return

            self.currPlayingStr.set(currPlaying) 
            self.cap = cv2.VideoCapture(str(currPlaying))
            self.FPS=self.cap.get(cv2.CAP_PROP_FPS)
            self.idx = 0
            self.oldDrawnIdx = 0

        if not os.path.isfile(currPlaying):
            #time.sleep(1)
            self.GUIapp.after(1, self.loopfunction)
            return 

        start = time.time()
        ret, frame = self.cap.read()
        if( not ret ):
            self.GUIapp.after(1, self.loopfunction)
            return 
        r = detect(np.array(frame))
        #print("Time for detection: ", 1000*(time.time()-start))
        for i in r:
            if i[0]==self.SEARCHTERM:
                self.locs.append(self.idx)

        print(self.idx)

        self.idx += 1
        # Add buttons
        for i in self.locs[self.oldDrawnIdx:]:
            Button(self.GUIapp, text=str(i), command=lambda j=i: self.vlc.seek(int(i/self.FPS))).pack()
        self.oldDrawnIdx = len(self.locs)
        self.GUIapp.after(1, self.loopfunction)
