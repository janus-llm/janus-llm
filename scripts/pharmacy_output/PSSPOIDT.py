def PSSPOIDT():
    # BIR/RTR/WRT-Date update in Orderable Item File
    # 02/14/00
    # 1.0;PHARMACY DATA MANAGEMENT;**19,29,38,57,68,69,82**;9/30/97
    # Reference to ^PS(59 supported by DBIA #1976
    # Passed in is Internal number of Pharmacy Orderable Item
    # Changed all IIII's to II (PWC-4/5/04). Lines were too long to add new code.
    def EN(PSPOINT):
        EN1()
        if PSSCROSS:
            if PSSTEST:
                PSPOINT = PSSTEST
        else:
            if not PSSTEST or not ^PS(50.7, PSSTEST, 0):
                if ZTQUEUED:
                    ZTREQ = "@"
        if ^PS(50.7, PSPOINT, 0):
            return
        if ^PS(50.7, PSPOINT, 0)["^", 4:
            SET()
            return ENT()
        PSSVNAME = $P(^PS(50.7, PSPOINT, 0), "^")
        PSSVDOSE = $P(^PS(50.606, +$P(^PS(50.7, PSPOINT, 0), "^", 2), 0), "^")
        PSACDATE = DT
        PSLATEST = 0
        INACFLAG = 0
        ZZZ = 0
        while ZZZ:
            ZZZ = $O(^PS(50.7, "A50", PSPOINT, ZZZ))
            if ZZZ:
                PSUAPP = $P(^PSDRUG(ZZZ, 2), "^", 3)
                if PSUAPP["O" or PSUAPP["X" or PSUAPP["I" or PSUAPP["U":
                    PSSVAP = $P(^PSDRUG(ZZZ, "I"), "^")
                    if PSSVAP and PSSVAP > PSLATEST:
                        PSLATEST = PSSVAP
                    if not PSSVAP:
                        INACFLAG = 1
                ZZZA = 0
                while ZZZA:
                    ZZZA = $O(^PSDRUG("A526", ZZZ, ZZZA))
                    if ZZZA and ^PS(52.6, ZZZA, 0):
                        PSSVAP = +$P(^PS(52.6, ZZZA, "I"), "^")
                        if PSSVAP and PSSVAP > PSLATEST:
                            PSLATEST = PSSVAP
                        if not PSSVAP:
                            INACFLAG = 1
                ZZZS = 0
                while ZZZS:
                    ZZZS = $O(^PSDRUG("A527", ZZZ, ZZZS))
                    if ZZZS and ^PS(52.7, ZZZS, 0):
                        PSSVAP = +$P(^PS(52.7, ZZZS, "I"), "^")
                        if PSSVAP and PSSVAP > PSLATEST:
                            PSLATEST = PSSVAP
                        if not PSSVAP:
                            INACFLAG = 1
        if not INACFLAG and not $P(^PS(50.7, PSPOINT, 0), "^", 4):
            WRITE:'PSSCROSS and PSPOINT <= DT, PSSVNAME, "   ", PSSVDOSE, !, "is being marked inactive since no Additives, Solutions, or Dispense Drugs", !, "marked with an 'I', 'O' or 'U' in the Application Package Use field are matched", !, "to it.", !
        if not INACFLAG and not $P(^PS(50.7, PSPOINT, 0), "^", 4):
            PSLATEST = $S(not PSLATEST: DT, 1: PSLATEST)
            $P(^PS(50.7, PSPOINT, 0), "^", 4) = PSLATEST
        SET()
        return ENT()

    def SUP(PSSORDIT):
        # Supply at Orderable Item
        ENT()
        if not ^PS(50.7, PSSORDIT, 0):
            return
        if ^PS(50.7, PSSORDIT, 0)["^", 3:
            NONFORM()
            return ENTZ()
        ZZZ = 0
        while ZZZ:
            ZZZ = $O(^PS(50.7, "A50", PSSORDIT, ZZZ))
            if ZZZ and not PSSQYES:
                if ^PSDRUG(ZZZ, 0)["^", 3)["S":
                    PSSSAP = $P(^PSDRUG(ZZZ, 2), "^", 3)
                    PSSINA = $P(^PSDRUG(ZZZ, "I"), "^")
                    if PSSSAP["O" or PSSSAP["I" or PSSSAP["U" or PSSSAP["X":
                        if not PSSINA:
                            PSSQYES = 1
                            PSSSUYES = 1
                        if PSSINA > DT:
                            PSSQDATE($E(PSSINA, 1, 7)) = ""
                            PSSSUYES = 1
        if not PSSSUP and PSSSUYES:
            $P(^PS(50.7, PSSORDIT, 0), "^", 9) = 1
            WRITE:'PSSCROSS and not PSSSUYES, !!, "The supply indicator is now being set for the Orderable Item", !, $P(^PS(50.7, PSSORDIT, 0), "^") + "   " + $P(^PS(50.606, +$P(^PS(50.7, PSSORDIT, 0), "^", 2), 0), "^"), !
        if PSSSUP and not PSSSUYES:
            $P(^PS(50.7, PSSORDIT, 0), "^", 9) = ""
            WRITE:'PSSCROSS and not PSSSUYES, !!, "The supply indicator is now being removed for the Orderable Item", !, $P(^PS(50.7, PSSORDIT, 0), "^") + "   " + $P(^PS(50.606, +$P(^PS(50.7, PSSORDIT, 0), "^", 2), 0), "^"), !
        if not PSSQYES and PSSSUYES and $O(PSSQDATE(0)):
            ZZZZ = 0
            while ZZZZ:
                ZZZZ = $O(PSSQDATE(ZZZZ))
                if ZZZZ:
                    ZTRTN = "ENT^PSSPOIDT"
                    ZTIO = ""
                    ZTDTH = ZZZZ_.01
                    ZTDESC = "Supply update for Orderable Item"
                    ZTSAVE("PSSORDIT") = ""
                    HLDCROSS = PSSCROSS
                    PSSCROSS = 1
                    ZTSAVE("PSSCROSS") = ""
                    ^%ZTLOAD()
                    if not HLDCROSS:
                        PSSCROSS = ""
        ENTZ()
        if PSSCROSS:
            EN2^PSSHL1(PSSORDIT, "MUP")
        if ZTQUEUED:
            ZTREQ = "@"

    def SET():
        PSSORDIT = PSPOINT
        return

    def REST(PSSREST):
        ASKQ()
        return

    def ASKQ():
        WRITE ! 
        DIR("A", 1) = "Do you want to " + $S(PSINORDE = "I": "inactivate", 1: "reactivate") + " all Drugs/Additives/Solutions"
        DIR("A") = "that are matched to this Orderable Item?"
        DIR(0) = "SB^Y:YES;N:NO;L:LIST ALL DRUGS/ADDITIVES/SOLUTIONS"
        DIR("B") = "N"
        ^DIR()
        if Y = "L":
            LDISThing()
            if not $G(PSSCXXX) and not $G(PSSCOUT):
                WRITE !!, "Nothing matched to this Orderable Item.", !
            if not $G(PSSCXXX) and not $G(PSSCOUT):
                QREST()
            K PSSCXXX, PSSCOUT
        if Y = "Y":
            WRITE !, "Please wait..", !
            if $G(PSINORDE) = "I":
                PSIDATEX = $P($G(^PS(50.7, PSSREST, 0)), "^", 4)
                if PSIDATEX:
                    II = 0
                    while II:
                        II = $O(^PS(52.7, "AOI", PSSREST, II))
                        if II and ^PS(52.7, II, 0):
                            $P(^PS(52.7, II, "I"), "^") = PSIDATEX
                    II = 0
                    while II:
                        II = $O(^PS(52.6, "AOI", PSSREST, II))
                        if II and ^PS(52.6, II, 0):
                            $P(^PS(52.6, II, "I"), "^") = PSIDATEX
            if $G(PSINORDE) = "D":
                II = 0
                while II:
                    II = $O(^PS(52.7, "AOI", PSSREST, II))
                    if II and ^PS(52.7, II, 0) and $P($G(^("I")), "^"):
                        $P(^PS(52.7, II, "I"), "^") = ""
                II = 0
                while II:
                    II = $O(^PS(52.6, "AOI", PSSREST, II))
                    if II and ^PS(52.6, II, 0) and $P($G(^("I")), "^"):
                        $P(^PS(52.6, II, "I"), "^") = ""
            K DA, DIE, DR
        K II, PSIDATEX
        QREST()
        K PSSCXXX, PSSCOUT
        return

    def LDISThing():
        FLAG = 1
        PSSCFLAG = 0
        for ZZ in range(100000):
            if not ZZ:
                ZZ = $O(^PSDRUG("ASP", PSSREST, ZZ))
            if not ZZ or $G(PSSCOUT):
                break
            FLAG = 0
            if ($Y + 5) > IOSL:
                DHEAD()
            if ZZ:
                PSSCXXX = 1
                WRITE $P(^PSDRUG(ZZ, 0), "^")
                DTE()
        if not $G(PSSCOUT):
            FLAG = 0
            PSSCFLAG = 0
            for ZZ in range(100000):
                if not ZZ:
                    ZZ = $O(^PS(52.6, "AOI", PSSREST, ZZ))
                if not ZZ or $G(PSSCOUT):
                    break
                if ($Y + 5) > IOSL:
                    DHEAD()
                if ZZ:
                    PSSCFLAG = 1
                    PSSCXXX = 1
                    WRITE $P(^PS(52.6, ZZ, 0), "^"), ?42, "(A)"
                    PSSCDATE = $P(^PS(52.6, ZZ, "I"), "^")
                    if PSSCDATE:
                        DTEX()
        if not $G(PSSCOUT):
            for ZZ in range(100000):
                if not ZZ:
                    ZZ = $O(^PS(52.7, "AOI", PSSREST, ZZ))
                if not ZZ or $G(PSSCOUT):
                    break
                if ($Y + 5) > IOSL:
                    DHEAD()
                if ZZ:
                    WRITE $P(^PS(52.7, ZZ, 0), "^"), ?31, $P(^(0), "^", 3), ?42, "(S)"
                    PSSCDATE = $P(^PS(52.7, ZZ, "I"), "^")
                    if PSSCDATE:
                        DTEX()
        return

    def DHEAD():
        if not FLAG:
            WRITE ! 
            DIR(0) = "E"
            DIR("A") = "Press RETURN to continue"
            ^DIR()
            if not Y:
                PSSCOUT = 1
                return
        WRITE @IOF, !, ?6, "Orderable Item ->  ", $P($G(^PS(50.7, PSSREST, 0)), "^"), !, ?6, "Dosage Form    ->  ", $P($G(^PS(50.606, +$P($G(^PS(50.7, PSSREST, 0)), "^", 2), 0)), "^"), !!, "Dispense Drugs:"_$S(not FLAG:" (continued)", 1:""), !, "---------------"
        return

    def DTE():
        if $D(^PSDRUG(ZZ, "I")):
            Y = $P(^PSDRUG(ZZ, "I"), "^")
            D ^%DT
            WRITE ?50, Y
        return

    def DTEX():
        Y = PSSCDATE
        D ^%DT
        WRITE ?50, Y
        return

    def NONFORM():
        # formulary status of Orderable Item
        if not PSSORDIT:
            return
        PSNFX1 = 0
        PSNFX2 = 0
        PSNFXB = $P($G(^PS(50.7, PSSORDIT, 0)), "^", 12)
        PSNFX = 0
        while PSNFX:
            PSNFX = $O(^PS(50.7, "A50", PSSORDIT, PSNFX))
            if PSNFX:
                if $P($G(^PSDRUG(PSNFX, 2)), "^", 3)["O" or $P($G(^(2)), "^", 3)["I" or $P($G(^(2)), "^", 3)["U" or $P($G(^(2)), "^", 3)["X":
                    if $P($G(^PSDRUG(PSNFX, "I")), "^") and $P($G(^("I")), "^") <= DT:
                        if $P($G(^PSDRUG(PSNFX, 0)), "^", 9) = 1:
                            PSNFX1 = 1
                        else:
                            PSNFX2 = 1
        if PSNFX1 and not PSNFX2:
            $P(^PS(50.7, PSSORDIT, 0), "^", 12) = 1
        if PSNFX2:
            $P(^PS(50.7, PSSORDIT, 0), "^", 12) = ""
        if $P($G(^PS(50.7, PSSORDIT, 0)), "^", 12) != PSNFXB and not PSSCROSS:
            WRITE !!, "The Formulary Status of the Pharmacy Orderable Item", !, $P($G(^PS(50.7, PSSORDIT, 0)), "^") + "  " + $P($G(^PS(50.606, +$P($G(^(0)), "^", 2), 0)), "^"), !, "has been changed to " + $S($P($G(^PS(50.7, PSSORDIT, 0)), "^", 12): "Non-Formulary.", 1: "Formulary."), !
        return

    def MSSG():
        if not PSSCROSS:
            WRITE !!, "This Orderable Item is " + $S($P($G(^PS(50.7, PSSORDIT, 0)), "^", 12): "Non-Formulary.", 1: "Formulary."), !
        return

    def NONVA():
        # Evaluates the Non-VA Med Indicator of the Orderable Item
        if not PSSORDIT:
            return
        PSNVADG = 0
        PSNONVA = $P($G(^PS(50.7, PSSORDIT, 0)), "^", 10)
        PSDRG = 0
        while PSDRG:
            PSDRG = $O(^PS(50.7, "A50", PSSORDIT, PSDRG))
            if PSDRG and not PSNVADG:
                if $P($G(^PSDRUG(PSDRG, "I")), "^") and $P($G(^("I")), "^") <= DT:
                    if $P($G(^PSDRUG(PSDRG, 2)), "^", 3)["X":
                        PSNVADG = 1
        if PSNVADG:
            $P(^PS(50.7, PSSORDIT, 0), "^", 10) = 1
        if not PSNVADG:
            $P(^PS(50.7, PSSORDIT, 0), "^", 10) = ""
        if +$P($G(^PS(50.7, PSSORDIT, 0)), "^", 10) != +PSNONVA and not PSSCROSS:
            WRITE !!, "The Pharmacy Orderable Item ", $P($G(^PS(50.7, PSSORDIT, 0)), "^"), !, "is ", $S(not PSNONVA: "now", 1: "no longer") + " marked as a NON-VA MED Drug."
        return

    EN(PSPOINT)