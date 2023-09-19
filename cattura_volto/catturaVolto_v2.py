import face_recognition
import cv2
import numpy as np

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)
WIDTH = int(video_capture.get(3))
HEIGTH = int(video_capture.get(4))


# Initialize some variables
face_locations = []
process_this_frame = False

edge = 200

from rembg import remove


while True:

    ret, frame = video_capture.read()

    if process_this_frame:

        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        rgb_small_frame = small_frame[:, :, ::-1]
        
        face_locations = face_recognition.face_locations(rgb_small_frame)

        if (len(face_locations) > 0):
            for (top, right, bottom, left) in face_locations:
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                cH = int((bottom-top)/2)+top
                cW = int((right-left)/2)+left

                # Draw a box around the face
                #cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 1)
                #cv2.circle(frame, (cW,cH), 2, (0,0,255), 1)
                cv2.rectangle(frame, (cW-edge, cH-edge), (cW+edge, cH+edge), (0, 255, 0), 1)

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


            crop_frame = frame[yC:hC, xC:wC]
            output = remove(crop_frame)
            cv2.imshow('REC', output)

            process_this_frame = False
        


    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    k = cv2.waitKey(1)

    if k == ord('q'):
        break
    elif k == ord('p'):
        process_this_frame = True

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
