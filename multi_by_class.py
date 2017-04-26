import matplotlib.pyplot as plt
import numpy as np

stuffs = ['aftertax', 'commission', 'tripdate', 'traveller', 'voucherdate', 'duedate', 'pretax', 'pstreet', 'pzip', 'pcity', 'cname', 'cstreet', 'czip', 'currency', 'vatpercent', 'ccity']
refer_dict = dict((x[0]+2, x[1]) for x in enumerate(stuffs))
refer_dict[20] = 'all'

f = open("19.precision.txt", 'r')

stats = dict()

p = []
r = []
c = []

for line in f:
    fields = line.split(' ')
    stats[fields[7].strip()] = (fields[5],fields[6]) #(r,p) pair
    p += [float(fields[6])]
    r += [float(fields[5])]
    c += [int(fields[7].strip())]
names = [refer_dict[x] for x in c]
'''
fig = pl.figure()
ax = fig.add_subplot(111)

pl.plot(c,p, 'ro')

for xy in zip(c,p):
    ax.annotate('(%s)' % refer_dict[xy[0]], xy=xy,
        textcoords='offset points')

pl.xlabel('class')
pl.ylabel('precision')

pl.grid()
pl.show()
'''
ind = np.arange(len(refer_dict))
width = 0.35
fig, ax = plt.subplots(figsize =(20,20))
rects1 = ax.bar(ind, p, width, color='r')
rects2 = ax.bar(ind + width, r, width, color='y')

ax.set_ylabel('Counts')
ax.set_title('Label distribution')
ax.set_xticks(ind + width / 2)
ax.set_xticklabels(names)

ax.legend((rects1[0], rects2[0]), ('Precision', 'Recall'))
plt.show()
