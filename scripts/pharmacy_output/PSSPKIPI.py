# BIR/MHA-DEA/PKI Post-Inst DEA-CS FED SCH mismatch report
# 08/08/02
# 1.0;PHARMACY DATA MANAGEMENT;**61**;9/30/97
# Reference to ^PSNDF(50.68 supported by DBIA 3735

def PSSPKIPI():
    ZZ = "PSSPKI"
    XTMP = dict()
    PSSX, PSSD, PSSJ, PSSK, PSSN, NDR = '', '', '', '', '', ''
    PSSX = ''
    while PSSX != '':
        PSSX = next(iter(PSDRUG))
        if PSSX == '':
            break
        PSSN = 0
        while PSSN != 0:
            PSSN = next(iter(PSDRUG[PSSX]))
            if PSSN == 0:
                break
            if PSSN in PSDRUG:
                if PSDRUG[PSSN]['I'] and PSDRUG[PSSN]['I'] < DT:
                    continue
                PSSD = PSDRUG[PSSN][0]
                if PSSD == '':
                    GCS()
                    continue
                if PSSD[1] or PSSD[2] or PSSD[3] or PSSD[4] or PSSD[5] or PSDRUG[PSSN][2][2] == 'N':
                    PSSJ = 0
                    NDR = ''
                    if PSSD['A'] and PSSD['C'] and (int(PSSD) == 2 or int(PSSD) == 3):
                        PSSJ = 3
                    else:
                        PSSL = ''
                        PSSK = PSDRUG[PSSN]['ND'][2]
                        if not PSSK:
                            PSSJ = 2
                        else:
                            PSSL = get1(50.68, PSSK, 19, 'I')
                            if PSSL:
                                PSSL = PSSL[0] + ('C' if 'n' in PSSL else 'A' if int(PSSL) == 2 or int(PSSL) == 3 else '')
                                if len(PSSL) == 1 and PSSD[PSSL]:
                                    continue
                                if PSSD[PSSL[0]] and PSSD[PSSL[1]]:
                                    continue
                                PSSJ = 1
                                NDR = get1(50.68, PSSK, .01)
                                PSSL = get1(50.68, PSSK, 19, 'I')
                    REP()
    REP4()
    SM()

def GCS():
    PSSL = ''
    PSSK = PSDRUG[PSSN]['ND'][2]
    if PSSK:
        PSSL = get1(50.68, PSSK, 19, 'I')
        if PSSL:
            PSSL = PSSL[0] + ('C' if 'n' in PSSL else 'A' if int(PSSL) == 2 or int(PSSL) == 3 else '')
            if int(PSSL):
                PSDRUG[PSSN][0] = PSSL

def REP():
    XTMP[ZZ][PSSJ][PSSX] = NDR + "^" + PSDRUG[PSSN][1] + "^" + PSSD + ("^" + PSSL if PSSJ == 1 else "")

