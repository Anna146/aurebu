import urllib2
import os
import os

imgdir_path = 'C:/DVD_Potocnik_31.08.2016/original/GB3613B1.60552016010120160331.12110' #'/Users/tigunova/PycharmProjects/untitled1/imgs'

def fetch_doc(docnum):
    print(docnum)
    url = 'http://aurebu.dev.inquence.com/dboard/bill/words/' + docnum + '.tif::0001'

    file_name = url.split('/')[-1]
    try:
        u = urllib2.urlopen(url)
    except:
        print('no such url')
        return
    f = open('jsons/' + docnum + '-words.json', 'wb')
    meta = u.info()
    #file_size = int(meta.getheaders("Content-Length")[0])
    #print "Downloading: %s Bytes: %s" % (file_name, file_size)

    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        file_size_dl += len(buffer)
        f.write(buffer)
        status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100.)
        status = status + chr(8)*(len(status)+1)

    f.close()

'''
for fil in os.listdir(imgdir_path):
    document_numb = fil[:-4]
'''

#f = open('img_list.txt', 'r')
f = os.listdir(imgdir_path)
for document_numb in f:
    fetch_doc(document_numb[:-4].strip())


