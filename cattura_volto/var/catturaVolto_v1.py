from fer import FER
import cv2
import cvzone
from cvzone.SelfiSegmentationModule import SelfiSegmentation
import numpy as np
import torch
from torchvision import transforms
import time

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

# Desired Image Dimensions.
IMG_WIDTH = 480
IMG_HEIGHT = 640

method = 'midas'
model_names = {"deeplabv3": ['pytorch/vision:v0.6.0', 'deeplabv3_resnet101'],"midas": ["intel-isl/MiDaS", "MiDaS"]}

model = torch.hub.load(model_names[method][0],model_names[method][1], pretrained=True)

def blur(img):
    return cv2.GaussianBlur(img, (25, 25), 0)


def to_tensor(img):
    # Preprocess the image to meet the input requirement of the networks.
    preprocess = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    input_tensor = preprocess(img)
    input_batch = input_tensor.unsqueeze(0)  # create a mini-batch as expected by the model.
    return input_batch


def get_object_mask(img, model, method):
    if torch.cuda.is_available():
        img = img.to('cuda:0')
        model = model.to('cuda:0')
    if method == "deeplabv3":
        with torch.no_grad():
            output = model(img)['out'][0]
            output = output.argmax(0)
        mask = output.cpu().numpy()
        # Isolate the person class.
        mask = (mask == 15) * 255
        return np.array(mask, dtype=np.uint8, copy=True)
    elif method == "midas":
        with torch.no_grad():
            output = model(img)
            output = torch.nn.functional.interpolate(
                output.unsqueeze(1),
                size=[IMG_WIDTH, IMG_HEIGHT],
                mode="bicubic",
                align_corners=False,
            ).squeeze()

        mask = output.cpu().numpy()
        # Isolate the objects nearest to camera.
        mask = ((mask / np.max(mask)) > 0.6) * 255
        return np.array(mask, dtype=np.uint8, copy=True)

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
				xC = xB+1

			if (yB < 0):
				yC = 0
			else:
				yC = yB+1

			if (xB+wB) > WIDTH:
				wC = WIDTH
			else:
				wC = xB+wB-1

			if (yB+hB) > HEIGTH:
				hC = HEIGTH
			else:
				hC = yB+hB-1


			#try new method

			img = to_tensor(frame)
			object_mask = get_object_mask(img, model, method)
			image_with_mask = cv2.bitwise_and(frame, frame, mask=object_mask)

			crop_image = image_with_mask[yC:hC, xC:wC]

			cv2.imwrite('/home/pol/Documents/catturaVolto/01_frame.png',frame)
			cv2.imwrite('/home/pol/Documents/catturaVolto/02_crop.png',crop_image)

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
