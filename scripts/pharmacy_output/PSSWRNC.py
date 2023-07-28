#DAL/RJS-NEW WARNING SOURCE CUSTOM WARNING LIST BUILDER CONT;
#1.0;PHARMACY DATA MANAGEMENT;**98,144**;10/12/05;Build 13
#
#IA: 3735 ^PSNDF(50.68
#IA: 4445 ^PS(50.625
#IA: 4446 ^PS(50.626
#IA: 4448 ^PS(50.627

def SEL1():
    DR=0
    while DR:
        DR += 1
        if not DR in ^PSDRUG: continue
        if not ^PSDRUG(DR,0): continue
        WARN54 = ^PSDRUG(DR,0)[8]
        if not WARN54: continue
        if SKIP and ^PSDRUG(DR, "WARN")[1]: continue
        ACTIVE = PSSWRNB.ACTIVE()
        if not ACTIVE: continue
        PSSWRNB.DRUG()
        if not PSSWRN:
            ^TMP("PSSWRNB", $J, ^PSDRUG(DR,0)) = WARN54_"^"_NDF

def SEL2():
    DR=0
    while DR:
        DR += 1
        if not DR in ^PSDRUG: continue
        if not ^PSDRUG(DR,0): continue
        WARN54 = ^PSDRUG(DR,0)[8]
        if not WARN54: continue
        if SKIP and ^PSDRUG(DR, "WARN")[1]: continue
        ACTIVE = PSSWRNB.ACTIVE()
        if not ACTIVE: continue
        for I in range(1, len(WARN54.split(","))+1):
            WARN = WARN54.split(",")[I]
            if WARN > 20:
                if not WARN in ^PS(54): continue
                ^TMP("PSSWRNB", $J, ^PSDRUG(DR,0)) = WARN54

def SEL3():
    print("\n")
    DIC = dict()
    DIC["B"] = ""
    DIC = "^PSDRUG("
    DIC[0] = "AEKQM"
    DIC["A"] = "Enter starting drug name: "
    DIC = PSSWRNB.DIC()
    if not DIC: continue
    PSSDRG = DIC[2]
    PSSDG[PSSDRG] = 1
    print("\n")
    DIC = dict()
    DIC["B"] = ""
    DIC = "^PSDRUG("
    DIC[0] = "AEKQM"
    DIC["A"] = "Enter ending drug name: "
    DIC = PSSWRNB.DIC()
    if not DIC: continue
    PSSEDRG = DIC[2]
    PSSDG[PSSEDRG] = 2
    PSS1 = ""
    PSS1 = PSSDG[1]
    if PSSDG[PSS1] > 1:
        print("\n", "The Ending drug name must come alphabetically", "\n", "after your Starting drug name.", "\n")
        PSSDG = dict()

def SEL4():
    DR=0
    while DR:
        DR += 1
        if SKIP and ^PSDRUG(DR, "WARN")[1]: continue
        ACTIVE = PSSWRNB.ACTIVE()
        if not ACTIVE: continue
        PSSWRNB.DRUG()
        if not PSSWRN: continue
        XX = DR
        PSSWRNA.CHECK20()

        if len(PSSWRN.split(",")) > 5:
            ^TMP("PSSWRNB",$J,^PSDRUG(DR,0)) = PSSWRN

def SEL59():
    DIC = dict()
    DIC = 54
    DIC[0] = "AEQM"
    DIC["A"] = "Select drugs containing RX Consult number:"
    DIC = PSSWRNC.DIC()
    if DIC < 0: continue
    RXNUM = DIC[2]
    if not ^PS(54, RXNUM): continue
    if SEL == 9 and not ^PS(54, RXNUM, 2): continue
    if SEL == 9:
        PSO9 = ^PS(54, RXNUM, 2) + "N"
        print("  ", RXNUM, " is mapped to ", PSO9)
        DR=0
        while DR:
            DR += 1
            if not DR in ^PSDRUG: continue
            if not ^PSDRUG(DR,0): continue
            WARN54 = ^PSDRUG(DR,0)[8]
            if not WARN54: continue
            if SKIP and ^PSDRUG(DR, "WARN")[1]: continue
            ACTIVE = PSSWRNB.ACTIVE()
            if not ACTIVE: continue
            if ("," + WARN54 + ",").includes("," + RXNUM + ","):
                if SEL == 9:
                    PSSWRNB.DRUG()
                    if not PSSWRN: continue
                    if ("," + PSSWRN + ",").includes("," + PSO9 + ","): continue
                ^TMP("PSSWRNB", $J, ^PSDRUG(DR,0)) = WARN54

