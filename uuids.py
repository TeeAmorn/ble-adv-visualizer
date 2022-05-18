import csv

def load_csv_to_dict(filename):
    result_dict = dict()
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            uuid_, name = row['uuid'].strip(), row['name'].strip()
            if not name:
                # some rows are formatted weirdly
                uuid_, name = uuid_.strip().split(' ', maxsplit=1)

            result_dict[uuid_] = { 
                'allocation_type': row['allocation_type'].strip(),
                'name': name
            }

    return result_dict

def write_dict_to_csv(data_dict):
    '''
    Takes the output from `load_csv_to_dict` and writes it to
    a csv with the headers `['allocation_type', 'uuid', 'name']`
    '''
    with open('reformatted_uuids.csv', 'w', newline='') as csvfile:
        fieldnames = ['allocation_type', 'uuid', 'name']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for uuid_, info_dict in data_dict.items():
            row = {
                'uuid': uuid_, 
                **info_dict
            }
            writer.writerow(row)


if __name__ == '__main__':
    loaded_data_dict = load_csv_to_dict('uuid_data.csv')
    write_dict_to_csv(loaded_data_dict)