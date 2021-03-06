import mysql.connector
from mysql.connector import errorcode
from database import cursor

DB_NAME = 'demo'

TABLES = {}

for name in ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten']:
    TABLES[name] = (
        "CREATE TABLE `" + name + "` ("
        "`id` int(11) NOT NULL AUTO_INCREMENT,"
        "`type` varchar(20) NOT NULL,"
        "`timestamp` datetime NOT NULL,"
        "`epoch` double(10, 5) NOT NULL,"
        "`src_addr` varchar(17) NOT NULL,"
        "`dst_addr` varchar(17),"
        "`rssi` int(4) NOT NULL,"
        "`appearance_category` varchar(100),"
        "`appearance_subcategory` varchar(100),"
        "`service_class` varchar(100),"
        "`service_data` varchar(100),"
        "`device_name` varchar(40),"
        "`power_level` int(3),"
        "`manufacturer_specific_data` varchar(100),"
        "PRIMARY KEY (`id`)"
        ") ENGINE=InnoDB"
    )


def create_database():
    cursor.execute(
        "CREATE DATABASE IF NOT EXISTS {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    print("Database {} created!".format(DB_NAME))


def create_tables():
    cursor.execute("USE {}".format(DB_NAME))
    for table_name in TABLES:
        table_description = TABLES[table_name]
        try:
            print("Creating table ({})\n".format(table_name), end="")
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("Already Exists")
            else:
                print(err.msg)


create_database()
create_tables()
