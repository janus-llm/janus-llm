def DOSE(PSSX, PD, TYPE, PSSDFN):
    PSSX = []
    PSSOIU = 1 if TYPE == "I" or TYPE == "U" else 0
    for DLOOP in range(len(PSDRUG)):
        if PSDRUG[DLOOP]["ASP"] == PD:
            if PSDRUG[DLOOP]["DOS1"]:
                PSSTRN = PSDRUG[DLOOP]["DOS"]
                PSSUNITX = PSDRUG[DLOOP]["DOS2"]
                if PSSTRN:
                    PSSUNITX = PSSUNITX if PSSUNITX and not "/" in PSSUNITX else ""
                    if PSDRUG[DLOOP]["I"] and int(PSDRUG[DLOOP]["I"]) < int(DT):
                        continue
                    APPUSE = PSDRUG[DLOOP]["APP"]
                    if TYPE == "O":
                        if not "O" in APPUSE:
                            continue
                    elif TYPE == "X":
                        if not "X" in APPUSE:
                            continue
                    else:
                        if not "U" in APPUSE and not "I" in APPUSE:
                            continue
                    PSSDSE = int(PSDRUG[DLOOP]["DOS2"])
                    PSSVERB = PSDRUG[DLOOP]["MISC"]
                    PSSPREP = PSDRUG[DLOOP]["MISC2"]
                    PSNNN = ""
                    for PSNN in range(len(PSDRUG[DLOOP]["NOUN"])):
                        if PSDRUG[DLOOP]["NOUN"][PSNN]:
                            PSNNN = PSDRUG[DLOOP]["NOUN"][PSNN]
                            break
                    if "&" in PSNNN:
                        PSLOCV = PSNNN
                        PSNNN = AMP(PSLOCV)
                    for DLOOP1 in range(len(PSDRUG[DLOOP]["DOS1"])):
                        if PSDRUG[DLOOP]["DOS1"][DLOOP1]:
                            if PSSOIU and not "I" in PSDRUG[DLOOP]["DOS1"][DLOOP1]:
                                continue
                            if not PSSOIU and not "O" in PSDRUG[DLOOP]["DOS1"][DLOOP1]:
                                continue
                            PSSDOSE = PSDRUG[DLOOP]["DOS1"][DLOOP1][1]
                            PSSUNTS = PSDRUG[DLOOP]["DOS1"][DLOOP1][2]
                            PSSUDOS = PSDRUG[DLOOP]["DOS1"][DLOOP1][0]
                            PSSBCM = PSDRUG[DLOOP]["DOS1"][DLOOP1][3]
                            if "." in PSSUDOS:
                                PSSHLF[DLOOP] = ""
                            if PSSDOSE and PSSUDOS:
                                DCNT1 = DCNT1 + 1 if "DCNT1" in locals() else 1
                                LOW[PSSDOSE][PSSUDOS][DCNT1] = ""
                                FORM[PSSDOSE][1 if PSDRUG[DLOOP][9] == 1 else 0][DCNT1] = PSSUDOS
                                PARN()
                                PSSX.append(PSSDOSE + "^" + PSSUNTS + "^" + ("0" if PSSUDOS[0] == "." else "") + PSSUDOS + "^" + PSSNP if "PSSNP" in locals() and PSSNP else PSNNN + "^^" + DLOOP + "^" + PRICE(PSDRUG[DLOOP]) if "PRICE" in locals() else "")
    if not PSSX:
        DOSE2()
    PSSLOW = ""
    for PSSLOW in LOW:
        if PSSLOW in FORM and len(FORM[PSSLOW][1]) > 0:
            for PSSLOW2 in FORM[PSSLOW][1]:
                PSSX[PSSLOW4][len(PSSX[PSSLOW4]) - 1] = PSSX[PSSLOW2]
                del PSSX[PSSLOW2]
    PSSHOLD = {}
    for PL in PSSX:
        PSSHOLD[PSSX[PL][0]][PL] = PSSX[PL]
        if len(PSSX[PL]) > 1:
            for PL2 in PSSX[PL]:
                PSSHOLD[PSSX[PL][0]][PL][PL2] = PSSX[PL][PL2]
    PSSX = []
    PSSA = 1
    for PSSZ in PSSHOLD:
        for PSSC in PSSHOLD[PSSZ]:
            PSSX[PSSA] = PSSHOLD[PSSZ][PSSC]
            SLS()
            if not PSSX["DD"][PSSX[PSSA][5]] in locals():
                SETU()
            PSIEN = PSSX[PSSA][5]
            PSSMAX = ""
            if TYPE == "O":
                MAX()
            PSSX["DD"][PSIEN] = PSDRUG[PSIEN][0] + "^" + PSDRUG[PSIEN][6] + "^" + PSDRUG[PSIEN][9] + "^" + PSDRUG[PSIEN][8] + "^" + PSDRUG[PSIEN][10] + "^" + PSSUNITX + "^" + PSDRUG[PSIEN][1] + "^" + PSSMAX + "^" + PSSREQS + "^^"
            DEAPKI(PSIEN)
            PSSX["MISC"] = PSSVERB + "^" + PSSPREP + "^" + PSDRUG[PSIEN][3]
            PSSA = PSSA + 1
            SET3()
    PSSX["DEA"] = OIDEA(PD, TYPE)


