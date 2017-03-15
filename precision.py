from __future__ import division
import json
from PIL import Image
from PIL import ImageDraw
import numpy as np
import os.path
import csv
import string

eps = 10
imgdir_path = 'C:/DVD_Potocnik_31.08.2016/real_tif/'
json_dir = 'jsons'
itr = 0

def load_labels():
    reader = csv.reader(open('labels.csv'), delimiter=';')
    mydict = dict((row[1], int(row[0])) for row in reader)
    return mydict

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
        this_crop = (c['x1']-eps, c['y1']-eps, c['x2']+eps, c['y2']+eps)
        imm = im.crop([x for x in this_crop])
        imm.save('res_parts/' + str(itr) + '.png')
        #imm.show()
        #draw.rectangle(this_crop, outline='blue')
        #print(words[j] + '===' + str(itr))
        itr += 1
        j += 1
    #im.save('imgs_out/new.jpg')
    #orig_im.save(out_path)
    #im.show()
    #text_im.save(out_path)


def calc_match(r1,r2):
    preds = [0 for x in r2]
    lstat = [0,0,0]
    for rec1 in r1:
        found = False
        for j in range(len(r2)):
            rec2 = r2[j]
            if abs(rec1['x1']-rec2['x1']) < eps and abs(rec1['x2']-rec2['x2']) < eps and abs(rec1['y1']-rec2['y1']) < eps and abs(rec1['y2']-rec2['y2']) < eps:
                found = True
                preds[j] = 1
                break
        if found:
            lstat[0] += 1
        else:
            lstat[2] += 1
    for j in preds:
        if not j:
            lstat[1] += 1
    return np.array(lstat)

f = open('precise.txt', 'w')

def word_match(reals, preds):
    tp = len([i for i in range(len(reals)) if reals[i] == preds[i]])
    return tp, len(reals)-tp

def area(a, b):  # returns None if rectangles don't intersect
    dx = min(a['x2'], b[3]) - max(a['x1'], b[1])
    dy = min(a['y2'], b[4]) - max(a['y1'], b[2])
    if (dx>=0) and (dy>=0):
        return dx*dy
    else:
        return 0

def dist(c1, c2):
    return (abs(c1[0]-c2[0])**2 + abs(c1[1]-c2[1])**2)**0.5

def try_json(j_path, coords, field,doc_num, mdic, fname, page):
    thr = 0.01
    try:
        true_doc = json.load(open(j_path, 'r'))
    except:
        return '?','?'
    date_ch = 0 if field.find('date') == -1 else 1
    money_ch = 1 if field in ['pretax', 'aftertax', 'commission'] else 0
    real = mdic[int(doc_num)][fname]
    words = [x for x in true_doc['result'] if x['page'] == page+1][0]['words']
    if len(coords) == 0 or len(words) < 70:
        return real, [], []
    predict = ''
    if date_ch:
        real = real[:-4] + real[-2:]
    cur_preds = []
    confs = []
    for rec1 in coords:
        if rec1['score'] < 0.1:
            continue
        mid = ((rec1['y2'] - rec1['y1']) / 2 + rec1['y1'],(rec1['x2'] - rec1['x1']) / 2 + rec1['x1'])
        min_dist = 100500
        min_dist_wrd = ''
        for rec2 in words:
            wmid = ((rec2[4] - rec2[2]) / 2 + rec2[2],(rec2[3] - rec2[1]) / 2 + rec2[1])
            di = dist(mid, wmid)
            if di < min_dist:
                min_dist = di
                min_dist_wrd = rec2[0].encode("ascii","ignore").translate(string.maketrans("","")).lower()
            #if abs(rec1['x1']-rec2[1]) < eps and abs(rec1['y1']-rec2[2]) < eps:# and abs(rec1['y1']-rec2[2]) < eps and abs(rec1['y2']-rec2[4]) < eps:
            if area(rec1,rec2) / abs(rec2[3]-rec2[1]) / abs(rec2[4]-rec2[2]) > thr:
                if date_ch or money_ch:
                    predict += rec2[0].encode("ascii","ignore").translate(string.maketrans("",""), string.punctuation.replace('.','').replace(',','')).lower()
                    #f.write(rec2[0].encode("ascii","ignore").translate(string.maketrans("",""), string.punctuation.replace('.','')).lower() + '  ---  ' + real + '\n')
                else:
                    predict += rec2[0].encode("ascii","ignore").translate(string.maketrans("",""), string.punctuation).lower()
                rec1['x1'] = rec2[3]
                if rec1['x1'] > rec1['x2']:
                    break
        if predict == '' and rec1['score'] > 0.5 and min_dist_wrd != '':
            predict = min_dist_wrd
        if date_ch and len(predict.split('.')[-1]) == 4:
           predict = predict[:-4]+predict[-2:]
        if date_ch and len(predict.split('.')) != 3:
            predict = ''
        if predict != '':
            if field in ['traveller', 'pcity', 'pstreet']:
                predict = ''.join([i for i in predict if i.isalpha()])
                if predict != '':
                    predict = predict[0].upper() + predict[1:]
            if date_ch or money_ch or field == 'pzip':
                predict = ''.join([i for i in predict if not i.isalpha()])
                if len(''.join([i for i in predict if i.isdigit()])) == 0:
                    predict = ''
            cur_preds += [predict]
            confs += [rec1['score']]
        predict = ''
    return real, cur_preds, confs
                    #f.write(rec2[0].encode("ascii","ignore").translate(string.maketrans("","")).lower() + '  --- ' + real.lower() + '\n')
