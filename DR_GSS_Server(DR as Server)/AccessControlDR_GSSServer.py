import ECC
import hashlib
import time
from random import SystemRandom 
rand=SystemRandom()
curve=ECC.secp256k1
delta = 100
import multi

def ACDG1():
    fp=open("DR.txt","r")
    l=fp.readlines()
    ID_DRj= int(l[0])
    Cert_DRj= int(l[2])
    TCDRj = int(l[1])
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

    temp = l[3].split(',')
    xx = int(temp[0][1:])
    yy=int(temp[1].split(')')[0])
    PubGSS = ECC.ECpoint(curve,xx,yy)


    fp.close()



    TS1 = (int(time.time()))
    rDRj = rand.getrandbits(256)% curve.p
    aDRj_dash = ECC.hex2int(hashlib.sha256((str(ID_DRj)+str(TCDRj)+str(rDRj)+str(TS1)).encode("utf-8")).hexdigest())
    ADRj=curve.mul(curve.G,aDRj_dash)
    # SigDRi=(r1_dash+ECC.hex2int(hashlib.sha256((str(PkDRi)+str(RID_DRi)+str(PkCRj)+str(PubGSSj)+str(ADRi)+str(TS1)).encode("utf-8")).hexdigest()) * int(kDRi) )
    Msg1=str(ID_DRj)+":"+ str(ADRj)+":"+str(Cert_DRj)+":"+str(TS1)
    # print(Msg1,TS1)
    return Msg1,aDRj_dash,TS1


def ACDG4(Msg2,aDRj,TS1):
    l=Msg2.split(':')
    TS2 = int(l[2])
    TS3 = (int(time.time()))
    Cert_GSS = (int(l[3]))
    SKVj2j1 = int(l[1])
    temp = l[0].split(',')
    xx = int(temp[0][1:])
    yy=int(temp[1].split(')')[0])
    BGSS = ECC.ECpoint(curve,xx,yy)
    fp=open('ID.txt','r')
    l=fp.readlines()
    ID_GSS = int(l[1])

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
    fp.close()

    fp=open("DR.txt","r")
    l=fp.readlines()
    ID_DRj= int(l[0])
    Cert_DRj= int(l[2])
    TCDRj = int(l[1])
    fp.close()
    

    if(abs(TS3-TS2)<delta):
        val1 = curve.mul(curve.G,Cert_GSS)
        # has = ECC.hex2int(hashlib.sha256((str(RID_GSSj)+str(ID_CRj)+str(PubCRj)+str(PubGSSj)).encode("utf-8")).hexdigest())
        # print(Cert_GSSj)
        # print(RID_GSSj,ID_CRj,PubCRj,PubGSSj)
        # print(PubGSSj,PkCRj,has)
        val2=  curve.add(PubGSS,curve.mul(PubCR,ECC.hex2int(hashlib.sha256((str(PubGSS)+str(ID_GSS)+str(PubCR)).encode("utf-8")).hexdigest())))
        
        # print(val1,val2)
        if (val1.x==val2.x and val1.y==val2.y) :
            DKDRjGSS=curve.mul(BGSS,aDRj)
            multivariate = multi.fxy(ID_DRj,ID_GSS)
            SKDRjGSS=ECC.hex2int(hashlib.sha256((str(DKDRjGSS)+str(multivariate)+str(Cert_DRj)+str(Cert_GSS)+str(TS1)+str(TS2)).encode("utf-8")).hexdigest())
            # print(SKDRi_GSSj)
            SKVj1j2=ECC.hex2int(hashlib.sha256((str(SKDRjGSS)+str(BGSS)+str(TS2)+str(ID_GSS)).encode("utf-8")).hexdigest())
            if (SKVj1j2==SKVj2j1):
                ACKj1j2=ECC.hex2int(hashlib.sha256((str(SKDRjGSS)+str(TS3)).encode("utf-8")).hexdigest())
                Msg3=str(ACKj1j2)+":"+ str(TS3)
                # print("messae 3 = ",Msg3)
                return Msg3,SKDRjGSS
            else:
                print("Error4")
                return "0"
        else:
            print("Error5")
            return "0"
    else:
        print("Error6")
        return "0"

