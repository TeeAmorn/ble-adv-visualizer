import json

# Constants
PDU_ADV_IND = "0x00"
PDU_ADV_DIRECT_IND = "0x01"
PDU_ADV_NONCONN_IND = "0x02"
PDU_SCAN_REQ = "0x03"
PDU_SCAN_RSP = "0x04"
PDU_CONNECT_REQ = "0x05"
PDU_ADV_SCAN_IND = "0x06"


def load_raw(filename):
    with open(filename) as file:
        data = json.load(file)
    return data


def parse_entry(entry):

    # Layers
    layers = entry['_source']['layers']
    frame = layers['frame']
    nordic_ble = layers['nordic_ble']
    btle = layers['btle']

    # Packet Info
    packet_id = frame['frame.number']
    time = frame['frame.time']
    channel = nordic_ble['nordic_ble.channel']
    rssi = nordic_ble['nordic_ble.rssi']
    access_address = btle['btle.access_address']

    # PDU Type
    pdu_type_hex = btle['btle.advertising_header_tree']['btle.advertising_header.pdu_type']

    # Populate fields based on PDU type
    if pdu_type_hex == PDU_ADV_IND:
        pdu = 'PDU_ADV_IND'
        advertising_address = btle['btle.advertising_address']
    elif pdu_type_hex == PDU_ADV_DIRECT_IND:
        pdu = 'PDU_ADV_DIRECT_IND'
        advertising_address = btle['btle.advertising_address']
        target_address = btle['btle.target_address']
    elif pdu_type_hex == PDU_ADV_NONCONN_IND:
        pdu = 'PDU_ADV_NONCONN_IND'
        advertising_address = btle['btle.advertising_address']
    elif pdu_type_hex == PDU_SCAN_REQ:
        pdu = 'PDU_SCAN_REQ'
        advertising_address = btle['btle.advertising_address']
        scanning_address = btle['btle.scanning_address']
    elif pdu_type_hex == PDU_SCAN_RSP:
        pdu = 'PDU_SCAN_RSP'
        advertising_address = btle['btle.advertising_address']
    elif pdu_type_hex == PDU_CONNECT_REQ:
        pdu = 'PDU_CONNECT_REQ'
        advertising_address = btle['btle.advertising_address']
        initiator_address = btle['btle.initiator_address']
    elif pdu_type_hex == PDU_ADV_SCAN_IND:
        pdu = 'PDU_ADV_SCAN_IND'
        advertising_address = btle['btle.advertising_address']
    else:
        return None

    # Data
    access_address = btle["btle.access_address"]
    advertising_address = btle["btle.advertising_address"]


if __name__ == "__main__":
    data = load_raw('raw.json')
    print('DONE')
