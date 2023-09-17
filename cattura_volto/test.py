from fer import FER
import cv2
import cvzone
from cvzone.SelfiSegmentationModule import SelfiSegmentation
import numpy as np

vid = cv2.VideoCapture(0)
WIDTH = int(vid.get(3))
HEIGTH = int(vid.get(4))

detector = FER(mtcnn=True)

segmentor = SelfiSegmentation()

offset = 100

xB = 0
yB = 0
wB = 0
hB = 0

xC = 0
yC = 0
wC = 0
hC = 0

record = False

while(True):

	ret, frame = vid.read()

	dati = detector.detect_emotions(frame)

	k = cv2.waitKey(1)

	if len(dati) > 0:
		xB = dati[0]['box'][0] - offset
		yB = dati[0]['box'][1] - offset
		wB = dati[0]['box'][2] + offset*2
		hB = dati[0]['box'][3] + offset*2

		cv2.rectangle(frame,(xB,yB),(xB+wB,yB+hB),(0,255,0),1)

		if record:
			if (xB < 0):
				xC = 0
			else:
				xC = xB

			if (yB < 0):
				yC = 0
			else:
				yC = yB

			if (xB+wB) > WIDTH:
				wC = WIDTH
			else:
				wC = xB+wB

			if (yB+hB) > HEIGTH:
				hC = HEIGTH
			else:
				hC = yB+hB

			crop_image = frame[yC:hC, xC:wC]
			imgNoBg = segmentor.removeBG(crop_image, (0,0,0))
			cv2.imshow('1',imgNoBg)
			blurred_img = cv2.GaussianBlur(imgNoBg, (31, 31), 0)
			cv2.imshow('2',imgNoBg)

			maskA = cv2.inRange(imgNoBg, (0,255,0),(0,255,0))
			maskB = cv2.GaussianBlur(maskA, (31, 31), 0)
			maskC = cv2.GaussianBlur(maskB, (31, 31), 0)
			maskD = cv2.bitwise_not(maskC)
			contours, hierarchy = cv2.findContours(maskD, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
			cv2.drawContours(maskD, contours, -1, (255,255,255),5)
			cv2.imshow('3',maskD)

			output = np.where(mask==np.array([255, 255, 255]), blurred_img, imgNoBg)
			cv2.imshow('4',output)

			cv2.imwrite('/home/pol/catturaVolto/01_frame.png',frame)
			cv2.imwrite('/home/pol/catturaVolto/02_crop.png',crop_image)
			cv2.imwrite('/home/pol/catturaVolto/03_noBG.png',imgNoBg)
			#cv2.imwrite('/home/pol/catturaVolto/04_blurred.png',output)

			record = False


	if k == ord('q'):
		break
	elif k == ord('p'):
		record = True

	cv2.imshow('frame', frame)



# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()
