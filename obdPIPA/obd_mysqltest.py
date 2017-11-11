#PA 11.11.2017
#First test of python OBD library + mysql server functionality in Raspberry

#TODO: Exit from loop when serial connection is lost or "something else" happens

import obd
import datetime
import mysql.connector
from time import sleep

#First param is the RFCOMM port (e.g. '/dev/rfcomm0') and second is baud rate
#None is the default and performs automatic lookup of serial connection (bluetooth/usb)
#9600 works as the baud rate at least for obdSIM

#The port should be changed according to environment
#COM5 works locally with --> obdsim.exe -w COM4
c = obd.OBD('/dev/rfcomm5', 9600)
print(c.status())

#Queries to be submitted to ECU periodically
queries = [
obd.commands.RPM,
obd.commands.ENGINE_LOAD,
obd.commands.SPEED]

#initialize db connection
usr = 'panu'
pw = 'panu'
db = 'obdlogger'

cnx = mysql.connector.connect(user=usr, password=pw, database=db)
cur = cnx.cursor()

db_query = ("INSERT into Entry (DeviceID, RPM, Calc_load, Speed) VALUES ({0}, {1}, {2}, {3})")


#-----------MAIN LOOP-----------------
#Need to be changed to a while with conditional exit (connection lost/ignition power off)
while True:
  r = []
  
  for q in queries:
    res = c.query(q)

    #'None' values not saved!
    if not res.is_null():
      r.append(res.value.magnitude)
    else:
      r.append(-99)
  
  #debug
  print(r)
  
  #Commit ECU query results to db
  cur.execute(db_query.format(1, r[0], r[1], r[2]))
  cnx.commit()
  
  #Set the read interval in seconds
  sleep(5)

