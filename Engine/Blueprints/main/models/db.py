import mysql.connector
import sys

def connect():
    connection=None
    connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="drs_banka"
                )
    return connection