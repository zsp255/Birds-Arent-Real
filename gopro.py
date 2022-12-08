from goprocam import GoProCamera
from goprocam import constants
from PIL import Image

gopro1 = GoProCamera.GoPro(constants.gpcontrol)
#gopro1.mode(constants.Mode.PhotoMode)

tmp = gopro1.take_photo()
name1 = tmp.split("/")[5]
name2 = tmp.split("/")[6]
gopro1.downloadLastMedia()

im = Image.open(name1+"-"+name2)
im.show()
