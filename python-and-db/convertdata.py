from database import cursor
import csv

def get_packets(tablename):
    query = ("SELECT * FROM " + tablename + " ORDER BY epoch")
    cursor.execute(query)
    rows = cursor.fetchall()
    result = []
    for row in rows:
        row = list(row)
        row[2] = row[2].strftime("%m/%d/%Y, %H:%M:%S")
        result.append(row)
    return result

def convert_to_csv(filename, data):
    with open(filename, 'w') as f:
        write = csv.writer(f)
        write.writerows(data)

tablename = 'six'
filename = 'keyboard_pairing'
data = get_packets(tablename)
convert_to_csv('csv/' + filename + '.csv', data)