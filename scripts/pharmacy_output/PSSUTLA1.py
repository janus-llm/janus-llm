def EN3(PSSBINTR, PSSBLGTH):
    # Pass in to EN3 the internal number from 50.7, and the length of the array you want.
    # Returns expanded Instructions is PSSBSIG array
    PSSBSIG = []
    X = "^" + str(PSSBINTR)
    if X == "":
        return PSSBSIG
    PISIG = [""] * 2
    CNTZ = 1
    if len(X) < 1:
        return PSSBSIG
    for Z0 in range(1, len(X.split()) + 1):
        Z1 = X.split()[Z0 - 1]
        if Z1 != "":
            Y = 0
            try:
                Y = int(Z1)
            except ValueError:
                pass
            if Y > 0:
                continue
            PISIG[CNTZ] = PISIG[CNTZ] + " " + Z1
            if len(PISIG[CNTZ]) > PSSBLGTH:
                CNTZ += 1
                PISIG[CNTZ] = Z1
    BVAR = ""
    BVAR1 = ""
    III = 1
    for FFF in range(1, len(PISIG) + 1):
        if PISIG[FFF] == "":
            continue
        CNT = 0
        for NNN in range(1, len(PISIG[FFF]) + 1):
            if PISIG[FFF][NNN - 1] == " " or len(PISIG[FFF]) == NNN:
                CNT += 1
                BVAR1 = PISIG[FFF].split()[CNT - 1]
                BLIM = BVAR
                BVAR = BVAR1 if BVAR == "" else BVAR + " " + BVAR1
                if len(BVAR) > PSSBLGTH:
                    PSSBSIG.append(BLIM + " ")
                    III += 1
                    BVAR = BVAR1
    if BVAR != "":
        PSSBSIG.append(BVAR)
    if PSSBSIG[0] == "" or PSSBSIG[0] == " ":
        PSSBSIG[0] = PSSBSIG[1]
        del PSSBSIG[1]
    PSSX = {}
    for CNTZ in range(1, len(PSSBSIG) + 1):
        PSSX["PI", CNTZ] = PSSBSIG[CNTZ]
    return PSSX


def DEA(PSSDIENM):
    # Return DEA Special Handling for CPRS Dose Call
    # 1 Requires wet sig, DEA contains 1, or a 2
    # 2 = Controlled Sub, no wet sig required, DEA contains 3, 4, or 5
    # 0 = others
    if PSSDIENM == 0:
        return ""
    PSSDEAX = str(PSSDIENM)
    PSSDEAXV = 0
    if "1" in PSSDEAX or "2" in PSSDEAX:
        PSSDEAXV = 1
    elif "3" in PSSDEAX or "4" in PSSDEAX or "5" in PSSDEAX:
        PSSDEAXV = 2
    PSSX = {"DD": PSSDIENM}
    PSSX["DD"] = PSSX["DD"] + "^" + str(PSSDEAXV) + "^" + str(int(PSSDIENM in PSSHLF))
    return PSSX


def HELP(X):
    if X == "":
        return
    PSSSIG = []
    PSSCTX = 1
    if len(X) < 1:
        return PSSSIG
    for PSSZ0 in range(1, len(X.split()) + 1):
        PSSZ1 = X.split()[PSSZ0 - 1]
        if PSSZ1 != "":
            PSSYX = 0
            try:
                PSSYX = int(PSSZ1)
            except ValueError:
                pass
            if PSSYX > 0:
                continue
            PSSSIG[PSSCTX] = PSSSIG[PSSCTX] + " " + PSSZ1
            if len(PSSSIG[PSSCTX]) > 245:
                PSSCTX += 1
                PSSSIG[PSSCTX] = PSSZ1
    BVAR = ""
    BVAR1 = ""
    III = 1
    for FFF in range(0, len(PSSSIG)):
        if PSSSIG[FFF] == "":
            continue
        CNT = 0
        for NNN in range(1, len(PSSSIG[FFF]) + 1):
            if PSSSIG[FFF][NNN - 1] == " " or len(PSSSIG[FFF]) == NNN:
                CNT += 1
                BVAR1 = PSSSIG[FFF].split()[CNT - 1]
                BLIM = BVAR
                BVAR = BVAR1 if BVAR == "" else BVAR + " " + BVAR1
                if len(BVAR) > 70:
                    PSSSIG[III] = BLIM + " "
                    III += 1
                    BVAR = BVAR1
    PSSSIG[III] = BVAR if BVAR != "" else PSSSIG[III]
    if PSSSIG[0] == "" or PSSSIG[0] == " ":
        PSSSIG[0] = PSSSIG[1]
        del PSSSIG[1]
    for CNTZ in range(1, len(PSSSIG) + 1):
        EN^DDIOL(" ")
        EN^DDIOL(" " + PSSSIG[CNTZ])
    return PSSSIG


