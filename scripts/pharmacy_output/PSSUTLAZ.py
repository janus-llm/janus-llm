def EN3(PSSBINTR, PSSBLGTH):
    # Pass in to EN3 the internal number from 50.7, and the length of the
    # array you want. Returns expanded Instructions is PSSBSIG array
    PSSBSIG = []
    X, BVAR, BVAR1, III, CNT, NNN, BLIM, Y, PISIG, Z0, Z1, CNTZ, FFF = (None,) * 12

    if not PSSBINTR or not PSSBLGTH:
        return

    X = "^PS(50.7," + str(PSSBINTR) + ",\"INS\")"
    X = X.split("^")[1]  # Get the value from the global

    if not X:
        return

    PISIG = [""]  # Initialize PISIG array
    CNTZ = 1

    if len(X) < 1:
        return

    for Z0 in range(1, len(X.split(" ")) + 1):
        if not Z0:
            START()
            break

        Z1 = X.split(" ")[Z0 - 1]

        if Z1:
            ADD()

    START()

    BVAR, BVAR1, III = "", "", 1

    for FFF in PISIG:
        if not FFF:
            break

        CNT = 0

        for NNN in range(1, len(FFF) + 1):
            if FFF[NNN - 1] == " " or len(FFF) == NNN:
                CNT += 1

                if len(BVAR) + len(BVAR1) > PSSBLGTH:
                    PSSBSIG.append(BLIM + " ")
                    III += 1
                    BVAR = BVAR1

                BVAR1 = FFF.split(" ")[CNT - 1]
                BLIM = BVAR
                BVAR = BVAR1

    if BVAR:
        PSSBSIG.append(BVAR)

    if not PSSBSIG[0] or PSSBSIG[0] == " ":
        PSSBSIG[0] = PSSBSIG[1]
        del PSSBSIG[1]

    PSSX = {}

    for CNTZ in range(1, len(PSSBSIG) + 1):
        PSSX["PI", CNTZ] = PSSBSIG[CNTZ - 1]

    return


def ADD():
    global CNTZ
    if len(PISIG[CNTZ - 1]) + len(Z1) + 1 < 246:
        PISIG[CNTZ - 1] += " " + Z1
    else:
        CNTZ += 1
        PISIG.append(Z1)


def START():
    global BVAR, BVAR1, III
    BVAR, BVAR1, III = "", "", 1

    for FFF in PISIG:
        if not FFF:
            break

        CNT = 0

        for NNN in range(1, len(FFF) + 1):
            if FFF[NNN - 1] == " " or len(FFF) == NNN:
                CNT += 1

                if len(BVAR) > PSSBLGTH:
                    PSSBSIG[III - 1] = BLIM + " "
                    III += 1
                    BVAR = BVAR1

                BVAR1 = FFF.split(" ")[CNT - 1]
                BLIM = BVAR
                BVAR = BVAR1

    if BVAR:
        PSSBSIG[III - 1] = BVAR

    if not PSSBSIG[0] or PSSBSIG[0] == " ":
        PSSBSIG[0] = PSSBSIG[1]
        del PSSBSIG[1]

    return


def DEA(PSSDIENM):
    # Return DEA Special Handling for CPRS Dose Call
    # 1 Requires wet sig, DEA contains 1, or a 2
    # 2 = Controlled Sub, no wet sig required, DEA contains 3, 4, or 5
    # 0 = others
    if not PSSDIENM:
        return

    PSSDEAX, PSSDEAXV = None, None
    PSSDEAX = "^PSDRUG," + str(PSSDIENM) + ",0"
    PSSDEAX = PSSDEAX.split("^")[3]  # Get the value from the global

    if "1" in PSSDEAX or "2" in PSSDEAX:
        PSSDEAXV = 1
    elif "3" in PSSDEAX or "4" in PSSDEAX or "5" in PSSDEAX:
        PSSDEAXV = 2
    else:
        PSSDEAXV = 0

    PSSX["DD", PSSDIENM] = PSSX["DD", PSSDIENM] + "^" + PSSDEAXV
    return


def HELP():
    if not X:
        return

    PSSSIG, PSSYX, PSSZ0, PSSZ1, PSSCTX, PSSLPX, PSSBVAR, PSSBVAR1, PSSIII, PSSFFF, PCT, PNNN, PSSBLIM, PSSIG = [], None, None, None, None, None, None, None, None, None, None, None, None

    PSSIG = [""]  # Initialize PSSIG array
    PSSCTX = 1

    if len(X) < 1:
        return

    for PSSZ0 in range(1, len(X.split(" ")) + 1):
        if not PSSZ0:
            HELP1()
            break

        PSSZ1 = X.split(" ")[PSSZ0 - 1]

        if PSSZ1:
            HELPADD()

    HELP1()

    PSSBVAR, PSSBVAR1, PSSIII = "", "", 1

    for PSSFFF in PSSIG:
        if not PSSFFF:
            break

        PCT = 0

        for PNNN in range(1, len(PSSIG[PSSFFF]) + 1):
            if PSSIG[PSSFFF][PNNN - 1] == " " or len(PSSIG[PSSFFF]) == PNNN:
                PCT += 1

                if len(PSSBVAR) + len(PSSBVAR1) > 70:
                    PSSSIG[PSSIII - 1] = PSSBLIM + " "
                    PSSIII += 1
                    PSSBVAR = PSSBVAR1

                PSSBVAR1 = PSSIG[PSSFFF].split(" ")[PCT - 1]
                PSSBLIM = PSSBVAR
                PSSBVAR = PSSBVAR1

    if PSSBVAR:
        PSSSIG[PSSIII - 1] = PSSBVAR

    if not PSSSIG[0] or PSSSIG[0] == " ":
        PSSSIG[0] = PSSSIG[1]
        del PSSSIG[1]

    for PSSLPX in PSSSIG:
        if not PSSLPX:
            break

        if PSSLPX == 1:
            EN^DDIOL(" ")
        EN^DDIOL(" " + PSSSIG[PSSLPX])


def HELPADD():
    global PSSCTX
    if len(PSSIG[PSSCTX - 1]) + len(PSSZ1) + 1 < 246:
        PSSIG[PSSCTX - 1] += " " + PSSZ1
    else:
        PSSCTX += 1
        PSSIG.append(PSSZ1)