from database import cursor, db
import datetime


def add_packet(pdu_type, timestamp, epoch, src_addr, dst_addr, rssi):
    if dst_addr is None:
        query = (
            "INSERT INTO one(type, timestamp, epoch, src_addr, dst_addr, rssi) VALUES (%s, %s, %s, %s, NULL, %s)")
        cursor.execute(query, (pdu_type, timestamp,
                       epoch, src_addr, rssi))
    else:
        query = (
            "INSERT INTO one(type, timestamp, epoch, src_addr, dst_addr, rssi) VALUES (%s, %s, %s, %s, %s, %s)")
        cursor.execute(query, (pdu_type, timestamp,
                       epoch, src_addr, dst_addr, rssi))
    db.commit()
    packet_id = cursor.lastrowid
    print("Added packet {}".format(packet_id))


def parse_time(time):
    return datetime.datetime.strptime(
        time, '%b %d, %Y %H:%M:%S.%f000 CDT').strftime('%Y-%m-%d %H:%M:%S')


# time = 'May 16, 2022 15:44:41.030922000 CDT'
# dt = datetime.datetime.strptime(
#     time, '%b %d, %Y %H:%M:%S.%f000 CDT').strftime('%Y-%m-%d %H:%M:%S')
# add_packet('ADV_IND', dt, '0.052304000', '0d:02:13:87:70:9f', None, '-83')