def SEL6():
    DR=0
    while DR:
        DR += 1
        if not DR in ^PSDRUG: continue
        if not ^PSDRUG(DR,0): continue
        WARN54 = ^PSDRUG(DR,0)[8]
        if not WARN54: continue
        if SKIP and ^PSDRUG(DR, "WARN")[1]: continue
        ACTIVE = PSSWRNB.ACTIVE()
        if not ACTIVE: continue
        for I in range(1, len(WARN54.split(","))+1):
            WARN = WARN54.split(",")[I]
            if WARN and ^PS(54, WARN, 1) and not ^PS(54, WARN, 2):
                ^TMP("PSSWRNB", $J, ^PSDRUG(DR,0)) = WARN54

def SEL7():
    print("\n")
    DIR = dict()
    DIR["A"] = "Select drugs containing New warning number"
    DIR["?",1] = "Answer with WARNING LABEL-ENGLISH NUMBER using the format #N."
    DIR["?",2] = "Where # is the numeric number of the warning label desired."
    DIR["?"] = "Example:  for the warning label number 15 entry 15N."
    DIR["??"] = "PSSWRNC.HELP"
    DIR[0] = "FO"
    DIR = PSSWRNC.DIR()
    RXNUM = DIR
    if RXNUM == "N" or RXNUM == "n" or RXNUM == "Y" or RXNUM == "y":
        print("\n", RXNUM, " is not a valid entry", "\n")
        QUIT = 1
        return
    if RXNUM.includes("N") or RXNUM.includes("n"):
        RXNUM = RXNUM.replace("N", "").replace("n", "")
    if RXNUM == "^" or RXNUM == "" or RXNUM == " ":
        QUIT = 1
        return
    if not ^PS(50.625, RXNUM):
        print("\n", RXNUM, " is not in the New warning file", "\n")
        QUIT = 1
        return
    print(chr(12))
    print("Searching for drugs that contain new warning number ", RXNUM)
    PSOWARN = RXNUM + "N"
    STAR = ""
    PSSWRNE.NEWWARN()

    DIR[0] = "E"
    DIR = PSSWRNC.DIR()
    if not DIR: continue
    DR=0
    while DR:
        DR += 1
        if SKIP and ^PSDRUG(DR, "WARN")[1]: continue
        ACTIVE = PSSWRNB.ACTIVE()
        if not ACTIVE: continue
        PSSWRNB.DRUG()
        if PSSWRN and ("," + PSSWRN + ",").includes("," + RXNUM + "N,"):
            ^TMP("PSSWRNB",$J,^PSDRUG(DR,0)) = PSSWRN

def SEL8():
    WARN = 0
    GEND = dict()
    while WARN:
        WARN += 1
        if ^PS(50.625, WARN, 2):
            GEND[WARN + "N"] = ""
    if not GEND: return
    DR=0
    while DR:
        DR += 1
        if SKIP and ^PSDRUG(DR, "WARN")[1]: continue
        ACTIVE = PSSWRNB.ACTIVE()
        if not ACTIVE: continue
        PSSWRNB.DRUG()
        if PSSWRN:
            for WARN in GEND:
                if ("," + PSSWRN + ",").includes("," + WARN + ","):
                    ^TMP("PSSWRNB",$J,^PSDRUG(DR,0)) = PSSWRN

def HELP():
    print("\n")
    DIR = dict()
    DIR["A"] = "Select drugs containing New warning number:"
    DIR["??"] = "PSSWRNC.HELP"
    DIR[0] = "FO"
    DIR = PSSWRNC.DIR()
    if DIR or Y == "^":
        PSSEND = "^"
        return
    print(chr(12))
    print("Select drugs containing New warning number:", "\n", "Choose from:", "\n")
    PSSIEN = 0
    DIR[0] = "FO"
    DIR["A"] = "   '^' to STOP"
    while PSSIEN:
        PSSIEN += 1
        PSSCNT = ^PS(50.625, PSSIEN, 1)[4]
        if PSSCNTR + PSSCNT > 17:
            DIR[0] = "E"
            DIR = PSSWRNC.DIR()
            if not DIR: continue
            if X or Y == "^":
                PSSEND = "^"
                return
            print(chr(12))
            print("Select drugs containing New warning number:", "\n", "Choose from:", "\n")
            PSSCNTR = 0
        print("\n", PSSIEN, "N")
        for PSSCT in range(1, PSSCNT+1):
            if PSSCT > 1:
                print("\n")
            print(" " * 12, ^PS(50.625, PSSIEN, 1, PSSCT))

def EOP():
    DIR[0] = "E"
    DIR = PSSWRNC.DIR()
    if X or Y == "^":
        PSSEND = "^"
        return
    print(chr(12))
    print("Select drugs containing New warning number:", "\n", "Choose from:", "\n")
    PSSCNTR = 0

SEL1()
SEL2()
SEL3()
SEL4()
SEL59()
SEL6()
SEL7()
SEL8()