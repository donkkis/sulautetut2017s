#PA 2017
#First test of python OBD library + mysql server functionality in Raspberry

import obd
import datetime
import mysql.connector
from time import sleep
from subprocess import call
from gps3.agps3threaded import AGPS3mechanism

#----------Initialize GPS receiver-----------
agps_thread = AGPS3mechanism()
agps_thread.stream_data()
agps_thread.run_thread()

#---------Initialize ELM327------------------
#First param is the RFCOMM port (e.g. '/dev/rfcomm0') and second is baud rate
#None is the default and performs automatic lookup of serial connection (bluetooth/usb)
#9600 works as the baud rate at least for obdSIM

#The port should be changed according to environment
#COM5 works locally with --> obdsim.exe -w COM4
c = obd.OBD('/dev/rfcomm1', 9600)
print(c.status())

#Queries to be submitted to ECU periodically
queries = [
obd.commands.RPM,
obd.commands.ENGINE_LOAD,
obd.commands.SPEED]

#initialize db connection (potentially unsafe!)
usr = 'panu'
pw = 'panu'
db = 'obdlogger'
h = '212.149.236.220'

cnx = mysql.connector.connect(host = h, user=usr, password=pw, database=db)
cur = cnx.cursor()

db_query = ("INSERT into Entry (DeviceID, RPM, Calc_load, Speed, GPS_Lat, GPS_Long) VALUES ({0}, {1}, {2}, {3}, {4}, {5})")

#initialize for conditional stopping
exit_count = 0

#set query interval globally
interval = 10

#shutdown latency in seconds
ttl = 60

#-----------MAIN LOOP-----------------
#Aqcuire data from target with conditional exit -> connection lost/ignition power off
while True:
#while exit_count < (ttl/interval):
  r = []
  c_status = c.status()

  #check exit conditions
  #-ELM327 connection down
  #-TODO Engine not running
  if c_status == "Not Connected":
    exit_count += 1
    print("Waiting " + str(ttl/interval -  exit_count) + " seconds for reconnection...")

  if c_status == "Car Connected":

    for q in queries:
      res = c.query(q)

      #'None' values not saved!
      if not res.is_null():
        r.append(res.value.magnitude)
      else:
        r.append(-99)

    #add GPS coordinates
    r.append(agps_thread.data_stream.lat)
    r.append(agps_thread.data_stream.lon)

    #debug
    print(r)

    #Commit ECU query results to db
    #GPS is only for simulation at this point
    if r[3] == "n/a" or r[4] == "n/a":
      cur.execute(db_query.format(1, r[0], r[1], r[2], 0, 0))
    else:
      cur.execute(db_query.format(1, r[0], r[1], r[2], r[3], r[4]))
    cnx.commit()
 
  sleep(interval)

print("No connection, stopping main loop.\nMain loop stopped")

#Will power off the system
#Keep commented for developement
#call("sudo shutdown -h now", shell=True)
