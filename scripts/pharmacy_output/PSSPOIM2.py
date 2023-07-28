def PSSPOIM2():
    # BIR/RTR/WRT-Orderable Item manual create - initial create ; 09/01/98 7:12
    # 1.0;PHARMACY DATA MANAGEMENT;**15**;9/30/97
    
    WOOPS()
    time.sleep(2)
    if '^TMP("PSSLOOP")' in globals():
        return
    PSSITE = int(+$O(^PS(59.7,0)))
    if $P($G(^PS(59.7,PSSITE,80)),"^",2) != 2:
        print("!!?3,$S($P($G(^(80)),"^",2)<2:"Orderable Item Auto-Create has not been completed!",1:"Manual matching process complete!"),!!")
        print("!!?")
        PSSITE = None
        return

    print("K DIR S DIR(""A"")=""Press RETURN to continue"",DIR(0)=""E"" D ^DIR K DIR")
    PSOUT = 0
    MESSZ_PSSPOIM1()
    if PSOUT:
        CHECK()
    
    PSCREATE = 1
    PSSPOIM3()
    if PSOOOUT:
        CHECK()
    
    print("W !!?3,""NOW MATCHING DISPENSE DRUGS!"",!!")
    X1 = DT
    X2 = -365
    C^%DTC()
    PSXDATE = X
    PSOUT = 0
    AAA = ""
    while AAA != "" and not PSOUT:
        PSIEN = 0
        while PSIEN != 0 and not PSOUT:
            ZXX = 0
            if $G(^PSDRUG(PSIEN,2)) and not $P($G(^PSDRUG(PSIEN,2)),"^"):
                APLU = $P($G(^PSDRUG(PSIEN,2)),"^",3)
                ZXX = 1
                PSXDDATE = +$P($G(^PSDRUG(PSIEN,"I")),"^")
                if PSXDDATE and PSXDDATE < PSXDATE:
                    ZXX = 0
            if ZXX and (APLU["I" or APLU["O" or APLU["U"):
                PSNAME = $P(^PSDRUG(PSIEN,0),"^")
                START()
    CHECK()
    CHECK^PSSPOIM1()
    END^PSSPOIM1()

def TMP():
    global PSCNT
    ^TMP($J,"PSSOO") = []
    PSCNT = 0
    if +$P(NODE,"^") and +$P(NODE,"^",3):
        ZZ = 0
        while ZZ != 0:
            if +$P($G(^PSDRUG(ZZ,2)),"^") and $P(^PSDRUG(ZZ,2),"^") != POINT and $D(^PS(50.7,$P(^PSDRUG(ZZ,2),"^"),0)):
                OTH = $G(^PSDRUG(ZZ,"ND"))
                if +$P(OTH,"^") and +$P(OTH,"^",3) and $G(DOSEFV) != 0:
                    DA = $P($G(OTH),"^")
                    K = $P($G(OTH),"^",3)
                    X = PSJDF^PSNAPIS(DA,K)
                    DOSA = X
                    if $G(DOSA) != 0 and DOSEFV == DOSA:
                        NOFLAG = 0
                        TMPTR = $P(^PSDRUG(ZZ,2),"^")
                        FFF = 0
                        while FFF != 0:
                            if $P(^TMP($J,"PSSOO",FFF),"^") == TMPTR:
                                NOFLAG = 1
                            FFF += 1
                        if not NOFLAG:
                            PSCNT += 1
                            ^TMP($J,"PSSOO",PSCNT) = $P(^PSDRUG(ZZ,2),"^")_"^"_ZZ
    return

def DISP():
    MATCH = 0
    TT = 0
    while TT != 0:
        SPT = $P(^TMP($J,"PSSOO",TT),"^")
        print("!,TT,"  ",$P($G(^PS(50.7,SPT,0)),"^")_" "_$P($G(^PS(50.606,+$P($G(^(0)),"^",2),0)),"^"))
        if $Y+5 > IOSL:
            Y = 0
        if Y == 0:
            PSOUT = 1
        if Y == "":
            PSOUT = 1
    return

def DISPO():
    if PSOUT:
        return
    print("!")
    Y = ""
    Y = '^'
    if Y == "" or (Y == '^'):
        PSOUT = 1
        return
    if not ^TMP($J,"PSSOO",+Y):
        print("!!,?5,"INVALID NUMBER"")
        DISPO()
    MATCH = $P(^TMP($J,"PSSOO",+Y),"^")
    return

def MCH():
    if $O(^TMP($J,"PSSOO",0)):
        print("!")
        Y = ""
        Y = '^'
        if not Y or (Y == '^'):
            PSOUT = 1
            return
        if Y:
            OTHER()
            DISP()
    if PSOUT or PSNO:
        PSOUT = 1
        return
    if $O(^TMP($J,"PSSOO",0)) and MATCH:
        PSSP = MATCH
        PSSPOIM1()
        if PSOUT or PSNO:
            PSOUT = 1
            return
    if $O(^TMP($J,"PSSOO",0)) and MATCH:
        DIE = "^PSDRUG("
        DA = PSIEN
        DR = "2.1////"_MATCH
        ^DIE
        PSPOI = MATCH
        COM()
    return

def START():
    global NODE, DOSEPTR, DA, X, VAGEN, DOSEFV, PSPOI, K, TMPTR, FFF, PSSDIR, DOSEFORM, SPHOLD, NEWSP, RESTART, COMM, PSNAME, STOP, PSNO, PSMAN, DIC, NEWFLAG, NOFLAG, DOSA, OTH
    
    print("!!!,?5,"Dispense Drug -> ",PSNAME")
    NODE = $G(^PSDRUG(PSIEN,"ND"))
    DOSEPTR = 0
    DA = $P($G(NODE),"^")
    X = $$VAGN^PSNAPIS(DA)
    VAGEN = X
    if +$P(NODE,"^") and +$P(NODE,"^",3) and $G(VAGEN) != 0:
        K = $P($G(NODE),"^",3)
        X = $$PSJDF^PSNAPIS(DA,K)
        DOSEFV = X
        if $G(DOSEFV) != 0:
            DOSEPTR = $P(X,"^")
            DOSEFORM = $P(X,"^",2)
    PSPOI = None
    TMP()
    MCH()
    if $G(PSPOI):
        print("!!!")
        PSOUT = 0
        RESTART = 1
        DIR(0) = "Y"
        DIR("B") = "NO"
        DIR("A") = "Do you want to exit this option"
        ^DIR
        if Y or (Y["^") or $D(DTOUT):
            PSOUT = 1
    if $G(RESTART) and not PSOUT:
        START()
    return

def PSSPOIM2():
    global PSSITE, PSOUT, PSCREATE, X1, X2, PSXDATE, AAA, PSIEN, ZXX, APLU, PSNAME
    
    print("K DIR S DIR(""A"")=""Press RETURN to continue"",DIR(0)=""E"" D ^DIR K DIR")
    PSOUT = 0
    MESSZ_PSSPOIM1()
    if PSOUT:
        CHECK()
    
    PSCREATE = 1
    PSSPOIM3()
    if PSOOOUT:
        CHECK()
    
    print("W !!?3,""NOW MATCHING DISPENSE DRUGS!"",!!")
    X1 = DT
    X2 = -365
    C^%DTC()
    PSXDATE = X
    PSOUT = 0
    AAA = ""
    while AAA != "" and not PSOUT:
        PSIEN = 0
        while PSIEN != 0 and not PSOUT:
            ZXX = 0
            if $G(^PSDRUG(PSIEN,2)) and not $P($G(^PSDRUG(PSIEN,2)),"^"):
                APLU = $P($G(^PSDRUG(PSIEN,2)),"^",3)
                ZXX = 1
                PSXDDATE = +$P($G(^PSDRUG(PSIEN,"I")),"^")
                if PSXDDATE and PSXDDATE < PSXDATE:
                    ZXX = 0
            if ZXX and (APLU["I" or APLU["O" or APLU["U"):
                PSNAME = $P(^PSDRUG(PSIEN,0),"^")
                START()
    CHECK()
    CHECK^PSSPOIM1()
    END^PSSPOIM1()

def TMP():
    global PSCNT
    ^TMP($J,"PSSOO") = []
    PSCNT = 0
    if +$P(NODE,"^") and +$P(NODE,"^",3):
        ZZ = 0
        while ZZ != 0:
            if +$P($G(^PSDRUG(ZZ,2)),"^") and $P(^PSDRUG(ZZ,2),"^") != POINT and $D(^PS(50.7,$P(^PSDRUG(ZZ,2),"^"),0)):
                OTH = $G(^PSDRUG(ZZ,"ND"))
                if +$P(OTH,"^") and +$P(OTH,"^",3) and $G(DOSEFV) != 0:
                    DA = $P($G(OTH),"^")
                    K = $P($G(OTH),"^",3)
                    X = PSJDF^PSNAPIS(DA,K)
                    DOSA = X
                    if $G(DOSA) != 0 and DOSEFV == DOSA:
                        NOFLAG = 0
                        TMPTR = $P(^PSDRUG(ZZ,2),"^")
                        FFF = 0
                        while FFF != 0:
                            if $P(^TMP($J,"PSSOO",FFF),"^") == TMPTR:
                                NOFLAG = 1
                            FFF += 1
                        if not NOFLAG:
                            PSCNT += 1
                            ^TMP($J,"PSSOO",PSCNT) = $P(^PSDRUG(ZZ,2),"^")_"^"_ZZ
    return

def DISP():
    MATCH = 0
    TT = 0
    while TT != 0:
        SPT = $P(^TMP($J,"PSSOO",TT),"^")
        print("!,TT,"  ",$P($G(^PS(50.7,SPT,0)),"^")_" "_$P($G(^PS(50.606,+$P($G(^(0)),"^",2),0)),"^"))
        if $Y+5 > IOSL:
            Y = 0
        if Y == 0:
            PSOUT = 1
        if Y == "":
            PSOUT = 1
    return

def DISPO():
    if PSOUT:
        return
    print("!")
    Y = ""
    Y = '^'
    if Y == "" or (Y == '^'):
        PSOUT = 1
        return
    if not ^TMP($J,"PSSOO",+Y):
        print("!!,?5,"INVALID NUMBER"")
        DISPO()
    MATCH = $P(^TMP($J,"PSSOO",+Y),"^")
    return

def MCH():
    if $O(^TMP($J,"PSSOO",0)):
        print("!")
        Y = ""
        Y = '^'
        if not Y or (Y == '^'):
            PSOUT = 1
            return
        if Y:
            OTHER()
            DISP()
    if PSOUT or PSNO:
        PSOUT = 1
        return
    if $O(^TMP($J,"PSSOO",0)) and MATCH:
        PSSP = MATCH
        PSSPOIM1()
        if PSOUT or PSNO:
            PSOUT = 1
            return
    if $O(^TMP($J,"PSSOO",0)) and MATCH:
        DIE = "^PSDRUG("
        DA = PSIEN
        DR = "2.1////"_MATCH
        ^DIE
        PSPOI = MATCH
        COM()
    return

def START():
    global NODE, DOSEPTR, DA, X, VAGEN, DOSEFV, PSPOI, K, TMPTR, FFF, PSSDIR, DOSEFORM, SPHOLD, NEWSP, RESTART, COMM, PSNAME, STOP, PSNO, PSMAN, DIC, NEWFLAG, NOFLAG, DOSA, OTH
    
    print("!!!,?5,"Dispense Drug -> ",PSNAME")
    NODE = $G(^PSDRUG(PSIEN,"ND"))
    DOSEPTR = 0
    DA = $P($G(NODE),"^")
    X = $$VAGN^PSNAPIS(DA)
    VAGEN = X
    if +$P(NODE,"^") and +$P(NODE,"^",3) and $G(VAGEN) != 0:
        K = $P($G(NODE),"^",3)
        X = $$PSJDF^PSNAPIS(DA,K)
        DOSEFV = X
        if $G(DOSEFV) != 0:
            DOSEPTR = $P(X,"^")
            DOSEFORM = $P(X,"^",2)
    PSPOI = None
    TMP()
    MCH()
    if $G(PSPOI):
        print("!!!")
        PSOUT = 0
        RESTART = 1
        DIR(0) = "Y"
        DIR("B") = "NO"
        DIR("A") = "Do you want to exit this option"
        ^DIR
        if Y or (Y["^") or $D(DTOUT):
            PSOUT = 1
    if $G(RESTART) and not PSOUT:
        START()
    return

def TMP():
    global PSCNT
    ^TMP($J,"PSSOO") = []
    PSCNT = 0
    if +$P(NODE,"^") and +$P(NODE,"^",3):
        ZZ = 0
        while ZZ != 0:
            if +$P($G(^PSDRUG(ZZ,2)),"^") and $P(^PSDRUG(ZZ,2),"^") != POINT and $D(^PS(50.7,$P(^PSDRUG(ZZ,2),"^"),0)):
                OTH = $G(^PSDRUG(ZZ,"ND"))
                if +$P(OTH,"^") and +$P(OTH,"^",3) and $G(DOSEFV) != 0:
                    DA = $P($G(OTH),"^")
                    K = $P($G(OTH),"^",3)
                    X = PSJDF^PSNAPIS(DA,K)
                    DOSA = X
                    if $G(DOSA) != 0 and DOSEFV == DOSA:
                        NOFLAG = 0
                        TMPTR = $P(^PSDRUG(ZZ,2),"^")
                        FFF = 0
                        while FFF != 0:
                            if $P(^TMP($J,"PSSOO",FFF),"^") == TMPTR:
                                NOFLAG = 1
                            FFF += 1
                        if not NOFLAG:
                            PSCNT += 1
                            ^TMP($J,"PSSOO",PSCNT) = $P(^PSDRUG(ZZ,2),"^")_"^"_ZZ
    return

def DISP():
    MATCH = 0
    TT = 0
    while TT != 0:
        SPT = $P(^TMP($J,"PSSOO",TT),"^")
        print("!,TT,"  ",$P($G(^PS(50.7,SPT,0)),"^")_" "_$P($G(^PS(50.606,+$P($G(^(0)),"^",2),0)),"^"))
        if $Y+5 > IOSL:
            Y = 0
        if Y == 0:
            PSOUT = 1
        if Y == "":
            PSOUT = 1
    return

def DISPO():
    if PSOUT:
        return
    print("!")
    Y = ""
    Y = '^'
    if Y == "" or (Y == '^'):
        PSOUT = 1
        return
    if not ^TMP($J,"PSSOO",+Y):
        print("!!,?5,"INVALID NUMBER"")
        DISPO()
    MATCH = $P(^TMP($J,"PSSOO",+Y),"^")
    return

def MCH():
    if $O(^TMP($J,"PSSOO",0)):
        print("!")
        Y = ""
        Y = '^'
        if not Y or (Y == '^'):
            PSOUT = 1
            return
        if Y:
            OTHER()
            DISP()
    if PSOUT or PSNO:
        PSOUT = 1
        return
    if $O(^TMP($J,"PSSOO",0)) and MATCH:
        PSSP = MATCH
        PSSPOIM1()
        if PSOUT or PSNO:
            PSOUT = 1
            return
    if $O(^TMP($J,"PSSOO",0)) and MATCH:
        DIE = "^PSDRUG("
        DA = PSIEN
        DR = "2.1////"_MATCH
        ^DIE
        PSPOI = MATCH
        COM()
    return

def START():
    global NODE, DOSEPTR, DA, X, VAGEN, DOSEFV, PSPOI, K, TMPTR, FFF, PSSDIR, DOSEFORM, SPHOLD, NEWSP, RESTART, COMM, PSNAME, STOP, PSNO, PSMAN, DIC, NEWFLAG, NOFLAG, DOSA, OTH
    
    print("!!!,?5,"Dispense Drug -> ",PSNAME")
    NODE = $G(^PSDRUG(PSIEN,"ND"))
    DOSEPTR = 0
    DA = $P($G(NODE),"^")
    X = $$VAGN^PSNAPIS(DA)
    VAGEN = X
    if +$P(NODE,"^") and +$P(NODE,"^",3) and $G(VAGEN) != 0:
        K = $P($G(NODE),"^",3)
        X = $$PSJDF^PSNAPIS(DA,K)
        DOSEFV = X
        if $G(DOSEFV) != 0:
            DOSEPTR = $P(X,"^")
            DOSEFORM = $P(X,"^",2)
    PSPOI = None
    TMP()
    MCH()
    if $G(PSPOI):
        print("!!!")
        PSOUT = 0
        RESTART = 1
        DIR(0) = "Y"
        DIR("B") = "NO"
        DIR("A") = "Do you want to exit this option"
        ^DIR
        if Y or (Y["^") or $D(DTOUT):
            PSOUT = 1
    if $G(RESTART) and not PSOUT:
        START()
    return

def COM():
    print("!!,!"Match Complete!"",!")
    PSPOI = PSPOI if $G(PSPOI) else $G(NEWSP)
    return

def OTHER():
    print("@IOF,!")
    print("There are other Dispense Drugs with the same VA Generic Name and same Dose")
    print("Form already matched to orderable items. Choose a number to match, or enter")
    print("' ^ ' to enter a new one.")
    print("!!,?6,"Disp. drug -> ",PSNAME,!")
    return

def WOOPS():
    if $D(^TMP("PSSLOOP")):
        print("!!,$C(7),"Sorry, but someone else is using this option.",!")
    return

PSSPOIM2()