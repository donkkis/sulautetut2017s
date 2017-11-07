#PA 5.11.2017
#First test of python OBD library

#TODO: Exit from loop when serial connection is lost or "something else" happens

import obd
import datetime
from time import sleep

#First param is the RFCOMM port (e.g. '/dev/rfcomm0') and second is baud rate
#None is the default and performs automatic lookup of serial connection (bluetooth/usb)
#9600 works as the baud rate at least for obdSIM

#The port should be changed according to environment
#COM5 works locally with --> obdsim.exe -w COM4
c = obd.OBD('/dev/rfcomm1', 9600)
print(c.status())

#outputfile
fl = open('output_' + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")+ '.csv', 'w')

#Queries to be submitted to ECU periodically
queries = [
obd.commands.PIDS_A,
obd.commands.PIDS_B,
obd.commands.PIDS_C,
obd.commands.MIDS_A,
obd.commands.MIDS_B,
obd.commands.MIDS_C,
obd.commands.MIDS_D,
obd.commands.MIDS_E,
obd.commands.MIDS_F]

#initialize outputfile with column headers
fl.write('TIMESTAMP,')
for q in queries:
  fl.write(q.name+',')
fl.write('\n')
  
#Just some random stuff for testing
#Need to be changed to a while with conditional exit (connection lost/ignition power off)
while True:
  r = []

  r.append(str(datetime.datetime.now()))
  fl.write(str(datetime.datetime.now())+',')
  
  for q in queries:
    res = c.query(q)

    #'None' values not saved!
    if not res.is_null():
      r.append(str(res.value))
      fl.write(str(res.value)+',')
    else:
      r.append('null')
      fl.write('null,')
  
  #debug
  print(r)
  
  #Save changes to file on every iteration?
  fl.write('\n')
  fl.flush()
  
  #Set the read interval in seconds
  sleep(5)

fl.close()
