import csv

reader = csv.reader(open('doc.csv'), delimiter=';')
reader.next()
mydict = dict((str(rows[1]),list(rows[i] for i in range(2,26))) for rows in reader)
print(mydict["07010000259094"])