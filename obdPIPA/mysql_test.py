import mysql.connector

cnx = mysql.connector.connect(user='panu', password='panu', database='obdlogger')
c = cnx.cursor()

query = ("SELECT * FROM Entry")

c.execute(query)

for e in c:
    print(e)
