def EN3(PSSBINTR, PSSBLGTH):
    # Pass in to EN3 the internal number from 50.7, and the length of the
    # array you want. Returns expanded Instructions is PSSBSIG array
    PSSBSIG = []
    X, BVAR, BVAR1, III, CNT, NNN, BLIM, Y, PISIG, Z0, Z1, CNTZ, FFF = None, None, None, None, None, None, None, None, None, None, None, None, None

    if not PSSBINTR or not PSSBLGTH:
        return

    X = str(^PS(50.7, PSSBINTR, "INS"))
    if not X:
        return

    PISIG = [""]
    CNTZ = 1
    if len(X) < 1:
        for Z0 in range(1, len(X.split(" "))+1):
            if Z0 == "":
                START()
            else:
                Z1 = X.split(" ")[Z0-1]
                if Z1:
                    if ADD():
                        Y = ^PS(51, "B", Z1, 0)
                        if Y and ^PS(51, +Y, 0).split("^")[4] > 1:
                            Z1 = ^PS(51, Y, 0).split("^")[2]
                            if ^PS(51, Y, 0).split("^")[9]:
                                Y = X.split(" ")[Z0-2]
                                Y = Y[len(Y)-1]
                                if Y > 1:
                                    Z1 = ^PS(51, Y, 0).split("^")[9]
    (BVAR, BVAR1) = ("", "")
    III = 1
    for FFF in range(0, len(PISIG)+1):
        if FFF:
            CNT = 0
            for NNN in range(1, len(PISIG[FFF])+1):
                if PISIG[FFF][NNN-1] == " " or len(PISIG[FFF]) == NNN:
                    CNT += 1
                    if BVAR:
                        if len(BVAR) > PSSBLGTH:
                            PSSBSIG[III] = BLIM + " "
                            III += 1
                            BVAR = BVAR1
    if BVAR:
        PSSBSIG[III] = BVAR
    if PSSBSIG[1] == "" or PSSBSIG[1] == " ":
        PSSBSIG[1] = PSSBSIG[2]
        del PSSBSIG[2]
    for CNTZ in range(0, len(PSSBSIG)+1):
        if CNTZ:
            PSSX["PI", CNTZ] = PSSBSIG[CNTZ]
    PSSBSIG = []

def ADD():
    if len(PISIG[CNTZ]) + len(Z1) + 1 < 246:
        PISIG[CNTZ] = PISIG[CNTZ] + " " + Z1
        return True
    CNTZ += 1
    PISIG[CNTZ] = Z1
    return False

def START():
    global Z1
    if D() and Z1:
        return
    D()

def ORDRNUM(PSSDFN, PSSTYPE, PSSORPK):
    # Get order number by PSSDFN, PSSTYPE, & PSSORPK
    # PSSDFN - patient dfn
    # PSSTYPE - type of IP order
    # PSSORPK - parent order (IP order #)
    # PSSORIFN - CPRS order number
    if not int(PSSDFN):
        return ""
    if not (PSSTYPE == "IV" or PSSTYPE == 5):
        return ""
    if not int(PSSORPK):
        return ""
    PSSORIEN = ^PS(55, PSSDFN, PSSTYPE, +PSSORPK, 0).split("^")[21]
    return PSSORIEN

def HELP():
    if not X:
        return
    PSSSIG, PSSYX, PSSZ0, PSSZ1, PSSCTX, PSSLPX, PSSBVAR, PSSBVAR1, PSSIII, PSSFFF, PCT, PNNN, PSSBLIM, PSSIG = [], None, None, None, None, None, None, None, None, None, None, None, None
    PSSIG = [""]
    PSSCTX = 1
    if len(X) < 1:
        for PSSZ0 in range(1, len(X.split(" "))+1):
            if PSSZ0 == "":
                HELP1()
            else:
                PSSZ1 = X.split(" ")[PSSZ0-1]
                if PSSZ1:
                    if HELPADD():
                        PSSYX = ^PS(51, "B", PSSZ1, 0)
                        if PSSYX and ^PS(51, +PSSYX, 0).split("^")[4] > 1:
                            PSSZ1 = ^PS(51, PSSYX, 0).split("^")[2]
                            if ^PS(51, PSSYX, 0).split("^")[9]:
                                PSSYX = X.split(" ")[PSSZ0-2]
                                PSSYX = PSSYX[len(PSSYX)-1]
                                if PSSYX > 1:
                                    PSSZ1 = ^PS(51, PSSYX, 0).split("^")[9]
    (PSSBVAR, PSSBVAR1) = ("", "")
    PSSIII = 1
    for PSSFFF in range(0, len(PSSIG)+1):
        if PSSFFF:
            PCT = 0
            for PNNN in range(1, len(PSSIG[PSSFFF])+1):
                if PSSIG[PSSFFF][PNNN-1] == " " or len(PSSIG[PSSFFF]) == PNNN:
                    PCT += 1
                    if PSSBVAR:
                        if len(PSSBVAR) > 70:
                            PSSSIG[PSSIII] = PSSBLIM + " "
                            PSSIII += 1
                            PSSBVAR = PSSBVAR1
    if PSSBVAR:
        PSSSIG[PSSIII] = PSSBVAR
    if PSSSIG[1] == "" or PSSSIG[1] == " ":
        PSSSIG[1] = PSSSIG[2]
        del PSSSIG[2]
    for PSSLPX in range(0, len(PSSSIG)+1):
        if PSSLPX:
            if PSSLPX == 1:
                EN^DDIOL(" ")
            EN^DDIOL(" " + str(PSSSIG[PSSLPX]))

def HELPADD():
    if len(PSSIG[PSSCTX]) + len(PSSZ1) + 1 < 246:
        PSSIG[PSSCTX] = PSSIG[PSSCTX] + " " + PSSZ1
        return True
    PSSCTX += 1
    PSSIG[PSSCTX] = PSSZ1
    return False