from PIL import Image

from tesseract import image_to_string
print image_to_string(Image.open('test.png'))