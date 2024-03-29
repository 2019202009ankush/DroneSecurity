import ECC
import hashlib
import time
from random import SystemRandom 
rand=SystemRandom()
curve=ECC.secp256k1
delta = 100
import multi

def ACDG2_G3(Msg1):
    print(Msg1)
    l=Msg1.split(':')
    TS1 = int(l[3])
    TS2 = (int(time.time()))
    Cert_DRj = (int(l[2]))
    # print('Cert_DRj=',Cert_DRj)
    ID_DRj =int(l[0])
    temp = l[1].split(',')
    xx = int(temp[0][1:])
    yy=int(temp[1].split(')')[0])
    # print(xx,yy)
    Aj1 =ECC.ECpoint(curve,xx,yy)
    # print(ADRi)

    fp=open("ID.txt","r")
    l=fp.readlines()
    ID_GSS= int(l[1])
    fp.close()

    fp=open("DR1.txt","r")
    l=fp.readlines()
    ID_DRj1= int(l[0])
    Cert_DRj1= int(l[2])
    TCDRj1 = int(l[1])
    fp.close()

    fp=open("pub.txt",'r')
    l=fp.readlines()
    temp = l[0].split(',')
    xx = int(temp[0][1:])
    yy=int(temp[1].split(')')[0])
    PubCR = ECC.ECpoint(curve,xx,yy)

    temp = l[1].split(',')
    xx = int(temp[0][1:])
    yy=int(temp[1].split(')')[0])
    PubDRj = ECC.ECpoint(curve,xx,yy)

    temp = l[2].split(',')
    xx = int(temp[0][1:])
    yy=int(temp[1].split(')')[0])
    PubDRj1 = ECC.ECpoint(curve,xx,yy)

    temp = l[3].split(',')
    xx = int(temp[0][1:])
    yy=int(temp[1].split(')')[0])
    PubGSS = ECC.ECpoint(curve,xx,yy)
    
    if(abs(TS1-TS2)<delta):
        # print(Cert_DRi)
        val1 = curve.mul(curve.G,Cert_DRj)
        print(PubDRj,ID_GSS,PubCR)
        tm = curve.mul(PubCR,ECC.hex2int(hashlib.sha256((str(PubDRj)+str(ID_GSS)+str(PubCR)).encode("utf-8")).hexdigest()))
        # tm = curve.mul(PkCRj,ECC.hex2int(hashlib.sha256((str(RID_DRi)+str(PubCRj)+str(PubGSSj)+str(PubDRi)).encode("utf-8")).hexdigest()))
        # print(tm)
        val2=curve.add(PubDRj,tm)
        print(val1)
        print(val2)
        if(val1.x==val2.x and val1.y==val2.y):
                rj2 = rand.getrandbits(256)% curve.p
                bj2 = ECC.hex2int(hashlib.sha256((str(ID_DRj1)+str(TCDRj1)+str(rj2)+str(TS2)).encode("utf-8")).hexdigest())
                Bj2=curve.mul(curve.G,bj2)
                # print(bj2,Bj2)
                DKj2j1= curve.mul(Aj1,bj2)
                # print(DKj2j1)
                multivariate = multi.fxy(ID_DRj1,ID_DRj)
                SKDRj2DRj1=ECC.hex2int(hashlib.sha256((str(DKj2j1)+str(multivariate)+str(Cert_DRj)+str(Cert_DRj1)+str(TS1)+str(TS2)).encode("utf-8")).hexdigest())
                # print(SKDRj2DRj1)
                SKVj2j1=ECC.hex2int(hashlib.sha256((str(SKDRj2DRj1)+str(Bj2)+str(TS2)+str(ID_DRj1)).encode("utf-8")).hexdigest())
                Msg2=str(ID_DRj1)+":"+ str(Bj2)+":"+str(SKVj2j1)+":"+str(TS2)+":"+ str(Cert_DRj1)
                return Msg2,TS2,SKDRj2DRj1

            
        else:
            print("Error2")
            return "0"
    else:
        print("Error3")
        return "0"

def ACDG5(Msg3,TS2,SKDRj2DRj1):
    # print(Msg3)
    l=Msg3.split(':')
    # print(l)
    TS3 = int(l[1])
    TS4= int(time.time())
    if(TS4-TS3<delta):
            
        ACKj1j2 = int(l[0])
        ACKj2j1=ECC.hex2int(hashlib.sha256((str(SKDRj2DRj1)+str(TS3)).encode("utf-8")).hexdigest())
        if ACKj1j2 == ACKj2j1:
            print("     session key established     ")
        else:
            print("error")

