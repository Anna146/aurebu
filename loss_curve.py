import matplotlib.pyplot as pl

dir = 'reses/'

ratios = [1,2,3,4,5,6,7,8,9,10]
tests = []
trains = []
max_iter = 99

for ratio in ratios:
    print(ratio)
    f = open(dir + 'rat' + str(ratio) + '.out', 'r')
    line = ''
    while not line.startswith('Step'):
        line = f.readline()
    cnt = 0
    train_loss = 0.0
    test_loss = 0.0
    while len(line) > 0:# and cnt<max_iter:
        try:
            train_loss += float(line.split(',')[2].split(' ')[-1])
            test_loss += float(line.split(',')[3].split(' ')[-1])
            cnt += 1
            line = f.readline()
        except:
            line = f.readline()
            continue
    tests += [test_loss / cnt]
    trains += [train_loss / cnt]
    print('For %d ratio avg train loss: %f avg test loss: %f' % (ratio, train_loss / cnt, test_loss / cnt))

ratios = [x / 10.0 for x in ratios]
print ratios
pl.plot(ratios, tests, 'ro', ratios, tests, 'r')
pl.plot(ratios, trains, 'bo', ratios, trains, 'b')
#pl.xlim(0,1)
pl.xlabel('train_ratio')
pl.ylabel('loss')
pl.show()
#pl.savefig('loss_plt.png')