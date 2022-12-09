import cv2
import os
import time
import numpy as np
# from goprocam import GoProCamera
# from goprocam import constants

import PIL
from PIL import Image, ImageOps, ImageDraw, ImageFont

#gopro1 = GoProCamera.GoPro(constants.gpcontrol)
#gopro1.mode(constants.Mode.PhotoMode)

### Global variables for photostrip
strip_rows = 4
strip_columns = 1
strip_width = 300
strip_height = 750

column_grayscale = (0, 1)
strip = Image.new('RGB', (strip_width, strip_height), (255,255,255))
row_gutter = 15
column_gutter = 10
target_height = int((strip_height - ((strip_rows + 1) * row_gutter)) / strip_rows)
target_width = int((strip_width-20 - ((strip_columns - 1) * column_gutter)) / strip_columns)

### Helper functionss
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


### Style
FONT = cv2.FONT_HERSHEY_DUPLEX


### Main Program
cam = cv2.VideoCapture(0)

def get_image():
  retval, image = cam.read()
  image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
  image = Image.fromarray(image)
  return image

# cv2.namedWindow("test")
cv2.namedWindow("test_flipped")

img_counter = 0
time_stamp = None
img_saved = False
img_name = ""

while True:
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
        break
    frame_flipped = cv2.flip(frame, 1)
    frame_no_text = frame_flipped
    if not time_stamp:
        cv2.putText(frame_flipped,'To take a selfie with the birds, press spacebar!',(10,100), FONT, 1.5,(255,255,255),2,cv2.LINE_AA)
        cv2.imshow("test_flipped", frame_flipped)
    else: 
        if time.time() - time_stamp < 1:
            cv2.putText(frame_flipped,'3',(500,300), FONT, 10,(233,255,255),5,cv2.LINE_AA)
            cv2.imshow("test_flipped", frame_flipped)   # 3
        elif 1 <= time.time() - time_stamp < 2:
            cv2.putText(frame_flipped,'2',(500,300), FONT, 10,(233,255,255),5,cv2.LINE_AA)
            cv2.imshow("test_flipped", frame_flipped)   # 2
        elif 2 <= time.time() - time_stamp < 3:
            cv2.putText(frame_flipped,'1',(500,300), FONT, 10,(233,255,255),5,cv2.LINE_AA)
            cv2.imshow("test_flipped", frame_flipped)   # 1
        else:
            if img_saved:
                # # ### Load images & show images in multiple new small windows to populate the screen 
                for row in range(strip_rows):
                    # PIL 
                    image = get_image()
                    if row == 3:
                        image = Image.open('assets/slogan.jpeg')
                    
                    # Scale/crop the image to fit our desired width/height.
                    image = ImageOps.fit(image, (target_width, target_height))
                    
                    y = (row * target_height) + ((row+1) * row_gutter)
                    
                    x = 10
                    strip.paste(image, (x,y))

                # Show the strip to the user, this is where you'd put print/save code as well.
                # Add Text to an image
                I1 = ImageDraw.Draw(image)
                font = ImageFont.truetype("Chalkduster.ttf", 1)
                I1.text((242, 739), "12.9.2022", fill=(255, 0, 0))
                strip.show()
                img_saved = False
                # break

            time_stamp = None
            break

    k = cv2.waitKey(1)
    if k%256 == 27:
        ### ESC pressed
        print("Escape hit, removing images taken")

        break
    elif k%256 == 32: 
        ### SPACE pressed --> birds start taking pic, assign time stamp & start count down

        if not time_stamp:
            ### Saving time stamp
            time_stamp = time.time()
            ### Saving the image
            img_name = "opencv_frame_{}.jpeg".format(img_counter)
            cv2.imwrite(img_name, frame_flipped)
            # my_img_1 = np.zeros((512, 512, 1), dtype = "uint8")   # Black image placeholder

            ### Save go pro pic
            # pic1 = gopro1.downloadLastMedia(gopro1.take_photo())

            img_saved = True
            print("{} written!".format(img_name))
            img_counter += 1
        else:   
            ### If time_stamp is on, refresh time_stamp
            time_stamp = time.time()
    
cam.release()

### Remove all saved images upon exiting
for img in os.listdir('./'):
            if img.endswith('.png'):
                os.remove(img) 
print("Images removed, closing...")

cv2.destroyAllWindows()