def HELPADD(PSSCTX, PSSZ1):
    if len(PSSSIG[PSSCTX]) + len(PSSZ1) + 1 < 246:
        PSSSIG[PSSCTX] = PSSSIG[PSSCTX] + " " + PSSZ1
    else:
        PSSCTX += 1
        PSSSIG[PSSCTX] = PSSZ1
    return PSSCTX, PSSSIG


def PRICE(DLOOP, PSSUDOS, PSSBCM):
    # Return price per dose for CPRS Dose call
    # DLOOP = Internal entry number from Drug file
    # PSSUDOS = Dispense units per Dose
    PSSPRICE = 0
    PSSPRQ = ""
    if DLOOP == 0:
        return ""
    if PSSUDOS:
        PSSPRQ = PSSUDOS * PSSPRICE
    elif PSSBCM:
        PSSPRQ = PSSBCM * PSSPRICE
    if PSSPRQ != "":
        if PSSPRQ[0] == ".":
            PSSPRQ = "0" + PSSPRQ
    return PSSPRQ


def OIDEA(PSSXOI, PSSXOIP):
    # DEA return based on Orderable Item, Item and Usage passed in
    # 1 means DEA contains a 1, or a 2
    # 2 means DEA contains a 3, or a 4, or a 5
    # 0 means all others
    PSSXOLPD = 0
    PSSXNODD = 0
    if PSSXOIP == "X":
        return ""
    if PSSXOI == 0 or PSSXOIP == "":
        return ""
    PSSPKLX = 1 if PSSXOIP == "I" or PSSXOIP == "U" else 0
    for PSSXOLP in range(0, len(PSSDRUG)):
        if PSSXOLP != 0 and PSSXOLPD == 1:
            break
        if PSSXOLP == 0:
            PSSXOLPX = PSSDRUG[PSSXOLP]["DEA"]
            if "1" in PSSXOLPX or "2" in PSSXOLPX:
                PSSXOLPD = 1
                continue
            if "3" in PSSXOLPX or "4" in PSSXOLPX or "5" in PSSXOLPX:
                PSSXOLPD = 2
    if PSSXOLPD == 0 and PSSXNODD == 0:
        PSSXOLPD = ""
    return PSSXOLPD


def LEAD():
    # Leading zeros, CPRS Dosage call
    for PSSLD in range(0, len(PSSX)):
        if PSSX[PSSLD]["DOSE"] != "":
            if PSSX[PSSLD]["DOSE"][0] == ".":
                PSSX[PSSLD]["DOSE"] = "0" + PSSX[PSSLD]["DOSE"]
            if PSSX[PSSLD]["DOSE2"][0] == ".":
                PSSX[PSSLD]["DOSE2"] = "0" + PSSX[PSSLD]["DOSE2"]
            if PSSX[PSSLD]["DOSE2"].find("/.") != -1:
                PSSBKD = PSSX[PSSLD]["DOSE2"]
                PSSBK = PSSBKD.split("/.")[0]
                PSSBK1 = PSSBKD.split("/.")[1]
                PSSX[PSSLD]["DOSE2"] = PSSBK + "/0." + PSSBK1
            if PSSX[PSSLD]["DOSE3"][0] == ".":
                PSSX[PSSLD]["DOSE3"] = "0" + PSSX[PSSLD]["DOSE3"]
            if PSSX[PSSLD]["DOSE3"].find("/.") != -1:
                PSSBKD = PSSX[PSSLD]["DOSE3"]
                PSSBK = PSSBKD.split("/.")[0]
                PSSBK1 = PSSBKD.split("/.")[1]
                PSSX[PSSLD]["DOSE3"] = PSSBK + "/0." + PSSBK1
            if PSSX[PSSLD]["DOSE4"][0] == ".":
                PSSX[PSSLD]["DOSE4"] = "0" + PSSX[PSSLD]["DOSE4"]


