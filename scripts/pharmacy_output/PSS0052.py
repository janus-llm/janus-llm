# PSS0052 ;BIR/JLC-POPULATE FIRST SERVICE DATE ;01/14/2002
# ;1.0;PHARMACY DATA MANAGEMENT;**52,125**;9/30/97;Build 2
#
# ;Reference to ^PSRX is supported by DBIA 3500.
#
import os
import time
import sys

def EN():
    if not os.environ.get('DUZ'):
        print("Your DUZ is not defined. It must be defined to run this routine.")
        return
    
    os.environ["ZTRTN"] = "ENQN^PSS0052"
    os.environ["ZTDESC"] = "Build FIRST PHARMACY SERVICE Info (PDM)"
    os.environ["ZTIO"] = ""
    os.system("^%ZTLOAD")
    
    print("\nThe build of first pharmacy service info is" + (" NOT" if not os.environ.get("ZTSK") else "") + " queued\n")
    
    if os.environ.get("ZTSK"):
        print(" (to start NOW).\n")
        print("YOU WILL RECEIVE A MAILMAN MESSAGE WHEN TASK #" + os.environ["ZTSK"] + " HAS COMPLETED.")

def ENQN():
    DFN = 0
    while True:
        DFN += 1
        if not os.path.exists(os.path.join("^PS(55,", str(DFN))):
            break
        os.environ["A"] = ""
        os.system("^PS(55," + str(DFN) + "):" + (str(os.environ.get("DILOCKTM")) if os.environ.get("DILOCKTM") else "3"))
        
        PSJORD = 0
        while True:
            PSJORD += 1
            if not os.path.exists(os.path.join("^PS(55,", str(DFN), ",5,", str(PSJORD))):
                break
            
            LOG = os.popen("^PS(55," + str(DFN) + ",5," + str(PSJORD) + ",0)").read().split("^")[16]
            if LOG:
                os.environ["A(LOG)"] = ""
                break
        
        PSJORD = 0
        while True:
            PSJORD += 1
            if not os.path.exists(os.path.join("^PS(55,", str(DFN), ",IV,", str(PSJORD))):
                break
            
            LOG = os.popen("^PS(55," + str(DFN) + ",IV," + str(PSJORD) + ",2)").read().split("^")[0]
            if LOG:
                os.environ["A(LOG)"] = ""
                break
        
        ARC = os.popen("^PS(55," + str(DFN) + ",ARC,0)").read().split("^")[0]
        if ARC:
            os.environ["A(ARC)"] = ""
        
        X = os.popen("^PS(55," + str(DFN) + ",P,0)").read().split("^")[0]
        if X:
            RX = os.popen("^PS(55," + str(DFN) + ",P," + str(X) + ",0)").read()
            LOG = RX.split("^")[2]
            if LOG:
                os.environ["A(LOG)"] = ""
        
        LOG = os.popen("^PS(55," + str(DFN) + ",0)").read().split("^")[0]
        if LOG:
            A = os.popen("^PS(55," + str(DFN) + ",0)").read()
            if not A.split("^")[6] or A.split("^")[6] > LOG:
                A = A.split("^")
                A[6] = LOG.split(".")[0]
                A[7] = "H"
                os.system("^PS(55," + str(DFN) + ",0)=\"" + "^".join(A) + "\"")
        
        os.system("L")

def SENDMSG():
    os.environ["PSG"] = ""
    os.environ["XMY(DUZ)"] = ""
    os.environ["XMY(\"G.PSU PBM@\"_$G(^XMB(\"NETNAME\")))"] = ""
    os.system("^DD(\"DD\")")
    os.system("^XMD")
    pass

EN()