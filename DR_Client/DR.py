def print_option():
	print('Enter 1 to request a file')
	print('Enter 2 quit')
def decry(ciphertext, key):
		IV = ciphertext[:AES.block_size]
		# print(IV)
		cipher = AES.new(hashlib.sha256(str(key).encode()).digest(), AES.MODE_CBC,IV)
		plaintext = cipher.decrypt(ciphertext[AES.block_size:])
		return plaintext.rstrip(b"\0")
		
def decrypt(key, filename):
	
	with open('credentials.enc', 'rb') as fo:
			ciphertext = fo.read()
	dec = decry(ciphertext, key)
	with open(filename[:-4], 'wb') as fo:
			fo.write(dec)


import time
import socket
# import encrypt
import sys
import os
from sys import getsizeof
from Crypto.Cipher import AES
import random
import os
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
import Crypto
BUFFER_SIZE=1024
HOST = ""
PORT = 9851
import hashlib



client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

#key set up
out_data ="KEYSETUP"
client.sendall(bytes(out_data,'UTF-8'))
import AccessControlDR_DRClient
Msg1=  client.recv(BUFFER_SIZE).decode()
(Msg2,TS2,SKGSSDRj1)=AccessControlDR_DRClient.ACDG2_G3(Msg1)
client.sendall(bytes(Msg2,'UTF-8'))
Msg3=  client.recv(BUFFER_SIZE).decode()
AccessControlDR_DRClient.ACDG5(Msg3,TS2,SKGSSDRj1)
serect_key=SKGSSDRj1
print(serect_key)

from sys import getsizeof
# print(serect_key,getsizeof(serect_key),len(arr))

# print('serect_key size=',getsizeof(serect_key),serect_key)
while 1:
	print_option()
	i=int(input())
	if i == 1:
		print("Enter the file name ")
		fname=input()
		out_data="REQSERV"+" "+fname
		client.sendall(bytes(out_data,'UTF-8'))
		in_data =  client.recv(BUFFER_SIZE).decode()
		# print(in_data)
		if 'DISCONNECT' in in_data:
			out_data ="DISCONNECT"
			client.sendall(bytes(out_data,'UTF-8'))
			client.close()
			exit()
		else:
			with open('credentials.enc', 'wb') as fw:
				fsize = int(in_data)
				out_data="gotsize"
				client.sendall(bytes(out_data,'UTF-8'))
				rsize = 0

				while True:
					# print(1)
					data = client.recv(BUFFER_SIZE)
					rsize = rsize + len(data)
					fw.write(data)
					if  rsize >= fsize:
						out_data="gotfile"
						client.sendall(bytes(out_data,'UTF-8'))
						break
			print("waiting")
			in_data =  client.recv(BUFFER_SIZE).decode()
			print(in_data)
			if 'REQCOM' in in_data:
					fsize=int(in_data.split()[1])
					decrypt(serect_key,fname)
					# os.remove('credentials.enc')
					print('Sucessfully received the file')
	else:
			out_data ="DISCONNECT"
			client.sendall(bytes(out_data,'UTF-8'))
			client.close()
			exit()