def LEADP():
    # Leading zeros pharmacy call
    for PSSMD in range(0, len(PSSX)):
        if PSSX[PSSMD]["DOSE"] != "":
            if PSSX[PSSMD]["DOSE"][0] == ".":
                PSSX[PSSMD]["DOSE"] = "0" + PSSX[PSSMD]["DOSE"]
            if PSSX[PSSMD]["DOSE2"][0] == ".":
                PSSX[PSSMD]["DOSE2"] = "0" + PSSX[PSSMD]["DOSE2"]
            if PSSX[PSSMD]["DOSE2"].find("/.") != -1:
                PSSBKD = PSSX[PSSMD]["DOSE2"]
                PSSBK = PSSBKD.split("/.")[0]
                PSSBK1 = PSSBKD.split("/.")[1]
                PSSX[PSSMD]["DOSE2"] = PSSBK + "/0." + PSSBK1
            if PSSX[PSSMD]["DOSE3"][0] == ".":
                PSSX[PSSMD]["DOSE3"] = "0" + PSSX[PSSMD]["DOSE3"]
            if PSSX[PSSMD]["DOSE3"].find("/.") != -1:
                PSSBKD = PSSX[PSSMD]["DOSE3"]
                PSSBK = PSSBKD.split("/.")[0]
                PSSBK1 = PSSBKD.split("/.")[1]
                PSSX[PSSMD]["DOSE3"] = PSSBK + "/0." + PSSBK1
            if PSSX[PSSMD]["DOSE4"][0] == ".":
                PSSX[PSSMD]["DOSE4"] = "0" + PSSX[PSSMD]["DOSE4"]
                

def DUP():
    # delete str/unit if duplicate local doses with strength are found
    PSSLXA = {}
    PSSLXL = ""
    PSSLXFL = False
    PSSLXQ = ""
    PSSLXLD = ""
    PSSLXMED = ""
    PSSLXSTR = ""
    PSSLXND = ""
    PSSLXX = ""
    for PSSLXL in range(0, len(PSSX)):
        PSSLXND = PSSX[PSSLXL]
        PSSLXSTR = ""
        PSSLXLD = PSSLXND["DOSE"]
        PSSLXMED = PSSLXND["DD"]
        if PSSLXMED:
            PSSLXSTR = PSSX["DD"][PSSLXMED]["DOSE"]
        if PSSLXLD and PSSLXMED and PSSLXSTR:
            PSSLXA[PSSLXLD, PSSLXSTR, PSSLXMED] = True
            for PSSLXX in PSSLXA:
                if PSSLXX != PSSLXMED:
                    PSSLXFL = True
                    break
    if PSSLXFL:
        for PSSLXQ in PSSX["DD"]:
            PSSX["DD"][PSSLXQ]["DOSE"] = ""
            PSSX["DD"][PSSLXQ]["DD"] = ""
    return PSSX


def PLACER(PSSPDFN, PSSPIEN):
    # Return CPRS order number from Pharmacy order
    # PSSPDFN = Patient internal number
    # PSSPIEN = Pharmacy number - U-Unit Dose, V-IV, P-Inpatient Pending, S-Outpatient Pending, R-Prescription, N-Non-VA
    if PSSPDFN == 0 or not PSSPIEN.isdigit() or len(PSSPIEN) != 2:
        return ""
    PSSPAK = PSSPIEN[-1]
    PSSLOC = ""
    if PSSPAK == "U":
        PSSLOC = 5
    elif PSSPAK == "V":
        PSSLOC = "IV"
    elif PSSPAK == "P" or PSSPAK == "S":
        PSSLOC = 1
    elif PSSPAK == "R":
        PSSLOC = int(PSSPIEN[0])
    elif PSSPAK == "N":
        PSSLOC = 4
    if PSSLOC == "":
        return ""
    if PSSPAK == "U" or PSSPAK == "V":
        return PSSX[55][PSSPDFN][PSSLOC][PSSPIEN][21]
    if PSSPAK == "R":
        return PSSX[52][PSSPIEN]["OR1"][2]
    if PSSPAK == "P":
        return PSSX[53.1][PSSPIEN][21]
    if PSSPAK == "S":
        return PSSX[52.41][PSSPIEN][0]
    return PSSX[55][PSSPDFN]["NVA"][PSSPIEN][8]


