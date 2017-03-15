import csv
import pprint
import json
from PIL import Image
from PIL import ImageDraw
import os
import cv2
import string
import pylev

imgdir_path = 'C:/DVD_Potocnik_31.08.2016/real_tif' #'/Users/tigunova/PycharmProjects/untitled1/imgs'
json_dir = 'jsons'
parts_path = 'C:/Users/tigunova/PycharmProjects/untitled1/parts/'

itr = 0
koef = 1

def process_image(path, c_info, words):
    try:
        im = Image.open(path)
    except:
        return
    draw = ImageDraw.Draw(im)

    '''
    for c in c_info:
        this_crop = c['x1'], c['y1'], c['x2'], c['y2']
        draw.rectangle(this_crop, fill='blue')
    '''
    global itr
    j = 0
    for c in c_info:
        this_crop = (c['x1']*koef, c['y1']*koef, c['x2']*koef, c['y2']*koef)
        imm = im.crop([x for x in this_crop])
        imm.save(parts_path + str(itr) + '.png')
        #imm.show()
        #draw.rectangle(this_crop, outline='blue')
        #print(words[j] + '===' + str(itr))
        itr += 1
        j += 1

boxes = json.load(open('boxes_voucherdate/train_boxes.json','r'))
for box in boxes:
    process_image(imgdir_path+ '/' + box['image_path'][5:],box['rects'],[])

