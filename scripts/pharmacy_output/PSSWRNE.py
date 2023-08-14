#PSSWRNE ;BIR/EJW - NEW WARNING SOURCE NEW WARNING LABEL LIST EDITOR ;05/24/04
## 1.0;PHARMACY DATA MANAGEMENT;**87,233**;9/30/97;Build 2

# Reference to ^PS(50.625 supported by DBIA 4445
def EN(RTN):
    PSSSTWN = 1
    STAR, QUIT, PSSOUT = "", 0, 0
    DRUG = ""
    while True:
        DRUG = next(iter(^TMP("PSSWRNB",$J,DRUG)), "")
        if DRUG == "":
            break
        DRUGN = next(iter(^PSDRUG("B",DRUG,0)), "")
        if not DRUGN:
            continue
        DEA()
        PRINT()
        if QUIT:
            break
    if PSSSTWN:
        RTN = QUIT

def PRINT():
    NEWLIST, STAR = "", ""
    if not PSSLOOK:
        print()
        print("Current Warning labels for", DRUG)
        if NEWLIST == "" and "N" not in PSSWRN:
            print("No warnings from the new data source exist for this drug.")
            print("Verify that the drug is matched to the National Drug File.")
    if PSSWRN != "":
        if not PSSLOOK:
            print("Labels will print in the order in which they appear for local and CMOP fills:")
        if not ENDWARN:
            ENDWARN = 5
        STAR = ""
        for WWW in range(1, ENDWARN+1):
            PSOWARN = PSSWRN.split(",")[WWW-1]
            if PSOWARN == "":
                continue
            if WWW > 5:
                STAR = "*"
            if "N" in PSOWARN:
                NEWWARN()
            else:
                WARN54()
            if QUIT:
                break
        FULL()
        if not PSSOUT:
            print()
            print("Pharmacy fill card display: DRUG WARNING", PSSWRN)
        if PSSLOOK:
            return
        if SEL == 6:
            WARN54 = ^TMP("PSSWRNB",$J,DRUG)
            FULL()
            print("  RX CONSULT file Drug Warning=", WARN54)
            for I in WARN54.split(","):
                if I != "" and not ^PS(54,I,2):
                    FULL()
                    print("  ", I, ^PS(54,I,0), "is not mapped to the new data source")
        if SEL == 8:
            print()
            DIE = "^PSDRUG("
            DA = DRUGN
            DR = 8.2
            ^DIE(DA,DR)
        NEWLIST = ^PSDRUG(DRUGN,"WARN")
        if NEWLIST == "":
            if "N" in PSSWRN:
                FULL()
                print("NOTE: Because the NEW WARNING LABEL LIST field is empty, the warnings above")
                FULL()
                print("are the warnings that our national data source distributes for this drug.")
    if PSSLOOK:
        return
    if NEWLIST != "":
        FULL()
        print("NEW WARNING LABEL LIST:", NEWLIST)
    FULL()
    print()
    DIR(0) = "Y"
    DIR("B") = "N"
    DIR("A") = "Would you like to edit this list of warnings"
    ^DIR
    if DTOUT or DUOUT:
        QUIT = 1
    if not Y:
        if DRUGENT:
            WARNEDIT = 0
            ^TMP("PSSWRNB",$J) = ""
    if DRUGENT:
        WARNEDIT = 1
        ^TMP("PSSWRNB",$J) = ""
    OLDWARN = PSSWRN
    DIE = "^PSDRUG("
    DA = DRUGN
    DR = 8.1
    ^DIE(DA,DR)
    PSSWRN = ^PSDRUG(DRUGN,"WARN")
    if PSSWRN != "":
        CHECK20()
        PRINT()
    if OLDWARN != "" and PSSWRN == "":
        DEA()
        PRINT()
    return

def FULL():
    if ($Y+3) > IOSL and not PSSOUT:
        HDR()

def NEWWARN():
    PSOWRNN = int(PSOWARN)
    if ^PS(50.625,PSOWRNN):
        if not PSSLOOK:
            print()
        TEXT = STAR+PSOWARN+" "
        JJJ = 0
        while True:
            JJJ += 1
            STR = ^PS(50.625,PSOWRNN,1,JJJ,0)
            if not STR:
                break
            TEXT = TEXT+" "+STR
    if TEXT != "":
        FORMAT()
        if PSSLOOK:
            FULL()
        else:
            FULL^PSSLOOK()
    return

def WARN54():
    TEXT = ""
    if ^PS(54,PSOWARN,1):
        if not PSSLOOK:
            print()
        TEXT = STAR+PSOWARN+" "
        JJJ = 0
        while True:
            JJJ += 1
            TEXT = TEXT+" "+^PS(54,PSOWARN,1,JJJ,0)
            if not ^PS(54,PSOWARN,1,JJJ):
                break
    if TEXT != "":
        FORMAT()
        if PSSLOOK:
            FULL()
        else:
            FULL^PSSLOOK()
    return

def VALID():
    BAD = 0
    if X == "":
        print("TOO MANY WARNINGS. LIMIT ANSWER STRING TO 30 CHARACTERS OR LESS")
        del Y
        return
    for PSOWARN in X.split(","):
        if PSOWARN != "":
            if "N" in PSOWARN:
                PSOWRNN = int(PSOWARN)
                if not ^PS(50.625,PSOWRNN):
                    print(PSOWARN, "does not exist in the WARNING LABEL-ENGLISH file")
                    BAD = 1
            else:
                if not ^PS(54,PSOWARN):
                    print(PSOWARN, "does not exist in the RX CONSULT file")
                    BAD = 1
    if BAD:
        del X
    return

def FORMAT():
    LEN = 0
    PTEXT = ""
    for STR in TEXT.split(" "):
        STR = STR + " "
        if LEN + len(STR) < 80:
            PTEXT = PTEXT + STR
            LEN = LEN + len(STR)
        else:
            LEN = 0
            FULL()
            print(PTEXT)
            PTEXT = ""
    if PTEXT != "":
        FULL()
        print(PTEXT)
        PTEXT = ""
    return

def NOTE():
    PSSWSITE = ^PS(59.7,0)
    if $P(^PS(59.7,PSSWSITE,10),"^",9) != "N":
        print("NOTE: You must edit the WARNING LABEL SOURCE field using the option")
        print("Pharmacy System Parameters Edit to enable national warning labels.")
    return

def DEA():
    DEA = $P(^PSDRUG(DRUGN,0),"^",3)
    XX = DRUGN
    WARNLST()
    if PSSWRN == "":
        PSSWRN = $P(^PSDRUG(DRUGN,0),"^",8)
    CHECK20()
    CHECKLST()
    return

def HDR():
    DIR(0)="E"
    ^DIR
    if not Y:
        PSSOUT = 1
        QUIT = 1
    print("Current Warning labels for", DRUG, "(continued)")
    return

def NOTE2():
    print()
    print("The RX CONSULT File (#54) contains local label expansions.")
    print("The WARNING LABEL-ENGLISH file (#50.625) contains national label")
    print("expansions in English.")
    print("The WARNING LABEL-SPANISH file (#50.626) contains national label")
    print("expansions in Spanish.")
    print("It is important to note that RX Consult entry numbers do not")
    print("correlate with the other files (i.e. Number 7 in file 54 is not")
    print("included in file 50.625).")
    print()
    print("You should print a list of the current RX CONSULT file entries")
    print("and the current WARNING LABEL-ENGLISH file entries.")
    print()
    return