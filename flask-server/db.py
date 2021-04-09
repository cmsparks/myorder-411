import mysql.connector

def db_conn():
    mydb = mysql.connector.connect(
        host= "34.67.0.57",
        user= "root",
        password= "1234",
        database = "one_data"
    )

    mycursor = mydb.cursor()

    return mydb, mycursor