import itertools
import operator

def filter_predictions(f_name, preds, confs):
    preds = zip(preds,confs)
    fat = sorted([(k,[y for y in v]) for k,v in itertools.groupby(sorted(preds, key=operator.itemgetter(0)),key=operator.itemgetter(0))], key=lambda x: (len(x[1]),sum([y[1] for y in x[1]])))
    return fat[-1][0]
    #return max(zip(preds,confs), key = lambda x: x[1])[0]


reader = csv.reader(open('doc.csv'), delimiter=';')
reader.next()
mdic = dict((int(rows[1]),list(rows[i] for i in range(0,31))) for rows in reader)

labels = load_labels()

stats = np.array([0,0,0])
'''
for i in range(len(true)):
    stats = calc_match(true[i]['rects'],pred[i]['rects']) + stats
'''

field_names = ['traveller','voucherdate', 'pstreet', 'aftertax', 'commission', 'duedate', 'pretax', 'pcity', 'pzip']
big_dict = dict()
i = 0
want = '07010000416093'
doc_lst = []
files_dic = dict()

for name in field_names:
    np = 0
    pred = json.load(open('C:/Users/tigunova/Desktop/predictions/pred_'+name+'.json', 'r'))
    true = json.load(open('C:/Users/tigunova/Desktop/predictions/true_'+name+'.json', 'r'))
    doc_lst = list(set(x['image_path'].split('_')[0].split('/')[-1] for x in pred))
    files_dic = dict((str(x),[z for z in pred if z['image_path'].find(str(x)) != -1]) for x in doc_lst)
    if len(big_dict) == 0:
        big_dict = dict((x,['' for x in range(len(field_names))]) for x in doc_lst)
        print(len(big_dict))
        #big_dict = dict((pr['image_path'].split('_')[0].split('/')[-1],['' for x in range(len(field_names))]) for pr in pred)
    reals = []
    predicts = []
    j = 0
    #for pr in pred:
    for document_numb in doc_lst:
        #document_numb = pr['image_path'].split('_')[0].split('/')[-1]
        #if document_numb != want:
        #    continue
        ps1 = []
        confs1 = []
        for pr in files_dic[document_numb]:
            json_path = json_dir + '/' + document_numb + "-words.json"
            r1, ps11, confs11 = try_json(json_path, pr['rects'],name, document_numb,mdic, labels[name], int(pr['image_path'].split('_')[2])-1)
            ps1 += ps11
            confs1 += confs11
        if len(ps1) == 0:
            if len(pr['rects']) > 0:
                np += 1
            continue
        p1 = filter_predictions(name, ps1, confs1)
        reals += [r1]
        predicts += [p1]
        if document_numb in big_dict:
            big_dict[document_numb][i] = p1
        else:
            big_dict[document_numb] = ['' for x in range(len(field_names))]
            big_dict[document_numb][i] = p1
        j += 1
    i += 1
    tp, fp = word_match(reals, predicts)
    print('On field ' + name + ' precision: ' + str(tp/(tp+fp)) + ' not recognized ' + str(np))
        #process_image(imgdir_path + os.path.split(pr['image_path'])[1], pr['rects'],[])

#print('precision = ' + str(stats[0]/(stats[0]+stats[1])))
#print('recall = ' + str(stats[0]/(stats[0]+stats[2])))
#print(stats)
print(len(big_dict))
writer = csv.writer(open("result.csv", 'w'), delimiter=';', lineterminator='\n')
writer.writerow(['doc_num'] + field_names)
fg = open('faulty_guys.txt', 'w')
for k,v in big_dict.items():
    if any(len(x) for x in v) == 0:
        fg.write(str(k) + '\n')
    else:
        writer.writerow([k]+v)