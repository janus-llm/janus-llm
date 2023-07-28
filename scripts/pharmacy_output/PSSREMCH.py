def PSSREMCH():
    # BIR/RTR-Pre release Orderable Item report ;02/14/00
    # 1.0;PHARMACY DATA MANAGEMENT;**34**;9/30/97

    PSSOUT = 0
    TEXT()
    if PSSOUT:
        del PSSOUT
        return
    ADDRP()

def ADD():
    global PSSOUT, PSSADSUM, PSSTOTAL, PSSIVID, PSSIVIDL, PSSSOSUM, PSSDV, PSSCOT
    PSSOUT = 0
    PSSADSUM = None
    PSSTOTAL = None
    PSSIVID = None
    PSSIVIDL = None
    PSSSOSUM = None
    PSSDV = 'C' if IOST[0].upper() == 'C' else 'P'
    PSSCOT = 1
    
    PSSIVID = ^PS(59.7,1,31)
    if $P($G(^PS(59.7,1,31)),"^",2) != "":
        PSSIVID = $P($G(^(31)),"^",2)
    else:
        PSSIVID = "IV"
    PSSIVIDL = $L(PSSIVID)
    
    if PSSTYPE == "S":
        SOL()
        return

    PSSWH = "A"
    ADDH()
    ADD = ""
    while ADD != "":
        ADD = ADD + 1
        ADDIEN = 0
        while ADDIEN != 0:
            ADDIEN = ADDIEN + 1
            if $P($G(^PS(52.6,ADDIEN,0)),"^",11):
                ZERO = $G(^PS(52.6,ADDIEN,0))
                LEN = $L($P(ZERO,"^"))
                PSSADID = ""
                PSSADIN = $P($G(^PS(52.6,ADDIEN,"I")),"^")
                if PSSADIN:
                    PSSADID = "("_$E(PSSADIN,4,5)_"/"_$E(PSSADIN,6,7)_"/"_$E(PSSADIN,2,3)_")"
                LEN = LEN + $S(PSSADID != "":11,1:0)
                PAD = "=" * (42-LEN) + "> "
                OINAME = $P($G(^PS(50.7,+$P(ZERO,"^",11),0)),"^")
                OIDOSE = $P($G(^PS(50.606,+$P($G(^(0)),"^",2),0)),"^")
                OILT = $L($G(OINAME)) + $L($G(OIDOSE)) + 2
                OIDATED = ""
                OIDATE = $P($G(^PS(50.7,+$P(ZERO,"^",11),0)),"^",4)
                if OIDATE:
                    OIDATED = "("_$E(OIDATE,4,5)_"/"_$E(OIDATE,6,7)_"/"_$E(OIDATE,2,3)_")"
                ADDLT = $L(ADDIEN) + 3
                PSSTOTAL = $G(ADDLT) + 45 + $G(OILT) + $S($G(OIDATED) != "":11,1:0) + $G(PSSIVIDL)
                PSSPADZ = $G(ADDLT) + 42
                if ($Y+5) > IOSL:
                    ADDH()
                    if PSSOUT:
                        return
                if $G(PSSTOTAL) < 132:
                    print("("_$G(ADDIEN)_") "_$P(ZERO,"^")_$S($G(PSSADID) != "":$G(PSSADID),1:"")_$G(PAD)_$G(OINAME)_"  "_$G(OIDOSE)_$S($G(OIDATED) != "":$G(OIDATED),1:"")_"  "_$G(PSSIVID))
                if $G(PSSTOTAL) > 131:
                    print("("_$G(ADDIEN)_") "_$P(ZERO,"^")_$S($G(PSSADID) != "":$G(PSSADID),1:"")_$G(PAD))
                    print("=====> "_$G(OINAME)_"  "_$G(OIDOSE)_$S($G(OIDATED) != "":$G(OIDATED),1:"")_"  "_$G(PSSIVID))
                OI = $P($G(^PSDRUG(+$P(ZERO,"^",2),2)),"^")
                if 'OI:
                    print("cannot re-match, no Orderable Item for the Dispense Drug")
                    continue
                PSSATMP = $P($G(^PS(50.7,OI,0)),"^")_"  "_$P($G(^PS(50.606,+$P($G(^(0)),"^",2),0)),"^")
                ^TMP($J,"PSSAD",PSSATMP,ADDIEN) = OI
                NEWOI = $P($G(^PS(50.7,+$G(OI),0)),"^")_"  "_$P($G(^PS(50.606,+$P($G(^(0)),"^",2),0)),"^")
                OIZDZ = ""
                OIZD = $P($G(^PS(50.7,+$G(OI),0)),"^",4)
                if OIZD:
                    OIZDZ = "("_$E(OIZD,4,5)_"/"_$E(OIZD,6,7)_"/"_$E(OIZD,2,3)_")"
                PSSPADZZ = ""
                PSSPADX = $G(PSSPADZ) - 18
                PSSPADZZ = "=" * PSSPADX + "> "
                print("New Orderable Item"_$G(PSSPADZZ)_$G(NEWOI)_$S($G(OIZDZ) != "":$G(OIZDZ),1:""))
                print("Dispense Drugs matched to Orderable Item:")
                for PAA in ^PSDRUG("ASP",OI):
                    if ($Y+4) > IOSL:
                        ADDH()
                        if PSSOUT:
                            return
                    PSINDATE = ""
                    PSINDAT = $P($G(^PSDRUG(PAA,"I")),"^")
                    if PSINDAT:
                        PSINDATE = " ("_$E(PSINDAT,4,5)_"/"_$E(PSINDAT,6,7)_"/"_$E(PSINDAT,2,3)_")"
                    if PSINDAT and PSINDAT < $G(PSSYRX):
                        continue
                    print($P($G(^PSDRUG(PAA,0)),"^")_$G(PSINDATE), end='')
                    if PAA == $P(ZERO,"^",2):
                        print(" "*42 + "(Additive link)")
                    else:
                        print()
    if PSSOUT:
        ADDX()
        return

    ADDHS()
    if PSSOUT:
        ADDX()
        return

    PSSADSUM = 1
    AA = ""
    while AA != "":
        AA = AA + 1
        AAZ = $O(^TMP($J,"PSSAD",AA,0))
        AAZZ = +$G(^TMP($J,"PSSAD",AA,+$G(AAZ)))
        if ($Y+4) > IOSL:
            ADDH()
            if PSSOUT:
                return
        print("OI => "_AA_$S($P($G(^PS(50.7,AAZZ,0)),"^",4) == "":"",1:" ("_$E($P($G(^(0)),"^",4),4,5)_"/"_$E($P($G(^(0)),"^",4),6,7)_"/"_$E($P($G(^(0)),"^",4),2,3)_")"))
        PZZ = 0
        while PZZ != 0:
            PZZ = PZZ + 1
            if ($Y+4) > IOSL:
                ADDH()
                if PSSOUT:
                    return
            print("("_$G(PZZ)_") ", end='')
            print($P($G(^PS(52.6,PZZ,0)),"^")_$S($P($G(^("I")),"^") == "":"",1:" ("_$E($P($G(^("I")),"^"),4,5)_"/"_$E($P($G(^("I")),"^"),6,7)_"/"_$E($P($G(^("I")),"^"),2,3)_")"), end='')
            print(" "*27 + "(Additive)")
        if PSSOUT:
            return
        print("Dispense Drugs matched to OI:")
        PDD = 0
        while PDD != 0:
            PDD = PDD + 1
            if ($Y+4) > IOSL:
                ADDH()
                if PSSOUT:
                    return
            if $P($G(^PSDRUG(PDD,"I")),"^") and $P($G(^("I")),"^") < $G(PSSYRX):
                continue
            print(" "*11 + $P($G(^PSDRUG(PDD,0)),"^")_$S($P($G(^("I")),"^") == "":"",1:" ("_$E($P($G(^("I")),"^"),4,5)_"/"_$E($P($G(^("I")),"^"),6,7)_"/"_$E($P($G(^("I")),"^"),2,3)_")"))
    ADDX()
    
