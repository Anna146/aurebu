import csv
import pprint
import json
from PIL import Image
from PIL import ImageDraw
import os
import cv2
import string
import translitcodec
import pylev

imgdir_path = 'C:/DVD_Potocnik_31.08.2016/real_tif3' #'/Users/tigunova/PycharmProjects/untitled1/imgs'
json_dir = 'jsons3'
parts_path = 'C:/Users/tigunova/PycharmProjects/untitled1/parts/'

koeff = 1
itr =1


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
        this_crop = (c['x1'], c['y1'], c['x2'], c['y2'])
        imm = im.crop([x for x in this_crop])
        imm.save(parts_path + str(itr) + '.png')
        #imm.show()
        #draw.rectangle(this_crop, outline='blue')
        #print(words[j] + '===' + str(itr))
        itr += 1
        j += 1
    #im.save('imgs_out/new.jpg')
    #orig_im.save(out_path)
    #im.show()
    #text_im.save(out_path)


def load_labels():
    reader = csv.reader(open('labels.csv'), delimiter=';')
    mydict = dict((int(row[0]),row[1]) for row in reader)
    return mydict


def min(a,b):
    return -max(-a,-b)

def make_squares(path, out_path, json_path, dic, field_names):
    #print('==================')
    tresh = 0.1
    #orig_im = Image.open(path)
    dic = dict([(x,dic[x]) for x in field_names])#dict([(field_name,dic[field_name])])
    #a,b = orig_im.size
    #im = Image.new("RGBA", (a*2,b*2), color = "white")
    #draw = ImageDraw.Draw(im)
    try:
        js = json.load(open(json_path, 'r'))
    except:
        raise Exception('no such json')
    sqrs = []
    pages = []
    page_num = len(js["result"])
    kwords = []
    if 'vatpercent' in field_names:
        if dic['vatpercent'] == 0:
            return sqrs, pages, page_num
    for page in range(len(js["result"])):
        words = [x for x in js['result'] if x['page'] == page+1][0]['words']
        prev = ''
        prev_bx = dict()
        maxx = -1
        maxy = -1
        j = 0
        uncomb = False
        uncomb_prev = False
        for wrd in words:
            j += 1
            maxx = max(maxx, wrd[3])
            maxy = max(maxy, wrd[4])
            for key, k in dic.items():
                if key.find('date') == -1:
                     decoded = wrd[0].translate({0xfc: u'ue',0xe4: u'ae',0xf6: u'oe',0xdf: u'ss'}).encode("ascii",'ignore').translate(string.maketrans("",""), string.punctuation).lower()
                else:
                    decoded = wrd[0].encode("ascii","ignore").translate(string.maketrans("",""), string.punctuation.replace('.','')).lower()
                    if len(decoded.split('.')[-1]) == 4:
                      decoded = decoded[:-4]+decoded[-2:]
                k = k.replace(',','')
                if key.find('date') != -1:
                    k = k[:-4]+k[-2:]
                #k = k.split(' ')[0]
                if k == '':
                    continue
                distance = pylev.levenshtein(k, decoded)
                if key.find('date') != -1:
                    k_w20 = k[:6] + '20' + k.split('.')[-1]
                    distance = min(distance, pylev.levenshtein(k_w20, decoded))

                if key.find('street') != -1:
                    kk = k.split(' ')[0].split('.')[0]
                    if len(kk) > 4:
                        distance = min(distance, pylev.levenshtein(kk, decoded))
                if len(decoded)>1 and (distance*1.0/min(len(k),len(decoded))<tresh):
                    #print(decoded)
                    #draw.rectangle(((wrd[1],wrd[2]),(wrd[3],wrd[4])), fill = "black", outline = "blue")
                    sqrs += [{'x1':wrd[1]*koeff,'y1':wrd[2]*koeff,'x2':wrd[3]*koeff,'y2':wrd[4]*koeff}]
                    pages += [page]
                    kwords += [k]
                    uncomb = True
                    continue

                if len(prev_bx) > 0 and prev_bx[1] < wrd[3] and prev_bx[2] < wrd[4] and prev_bx[4] > wrd[2]:
                    comb = prev+decoded
                    distance = pylev.levenshtein(k, comb)

                    if key.find('date') != -1:
                        k_w20 = k[:6] + '20' + k.split('.')[-1]
                        distance = min(distance, pylev.levenshtein(k_w20, comb))
                    if len(decoded)>0 and (distance*2.0/(len(k)+len(comb))<tresh) and not uncomb_prev and not uncomb:
                        #print(decoded)
                        #draw.rectangle(((wrd[1],wrd[2]),(wrd[3],wrd[4])), fill = "black", outline = "blue")
                        if key.find('street') != -1 and len(sqrs) > 0 and sqrs[-1]['x1'] == prev_bx[1] and sqrs[-1]['y1'] == prev_bx[2]:
                            sqrs = sqrs[:-1]
                        sqrs += [{'x1':prev_bx[1]*koeff,'y1':prev_bx[2]*koeff,'x2':wrd[3]*koeff,'y2':wrd[4]*koeff}]
                        pages += [page]
                        kwords += [k]
                        continue
                        #print(comb + '-' + k)

            uncomb_prev = uncomb
            if key.find('street') != -1:
                uncomb_prev == False
            uncomb = False
            prev = decoded
            prev_bx = wrd
    #im.save(out_path)
    #im.show()

    '''
    if len(sqrs)  > 0:
        for lab in range(page_num):
            sqrs1 = [sqrs[j] for j in range(len(sqrs)) if pages[j] == lab]
            #kwords1 = [kwords[j] for j in range(len(sqrs)) if pages[j] == lab]
            if len(sqrs1) > 0:# and lab == 0:
                try:
                    #process_image(imgdir_path + '/' + path.split('/')[-1][:-11] + '_Seite_' + str(lab+1) + '_Bild_0001.tif', sqrs1, kwords)
                    process_image(imgdir_path + '/' + path.split('/')[-1].split('_')[0] + '_Seite_' + str(lab+1) + '_Bild_0001.tif', sqrs1, kwords)
                except:
                    continue
    '''
    return sqrs, pages, page_num