def DOSE2():
    PSSX = []
    PSOCT = 1
    PSOXDOSE = PSDRUG[PD][1]
    for DLOOP in range(len(PSDRUG)):
        if PSDRUG[DLOOP]["ASP"] == PD:
            APPUSE = PSDRUG[DLOOP]["APP"]
            if not PSDRUG[DLOOP]["I"] or int(PSDRUG[DLOOP]["I"]) >= int(DT):
                if PSDRUG[DLOOP]["DOS2"]:
                    PSONDS = PSDRUG[DLOOP]["DOS"]
                    PSONDU = PSDRUG[DLOOP]["DOS2"]
                    PSOND = PSDRUG[DLOOP]["ND"][2]
                    PSOND1 = PSDRUG[DLOOP]["ND"][1]
                    if not PSONDS or not PSONDU:
                        PSONDX = DFSU(PSOND1, PSOND)
                        if PSOND and PSOND1:
                            if not PSONDS:
                                PSONDS = PSONDX[4]
                            if not PSONDU:
                                PSONDU = PSONDX[5]
                    NU()
                    PSODOS = PSDRUG[DLOOP]["DOS2"]
                    for PSLOC in range(len(PSDRUG[DLOOP]["DOS2"])):
                        PSLOCV = PSDRUG[DLOOP]["DOS2"][PSLOC]
                        if PSSOIU and not "I" in PSDRUG[DLOOP]["DOS2"][PSLOC]:
                            continue
                        if not PSSOIU and not "O" in PSDRUG[DLOOP]["DOS2"][PSLOC]:
                            continue
                        SET2()
    if not PSSX:
        PSOCT = 1
        for DLOOP in range(len(PSDRUG)):
            if PSDRUG[DLOOP]["ASP"] == PD:
                APPUSE = PSDRUG[DLOOP]["APP"]
                if not PSDRUG[DLOOP]["I"] or int(PSDRUG[DLOOP]["I"]) >= int(DT):
                    PSONDS = PSDRUG[DLOOP]["DOS"]
                    PSONDU = PSDRUG[DLOOP]["DOS2"]
                    PSOND = PSDRUG[DLOOP]["ND"][2]
                    PSOND1 = PSDRUG[DLOOP]["ND"][1]
                    PSONDX = DFSU(PSOND1, PSOND)
                    if PSOND and PSOND1:
                        if not PSONDS:
                            PSONDS = PSONDX[4]
                        if not PSONDU:
                            PSONDU = PSONDX[5]
                    NU()
                    PSODOS = PSDRUG[DLOOP]["DOS2"]
                    SET3()
    LEAD()
    if TYPE == "O":
        EN3(PD, 245)
    PSSX["DEA"] = OIDEA(PD, TYPE)
    DUP()


def SET2():
    if PSLOCV and "&" in PSLOCV:
        AMP()
    PSSX[PSOCT] = ["", PSONDU, "", PSNNN, PSLOCV, DLOOP, PRICE(PSDRUG[DLOOP])]
    SETU()
    PSIEN = PSSX[PSOCT][5]
    SET3()
    PSOCT = PSOCT + 1


def SET3():
    if not PSIEN in PSSX["DD"]:
        REQS()
        MAX()
        PSSX["DD"][PSIEN] = PSDRUG[PSIEN][0] + "^" + PSDRUG[PSIEN][6] + "^" + PSDRUG[PSIEN][9] + "^" + PSDRUG[PSIEN][8] + "^" + PSONDS + "^" + PSONDU + "^" + PSDRUG[PSIEN][1] + "^" + PSDRUG[PSIEN][10] + "^" + PSSREQS
        DEAPKI(PSIEN)
    PSSX["MISC"] = PSDRUG[PSIEN][3] + "^" + PSDRUG[PSIEN][4] + "^" + PSDRUG[PSIEN][5]
    PSOCT = PSOCT + 1


