from database import cursor
import csv

def get_packets():
    query = ("SELECT * FROM one ORDER BY epoch")
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

data = get_packets()
convert_to_csv('one.csv', data)