import cv2
import os
import time
import numpy as np
from goprocam import GoProCamera
from goprocam import constants

#gopro1 = GoProCamera.GoPro(constants.gpcontrol)
#gopro1.mode(constants.Mode.PhotoMode)

### Helper functions
def ResizeWithAspectRatio(image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    return cv2.resize(image, dim, interpolation=inter)
# Ref
# https://stackoverflow.com/questions/35180764/opencv-python-image-too-big-to-display


cam = cv2.VideoCapture(0)

# cv2.namedWindow("test")
cv2.namedWindow("test_flipped")

img_counter = 0

while True:
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
        break
    frame_flipped = cv2.flip(frame, 1)
    # cv2.imshow("test", frame) 
    cv2.imshow("test_flipped", frame_flipped)

    k = cv2.waitKey(1)
    if k%256 == 27:
        ### ESC pressed
        print("Escape hit, removing images taken")
        ### Remove all saved images upon exiting
        for img in os.listdir('./'):
            if img.endswith('.png'):
                os.remove(img) 
        print("Images removed, closing...")
        break
    elif k%256 == 32:
        ### SPACE pressed
        img_name = "opencv_frame_{}.png".format(img_counter)
        cv2.imwrite(img_name, frame)
        # my_img_1 = np.zeros((512, 512, 1), dtype = "uint8")   # Black image placeholder
        my_img_1 = cv2.imread(img_name)
        my_img_1  = ResizeWithAspectRatio(my_img_1 , width=400) # Resize to window size

        ### Show images in multiple new small windows & populate the screen 
        window_name = "image_{}".format(img_counter)
        cv2.namedWindow(window_name)
        # cv2.resizeWindow(window_name, 300, 400)
        cv2.moveWindow(window_name, (img_counter%4)*400,(img_counter%4)*225)
        cv2.imshow(window_name, my_img_1)

        ### Show go pro pic
        # pic1 = gopro1.downloadLastMedia(gopro1.take_photo())

        ### Show image in the same window
        # cv2.imshow("test_flipped", my_img_1)
        time.sleep(2)
        cv2.imshow("test_flipped", frame_flipped)
        print("{} written!".format(img_name))
        img_counter += 1

cam.release()

cv2.destroyAllWindows()
