import csv
import pprint
import json
from PIL import Image
from PIL import ImageDraw
import os
import cv2
import string
import pylev

imgdir_path = 'C:/Users/tigunova/Desktop/'#'C:/DVD_Potocnik_31.08.2016/real_tif/' #'/Users/tigunova/PycharmProjects/untitled1/imgs'
json_dir = 'jsons3'
parts_path = 'C:/Users/tigunova/PycharmProjects/untitled1/segm/'
im_num = '00000005142008'

koeff = 0.5
itr =0

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
        this_crop = (c[1], c[2], c[3], c[4])
        imm = im.crop([x*koeff for x in this_crop])
        imm.save(parts_path + im_num + '/' + str(itr) + '.png')
        #imm.show()
        #draw.rectangle(this_crop, outline='blue')
        #print(words[j] + '===' + str(itr))
        itr += 1
        j += 1
    #im.save('imgs_out/new.jpg')
    #orig_im.save(out_path)
    #im.show()
    #text_im.save(out_path)

def get_squares(json_path,page):
    try:
        js = json.load(open(json_path, 'r'))
    except:
        raise Exception('no such json')
    return [x for x in js['result'] if x['page'] == page][0]['words']

if __name__ == '__main__':
    page_num = 1
    json_path = json_dir + '/' + im_num + ".json"
    direc = parts_path + im_num
    try:
        os.stat(direc)
    except:
        os.mkdir(direc)
    process_image(imgdir_path + im_num+'_Seite_'+str(page_num) +'_Bild_0001.tif',get_squares(json_path,page_num),[])