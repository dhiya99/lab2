import socket
import sys
import json
import tqdm
import os
import datetime
from datetime import datetime
from os import system

def calcOffset(T1, T2, T3, T4):
	print("\n[+] -==[Calculating Offset]==-") 

	offsetStatusA = 0
	offsetStatusB = 0

	T1 = datetime.strptime(T1, "%H:%M:%S.%f")
	T2 = datetime.strptime(T2, "%H:%M:%S.%f")
	T3 = datetime.strptime(T3, "%H:%M:%S.%f")
	T4 = datetime.strptime(T4, "%H:%M:%S.%f")

	if(T1 >= T2):
		a = T1 - T2
		offsetStatusA = 1
	elif(T2 > T1):
		a = T2 -T1
	if(T3 >= T4):
		b = T3 -T4
	elif(T4 > T3):
		b = T4 - T3
		offsetStatusB = 1

	offset = ((a + b) / 2)
	offsetSec = offset.total_seconds()
	if(offsetStatusA == 1 and offsetStatusB == 1):
		sign = "Haste(+)"
		print(f"[+] Please adjust the local time by minus {offsetSec} seconds to sync with NTP Server")
	else:
		sign = "Delay(-)"
		print(f"[+] Please adjust the local time by adding {offsetSec} seconds to sync with NTP Server")
	print("[+] Offset DateTime :", offsetSec, f"seconds [{sign}]")



def calcDelay(T1, T2, T3, T4):
	print("\n[+] -==[Calculating Delay]==-")

	T1 = datetime.strptime(T1, "%H:%M:%S.%f")
	T2 = datetime.strptime(T2, "%H:%M:%S.%f")
	T3 = datetime.strptime(T3, "%H:%M:%S.%f")
	T4 = datetime.strptime(T4, "%H:%M:%S.%f")

	delay = (T4 - T1) - (T3 - T2)
	delaySec = delay.total_seconds()
	print("[+] Delay Roundtrip :", delaySec, "seconds")

_ = system('clear')

print(r"""NTP CLIENT""")

def main():

	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)

	host = '192.168.1.14'


	port = 123

	print(f"[+] Connecting to {host}:{port}")
	s.connect((host, port))
	print("[+] Connected.")

	localDT = datetime.now()

	print("[+] Local System DateTime : ", localDT)

	localDTStr = localDT.strftime("%Y-%m-%d, %H:%M:%S.%f")

	bytesSend = str.encode(localDTStr)
	buffer = 1024

	s.sendto(bytesSend, (host, port))

	print("[+] Sending 'Originate Timestamp' from Client to NTP Server")

	T1 = localDT

	T2, address = s.recvfrom(buffer)
	T2 = datetime.strptime(T2.decode(), "%Y-%m-%d %H:%M:%S.%f")
	print("[+] T1 :", T1)

	print("\n[+] Received 'Received Timestamp(T2)' and 'Transmitted Timestamp(T3)' from NTP Server")
	print("[+] T2 :", T2)
	T3, address = s.recvfrom(buffer)
	T3 = datetime.strptime(T3.decode(), "%Y-%m-%d %H:%M:%S.%f")
	print("[+] T3 :", T3)

	print("\n[+] Generate 'Timestamp Reference(T4)' from Client Local Clock")
	T4 =  datetime.now()
	T4 = T4.strftime("%Y-%m-%d %H:%M:%S.%f")
	T4 = datetime.strptime(T4, "%Y-%m-%d %H:%M:%S.%f")
	print("[+] T4 :", T4)

	T1 = datetime.strftime(T1, "%H:%M:%S.%f")
	T2 = datetime.strftime(T2, "%H:%M:%S.%f")
	T3 = datetime.strftime(T3, "%H:%M:%S.%f")
	T4 = datetime.strftime(T4, "%H:%M:%S.%f")

	calcOffset(T1, T2, T3, T4)
	calcDelay(T1, T2, T3, T4)

	print("[+] Successfully Calculate Clock Offset & Roundtrip Delay")

	print("\n[+] Closing Socket")
	s.close()

	print("[+] Exiting Client Program\n")

if __name__ == "__main__":
	try:
        	main()
	except KeyboardInterrupt:
		print('Interrupted')
		try:
			sys.exit(0)
		except SystemExit:
			os._exit(0)
