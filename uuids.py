import csv
import re

def load_csv_to_dict(filename):
    with open(filename) as csvfile:
        # cases:
        # 1. row contains all three items -> uuid + name will be in same row
        # 2. row contains only allocation type -> uuids + names listed separately
        # 3. rows to skip (there's a bunch)
        case1_flag, case2_flag = False, False
        i = 0
        prev_iter = None
        all_rows_dicts, one_page_dicts = [], []
        reader = csv.reader(csvfile)

        for row in reader:
            if not row:
                continue

            cell = row[0]
            if cell in ['Bluetooth SIG Proprietary', '16‐bit UUID Numbers / Document']:
                continue
            elif cell == 'Allocation type Allocated UUID Allocated for':
                # start of case 1
                i, case1_flag = 0, True
                prev_iter = 'Allocation type'
            elif cell == 'Allocation type' and not prev_iter:
                # start of case 2
                i, case2_flag = 0, True
                prev_iter = 'Allocation type'
            elif cell.endswith('of 25'):
                all_rows_dicts.extend(one_page_dicts)
                i, one_page_dicts = 0, []
                case1_flag, case2_flag = False, False
                prev_iter = None
            elif case1_flag:
                if i == 0 and prev_iter == 'Allocation type':
                    split_cell = cell.split(' 0x', maxsplit=1)
                    one_page_dicts.append({
                        'allocation_type': split_cell[0],
                        'uuid': '0x' + split_cell[1][:4],
                        'name': split_cell[1][5:] # split_cell[1] looks like 'FCE1 Sony Group Corporation'
                    })
                    prev_iter = 'Allocation type'
                elif re.search('^0[xX][0-9A-F]{4}', cell):
                    if prev_iter == 'Allocation type':
                        i = 1
                    
                    cell = '0x' + cell[2:]
                    one_page_dicts[i]['uuid'] = cell[:6] # cell looks like: '0xFE91 Shanghai Imilab Technology Co.,Ltd'
                    one_page_dicts[i]['name'] = cell[7:]
                    prev_iter = 'uuid name'
                elif prev_iter == 'Allocation type':
                    one_page_dicts.append({ 'allocation_type': cell })

                i += 1
            elif case2_flag:
                # if cell == 'Allocation type':
                #     i, prev_iter = 0, 'Allocation type'
                if cell == 'Allocated UUID':
                    i, prev_iter = 0, 'Allocated UUID'
                elif cell == 'Allocated for':
                    i, prev_iter = 0, 'Allocated for'
                elif prev_iter == 'Allocation type':
                    one_page_dicts.append({ 'allocation_type': cell })
                    i += 1
                elif prev_iter == 'Allocated UUID':
                    cell = '0x' + cell[2:]
                    one_page_dicts[i]['uuid'] = cell
                    i += 1
                elif prev_iter == 'Allocated for':
                    one_page_dicts[i]['name'] = cell
                    i += 1

    all_rows_dicts.extend(one_page_dicts)
    result = dict()
    for row in all_rows_dicts:
        print(row)
        result[row['uuid']] = {
            'allocation_type': row['allocation_type'],
            'name': row['name']
        }

    return result

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
    loaded_data_dict = load_csv_to_dict('uuid_data_all.csv')
    write_dict_to_csv(loaded_data_dict)
    print(loaded_data_dict)