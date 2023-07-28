def PSSNFI():
    print("\nThis report shows the dispense drugs and orderable items")
    print("with the formulary information associated with them.")

    PSSHOW = input("Print Report for (A)ll or (S)elect a Range (default=S): ")
    if PSSHOW != "A":
        PSSHOW = "S"
        PSSBEG = input("Enter the beginning letter of the range: ")
        PSSEND = input("Enter the ending letter of the range: ")
        PSSSRT = "X"
    else:
        PSSBEG = "A"
        PSSEND = "Z"
        PSSSRT = "A"

    PSSNUMB = next(iter(PSDRUG_B))
    if PSSNUMB:
        print("\nThere are drugs in the Drug file with leading numerics.")
        PSSNUMBX = input("Print report for drugs with leading numerics? (Y/N): ")
        if PSSNUMBX == "Y":
            PSSSRT = "N"

    PSSBEG = input("Select a Range (1 letter or A-C format): ")
    PSSEND = PSSBEG

    PSSTX = 0
    PSSFLAG = 0
    PSSTX = input("Include drug text information? (Y/N): ")

    if PSSTX.lower() == "y":
        PSSTX = 1

    print("\nReport will be for drugs starting with the letter", PSSBEG)
    print("and ending with drugs starting with the letter", PSSEND)

    PSSOUT = 0
    PSSDV = "C"
    PSSPGCT = 0
    PSSPGLNG = 27
    PSSPRT = 0
    PSSPGCT = 1

    print("\nDate printed: ", DT, "\tPage: ", PSSPGCT)
    print("\nGeneric Name", " " * 37, "Local", "Visn", "National", "Restriction", "Appl", "Drug")
    print(" " * 43, "Pkg", "Text", "Use")
    print("-" * 132)
    PSSPGCT += 1

    PSSLCL = chr(ord(PSSBEG) - 1) + "zzzz"

    while True:
        PSSLCL = next((x for x in PSDRUG_B if x > PSSLCL), "")

        if PSSSRT == "N" and not PSSLCL:
            break
        if PSSSRT == "X" and PSSLCL > PSSEND + "zzzz":
            break
        if PSSLCL == "":
            break

        PSSB = next(iter(PSDRUG_B[PSSLCL]), None)
        if not PSSB:
            continue

        LOC = ""
        VISN = ""
        NAT = ""
        OIFS = ""
        DRTX = ""
        DEA = ""
        TXT = ""
        APU = ""
        OINM = ""

        if not PSDRUG_B[PSSB]["I"] or int(PSDRUG_B[PSSB]["I"]) > DT:
            NOTHG()
            POI()
            DTEXT()
            ITEXT()


def DTEXT():
    if PSSDRUG_B[PSSB]["9"]:
        PSF = 1
        for TD in PSSDRUG_B[PSSB]["9"]:
            POINT = PSSDRUG_B[PSSB]["9"][TD]
            PSSDAY = PS_B[51.7][POINT][0][2]
            if not PSSDAY or PSSDAY >= DT:
                if PSF == 1:
                    PDTEXT1()
                    PSF = 0
                if PSSPGLNG - PSSPRT < 5:
                    TITLE()
                    if PSSOUT:
                        return
                PDTEXT()


def PDTEXT1():
    print("\nDispense Drug text:")
    if PSSPGLNG - PSSPRT >= 5:
        TITLE()
        if PSSOUT:
            return


def PDTEXT():
    TXNFO = PS_B[51.7][POINT][2][1]
    if len(TXNFO) > 70:
        TXNFO = TXNFO[:70] + "..."
    print(f"     {TXNFO}")
    if PSSPGLNG - PSSPRT >= 5:
        TITLE()
        if PSSOUT:
            return


def NOTHG():
    ZERO = PSDRUG_B[PSSB]["0"]
    LOC = ZERO[9]
    VISN = ZERO[11]
    DEA = ZERO[3]
    if LOC == 1:
        LOC = "N"
    if VISN == 1:
        VISN = "N"
    if "R" in DEA:
        DEA = "R"
    else:
        DEA = ""
    APU = PSDRUG_B[PSSB][2][3]
    MCLS()
    DTX()
    POITXT()
    REPRT()


def POI():
    PT1 = PSDRUG_B[PSSB][2]
    if PT1:
        DFPTR = PSDRUG_B[50.7][PT1][0][2]
        DF = PSDRUG_B[50.606][DFPTR][0]
        OINM = PSDRUG_B[50.7][PT1][0] + " " + DF
        OIFS = PSDRUG_B[50.7][PT1][12]
        if OIFS == 1:
            OIFS = "(N/F)"
        OI()


def POITXT():
    OITM = PSDRUG_B[PSSB][2]
    if OITM and len(PSDRUG_B[PSSB][2]) > 1:
        TXT = "I"


def OI():
    print(f"Orderable Item: {OINM}   {OIFS}")
    if PSSPGLNG - PSSPRT >= 5:
        TITLE()
        if PSSOUT:
            return


def POOI():
    print("\nOrderable Item text:")
    if PSSPGLNG - PSSPRT >= 5:
        TITLE()
        if PSSOUT:
            return


def PPOITXT():
    INFO = PS_B[51.7][POINTR][2][1]
    if len(INFO) > 70:
        INFO = INFO[:70] + "..."
    print(f"     {INFO}")
    if PSSPGLNG - PSSPRT >= 5:
        TITLE()
        if PSSOUT:
            return


def MCLS():
    if PSSDRUG_B[PSSB]["ND"]:
        PSSMC = PSSDRUG_B[PSSB]["ND"]
        if not PSSMC[1]:
            NAT = PSSMC[11]


def REPRT():
    if PSSPGLNG - PSSPRT >= 5:
        TITLE()
        if PSSOUT:
            return
    print(f"{PSSLCL}        {LOC}     {VISN}     {NAT}        {DEA}       {APU}     {TXT}")
    PSSPRT = 1


def ITEXT():
    PT1 = PSDRUG_B[PSSB][2]
    if PT1 and PSDRUG_B[50.7][PT1][1]:
        PSF = 1
        for TDD in PSDRUG_B[50.7][PT1][1]:
            POINTR = PSDRUG_B[50.7][PT1][1][TDD]
            TXT = "I"
            PSSDAY1 = PS_B[51.7][POINTR][0][2]
            if not PSSDAY1 or PSSDAY1 >= DT:
                if PSF == 1:
                    POOI()
                    PSF = 0
                if PSSPGLNG - PSSPRT < 5:
                    TITLE()
                    if PSSOUT:
                        return
                PPOITXT()


def TITLE():
    if PSSDV == "C" and PSSPGCT != 1:
        input("Press Enter to continue...")
        if not Y:
            PSSOUT = 1
            return

    print("\n", "Formulary Information Report for Drugs with Leading Numerics" if PSSSRT == "N" else
          "Formulary Information Report for All Drugs" if PSSSRT == "A" else
          f"Formulary Information Report for Drugs from {PSSBEG} through {PSSEND}", "\n")
    print("Date printed: ", DT, "\tPage: ", PSSPGCT)
    print("\nGeneric Name", " " * 37, "Local", "Visn", "National", "Restriction", "Appl", "Drug")
    print(" " * 43, "Pkg", "Text", "Use")
    print("-" * 132)
    PSSPGCT += 1


PSSNFI()