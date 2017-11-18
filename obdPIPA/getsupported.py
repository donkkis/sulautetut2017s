import obd
c = obd.OBD('dev/rfcomm1', 9600)
print(c.status())
for i in c.supported_commands:
  print(str(i)+'\n')
