from collections import namedtuple
from database import cursor, db
import datetime

PacketInfo = namedtuple(
    "PacketInfo", "pdu timestamp epoch src_addr dst_addr rssi device_name service_class service_data appearance_category appearance_subcategory power manufacturer")


def add_packet(info, tablename):
    query = "INSERT INTO " + tablename + "(type, timestamp, epoch, src_addr, dst_addr, rssi, device_name, service_class, service_data, appearance_category, appearance_subcategory, power_level, manufacturer_specific_data) VALUES ("
    query += 'NULL, ' if info.pdu is None else "'" + info.pdu + "', "
    query += 'NULL, ' if info.timestamp is None else "'" + info.timestamp + "', "
    query += 'NULL, ' if info.epoch is None else "'" + info.epoch + "', "
    query += 'NULL, ' if info.src_addr is None else "'" + info.src_addr + "', "
    query += 'NULL, ' if info.dst_addr is None else "'" + info.dst_addr + "', "
    query += 'NULL, ' if info.rssi is None else "'" + info.rssi + "', "
    query += 'NULL, ' if info.device_name is None else "'" + info.device_name + "', "
    query += 'NULL, ' if info.service_class is None else "'" + info.service_class + "', "
    query += 'NULL, ' if info.service_data is None else "'" + info.service_data + "', "
    query += 'NULL, ' if info.appearance_category is None else "'" + \
        info.appearance_category + "', "
    query += 'NULL, ' if info.appearance_subcategory is None else "'" + \
        info.appearance_subcategory + "', "
    query += 'NULL, ' if info.power is None else "'" + info.power + "', "
    query += 'NULL)' if info.manufacturer is None else "'" + info.manufacturer + "')"
    cursor.execute(query)
    db.commit()
    packet_id = cursor.lastrowid
    print("Added packet {}".format(packet_id))


def parse_time(time):
    return datetime.datetime.strptime(
        time, '%b %d, %Y %H:%M:%S.%f000 CDT').strftime('%Y-%m-%d %H:%M:%S')
