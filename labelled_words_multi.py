import csv
import pprint
import json
from PIL import Image
from PIL import ImageDraw
import os
import cv2
import string
import pylev

imgdir_path = 'C:/DVD_Potocnik_31.08.2016/good_data/imgs' #'/Users/tigunova/PycharmProjects/untitled1/imgs'
json_dir = 'C:/DVD_Potocnik_31.08.2016/good_data/jsons'
parts_path = 'C:/Users/tigunova/PycharmProjects/untitled1/parts/'

koeff = 23.6 / 7.5
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

def doc_fields(ident):
    reader = csv.reader(open('doc.csv'), delimiter=';')
    reader.next()
    mydict = dict((int(rows[1]),list(rows[i] for i in range(0,26))) for rows in reader)
    return mydict[int(ident)]

def min(a,b):
    return -max(-a,-b)

def make_squares(path, out_path, json_path, dic, field_name):
    tresh = 0.1
    #orig_im = Image.open(path)
    dic = dict([(field_name,dic[field_name])])
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
    for page in range(len(js["result"])):
        words = js["result"][page]["words"]
        prev = ''
        maxx = -1
        maxy = -1
        for wrd in words:
            decoded = wrd[0].encode("ascii","ignore").translate(string.maketrans("",""), string.punctuation).lower()
            maxx = max(maxx, wrd[3])
            maxy = max(maxy, wrd[4])
            for k in dic.values():
                distance = pylev.levenshtein(k, decoded)
                if len(decoded)>1 and (distance*1.0/min(len(k),len(decoded))<tresh):
                    #print(decoded)
                    #draw.rectangle(((wrd[1],wrd[2]),(wrd[3],wrd[4])), fill = "black", outline = "blue")
                    sqrs += [{'x1':wrd[1],'y1':wrd[2],'x2':wrd[3],'y2':wrd[4]}]
                    pages += [page]
                    break
                comb = prev+decoded
                distance = pylev.levenshtein(k, comb)
                if len(comb)>1 and (distance*1.0/min(len(k),len(comb))<tresh):
                    #print(decoded)
                    #draw.rectangle(((wrd[1],wrd[2]),(wrd[3],wrd[4])), fill = "black", outline = "blue")
                    sqrs += [{'x1':wrd[1],'y1':wrd[2],'x2':wrd[3],'y2':wrd[4]}]
                    pages += [page]
                    kwords += [k]
                    break
                    #print(comb + '-' + k)
            prev = decoded
    #im.save(out_path)
    #im.show()

    '''
    if len(sqrs)  > 0:
        for lab in range(page_num):
            sqrs1 = [sqrs[j] for j in range(len(sqrs)) if pages[j] == lab]
            #kwords1 = [kwords[j] for j in range(len(sqrs)) if pages[j] == lab]
            if len(sqrs1) > 0 and lab == 1:
                process_image(imgdir_path + '/' + path[5:-11] + '_Seite_' + str(lab+1) + '_Bild_0001.tif', sqrs1, kwords)
    '''
    return sqrs, pages, page_num

if __name__ == '__main__':
    labels = load_labels()
    #pprint.pprint(labelling)
    pages = [0,1] #never do that please its hardcoded
    i=0
    res_data = []
    col = 0

    field_names = ['organizer [oname; ostreet; ozip; ocity]', '']
    for fil in os.listdir(json_dir):
        document_numb = fil[:-11]
        col += 1
        if col < 4001:
            continue
        table = doc_fields(document_numb)
        labelling = dict((labels[j].lower(),table[j].lower()) for j in range(len(table)) if labels[j] != '' and labels[j] != '-')
        path = "imgs/" + fil
        json_path = "jsons/" + document_numb + "-words.json"
        out_path = "imgs_squares/labelled_"+ document_numb +".png"
        field_name = 'traveller' #a number of column
        res_squrs, res_pgs, page_num = make_squares(path, out_path, json_path, labelling, field_name)
        try:
            for i in range(1): #here should be page_num
                new_doc = dict()
                new_doc['image_path'] = '/imgs/' + path[5:-11] + '_Seite_' + str(i+1) + '_Bild_0001.tif'
                new_doc['rects'] = [res_squrs[j] for j in range(len(res_squrs)) if res_pgs[j] == i]
                res_data += [new_doc]
        except Exception as e:
            print(e)
            with open('test_boxes1_'+str(col)+'.json', 'w') as outfile:
                json.dump(res_data,outfile)
            continue
        if col % 1000 == 0:
            print(col)
            with open('test_boxes1_'+str(col)+'.json', 'w') as outfile:
                json.dump(res_data,outfile)
        #print(path)

    with open('test_boxes1.json', 'w') as outfile:
        json.dump(res_data,outfile)


