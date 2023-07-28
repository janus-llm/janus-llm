# PSSGMI ;BIR/CML3-MISCELLANEOUS INFORMATION ; 08/30/96 10:17
# ;;1.0;PHARMACY DATA MANAGEMENT;;9/30/97

def ENPDN(X): # orderable item name
    # X - pointer to Orderable Item (50.7) file
    Y = ''
    if X == '':
        return "NOT FOUND"
    if X:
        Y = ^PS(50.7,X,0)
        Y = Y.split("^")[0]
        if Y == '':
            Y = X + ";PS(50.7,"
    return Y

def ENDDN(X): # dispense drug name
    # X - pointer to Drug (50) file
    Y = ''
    if X == '':
        return "NOT FOUND"
    if X:
        Y = ^PSDRUG(X,0)
        Y = Y.split("^")[0]
        if Y == '':
            Y = X + ";PSDRUG("
    return Y

def ENMRN(X): # med route name
    # X - pointer to Medication Route (51.2) file
    Y = ''
    if X == '':
        return "NOT FOUND"
    if X:
        Y = ^PS(51.2,X,0)
        Y = Y.split("^")[2] if Y.split("^")[2] else Y.split("^")[0]
        if Y == '':
            Y = X + ";PS(51.2,"
    return Y

def ENMRA(X): # Med Route Abbrev.
    return ^PS(51.2,X,0).split("^")[2]

def ENNPN(X): # new person name
    # X - pointer to New Person (200) file
    Y = ''
    if X == '':
        return "NOT FOUND"
    if X:
        Y = ^VA(200,X,0)
        Y = Y.split("^")[0]
        if Y == '':
            Y = X + ";VA(200,"
    return Y

def ENSTN(X): # schedule type name
    # X - Schedule Type code
    if X == '':
        return "NOT FOUND"
    X = "CONTINUOUS" if X == "C" else X
    X = "ONE TIME" if X == "O" else X
    X = "ON CALL" if X == "OC" else X
    X = "PRN" if X == "P" else X
    X = "FILL on REQUEST" if X == "R" else X
    return X

def ENDDTC(Y): # FM internal date/time to user readable, Inpatient style
    # Y - date in FileMan internal format
    if Y:
        Y = Y + "." + str(Y not in ".") + "0000"
        return Y[3:5] + "/" + Y[5:7] + "/" + Y[1:3] + "  " + Y[9:11] + ":" + Y[11:13]
    return "********"

def ENDDTC1(Y): # FM internal date/time to user readable, only 1 space before time.
    # Y - date in FileMan internal format
    if Y:
        Y = Y + "." + str(Y not in ".") + "0000"
        return Y[3:5] + "/" + Y[5:7] + "/" + Y[1:3] + " " + Y[9:11] + ":" + Y[11:13]
    return "********"

def ENDD(Y): # FM internal date/time to user readable - stolen from ^DD("DD")
    # Y - date in FileMan internal format
    if Y:
        Y = str(Y)
        Y = Y[4:6] + "/" + Y[6:8] + "/" + Y[2:4] + " " + Y[9:11] + ":" + Y[11:13] if Y[4:5] else ""
        Y += "@" + Y[9:11] + ":" + Y[11:13] if Y[13:14] else ""
        return Y
    return Y

def ENPDS(Y, CODES): # look-up screen for primary drugs
    # CODES - set of codes separated by commas
    # Y - pointer to the Primary Drug (50.3) file
    ND = ""
    X = ""
    if 0:
        ND = ^PS(50.7,+Y,0)
    return 1 if ND.split("^")[3] > DT else 0
    for Z in range(1, len(CODES.split(",")) + 1):
        X = CODES.split(",")[Z - 1]
        if X != "":
            if not $D(^PS(50.3,Y,1,"AFI",X)):
                ND = ^PS(50.3,Y,1,"AFI",X)
                if ND:
                    if not ND.split("^")[1] or ND.split("^")[1] > DT:
                        return 1
    return 0

def ENLU(X): # convert lower case to upper case
    return X.upper()

def ENUL(X): # convert upper case to lower case
    return X.lower()