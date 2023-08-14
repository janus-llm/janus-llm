def DEA():
    PSSHLP = []
    PSSHLP.append("THE SPECIAL HANDLING CODE IS A 2 TO 6 POSTION FIELD.  IF APPLICABLE,")
    PSSHLP.append("A SCHEDULE CODE MUST APPEAR IN THE FIRST POSITION.  FOR EXAMPLE,")
    PSSHLP.append("A SCHEDULE 3 NARCOTIC WILL BE CODED '3A', A SCHEDULE 3 NON-NARCOTIC WILL BE")
    PSSHLP.append("CODED '3C' AND A SCHEDULE 2 DEPRESSANT WILL BE CODED '2L'.")
    PSSHLP.append("THE CODES ARE:")
    WRITE(PSSHLP)
    for II in range(1, len(D)+1):
        PSSHLP[II-1] = D[II]
    PSSHLP[0,"F"] = "!!"
    WRITE(PSSHLP)
    PKIND()
    WRITE(PSSHLP)

def WRITE(lines):
    for line in lines:
        print(line)

def PKIND():
    PSSK = int(PSDRUG[DA]["ND"][2])
    PSSK = int(DIq(50.68,PSSK,19,"I"))
    if PSSK:
        PSSK = CSDEA(PSSK)
        if len(PSSK) == 1 and PSDRUG[DA][0][3:].find(PSSK) != -1:
            return
        if PSDRUG[DA][0][3:].find(PSSK[0]) != -1 and PSDRUG[DA][0][3:].find(PSSK[1]) != -1:
            return
        print("The CS Federal Schedule associated with this drug in the VA Product file")
        print("represents a DEA, Special Handling code of", PSSK)

def CSDEA(CS):
    if not CS:
        return ""
    if CS == "2n" or CS == "3n":
        return CS+"C"
    if (CS == 2 or CS == 3) and CS.find("C") == -1:
        return CS+"A"
    return CS

def SIG():
    if X[0] == " ":
        print("Leading spaces are not allowed in the SIG! ", end="")
        print("$C(7),!")
        X = None
        return
    SIG = ""
    if len(X) < 1:
        return
    for Z0 in range(1, len(X.split(" "))+1):
        Z1 = X.split(" ")[Z0-1]
        if len(Z1) > 32:
            print("MAX OF 32 CHARACTERS ALLOWED BETWEEN SPACES.","","$C(7),!?5")
            X = None
            return
        if Z1 and Z1 in PS[51]:
            Y = PS[51][Z1]
            if Y and Y[3] > 1:
                Z1 = Y[1]
                if Y[9]:
                    Y = X.split(" ")[Z0-2][-1]
                    if Y > 1:
                        Z1 = Y[9]
        SIG += " "+Z1
    Z1 = None

def DRUGW():
    for Z0 in range(1, len(X.split(","))+1):
        Z1 = X.split(",")[Z0-1]
        if Z1 and Z1 in PS[54]:
            print(PS[54][Z1][0], end="")
            print("",",?35")
        else:
            print("NO SUCH WARNING LABEL","","?35")
            X = None
            return

def P():
    PSSHLP = []
    PSSHLP.append("A TWO OR THREE POSITION CODE IDENTIFIES THE SOURCE OF SUPPLY AND WHETHER")
    PSSHLP.append("THE DRUG IS STOCKED BY THE STATION SUPPLY DIVISION.  THE FIRST")
    PSSHLP.append("POSITION OF THE CODE IDENTIFIES SOURCE OF SUPPLY.  THE CODES ARE:")
    WRITE(PSSHLP)
    for II in range(0, 11):
        PSSHLP[II] = S[II]
        PSSHLP[II,"F"] = "?10"
    PSSHLP[0,"F"] = "!!?10"
    WRITE(PSSHLP)
    PSSHLP[0] = "THE SECOND POSITION OF THE CODE INDICATES WHETHER THE ITEM IS"
    PSSHLP[1] = "OR IS NOT AVAILABLE FROM SUPPLY WAREHOUSE STOCK.  THE CODES ARE:"
    PSSHLP[2] = "P          POSTED STOCK"
    PSSHLP[2,"F"] = "!!?10"
    PSSHLP[3] = "U          UNPOSTED"
    PSSHLP[3,"F"] = "?10"
    PSSHLP[4] = "M          BULK COMPOUND"
    PSSHLP[4,"F"] = "?10"
    PSSHLP[5] = "*  USE CODE 0 ONLY WITH SECOND POSITION M."
    WRITE(PSSHLP)

