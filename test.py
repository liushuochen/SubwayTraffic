import mysql.connector

if __name__ == '__main__':
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="122510",
    )

    cursor = db.cursor()
    cursor.execute("create database demo999 charset utf8")