#if __name__ == '__main__':
def labelled_worder(field_name):
    labels = load_labels()
    #pprint.pprint(labelling)
    pages = [0,1] #never do that please its hardcoded
    i=0
    res_data = []
    col = 0

    #field_name = 'aftertax' #a number of column
    field_names = [field_name]#['aftertax']#, 'aftertax', 'commission', 'tripdate', 'duedate', 'traveller', 'voucherdate', 'duedate']
    #field_name = "pretax" #a number of column
    #field_names = ['pretax']

    direc = 'boxes_' + field_name + '/'
    try:
        os.stat(direc)
    except:
        os.mkdir(direc)

    #load csv
    reader = csv.reader(open('doc.csv'), delimiter=';')
    reader.next()
    csv_dict = dict((int(rows[1]),list(rows[i] for i in range(0,36))) for rows in reader)

    for fil in os.listdir(imgdir_path):
    #for fil in os.listdir(json_dir):
        #fil = '07010000450027-words.json'
        #document_numb = fil[:-11]
        document_numb = fil.split('_')[0]
        col += 1
        #bad stuff to be removed
        if col < 0:
            continue
        table = csv_dict[int(document_numb)]
        labelling = dict((labels[j].lower(),table[j].lower()) for j in range(len(table)) if labels[j] != '' and labels[j] != '-')
        path = imgdir_path + '/' + fil
        #json_path = json_dir + '/' + document_numb + "-words.json"
        json_path = json_dir + '/' + document_numb + ".json"
        out_path = "imgs_squares/labelled_"+ document_numb +".png"
        try:
            res_squrs, res_pgs, page_num = make_squares(path, out_path, json_path, labelling, field_names)
        except:
            continue
        #exit(0)
        try:
            for i in range(page_num): #here should be page_num
                new_doc = dict()
                #new_doc['image_path'] = '/imgs/' + path.split('/')[-1][:-11] + '_Seite_' + str(i+1) + '_Bild_0001.tif'
                new_doc['image_path'] = '/experiment/imgs3/' + path.split('/')[-1].split('_')[0] + '_Seite_' + str(i+1) + '_Bild_0001.tif'
                new_doc['rects'] = [res_squrs[j] for j in range(len(res_squrs)) if res_pgs[j] == i]
                if len(new_doc['rects']) > 0:
                    res_data += [new_doc]
        except Exception as e:
            print(e)
            with open(direc + 'test_boxes1_'+str(col)+'.json', 'w') as outfile:
                json.dump(res_data,outfile)
            continue
        if col % 1000 == 0:
            print(col)
            with open(direc + 'test_boxes1_'+str(col)+'.json', 'w') as outfile:
                json.dump(res_data,outfile)
        #print(path)

    with open(direc + '3test_boxes1.json', 'w') as outfile:
        json.dump(res_data,outfile)


