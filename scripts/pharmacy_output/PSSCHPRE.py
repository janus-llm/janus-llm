def PSSCHPRE():
    # BIR/WRT-CMOP-Host pre-install routine to kill off old DDs for files sent with the package- clean up 50
    # 09/29/97 9:32
    # 1.0;PHARMACY DATA MANAGEMENT;;9/30/97
    # PRE-INSTALL ROUTINE-CMOP HOST
    KILLIT()
    if not ('^PS(59.7,1,80)' in globals()):
        CLEAN50()
        CLEANDD()
        del IEN

def KILLIT():
    print("I Am Deleting Your Data Dictionary for \"MEDICATION ROUTES\" File.")
    DIU = 51.2
    DIU[0] = ""
    EN^DIU2()
    del DIU

def CLEAN50():
    IEN = 0
    while IEN:
        IEN = IEN + 1
        if ('^PSDRUG(IEN)' in globals()) and ('^PSDRUG(IEN,2)' in globals()):
            ^PSDRUG(IEN,2) = ""

def CLEANDD():
    del ^DD(50,12,1,535000)
    del ^DD(50,203)
    del ^DD(50,13,1,535000)
    del ^DD(50,15,1,535000)
    del ^DD(50,16,1,1)
    del ^DD(50,"TRB",50,16)
    del ^DD(50,23,2)
    del ^DD(50,23,2.1)
    del ^DD(50,24,2)
    del ^DD(50,24,2.1)

PSSCHPRE()