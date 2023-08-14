def DOSE(PSSX, PD, TYPE, PSSDFN):
    PSSX = {}
    PSSOIU = TYPE == "I" or TYPE == "U"
    for DLOOP in range(1, len(DRUGS)):
        if DRUGS[DLOOP]["DOS1"]:
            PSSTRN = DRUGS[DLOOP]["DOS"]
            PSSUNITX = DRUGS[DLOOP]["DOS_UNIT"]
            if PSSTRN:
                PSSUNITX = PSSUNITX if PSSUNITX and "/" not in PSSUNITX else ""
                if DRUGS[DLOOP]["I"] and DRUGS[DLOOP]["I"] <= datetime.now().date():
                    continue
                APP()
                PSSDSE = DRUGS[DLOOP][50.7]
                PSSVERB = DRUGS[DLOOP][50.606]["MISC"]
                PSSPREP = DRUGS[DLOOP][50.606]["MISC"]
                PSNNN = next((x["NOUN"] for x in DRUGS[DLOOP][50.606]["NOUN"] if x["NOUN"]), None)
                for DLOOP1 in range(1, len(DRUGS[DLOOP]["DOS1"])):
                    if not DRUGS[DLOOP]["DOS1"][DLOOP1]:
                        continue
                    if PSSOIU and "I" not in DRUGS[DLOOP]["DOS1"][DLOOP1][3]:
                        continue
                    if not PSSOIU and "O" not in DRUGS[DLOOP]["DOS1"][DLOOP1][3]:
                        continue
                    PSSDOSE = DRUGS[DLOOP]["DOS1"][DLOOP1][1]
                    PSSUNTS = DRUGS[DLOOP]["DOS_UNIT"]
                    PSSUDOS = DRUGS[DLOOP]["DOS1"][DLOOP1][1]
                    if PSSDOSE and PSSUDOS:
                        DCNT1 = DCNT1 + 1 if "DCNT1" in locals() else 1
                        LOW[PSSDOSE][PSSUDOS][DCNT1] = ""
                        FORM[PSSDOSE][1 if DRUGS[DLOOP][0][9] == 1 else 0][DCNT1] = PSSUDOS
                        PARN()
                        PSSX[DCNT1] = PSSDOSE + "^" + PSSUNTS + "^" + PSSUDOS + "^" + (PSSNP if "PSSNP" in locals() else PSNNN) + "^^" + str(DLOOP)
    if not PSSX:
        DOSE2()
        return
    PSSLOW = ""
    while PSSLOW in FORM:
        if FORM[PSSLOW]:
            PSSLOW2 = ""
            while PSSLOW2 in FORM[PSSLOW][1]:
                PSSX[PSSLOW4][PSOLC - 1] = PSSX[PSSLOW2]
                del PSSX[PSSLOW2]
    for PSSLOW in LOW:
        PSOLC = 0
        for PSSLOW1 in LOW[PSSLOW]:
            PSOLC += 1
            if PSOLC == 1:
                PSSLOW4 = next(iter(LOW[PSSLOW][PSSLOW1]))
            PSSLOW2 = ""
            while PSSLOW2 in LOW[PSSLOW][PSSLOW1]:
                if PSOLC > 1:
                    PSSX[PSSLOW4][(PSOLC - 1)] = PSSX[PSSLOW2]
                    del PSSX[PSSLOW2]
    PSSHOLD = {}
    for PL in PSSX:
        if isinstance(PL, int):
            PSSHOLD[PSSX[PL][0]][PL] = PSSX[PL]
            if PSSX[PL][1]:
                PL2 = 0
                for PL2 in PSSX[PL][1]:
                    PSSHOLD[PSSX[PL][0]][PL][PL2] = PSSX[PL][1][PL2]
    PSSX = {}
    PSSA = 1
    for PSSZ in PSSHOLD:
        PSSC = 0
        for PSSC in PSSHOLD[PSSZ]:
            PSSX[PSSA] = PSSHOLD[PSSZ][PSSC]
            SLS()
            if DLOOP not in PSSX["DD"]:
                MULTI()
            PSSA += 1
            PSIEN = DLOOP = PSSX[PSSA][5]
            PSSMAX = None
            if TYPE == "O":
                MAX()
            PSSX["DD"][PSIEN] = DRUGS[PSIEN][0] + "^" + DRUGS[PSIEN][660] + "^" + DRUGS[PSIEN][0][9] + "^" + DRUGS[PSIEN][660][8] + "^" + DRUGS[PSIEN]["DOS"] + "^" + PSSUNITX + "^" + DRUGS[PSIEN][50.606] + "^" + PSSMAX
            REQS()
            PSSX["DD"][PSIEN] += "^" + PSSREQS
            DEA(PSIEN)
            PSSX["MISC"] = PSSVERB + "^" + PSSPREP + "^" + DRUGS[PSIEN][50.606][4]
    PSSHOLD = {}
    for PSSDZ in PSSX:
        if "DD" in PSSDZ:
            if isinstance(PSSX[PSSDZ], list):
                PSSHOLD[PSSDZ] = PSSX[PSSDZ]
            else:
                PSIEN = DLOOP = PSSX[PSSDZ][5]
                PSSMAX = None
                if TYPE == "O":
                    MAX()
                PSSHOLD[PSSDZ] = DRUGS[DLOOP][0] + "^" + DRUGS[DLOOP][660] + "^" + DRUGS[DLOOP][0][9] + "^" + DRUGS[DLOOP][660][8] + "^" + DRUGS[DLOOP]["DOS"] + "^" + PSSUNITX + "^" + DRUGS[DLOOP][50.606] + "^" + PSSMAX
                REQS()
                PSSHOLD[PSSDZ] += "^" + PSSREQS
                DEA(DLOOP)
                PSSHOLD["MISC"] = PSSVERB + "^" + PSSPREP + "^" + DRUGS[DLOOP][50.606][4]
    PSSX = PSSHOLD
    LEAD()
    if TYPE == "O":
        LEAD()
        PSSJZUNT = PSSDZUNT
    PSSX["MISC"] = PSSX["MISC"][0] + "^" + PSSX["MISC"][1] + "^" + PSSX["MISC"][2]
    PSSX["MISC"] = PSSX["MISC"][0] + "^" + PSSX["MISC"][1] + "^" + PSSX["MISC"][2]
    LEAD()
    if TYPE == "O":
        EN3(PD, 80)
    return

