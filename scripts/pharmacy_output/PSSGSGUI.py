def PSGENCHK(X):
    if len(X) > 4 or len(X) < 2 or not X.isalnum():
        return False
    return True

def PSGEN(X, PSSGUIPK=None):
    if PSSGUIPK == "O":
        if X != "":
            if "\"" in X or ord(X[0]) == 45 or X.isprintable() or len(X.split()) > 2 or len(X) > 70 or len(X) < 1 or "P RN" in X or "PR N" in X or X[0] == " ":
                return
            X = X.upper()
    if "PRN" in X:
        X = "PRN"
    X = X.strip()
    if X.islower():
        X = X.upper()
    if X == "Q0":
        return
    PSGS0XT = ""
    PSGS0Y = ""
    if X == "PRN" or X == "ON CALL" or X == "ONCALL" or X == "ON-CALL" or X in ["ONCE", "STAT", "ONE TIME", "ONETIME", "1TIME", "1 TIME", "1-TIME", "ONE-TIME"] or X in ["NOW", "ONCE", "STAT", "ONE TIME", "ONETIME", "1TIME", "1 TIME", "1-TIME", "ONE-TIME"]:
        return
    if "PRN" in X:
        OK = False
        for i in range(1, 3):
            A = X.replace(" ", "").split("PRN")[i-1]
            if A != "":
                X = A
                if A in ["PRN", "PR N"] or A in ["PRN", "PR N"] or (A.isdigit() and len(A) in [2, 4]) or (A.isdigit() and len(A) in [2, 4]):
                    OK = True
                    break
        if OK:
            return
        else:
            DW(X)
            if X:
                return
    X0 = X
    if X and "X" not in X and (PSGENCHK(X.split("@")[0]) or (X.isdigit() and len(X) in [2, 4])):
        ENCHK(X)
        if X:
            Y = X
    if X in ["PRN", "ON CALL", "ONCALL", "ON-CALL"] or X in ["PRN", "ON CALL", "ONCALL", "ON-CALL"] or X == "PRN" or "^PS(51.1" in globals():
        DIC(X)
        if XT:
            return
    if (X.isdigit() and len(X) in [2, 4]):
        ENCHK(X)
        if X:
            Y = X
        return
    TMPX = X
    DW(X)
    if X:
        PSGSCH = X
        if "^PS(51.1" in globals():
            PSGS0XT = "D"
        Y = X.split("@")[1]
        return
    TMPSCHX = X
    if X:
        X = X.split("@")[1]
        if X:
            if "PSJ" in globals() and X in "^PS(51.1":
                TMPIEN = 0
                for i in range(len("^PS(51.1")):
                    if "^PS(51.1"[i] == X:
                        TMPIEN = i
                        break
                TMPAT = globals()["^PS(51.1"][TMPIEN]
                if TMPAT:
                    if not DOW(X.split("@")[0]):
                        TMPAT = None
                    WARD = globals()["^DPT"][DFN-1][0]
                    if WARD:
                        DIC("^DIC(42")
                        WARD = Y
                        if WARD:
                            WARD = globals()["^PS(59.6"][WARDS.index(WARD)]
                    if TMPAT:
                        PSGS0Y = TMPAT
                        X = Y
                        PSGS0XT = "D"
    X = XT
    PSGS0XT = XT
    PSGS0Y = Y
    return

def ENCHK(X):
    if len(X.split("-")[0]) > 4 or len(X) > 119 or len(X) < 2 or int(X) <= 0 or not X.isalnum():
        X = None
    else:
        X1 = int(X.split("-")[0])
        X = X.split("-")[1]
        X2 = 0
        if X[0] == "X":
            X2 = 1
            X = X[1:]
        XT = -1
        if "'" in X:
            XT = 1
        elif X in ["D", "AM", "PM", "HS"] or (X == "H" and "TH" not in X) or (X in ["AC", "PC"]) or X == "W" or X == "M":
            XT = 1440
        if XT < 0 or Y <= 0:
            X = None
        else:
            X = X0
            if X:
                X2 = XT // X1 if X2 else X2
                if not X2:
                    if "QO" in X:
                        XT = XT * 2
                    XT = XT * X1
    return