def ADDX():
    del ^TMP($J,"PSSAD")
    if PSSTYPE == "B" and not PSSOUT:
        SOL()
        return
    if not PSSOUT:
        PDIR()
    END()

def SOL():
    global PSSOUT, PSSOL, PSSCOTX, PSSWH
    PSSOL = None
    PSSCOTX = None
    PSSWH = "S"
    SOLH()
    if PSSOUT:
        SEND()
        return
    SOL = ""
    while SOL != "":
        SOL = SOL + 1
        SOLIEN = 0
        while SOLIEN != 0:
            SOLIEN = SOLIEN + 1
            if not $P($G(^PS(52.7,SOLIEN,0)),"^",11):
                continue
            ZERO = $G(^PS(52.7,SOLIEN,0))
            SNAME = $P(ZERO,"^")_"  ("_$P(ZERO,"^",3)_")"
            LEN = $L(SNAME)
            SDAT = ""
            SDA = $P($G(^PS(52.7,SOLIEN,"I")),"^")
            if SDA:
                SDAT = "("_$E(SDA,4,5)_"/"_$E(SDA,6,7)_"/"_$E(SDA,2,3)_")"
            LEN = LEN + $S($G(SDAT) != "":11,1:0)
            PAD = "=" * (53-LEN) + "> "
            SOINAME = $P($G(^PS(50.7,+$P(ZERO,"^",11),0)),"^")
            SOIDOSE = $P($G(^PS(50.606,+$P($G(^(0)),"^",2),0)),"^")
            SOILT = $L($G(SOINAME)) + $L($G(SOIDOSE)) + 2
            SDOID = ""
            SDOI = $P($G(^PS(50.7,+$P(ZERO,"^",11),0)),"^",4)
            if SDOI:
                SDOID = "("_$E(SDOI,4,5)_"/"_$E(SDOI,6,7)_"/"_$E(SDOI,2,3)_")"
            SOLLT = $L(SOLIEN) + 3
            PSSTOTAL = $G(SOLLT) + 67 + $G(SOILT) + $S($G(PDOID) != "":11,1:0) + $G(PSSIVIDL)
            PSSSOLZ = $G(SOLLT) + 53
            if ($Y+5) > IOSL:
                SOLH()
                if PSSOUT:
                    return
            print(" "*3 + "Current Solution/Orderable Item match:")
            if $G(PSSTOTAL) < 132:
                print("("_$G(SOLIEN)_") "_$G(SNAME)_$S($G(SDAT) != "":$G(SDAT),1:"")_$G(PAD)_$G(SOINAME)_"  "_$G(SOIDOSE)_$S($G(SDOID) != "":$G(SDOID),1:"")_"  "_$G(PSSIVID))
            if $G(PSSTOTAL) > 131:
                print("("_$G(SOLIEN)_") "_$G(SNAME)_$S($G(SDAT) != "":$G(SDAT),1:"")_$G(PAD))
                if ($Y+4) > IOSL:
                    SOLH()
                    if PSSOUT:
                        return
                print("=====> "_$G(SOINAME)_"  "_$G(SOIDOSE)_$S($G(SDOID) != "":$G(SDOID),1:"")_"  "_$G(PSSIVID))
            SLOI = $P($G(^PSDRUG(+$P(ZERO,"^",2),2)),"^")
            if not SLOI:
                print("cannot rematch, no Item for the Dispense Drug")
                continue
            PSSSTMP = $P($G(^PS(50.7,+$G(SLOI),0)),"^")_"  "_$P($G(^PS(50.606,+$P($G(^(0)),"^",2),0)),"^")
            ^TMP($J,"PSSOL",PSSSTMP,SOLIEN) = SLOI
            SLNEWOI = $P($G(^PS(50.7,+$G(SLOI),0)),"^")_"  "_$P($G(^PS(50.606,+$P($G(^(0)),"^",2),0)),"^")
            SOIZDZ = ""
            SOIZD = $P($G(^PS(50.7,+$G(SLOI),0)),"^",4)
            if SOIZD:
                SOIZDZ = "("_$E(SOIZD,4,5)_"/"_$E(SOIZD,6,7)_"/"_$E(SOIZD,2,3)_")"
            SZL = "=" * ($G(PSSSOLZ) - 18)
            SZL = SZL + "> "
            print("New Orderable Item"_$G(SZL)_$G(SLNEWOI)_$S($G(SOIZDZ) != "":$G(SOIZDZ),1:""))
            print("Dispense Drugs matched to Orderable Item:")
            for SAA in ^PSDRUG("ASP",SLOI):
                if ($Y+4) > IOSL:
                    SOLH()
                    if PSSOUT:
                        return
                SLID = ""
                SLIDD = $P($G(^PSDRUG(SAA,"I")),"^")
                if SLIDD:
                    SLID = " ("_$E(SLIDD,4,5)_"/"_$E(SLIDD,6,7)_"/"_$E(SLIDD,2,3)_")"
                if SLIDD and SLIDD < $G(PSSYRX):
                    continue
                print(" "*4 + $P($G(^PSDRUG(SAA,0)),"^")_$G(SLID), end='')
                if SAA == $P(ZERO,"^",2):
                    print(" "*59 + "(Solution link)")
                else:
                    print()
    if PSSOUT:
        SEND()
        return

    SOLHS()
    if PSSOUT:
        SEND()
        return

    PSSSOSUM = 1
    SOLAA = ""
    while SOLAA != "":
        SOLAA = SOLAA + 1
        SSZ = $O(^TMP($J,"PSSOL",SOLAA,0))
        SSZZ = +$G(^TMP($J,"PSSOL",SOLAA,+$G(SSZ)))
        if ($Y+4) > IOSL:
            SOLH()
            if PSSOUT:
                return
        print("OI => "_SOLAA_$S($P($G(^PS(50.7,SSZZ,0)),"^",4) == "":"",1:" ("_$E($P($G(^(0)),"^",4),4,5)_"/"_$E($P($G(^(0)),"^",4),6,7)_"/"_$E($P($G(^(0)),"^",4),2,3)_")"))
        SZZ = 0
        while SZZ != 0:
            SZZ = SZZ + 1
            if ($Y+4) > IOSL:
                SOLH()
                if PSSOUT:
                    return
            print("("_$G(SZZ)_") ", end='')
            print($P($G(^PS(52.7,SZZ,0)),"^")_"   ("_$P($G(^(0)),"^",3)_")"_$S($P($G(^("I")),"^") == "":"",1:" ("_$E($P($G(^("I")),"^"),4,5)_"/"_$E($P($G(^("I")),"^"),6,7)_"/"_$E($P($G(^("I")),"^"),2,3)_")"), end='')
            print(" "*27 + "(Solution)")
        if PSSOUT:
            return
        print("Dispense Drugs matched to OI:")
        SLDD = 0
        while SLDD != 0:
            SLDD = SLDD + 1
            if ($Y+4) > IOSL:
                SOLH()
                if PSSOUT:
                    return
            if $P($G(^PSDRUG(SLDD,"I")),"^") and $P($G(^("I")),"^") < $G(PSSYRX):
                continue
            print(" "*11 + $P($G(^PSDRUG(SLDD,0)),"^")_$S($P($G(^("I")),"^") == "":"",1:" ("_$E($P($G(^("I")),"^"),4,5)_"/"_$E($P($G(^("I")),"^"),6,7)_"/"_$E($P($G(^("I")),"^"),2,3)_")"))
    if not PSSOUT:
        PDIR()
    SEND()

