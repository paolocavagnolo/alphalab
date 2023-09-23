import face_recognition
import cv2
import numpy as np
from rembg import remove
import time
import os
import sys
import subprocess


ATTESA = 5      # secondi
FRAME_FERMI_SUM = 3000000  # frame stabili di volto
FRAME_FERMI = 2
DEBUG = False
BIG_HEIGTH = 1.5
BIG_WIDTH = 1.2

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
video_capture = cv2.VideoCapture(0)
WIDTH = int(video_capture.get(3))
HEIGTH = int(video_capture.get(4))

ret, frame = video_capture.read()
cv2.imshow('Video', frame)

# Initialize some variables
face_locations = []
process_this_frame = True

readyIdx = 0

# path
or_path = os.path.dirname(os.path.realpath(__file__))
black_path = os.path.join(or_path,"_showBlack.py")

if not DEBUG:
    subprocess.Popen(["python3",black_path])

oFrame = frame
tO = 0
rO = 0
bO = 0
lO = 0

tTime = 0

while True:

    # prendo il frame
    ret, frame = video_capture.read()

    k = cv2.waitKey(1)

    # cerco il volto
    rgb_frame = frame[:, :, ::-1]
    
    face_locations = face_recognition.face_locations(rgb_frame)

    if len(face_locations) > 0 and (time.time() - tTime > 5):
        top, right, bottom, left = face_locations[0]

        width = right - left
        heigth = bottom - top

        centerV = int(heigth / 2) + top
        centerH = int(width / 2) + left

        n_top = centerV - int(heigth/2*BIG_HEIGTH*BIG_HEIGTH)
        n_bottom = centerV + int(heigth/2*BIG_HEIGTH)
        n_left = centerH - int(width/2*BIG_WIDTH)
        n_right = centerH + int(width/2*BIG_WIDTH)

        if n_top < 0: n_top = 0
        if n_bottom > HEIGTH: n_bottom = HEIGTH
        if n_left < 0: n_left = 0
        if n_right > WIDTH: n_right = WIDTH

        # taglio il frame sul volto
        if DEBUG:
            #cv2.rectangle(frame,(xC,yC),(wC,hC),(255,0,0),1)
            cv2.rectangle(frame,(left,top),(right,bottom),(255,0,0),1)
            cv2.rectangle(frame,(n_left,n_top),(n_right,n_bottom),(0,255,0),1)

        else:
            if tO == n_top and rO == n_right and lO == n_left and bO == n_bottom:
                readyIdx = readyIdx + 1
            else:
                readyIdx = 0

            if readyIdx >= FRAME_FERMI:
                readyIdx = 0
                crop_frame = oFrame[n_top:n_bottom, n_left:n_right]
                # rimuovo lo sfondo
                output = remove(crop_frame)

                # creo il nome
                dir_path = os.path.join(or_path,"volti")
                j = max_number() + 1
                last_name_file = 'face-' + str(j) + '.png'
                name_file = os.path.join(dir_path,last_name_file)

                tTime = time.time()

                # salvo

                cv2.imwrite(str(name_file),output)
                img_path = os.path.join(or_path,"_showImage.py")
                subprocess.Popen(["python3",img_path,name_file])

            oFrame = frame.copy();
            tO = n_top
            bO = n_bottom
            rO = n_right
            lO = n_left


            

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    
    if k == ord('q'):
        break

    

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
