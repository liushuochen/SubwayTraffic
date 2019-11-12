import mysql.connector

if __name__ == '__main__':
    mysql_db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="122510",
        database="subway"
    )

    mycursor = mysql_db.cursor()

    mycursor.execute("SELECT * FROM user")

    myresult = mycursor.fetchall()
    print(myresult)