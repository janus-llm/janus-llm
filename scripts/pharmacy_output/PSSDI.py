def DIC(PSSFILE, PSSAPP, DIC, X, DLAYGO, PSSSCRDT, PSSSCRUS, PSSVACL):
    PSSX1 = None  # ADDED BY TS ON 09.20.2006
    PSSDIY = ""
    if int(PSSFILE) <= 0:
        PSSDIY = -1
        return
    PSRTEST = TEST(PSSFILE)
    if not PSRTEST:
        PSSDIY = -1
        return
    DIC.pop("S", None)
    if int(PSSSCRDT) > 0:
        SCREEN()
    if PSSVACL and PSSVACL.get(0):
        if PSSFILE == 50:
            VACL()
            if PSSX1:
                if "S" in DIC:
                    DIC["S"] = DIC["S"] + " " + PSSX1
                else:
                    DIC["S"] = PSSX1
    if PSSSCRUS and PSSFILE == 50:
        PSSAPLP = None
        DIC["S"] = DIC.get("S", "") + " ".join(
            [
                f"FOR PSSAPLP=1:1:$L(PSSSCRUS) I $P($G(^(2)),\"^\",3)[$E(PSSSCRUS,PSSAPLP) Q",
            ]
        )
    if not PSRTEST.split("^")[1]:
        DLAYGO = None
        if DIC.get(0):
            DIC[0] = DIC[0].replace("L", "")
            if not DIC[0]:
                PSSDIY = -1
                return
    if not DIC.get(0) and not X:
        PSSDIY = -1
        return
    DTOUT = None
    DUOUT = None
    # ^DIC
    Q()


def DO(PSSFILE, PSSAPP, DIC):
    PSSDIY = ""
    if int(PSSFILE) <= 0:
        PSSDIY = -1
        return
    PSRTEST = TEST(PSSFILE)
    if not PSRTEST:
        PSSDIY = -1
        return
    DTOUT = None
    DUOUT = None
    # ^DO^DIC1
    return


def IX(PSSFILE, PSSAPP, DIC, D, X, DLAYGO):
    PSSDIY = ""
    if int(PSSFILE) <= 0:
        PSSDIY = -1
        return
    PSRTEST = TEST(PSSFILE)
    if not PSRTEST:
        PSSDIY = -1
        return
    if not PSRTEST.split("^")[1]:
        DLAYGO = None
        if DIC.get(0):
            DIC[0] = DIC[0].replace("L", "")
            if not DIC[0]:
                PSSDIY = -1
                return
    if not DIC.get(0) and not X:
        PSSDIY = -1
        return
    DTOUT = None
    DUOUT = None
    # ^IX^DIC
    return


def MIX(PSSFILE, PSSAPP, DIC, D, X, DLAYGO, PSSSCRDT, PSSSCRUS, PSSVACL):
    PSSX1 = None  # ADDED BY TS ON 09.20.2006
    PSSDIY = ""
    if int(PSSFILE) <= 0:
        PSSDIY = -1
        return
    PSRTEST = TEST(PSSFILE)
    if not PSRTEST:
        PSSDIY = -1
        return
    DIC.pop("S", None)
    if int(PSSSCRDT) > 0:
        SCREEN()
    if PSSVACL and PSSVACL.get(0):
        if PSSFILE == 50:
            VACL()
            if PSSX1:
                if "S" in DIC:
                    DIC["S"] = DIC["S"] + " " + PSSX1
                else:
                    DIC["S"] = PSSX1
    if PSSSCRUS and PSSFILE == 50:
        PSSAPLP = None
        DIC["S"] = DIC.get("S", "") + " ".join(
            [
                f"FOR PSSAPLP=1:1:$L(PSSSCRUS) I $P($G(^(2)),\"^\",3)[$E(PSSSCRUS,PSSAPLP) Q",
            ]
        )
    if not PSRTEST.split("^")[1]:
        DLAYGO = None
        if DIC.get(0):
            DIC[0] = DIC[0].replace("L", "")
            if not DIC[0]:
                PSSDIY = -1
                return
    if not DIC.get(0) and not X:
        PSSDIY = -1
        return
    DTOUT = None
    DUOUT = None
    # ^MIX^DIC1
    return


def FILE(PSSFILE, PSSAPP, DIC, DA, X, DINUM, DLAYGO):
    PSSDIY = ""
    if int(PSSFILE) <= 0:
        PSSDIY = -1
        return
    PSRTEST = TEST(PSSFILE)
    if not PSRTEST:
        PSSDIY = -1
        return
    if not PSRTEST.split("^")[1]:
        PSSDIY = -1
        return
    DTOUT = None
    DUOUT = None
    DO = None
    # ^FILE^DICN
    return


def DIE(PSSFILE, PSSAPP, DIE, DA, DR, DIDEL):
    PSSDIY = ""
    if int(PSSFILE) <= 0:
        PSSDIY = -1
        return
    PSRTEST = TEST(PSSFILE)
    if not PSRTEST:
        PSSDIY = -1
        return
    if not PSRTEST.split("^")[1]:
        PSSDIY = -1
        return
    DTOUT = None
    # ^DIE
    return


def EN1(PSSFILE, PSSAPP, DIC, L, FLDS, BY, FR, TO, DHD):
    PSSDIY = ""
    if int(PSSFILE) <= 0:
        PSSDIY = -1
        return
    PSRTEST = TEST(PSSFILE)
    if not PSRTEST:
        PSSDIY = -1
        return
    # ^EN1^DIP
    return


def EN(PSSFILE, PSSAPP, DIC, DR, DA, DIQ):
    PSSDIY = ""
    if int(PSSFILE) <= 0:
        PSSDIY = -1
        return
    PSRTEST = TEST(PSSFILE)
    if not PSRTEST:
        PSSDIY = -1
        return
    # ^EN^DIQ1
    return


