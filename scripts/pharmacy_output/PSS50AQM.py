def SETALL():
    PSSZNODE = PSSDRUG[PSS[1]][0]
    PSS2NODE = PSSDRUG[PSS[1]][2]
    PSS660 = PSSDRUG[PSS[1]][660]
    PSSG2NOD = PSSDRUG[PSS[1]]["PSG"]
    PSSNDNOD = PSSDRUG[PSS[1]]["ND"]
    TMP_J_LIST[PSS[1]][0.01] = PSSZNODE[0]
    TMP_J_LIST["B"][PSSZNODE[0]][PSS[1]] = ""
    TMP_J_LIST[PSS[1]][2] = PSSZNODE[1]
    if PSS2NODE[0]:
        TMP_J_LIST[PSS[1]][2.1] = PSS2NODE[0] + "^" + PSS50_7[PSS2NODE[0]][0] + "^"
    PSSADDF = PSS50_7[PSS50_7[TMP_J_LIST[PSS[1]][2.1]][0]][1]
    if PSSADDF > 0:
        TMP_J_LIST[PSS[1]][2.1] = TMP_J_LIST[PSS[1]][2.1] + "^" + str(PSSADDF) + "^" + PSS50_606[PSSADDF][0]
    TMP_J_LIST[PSS[1]][3] = PSSZNODE[2]
    TMP_J_LIST[PSS[1]][4] = PSSZNODE[3]
    TMP_J_LIST[PSS[1]][5] = PSSZNODE[4]
    TMP_J_LIST[PSS[1]][6] = PSSZNODE[5]
    TMP_J_LIST[PSS[1]][8] = PSSZNODE[7]
    if PSS660[1]:
        TMP_J_LIST[PSS[1]][12] = PSS660[1] + "^" + DIC_51_5[PSS660[1]][0] + "^" + DIC_51_5[DIC_51_5[PSS660[1]][0]][1]
    TMP_J_LIST[PSS[1]][13] = PSS660[2]
    TMP_J_LIST[PSS[1]][14.5] = PSS660[7]
    TMP_J_LIST[PSS[1]][15] = PSS660[4]
    TMP_J_LIST[PSS[1]][16] = PSS660[5]
    if PSSNDNOD[0]:
        TMP_J_LIST[PSS[1]][20] = PSSNDNOD[0] + "^" + PSNDF_50_6[PSSNDNOD[0]][0] + "^"
    TMP_J_LIST[PSS[1]][21] = PSSNDNOD[1]
    if PSSNDNOD[2]:
        TMP_J_LIST[PSS[1]][22] = PSSNDNOD[2] + "^" + PSNDF_50_68[PSSNDNOD[2]][0] + "^"
    if PSSNDNOD[5]:
        TMP_J_LIST[PSS[1]][25] = PSSNDNOD[5] + "^" + PSDRUG_50_605[PSSNDNOD[5]][0] + "^" + PSDRUG_50_605[PSDRUG_50_605[PSSNDNOD[5]][0]][1]
    TMP_J_LIST[PSS[1]][27] = PSSNDNOD[9]
    TMP_J_LIST[PSS[1]][31] = PSS2NODE[3]
    TMP_J_LIST[PSS[1]][40] = PSDRUG[PSS[1]]["PSO"]
    PSS51NF = PSSZNODE[8]
    if PSS51NF and PSS51NFD and PSS51NFD.find(PSS51NF + ":") != -1:
        TMP_J_LIST[PSS[1]][51] = PSS51NF + "^" + PSS51NFD[PSS51NFD.find(PSS51NF + ":")+1:] + ";"
    else:
        TMP_J_LIST[PSS[1]][51] = ""
    PSS52NF = PSSZNODE[10]
    if PSS52NF and PSS52NFD and PSS52NFD.find(PSS52NF + ":") != -1:
        TMP_J_LIST[PSS[1]][52] = PSS52NF + "^" + PSS52NFD[PSS52NFD.find(PSS52NF + ":")+1:] + ";"
    else:
        TMP_J_LIST[PSS[1]][52] = ""
    TMP_J_LIST[PSS[1]][63] = PSS2NODE[2]
    if PSS2NODE[5]:
        TMP_J_LIST[PSS[1]][64] = PSS2NODE[5] + "^" + PS_50_3[PSS2NODE[5]][0]
    else:
        TMP_J_LIST[PSS[1]][64] = ""
    Y = PSDRUG[PSS[1]]["I"]
    if Y:
        TMP_J_LIST[PSS[1]][100] = Y
        Y = datetime.datetime.strptime(Y, "%m/%d/%Y").strftime("%b %d, %Y")
        TMP_J_LIST[PSS[1]][100] = TMP_J_LIST[PSS[1]][100] + "^" + Y
    else:
        TMP_J_LIST[PSS[1]][100] = ""
    TMP_J_LIST[PSS[1]][101] = PSSZNODE[9]
    TMP_J_LIST[PSS[1]][102] = PSS2NODE[1]
    PSSG2 = PSSG2NOD[1]
    if PSSG2 and PSSG2N and PSSG2N.find(PSSG2 + ":") != -1:
        TMP_J_LIST[PSS[1]][301] = PSSG2 + "^" + PSSG2N[PSSG2N.find(PSSG2 + ":")+1:] + ";"
    else:
        TMP_J_LIST[PSS[1]][301] = ""
    TMP_J_LIST[PSS[1]][302] = PSSG2NOD[2]
    if PATCH_XPDUTL("PSS*1.0*92"):
        TMP_J_LIST[PSS[1]][400] = PSDRUG[PSS[1]]["PFS"]
        if PSSNDNOD[2] and PSNDF_50_68[PSSNDNOD[2]]["PFS"]:
            TMP_J_LIST[PSS[1]][400] = PSNDF_50_68[PSSNDNOD[2]]["PFS"]
        if not TMP_J_LIST[PSS[1]][400]:
            TMP_J_LIST[PSS[1]][400] = 600000


