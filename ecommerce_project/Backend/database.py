import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='123456789',
        database='ecommerce_db'
    )
