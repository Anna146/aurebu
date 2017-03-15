import os
import os.path
import json
from sklearn.model_selection import ShuffleSplit

files = os.listdir('C:/DVD_Potocnik_31.08.2016/real_tif')
files_bare = [x.split('_')[0] for x in files]
files_dic = dict((x,[z for z in files if z.find(x) != -1]) for x in files_bare)


rs = ShuffleSplit(n_splits=1, test_size=.02, random_state=0)

for train_index, test_index in rs.split(files_bare):
    valid = [files_bare[x] for x in test_index]

for_js = []

for doc in valid:
    if not os.path.isfile('jsons/' + doc + '-words.json'):
        continue
    for_js += [{'image_path':'/imgs/'+x, 'rects':[{'x1':1,'y1':1,'x2':2,'y2':2}]} for x in files_dic[doc]]

print(len(for_js))

outfile = open('validation.json', 'w')
json.dump(for_js, outfile)