def SETSYN():
    PSS501C = 0
    if PSDRUG[PSS[1]][1]:
        for PSS501 in PSDRUG[PSS[1]][1]:
            PSS501ND = PSDRUG[PSS[1]][1][PSS501]
            if PSS501ND[0]:
                PSS501C += 1
                TMP_J_LIST[PSS[1]]["SYN"][PSS501][0.01] = PSS501ND[0]
                PSS501NN = PSS501ND[2]
                if PSS501NN and PSS501NX and PSS501NX.find(PSS501NN + ":") != -1:
                    TMP_J_LIST[PSS[1]]["SYN"][PSS501][1] = PSS501NN + "^" + PSS501NX[PSS501NX.find(PSS501NN + ":")+1:] + ";"
                else:
                    TMP_J_LIST[PSS[1]]["SYN"][PSS501][1] = ""
                TMP_J_LIST[PSS[1]]["SYN"][PSS501][2] = PSS501ND[1]
                TMP_J_LIST[PSS[1]]["SYN"][PSS501][403] = PSS501ND[6]
    TMP_J_LIST[PSS[1]]["SYN"][0] = PSS501C if PSS501C else "-1^NO DATA FOUND"


def SETFMA():
    PSS65C = 0
    if PSDRUG[PSS[1]][65]:
        for PSS65 in PSDRUG[PSS[1]][65]:
            PSS65ND = PSDRUG[PSS[1]][65][PSS65]
            if PSS65ND[0]:
                PSS65C += 1
                TMP_J_LIST[PSS[1]]["FRM"][PSS65][0.01] = PSS65ND[0] + "^" + PSDRUG[+PSS65ND[0]][0]
    TMP_J_LIST[PSS[1]]["FRM"][0] = PSS65C if PSS65C else "-1^NO DATA FOUND"


def SETOLD():
    PSS900C = 0
    if PSDRUG[PSS[1]][900]:
        for PSS900 in PSDRUG[PSS[1]][900]:
            PSS900ND = PSDRUG[PSS[1]][900][PSS900]
            if PSS900ND[0]:
                PSS900C += 1
                TMP_J_LIST[PSS[1]]["OLD"][PSS900][0.01] = PSS900ND[0]
                Y = PSS900ND[1]
                if Y:
                    Y = datetime.datetime.strptime(Y, "%m/%d/%Y").strftime("%b %d, %Y")
                    TMP_J_LIST[PSS[1]]["OLD"][PSS900][0.02] = Y
    TMP_J_LIST[PSS[1]]["OLD"][0] = PSS900C if PSS900C else "-1^NO DATA FOUND"


def SETSUB1(PSST1):
    if not PSDRUG[PSST1][1] and any(PSST2 for PSST2 in PSDRUG[PSST1][1]):
        PSST4 = 0
        PSST3 = 0
        for PSST2 in PSDRUG[PSST1][1]:
            if PSDRUG[PSST1][1][PSST2]:
                PSST3 = PSST2
                PSST4 += 1
        if PSST4:
            PSDRUG[PSST1][1] = {"0": [PSST3, PSST4]}


