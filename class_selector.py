import csv
import pprint

all_fields = ['aftertax', 'commission', 'tripdate', 'traveller', 'voucherdate', 'duedate', 'pretax', 'pstreet', 'pzip', 'pcity', 'cname', 'cstreet', 'czip', 'currency', 'vatpercent', 'ccity']

big_table_prec = dict((x,list()) for x in all_fields)
big_table_rec = dict((x,list()) for x in all_fields)

for amount in [18, 15, 12, 9]:
    f = open("%d.precision.txt" % amount, 'r')
    with open('reference_dict_%d.txt' % amount, 'r') as fil:
        reader = csv.reader(fil)
        refer_dict = {int(rows[1]):rows[0] for rows in reader}

    r = []
    p = []
    c = []

    for line in f:
        fields = line.split(' ')
        r += [fields[5]]
        p += [fields[6]]
        c += [fields[7].strip()]

    with_names = dict((refer_dict[int(x[0])],[x[1],x[2]]) for x in zip(c,p,r) if int(x[0]) in refer_dict)

    for field in all_fields:
        big_table_prec[field] += [with_names[field][0]] if field in with_names else [-1]
        big_table_rec[field] += [with_names[field][1]] if field in with_names else [-1]


    #print(with_names)
    #print(sorted(zip(c,p), key=lambda y: -float(y[1])))
    #print('Biggest precision: ' + str(max(zip(c,p), key = lambda y: y[1])))
    f.close()

with open('precision_single.txt', 'r') as f:
    for line in f:
        fields = line.split(' ')
        clas = fields[-1].strip().split('/')[-1].split('3')[0]
        big_table_prec[clas] += [fields[4]]
        big_table_rec[clas] += [fields[3]]

pprint.pprint(big_table_prec)
with open('precision_tab.csv', 'wb') as fp:
    a = csv.writer(fp, delimiter=' ')
    a.writerows([x[0]] + x[1] for x in big_table_prec.items())