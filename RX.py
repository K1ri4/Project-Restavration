import serial
import os

debug = 0

with open('com.txt', 'r') as file:
    COMn = file.read().strip()
    file.close()

with open('speed.txt', 'r') as file:
    baud = file.read().strip()
    file.close()

ser = serial.Serial(COMn, baudrate=baud)

req = ser.read()
if(req == b'?'):
    if debug: print("Ready to recieve")
else:
    if debug: print(req, "... Strange... But ok.")
ser.write(b'!')

fileName = ser.read_until(b':')[:-1]
if debug: print(fileName.decode(), os.listdir())
if fileName.decode() in os.listdir():
    if debug: print(f'note: file {fileName.decode()} already exist, rewriting')
    os.remove(fileName.decode())
file = open(fileName.decode(), 'ab')
rBytes = ser.read(4)
fileSize = 0

for i in range(4):
    fileSize += rBytes[3-i] << (8 * i)
if debug: print(f'recieving {fileSize} bytes to file {fileName}, please wait...')
for n in range(fileSize+1):
    promBufer = ser.read()
    file.write(promBufer)
    if debug: print(promBufer)
if debug: print(n, 'bytes recieved, writed to file', fileName)
file.close()

with open('get.txt', 'w') as file:
    file.write(os.getcwd() + '\\' + fileName)
    file.close()

ser.close()
