import matplotlib.pyplot as pl
import plotly.plotly as py

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

fig = pl.figure()
ax = fig.add_subplot(111)

pl.plot(c,r, 'ro')

for xy in zip(c,r):
    ax.annotate('(%s)' % refer_dict[xy[0]], xy=xy,
        textcoords='offset points')

pl.xlabel('class')
pl.ylabel('precision')

pl.grid()
pl.show()

