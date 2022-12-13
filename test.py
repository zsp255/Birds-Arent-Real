import cv2
import os
import time
from PIL import Image

image = Image.open("server_image.jpg")
take = image.rotate(270)
take.show()