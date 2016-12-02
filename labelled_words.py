import csv
import pprint
import json
from PIL import Image
from PIL import ImageDraw
import os
import string
import pylev

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

def make_squares(path, out_path, json_path, dict,page):
    tresh = 0.7
    orig_im = Image.open(path)
    a,b = orig_im.size
    im = Image.new("RGBA", (a*2,b*2), color = "white")
    draw = ImageDraw.Draw(im)
    js = json.load(open(json_path, 'r'))
    words = js["result"][page]["words"]
    prev = ''
    for wrd in words:
        decoded = wrd[0].encode("ascii","ignore").translate(string.maketrans("",""), string.punctuation).lower()
        for k in dict:
            distance = pylev.levenshtein(k, decoded)
            if len(decoded)>1 and (distance*1.0/min(len(k),len(decoded))<tresh):
                #print(decoded)
                draw.rectangle(((wrd[1],wrd[2]),(wrd[3],wrd[4])), fill = "black", outline = "blue")
                print(decoded + '-' + k)
            comb = prev+decoded
            distance = pylev.levenshtein(k, comb)
            if len(comb)>1 and (distance*1.0/min(len(k),len(comb))<tresh):
                #print(decoded)
                draw.rectangle(((wrd[1],wrd[2]),(wrd[3],wrd[4])), fill = "black", outline = "blue")
                print(comb + '-' + k)
        prev = decoded
    im.save(out_path)
    im.show()
    return

if __name__ == '__main__':
    labels = load_labels()
    #pprint.pprint(labelling)
    pages = [0,1] #never do that please its hardcoded
    i=0

    for fil in os.listdir('/Users/tigunova/PycharmProjects/untitled1/imgs'):
        document_numb = fil[:-4]
        table = doc_fields(document_numb)
        labelling = dict((table[i].lower(),labels[i].lower()) for i in range(len(table)) if labels[i] != '' and labels[i] != '-')
        path = "imgs/" + fil
        json_path = "jsons/" + document_numb + "-words.json"
        out_path = "imgs_squares/labelled_"+ document_numb +".png"
        make_squares(path, out_path, json_path, labelling,pages[i])
        i += 1