def ADDH():
    global PSSOUT, PSSCOT
    if PSSCOT == 1:
        print("ADDITIVE REPORT    (Additive Internal number in parenthesis)" + " "*46 + "PAGE: " + str(PSSCOT))
        PSSCOT = PSSCOT + 1
    if PSSDV == 'C':
        if not input("Press Return to continue, '^' to exit"):
            PSSOUT = 1
            return
    print("ADDITIVE " + ("REPORT" if not PSSADSUM else "SUMMARY") + "   (continued)" + " "*52 + "PAGE: " + str(PSSCOT))
    PSSCOT = PSSCOT + 1

def ADDHS():
    global PSSOUT, PSSCOT
    if PSSDV == 'C':
        if not input("Press Return to continue, '^' to exit"):
            PSSOUT = 1
            return
    print("ADDITIVE SUMMARY" + " "*59 + "PAGE: " + str(PSSCOT))
    PSSCOT = PSSCOT + 1

def SOLH():
    global PSSOUT, PSSCOT, PSSCOTX
    if not PSSCOTX:
        if PSSDV == 'C' and PSSCOT != 1:
            if not input("Press Return to continue, '^' to exit"):
                PSSOUT = 1
                return
    print("SOLUTION REPORT   (Solution Internal number in parenthesis)" + " "*55 + "PAGE: " + str(PSSCOT))
    PSSCOT = PSSCOT + 1

def SOLHS():
    global PSSOUT, PSSCOT
    if PSSDV == 'C':
        if not input("Press Return to continue, '^' to exit"):
            PSSOUT = 1
            return
    print("SOLUTION SUMMARY" + " "*61 + "PAGE: " + str(PSSCOT))
    PSSCOT = PSSCOT + 1

def PDIR():
    global PSSOUT
    if PSSDV == 'C':
        if not input("Pres Return to continue, '^' to exit"):
            PSSOUT = 1

def SEND():
    global PSSOUT
    del ^TMP($J,"PSSOL")
    END()

def END():
    global PSSTOTAL, PSSIVID, PSSIVIDL, PSSTYPE, PSSDV, PSSWH, PSSCOT, PSSOUT, PSSCOTX, PSSADSUM, PSSSOSUM, PSSYRX
    PSSTOTAL = None
    PSSIVID = None
    PSSIVIDL = None
    PSSTYPE = None
    PSSDV = None
    PSSWH = None
    PSSCOT = None
    PSSOUT = None
    PSSCOTX = None
    PSSADSUM = None
    PSSSOSUM = None
    PSSYRX = None
    ^%ZISC
    if $D(ZTQUEUED):
        ZTREQ = "@"