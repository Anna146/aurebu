import numpy as np
import cv2
from PIL import Image
from matplotlib import pyplot as plt
from skimage import segmentation, filters, io, color

'''
img = io.imread('imgs_squares/out_07010000259094.png')
img = color.rgb2gray(img)
from skimage import measure
'''
import itertools
import operator

def filter_predictions(f_name, preds, confs):
    preds = zip(preds,confs)
    fat = sorted([(k,[y for y in v]) for k,v in itertools.groupby(sorted(preds, key=operator.itemgetter(0)),key=operator.itemgetter(0))], key=lambda x: (len(x[1]),sum([y[1] for y in x[1]])))[-1]
    if len(fat[1])>1:
        print fat[0]

filter_predictions('', ['mama', 'nee', 'foo', 'mama', 'nee'],[71,2,3,4,8])
'''
mask = img > filters.threshold_otsu(img)
clean_border = segmentation.clear_border(mask)
plt.figure()
plt.imshow(clean_border, cmap='gray')
plt.figure()
coins_edges = segmentation.mark_boundaries(img, clean_border.astype(np.int))
plt.contour(clean_border, [0.5])
plt.show()
#misc.imsave('imgs_out/07010000259094_color.jpg', binary_img)
'''