def DRG(DRG, NEW):
    ACT = []
    CNT = 0
    DOS = None
    DOSF = None
    DRG0 = ""
    DRG2 = ""
    DRG3 = ""
    DRG6 = ""
    DRG60 = ""
    DRGN = ""
    DRGZ = ""
    DRGZ1 = ""
    INT = []
    MEDRT = ""
    PSSRESLT = []
    PSSOPTNS = ""
    PKG = ""
    PROT = 0
    SYN = []
    XX = 0
    HL = []
    HLA = []

    PROT = next((i for i, e in enumerate(ORD) if e == "PSS HUI DRUG UPDATE"), 0)
    if PROT == 0:
        print("Drug Update Protocol NOT Installed")
        return

    INIT(PROT, HL)
    if HL:
        return

    HL["ECH"] = "^~\\"
    CNT += 1
    HLA[CNT] = "MFI|50^DRUG^99PSD"
    HLA[CNT][6] = "NE"
    CNT += 1
    HLA[CNT] = "MFA|" + ("MAD" if NEW else "MUP")
    CNT += 1
    HLA[CNT] = "MFE|" + ("MAD" if NEW else "MUP")
    HLA[CNT][5] = DRG + "^" + DRG0[0] + "^99PSD"
    CNT += 1
    HLA[CNT] = "ZPA|" + DRG2[3] + "|" + DRG0[8] + "|" + HLDATE(PSDRUG[DRG][I], "TS") + "|"
    HLA[CNT] += DRG2[2] + "|" + DRG0[9] + "|" + DRG0[1] + "|" + DRG0[2] + "|" + DRG0[5] + "|" + DRG0[7] + "|" + DRG0[10]
    CNT += 1
    HLA[CNT] = "ZPB|" + (DRG2[0] + "^" + PS[50.7][DRG2[0]][0] + "^PSD50.7" if DRG2[0] and PS[50.7][DRG2[0]] else "") + "|"
    DOSF = DRG2[0] + "^" + PS[50.7][DRG2[0]][1] + "^PSD50.606" if DRG2[0] and PS[50.7][DRG2[0]][1] else ""
    MEDRT = DRG2[0] + "^" + PS[50.7][DRG2[0]][5] + "^PSD51.2" if DRG2[0] and PS[50.7][DRG2[0]][5] else ""
    HLA[CNT] += DOSF + "|" + MEDRT + "|"
    HLA[CNT] += (DRGN[2] + "^" + PSNDF[50.68][DRGN[2]][0] + "^PSD50.68" if DRGN[2] and PSNDF[50.68][DRGN[2]] else "") + "|"
    HLA[CNT] += DRG60[7] + "|" + DRG3[0] + "|" + DRG6[0] + "|" + HLDATE(DRG60[8], "TS") + "|"
    HLA[CNT] += (DRGZ[0] + "^" + LAB[60][DRGZ[0]][0] + "^LAB60" if DRGZ[0] and LAB[60][DRGZ[0]] else "")
    CNT += 1
    HLA[CNT] = "ZPC|" + (DRGZ[2] + "^" + LAB[61][DRGZ[2]][0] + "^LAB61" if DRGZ[2] and LAB[61][DRGZ[2]] else "") + "|"
    HLA[CNT] += DRGZ1[0] + "|" + DRGZ1[1] + "|" + DRG[DRG][DOS] + "|"
    DOS = DRG[DRG][DOS]
    HLA[CNT] += (DOS + "^" + PS[50.607][DOS][0] + "^PSD50.607" if DOS and PS[50.607][DOS] else "") + "|"
    HLA[CNT] += DRG60[2] + "|" + DRG60[5]
    CNT += 1
    SYN = []
    for XX, _ in enumerate(DRG[DRG][1]):
        SYN = DRG[DRG][1][XX]
        CNT += 1
        HLA[CNT] = "ZPD|" + SYN[0] + "|" + SYN[1] + "|"
        HLA[CNT] += (SYN[2] + "^" + ("TRADE NAME" if SYN[2] == 0 else "QUICK CODE" if SYN[2] == 1 else "DRUG ACCOUNTABILITY" if SYN[2] == "D" else "CONTROLLED SUBSTANCE" if SYN[2] == "C" else "") + "^PSD51.5" if SYN[2] else "") + "|"
        HLA[CNT] += SYN[3] + "|" + (SYN[4] + "^" + DIC[51.5][SYN[4]][0] + "^" + DIC[51.5][SYN[4]][1] + "^PSD51.5" if SYN[4] and DIC[51.5][SYN[4]] else "") + "|"
        HLA[CNT] += SYN[5] + "|" + SYN[6] + "|" + SYN[7] + "|" + SYN[8]
        SYN = []
    ACT = []
    for XX, _ in enumerate(DRG[DRG][4]):
        ACT = DRG[DRG][4][XX]
        CNT += 1
        HLA[CNT] = "ZPE|" + HLDATE(ACT[0], "TS") + "|" + ("E^EDIT" if ACT[1] else "") + "|"
        INT = ACT[2] + "^" + VA[200][ACT[2]][0] + "^VA200" if ACT[2] and VA[200][ACT[2]] else ""
        HLA[CNT] += INT + "|" + ACT[3] + "|" + ACT[4] + "|" + ACT[5]
        INT = []
        ACT = []
    ACT = []
    for XX, _ in enumerate(DRG[DRG][DOS1]):
        ACT = DRG[DRG][DOS1][XX]
        CNT += 1
        HLA[CNT] = "ZPF|" + ACT[0] + "|" + ACT[1] + "|" + ("I^INPATIENT" if ACT[2] == "I" else "O^OUTPATIENT" if ACT[2] == "O" else "IO^INPATIENT/OUTPATIENT" if ACT[2] == "IO" or ACT[2] == "OI" else "") + "|" + ACT[3]
        ACT = []
    ACT = []
    for XX, _ in enumerate(DRG[DRG][CLOZ2]):
        ACT = DRG[DRG][CLOZ2][XX]
        CNT += 1
        HLA[CNT] = "ZPG|" + (ACT[0] + "^" + LAB[60][ACT[0]][0] + "^LAB60" if ACT[0] and LAB[60][ACT[0]] else "") + "|" + ACT[1] + "|"
        HLA[CNT] += (ACT[2] + "^" + LAB[61][ACT[2]][0] + "^LAB61" if ACT[2] and LAB[61][ACT[2]] else "") + "|" + (ACT[3] + "^WBC" if ACT[3] == 1 else "2^ANC" if ACT[3] == 2 else "")
        ACT = []
    ACT = []
    for XX, _ in enumerate(DRG[DRG][DOS2]):
        ACT = DRG[DRG][DOS2][XX]
        CNT += 1
        HLA[CNT] = "ZPH|" + ACT[0] + "|"
        PKG = ACT[1] + "^OUTPATIENT" if ACT[1] == "O" else "I^INPATIENT" if ACT[1] == "I" else "IO^INPATIENT/OUTPATIENT" if ACT[1] == "IO" or ACT[1] == "OI" else ""
        HLA[CNT] += PKG + "|" + ACT[2]
        PKG = []
        ACT = []

    GENERATE("PSS HUI DRUG UPDATE", "LM", 1, PSSRESLT, "", PSSOPTNS)
    return

def PSN():
    PROT = next((i for i, e in enumerate(ORD) if e == "PSS HUI DRUG UPDATE"), 0)
    if PROT == 0:
        return
    INIT(PROT, HL)
    if HL:
        return
    for PSN in TMP:
        DRG(PSN)
    return