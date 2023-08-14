def IV(PSSADFOI):
    PSSADFRS = ""
    PSSADFXX = PSSADFCT = 0
    if not PSSADFOI:
        return PSSADFRS
    PSSADFLP = 0
    while True:
        PSSADFLP = next(iter(filter(lambda x: x > PSSADFLP, ^PS(52.6, "AOI", PSSADFOI))))
        if not PSSADFLP or PSSADFXX:
            break
        PSSADFNN = PSSADFLP + ","
        PSSADFLD = GETS^DIQ(52.6, PSSADFNN, "12;18", "I", "PSSADFLD", "PSSADFER")
        if PSSADFER["DIERR":
            continue
        PSSADFIN = PSSADFLD[52.6, PSSADFNN, 12, "I"]
        PSSADFHD = PSSADFLD[52.6, PSSADFNN, 18, "I"]
        if PSSADFIN and PSSADFIN <= DT:
            continue
        if not PSSADFHD:
            PSSADFXX = 1
            continue
        if not PSSADFCT:
            PSSADFRS = PSSADFHD
            PSSADFCT = 1
            continue
        if PSSADFHD != PSSADFRS:
            PSSADFXX = 1
            break
    if PSSADFXX:
        PSSADFRS = ""
    return PSSADFRS


def RESET():
    for PSSDBCD1 in PSSDBCDA:
        for PSSDBCD2 in PSSDBCDA[PSSDBCD1]:
            PSSDBCD3 = PSSDBCDA[PSSDBCD1][PSSDBCD2]
            if PSSDBCD3 != "":
                PSSDBCDP[PSSDBRLS][PSSDBCD3] = ""


def SGEN():
    PSSDBCD6 = 1
    for PSSDBCD5 in PSSDBCDP[PSSDWE5]:
        PSSDBCD7 = PSSDBCAR[PSSDBCD5][1]
        PSSDBCD8 = PSSDBCAR[PSSDBCD5][2]
        if PSSDBCD7 == "" or PSSDBCD8 == "":
            continue
        if ^TMP[$J][PSSDBASE]["OUT"]["DOSE"][PSSDBCD5][PSSDBCD7]["GENERAL"]["MESSAGE"][PSSDBCD8] != "":
            if PSSDBASA:
                ^TMP[$J][PSSDBASF]["OUT"]["DOSE"][PSSDWE5][PSSDBCD7]["3_GENERAL"]["MESSAGE"][PSSDBCD8][PSSDBCD6] = ^TMP[$J][PSSDBASE]["OUT"]["DOSE"][PSSDBCD5][PSSDBCD7]["GENERAL"]["MESSAGE"][PSSDBCD8]
            if PSSDBASB:
                ^TMP[$J][PSSDBASG]["OUT"][PSSDWE5]["MESSAGE"]["3_GENERAL"][PSSDBCD8][PSSDBCD6] = ^TMP[$J][PSSDBASE]["OUT"]["DOSE"][PSSDBCD5][PSSDBCD7]["GENERAL"]["MESSAGE"][PSSDBCD8]
        PSSDBCD6 += 1


def SGENA():
    PSSDBCD7 = PSSDBCAR[PSSDBCD5][2]
    PSSDBCD8 = PSSDBCAR[PSSDBCD5][3]
    if PSSDBCD7 == "" or PSSDBCD8 == "":
        return
    if ^TMP[$J][PSSDBASE]["OUT"]["DOSE"][PSSDBCD5][PSSDBCD7]["GENERAL"]["MESSAGE"][PSSDBCD8] != "":
        if PSSDBASA:
            ^TMP[$J][PSSDBASF]["OUT"]["DOSE"][PSSDWE5][PSSDBCD7]["3_GENERAL"]["MESSAGE"][PSSDBCD8][PSSDBCD6] = ^TMP[$J][PSSDBASE]["OUT"]["DOSE"][PSSDBCD5][PSSDBCD7]["GENERAL"]["MESSAGE"][PSSDBCD8]
        if PSSDBASB:
            ^TMP[$J][PSSDBASG]["OUT"][PSSDWE5]["MESSAGE"]["3_GENERAL"][PSSDBCD8][PSSDBCD6] = ^TMP[$J][PSSDBASE]["OUT"]["DOSE"][PSSDBCD5][PSSDBCD7]["GENERAL"]["MESSAGE"][PSSDBCD8]


def REM():
    for PSSRMV1 in ^TMP[$J][PSSDBASG]["OUT"]:
        for PSSRMV2 in ^TMP[$J][PSSDBASG]["OUT"][PSSRMV1]:
            if PSSDBCAR[PSSRMV2][14]:
                del ^TMP[$J][PSSDBASG]["OUT"][PSSRMV1][PSSRMV2]
                continue
            for PSSRMV7 in ^TMP[$J][PSSDBASG]["OUT"][PSSRMV1][PSSRMV2]["ERROR"]:
                if ^TMP[$J][PSSDBASG]["OUT"][PSSRMV1][PSSRMV2]["ERROR"][PSSRMV7]["WARN"] == "Warning" and not PSSRMV2.split(";")[5]:
                    del ^TMP[$J][PSSDBASG]["OUT"][PSSRMV1][PSSRMV2]["ERROR"][PSSRMV7]["WARN"]
                    PSSDBCAR[PSSRMV2][13] = ""
                    continue
                del ^TMP[$J][PSSDBASG]["OUT"][PSSRMV1][PSSRMV2]["ERROR"][PSSRMV7]["MSG"]
                del ^TMP[$J][PSSDBASG]["OUT"][PSSRMV1][PSSRMV2]["ERROR"][PSSRMV7]["TEXT"]
            if PSSDBCAR[PSSRMV2][15] or PSSDBCAR[PSSRMV2][16] or PSSRMV2.split(";")[5]:
                del ^TMP[$J][PSSDBASG]["OUT"][PSSRMV1][PSSRMV2]["MESSAGE"]["2_RANGE"]
            if ^TMP[$J][PSSDBASG]["OUT"][PSSRMV1][PSSRMV2]["MESSAGE"]:
                PSSPERR = PSSDBCAR[PSSRMV2][9]
                if PSSPERR == "OTIC" or PSSPERR == "OPHTHALMIC" or PSSPERR == "INTRANASAL":
                    ^TMP[$J][PSSDBASG]["OUT"][PSSRMV1][PSSRMV2]["MESSAGE"][".1_INTRO"] = "Dosing Information provided is PER " + PSSPERR + ":"
    if PSSDBASB:
        for PSSDADO in PSSDBCAR:
            if PSSDBCAR[PSSDADO][29]:
                CHKCFREQ^PSSDSUTA(PSSDADO, PSSDBASE, PSSDBASG, PSSDBCAR)
    if PSSDBASA:
        UPCPRS^PSSDSUTL()
    for PSSRMV8 in PSSDBCAR:
        if PSSDBCAR[PSSRMV8][13] and PSSDSDPL[PSSRMV8] and not PSSDBCAR[PSSRMV8][14]:
            PSSRMVX = "Dosing Checks"
            if PSSDBCAR[PSSRMV8][15] or PSSDBCAR[PSSRMV8][16]:
                PSSRMVX = "Maximum Single Dose Check"
            if PSSDBCAR[PSSRMV8][17]:
                ^TMP[$J][PSSDBASG]["OUT"][PSSRMV8.split(";")[4]][PSSRMV8]["EXCEPTIONS"][1] = PSSRMVX + " could not be performed for Drug: " + PSSDBCAR[PSSRMV8][2] + ", please complete a manual check for appropriate Dosing."


def SQX(PSSQBSS):
    PSSQBARS = ""
    PSSADFXX = False
    if not PSSQBSS:
        return PSSQBARS
    PSSQBSTM = PSSQBSS
    while True:
        PSSQBSTM = PSSQBSS
        PSSQBSTM = PSSQBSS[:-4]
        if not PSSQBSTM or PSSADFXX:
            break
        PSSQBA3 = len(PSSQBSS)
        if PSSQBA3 > 4:
            PSSQBA4 = PSSQBSS[PSSQBA3 - 3:PSSQBA3]
            PSSQBA4 = PSSQBA4.upper()
            if PSSQBA4 == " PRN":
                PSSQBSTM = PSSQBSS[:PSSQBA3 - 4]
                PSSQBSTM = PSSQBSS
        if "@" not in PSSQBSS:
            return PSSQBARS
        PSSQBA5 = len(PSSQBSS)
        PSSQBA6 = PSSQBSS.index("@") + 1
        if PSSQBA6 > PSSQBA5:
            return PSSQBARS
        PSSQBSTM = PSSQBSS[PSSQBA6 - 1:PSSQBA5]
        if not PSSQBSTM or PSSADFXX:
            return PSSQBARS
        PSSQBA3 = len(PSSQBSTP)
        if PSSQBA3 > 4:
            PSSQBA4 = PSSQBSTP[PSSQBA3 - 3:PSSQBA3]
            PSSQBA4 = PSSQBA4.upper()
            if PSSQBA4 == " PRN":
                PSSQBSTM = PSSQBSTP[:PSSQBA3 - 4]
                PSSQBSTM = PSSQBSTP
        for PSSQBA1 in ^PS(51.1, "APPSJ", PSSQBSTM):
            PSSQBA2 = ^PS(51.1, PSSQBA1, "0")
            if not PSSQBA2:
                continue
            PSSQBARS = PSSQBA2[9] + "^" + PSSQBA2[10]
            PSSADFXX = True
            break
    return PSSQBARS


def SXCL():
    if PSSDBEB3:
        if PSSDBEB2[4] == "" or PSSDBEB2[5] == "":
            EXCPS^PSSDSAPD(1)
        $P(PSSDBCAR[PSSDBEB1], "^", 21) = 1
        EXCPS^PSSDSAPD(3)
        INFERRS^PSSDSAPK()
        if PSSDBCAZ[PSSDBEB1]["FRQ_ERROR"]:
            EXCPS^PSSDSAPD(2)
        if PSSDBCAR[PSSDBEB1][5]:
            $P(PSSDBCAR[PSSDBEB1], "^", 6) = 1
            $P(PSSDBCAR[PSSDBEB1], "^", 10) = 1
        else:
            $P(PSSDBCAR[PSSDBEB1], "^") = "S"
            $P(PSSDBCAR[PSSDBEB1], "^", 7) = 1


def INFRQ():
    if PSSDBEB3:
        if PSSDBEB2[11] == "":
            return
        EXCPS^PSSDSAPD(2)
        $P(PSSDBCAR[PSSDBEB1], "^") = "S"
        if PSSDBCAR[PSSDBEB1][5]:
            $P(PSSDBCAR[PSSDBEB1], "^", 8) = 1
            $P(PSSDBCAR[PSSDBEB1], "^", 10) = 1
        ^TMP[$J][PSSDBASE]["IN"]["DOSE"][PSSDBEB1][8] = 1
        ^TMP[$J][PSSDBASE]["IN"]["DOSE"][PSSDBEB1][9] = 1
        ^TMP[$J][PSSDBASE]["IN"]["DOSE"][PSSDBEB1][10] = ^TMP[$J][PSSDBASE]["IN"]["DOSE"][PSSDBEB1][7]
        $P(PSSDBCAR[PSSDBEB1], "^", 33) = 1


def DUNIT():
    PSSDBEG1 = $P(PSSDBCAR[PSSDBEB1], "^", 3)
    if PSSDBEG1:
        PSSDBEG2 = ^PSDRUG[PSSDBEG1, 2]
        PSSDBEG3 = ^PSDRUG[PSSDBEG1, 2, 3]
        if PSSDBEG2 and PSSDBEG3:
            PSSDBEG5 = $$DFSU^PSNAPIS(PSSDBEG2, PSSDBEG3)
            PSSDBEG6 = PSSDBEG5[6]
            if PSSDBEG6:
                PSSDBEG7 = $$UNIT^PSSDSAPI(PSSDBEG6)
                if PSSDBEG7:
                    return PSSDBEG7
    if PSSDBEG1:
        PSSDBEG2 = ^PSDRUG[PSSDBEG1, 2]
        if PSSDBEG2:
            PSSDBEG3 = ^PS[50.7, PSSDBEG2, 2]
            if PSSDBEG3:
                for PSSDBEG5 in ^PS[50.606, PSSDBEG3, "NOUN"]:
                    PSSDBEG6 = ^PS[50.606, PSSDBEG3, "NOUN", PSSDBEG5]
                    if PSSDBEG6:
                        PSSDBEG7 = $$UNIT^PSSDSAPI(PSSDBEG6)
                        if PSSDBEG7:
                            return PSSDBEG7
    return "EACH"


def INRATE():
    if not PSSDBEB3:
        return
    if PSSDBEB2[5] == "" or PSSDBEB2[6] == "":
        EXCPS^PSSDSAPD(1)
    $P(PSSDBCAR[PSSDBEB1], "^", 21) = 1
    EXCPS^PSSDSAPD(3)
    INFERRS^PSSDSAPK()
    if PSSDBCAZ[PSSDBEB1]["FRQ_ERROR"]:
        EXCPS^PSSDSAPD(2)
    if PSSDBCAR[PSSDBEB1][5]:
        $P(PSSDBCAR[PSSDBEB1], "^", 6) = 1
        $P(PSSDBCAR[PSSDBEB1], "^", 10) = 1
    else:
        $P(PSSDBCAR[PSSDBEB1], "^") = "S"
        $P(PSSDBCAR[PSSDBEB1], "^", 7) = 1


def ONT():
    PSSOTOI = ^PSDRUG[+PSSDBIFG, 2]
    if not PSSOTOI:
        return
    for PSSOTOL in ^PSDRUG["ASP", PSSOTOI:
        if PSSOTOL != +PSSDBIFG:
            if EXMT^PSSDSAPI(PSSOTOL):
                continue
            PSSOTOD = ^PSDRUG[PSSOTOL, "I"]
            if PSSOTOD and PSSOTOD <= DT:
                continue
            PSSOTOA = ^PSDRUG[PSSOTOL, 2, 3]
            if PSSOTOA not in PSSDBFDB["PACKAGE"]:
                continue
            PSSOTOB2 = ^PSDRUG[PSSOTOL, "ND"]
            PSSOTOB1 = PSSOTOB2[1]
            PSSOTOB3 = PSSOTOB2[3]
            if not PSSOTOB1 or not PSSOTOB3:
                continue
            PSSOTOB4 = $$PROD0^PSNAPIS(PSSOTOB1, PSSOTOB3)
            if not PSSOTOB4[7]:
                continue
            return
    PSSDBIFL = 0
    PSSOTON = ^PSDRUG[+PSSDBIFG, 0]
    PSSDBFDB[PSSDBLP, "DRUG_NM"] = PSSOTON if PSSOTON else "UNKNOWN DRUG NAME"
    PSSDBFDB[PSSDBLP, "DRUG_IEN"] = +PSSDBIFG


def INFRQ():
    if not PSSDBEB3:
        return
    if PSSDBEB2[11] == "":
        return
    EXCPS^PSSDSAPD(2)
    $P(PSSDBCAR[PSSDBEB1], "^") = "S"
    if PSSDBCAR[PSSDBEB1][5]:
        $P(PSSDBCAR[PSSDBEB1], "^", 8) = 1
        $P(PSSDBCAR[PSSDBEB1], "^", 10) = 1
    ^TMP[$J][PSSDBASE]["IN"]["DOSE"][PSSDBEB1][8] = 1
    ^TMP[$J][PSSDBASE]["IN"]["DOSE"][PSSDBEB1][9] = 1
    ^TMP[$J][PSSDBASE]["IN"]["DOSE"][PSSDBEB1][10] = ^TMP[$J][PSSDBASE]["IN"]["DOSE"][PSSDBEB1][7]
    $P(PSSDBCAR[PSSDBEB1], "^", 33) = 1


def DUNIT():
    PSSDBEG1 = $P(PSSDBCAR[PSSDBEB1], "^", 3)
    if PSSDBEG1:
        PSSDBEG2 = ^PSDRUG[PSSDBEG1, 2]
        PSSDBEG3 = ^PSDRUG[PSSDBEG1, 2, 3]
        if PSSDBEG2 and PSSDBEG3:
            PSSDBEG5 = $$DFSU^PSNAPIS(PSSDBEG2, PSSDBEG3)
            PSSDBEG6 = PSSDBEG5[6]
            if PSSDBEG6:
                PSSDBEG7 = $$UNIT^PSSDSAPI(PSSDBEG6)
                if PSSDBEG7:
                    return PSSDBEG7
    if PSSDBEG1:
        PSSDBEG2 = ^PSDRUG[PSSDBEG1, 2]
        if PSSDBEG2:
            PSSDBEG3 = ^PS[50.7, PSSDBEG2, 2]
            if PSSDBEG3:
                for PSSDBEG5 in ^PS[50.606, PSSDBEG3, "NOUN"]:
                    PSSDBEG6 = ^PS[50.606, PSSDBEG3, "NOUN", PSSDBEG5]
                    if PSSDBEG6:
                        PSSDBEG7 = $$UNIT^PSSDSAPI(PSSDBEG6)
                        if PSSDBEG7:
                            return PSSDBEG7
    return "EACH"