def FNAME(PSSFNO, PSSFILE):
    # Return the label for the field of the File or Subfile passed in
    # PSSFNO  - Field number
    # PSSFILE - File or Subfile number
    return PSS50E(PSSFNO, PSSFILE)


def TEST(PSTFILE):
    PSFFLAG = 0
    PSRSLT = "0^0"
    for PSFLOOP in range(1, 1000):
        PSFTEST = FILE2[PSFLOOP].split(";;")[1]
        if int(PSFTEST.split(";;")[0]) == PSTFILE:
            PSRSLT = "1^0"
            PSLNODE = FILE2[PSFLOOP]
            for CNT in range(3, len(PSLNODE.split(";;"))):
                PSSAPP2 = PSLNODE.split(";;")[CNT]
                if PSSAPP2 == PSSAPP:
                    PSFFLAG = 1
                    PSRSLT = "1^1"
                    break
            break
    return PSRSLT


def SCREEN():
    global DIC
    PSSINFLG = 0
    for PSSILOOP in range(1, 1000):
        PSSILOC = FILE3[PSSILOOP].split(";;")[1]
        if int(PSSILOC.split(";;")[0]) == PSSFILE:
            PSSINFLG = 1
            PSSINODE = FILE3[PSSILOOP]
            PSSSUBSC = PSSINODE.split(";;")[3]
            PSSPIECE = PSSINODE.split(";;")[4]
            if PSSSUBSC and PSSPIECE:
                DIC["S"] = (
                    f"I $P($G(^(PSSSUBSC)),\"^\",PSSPIECE)=\"\"!(+$P($G(^(PSSSUBSC)),\"^\",PSSPIECE)>+$G(PSSSCRDT))"
                )
            break


def VACL():
    global DIC
    PSSVACL1 = 0
    PSSX = "=" if PSSVACL.get("R") else "'="
    PSSX1 = None
    while True:
        PSSVACL1 += 1
        if PSSVACL1 not in PSSVACL or PSSVACL1 == "R" or PSSVACL1 == "P":
            continue
        PSSX1 = (
            f"I $P(^PSDRUG(+Y,0),U,2){PSSX}\"{PSSVACL1}\""
            if not PSSX1
            else f"{PSSX1}{'!' if PSSX == '=' else '&'}($P(^PSDRUG(+Y,0),U,2){PSSX}\"{PSSVACL1}\")"
        )
    return


def Q():
    global PSSVACL, PSSVACL1, PSSX, PSSX1, PSSFILE, PSSAPP, PSSINODE, PSSSCRUS
    PSSVACL = None
    PSSVACL1 = None
    PSSX = None
    PSSX1 = None
    PSSFILE = None
    PSSAPP = None
    PSSINODE = None
    PSSSCRUS = None


# File2
FILE2 = [
    "50;;PSX;;PSD;;PSJ;;PSN;;PSO;;PSGW;;PSS",
    "50.1;;PSX;;PSD;;PSJ;;PSN;;PSO;;PSGW;;PSS",
    "50.0214;;PSX;;PSD;;PSJ;;PSN;;PSO;;PSGW;;PSS",
    "50.037;;PSX;;PSD;;PSJ;;PSN;;PSO;;PSGW;;PSS",
    "50.065;;PSX;;PSD;;PSJ;;PSN;;PSO;;PSGW;;PSS",
    "50.0212;;PSX;;PSD;;PSJ;;PSN;;PSO;;PSGW;;PSS",
    "50.0441;;PSX;;PSD;;PSJ;;PSN;;PSO;;PSGW;;PSS",
    "50.01;;PSX;;PSD;;PSJ;;PSN;;PSO;;PSGW;;PSS",
    "50.02;;PSX;;PSD;;PSJ;;PSN;;PSO;;PSGW;;PSS",
    "50.0903;;PSX;;PSD;;PSJ;;PSN;;PSO;;PSGW;;PSS",
    "50.0904;;PSX;;PSD;;PSJ;;PSN;;PSO;;PSGW;;PSS",
    "50.4;;PSJ;;PSS",
    "50.606;;PSJ;;PSN;;PSS",
    "50.7;;PSJ;;PSO;;PSN;;PSS",
    "50.76;;PSJ;;PSO;;PSN;;PSS",
    "50.72;;PSJ;;PSO;;PSN;;PSS",
    "51;;PSJ;;PSS",
    "51.01;;PSJ;;PSS",
    "51.1;;PSJ;;PSS",
    "51.11;;PSJ;;PSS",
    "51.17;;PSJ;;PSS",
    "51.2;;PSJ;;PSS",
    "51.5;;PSS",
    "52.6;;PSJ;;PSN;;PSS",
    "52.61;;PSJ;;PSN;;PSS",
    "52.62;;PSJ;;PSN;;PSS",
    "52.63;;PSJ;;PSN;;PSS",
    "52.64;;PSJ;;PSN;;PSS",
    "52.7;;PSJ;;PSN;;PSS",
    "52.702;;PSJ;;PSN;;PSS",
    "52.703;;PSJ;;PSN;;PSS",
    "52.704;;PSJ;;PSN;;PSS",
    "54;;PSS;;PSO",
    "54.1;;PSS;;PSO",
    "9009032.3;;PSS",
    "9009032.5;;PSS",
]


# File3
FILE3 = [
    "50;;I;;1",
    "50.606;;0;;2",
    "50.7;;0;;4",
    "51.2;;0;;5",
    "52.6;;I;;1",
    "52.7;;I;;1",
]


def PSS50E(PSSFNO, PSSFILE):
    # Placeholder for PSS50E function
    pass