def DIC():
    if "^PS(51.1" in globals():
        DIC = globals()["^PS(51.1"]
        if DIC:
            if "C" in DIC[4]:
                XT = DIC[2]
            else:
                XT = DIC[4]
            X = DIC[0]
            Y = DIC[0]
            if Y == "":
                Y = DIC[2]
            X = Y[0]
            X0 = Y
            if Y:
                Y = DIC[2] if globals().get("PSJPWD") else DIC[0]
                if globals().get("PSJPWD"):
                    if DIC[1][globals()["PSJPWD"]] != "":
                        Y = DIC[1][globals()["PSJPWD"]]
                if Y == "":
                    Y = DIC[2]
            X = Y[0]
    return

def DW():
    SWD = "SUNDAYS^MONDAYS^TUESDAYS^WEDNESDAYS^THURSDAYS^FRIDAYS^SATURDAYS"
    SDW = X
    X = X.split("@")[1]
    if X:
        ENCHK(X)
        if not X:
            return
    X = SDW.split("@")[0]
    X1 = "-"
    if X:
        for i in range(len(X)):
            if X[i].isprintable() and not X[i].isalnum():
                X1 = X[i]
                break
        for q in range(1, len(SWD.split("^"))+1):
            Y = SWD.split("^")[q-1]
            if Y.split(X1)[0] == "":
                SWD = SWD.split(Y)[1]
                if SWD != "":
                    SWD = SWD[1:]
                break
    else:
        X = SDW
    return

def DOW(Z):
    if len(Z) < 2:
        return False
    for q in range(1, len(SWD.split("^"))+1):
        Y = SWD.split("^")[q-1]
        if Z not in Y:
            SWD = SWD.split(Y)[0] + SWD.split(Y)[1]
        else:
            SWD = SWD.split(Y)[1]
            if SWD:
                SWD = SWD[1:]
            else:
                SWD = None
            break
    return SWD

def PSGENOS(X):
    PSGST = globals()["^PS(55"][DA1-1][4]
    return PSGEN(X)

def PSGEN5(X):
    PSGST = globals()["^PS(55"][DA1-1][1][DA-1][4]
    return PSGEN(X)

def PSGSGENGUI(X, PSSGUIPK):
    X = X.split("\"\"\"PSSGSGUI ;BIR/CML3-SCHEDULE PROCESSOR FOR GUI ONLY ;05/29/98\n ;;1.0;PHARMACY DATA MANAGEMENT;**12,27,38,44,56,59,94,119**;9/30/97;Build 9\n ;\n ; Reference to ^PS(53.1 supported by DBIA #2140\n ; Reference to ^PSIVUTL supported by DBIA #4580\n ; Reference to ^PS(59.6 supported by DBIA #2110\n ; Reference to ^DIC(42 is supported by DBIA# 10039\n ;\n ;ENA ; entry point for train option\n ;N X S X=\"PSGSETU\" X ^%ZOSF(\"TEST\") I  D ENCV^PSGSETU Q:$D(XQUIT)\n ;F  S (PSGS0Y,PSGS0XT)=\"\" R !!,\"Select STANDARD SCHEDULE: \",X:DTIME W:'$T $C(7) S:'$T X=\"^\" Q:\"^\"[X  D:X?1.\"?\" ENQ^PSSGSH I X'?1.\"?\" D EN W:$D(X)[0 $C(7),\"  ??\" I $D(X)#2,'PSGS0Y,PSGS0XT W \"  Every \",PSGS0XT,\" minutes\"\n ;K DIC,DIE,PSGS0XT,PSGS0Y,Q,X,Y,PSGDT Q\n Q\n ;\n ;EN3 ;\n ;S PSGST=$P($G(^PS(53.1,DA,0)),\"^\",7) G EN\n ;\n ;EN5 ;\n ;S PSGST=$P($G(^PS(55,DA(1),5,DA,0)),\"^\",7)\n ;\n ;EN(X,PSSGUIPK) ; validate\n ;I X[\"\"\"\"\"!(\"\"\"\"\".A(X)=45)!(X?.E1C.E)!($L(X,\"\"\"\" \")>2)!($L(X)>70)!($L(X)<1)!(X[\"\"\"\"P RN\"\"\")!(X[\"\"\"\"PR N\"\"\")!(\"\"\"\"\".E(X,1)=\"\"\"\"\") K X Q\n I $G(PSSGUIPK)=\"\"\"\"O\"\"\"\" D  Q\n .Q:$G(X)=\"\"\"\"
    PSGGEN(X, PSSGUIPK)
    X = X.split("\"\"\"")
    if len(X) > 1:
        return X[1]
    else:
        return ''

X = ""
PSSGUIPK = ""
PSGEN(X, PSSGUIPK)