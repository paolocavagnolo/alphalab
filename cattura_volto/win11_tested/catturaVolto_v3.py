import face_recognition
import cv2
import numpy as np
from rembg import remove
import time
import os
import sys
import subprocess


ATTESA = 5      # secondi
FRAME_FERMI = 10  # frame stabili di volto
DEBUG = False

def max_number():
    or_path = os.path.dirname(os.path.realpath(__file__))
    dir_path = os.path.join(or_path,"volti")
    files = os.listdir(dir_path)

    numbers = []

    if len(files) == 0:
        return 0

    for f in files:
        if f[-4:] == '.png':
            name = f.split('.')[0]
            nn = name.split('-')
            if (len(nn)) == 2:
                numbers.append(int(nn[1]))

    return max(numbers)


# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(1)
WIDTH = int(video_capture.get(3))
HEIGTH = int(video_capture.get(4))

ret, frame = video_capture.read()
cv2.imshow('Video', frame)

# Initialize some variables
face_locations = []
process_this_frame = True

edge = 200
readyIdx = 0

# path
or_path = os.path.dirname(os.path.realpath(__file__))
black_path = os.path.join(or_path,"_showBlack.py")

if not DEBUG:
    subprocess.Popen(["py",black_path])

oFrame = frame
topOld = 0
rightOld = 0

while True:

    ret, frame = video_capture.read()

    k = cv2.waitKey(1)

    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    rgb_small_frame = small_frame[:, :, ::-1]
    
    face_locations = face_recognition.face_locations(rgb_small_frame)

    if len(face_locations) > 0:
        top, right, bottom, left = face_locations[0]

        dT = abs(top - topOld)
        dR = abs(right - rightOld)

        topOld = top
        rightOld = right

        if (dT == 0 and dR == 0):
            readyIdx = readyIdx + 1
        else:
            readyIdx = 0

        if readyIdx >= FRAME_FERMI:
            
            readyIdx = 0
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            cH = int((bottom-top)/2)+top
            cW = int((right-left)/2)+left

            if (cW-edge) < 0:
                xC = 0
            else:
                xC = cW-edge

            if (cH-edge) < 0:
                yC = 0
            else:
                yC = cH-edge

            if (cW+edge) > WIDTH:
                wC = WIDTH
            else:
                wC = cW+edge

            if (cH+edge) > HEIGTH:
                hC = HEIGTH
            else:
                hC = cH+edge

            # 1 : taglio il frame
            crop_frame = frame[yC:hC, xC:wC]

            # 2 : rimuovo lo sfondo
            output = remove(crop_frame)

            # 3 : creo il nome
            dir_path = os.path.join(or_path,"volti")
            j = max_number() + 1
            last_name_file = 'face-' + str(j) + '.png'
            name_file = os.path.join(dir_path,last_name_file)

            # 4 : salvo
            if not DEBUG:
                cv2.imwrite(str(name_file),output)
                img_path = os.path.join(or_path,"_showImage.py")
                subprocess.Popen(["py",img_path,name_file])
                time.sleep(5)
            else:
                cv2.imshow('Video2', output)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    
    if k == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
