import os

f = open('img_list.txt', 'w')

imgdir_path = 'C:/DVD_Potocnik_31.08.2016/original'

for vec in os.walk(imgdir_path):
    for name in vec[2]:
        f.write(name.split('.')[0] + '\n')

