import csv
with open('appearance.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    APPEARANCES = {}
    for i, entry in enumerate(spamreader):
        if entry[2] == 'Outdoor Sports Activity':
            APPEARANCES[81] = entry[2]
        else:
            APPEARANCES[i] = entry[2]

print(APPEARANCES)
