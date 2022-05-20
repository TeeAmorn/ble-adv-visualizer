import mysql.connector

config = {
    'user': 'root',
    'password': 'password',
    'host': 'localhost',
    'database': 'demo'
}

db = mysql.connector.connect(**config)
cursor = db.cursor()
