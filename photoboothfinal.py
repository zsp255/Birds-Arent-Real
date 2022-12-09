import cv2
import os
import time
# import numpy as np
from goprocam import GoProCamera
from goprocam import constants
import socket
import urllib.request

from PIL import Image, ImageOps, ImageDraw, ImageFont

strip_rows = 4
strip_columns = 1
strip_width = 300
strip_height = 750

strip = Image.new('RGB', (strip_width, strip_height), (255,255,255))
row_gutter = 15

target_height = int((strip_height - ((strip_rows + 1) * row_gutter)) / strip_rows)
target_width = int(strip_width-20)


gopro1 = GoProCamera.GoPro(constants.gpcontrol)
gopro1.mode(constants.Mode.PhotoMode)

### Style
FONT = cv2.FONT_HERSHEY_DUPLEX


### Main Program
cam = cv2.VideoCapture(0)

cv2.namedWindow("test_flipped")

img_counter = 0
time_stamp = None
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
            ### Prompt the go pro to take picture
            tmp = gopro1.take_photo()
            print("gp photo taken")
            urllib.request.urlretrieve(tmp, "testgp.jpg")
            print("download")
            break
            # time stamp = None

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
        else:   
            ### If time_stamp is on, refresh time_stamp
            time_stamp = time.time()

cam.release()

cv2.destroyAllWindows()

print("destroy windows")
t = time.time()

print("switching network")
#os.system("networksetup -setairportnetwork en0 C4\ Wifi Hoover2023")
os.system("networksetup -setairportnetwork en0 AK hello123")
print("switched network")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('172.20.10.8', 8080))
server.listen()

print("socket open")

client_socket, client_address = server.accept()

file = open("server_image.jpg", 'wb')

image_chunk = client_socket.recv(2048)

while image_chunk:
    file.write(image_chunk)
    image_chunk = client_socket.recv(2048)

# if msg_rec == "ready":
#     urllib.request.urlretrieve("http://10.150.66.178:8000/readme.md", "readme_download.md")

file.close()
client_socket.close()    


image = Image.open("opencv_frame_1.jpg")
# image = Image.open("assets/slogan.jpeg")
image = ImageOps.fit(image, (target_width, target_height))
y = (0 * target_height) + ((0+1) * row_gutter)
x = 10
strip.paste(image, (x,y))

image = Image.open("testgp.jpg")
# image = Image.open("assets/slogan.jpeg")
image = ImageOps.fit(image, (target_width, target_height))
y = (1 * target_height) + ((1+1) * row_gutter)
x = 10
strip.paste(image, (x,y))

image = Image.open("server_image.jpg")
# image = Image.open("assets/slogan.jpeg")
image = ImageOps.fit(image, (target_width, target_height))
y = (2 * target_height) + ((2+1) * row_gutter)
x = 10
strip.paste(image, (x,y))

image = Image.open("assets/slogan.jpeg")
image = ImageOps.fit(image, (target_width, target_height))
y = (3 * target_height) + ((3+1) * row_gutter)
x = 10
strip.paste(image, (x,y))
                    
I1 = ImageDraw.Draw(image)
font = ImageFont.truetype("Chalkduster.ttf", 1)
I1.text((238, 737), "12.9.2022", fill=(255, 0, 0))
strip.save("photostrip.jpeg")
strip.show()

os.system("python3 tkinter_send_mail.py")