import cv2
import os
import time
import numpy as np
from goprocam import GoProCamera
from goprocam import constants
import socket
import urllib.request
from PIL import Image

gopro1 = GoProCamera.GoPro(constants.gpcontrol)
gopro1.mode(constants.Mode.PhotoMode)

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
                # ### Load images & show images in multiple new small windows to populate the screen 
                # my_img_1 = cv2.imread(img_name)
                # my_img_1  = ResizeWithAspectRatio(my_img_1 , width=400) # Resize to window size
                # window_name = "image_{}".format(img_counter)
                # cv2.namedWindow(window_name)
                # cv2.moveWindow(window_name, (img_counter%4)*350,(img_counter%4)*200)
                # cv2.imshow(window_name, my_img_1)
                # img_saved = False    

                ### Basic photobooth function - show pic after end of count down
                img_name = "opencv_frame_{}.png".format(img_counter)
                cv2.imwrite(img_name, frame_no_text)
                my_img_1  = ResizeWithAspectRatio(frame_no_text , width=400) # Resize to window size
                window_name = "image_{}".format(img_counter)
                cv2.namedWindow(window_name)
                cv2.moveWindow(window_name, (img_counter%4)*350,(img_counter%4)*200)
                cv2.imshow(window_name, my_img_1)

                tmp = gopro1.take_photo()
                print("gp photo taken")
                urllib.request.urlretrieve(tmp, "testgp.jpg")
                print("download")
                im = Image.open("testgp.jpg")

                img_saved = False

            time_stamp = None
            break

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
        ### SPACE pressed --> birds start taking pic, assign time stamp & start count down

        if not time_stamp:
            ### Saving time stamp
            time_stamp = time.time()
            ### Saving the image
            # img_name = "opencv_frame_{}.png".format(img_counter)
            # cv2.imwrite(img_name, frame_flipped)
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

cv2.destroyAllWindows()

print("destroy windows")
t = time.time()

while time.time() < t + 2:
    print("slow down")

print("switching network")
#os.system("networksetup -setairportnetwork en0 C4\ Wifi Hoover2023")
os.system("networksetup -setairportnetwork en0 AK hello123")
print("switched network")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('172.20.10.8', 8080))
server.listen()

print("socket open")

client_socket, client_address = server.accept()

msg_rec = client_socket.recv(1024)
msg_rec = msg_rec.decode()

# if msg_rec == "ready":
#     urllib.request.urlretrieve("http://10.150.66.178:8000/readme.md", "readme_download.md")
# client_socket.close() 
    

