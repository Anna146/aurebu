import numpy as np
import cv2
from PIL import Image
from matplotlib import pyplot as plt
from skimage import segmentation, filters, io, color


img = io.imread('imgs_squares/out_07010000259094.png')
img = color.rgb2gray(img)
from skimage import measure

mask = img > filters.threshold_otsu(img)
clean_border = segmentation.clear_border(mask)
plt.figure()
plt.imshow(clean_border, cmap='gray')
plt.figure()
coins_edges = segmentation.mark_boundaries(img, clean_border.astype(np.int))
plt.contour(clean_border, [0.5])
plt.show()
#misc.imsave('imgs_out/07010000259094_color.jpg', binary_img)
