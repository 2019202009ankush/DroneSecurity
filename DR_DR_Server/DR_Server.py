import socket, threading,sys
import os
from Crypto.Cipher import AES
BUFFER_SIZE=1024
import random
import os
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
import Crypto
import ECC
import AccessControlDR_DRServer
import hashlib
class handle_req(threading.Thread):
	

	def __init__(self,addr,sock):
		threading.Thread.__init__(self)
		self.self_socket = sock
		self.add=addr
		self.serect_key=None
		self.cipher=None

	def pad(self,s):
		return s + b"\0" * (AES.block_size - len(s) % AES.block_size)

	def encrypt(self,message, key, key_size=256):
		message = self.pad(message)
		IV = Random.new().read(AES.block_size)
		cipher = AES.new(hashlib.sha256(str(key).encode()).digest(), AES.MODE_CBC,IV)
		return IV + cipher.encrypt(message)

	def decrypt(self,ciphertext, key):
		IV = ciphertext[:AES.block_size]
		cipher = AES.new(hashlib.sha256(str(key).encode()).digest(), AES.MODE_CBC,IV)
		plaintext = cipher.decrypt(ciphertext[AES.block_size:])
		return plaintext.rstrip(b"\0")

	def encrypt_file(self, key,file_name):
		with open(file_name, 'rb') as fo:
			plaintext = fo.read()
		enc = self.encrypt(plaintext, key)
		with open('credentials.enc', 'wb') as fo:
			fo.write(enc)

	def decrypt_file(self,file_name, key):
		with open(file_name, 'rb') as fo:
			ciphertext = fo.read()
		dec = self.decrypt(ciphertext, key)
		with open(file_name[:-4], 'wb') as fo:
			fo.write(dec)


	
	def run(self):
		msg = ''
		while True:
			data = self.self_socket.recv(BUFFER_SIZE)
			msg = data.decode()
			#server sekleton
			if 'KEYSETUP' in msg:
				(Msg1,aDRj,TS1)=AccessControlDR_DRServer.ACDG1()
				self.self_socket.send(str(Msg1).encode())
				Msg2 = self.self_socket.recv(BUFFER_SIZE).decode()
				(Msg3,SKDRjGSS)=AccessControlDR_DRServer.ACDG4(Msg2,aDRj,TS1)
				self.self_socket.send(str(Msg3).encode())
				self.serect_key=SKDRjGSS
				print(SKDRjGSS)
				
			elif 'REQSERV' in msg:
				lis=msg.split()
				fname=str(lis[1])
				print(fname)

				try:
					fsize1 = os.path.getsize(os.path.abspath(os.path.join('', fname)))
					self.encrypt_file(self.serect_key,fname)
					fname='credentials.enc'
					fsize2=os.path.getsize(os.path.abspath(os.path.join('', fname)))
					self.self_socket.send(str(fsize2).encode('UTF-8'))
					print(self.self_socket.recv(BUFFER_SIZE).decode())
					# self.encrypt_file(self.serect_key,filename)
					# fname2=fname+'.enc'
					# fsize2=os.path.getsize(os.path.abspath(os.path.join('', fname2)))
					# self.self_socket.send(str(fsize2).encode('UTF-8'))
					# print(self.self_socket.recv(BUFFER_SIZE).decode())
					print('Sending......')
					with open(fname, 'rb') as fs:
							data = fs.read(BUFFER_SIZE)
							while data:
								# print(2)
								self.self_socket.send(data)
								data = fs.read(BUFFER_SIZE)

					self.self_socket.recv(BUFFER_SIZE).decode()
					s='REQCOM '+str(fsize1)
					# os.remove('credentials.enc')
					self.self_socket.send(str(s).encode())

				except Exception as e:
					print(e)
					print('Now do DISCONNECT')
					s='DISCONNECT'
					self.self_socket.send(str(s).encode())



HOST =''
PORT = 9851
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
while True:
	server.listen(1)
	sock, addr = server.accept()
	nth = handle_req(addr, sock)
	nth.start()
