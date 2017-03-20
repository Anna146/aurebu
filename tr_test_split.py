import numpy as np
from sklearn.model_selection import ShuffleSplit
import json
import os


experim_folder = 'experiment/'

def tr_test_splitter(field_name):

    imgdir_path3 = 'C:/DVD_Potocnik_31.08.2016/real_tif3'
    imgdir_path = 'C:/DVD_Potocnik_31.08.2016/real_tif'

    koef = 1

    #field_name = 'traveller' #a number of column
    direc = 'boxes_' + field_name + '/'

    #dirlist = os.listdir(imgdir_path)
    dirlist3 = os.listdir(imgdir_path3)

    js = json.load(open(direc + '3test_boxes1.json', 'r'))
    #js =js[:len(js)//2]#shrink
    print(len(js))
    js = [{'image_path':x['image_path'][1:], 'rects' : [{'x1':y['x1']*koef,'x2':y['x2']*koef,'y1':y['y1']*koef,'y2':y['y2']*koef} for y in x['rects']]} for x in js if (x['image_path'][18:] in dirlist3) and (len(x['rects']) > 0)]
    print('Len of sample for field ' + field_name + ' ' + str(len(js)))

    rs = ShuffleSplit(n_splits=1, test_size=.05, random_state=0)

    for train_index, test_index in rs.split(js):
        outfile = open(experim_folder + 'test_boxes_' + field_name + '3.json', 'w')
        json.dump([js[i] for i in test_index], outfile)
        train = [js[i] for i in train_index]
        for train_index1, val_index in rs.split(train):
            outfile = open(experim_folder + 'train_boxes_' + field_name + '3.json', 'w')
            json.dump([train[i] for i in train_index1], outfile)
            outfile = open(experim_folder + 'val_boxes_' + field_name + '3.json', 'w')
            json.dump([train[i] for i in val_index], outfile)
