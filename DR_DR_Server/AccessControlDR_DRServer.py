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
    # print('Cert_DRj=',Cert_DRj)
    TCDRj = int(l[1])
    fp.close()
    fp=open("pub.txt",'r')
    l=fp.readlines()
    temp = l[0].split(',')
    # print(temp)
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
    rj1 = rand.getrandbits(256)% curve.p
    aj1_dash = ECC.hex2int(hashlib.sha256((str(ID_DRj)+str(TCDRj)+str(rj1)+str(TS1)).encode("utf-8")).hexdigest())
    Aj1=curve.mul(curve.G,aj1_dash)
    # print(aj1_dash,Aj1)
    # SigDRi=(r1_dash+ECC.hex2int(hashlib.sha256((str(PkDRi)+str(RID_DRi)+str(PkCRj)+str(PubGSSj)+str(ADRi)+str(TS1)).encode("utf-8")).hexdigest()) * int(kDRi) )
    Msg1=str(ID_DRj)+":"+ str(Aj1)+":"+str(Cert_DRj)+":"+str(TS1)
    # print(Msg1,TS1)
    return Msg1,aj1_dash,TS1


def ACDG4(Msg2,aj1,TS1):
    l=Msg2.split(':')
    TS2 = int(l[3])
    TS3 = (int(time.time()))
    Cert_DRj1 = (int(l[4]))
    ID_DRj1=int(l[0])
    SKVj2j1 = int(l[2])
    temp = l[1].split(',')
    xx = int(temp[0][1:])
    yy=int(temp[1].split(')')[0])
    Bj2 = ECC.ECpoint(curve,xx,yy)

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

    fp=open("ID.txt","r")
    l=fp.readlines()
    ID_GSS= int(l[1])
    fp.close()
    fp=open("DR.txt","r")
    l=fp.readlines()
    ID_DRj= int(l[0])
    Cert_DRj= int(l[2])
    TCDRj = int(l[1])
    fp.close()
    

    if(abs(TS3-TS2)<delta):
        val1 = curve.mul(curve.G,Cert_DRj1)
        # has = ECC.hex2int(hashlib.sha256((str(RID_GSSj)+str(ID_CRj)+str(PubCRj)+str(PubGSSj)).encode("utf-8")).hexdigest())
        # print(Cert_GSSj)
        # print(RID_GSSj,ID_CRj,PubCRj,PubGSSj)
        # print(PubGSSj,PkCRj,has)
        val2=  curve.add(PubDRj1,curve.mul(PubCR,ECC.hex2int(hashlib.sha256((str(PubDRj1)+str(ID_GSS)+str(PubCR)).encode("utf-8")).hexdigest())))
        
        # print(val1,val2)
        if (val1.x==val2.x and val1.y==val2.y) :
            DKj1j2=curve.mul(Bj2,aj1)
            multivariate = multi.fxy(ID_DRj,ID_DRj1)
            SKDRj1DRj2=ECC.hex2int(hashlib.sha256((str(DKj1j2)+str(multivariate)+str(Cert_DRj)+str(Cert_DRj1)+str(TS1)+str(TS2)).encode("utf-8")).hexdigest())
            # print(SKDRi_GSSj)
            # print(DKj1j2)

            # print(SKDRj1DRj2)
            SKVj1j2=ECC.hex2int(hashlib.sha256((str(SKDRj1DRj2)+str(Bj2)+str(TS2)+str(ID_DRj1)).encode("utf-8")).hexdigest())
            # print(SKVj1j2,SKVj2j1)
            if (SKVj1j2==SKVj2j1):
                ACKj1j2=ECC.hex2int(hashlib.sha256((str(SKDRj1DRj2)+str(TS3)).encode("utf-8")).hexdigest())
                Msg3=str(ACKj1j2)+":"+ str(TS3)
                # print("messae 3 = ",Msg3)
                return Msg3,SKDRj1DRj2
            else:
                print("Error4")
                return "0"
        else:
            print("Error5")
            return "0"
    else:
        print("Error6")
        return "0"



# (Msg1,aj1,TS1) = ACDG1()
# (Msg2,TS2,SKDRj2DRj1) = ACDG2_G3(Msg1)
# (Msg3,SKDRj1DRj2) = ACDG4(Msg2,aj1,TS1)
# ACDG5(Msg3,TS2,SKDRj2DRj1)
