#PA 5.11.2017
#First test of python OBD library

#TODO: Exit from loop when serial connection is lost or "something else" happens

import obd
from time import sleep

#First param is the RFCOMM port (e.g. '/dev/rfcomm0') and second is baud rate
#None is the default and performs automatic lookup of serial connection (bluetooth/usb)
#9600 works as the baud rate at least for obdSIM
connection = obd.OBD(None, 9600)
print(connection.status())

fl = open('output.csv', 'w')

#Just some random stuff for testing
#Need to be changed to a while with conditional exit (connection lost/ignition power off)
for i in range(0, 1000):
  r = connection.query(obd.commands.RPM)
  v = connection.query(obd.commands.ENGINE_LOAD)
  f = connection.query(obd.commands.SPEED)
  d = connection.query(obd.commands.INTAKE_PRESSURE)
  h = connection.query(obd.commands.COOLANT_TEMP)
  
  print(i, str(r.value) , str(v.value), str(d.value), str(h.value))
  fl.write(str(i)+','+str(r.value)+','+str(v.value)+','+str(d.value)+','+str(h.value))
  
  #Set the read interval in seconds
  sleep(5)

#Need to change this to periodically flush the changes to outputfile
fl.close()