import cv2
import time
import numpy as np
from goprocam import GoProCamera
from goprocam import constants

#gopro1 = GoProCamera.GoPro(constants.gpcontrol)
#gopro1.mode(constants.Mode.PhotoMode)

cam = cv2.VideoCapture(0)

cv2.namedWindow("test")

img_counter = 0

while True:
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
        break
    cv2.imshow("test", frame)

    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
        # SPACE pressed
        img_name = "opencv_frame_{}.png".format(img_counter)
        cv2.imwrite(img_name, frame)
        my_img_1 = np.zeros((512, 512, 1), dtype = "uint8")
        cv2.imshow('test', my_img_1)
        #pic1 = gopro1.downloadLastMedia(gopro1.take_photo())
        time.sleep(2)
        cv2.imshow("test", frame)
        print("{} written!".format(img_name))
        img_counter += 1

cam.release()

cv2.destroyAllWindows()