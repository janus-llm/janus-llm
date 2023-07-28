def ENNV():
    ZTSAVE,ZTSK = [], []
    ZTRTN = "ENQN^PSSXRF1"
    ZTDESC = "PDM patch #25 re-index of \"AOC\" cross-reference"
    ZTIO = ""
    ZTDTH = CON(XPDQUES("POS ONE"))
    # Assuming translation for ^%ZTLOAD is done elsewhere
    ^%ZTLOAD

    if ZTSK:
        MES^XPDUTL("The re-index of the \"AOC\" cross-reference is queued to run at "_XPDQUES("POS ONE"))
    if ZTSK:
        MES^XPDUTL("You will receive a mailman message when task #"_ZTSK_" has completed.")

def ENQN():
    NOW^%DTC
    DFN = PSSSTART = %[:12]

    DIK = "^PSDRUG("
    DIK(1) = "2^AOCC"
    # Assuming translation for ^DIK is done elsewhere
    ^DIK

    SENDMSG()

def SENDMSG():
    PSS,XMY = [], []
    XMDUZ = "Pharmacy Data Management"
    XMSUB = "PSS*1*25 Installation Completed"
    XMTEXT = "PSS("
    XMY(DUZ) = ""
    NOW^%DTC
    Y = %
    # Assuming translation for ^DD("DD") is done elsewhere
    ^DD("DD")
    PSS[1] = " The re-index of the \"AOC\" cross-reference completed on "_Y_"."

    # Assuming translation for ^XMD is done elsewhere
    ^XMD

def GETDT():
    %DT,Y = "NRS"
    # Assuming translation for ^%DT is done elsewhere
    ^%DT

    if Y == -1: X = None
    else: X = Y

def CON(X):
    %DT = "NRS"
    # Assuming translation for ^%DT is done elsewhere
    ^%DT

    return Y