def SETWS():
    global PSS, LIST
    LIST = ""
    PSS = [1]
    while PSS[0]:
        PSS[0] = next((x for x in range(PSS[0] + 1, len(PSDRUG)) if PSDRUG[x][0]), 0)
        if not PSS[0]:
            break
        if PSDRUG[PSS[0]][0]:
            continue
        if PSSFL and PSDRUG[PSS[0]]["I"] and PSDRUG[PSS[0]]["I"] <= PSSFL:
            continue
        if PSSRTOI == 1 and not PSDRUG[PSS[0]][2]:
            continue
        if PSSPK:
            PSSZ5 = 0
            for PSSZ6 in range(len(PSSPK)):
                if PSDRUG[PSS[0]][2][2].find(PSSPK[PSSZ6]) != -1:
                    PSSZ5 = 1
                    break
            if PSSPK and not PSSZ5:
                continue
        SETWSL()
    TMP[J][LIST][0] = PSS[0] if PSS[0] else "-1^NO DATA FOUND"

def SETWSL():
    global PSS, LIST
    TMP[J][LIST][PSS[0]][0] = PSDRUG[PSS[0]][0]
    TMP[J][LIST]["B"][PSDRUG[PSS[0]][0]][PSS[0]] = ""
    TMP[J][LIST][PSS[0]][300] = PSDRUG[PSS[0]]["PSG"][0]
    PSSPCAT = PSDRUG[PSS[0]]["PSG"][1]
    if PSSPCAT and PSSPCATS and PSSPCAT + ":" in PSSPCATS:
        TMP[J][LIST][PSS[0]][301] = f"{PSSPCAT}^{PSSPCATS[PSSPCATS.index(PSSPCAT + ":") + len(PSSPCAT + ":"):].split(';')[0]}"
    else:
        TMP[J][LIST][PSS[0]][301] = ""
    TMP[J][LIST][PSS[0]][302] = PSDRUG[PSS[0]]["PSG"][2]

def LOOP():
    global PSS, LIST
    PSS50DD6 = {}
    PSS50ER6 = {}
    FIELD(50, 301, "Z", "POINTER", PSS50DD6, PSS50ER6)
    PSSPCATS = PSS50DD6["POINTER"]
    PSSENCT = 0
    PSS = [0]
    while PSS[0]:
        PSS[0] = next((x for x in range(PSS[0] + 1, len(PSDRUG)) if PSDRUG[x][0]), 0)
        if not PSS[0]:
            break
        if PSDRUG[PSS[0]][0]:
            continue
        if PSSFL and PSDRUG[PSS[0]]["I"] and PSDRUG[PSS[0]]["I"] <= PSSFL:
            continue
        if PSSRTOI == 1 and not PSDRUG[PSS[0]][2]:
            continue
        if PSSPK:
            PSSZ5 = 0
            for PSSZ6 in range(len(PSSPK)):
                if PSDRUG[PSS[0]][2][2].find(PSSPK[PSSZ6]) != -1:
                    PSSZ5 = 1
                    break
            if PSSPK and not PSSZ5:
                continue
        SETWSL()
        PSSENCT += 1
    TMP[J][LIST][0] = PSSENCT if PSSENCT else "-1^NO DATA FOUND"

def SETMRTN():
    global PSS, LIST
    TMP[J][LIST][PSS[0]][0] = TMP["PSSP50"][50][PSS[0]][0]
    TMP[J][LIST]["B"][TMP["PSSP50"][50][PSS[0]][0]][PSS[0]] = ""
    TMP[J][LIST][PSS[0]][17.2] = TMP["PSSP50"][50][PSS[0]][17.2][0] if TMP["PSSP50"][50][PSS[0]][17.2][0] else ""
    TMP[J][LIST][PSS[0]][17.5] = TMP["PSSP50"][50][PSS[0]][17.5]
    TMP[J][LIST][PSS[0]][31] = TMP["PSSP50"][50][PSS[0]][31]

def LOOPMR():
    global PSS, LIST
    PSSENCT = 0
    PSS = [0]
    while PSS[0]:
        PSS[0] = next((x for x in range(PSS[0] + 1, len(PSDRUG)) if PSDRUG[x][0]), 0)
        if not PSS[0]:
            break
        if PSDRUG[PSS[0]][0]:
            continue
        if PSSFL and PSDRUG[PSS[0]]["I"] and PSDRUG[PSS[0]]["I"] <= PSSFL:
            continue
        if PSSRTOI == 1 and not PSDRUG[PSS[0]][2]:
            continue
        if PSSPK:
            PSSZ5 = 0
            for PSSZ6 in range(len(PSSPK)):
                if PSDRUG[PSS[0]][2][2].find(PSSPK[PSSZ6]) != -1:
                    PSSZ5 = 1
                    break
            if PSSPK and not PSSZ5:
                continue
        SETMRTN()
        PSSENCT += 1
    TMP[J][LIST][0] = PSSENCT if PSSENCT else "-1^NO DATA FOUND"

