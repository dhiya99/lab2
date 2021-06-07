from os import system
import socket
from tqdm import tqdm
import time
import sys
import os
import ntplib
from time import ctime
from datetime import datetime
from _thread import *

_ = system('clear')

print(r"""NTP""")

def threaded_client(s, dateRecv, host, port):

	while True:
		if not dateRecv:
			break

		print("[+] Client IP Address :", host)
		clientLocalDT = datetime.strptime(dateRecv.decode(), "%Y-%m-%d, %H:%M:%S.%f")
		print("[+] T1 :",clientLocalDT)

		T2 = datetime.now()
		T2 = T2.strftime("%Y-%m-%d %H:%M:%S.%f")
		print("[+] T2 :", T2)
		bytesSend = str.encode(T2)
		s.sendto(bytesSend, (host, port))
		print("[+] Sending T2 to Client")

		T3 = datetime.now()
		T3 = T3.strftime("%Y-%m-%d %H:%M:%S.%f")
		print("[+] T3 :", T3)
		bytesSend = str.encode(T3)
		s.sendto(bytesSend, (host, port))
		print("[+] Sending T3 to Client")
		print("[+] Process Completed\n")

		print(f"[+] Server is listening.. | Port: 123")

		break

def main():

	status = '1'
	while(status != '0'):
		print("\n[0] Exit the Program\n[1] Print Latest DateTime Information\n[2] Start NTP Server\n")
		option = input("Choose option: ")
		print("Option choosed is", option)

		status = option

		if(option == '1'):
			local = datetime.now()
			print("\nQuerying the NTP Server\n---------------------")
			c = ntplib.NTPClient()
			response = c.request('my.pool.ntp.org', version=3)
			print("Response Offset\t\t: ", response.offset)
			print("Response Version\t: ", response.version)
			print("Response Time\t\t: ", datetime.fromtimestamp(response.tx_time))
			print("Local DateTime\t\t: ", local)
			print("\n")
		elif(option == '2'):
			print("\nStarting NTP Server..")

			s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
			print(f"[+] Socket successfully created")

			port = 123
			buffer = 1024
			ThreadCount = 0

			s.bind(('', port))
			print(f"[+] Socket binded to " + str(port))

			print(f"[+] Server is listening.. | Port: {port}")

			while(True):

				dateRecv, address = s.recvfrom(buffer)
				host, port = address

				print(f"[+] {address} is connected.")

				start_new_thread(threaded_client, (s, dateRecv, host, port))

				ThreadCount += 1
				print("\n[+] Thread Number :" + str(ThreadCount))

			s.close()


	print("Exiting..")


if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print('Interrupted')
		try:
			sys.exit(0)
		except SystemExit:
			os._exit(0)
