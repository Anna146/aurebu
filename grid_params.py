__author__ = 'tigunova'
import matplotlib.pyplot as pl



f = open('grids/step_precision.txt', 'r')

l0 = []
l1 = []
p = []
r = []
par = []

for line in f:
    fields = line.strip().split(' ')
    l0.append(fields[0])
    l1.append(fields[1])
    r.append(fields[5])
    p.append(fields[6])
    par.append(fields[-1])

fig = pl.figure()
ax = fig.add_subplot(111)


pl.plot(p,r, 'ro')

for xy in zip(par, p, r):                                       # <--
    ax.annotate('(%s)' % xy[0], xy=xy[1:],
        textcoords='offset points') # <--
'''
for xy in enumerate(zip(p, r)):                                       # <--
    ax.annotate('(%d)' % (int(xy[0])+1), xy=xy[1],
        textcoords='offset points')
'''

pl.xlabel('precision')
pl.ylabel('recall')

pl.grid()
#pl.show()
pl.savefig('grids/grid_step.png')
