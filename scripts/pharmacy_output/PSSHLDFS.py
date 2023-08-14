def ENP(PSSHLDRG, PSSACT):
    SPNAM = "PSS MFNM01 SERVER"
    VR = ord(101)["B", SPNAM, 0
    if not VR:
        print("Drug Update Protocol " + SPNAM + " is NOT Installed.")
        return
    XX = 0
    while XX:
        PSSD = PS[58.7][XX]
        if not PSSD:
            continue
        PSSNM = PSSD[0]
        DNSNAM = PSSD[1]
        DNSPORT = PSSD[2]
        if not PSSNM or not DNSNAM or not DNSPORT:
            continue
        VR = PSSD[3]
        if VR and VR < DT:
            continue
        VR = PSSD[4]
        if VR == "X" or not VR:
            continue
        PSSHLDRG = int(PSSHLDRG)
        PSSACT = str(PSSACT)
        if PSSHLDRG:
            PROCESS1(SPNAM, PSSHLDRG, PSSACT, DNSNAM, DNSPORT)

def PROCESS1(SPNAM, DRG, PSSACT, DNSNAM, DNSPORT):
    PSSHLFS = HL["FS"]
    PSSHLCS = HL["ECH"][0]
    PSSHLSCS = HL["ECH"][3]
    PSSFIEN = KSP["INST"]
    PSSFNAM = GET1("DIQ", 4, PSSFIEN, ".01")
    HLA = []
    PSSHLCNT = 0
    PSSCNT = 0
    MFI(PSSACT, HLSCOUNT)
    MFE(DRG, PSS50, PSSACT, HLSCOUNT)
    ZFM(DRG, PSS50, PSSACT, HLSCOUNT)
    TRANS()
    HL = {}

def MFI(ACTION, PSSCNT):
    PSSCNT = 1
    SEG = "MFI" + PSSHLFS
    SEG = SEG[:2] + "CDM" + PSSHLCS + "FORMULARY" + PSSHLFS
    SEG = SEG[:4] + (ACTION if ACTION == "MAD" else "UPD") + PSSHLFS
    SEG = SEG[:7] + "NE"
    PSSARRAY["HLS"][PSSCNT] = SEG
    STORE(PSSARRAY, PSSCNT)
    PSSARRAY = {}
    PSSCNT = PSSCNT + 1

def MFE(DRG, FILE50, ACTION, PSSCNT):
    SEG = "MFE" + PSSHLFS + ACTION
    SEG = SEG[:5] + GIVECODE(DRG, PSSHLCS) + PSSHLFS
    SEG = SEG[:6] + "CE"
    PSSARRAY["HLS"][PSSCNT] = SEG
    STORE(PSSARRAY, HLSCOUNT)
    PSSARRAY = {}
    PSSCNT = PSSCNT + 1

def ZFM(DRG, FILE50, ACTION, PSSCNT):
    NDF = int(FILE50["ND"][2])
    SCHED = int(FILE50[0][3])
    SCHED = SCHED if (SCHED >= 1 and SCHED <= 5) else "U"
    SEG = "ZFM" + PSSHLFS + (ACTION if ACTION == "MAD" else "D" if ACTION == "MDL" else "C")
    SEG = SEG[:3] + GIVECODE(DRG, PSSHLCS) + GENDRG
    SEG = SEG[:4] + GET1("DIQ", 50.7, PSSOI, ".01")
    SEG = SEG[:5] + SCHED
    SEG = SEG[:7] + PSSFNAM + PSSHLCS + "D" + PSSHLCS + PSSFIEN
    PSSSYN = ""
    II = 0
    while II:
        ND = FILE50[1][II]
        if ND[0] and ND[3] == 0:
            PSSSYN = ND[0]
            break
    if PSSSYN:
        SEG = SEG[:8] + PSSSYN
    X = FILE50[0][2]
    if X:
        PSSDOSF = GET1("DIQ", 50.606, X, ".01")
    SEG = SEG[:9] + PSSDOSF
    PSSDSQ = FILE50["DOS"]
    if PSSDSQ:
        SEG = SEG[:10] + PSSDSQ[0] + PSSHLFS + FILE50[50.607][PSSDSQ[1]][0]
    elif PSSDRINF[3]:
        SEG = SEG[:10] + PSSDRINF[3] + PSSHLFS + PSSDRINF[5]
    if PSSCLASS:
        C = []
        C.append("")
        C.append("")
        C.append(1)
        C[1] = GET1("DIQ", 50.605, PSSCLASS, 1)
        CLASSNAM = C[1]
        if CLASSNAM:
            SEG = SEG[:15] + CLASSNAM
    PSSCPDU = int(FILE50[660][6])
    if PSSCPDU:
        SEG = SEG[:16] + PSSCPDU
    SEG = SEG[:18] + FILE50[2][4]
    PSSARRAY["HLS"][PSSCNT] = SEG
    return

def GIVECODE(ID, CS):
    DRGID = ""
    DRGNM = ""
    DRGNM2 = ""
    DRGSTR = ""
    DRUGND = ""
    if ID in DRUG:
        DRUGND = DRUG[ID][0]
        DRGID = DRUGND[2]
        DRGNM = DRUG[ID][0]
        DRGSTR = str(ID) + CS + DRGNM + CS + "99PSD"
        DRGNM2 = DRUGND[1]
        DRGSTR = DRGSTR[:3] + (CS + DRGID + CS + DRGNM2 + CS + "99PSP") if DRGID else ""
    return DRGSTR

def STORE(SEGMENT, NODE):
    NEXTND = len(TMP["HLS"]) + 1
    for I in range(1, NODE+1):
        if SEGMENT["HLS"][I]:
            TMP["HLS"][NEXTND] = SEGMENT["HLS"][I]
            NEXTND = NEXTND + 1

def TRANS():
    HLP = ""
    HLP["SUBSCRIBER"] = "^^^^~" + DNSNAM + ":" + DNSPORT + "~DNS"
    print("Generating HL7 message and Sending " + DRG + "-" + DRUG[DRG][0])
    GENERATE(SPNAM, "GM", 1, PSSMFSND, "", HLP)
    if PSSMFSND[1]:
        print("Drug Update transmission to PADE(s) failed because the HL7 Message could not generate.")
        print("  Reason(s): " + PSSMFSND[1] + " " + PSSMFSND[2])

ENP(PSSHLDRG, PSSACT)