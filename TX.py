import serial

debug = 0

with open('com.txt', 'r') as file:
    COMn = file.read().strip()
    file.close()

with open('speed.txt', 'r') as file:
    baud = file.read().strip()
    file.close()

ser = serial.Serial(COMn, baudrate=baud)
ser.write(b'?')
resp = ser.read()
if(resp == b'!'):
    if debug: print("Ready to transmit")
else:
    if debug: print(resp, "... Strange... But ok.")

with open('send.txt', 'r') as file:
    filePath = file.read().strip()
    file.close()

fileName = filePath[filePath.rfind('\\')+1:]
ser.write(bytes(fileName + ":", 'utf-8'), )
file = open(filePath, 'rb')
data = file.read()
fileSize = len(data)
fileSizeBytes = [0, 0, 0, 0]
for i in range(4):
    fileSizeBytes[3-i] = ((fileSize-1) >> i*8) & 0xFF
ser.write(bytes(fileSizeBytes))
for n in range(fileSize):
    ser.write(int.to_bytes(data[n], 1, 'little'))
    if debug: print('sended', data[n])
print(n, 'bytes transmited from file', fileName)
file.close()

ser.close()
