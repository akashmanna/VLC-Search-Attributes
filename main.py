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


vlc = VLC()
time.sleep(1)
vlc.add(FILENAME)
time.sleep(1)
vlc.play()
time.sleep(1)




cap = None
FILENAME = "" 
idx = 0
oldDrawnIdx = 0

def loop():
    global idx
    global oldDrawnIdx
    global cap
    global FILENAME
    
    currPlaying = vlc.getCurrPlaying().decode('utf-8')[2:].strip()
    currPlayingStr.set(currPlaying) 


    if(FILENAME!=currPlaying):
        FILENAME = currPlaying
        print(currPlaying)
        cap = cv2.VideoCapture(str(currPlaying))
        FPS=cap.get(cv2.CAP_PROP_FPS)
        idx = 0
        oldDrawnIdx = 0
        

    start = time.time()
    ret, frame = cap.read()
    #print("Ret: ", ret)
    if( not ret ):
        main.after(1, loop)
        return
    r = detect(np.array(frame))
    #print("Time for detection: ", 1000*(time.time()-start))
    for i in r:
        if i[0]==SEARCHTERM:
            locs.append(idx)

    #print(locs)
    print(idx)

    idx += 1
    # Add buttons
    for i in locs[oldDrawnIdx:]:
        Button(main, text=str(i), command=lambda j=i: vlc.seek(int(i/FPS))).pack()
    oldDrawnIdx = len(locs)
    main.after(1, loop)


main = Tk()
main.geometry("640x480")
main.title("VLC Search by attributes")
currPlayingStr = StringVar()
label = Label( main, textvariable=currPlayingStr, relief=RAISED )
label.pack()

main.after(500, loop)
main.mainloop()


print(locs)

vlc.seek(int(locs[0]/FPS))
time.sleep(1)
time.sleep(1)