def LOC(PSSPDFN, PSSPIEN):
    # Return Location from Pharmacy order
    # PSSPDFN = Patient internal number
    # PSSPIEN = Pharmacy number - U-Unit Dose, V-IV, P-Inpatient Pending, S-Outpatient Pending, R-Prescription, N-Non-VA
    if PSSPDFN == 0 or PSSPIEN[-1] not in ["U", "V", "P", "S", "R", "N"]:
        return LOCIN()
    PSSPAK = PSSPIEN[-1]
    PSSHLOC = ""
    PSSWRD = 0
    PSSWRDN = ""
    PSSRSLT = ""
    PSSROOM = ""
    PSSRLIN = ""
    PSSRLINN = ""
    PSSERR = False
    if PSSPAK == "U" or PSSPAK == "V" or PSSPAK == "P":
        if PSSPAK == "V":
            PSSHLOC = PSSX[55][PSSPDFN]["IV"][PSSPIEN]["DSS"]
        elif PSSPAK == "P":
            PSSHLOC = PSSX[53.1][PSSPIEN]["DSS"]
        elif PSSPAK == "U":
            PSSHLOC = PSSX[55][PSSPDFN][5][PSSPIEN][8]
        if PSSHLOC:
            PSSRSLT = LOCHL(PSSHLOC)
            if PSSRSLT:
                return PSSRSLT
        PSSWRD = LOCWA()
        if PSSWRD:
            PSSHLOC = PSSX[42][PSSWRD][44]
            if PSSHLOC:
                PSSRSLT = LOCHL(PSSHLOC)
                if PSSRSLT:
                    return PSSRSLT
            if PSSWRD:
                PSSWRDN = PSSX[42][PSSWRD][0]
                if PSSWRDN:
                    PSSRSLT = str(PSSWRD) + "^" + PSSWRDN + "^" + "42"
                    return PSSRSLT
        if PSSPAK == "V":
            PSSROOM = PSSX[55][PSSPDFN]["IV"][PSSPIEN][2]
        elif PSSPAK == "P":
            PSSROOM = PSSX[53.1][PSSPIEN][8][8]
        if PSSROOM:
            PSSRSLT = LOCDI(PSSROOM)
            if PSSRSLT:
                return PSSRSLT
        return LOCIN()
    if PSSPAK == "S" or PSSPAK == "R" or PSSPAK == "N":
        if PSSPAK == "N":
            PSSHLOC = PSSX[55][PSSPDFN]["NVA"][PSSPIEN][12]
        elif PSSPAK == "R":
            PSSHLOC = PSSX[52][PSSPIEN][5]
        elif PSSPAK == "S":
            PSSHLOC = PSSX[52.41][PSSPIEN][13]
        if PSSHLOC:
            PSSRSLT = LOCHL(PSSHLOC)
            if PSSRSLT:
                return PSSRSLT
        if PSSPAK == "S":
            PSSRLIN = PSSX[52.41][PSSPIEN]["INI"]
            if PSSRLIN:
                PSSRLINN = PSSX[52.41][PSSPIEN]["100"]
                if PSSRLINN:
                    PSSRSLT = str(PSSRLIN) + "^" + PSSRLINN + "^" + "4"
                    return PSSRSLT
        return LOCIN()
    return LOCIN()


def LOCWA():
    # Return ward
    VAHOW = 0
    VAROOT = 0
    VAINDT = 0
    VAIN = 0
    VAERR = 0
    INP^VADPT()
    return int(VAIN[4])


def LOCHL(PSSCLN):
    # Return hospital location file #44
    PSSCLNN = PSSX[44][PSSCLN][0]
    return str(PSSCLN) + "^" + PSSCLNN + "^" + "44"


def LOCDI(PSSDIV):
    # Return division file #40.8
    PSSDIVN = PSSX[40.8][PSSDIV][0]
    return str(PSSDIV) + "^" + PSSDIVN + "^" + "40.8"


def LOCIN():
    # Return institution file #4
    return PSSX[4]