def DOSE2():
    PSOCT = 1
    PSOXDOSE = DRUGS[PD][0][2]
    for DLOOP in range(1, len(DRUGS)):
        if not DRUGS[DLOOP]["I"] or DRUGS[DLOOP]["I"] >= datetime.now().date():
            APP()
            PSONDS = DRUGS[DLOOP]["DOS"]
            PSONDU = DRUGS[DLOOP]["DOS_UNIT"]
            PSOND = DRUGS[DLOOP]["ND"][3]
            PSOND1 = DRUGS[DLOOP]["ND"][0]
            if not PSONDS and PSOND and PSOND1:
                PSONDS = PSONDX(PSOND1, PSOND)
            if not PSONDU and PSOND and PSOND1:
                PSONDU = PSONDX(PSOND1, PSOND)
            PSODOS = DRUGS[PD][0][2]
            for PSLOC in range(1, len(DRUGS[DLOOP]["DOS2"])):
                PSLOCV = DRUGS[DLOOP]["DOS2"][PSLOC][0]
                if PSLOCV:
                    if PSSOIU and "I" not in DRUGS[DLOOP]["DOS2"][PSLOC][1]:
                        continue
                    if not PSSOIU and "O" not in DRUGS[DLOOP]["DOS2"][PSLOC][1]:
                        continue
                    SET2()
    if not PSSX:
        PSLOCV = ""
        PSOCT = 1
        for DLOOP in range(1, len(DRUGS)):
            if not DRUGS[DLOOP]["I"] or DRUGS[DLOOP]["I"] >= datetime.now().date():
                APP()
                PSONDS = DRUGS[DLOOP]["DOS"]
                PSONDU = DRUGS[DLOOP]["DOS_UNIT"]
                PSOND = DRUGS[DLOOP]["ND"][3]
                PSOND1 = DRUGS[DLOOP]["ND"][0]
                PSONDX(PSOND1, PSOND)
                PSODOS = DRUGS[PD][0][2]
                SET2()
    LEAD()
    if TYPE == "O":
        EN3(PD, 80)
    return

def SET2():
    if PSLOCV and "&" in PSLOCV:
        AMP()
    PSSX[PSOCT] = ("^" + PSONDU if PSONDU else "") + "^^" + PSNNN + "^" + PSLOCV + "^" + str(DLOOP)
    if DLOOP not in PSSX["DD"]:
        REQS()
        if TYPE == "O":
            MAX()
        PSSX["DD"][DLOOP] = DRUGS[DLOOP][0] + "^" + DRUGS[DLOOP][660] + "^" + DRUGS[DLOOP][0][9] + "^" + DRUGS[DLOOP][660][8] + "^" + DRUGS[DLOOP]["DOS"] + "^" + (PSONDU if PSONDU else "") + "^" + DRUGS[DLOOP][50.606] + "^" + PSSMAX
        DEA(DLOOP)
        PSSX["DD"][DLOOP] += "^" + PSSREQS
        PSSX["MISC"] = PSSVERB + "^" + PSSPREP + "^" + DRUGS[DLOOP][50.606][4]
    PSOCT += 1
    return

