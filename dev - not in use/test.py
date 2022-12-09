from PIL import Image
from PIL import ImageDraw, ImageFont
 
# Open an Image

# img = Image.open('assets/camera.jpeg')

image = Image.open('assets/slogan.jpeg')

img = Image.new('RGB', (300, 750), (255,255,255))
 
# Call draw Method to add 2D graphics in an image
I1 = ImageDraw.Draw(img)

font = ImageFont.truetype("Chalkduster.ttf", 1)
 
# Add Text to an image
I1.text((242, 739), "12.9.2022", fill=(255, 0, 0))
 
# Display edited image
img.show()
 
# Save the edited image