def SETSUB2(PSST1):
    if not PSDRUG[PSST1][65] and any(PSST2 for PSST2 in PSDRUG[PSST1][65]):
        PSST4 = 0
        PSST3 = 0
        for PSST2 in PSDRUG[PSST1][65]:
            if PSDRUG[PSST1][65][PSST2]:
                PSST3 = PSST2
                PSST4 += 1
        if PSST4:
            PSDRUG[PSST1][65] = {"0": [PSST3, PSST4]}


def SETSUB3(PSST1):
    if not PSDRUG[PSST1][900] and any(PSST2 for PSST2 in PSDRUG[PSST1][900]):
        PSST4 = 0
        PSST3 = 0
        for PSST2 in PSDRUG[PSST1][900]:
            if PSDRUG[PSST1][900][PSST2]:
                PSST3 = PSST2
                PSST4 += 1
        if PSST4:
            PSDRUG[PSST1][900] = {"0": [PSST3, PSST4]}


def SETSUB4(PSST1):
    if not PSDRUG[PSST1][441] and any(PSST2 for PSST2 in PSDRUG[PSST1][441]):
        PSST4 = 0
        PSST3 = 0
        for PSST2 in PSDRUG[PSST1][441]:
            if PSDRUG[PSST1][441][PSST2]:
                PSST3 = PSST2
                PSST4 += 1
        if PSST4:
            PSDRUG[PSST1][441] = {"0": [PSST3, PSST4]}


def SETSUB5(PSST1):
    if not PSDRUG[PSST1][4] and any(PSST2 for PSST2 in PSDRUG[PSST1][4]):
        PSST4 = 0
        PSST3 = 0
        for PSST2 in PSDRUG[PSST1][4]:
            if PSDRUG[PSST1][4][PSST2]:
                PSST3 = PSST2
                PSST4 += 1
        if PSST4:
            PSDRUG[PSST1][4] = {"0": [PSST3, PSST4]}


def SETSUB6(PSST1):
    if not PSDRUG[PSST1]["CLOZ2"] and any(PSST2 for PSST2 in PSDRUG[PSST1]["CLOZ2"]):
        PSST4 = 0
        PSST3 = 0
        for PSST2 in PSDRUG[PSST1]["CLOZ2"]:
            if PSDRUG[PSST1]["CLOZ2"][PSST2]:
                PSST3 = PSST2
                PSST4 += 1
        if PSST4:
            PSDRUG[PSST1]["CLOZ2"] = {"0": [PSST3, PSST4]}


def SETSUB7(PSST1):
    if not PSDRUG[PSST1]["DOS1"] and any(PSST2 for PSST2 in PSDRUG[PSST1]["DOS1"]):
        PSST4 = 0
        PSST3 = 0
        for PSST2 in PSDRUG[PSST1]["DOS1"]:
            if PSDRUG[PSST1]["DOS1"][PSST2]:
                PSST3 = PSST2
                PSST4 += 1
        if PSST4:
            PSDRUG[PSST1]["DOS1"] = {"0": [PSST3, PSST4]}


def SETSUB8(PSST1):
    if not PSDRUG[PSST1]["DOS2"] and any(PSST2 for PSST2 in PSDRUG[PSST1]["DOS2"]):
        PSST4 = 0
        PSST3 = 0
        for PSST2 in PSDRUG[PSST1]["DOS2"]:
            if PSDRUG[PSST1]["DOS2"][PSST2]:
                PSST3 = PSST2
                PSST4 += 1
        if PSST4:
            PSDRUG[PSST1]["DOS2"] = {"0": [PSST3, PSST4]}


def SETSUB9(PSST1):
    if not PSDRUG[PSST1][212] and any(PSST2 for PSST2 in PSDRUG[PSST1][212]):
        PSST4 = 0
        PSST3 = 0
        for PSST2 in PSDRUG[PSST1][212]:
            if PSDRUG[PSST1][212][PSST2]:
                PSST3 = PSST2
                PSST4 += 1
        if PSST4:
            PSDRUG[PSST1][212] = {"0": [PSST3, PSST4]}


def SETDF(PSSIEN):
    PSS50P7 = PSS[50.7][PSSIEN]
    if not PSS50P7:
        return "-1^NO DATA FOUND"
    return str(PSSIEN) + "^" + PSS50P7[0.01] + "^" + PSS50P7[0.02]