import time
import serial
import keyboard
import win10toast
import os

# username = "Robert"
username = input("Please, enter your username: ").strip().capitalize()
end = 0

os.system('cls')

toaster = win10toast.ToastNotifier()

reading = 0

with open('com.txt', 'r') as file:
    COMn = file.read().strip()
    file.close()

with open('speed.txt', 'r') as file:
    baud = int(file.read().strip())
    file.close()

with open('chat.txt', 'r') as file:
    chatHistory = file.read().strip().split('\n')
    file.close()

ser = serial.Serial(COMn, baudrate=baud)

keyb_buff = ""

def updateInput():
    print(Colors.LIGHT_PURPLE + " >>> " + keyb_buff + Colors.LIGHT_WHITE, end='    \r')

def sendMessage():
    global keyb_buff
    message = Colors.BLUE + "(" + getTime() + ") " + Colors.LIGHT_BLUE + username + ": " + Colors.LIGHT_WHITE + keyb_buff
    txtmsg = "(" + getTime() + ") " + username + ": " + keyb_buff
    ser.write(b'!')
    req = b''
    while (req != b'?'):
        req = ser.read()
    ser.write(bytes(txtmsg + '\n', 'utf-8'))
    chatHistory.append(txtmsg)
    print(message)
    keyb_buff = ""
    updateInput()

def on_prs(key):
    global keyb_buff
    global end
    # print(f'Нажата клавиша {key.name}')
    if(len(key.name) == 1):
        keyb_buff += key.name
    if(key.name == 'space'):
        keyb_buff += " "
    if(key.name == 'enter'):
        if ~reading:
            if keyb_buff.strip() == 'q':
                end = 1
            elif len(keyb_buff.strip()) > 0:
                sendMessage()
                saveHistory()
    if(key.name == 'backspace'):
        keyb_buff = keyb_buff[:-1]
    # print(keyb_buff)
    if ~reading:
        updateInput()

def on_rel(key):
    pass
keyboard.on_press(on_prs)
keyboard.on_release(on_rel)

class Colors:
    BLACK = "\033[0;30m"
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    BROWN = "\033[0;33m"
    BLUE = "\033[0;34m"
    PURPLE = "\033[0;35m"
    CYAN = "\033[0;36m"
    LIGHT_GRAY = "\033[0;37m"
    DARK_GRAY = "\033[1;30m"
    LIGHT_RED = "\033[1;31m"
    LIGHT_GREEN = "\033[1;32m"
    YELLOW = "\033[1;33m"
    LIGHT_BLUE = "\033[1;34m"
    LIGHT_PURPLE = "\033[1;35m"
    LIGHT_CYAN = "\033[1;36m"
    LIGHT_WHITE = "\033[1;37m"
    BOLD = "\033[1m"
    FAINT = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    NEGATIVE = "\033[7m"
    CROSSED = "\033[9m"
    END = "\033[0m"

# chatHistory = ["(23:52) Timur: Hello", "(23:59) Robert: YEEEA", "(23:59) Kirill: IT WORKS???"]

# print(Colors.RED + "R" + Colors.GREEN + "G" + Colors.BLUE + "B")

def getTime():
    t = time.asctime().split(' ')[3]
    return t[:t.rfind(":")]

def printHistory():
    for n in chatHistory:
        nc = n[n.find(':')+1:]
        message = Colors.BLUE + n[:n.find(')')+1]
        if username in nc[:nc.find(':')]:
            col = Colors.LIGHT_BLUE
        else:
            col = Colors.DARK_GRAY
        message += col + nc[nc.find(')')+1:nc.find(':')+1]
        message += Colors.LIGHT_WHITE + nc[nc.find(':')+1:]
        print(message)

def saveHistory():
    with open("chat.txt", 'w') as file:
        for n in chatHistory:
            file.write(n + '\n')
        file.close()

printHistory()

print(Colors.LIGHT_WHITE, end='')

while end == 0:
    if(ser.in_waiting > 0):
        reading = 1
        req = ser.read_until(b'!')
        ser.write(b'?')
        msg = ser.read_until(b'\n')
        chatHistory.append(msg.decode().strip())

        n = msg.decode().strip()
        nc = n[n.find(':')+1:]
        message = Colors.BLUE + n[:n.find(')')+1]
        if username in nc[:nc.find(':')]:
            col = Colors.LIGHT_BLUE
        else:
            col = Colors.DARK_GRAY
        message += col + nc[nc.find(')')+1:nc.find(':')+1]
        message += Colors.LIGHT_WHITE + nc[nc.find(':')+1:]
        print(message)
        saveHistory()
        reading = 0

# ser.read_all()
