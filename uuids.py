import csv

def load_csv_to_dict(filename):
    result_dict = dict()
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            uuid_, name = row['uuid'].strip(), row['name'].strip()
            if not name:
                # some rows are formatted weirdly
                uuid_, name = uuid_.strip().split(" ", maxsplit=1)

            result_dict[uuid_] = { 
                'allocation_type': row['allocation_type'].strip(),
                'name': name
            }

    return result_dict

if __name__ == "__main__":
    print(load_csv_to_dict('uuid_data.csv')['0xFECC'])