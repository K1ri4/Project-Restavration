import serial
import os
import time
import math
import win10toast

toaster = win10toast.ToastNotifier()

def printProgressBar(progress,maxProgress,leng=40,prog='+',bar='=',mpty='-'):
    num = str(progress)+"/"+str(maxProgress)
    barS = bar*math.floor(progress/maxProgress*leng-1)+prog
    print(num+" "*(len(str(maxProgress))*2+1-len(str(num)))+" ["+barS+mpty*(leng-len(barS))+"]",end='\r')

with open('config.txt', 'r') as file:
    prom = file.read().split('\n')
    debug = int(prom[0].strip())
    notif = int(prom[1].strip())
    file.close()

try:
    if notif:
        # plyer.notification.notify(message=f'Товсь!', app_name='Restoration_project', title='Подготовка к передаче...')
        toaster.show_toast("Подготовка к передаче...", "Товсь!")
    else:
        print("Товь! Подготовка к передаче...")

    with open('com.txt', 'r') as file:
        COMn = file.read().strip()
        file.close()

    with open('speed.txt', 'r') as file:
        baud = int(file.read().strip())
        file.close()

    with open('send.txt', 'r') as file:
        filePath = file.read().strip()
        file.close()

    ser = serial.Serial(COMn, baudrate=baud)
    ser.write(b'?')
    resp = ser.read()
    if(resp == b'!'):
        print("Ready to transmit")
        # if notif: plyer.notification.notify(message=f'Устройство-передатчик отправило запрос успешно', app_name='Restoration_project', title='Передача данных начата')
        toaster.show_toast("Передача данных начата", "Устройство-передатчик отправило запрос успешно")
    else:
        print(resp, "... Strange... But ok.")
        # if notif: plyer.notification.notify(message=f'Устройство-передатчик отправило странный запрос...', app_name='Restoration_project', title='Передача данных начата')
        toaster.show_toast("Передача данных начата", "Устройство-передатчик отправило странный запрос...")

    fileName = filePath[filePath.rfind('\\')+1:]
    print(f"Передача файла {filePath} началась")
    ser.write(bytes(fileName + ":", 'utf-8'), )
    file = open(filePath, 'rb')
    data = file.read()
    fileSize = len(data)
    fileSizeBytes = [0, 0, 0, 0]
    for i in range(4):
        fileSizeBytes[3-i] = ((fileSize-1) >> i*8) & 0xFF
    time.sleep(2)
    ser.write(bytes(fileSizeBytes))
    for n in range(fileSize):
        ser.write(int.to_bytes(data[n], 1, 'little'))
        printProgressBar(n, fileSize)
        if debug: print('sended', data[n])
    print('\n', n, 'bytes transmited from file', fileName)
    file.close()

    # if notif: plyer.notification.notify(message=f'Файл {filePath} успешно отправлен', app_name='Restoration_project', title='Ваш файл успешно отправлен')
    toaster.show_toast("Ваш файл успешно отправлен", f'Файл {filePath} успешно отправлен')
    print(f'Файл {filePath} успешно отправлен')

    try:
        os.remove(os.getcwd() + '\\' + 'send.txt')
    except:
        if debug: print("Error during removing file")

    ser.close()
except:
    if notif: 
        toaster.show_toast("Ваш файл успешно отправлен", f'Файл {filePath} успешно отправлен')
    else:
        print("TX error")