def MAX():
    global PSSMAX
    PSSDEA = DRUGS[DLOOP][0][3]
    if "1" in PSSDEA or "2" in PSSDEA:
        PSSMAX = 0
        return
    if "A" in PSSDEA and "B" not in PSSDEA:
        PSSMAX = 0
        return
    if DRUGS[DLOOP]["CLOZ1"] == "PSOCLO1" and PSSDFN:
        PSSCLO = next((x for x in YSCL if x[0] == PSSDFN), None)
        if PSSCLO and PSSCLO[3] == "B":
            PSSMAX = 1
            return
    if "3" in PSSDEA or "4" in PSSDEA or "5" in PSSDEA:
        PSSMAX = 5
        return
    PSSMAX = 11
    return

def SLS():
    global PSSDZUNT
    if "/" not in PSSX[PSSA][1]:
        PSSX[PSSA][4] = PSSX[PSSA][0] + PSSX[PSSA][1]
        return
    PSSF = PSSX[PSSA][0]
    PSSG = PSSX[PSSA][1]
    PSSDZSL = 0
    PSSDZI = PSSX[PSSA][5]
    PSSDZ50 = DRUGS[PSSDZI]["DOS"]
    PSSDZND = PSJST(DRUGS[PSSDZI]["ND"][0], DRUGS[PSSDZI]["ND"][3])[1]
    if not PSSDZND:
        PSSX[PSSA][4] = PSSF
        return
    PSSFA = PSSG.split("/")[0]
    PSSFB = PSSG.split("/")[1]
    PSSFA1 = int(PSSFA) if PSSFA else None
    PSSFB1 = int(PSSFB) if PSSFB else None
    if not PSSDZND:
        PSSX[PSSA][4] = PSSF
        return
    PSSDZSL2 = PSSDZ50 / PSSDZND
    PSSDZSL3 = PSSDZSL2 * int(PSSX[PSSA][2])
    PSSDZSL4 = PSSDZSL3 * (PSSFB1 if PSSFB1 else 1)
    PSSDZSL5 = str(PSSDZSL4) + (PSSFB[PSSFB1:] if PSSFB1 else "")
    PSSF2 = PSSF * PSSFA1 + (PSSF * int(PSSFA[0])) if PSSFA1 else PSSF
    PSSDZUNT = PSSG.split("/")[0] + "/" + str(PSSDZSL4) + (PSSG.split("/")[1][PSSFB1:] if PSSFB1 else "")
    PSSX[PSSA][1] = PSSDZUNT
    PSSX[PSSA][4] = PSSF2
    return

def REQS():
    global PSSREQS
    PSSREQS = 1
    return

def MULTI():
    PL3 = 0
    for PL3 in PSSHOLD[PSSZ][PSSC]:
        PSSX[PSSA][PL3] = PSSHOLD[PSSZ][PSSC][PL3]
        SLS()
        if DLOOP not in PSSX["DD"]:
            MULTI()
    return

def PARN():
    global PSSNP
    if PSNNN:
        if len(PSNNN) > 3:
            PSSNPL = PSNNN[-3:]
            if PSSNPL == "(S)" or PSSNPL == "(s)":
                if PSSUDOS and PSSUDOS <= 1:
                    PSSNP = PSNNN[:-3]
                if PSSUDOS and PSSUDOS > 1:
                    PSSNP = PSNNN[:-3] + PSSNPL[1:]
    return

def LEAD():
    for PSSLD in PSSX:
        if isinstance(PSSLD, int):
            if PSSX[PSSLD][0][0] == ".":
                PSSX[PSSLD][0] = "0" + PSSX[PSSLD][0]
            if PSSX[PSSLD][4][0] == ".":
                PSSX[PSSLD][4] = "0" + PSSX[PSSLD][4]
            if isinstance(PSSX[PSSLD], list):
                for PSSLD1 in PSSX[PSSLD]:
                    if PSSX[PSSLD][PSSLD1][0][0] == ".":
                        PSSX[PSSLD][PSSLD1][0] = "0" + PSSX[PSSLD][PSSLD1][0]
                    if PSSX[PSSLD][PSSLD1][4][0] == ".":
                        PSSX[PSSLD][PSSLD1][4] = "0" + PSSX[PSSLD][PSSLD1][4]
            else:
                if PSSX[PSSLD][5][0] == ".":
                    PSSX[PSSLD][5] = "0" + PSSX[PSSLD][5]
    for PSSLD in PSSX["DD"]:
        if PSSX["DD"][PSSLD][4][0] == ".":
            PSSX["DD"][PSSLD][4] = "0" + PSSX["DD"][PSSLD][4]
    return

def APP():
    global PSSQT
    if TYPE == "O" and "O" not in DRUGS[DLOOP][2]:
        PSSQT = 1
        return
    if "U" not in DRUGS[DLOOP][2] and "I" not in DRUGS[DLOOP][2]:
        PSSQT = 1
    return

DOSE(PSSX, PD, TYPE, PSSDFN)