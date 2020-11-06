import mysql.connector

cnx = mysql.connector.connect(user='root', password='aksjhs',
                              host='localhost',
                              database='emr2')
cur = cnx.cursor()

cur.execute("SELECT * FROM EMR_Provider")
row = cur.fetchone()
print(row)
cnx.close()