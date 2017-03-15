import numpy as np
from sklearn.model_selection import ShuffleSplit
import json
import os

imgdir_path = 'C:/DVD_Potocnik_31.08.2016/real_tif'

koef = 1

field_name = 'ccity' #a number of column
direc = 'boxes_' + field_name + '/'

js = json.load(open(direc + 'test_boxes1.json', 'r'))
#js =js[:len(js)//2]#shrink
print(len(js))
js = [{'image_path':x['image_path'][1:], 'rects' : [{'x1':y['x1']*koef,'x2':y['x2']*koef,'y1':y['y1']*koef,'y2':y['y2']*koef} for y in x['rects']]} for x in js if x['image_path'][6:] in os.listdir(imgdir_path) and (len(x['rects']) > 0 or field_name == 'vatpercent')]
print(len(js))

rs = ShuffleSplit(n_splits=1, test_size=.05, random_state=0)

for train_index, test_index in rs.split(js):
    outfile = open(direc + 'test_boxes_' + field_name + '.json', 'w')
    json.dump([js[i] for i in test_index], outfile)
    train = [js[i] for i in train_index]
    for train_index1, val_index in rs.split(train):
        outfile = open(direc + 'train_boxes_' + field_name + '.json', 'w')
        json.dump([train[i] for i in train_index1], outfile)
        outfile = open(direc + 'val_boxes_' + field_name + '.json', 'w')
        json.dump([train[i] for i in val_index], outfile)
