import time
import numpy as np
import cv2
from tkinter import *

from vlc import VLC
from darknet.darknet import detect

locs = []
FILENAME = "WatchtowerOfTurkey.MKV"
#FILENAME = "TownCentreXVID.avi"
#FILENAME = 0
SEARCHTERM = b"person"


class GUI:

    def __init__(self):
    
        self.idx = 0
        self.oldDrawnIdx = 0
        self.cap = None
        self.FILENAME = ""
        self.locs = []


        self.GUIapp = Tk()
        self.GUIapp.geometry("640x480")
        self.GUIapp.title("VLC Search by attributes")
        self.currPlayingStr = StringVar()
        label = Label( self.GUIapp, textvariable=self.currPlayingStr, relief=RAISED )
        label.pack()

        self.GUIapp.after(500, self.loopfunction)
        self.GUIapp.mainloop()
            


    def loopfunction(self):
        
        currPlaying = vlc.getCurrPlaying().decode('utf-8')[2:].strip()
        self.currPlayingStr.set(currPlaying) 


        if(self.FILENAME!=currPlaying):
            self.FILENAME = currPlaying
            print(currPlaying)
            self.cap = cv2.VideoCapture(str(currPlaying))
            FPS=self.cap.get(cv2.CAP_PROP_FPS)
            self.idx = 0
            self.oldDrawnIdx = 0
            

        start = time.time()
        ret, frame = self.cap.read()
        #print("Ret: ", ret)
        if( not ret ):
            self.GUIapp.after(1, self.loopfunction)
            return
        r = detect(np.array(frame))
        #print("Time for detection: ", 1000*(time.time()-start))
        for i in r:
            if i[0]==SEARCHTERM:
                self.locs.append(self.idx)

        #print(self.locs)
        print(self.idx)

        self.idx += 1
        # Add buttons
        for i in self.locs[self.oldDrawnIdx:]:
            Button(self.GUIapp, text=str(i), command=lambda j=i: vlc.seek(int(i/FPS))).pack()
        self.oldDrawnIdx = len(self.locs)
        self.GUIapp.after(1, self.loopfunction)


vlc = VLC()
time.sleep(1)
vlc.add(FILENAME)
time.sleep(1)
vlc.play()
time.sleep(1)

mainApp = GUI()


