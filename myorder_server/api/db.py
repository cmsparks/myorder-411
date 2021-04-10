import mysql.connector
from threading import Thread, Lock

conn = mysql.connector.connect(
    host= "34.67.0.57",
    user= "root",
    password= "1234",
    database = "one_data"
)

cursor = conn.cursor()

mutex = Lock()

def db_acq_lock():
    mutex.acquire()
    return conn, cursor

def db_rel_lock():
    mutex.release()
