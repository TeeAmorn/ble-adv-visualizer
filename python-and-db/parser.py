from ast import parse
import json
from dbtools import add_packet, parse_time, PacketInfo
import multiprocessing

# Constants

# PDU
PDU_ADV_IND = "0x00"
PDU_ADV_DIRECT_IND = "0x01"
PDU_ADV_NONCONN_IND = "0x02"
PDU_SCAN_REQ = "0x03"
PDU_SCAN_RSP = "0x04"
PDU_CONNECT_REQ = "0x05"
PDU_ADV_SCAN_IND = "0x06"

# AD TYPES
AD_TYPE_DEVICE_NAME = "0x09"
AD_TYPE_SERVICE_DATA = "0x16"
AD_TYPE_APPEARANCE = "0x19"
AD_TYPE_POWER_LEVEL = "0x0a"
AD_TYPE_MANUFACTURER_SPECIFIC_DATA = "0xff"


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

    # Initialize default values
    pdu = timestamp = epoch = src_addr = dst_addr = \
        rssi = device_name = service_data = appearance = \
        power = manufacturer = None

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

    if 'btcommon.eir_ad.advertising_data' in btle:
        advertising_data = btle['btcommon.eir_ad.advertising_data']
        for i in range(10):
            if str(i) not in advertising_data:
                break
            ad = advertising_data[str(i)]
            if ad["btcommon.eir_ad.entry.type"] == AD_TYPE_DEVICE_NAME:
                device_name_id = ad["btcommon.eir_ad.entry.device_name"]
                device_name = None
            if ad["btcommon.eir_ad.entry.type"] == AD_TYPE_SERVICE_DATA:
                service_data = ad["btcommon.eir_ad.entry.uuid_16"]
            if ad["btcommon.eir_ad.entry.type"] == AD_TYPE_APPEARANCE:
                appearance = ad["btcommon.eir_ad.entry.appearance"]
            if ad["btcommon.eir_ad.entry.type"] == AD_TYPE_POWER_LEVEL:
                power = ad["btcommon.eir_ad.entry.power_level"]
            if ad["btcommon.eir_ad.entry.type"] == AD_TYPE_MANUFACTURER_SPECIFIC_DATA:
                manufacturer = ad["btcommon.eir_ad.entry.company_id"]

    # print(json.dumps(btle, indent=4, sort_keys=True))
    return PacketInfo(pdu, timestamp, epoch, src_addr, dst_addr, rssi, device_name, service_data, appearance, power, manufacturer)


def parse_and_add_entry(entry):
    packet_info = parse_entry(entry)
    if packet_info is not None:
        add_packet(packet_info)


if __name__ == "__main__":
    data = load_raw('raw_parsed.json')
    pool = multiprocessing.Pool()
    pool.map(parse_and_add_entry, data)
    # pool.map(parse_entry, data)
    # print(parse_entry(data[0]))
    print('DONE')
