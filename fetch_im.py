import urllib2
import os
import PythonMagick

imgdir_path = 'imgs/' #'/Users/tigunova/PycharmProjects/untitled1/imgs'

def fetch_doc(docnum):
    url = 'http://aurebu.dev.inquence.com/dboard/bill/' + docnum + '.tif__0001.pdf'
    #http://aurebu.dev.inquence.com/dboard/bill/07010000259094.tif__0001.pdf
    file_name = url.split('/')[-1]
    try:
        u = urllib2.urlopen(url)
    except:
        return
    f = open(imgdir_path + docnum + '.pdf', 'wb')
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
for fil in os.listdir('jsons/'):
    document_numb = fil[:-11]
    fetch_doc(document_numb)
'''

f = open('img_list.txt', 'r')
for document_numb in f:
    fetch_doc(document_numb.strip())


