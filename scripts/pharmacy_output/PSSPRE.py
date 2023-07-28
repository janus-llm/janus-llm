# BIR/WRT-Pre-install routine to kill off old DDs for files sent with the package- clean up 50, additives and solutions files
# 09/30/97 14:58
# 1.0;PHARMACY DATA MANAGEMENT;;9/30/97
# PRE-INSTALL ROUTINE

def PSSPRE():
    KILLIT()
    if not "^PS(59.7,1,80)" in globals():
        CLEAN50()
        CLEANAD()
        CLEANSOL()
        CLEANDD()
    del globals()["IEN"]

def KILLIT():
    print("\nI Am Deleting Your Data Dictionary for \"APSP INTERVENTION RECOMMENDATION\" File.")
    DIU = 9009032.5
    DIU[0] = ""
    EN(DIU)
    print("\nI Am Deleting Your Data Dictionary for \"MEDICATION ROUTES\" File.")
    DIU = 51.2
    DIU[0] = ""
    EN(DIU)

def CLEAN50():
    IEN = 0
    while True:
        IEN += 1
        if not "^PSDRUG(" + str(IEN) in globals():
            break
        if "^PSDRUG(" + str(IEN) + ",2)" in globals():
            globals()["^PSDRUG(" + str(IEN) + ",2)"] = ""

def CLEANAD():
    IEN = 0
    while True:
        IEN += 1
        if not "^PS(52.6," + str(IEN) in globals():
            break
        if "^PS(52.6," + str(IEN) + ",0)" in globals():
            globals()["^PS(52.6," + str(IEN) + ",0)"] = ""

def CLEANSOL():
    IEN = 0
    while True:
        IEN += 1
        if not "^PS(52.7," + str(IEN) in globals():
            break
        if "^PS(52.7," + str(IEN) + ",0)" in globals():
            globals()["^PS(52.7," + str(IEN) + ",0)"] = ""

def CLEANDD():
    del globals()["^DD(50,12,1,535000)"]
    del globals()["^DD(50,203)"]
    del globals()["^DD(50,13,1,535000)"]
    del globals()["^DD(50,15,1,535000)"]
    del globals()["^DD(50,16,1,1)"]
    del globals()["^DD(50,\"TRB\",50,16)"]
    del globals()["^DD(50,0,\"IX\",\"AE\",50,202)"]
    del globals()["^DD(50,0,\"IX\",\"IV\",50.03,.01)"]
    del globals()["^DD(50,0,\"IX\",\"IV1\",50,204)"]
    del globals()["^DD(50,0,\"IX\",\"IV2\",50,201.1)"]
    del globals()["^DD(50,0,\"PT\",50.03,.02)"]
    del globals()["^DD(50,0,\"IX\",\"AV1\",50,200)"]
    del globals()["^DD(50,0,\"IX\",\"AD\",50,201)"]
    del globals()["^DD(50,0,\"IX\",\"AF\",50,201.3)"]
    del globals()["^DD(50,0,\"IX\",\"AV2\",50,201)"]
    del globals()["^DD(50,23,2)"]
    del globals()["^DD(50,23,2.1)"]
    del globals()["^DD(50,24,2)"]
    del globals()["^DD(50,24,2.1)"]
    del globals()["^DD(50,8,9.2)"]
    DIK = "^DD(55,"
    DA = 99
    DA[1] = 55
    DIK()

PSSPRE()