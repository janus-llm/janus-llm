def ADTM():
    PSSHLP = []
    PSSHLP.append("THE TIMES MUST BE TWO (2) OR FOUR (4) DIGITS, SEPARATED WITH")
    PSSHLP.append("DASHES ('-'), AND BE IN ASCENDING ORDER. (IE. 01-05-13)")
    WRITE(PSSHLP)

def SPCIN():
    PSSHLP = []
    PSSHLP.append("IF ABBREVIATIONS ARE USED, THE TOTAL LENGTH OF THE EXPANDED")
    PSSHLP.append("INSTRUCTIONS ALSO MAY NOT EXCEED 180 CHARACTERS.")
    WRITE(PSSHLP)

def SCHTP():
    PSSHLP = []
    PSSHLP.append("CHOOSE FROM:")
    PSSHLP.append("C - CONTINUOUS")
    PSSHLP.append("O - ONE-TIME")
    PSSHLP.append("OC - ON CALL")
    PSSHLP.append("P - PRN")
    PSSHLP.append("R - FILL ON REQUEST")
    WRITE(PSSHLP)

def CHKSI(X):
    if not X or not X.isprintable() or X.count('^') > 0 or len(X) > 180:
        return None
    Y = ''
    for Y_1 in X.split(' '):
        if Y_1:
            Y_2 = Y_1.strip()
            if len(Y) + len(Y_2) > 180:
                return None
            Y += Y_2 + ' '
    return Y.strip()

def EN2():
    PSGDLS = []
    ND2 = PS[55][DA[1]][5][DA][2]
    if not (ND2[5] or ND2[6]):
        return
    PSGDLS.extend(PSGDLS)
    if PSJSYSW0[5] == 2:
        PSJSYSW0[5] = 1
        if 'PSGNE3' in globals():
            ST = PSGNE3.ENSD(ST, TS, ST, "")
        PSJSYSW0[5] = 2

def DONE():
    PSGDLS = []
    ND2 = PS[55][DA[1]][5][DA][2]
    if not (ND2[5] or ND2[6]):
        return
    PSGDLS.extend(PSGDLS)
    if PSJSYSW0[5] == 2:
        PSJSYSW0[5] = 1
        if 'PSGNE3' in globals():
            ST = PSGNE3.ENSD(ST, TS, ST, "")
        PSJSYSW0[5] = 2

def ENDL():
    PSIVMIN = P[15] * X
    PSIVSD = +P[2]
    if PSIVMIN < 0:
        print(" --- There is something wrong with this order !!")
        print("     Call inpatient supervisor .....")
        return
    if P[4] == "P" or P[5] or P[23] == "P":
        if PSIVMIN == 0 and P[9].split(' ')[0] not in ["NOW", "STAT", "ONCE"]:
            DLP()
    X = Y
    X = Y

def ENI():
    if len(X) < 1 or len(X) > 30 or '"' in X or ord(X[0]) == 45:
        return None
    if not X or not P[4]:
        return None
    if P[4] == "P" or P[5] or P[23] == "P":
        if not X:
            return None
        X = str(X) + " ml/hr"
        SPSOL = SPSOL[0]
        if not SPSOL:
            print("  You must define at least one solution !!")
            return None
        if not X.isdigit():
            X = str(SPSOL // int(X) * 60 + (SPSOL % int(X) / int(X) * 60 + 0.5) // 1)
        else:
            X = str(SPSOL // int(X) * 60)
        SPSOL = None
    else:
        SPSOL = int(X.split('@')[1])
        if X.split('@')[0].isdigit():
            X = str(int(X.split('@')[0])) + " ml/hr"
        else:
            X = X.split('@')[0]
            SPSOL = None

def AASCRN(PSSREC):
    if "^APSPQA(32.3," + str(int("PSSREC")) + ",0)" == "NO ALLERGY ASSESSMENT":
        if "^APSPQA(32.5," + str(int("PSSREC")) + ",0)" == "UNABLE TO ASSESS":
            return True
        elif "^APSPQA(32.5," + str(int("PSSREC")) + ",0)" == "OTHER":
            return True
        else:
            return False
    else:
        if "^APSPQA(32.5," + str(int("PSSREC")) + ",0)" == "UNABLE TO ASSESS":
            return False
        else:
            return True