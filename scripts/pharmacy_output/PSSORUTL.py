def DOSE(PSSX, PD, TYPE, PSSDFN):
    PSSOIU = 1 if TYPE == "I" or TYPE == "U" else 0
    for DLOOP in range(1, len(PSDRUG)):
        if not PSDRUG[DLOOP]["DOS1"]:
            continue
        PSSTRN = PSDRUG[DLOOP]["DOS"]
        PSSUNITX = PSDRUG[DLOOP]["DOS"][1]
        if PSSTRN == "":
            continue
        PSSUNITX = PSSUNITX if PSDRUG[DLOOP]["DOS"][0] != "" and "/" not in PSDRUG[DLOOP]["DOS"][0] else ""
        if PSDRUG[DLOOP]["I"] and int(PSDRUG[DLOOP]["I"]) < int(DT):
            continue
        APPUSE = PSDRUG[DLOOP]["APPUSE"]
        if TYPE == "O" and "O" not in APPUSE:
            continue
        if TYPE == "X" and "X" not in APPUSE:
            continue
        if "U" not in APPUSE and "I" not in APPUSE:
            continue
        PSSDSE = PSDRUG[DLOOP]["DSE"]
        PSSVERB = PSDRUG[PSSDSE]["MISC"][0]
        PSSPREP = PSDRUG[PSSDSE]["MISC"][2]
        for PSNN in range(1, len(PSDRUG[PSSDSE]["NOUN"])):
            PSNNN = PSDRUG[PSSDSE]["NOUN"][PSNN]
            if "&" in PSNNN:
                PSNNN = AMP(PSNNN)
        for DLOOP1 in range(1, len(PSDRUG[DLOOP]["DOS1"])):
            if not PSDRUG[DLOOP]["DOS1"][DLOOP1]:
                continue
            if PSSOIU and "I" not in PSDRUG[DLOOP]["DOS1"][DLOOP1][2]:
                continue
            if not PSSOIU and "O" not in PSDRUG[DLOOP]["DOS1"][DLOOP1][2]:
                continue
            PSSDOSE = PSDRUG[DLOOP]["DOS1"][DLOOP1][1]
            PSSUNTS = PSDRUG[DLOOP]["DOS"][1]
            PSSUDOS = PSDRUG[DLOOP]["DOS1"][DLOOP1][0]
            PSSBCM = PSDRUG[DLOOP]["DOS1"][DLOOP1][3]
            if "." in PSSUDOS:
                PSSHLF[DLOOP] = None
            if PSSDOSE and PSSUDOS:
                DCNT1 = DCNT1 + 1 if DCNT1 else 1
                LOW[PSSDOSE][PSSUDOS][DCNT1] = None
                FORM[PSSDOSE][1 if PSDRUG[DLOOP]["0"][8] == 1 else 0][DCNT1] = PSSUDOS
                PARN()
                PSSX[DCNT1] = PSSDOSE + "^" + PSSUNTS + "^" + ("0" + PSSUDOS[1:] if PSSUDOS[0] == "." else PSSUDOS) + "^" + (PSSNP if PSSNP else PSNNN) + "^^" + str(DLOOP) + "^" + str(PRICE())
    if not PSSX:
        return
    PSSLOW = ""
    for PSSLOW in FORM:
        if FORM[PSSLOW][1]:
            for PSSLOW2 in FORM[PSSLOW][1]:
                if PSSLOW2 in PSSX:
                    del PSSX[PSSLOW2]
                    del LOW[PSSLOW][1][PSSLOW2]
    PSSLOW = ""
    for PSSLOW in LOW:
        PSOLC = 0
        for PSSLOW1 in LOW[PSSLOW]:
            PSOLC += 1
            if PSOLC == 1:
                PSSLOW4 = min(LOW[PSSLOW][PSSLOW1])
            for PSSLOW2 in LOW[PSSLOW][PSSLOW1]:
                if PSOLC > 1:
                    PSSX[PSSLOW4][PSOLC - 1] = PSSX[PSSLOW2]
                    del PSSX[PSSLOW2]
    PSSHOLD = {}
    PL = 0
    for PL in PSSX:
        PSSHOLD[PSSX[PL][0]][PL] = PSSX[PL]
        if len(PSSX[PL]) > 1:
            PL2 = 0
            for PL2 in PSSX[PL]:
                PSSHOLD[PSSX[PL][PL2][0]][PL][PL2] = PSSX[PL][PL2]
                SLS()
                if PSSX[PSSA]["DD"].get(int(PSSX[PSSA][0][5])) == None:
                    SETU()
                    PSSX["DD"][PSIEN] = [PSDRUG[PSIEN][0], PSDRUG[PSIEN][660][5], PSDRUG[PSIEN][0][9], PSDRUG[PSIEN][660][8], PSDRUG[PSIEN]["DOS"], PSSUNITX, PSDRUG[PSSDSE][0], PSSMAX]
                    REQS()
                    PSSX["DD"][PSIEN].append(PSSREQS)
                    DEA(PSIEN)
                    PSSX["DD"][PSIEN].append(PSSDEA)
                MISC()
                PSSA += 1
                PSIEN = PSDRUG[PSSA][0][5]
                PSSMAX = None
                if TYPE == "O":
                    MAX()
                SETU()
                PSSX["DD"][PSIEN] = [PSDRUG[PSIEN][0], PSDRUG[PSIEN][660][6], PSDRUG[PSIEN][0][9], PSDRUG[PSIEN][660][8], PSDRUG[PSIEN]["DOS"], PSSUNITX, PSDRUG[PSSDSE][0], PSSMAX]
                REQS()
                PSSX["DD"][PSIEN].append(PSSREQS)
                DEA(PSIEN)
                PSSX["DD"][PSIEN].append(PSSDEA)
                PSSX["MISC"] = [PSSVERB, PSSPREP, PSDRUG[PSSDSE]["MISC"][3]]
    PSSHOLD = {}
    for PSOCT in range(1, len(PSSX)):
        PSOXDOSE = PSDRUG[PD][0][2]
        if not PSOXDOSE:
            continue
        PSSDZSL = 0
        PSSDZI = PSDRUG[PD][6][5]
        PSSDZ50 = PSDRUG[PSSDZI][2]
        PSSDZND = PSJST(PSDRUG[PSSDZI][6][3], PSDRUG[PSSDZI][6][4])
        PSSDZND = PSSDZND[1] if PSSDZND else None
        if not PSSDZND:
            PSSX[PSOCT][4] = PSSX[PSOCT][0]
            continue
        PSSFA = PSSX[PSOCT][1].split("/")[0]
        PSSFB = PSSX[PSOCT][1].split("/")[1]
        PSSFA1 = int(PSSFA) if PSSFA else None
        PSSFB1 = int(PSSFB) if PSSFB else None
        if not PSSDZND:
            PSSX[PSOCT][4] = PSSX[PSOCT][0]
            continue
        PSSDZSL2 = PSSDZ50 / PSSDZND
        PSSDZSL3 = PSSDZSL2 * int(PSSX[PSOCT][2])
        PSSDZSL4 = PSSDZSL3 * (PSSFB1 if PSSFB1 else 1)
        PSSDZSL5 = str(PSSDZSL4) + (PSSFB if not PSSFB1 else PSSFB.split(str(PSSFB1))[1])
        PSSF2 = (PSSX[PSOCT][0] * PSSFA1 if PSSFA1 else PSSX[PSOCT][0]) + ("/" + PSSDZSL5)
        PSSDZUNT = PSSX[PSOCT][1].split("/")[0] + "/" + str(PSSDZSL4) + (PSSFB if not PSSFB1 else PSSFB.split(str(PSSFB1))[1])
        PSSX[PSOCT][1] = PSSDZUNT
        PSSX[PSOCT][4] = PSSF2
    LEAD()
    if PSSX["DD"].get(PD) == None:
        REQS()
        PSSX["DD"][PD] = [PSDRUG[PD][0], PSDRUG[PD][660][5], PSDRUG[PD][0][9], PSDRUG[PD][660][8], PSDRUG[PD]["DOS"], PSSUNITX, PSDRUG[PSODOS][0], PSSMAX, PSSREQS]
        DEA(PD)
        PSSX["DD"][PD].append(PSSDEA)
    LEAD()
    LEAD()
    LEAD()
    LEAD()
    if TYPE == "O":
        LEAD()
        LEAD()
    PSSX["DEA"] = OIDEA(PD, TYPE)
    DUP()