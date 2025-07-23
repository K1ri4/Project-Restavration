import serial
import os
import math
import win10toast

toaster = win10toast.ToastNotifier()

def printProgressBar(progress,maxProgress,leng=40,prog='+',bar='=',mpty='-'):
    num = str(progress)+"/"+str(maxProgress)
    barS = bar*math.floor(progress/maxProgress*leng-1)+prog
    print(num+" "*(len(str(maxProgress))*2+1-len(str(num)))+" ["+barS+mpty*(leng-len(barS))+"]",end='\r')

with open('config.txt', 'r') as file:
    prom = file.read().strip().split('\n')
    debug = int(prom[0].strip())
    notif = int(prom[1].strip())
    file.close()

try:
    if notif:
        # plyer.notification.notify(message=f'Товсь!', app_name='Restoration_project', title='Подготовка к приёму...')
        toaster.show_toast("Подготовка к приёму...", "Товсь!")
    else:
        print("Товь! Подготовка к приёму...")

    with open('com.txt', 'r') as file:
        COMn = file.read().strip()
        file.close()

    with open('speed.txt', 'r') as file:
        baud = int(file.read().strip())
        file.close()

    ser = serial.Serial(COMn, baudrate=baud)

    req = b""
    while(req != b'?'):
        req = ser.read()
    print("Ready to recieve")
    ser.write(b'!')

    fileName = ser.read_until(b':')[:-1]
    toGetFile = os.getcwd() + '\\' + fileName.decode()
    print(f"Приём файла {toGetFile} начался")
    if debug: print(fileName.decode(), os.listdir())
    if fileName.decode() in os.listdir():
        if debug: print(f'note: file {fileName.decode()} already exist, rewriting')
        os.remove(fileName.decode())
    file = open(fileName.decode(), 'ab')
    rBytes = ser.read(4)
    fileSize = 0

    for i in range(4):
        fileSize += rBytes[3-i] << (8 * i)
    if debug: print(f'recieving {fileSize} bytes to file {toGetFile}, please wait...')
    for n in range(fileSize+1):
        # promBufer = 
        file.write(ser.read())
        printProgressBar(n, fileSize)
        # if debug: print(promBufer)
    print('\n', n, 'bytes recieved, writed to file', toGetFile)
    file.close()

    with open(os.getcwd() + '\\' + 'get.txt', 'w') as file:
        file.write(toGetFile)
        file.close()

    if notif: 
        plyer.notification.notify(message=f'Он сохранён в {fileName}', app_name='Restoration_project', title='Файл успешно принят')
    else:
        print(f'Он сохранён в {toGetFile}')

    ser.close()
except:
    if notif: 
        plyer.notification.notify(message='=(', app_name='Restoration_project', title='Что-то пошло не так! (RX)')
    else:
        print("RX error")
