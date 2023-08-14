def CHECK(PSSROIT):
    # PSSDACT = ARRAY OF ACTIVE DISPENSE DRUGS
    # PSSDACTI = ARRAY OF INACTIVE DISPENSE DRUGS
    # PSSSACT = ARRAY OF ACTIVE SOLUTIONS
    # PSSSACTI = ARRAY OF INACTIVE SOLUTIONS
    # PSSAACT = ARRAY OF ACTIVE ADDITIVES
    # PSSAACTI = ARRAY OF INACTIVE ADDITIVES
    PSSDACT = {}
    PSSDACTI = {}
    PSSSACT = {}
    PSSSACTI = {}
    PSSAACT = {}
    PSSAACTI = {}

    PSSRDATE = None
    PSSRFLAG = None
    PSSAI = None

    if not PSSROIT:
        return

    if PSSROIT in ^PS(50.7,0):
        for PSSAI in ^PS(52.7, "AOI", PSSROIT, 0):
            if PSSAI in ^PS(52.7, 0):
                PSSRDATE = ^PS(52.7, PSSAI, "I") ^ 0
                DTE()
                if PSSRFLAG:
                    PSSSACT[PSSAI] = ""
                else:
                    PSSSACTI[PSSAI] = ""

        for PSSAI in ^PS(52.6, "AOI", PSSROIT, 0):
            if PSSAI in ^PS(52.6, 0):
                PSSRDATE = ^PS(52.6, PSSAI, "I") ^ 0
                DTE()
                if PSSRFLAG:
                    PSSAACT[PSSAI] = ""
                else:
                    PSSAACTI[PSSAI] = ""

        for PSSAI in ^PSDRUG("ASP", PSSROIT, 0):
            if PSSAI in ^PSDRUG(0):
                PSSRDATE = ^PSDRUG(PSSAI, "I") ^ 0
                DTE()
                if PSSRFLAG:
                    PSSDACT[PSSAI] = ""
                else:
                    PSSDACTI[PSSAI] = ""

def DTE():
    global PSSRFLAG
    if not PSSRDATE or int(PSSRDATE) > int(DT):
        PSSRFLAG = 1