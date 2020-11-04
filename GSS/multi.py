import ECC
import hashlib
import time
from random import SystemRandom 
rand=SystemRandom()
curve=ECC.secp256k1
delta = 1000000
def fxy(x,y):
	A=[[0,0,0],[0,0,0],[0,0,0]]
	fp=open('multivariate.txt','r')
	l=fp.readlines()
	# print(l)
	fp.close()
	count = 0
	for i in range (0,3):
		for j in range(i,3):
			A[i][j]=int(l[count].split('\n')[0])
			count=count+1
	for i in range (1,3):
		for j in range (0,i):
			A[i][j] = A[j][i]
	X=[]
	for i in range (0,3):
		X.append((x**i)%curve.p)
	# print(X)

	Y=[]
	for i in range (0,3):
		Y.append((y**i%curve.p))
	# print(Y)
	
	res1=[0,0,0]
	for i in range( len(X)):
		for j in range (len(A[i])):
			for k in range (len(A)):
				res1[i] = ((res1[i]%curve.p)+(A[i][k]*X[k])%curve.p)%curve.p
	# print(res1)
	multivariate = 0
	for i in range (len(res1)):
		multivariate=(multivariate%curve.p + (res1[i]*Y[i])%curve.p ) %curve.p

	# print(multivariate)
	return multivariate

