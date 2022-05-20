import json
from dbtools import add_packet, parse_time
import multiprocessing

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

    # Check if packet is malformed
    if "_ws.malformed" in layers:
        return None

    # Obtain specific layers
    frame = layers['frame']
    nordic_ble = layers['nordic_ble']
    btle = layers['btle']

    # Packet Info
    timestamp = parse_time(frame['frame.time'])
    epoch = frame['frame.time_relative']
    channel = nordic_ble['nordic_ble.channel']
    rssi = nordic_ble['nordic_ble.rssi']

    # PDU Type
    pdu_type_hex = btle['btle.advertising_header_tree']['btle.advertising_header.pdu_type']

    # Populate fields based on PDU type
    if pdu_type_hex == PDU_ADV_IND:
        pdu = 'ADV_IND'
        src_addr = btle['btle.advertising_address']
        dst_addr = None
    elif pdu_type_hex == PDU_SCAN_REQ:
        pdu = 'SCAN_REQ'
        src_addr = btle['btle.scanning_address']
        dst_addr = btle['btle.advertising_address']
    elif pdu_type_hex == PDU_SCAN_RSP:
        pdu = 'SCAN_RSP'
        src_addr = btle['btle.advertising_address']
        dst_addr = None
    # Ignore these for now
    elif pdu_type_hex == PDU_ADV_DIRECT_IND:
        pdu = 'ADV_DIRECT_IND'
        target_address = btle['btle.target_address']
        return
    elif pdu_type_hex == PDU_ADV_NONCONN_IND:
        pdu = 'ADV_NONCONN_IND'
        return
    elif pdu_type_hex == PDU_CONNECT_REQ:
        pdu = 'CONNECT_REQ'
        initiator_address = btle['btle.initiator_address']
        return
    elif pdu_type_hex == PDU_ADV_SCAN_IND:
        pdu = 'ADV_SCAN_IND'
        return
    else:
        return

    # Return arguments to add_packet as a tuple
    return (pdu, timestamp, epoch, src_addr, dst_addr, rssi)


def parse_and_add_entry(entry):
    parsed = parse_entry(entry)
    if parsed is not None:
        add_packet(*parsed)


if __name__ == "__main__":
    data = load_raw('raw.json')
    # pool = multiprocessing.Pool()
    # pool.map(parse_and_add_entry, data)
    print('DONE')
