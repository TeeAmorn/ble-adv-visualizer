import json


def parse(readfile, writefile):

    with open(readfile, mode='r') as rf, open(writefile, mode='w') as wf:
        opened_ad = False
        count = 0
        for line in rf:
            if line == '          "btcommon.eir_ad.advertising_data": {\n':
                wf.write(line)
                opened_ad = True
            elif opened_ad and line == '            "btcommon.eir_ad.entry": {\n':
                wf.write('            "' + str(count) + '": {\n')
                count += 1
            elif opened_ad and (line == '          }\n' or line == '          },\n'):
                wf.write(line)
                count = 0
                opened_ad = False
            else:
                wf.write(line)


parse('raw.json', 'raw_parsed.json')
