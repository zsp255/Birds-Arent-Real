import socket
from goprocam import GoProCamera
from goprocam import constants
import urllib.request
import os

### Need to connect to GoPro2 NeelsSession before running the program

gopro1 = GoProCamera.GoPro(constants.gpcontrol)
tmp = gopro1.take_photo()
urllib.request.urlretrieve(tmp, "testgp2.jpg")

os.system("networksetup -setairportnetwork en0 AK hello123")


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('172.20.10.8', 8080))   # zach's ip on AK
# client.connect(('172.20.10.7', 8080))   # yifan's ip on AK

file1 = open("testgp2.jpg", "rb")
imagedata = file1.read(2048)

while imagedata:
    client.send(imagedata)
    imagedata = file1.read(2048)

file1.close()    
client.close()

os.remove("testgp2.jpg")
