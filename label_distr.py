import matplotlib.pyplot as plt
import json
import numpy as np

stuffs = ['aftertax', 'commission', 'tripdate', 'traveller', 'voucherdate', 'duedate', 'pretax', 'pstreet', 'pzip', 'pcity', 'cname', 'cstreet', 'czip', 'currency', 'vatpercent', 'ccity']
#['traveller', 'pcity', 'tripdate', 'cname', 'pretax']
refer_dict = dict((x[0]+2, x[1]) for x in enumerate(stuffs))

label_file = 'boxes_all/test_boxes_good_full.json'

js = json.load(open(label_file, 'r'))

lab_counts_total = dict()
lab_counts_doc = dict()

for doc in js:
    lab_loc = set()
    for rect in doc['rects']:
        lab_loc.add(rect['label'])
        if rect['label'] in lab_counts_total:
            lab_counts_total[rect['label']] += 1
        else:
            lab_counts_total[rect['label']] = 1
    for lab in lab_loc:
        if lab in lab_counts_doc:
            lab_counts_doc[lab] += 1
        else:
            lab_counts_doc[lab] = 1

names = [refer_dict[x[0]] for x in lab_counts_doc.items()]
vals_doc = [x[1] for x in lab_counts_doc.items()]
vals_total = [x[1] for x in lab_counts_total.items()]

print(lab_counts_doc)
print(lab_counts_total)

ind = np.arange(len(refer_dict))
width = 0.35
fig, ax = plt.subplots(figsize =(20,20))
rects1 = ax.bar(ind, vals_doc, width, color='r')
rects2 = ax.bar(ind + width, vals_total, width, color='y')

ax.set_ylabel('Counts')
ax.set_title('Label distribution')
ax.set_xticks(ind + width / 2)
ax.set_xticklabels(names)

ax.legend((rects1[0], rects2[0]), ('Doc', 'Total'))
plt.show()
