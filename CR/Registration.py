import ECC
import hashlib
import time
from random import SystemRandom 
rand=SystemRandom()
curve=ECC.secp256k1

def Init():
    
    ID_CR=rand.getrandbits(256)%curve.p
    ID_GSS=rand.getrandbits(256)%curve.p
    rCR = rand.getrandbits(256)%curve.p
    PubCR = curve.mul(curve.G,rCR)


    fp=open('CR.txt','a')
    fp.write(str(ID_CR)+'\n')
    fp.write(str(rCR)+'\n')
    fp.close()
    fp=open('GSS.txt','a')
    fp.write(str(ID_GSS)+'\n')
    fp.close()
    fp=open('pub.txt','a')
    fp.write(str(PubCR)+'\n')
    fp.close()
    fp=open('ID.txt','a')
    fp.write(str(ID_CR)+'\n')
    fp.write(str(ID_GSS)+'\n')
    fp.close()
    fp=open('multivariate.txt','a')
    for i in range(0,6):
        Aij = rand.getrandbits(256)%curve.p
        fp.write(str(Aij)+'\n')
    fp.close()


def CR_to_DR1():
    ID_DRj=rand.getrandbits(256)%curve.p
    fp=open('DR.txt','a')
    fp.write(str(ID_DRj)+'\n')
    fp.close()
    fp=open('ID.txt','a')
    fp.write(str(ID_DRj)+'\n')
    fp.close()
    
    fp=open('CR.txt','r')
    l=fp.readlines()
    ID_CR = int(l[0])
    rCR=int(l[1])
    fp.close()
    fp=open('GSS.txt','r')
    l=fp.readlines()
    ID_GSS=int(l[0])
    fp.close()
    fp=open('pub.txt','r')
    l=fp.readlines()
    temp = l[0].split(',')
    xx = int(temp[0][1:])
    yy=int(temp[1].split(')')[0])
    PubCR  = ECC.ECpoint(curve,xx,yy)
    fp.close()

    MKDRj=rand.getrandbits(256)%curve.p
    rDRj=rand.getrandbits(256)%curve.p
    PubDRj=curve.mul(curve.G,rDRj)
    TCDRj= ECC.hex2int(hashlib.sha256((str(MKDRj)+str(ID_DRj)+str(ID_CR)+str(ID_GSS)+str(int(time.time()))).encode("utf-8")).hexdigest())
    Cert_DRj = (rDRj +  ECC.hex2int(hashlib.sha256((str(PubDRj)+str(ID_GSS)+str(PubCR)).encode("utf-8")).hexdigest())*rCR )
    fp=open('DR.txt','a')
    fp.write(str(TCDRj)+'\n')
    fp.write(str(Cert_DRj)+'\n')
    fp.write(str(PubDRj))
    fp.close()
    fp=open('pub.txt','a')
    fp.write(str(PubDRj)+'\n')
    fp.close()

def CR_to_DR2():
    ID_DRj1=rand.getrandbits(256)%curve.p
    fp=open('DR1.txt','a')
    fp.write(str(ID_DRj1)+'\n')
    fp.close()
    fp=open('ID.txt','a')
    fp.write(str(ID_DRj1)+'\n')
    fp.close()
    
    fp=open('CR.txt','r')
    l=fp.readlines()
    ID_CR = int(l[0])
    rCR=int(l[1])
    fp.close()
    fp=open('GSS.txt','r')
    l=fp.readlines()
    ID_GSS=int(l[0])
    fp.close()
    fp=open('pub.txt','r')
    l=fp.readlines()
    temp = l[0].split(',')
    xx = int(temp[0][1:])
    yy=int(temp[1].split(')')[0])
    PubCR  = ECC.ECpoint(curve,xx,yy)
    fp.close()

    MKDRj1=rand.getrandbits(256)%curve.p
    rDRj1=rand.getrandbits(256)%curve.p
    PubDRj1=curve.mul(curve.G,rDRj1)
    TCDRj1= ECC.hex2int(hashlib.sha256((str(MKDRj1)+str(ID_DRj1)+str(ID_CR)+str(ID_GSS)+str(int(time.time()))).encode("utf-8")).hexdigest())
    Cert_DRj1 = (rDRj1 +  ECC.hex2int(hashlib.sha256((str(PubDRj1)+str(ID_GSS)+str(PubCR)).encode("utf-8")).hexdigest())*rCR )
    fp=open('DR1.txt','a')
    fp.write(str(TCDRj1)+'\n')
    fp.write(str(Cert_DRj1)+'\n')
    fp.write(str(PubDRj1))
    fp.close()
    fp=open('pub.txt','a')
    fp.write(str(PubDRj1)+'\n')
    fp.close()

def CR_to_GSS():
    rGSS = rand.getrandbits(256)%curve.p 
    PubGSS = curve.mul(curve.G,rGSS)
    fp=open('GSS.txt','r')
    l=fp.readlines()
    ID_GSS=int(l[0])
    fp.close()
    fp=open('CR.txt','r')
    l=fp.readlines()
    ID_CR = int(l[0])
    rCR=int(l[1])
    fp.close()
    fp=open('pub.txt','r')
    l=fp.readlines()
    temp = l[0].split(',')
    xx = int(temp[0][1:])
    yy=int(temp[1].split(')')[0])
    PubCR  = ECC.ECpoint(curve,xx,yy)
    fp.close()
    Cert_GSS = (rGSS +  ECC.hex2int(hashlib.sha256((str(PubGSS)+str(ID_GSS)+str(PubCR)).encode("utf-8")).hexdigest())*rCR )
    TCGSS= ECC.hex2int(hashlib.sha256((str(ID_GSS)+str(ID_CR)+str(rGSS)+str(int(time.time()))).encode("utf-8")).hexdigest())
    fp=open('GSS.txt','a')
    fp.write(str(TCGSS)+'\n')
    fp.write(str(Cert_GSS)+'\n')
    fp.write(str(PubGSS)+'\n')
    fp.close()
    fp=open('pub.txt','a')
    fp.write(str(PubGSS)+'\n')
    fp.close()

Init()
CR_to_DR1()
CR_to_DR2()
CR_to_GSS()