def MAX():
    PSSMAX = ""
    PSSDEA = PSDRUG[DLOOP][2]
    if "1" in PSSDEA or "2" in PSSDEA:
        PSSMAX = 0
    elif "A" in PSSDEA and "B" not in PSSDEA:
        PSSMAX = 0
    elif PSDRUG[DLOOP]["CLOZ1"] == "PSOCLO1" and PSSDFN:
        PSSCLO = YSCL[PSDFN]
        if PSSCLO and YSCL[PSSCLO][2] == "B":
            PSSMAX = 1
        else:
            PSSMAX = 0
    elif "3" in PSSDEA or "4" in PSSDEA or "5" in PSSDEA:
        PSSMAX = 5
    else:
        PSSMAX = 11


def SLS():
    if "/" not in PSSX[PSA][1]:
        PSSX[PSA][4] = PSSX[PSA][0] + PSSX[PSA][1]
        return
    PSSDZUNT = ""
    if PSSX[PSA][4]:
        PSSDZUNT = PSSX[PSA][4]
    PSSDZI = PSSX[PSA][5]
    PSSDZ50 = PSDRUG[PSSDZI][10]
    PSSDZND = PSJST(PSDRUG[PSSDZI][13], PSDRUG[PSSDZI][14])
    PSSDZND = PSSDZND[1] if PSSDZND and PSSDZND[0] else 0
    if not PSSDZND:
        PSSDZSL = 0
    elif PSSDZ50 and PSSDZND and int(PSSDZND) != int(PSSDZ50):
        PSSDZSL = 1
    PSSFA = PSSX[PSA][1].split("/")[0]
    PSSFB = PSSX[PSA][1].split("/")[1]
    PSSFA1 = int(PSSFA) if PSSFA else 0
    PSSFB1 = int(PSSFB) if PSSFB else 0
    if not PSSDZND:
        PSSX[PSA][1] = PSSX[PSA][0]
        return
    PSSDZSL2 = PSSDZ50 / PSSDZND
    PSSDZSL3 = PSSDZSL2 * int(PSSX[PSA][2])
    PSSDZSL4 = PSSDZSL3 * (int(PSSFB1) if PSSFB1 else 1)
    PSSDZSL5 = str(PSSDZSL4) + (PSSFB[PSSFB1:] if PSSFB1 else "")
    PSSF2 = (int(PSSFA1) * PSSX[PSA][0]) + (PSSFA[PSSFA1:] if PSSFA1 else "") + "/" + PSSDZSL5
    PSSDZUNT = PSSX[PSA][1].split("/")[0] + "/" + str(PSSDZSL4) + (PSSFB[PSSFB1:] if PSSFB1 else "")
    PSSX[PSA][1] = PSSDZUNT
    PSSX[PSA][4] = PSSF2


def REQS():
    PSSREQS = 1


def MULTI():
    for PL3 in PSSHOLD[PSSZ][PSSC]:
        PSSX[PSA][PL3] = PSSHOLD[PSSZ][PSSC][PL3]
        SLS()
        if not PSSX["DD"][PSDRUG[PSSX[PSA][PL3]][4]] in locals():
            SETU()
        PSIEN = PSSX[PSA][PL3][5]
        SET3()
    PSSJZUNT = ""


def PARN():
    if PSNNN:
        if len(PSNNN) > 3:
            PSSNPL = PSNNN[len(PSNNN) - 3:]
            if PSSNPL == "(S)" or PSSNPL == "(s)":
                if PSSUDOS <= 1:
                    PSSNP = PSNNN[:len(PSNNN) - 3]
                else:
                    PSSNP = PSNNN[:len(PSNNN) - 3] + PSSNPL[1]


def APP():
    PSSQT = 0
    APPUSE = PSDRUG[DLOOP][7]
    if TYPE == "O":
        if "O" not in APPUSE:
            PSSQT = 1
    elif TYPE == "X":
        if "X" not in APPUSE:
            PSSQT = 1
    else:
        if "U" not in APPUSE and "I" not in APPUSE:
            PSSQT = 1


def NS():
    if not PSONDS.isdigit() and not PSONDS.replace(".", "").isdigit():
        PSONDS = None


def NU():
    PSONDU = PSDRUG[DLOOP]["DOS2"]
    if PSONDS and PSONDU:
        PSONDU = PSONDU if PSONDU and not "/" in PSONDU else ""


def SETU():
    PSSUNITX = PSDRUG[PSIEN]["DOS2"]
    PSSUNITX = PSSUNITX if PSSUNITX and not "/" in PSSUNITX else ""


DOSE([], PD, TYPE, PSSDFN)