def S():
    PSSHLP = []
    PSSHLP.append("!!")
    for i in range(1, 11):
        PSSHLP.append(S[i])
    WRITE(PSSHLP)

def CLOZ():
    PSSHLP = []
    PSSHLP.append("To delete this field use the Unmark Clozapine Drug option in the")
    PSSHLP.append("Clozapine Pharmacy Manager menu.")
    WRITE(PSSHLP)

def NONF():
    if not DA(1):
        print(" (This non-formulary item is "+PSDRUG[DA]+".")

def STRTH():
    STR = " "+X.split(" ")[1]
    PSSHLP = []
    PSSHLP.append(STR)
    WRITE(PSSHLP)
    STR = None

def PSYS1():
    print(("""("From" ward is ""+(!(PS[59.7][D0][22][D1])) ? "UNKNOWN" : !(^DIC(42,+(^(0)),0)) ? "UNKNOWN" : ^(0)),"","!?3"))

def PSYS2():
    print(("""("From" service is ""+(!(PS[59.7][D0][23][D1])) ? "UNKNOWN" : $P(^(0),"^"))"))

def NCINIT():
    PSSNQM = []
    PSSNQM2 = None
    PSSNQM3 = None
    global PSSONDU
    global PSSONQM

def NCINIT1():
    if not PSDRUG[DA]["EPH"][2]:
        PSDRUG[DA]["EPH"][2] = "EA"
        PSDRUG[DA]["EPH"][3] = 1
        PSSHLP = []
        PSSHLP.append("  Note:     Defaulting the NCPDP DISPENSE UNIT to EACH and the")
        PSSHLP.append("            NCPDP QUANTITY MULTIPLIER to 1 (one).")
        PSSHLP[0,"F"] = "!!"
        WRITE(PSSHLP)
        PSSHLP[1,"F"] = "!"
        WRITE(PSSHLP)
    PSSONDU = PSDRUG[DA]["EPH"][2]
    PSSONQM = PSDRUG[DA]["EPH"][3]

def NCPDPDU():
    if not X:
        X = "EA"
    NCINIT1() if not PSSONDU
    if PSSONDU != X and PSSONQM != 1:
        PSSHLP = []
        PSSHLP.append("Defaulting the NCPDP QUANTITY MULTIPLIER to 1 (one).")
        PSSHLP[0,"F"] = "!!"
        WRITE(PSSHLP)
        PSDRUG[DA]["EPH"][3] = 1
        PSSONDU = PSDRUG[DA]["EPH"][2]
        PSSONQM = PSDRUG[DA]["EPH"][3]

def NCPDPQM():
    PSSNQM = 0
    PSSNQM2 = ""
    if X < .00001:
        X = 1
    if X == "":
        X = 1
    if int(X) != 1:
        NCPDPWRN()
    while PSSNQM:
        ZXX = input("Ok to continue? (Y/N) ")
        ZXX = ZXX.upper()
        if ZXX == "^":
            X = 1
            print("Warning:  Defaulting NCPDP QUANTITY MULTIPLIER to 1 (one).", end="")
            print()
            break
        if ZXX != "Y" and ZXX != "N":
            print("Y or N must be entered.")
            continue
        if ZXX != "Y" and ZXX != "y":
            PSSNQM = 1
            PSSNQM2 = X
            X = None

def NCPDPWRN():
    PSSHLP = []
    PSSHLP.append("WARNING:    For most drug products, the value for this field should be 1 (one).")
    PSSHLP.append("            Answering NO for the following prompt will display more information")
    PSSHLP.append("            on how this field is used.")
    PSSHLP[1,"F"] = "!!"
    WRITE(PSSHLP)
    PSSHLP[3,"F"] = "!"
    WRITE(PSSHLP)

def MXDAYSUP():
    if X < 1 or X > 365:
        print("Type a number between 1 and 365, 0 decimal digits.","","!!")
        X = None
        print()
    VAPRDIEN = int(DIq(50,DA,22,"I"))
    if VAPRDIEN:
        NDFMAXDS = int(DIq(50.68,VAPRDIEN,32))
        if NDFMAXDS and NDFMAXDS < X:
            print("Cannot be greater than NDF Maximum Days Supply: "+NDFMAXDS,"","!!")
            X = None
            print()
    DEASPHLG = DIq(50,DA,3)
    if "2" in DEASPHLG and X > 30:
        print("Schedule 2 controlled substances have a maximum days supply limit of 30 days","","!!")
        X = None
        print()
    if ("3" in DEASPHLG or "4" in DEASPHLG or "5" in DEASPHLG) and X > 90:
        print("Schedule 3-5 controlled substances have a maximum days supply limit of 90 days","","!!")
        X = None
        print()
    if ("CLOZ1" in PSDRUG[DA]) and X:
        print("Maximum Days Supply for this drug is controlled by the Clozapine functionality","","!!")
        X = None
        print()
    if X and X < MXDAYSUP(DA):
        print("Note: Decreasing the MAXIMUM DAYS SUPPLY field will only affect new","","!")
        print("      prescriptions, including renewals and copies. Orders that are pending","","!")
        print("      or unreleased when the MAXIMUM DAYS SUPPLY field is decreased are not","","!")
        print("      affected by the decrease, so prescriptions with a DAYS SUPPLY above the","","!")
        print("      new MAXIMUM DAYS SUPPLY may need to be edited manually before they are","","!")
        print("      finished or released.","","!")
        print()
        input("Press Return to continue")

def IVSOLVOL():
    if X.find("\"") != -1 or ord(X[0]) == 45 or not X.isdigit() or int(X) > 9999 or float(X) < 0.01:
        X = None
        return
    if DIq(52.7,DA,17,"I"):
        OI = int(DIq(52.7,DA,9,"I"))
        if CKDUPSOL(OI,DA,float(X),1):
            X = None
            return
    X += " ML"
    print(" ML","","?0")

def UIVFOE():
    if X:
        OI = int(DIq(52.7,DA,9,"I"))
        if CKDUPSOL(OI,DA,float(DIq(52.7,DA,2)),1):
            X = None

def CKDUPSOL(OI,IVSOL,IVVOL,DSPMSG):
    DUPSOL = 0
    OTHSOL = 0
    if not IVSOL:
        return 0
    if DIq(52.7,IVSOL,8,"I") and DIq(52.7,IVSOL,8,"I") <= datetime.datetime.now().date():
        return 0
    DRUG = int(DIq(52.7,IVSOL,1,"I"))
    if OI:
        while OTHSOL:
            if DUPVOL(IVSOL,OTHSOL):
                DUPSOL = OTHSOL
            OTHSOL += 1
    else:
        while OTHSOL:
            if DUPVOL(IVSOL,OTHSOL):
                DUPSOL = OTHSOL
            OTHSOL += 1
    if DSPMSG and DUPSOL:
        print()
        print("The following IV Solution with the same volume is already linked to")
        if OI:
            print("the Orderable Item ",DIq(50.7,OI,.01))
        else:
            print("this dispense drug.")
        print()
        print("Dispense Drug: ",DIq(52.7,DUPSOL,1))
        print("  IV Solution: ",DIq(52.7,DUPSOL,.01))
        print()
        print("Only one Active IV Solution with a specific volume can be linked to an")
        print("Orderable Item or Dispense Drug when the IV Solution is marked to be used")
        print("in the CPRS IV Fluid Order Entry.")
        print("\a")
    return DUPSOL

def DUPVOL(IVSOL1,IVSOL2):
    if IVSOL1 == IVSOL2:
        return 0
    if not DIq(52.7,IVSOL2,17,"I"):
        return 0
    if DIq(52.7,IVSOL2,8,"I") and DIq(52.7,IVSOL2,8,"I") <= datetime.datetime.now().date():
        return 0
    OTHVOL = DIq(52.7,IVSOL2,2)
    if int(IVVOL) != int(OTHVOL):
        return 0
    return 1