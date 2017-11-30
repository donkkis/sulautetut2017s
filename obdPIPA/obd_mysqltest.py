#PA 2017
#First test of python OBD library + mysql server functionality in Raspberry

import obd
import datetime
import mysql.connector
import urllib2
from time import sleep
from subprocess import call
from gps3.agps3threaded import AGPS3mechanism

def main():
  #---------------------INIT------------------------
  #Initialize GPS receiver
  agps_thread = AGPS3mechanism()
  agps_thread.stream_data()
  agps_thread.run_thread()

  #Initialize ELM327
  #First param is the RFCOMM port (e.g. '/dev/rfcomm0') and second is baud rate
  #None is the default and performs automatic lookup of serial connection (bluetooth/usb)
  #9600 works as the baud rate at least for obdSIM

  #The port should be changed according to environment
  #COM5 works locally with --> obdsim.exe -w COM4
  port = '/dev/rfcomm1'
  baud_rate = 9600
  c = wait_for_obd(port, baud_rate)
  print(c.status())

  #Queries to be submitted to ECU periodically
  queries = [
  obd.commands.RPM,
  obd.commands.ENGINE_LOAD,
  obd.commands.SPEED,
  obd.commands.FUEL_LEVEL,
  obd.commands.DISTANCE_SINCE_DTC_CLEAR]

  #initialize db connection (potentially unsafe!)
  usr = 'panu'
  pw = ''
  db = 'obdlogger'
  h = ''

  wait_for_connection()

  cnx = mysql.connector.connect(host = h, user=usr, password=pw, database=db)
  cur = cnx.cursor()

  db_query = ("INSERT into Entry (DeviceID, RPM, Calc_load, Speed, Fuel_level, Distance, GPS_Lat, GPS_Long) VALUES ({0}, {1}, {2}, {3}, {4}, {5}, {6}, {7})")

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

    #check exit conditions
    #-ELM327 connection down
    #-TODO Engine not running
    #-TODO DB connection lost

    wait_for_connection()

    #delete this!!
    if 1==1:

      for q in queries:
        try:
          res = c.query(q)
        except:
          c = wait_for_obd(port, baud_rate)
          print(c.status())
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

      wait_for_connection()

      try:
        if r[5] == "n/a" or r[6] == "n/a":
          cur.execute(db_query.format(1, r[0], r[1], r[2], r[3], r[4], 0, 0))
        else:
          cur.execute(db_query.format(1, r[0], r[1], r[2], r[3], r[4], r[5], r[6]))
        cnx.commit()
      except mysql.connector.Error as e:
        print("No connection to db, dropping data. Message: ", e.msg)
 
    sleep(interval)

  print("No connection, stopping main loop.\nMain loop stopped")

  #Will power off the system
  #Keep commented for developement
  #call("sudo shutdown -h now", shell=True)

def wait_for_connection():
  waiting = 0
  while True:
    try:
      response = urllib2.urlopen('http://xxx.xxx.xxx.xxx:7777',timeout=5)
      return
    except urllib2.URLError:
      if waiting == 0:
        waiting = 1
        print("Waiting for network...")
      pass

def wait_for_obd(port, baud_rate):
  waiting = 0
  while True:
    try:
      c = obd.OBD(port, baud_rate)
      return c
    except:
      if waiting == 0:
        waiting = 1
        print("Waiting for OBD connection...")
      pass

if __name__ == "__main__":
  main()
