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
obd.commands.RPM,
obd.commands.ENGINE_LOAD,
obd.commands.SPEED,
obd.commands.SHORT_FUEL_TRIM_1,
obd.commands.LONG_FUEL_TRIM_1,
obd.commands.INTAKE_TEMP,
obd.commands.MAF,
obd.commands.FUEL_LEVEL,
obd.commands.AMBIANT_AIR_TEMP,
obd.commands.FUEL_RATE,
obd.commands.FUEL_STATUS,
obd.commands.COOLANT_TEMP,
obd.commands.SHORT_FUEL_TRIM_2,
obd.commands.LONG_FUEL_TRIM_2,
obd.commands.FUEL_PRESSURE,
obd.commands.INTAKE_PRESSURE,
obd.commands.TIMING_ADVANCE,
obd.commands.THROTTLE_POS,
obd.commands.AIR_STATUS,
obd.commands.O2_SENSORS,
obd.commands.RUN_TIME,
obd.commands.DISTANCE_W_MIL,
obd.commands.FUEL_RAIL_PRESSURE_VAC,
obd.commands.FUEL_RAIL_PRESSURE_DIRECT,
obd.commands.BAROMETRIC_PRESSURE,
obd.commands.RELATIVE_THROTTLE_POS,
obd.commands.THROTTLE_POS_C,
obd.commands.ACCELERATOR_POS_D,
obd.commands.ACCELERATOR_POS_E,
obd.commands.ACCELERATOR_POS_F,
obd.commands.THROTTLE_ACTUATOR,
obd.commands.MAX_MAF,
obd.commands.FUEL_TYPE,
obd.commands.ETHANOL_PERCENT,
obd.commands.FUEL_RAIL_PRESSURE_ABS,
obd.commands.RELATIVE_ACCEL_POS,
obd.commands.OIL_TEMP,
obd.commands.FUEL_INJECT_TIMING]

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
      r.append(str(res.value.magnitude))
      fl.write(str(res.value.magnitude)+',')
    else:
      r.append('null')
      fl.write('null,')
  
  #debug
  print(r)
  
  #Save changes to file on every iteration?
  fl.write('\n')
  fl.flush()
  
  #Set the read interval in seconds
  sleep(1)

fl.close()
