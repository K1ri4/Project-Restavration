import serial
import serial.tools.list_ports

ports = serial.tools.list_ports.comports()

COMport = "None"

debug = 0

for port in ports:
    if debug: print(f"Port: {port.device}")
    if debug: print(f"Description: {port.description}")
    if debug: print(f"Manufacturer: {port.manufacturer}\n")
    if "arduino" in port.description.lower() or "ch340" in port.description.lower():
        if debug: print("Found smthng like a USB-TTL... It was", port.device)
        COMport = port.device

with open("com.txt", 'w') as file:
    file.write(COMport)
    file.close()
