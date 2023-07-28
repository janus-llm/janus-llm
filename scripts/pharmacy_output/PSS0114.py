# PSS0114 ;BIR/JLC-UPDATE ORDERABLE ITEMS WITH DEFAULT MED ROUTES ;08/28/2006
# ;;1.0;PHARMACY DATA MANAGEMENT;**114**;9/30/97;Build 2
#
#
A = None
B = None
C = None
DF = None
Y = None
MRP = None
MR = None
OUT = None
IEN = None
OK = None
X = None

def EN():
    global X, DF
    DIC = "^PS(50.606,"
    DIC(0) = "AEMQ"
    DIC("A") = "Select DOSAGE FORM: "
    result = input(DIC("A"))
    X = result.strip()
    if X == "" or X == "^":
        return
    else:
        if Y < 0:
            EN()
        else:
            EN1()

def EN1():
    global OUT, IEN, MRP, MR
    DIC = "^PS(51.2,"
    DIC(0) = "AEMQ"
    DIC("A") = "Select MEDICATION ROUTE: "
    result = input(DIC("A"))
    X = result.strip()
    if X == "" or X == "^":
        return
    else:
        if Y < 0:
            EN1()
        else:
            print()
            MRP = Y
            MR = Y[1]
            OUT = 0
            while IEN:
                A = IEN[0]
                if A[5]:
                    B = A[1]
                    if B != "":
                        C = "^PS(50.606,B,0)"
                    if C != DF:
                        print(IEN, A[0], "ok to change? ", end="")
                        OK = input()
                        print("  ")
                        if OK == "^":
                            OUT = 1
                            break
                        else:
                            if OK != "Y":
                                continue
                            else:
                                IEN[0][5] = MRP
                                break
                else:
                    return

EN()

def EXIT():
    return