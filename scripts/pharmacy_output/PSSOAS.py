def OASDIC():
    # screening for the OLD SCHEDULE NAME(S) multiple
    PSSDA = DA
    PSSX = X
    PSSY = Y
    PSSFCHK = ""
    PSSFCHK2 = ""
    PSSFCHK3 = ""
    PSSFCHK4 = ""
    PSSFL = 0
    PSSFL2 = 0
    PSSFL3 = 0
    PSSODA = ""
    PSSOX = ""
    PSSEX = ""
    PSSAIEN = ""
    DA = PSSDA
    MSG = ""

    while True:
        PSSRN = OASLE(DA)
        DA(1) = DA
        if not DA(1):
            break
        DIC = "^PS(51.1," + DA(1) + ",5,"
        DIC(0) = "AEMLTVZ"
        DIC("A") = "Select OLD SCHEDULE NAME(S): " + PSSRN
        result = DIC
        if result <= 0:
            break
        if X.find('"') >= 0:
            X = Y.split("^")[1]
        X = X.upper()
        PSSFCHK = next((item for item in ^PS(51.1, "B") if item == X), None)
        if PSSFCHK and Y.split("^")[3] == 1:
            PSSFL = 0
            X = ""
            DIE = DIC
            DA = Y
            DR = ".01////@"
            result = DIE
            DA = PSSDA
            MSG = ""
            MSG.append("")
            MSG.append("      An OLD SCHEDULE NAME(S) entry cannot be the same as an existing NAME")
            MSG.append("      field.")
            MSG.append("")
            result = EN^DDIOL(MSG, "", "!")
        PSSODA = Y
        PSSOX = Y.split("^")[2]
        DIR(0) = "FAO^2:20"
        DIR("A") = "OLD SCHEDULE NAME(S): " + PSSOX + "// "
        result = DIR
        if X == "^":
            DA = PSSDA
            X = ""
            result = DIR
            break
        X = X.upper()
        if X == PSSOX:
            DA = PSSDA
            X = ""
            result = DIR
            break
        PSSFCHK2 = next((item for item in ^PS(51.1, "B") if item == X), None)
        if PSSFCHK2:
            PSSFL2 = 0
            X = ""
            result = DIR
            MSG = ""
            MSG.append("")
            MSG.append("      An OLD SCHEDULE NAME(S) entry cannot be the same as an existing NAME")
            MSG.append("      field.")
            MSG.append("")
            result = EN^DDIOL(MSG, "", "!")
        PSSFCHK3 = next((item for item in ^PS(51.1, DA, 5) if item == X), None)
        if PSSFCHK3 and X != "":
            PSSFL3 = 0
            X = ""
            result = DIR
            MSG = ""
            MSG.append("")
            MSG.append("      Duplicate exists in Old Schedule Name multiple for this entry.")
            MSG.append("")
            result = EN^DDIOL(MSG, "", "!")
        if PSSFL3 == 1:
            PSSFL3 = 0
        PSSFCHK4 = next((item for item in ^PS(51.1, "D") if item == X), None)
        if PSSFCHK4:
            PSSFL4 = 0
            PSSAIEN = next((item for item in ^PS(51.1, "D", PSSFCHK4) if item != ""), None)
        if PSSFL4:
            PSSFL4 = 0
            X = ""
            result = DIR
            MSG = ""
            MSG.append("")
            MSG.append("      Duplicate exists in Old Schedule Name multiple for the entry")
            MSG.append("      " + ^PS(51.1, PSSAIEN, 0).split("^")[1] + " (" + PSSAIEN + ") in the file.")
            MSG.append("")
            result = EN^DDIOL(MSG, "", "!")
        if X != "" and X != "@":
            PSSEX = X
            DIE = DIC
            DA = PSSODA
            DR = ".01///^S X=PSSEX"
            result = DIE
            DA = PSSDA
            DIR(0) = "YAO"
            DIR("A") = "SURE YOU WANT TO DELETE? "
            result = DIR
            if Y == 1:
                DIE = DIC
                DA = PSSODA
                DR = ".01///@"
                result = DIE
                DA = PSSDA
                DIR("A") = ""
                result = DIR
            if Y == 0:
                DA = PSSDA
                DIR("A") = ""
                result = DIR
    if X == "^":
        DIC = ""
        DIE = ""
        DR = ""
        DA = ""
        return
    if X.find("^") >= 0:
        EN^DDIOL("   No Jumping allowed??", "", "!")
        X = ""
        DIC = ""
        DIE = ""
        DR = ""
        DA = ""
        return
    X = PSSX
    Y = PSSY
    DIC = ""
    DIE = ""
    DR = ""
    DA = ""
    PSSDA = ""
    PSSX = ""
    PSSY = ""
    return


def OASLE(PSSDA):
    # retrieve the last entry from the OLD SCHEDULE NAME (#13) field multiple
    PSSLE = ""
    if ^PS(51.1, PSSDA, 5) != "":
        PSSLR = 999999
        while True:
            PSSLR = PSSLR - 1
            if ^PS(51.1, PSSDA, 5, PSSLR) != "":
                PSSLE = ^PS(51.1, PSSDA, 5, PSSLR).split("^")[0] + "// "
            if PSSLR == "":
                break
    return PSSLE