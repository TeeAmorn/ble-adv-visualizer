import csv
# APPEARANCE_SUBCATEGORIES
with open('appearance_subcategories.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    next(spamreader)
    APPEARANCE_SUBCATEGORIES = {entry[0]: entry[1] for entry in spamreader}

print(APPEARANCE_SUBCATEGORIES)
