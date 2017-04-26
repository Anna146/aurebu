import numpy as np
from sklearn.model_selection import ShuffleSplit
import json
import os


experim_folder = 'single_class/for_all/'
num_classes = 'full'

def tr_test_splitter_single(field_name):

    imgdir_path3 = 'C:/DVD_Potocnik_31.08.2016/real_real'

    koef = 1

    #field_name = 'traveller' #a number of column
    direc = 'single_class/boxes_' + field_name + '/'

    #dirlist = os.listdir(imgdir_path)
    dirlist3 = os.listdir(imgdir_path3)

    #js = json.load(open(direc + 'test_boxes_good_full.json', 'r'))
    js = json.load(open(direc + 'test_boxes_' + field_name +'.json', 'r'))
    #js =js[:len(js)//2]#shrink
    print(len(js))
    js = [{'image_path':x['image_path'][1:], 'rects' : [{'x1':y['x1']*koef,'x2':y['x2']*koef,'y1':y['y1']*koef,'y2':y['y2']*koef, 'label':y['label']} for y in x['rects']]} for x in js if (x['image_path'][7:] in dirlist3) and (len(x['rects']) > 0)]
    print('Len of sample for field ' + field_name + ' ' + str(len(js)))

    rs = ShuffleSplit(n_splits=1, test_size=.1, random_state=0)
    rs2 = ShuffleSplit(n_splits=1, test_size=.004, random_state=0)

    for train_index, test_index in rs.split(js):
        outfile = open(experim_folder + 'test_boxes_' + field_name + '.json', 'w')
        json.dump([js[i] for i in test_index], outfile)
        train = [js[i] for i in train_index]
        print('Test len %d' % len(test_index))
        for train_index1, val_index in rs2.split(train):
            outfile = open(experim_folder + 'train_boxes_' + field_name + '.json', 'w')
            json.dump([train[i] for i in train_index1], outfile)
            print('Train len %d' % len(train_index1))
            outfile = open(experim_folder + 'val_boxes_' + field_name + '.json', 'w')
            json.dump([train[i] for i in val_index], outfile)
            print('Validation len %d' % len(val_index))
