import json

experim_folder = 'experiment/'
all_fields = ['aftertax', 'commission', 'tripdate', 'traveller', 'voucherdate', 'duedate', 'pretax', 'pstreet', 'pzip', 'pcity', 'cname', 'cstreet', 'czip', 'currency', 'vatpercent', 'ccity']

for name in all_fields:
    f = json.load(open('hypes/templ.json','r'))
    f['data']["train_idl"] = "./data/names/" + experim_folder + "train_boxes_" + name + "3.json"
    f['data']["test_idl"] = "./data/names/" + experim_folder + "test_boxes_" + name + "3.json"
    json.dump(f,open('hypes/'+name+'3_detect.json', 'w'))

