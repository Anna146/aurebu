import labelled_words
import tr_test_split

all_fields = ['aftertax', 'commission', 'tripdate', 'traveller', 'voucherdate', 'duedate', 'pretax', 'pstreet', 'pzip', 'pcity', 'cname', 'cstreet', 'czip', 'currency', 'vatpercent', 'ccity']
#all_fields = ['ccity']
for name in all_fields:
    print('processing: '+name)
    labelled_words.labelled_worder(name)
    tr_test_split.tr_test_splitter(name)