def SM():
    TMP = dict()
    XMY = dict()
    for J in [1, 2, 3, 4]:
        if J in XTMP[ZZ]:
            S1 = ""
            S2 = ""
            K = ""
            UL = "=" * 79
            if J == 1:
                TMP[J] = [
                    "The following active Controlled Substances were identified as having a",
                    "discrepancy between the CS FEDERAL SCHEDULE in the VA PRODUCT file (#50.68)",
                    "and the DEA,SPECIAL HDLG code in the DRUG file (#50). You may wish to update",
                    "the DEA,SPECIAL HDLG code for these drugs.",
                    "",
                    "PLEASE NOTE:  The CS FEDERAL SCHEDULE will only identify DEA, SPECIAL HDLG",
                    "",
                    "codes of 1, 2A, 2C, 3A, 3C, 4, or 5.  In addition to these codes, you may",
                    "also use other DEA, SPECIAL HDLG codes such as L, P,R, S, etc., as needed.",
                    "",
                ]
                XX = 11
            if J == 2:
                TMP[J] = [
                    "The following active Controlled Substances have not been matched to NDF.",
                    "You may wish to match these drugs.",
                    "",
                    "GENERIC NAME" + " " * 42 + "VA CLASS" + " " * 10 + "CURR DEA, SPECIAL HDLG",
                    UL,
                    "",
                ]
                XX = 9
            if J == 3:
                TMP[J] = [
                    "The following active drugs are defined as Controlled Substances, but",
                    "not classified correctly as Narcotics or Non-Narcotics.",
                    "Please make sure they are defined correctly.",
                    "",
                    "GENERIC NAME" + " " * 42 + "VA CLASS" + " " * 10 + "CURR DEA, SPECIAL HDLG",
                    UL,
                    "",
                ]
                XX = 9
            if J == 4:
                TMP[J] = [
                    "The following pharmacy orderable items are associated with active dispense",
                    "drugs that have a discrepancy within their DEA Special Hdlg fields. Please",
                    "correct all entries to identify these orderable items with a specific",
                    "Controlled Substance schedule.",
                    "",
                    "PHARMACY ORDERABLE ITEM",
                    "   IEN   DISPENSE DRUG" + " " * 36 + "DEA SPEC. HDLG" + " " * 15 + "CS FED. SCHE.",
                    UL,
                    "",
                ]
                XX = 11
            for K in XTMP[ZZ][J]:
                if J != 4:
                    QQ = XTMP[ZZ][J][K]
                    if J == 1:
                        PDET()
                    else:
                        TMP[J].append(
                            "   "
                            + K
                            + " " * (42 - len(K))
                            + QQ[1]
                            + " " * (43 - len(QQ[1]))
                            + QQ[2]
                        )
                else:
                    DOS = ""
                    DOS = get1(50.7, K[1], 2)
                    if DOS:
                        DOS = get1(50.606, DOS, 0)
                    TMP[J].append(K[0] + " " + DOS)
                    for I in XTMP[ZZ][J][K]:
                        QQ = XTMP[ZZ][J][K][I]
                        TMP[J].append(
                            "   "
                            + I
                            + " " * (6 - len(I))
                            + QQ[1]
                            + " " * (43 - len(QQ[1]))
                            + QQ[2]
                            + " " * (13 - len(QQ[2]))
                            + QQ[3]
                        )
                TMP[J].append("")
                XX += 1
            XMY[DUZ] = ""
            XMDUZ = "Patch # - DEA/PKI Post-Install"
            if "PSNMGR" in XUSEC:
                for I in XUSEC["PSNMGR"]:
                    XMY[I] = ""
            if J == 1:
                XMSUB = "CS FEDERAL SCHEDULE AND DEA, SPECIAL HDLG DISCREPANCIES"
            if J == 2:
                XMSUB = "CONTROLLED SUBSTANCES NOT MATCHED"
            if J == 3:
                XMSUB = "CONTROLLED SUBSTANCES NOT SET CORRECTLY"
            if J == 4:
                XMSUB = "DISCREPANCY IN DEA WITHIN DRUGS TIED TO AN OI"
            XMTEXT = TMP[J]
            XMDUZ = "Patch # - DEA/PKI Post-Install"
            DIFROM()
            XMDUZ = ""
            TMP[J] = []
    XTMP[ZZ] = []
    TMP = []
    XMY = []
    XMDUZ = ""

def PDET():
    TMP[J].append("GENERIC NAME: " + K)
    TMP[J].append("VA PRODUCT NAME: " + QQ[0])
    TMP[J].append("VA CLASS: " + QQ[1])
    TMP[J].append("CURRENT DEA, SPECIAL HDLG: " + QQ[2])
    TMP[J].append("CS FEDERAL SCHEDULE: " + QQ[3])
    TMP[J].append("")
    return

def REP4():
    OI = ""
    for PSSL in PSDRUG:
        if PSSL in PSDRUG:
            if PSDRUG[PSSL][0]['A'] or PSDRUG[PSSL][0]['C']:
                if PSDRUG[PSSL][0][1] or PSDRUG[PSSL][0][2] or PSDRUG[PSSL][0][3] or PSDRUG[PSSL][0][4] or PSDRUG[PSSL][0][5] or PSDRUG[PSSL][2][2] == 'N':
                    PSSK = PSDRUG[PSSL]['ND'][2]
                    if PSSK:
                        PSSK = get1(50.68, PSSK, 19, 'I')
                        if PSSK:
                            AR = [OI, PSSL, PSSN, PSDRUG[PSSL][0], PSSD, PSSK]
                            if PSDRUG[PSSL][0]['A']:
                                I = 1
                            if PSDRUG[PSSL][0]['C']:
                                J = 1
                            if J and I:
                                I = ""
                                for I in AR:
                                    if I:
                                        XTMP[ZZ][4][AR[0:2]][I] = AR[2:6]