def SETZRO():
    global PSS, LIST
    TMP[J][LIST][PSS[0]][0] = TMP["PSSP50"][50][PSS[0]][0]
    TMP[J][LIST]["B"][TMP["PSSP50"][50][PSS[0]][0]][PSS[0]] = ""
    TMP[J][LIST][PSS[0]][2] = TMP["PSSP50"][50][PSS[0]][2]
    TMP[J][LIST][PSS[0]][3] = TMP["PSSP50"][50][PSS[0]][3]
    TMP[J][LIST][PSS[0]][4] = TMP["PSSP50"][50][PSS[0]][4]
    TMP[J][LIST][PSS[0]][5] = TMP["PSSP50"][50][PSS[0]][5]
    TMP[J][LIST][PSS[0]][6] = TMP["PSSP50"][50][PSS[0]][6]
    TMP[J][LIST][PSS[0]][8] = TMP["PSSP50"][50][PSS[0]][8]
    TMP[J][LIST][PSS[0]][51] = TMP["PSSP50"][50][PSS[0]][51][0] if TMP["PSSP50"][50][PSS[0]][51][0] else ""
    TMP[J][LIST][PSS[0]][52] = TMP["PSSP50"][50][PSS[0]][52][0] if TMP["PSSP50"][50][PSS[0]][52][0] else ""
    TMP[J][LIST][PSS[0]][101] = TMP["PSSP50"][50][PSS[0]][101]

def LOOPZR():
    global PSS, LIST
    PSS50DD7 = {}
    PSS50DD8 = {}
    PSS50ER7 = {}
    PSS50ER8 = {}
    PSS51NFD = ""
    PSS52NFD = ""
    FIELD(50, 51, "Z", "POINTER", PSS50DD7, PSS50ER7)
    PSS51NFD = PSS50DD7["POINTER"]
    FIELD(50, 52, "Z", "POINTER", PSS50DD8, PSS50ER8)
    PSS52NFD = PSS50DD8["POINTER"]
    PSSENCT = 0
    PSS = [0]
    while PSS[0]:
        PSS[0] = next((x for x in range(PSS[0] + 1, len(PSDRUG)) if PSDRUG[x][0]), 0)
        if not PSS[0]:
            break
        if PSDRUG[PSS[0]][0]:
            continue
        if PSSFL and PSDRUG[PSS[0]]["I"] and PSDRUG[PSS[0]]["I"] <= PSSFL:
            continue
        if PSSRTOI == 1 and not PSDRUG[PSS[0]][2]:
            continue
        if PSSPK:
            PSSZ5 = 0
            for PSSZ6 in range(len(PSSPK)):
                if PSDRUG[PSS[0]][2][2].find(PSSPK[PSSZ6]) != -1:
                    PSSZ5 = 1
                    break
            if PSSPK and not PSSZ5:
                continue
        LOOPZRD()
        PSSENCT += 1
    TMP[J][LIST][0] = PSSENCT if PSSENCT else "-1^NO DATA FOUND"

def LOOPZRD():
    global PSS, LIST
    PSSZNODE = PSDRUG[PSS[0]][0]
    PSSPSGND = PSDRUG[PSS[0]]["PSG"]
    TMP[J][LIST][PSS[0]][0] = PSSZNODE[0]
    TMP[J][LIST]["B"][PSSZNODE[0]][PSS[0]] = ""
    PSS51NF = PSSZNODE[8]
    if PSS51NF and PSS51NFD and PSS51NF + ":" in PSS51NFD:
        TMP[J][LIST][PSS[0]][51] = f"{PSS51NF}^{PSS51NFD[PSS51NFD.index(PSS51NF + ":") + len(PSS51NF + ":"):].split(';')[0]}"
    else:
        TMP[J][LIST][PSS[0]][51] = ""
    PSS52NF = PSSZNODE[10]
    if PSS52NF and PSS52NFD and PSS52NF + ":" in PSS52NFD:
        TMP[J][LIST][PSS[0]][52] = f"{PSS52NF}^{PSS52NFD[PSS52NFD.index(PSS52NF + ":") + len(PSS52NF + ":"):].split(';')[0]}"
    else:
        TMP[J][LIST][PSS[0]][52] = ""
    TMP[J][LIST][PSS[0]][101] = PSSZNODE[9]

