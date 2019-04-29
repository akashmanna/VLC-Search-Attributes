import time
import numpy as np
import cv2
from tkinter import *

from vlc import VLC
from darknet.darknet import detect

locs = [1]
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




cap = cv2.VideoCapture(FILENAME)
FPS=cap.get(cv2.CAP_PROP_FPS)
idx = 0
oldDrawnIdx = 0

print(FPS)
def add_buttons():
    global idx
    global oldDrawnIdx
    start = time.time()
    ret, frame = cap.read()
    r = detect(np.array(frame))
    #print("Time for detection: ", 1000*(time.time()-start))
    for i in r:
        if i[0]==SEARCHTERM:
            locs.append(idx)

    #print(locs)

    idx += 1
    # Add buttons
    for i in locs[oldDrawnIdx:]:
        Button(main, text=str(i), command=lambda j=i: vlc.seek(int(i/FPS))).pack()
    oldDrawnIdx = len(locs)
    main.after(1, add_buttons)

    # search for "Add Buttons" Button object and change text and function 
    #for child in main.winfo_children():
    #    if child.cget('text') == 'Add Buttons':
    #         child.config(text='Delete all buttons')
    #         child.config(command=delete_buttons)

main = Tk()
main.title("VLC Search by attributes")
Button(main,text='Add Buttons', command=add_buttons).pack()
main.after(1000, add_buttons)
main.mainloop()


print(locs)

vlc.seek(int(locs[0]/FPS))
time.sleep(1)
time.sleep(1)