def LOOPB():
    global PSS, LIST
    PSSENCT = 0
    PSS = [0]
    while PSS[0]:
        PSS[0] = next((x for x in range(PSS[0] + 1, len(PSDRUG)) if PSDRUG[x][0]), 0)
        PSSZNAM = PSDRUG[PSS[0]][0]
        if not PSSZNAM:
            break
        if PSSFL and PSDRUG[PSS[0]]["I"] and PSDRUG[PSS[0]]["I"] <= PSSFL:
            continue
        if PSSRTOI == 1 and not PSDRUG[PSS[0]][2]:
            continue
        if PSSPK:
            PSSZ5 = 0
            for PSSZ6 in range(len(PSSPK)):
                if PSDRUG[PSS[0]][2][2].find(PSSPK[PSSZ6]) != -1:
                    PSSZ5 = 1
                    break
            if PSSPK and not PSSZ5:
                continue
        TMP[J][LIST][PSS[0]][0] = PSSZNAM
        TMP[J][LIST]["B"][PSSZNAM][PSS[0]] = ""
        PSSENCT += 1
    TMP[J][LIST][0] = PSSENCT if PSSENCT else "-1^NO DATA FOUND"

def CSYN():
    global PSSIEN, PSSVAL, LIST
    if not LIST:
        return
    TMP[J][LIST] = {}
    if not PSSIEN or not PSSVAL:
        TMP[J][LIST][0] = "-1^NO DATA FOUND"
        return
    PSSCSNAM = PSDRUG[PSSIEN][0]
    if not PSSCSNAM:
        TMP[J][LIST][0] = "-1^NO DATA FOUND"
        return
    PSSCSX = next((x for x in range(len(PSDRUG[PSSIEN][1])) if PSDRUG[PSSIEN][1][x][0] == PSSVAL), 0)
    if not PSSCSX:
        TMP[J][LIST][0] = "-1^NO DATA FOUND"
        return
    PSSCSSYN = PSDRUG[PSSIEN][1][PSSCSX][0]
    if not PSSCSSYN:
        TMP[J][LIST][0] = "-1^NO DATA FOUND"
        return
    TMP[J][LIST][PSSIEN][0] = PSSCSNAM
    TMP[J][LIST][PSSIEN]["SYN"] = {}
    TMP[J][LIST][PSSIEN]["SYN"][0] = 1
    TMP[J][LIST][PSSIEN]["SYN"][PSSCSX][0] = PSSCSSYN
    TMP[J][LIST][PSSIEN]["SYN"][PSSCSX][403] = PSDRUG[PSSIEN][1][PSSCSX][6]
    TMP[J][LIST]["C"][PSSCSSYN][PSSIEN] = ""
    TMP[J][LIST][0] = 1

def DSPUNT():
    global PSSIEN, PSSIEN2, LIST
    if not LIST:
        return
    TMP[J][LIST] = {}
    if PSSIEN <= 0 or PSSIEN2 <= 0:
        TMP[J][LIST][0] = "-1^NO DATA FOUND"
        return
    PSSDSNAM = PSDRUG[PSSIEN][0]
    if not PSSDSNAM:
        TMP[J][LIST][0] = "-1^NO DATA FOUND"
        return
    PSSDSSYN = PSDRUG[PSSIEN][1][PSSIEN2][0]
    if not PSSDSSYN:
        TMP[J][LIST][0] = "-1^NO DATA FOUND"
        return
    TMP[J][LIST][PSSIEN][0] = PSSDSNAM
    TMP[J][LIST][PSSIEN]["SYN"] = {}
    TMP[J][LIST][PSSIEN]["SYN"][0] = 1
    TMP[J][LIST][PSSIEN]["SYN"][PSSIEN2][0] = PSSDSSYN
    TMP[J][LIST][PSSIEN]["SYN"][PSSIEN2][403] = PSDRUG[PSSIEN][1][PSSIEN2][6]
    TMP[J][LIST]["C"][PSSDSSYN][PSSIEN] = ""
    TMP[J][LIST][0] = 1

def SETSCRN():
    global PSSFL, PSSRTOI, PSSPK, SCR
    if PSSFL > 0:
        if SCR["S"]:
            SCR["S"] += " S PSS5ND=$P($G(^(""I"")),""^"") I PSS5ND=""""!(PSS5ND>PSSFL)"
        else:
            SCR["S"] = "S PSS5ND=$P($G(^(""I"")),""^"") I PSS5ND=""""!(PSS5ND>PSSFL)"
    if PSSRTOI == 1:
        if SCR["S"]:
            SCR["S"] += " I $P($G(^(2)),""^"")"
        else:
            SCR["S"] = "I $P($G(^(2)),""^"")"
    if PSSPK:
        if SCR["S"]:
            SCR["S"] += " S PSSZ3=0 F PSSZ4=1:1:$L(PSSPK) Q:PSSZ3  I $P($G(^(2)),""^"",3)[$E(PSSPK,PSSZ4) S PSSZ3=1"
        else:
            SCR["S"] = "S PSSZ3=0 F PSSZ4=1:1:$L(PSSPK) Q:PSSZ3  I $P($G(^(2)),""^"",3)[$E(PSSPK,PSSZ4) S PSSZ3=1"