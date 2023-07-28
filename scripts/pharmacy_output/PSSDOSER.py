def PSSDOSER():
    # BIR/RTR-Dose edit option
    # 21 Sep 2015  8:37 PM
    # 1.0;PHARMACY DATA MANAGEMENT;**34,38,50,57,47,68,82,125,129,144,155,194**;9/30/97;Build 9
    # Reference to ^PS(50.607 supported by DBIA #2221
    # Reference to ^PS(59 supported by DBIA #1976

    # have an entry point for NDF to call when rematching
    def DOS():
        CHECK_PSSUTLPR()
        if PSSNOCON:
            del PSSNOCON
            END()
            return
        END()
        print("\n")
        DIC(0) = "QEAMZ"
        DIC("A") = "Select Drug: "
        DIC = "^PSDRUG("
        Y = DIC()
        if Y<1 or DTOUT in globals() or DUOUT in globals():
            END()
            print("\n")
            return
        PSSIEN = Y
        PSSNAME = $P($G(^PSDRUG(PSSIEN,0)),"^")
        PSSIND = $P($G(^("I")),"^")
        PSSNFID = $P($G(^(0)),"^",9)
        PSSPKG = $P($G(^PSDRUG(PSSIEN,2)),"^",3)
        print("\n")
        print("This entry is marked for the following PHARMACY packages:")
        if "O" in PSSPKG:
            print("Outpatient")
        if "U" in PSSPKG:
            print("Unit Dose")
        if "I" in PSSPKG:
            print("IV")
        if "W" in PSSPKG:
            print("Ward Stock")
        if "N" in PSSPKG:
            print("Controlled Substances")
        if "X" in PSSPKG:
            print("Non-VA Med")
        if "O" not in PSSPKG and "U" not in PSSPKG and "I" not in PSSPKG and "W" not in PSSPKG and "N" not in PSSPKG and "X" not in PSSPKG:
            print(" (none)")
        del PSSPKG
        L = +^PSDRUG(PSSIEN)
        if not L:
            print("\n")
            print(chr(7))
            print("Another person is editing this drug.")
            print("\n")
            DIR(0) = "E"
            DIR("A") = "Press Return to continue"
            DIR()
            if Y in globals():
                del Y
            DOS()
            return
        print("\n")
        print(PSSNAME, end="")
        if PSSNFID:
            print("    *N/F*", end="")
        print(" "*(52 - len(PSSNAME)), end="")
        print("Inactive Date: ", end="")
        if PSSIND:
            print(PSSIND[4:6] + "/" + PSSIND[6:8] + "/" + PSSIND[2:4])
        else:
            print("")
        PSSIZZ = 0
        PSSOZZ = 0
        PSSSKIPP = 0
        RES()
        if PSSST == "" and ^PSDRUG(PSSIEN,"DOS1") in globals():
            del ^PSDRUG(PSSIEN,"DOS")
            del ^PSDRUG(PSSIEN,"DOS1")
        PSSXYZ = 0
        CHECK()
        if PSSXYZ and PSSUPRA == "NN":
            MPD()
            if PSSZ in globals():
                del PSSZ
            return
        if PSSST in globals():
            XNWS()
        if PSSST in globals() and ^PSDRUG(PSSIEN,"DOS1") in globals():
            STR()
        if PSSXYZ and not ^PSDRUG(PSSIEN,"DOS1") in globals():
            DIR(0) = "Y"
            DIR("B") = "N"
            DIR("A") = "Create Possible Dosages for this drug"
            DIR("?") = " "
            DIR("?",1) = "This drug meets the criteria to have Possible Dosages, but it currently does"
            DIR("?",2) = "not have any. If you answer 'YES', Possible Dosages will be created for this"
            DIR("?",3) = "drug, based on the match to the National Drug File."
            print("\n\n")
            print("This drug can have Possible Dosages, but currently does not have any.")
            if PSSUPRA == "N":
                print("This drug has been set within the National Drug File to ", end="")
                if PSSUPRA == "NN":
                    print("not ", end="")
                print("auto create ", end="")
                if PSSUPRA == "NO":
                    print("only one ", end="")
                if PSSUPRA == "NB":
                    print("two ", end="")
                print("possible dosage", end="")
                if PSSUPRA == "NO":
                    print(".", end="")
                else:
                    print("s.", end="")
                print("")
            print("")
            DIR()
            if Y == 1:
                PSSSKIPP = 1
                EN2^PSSUTIL(PSSIEN, 1)
                RES()
                return
        del PSSZ
        if not ^PSDRUG(PSSIEN,"DOS1") in globals():
            LOCX()
        else:
            DOSA()
        return

    def DOSA():
        PSSST = ^PSDRUG(PSSIEN,"DOS")
        print("\n")
        print("Strength => ", end="")
        if $E(PSSST,1) == ".":
            print("0", end="")
        print(PSSST, end="")
        print("   Unit => ", end="")
        if $P(^PS(50.607,+PSSUN,0),"^") not in globals():
            print($P(^PS(50.607,+PSSUN,0),"^"), end="")
        print("\n")
        if PSSUPRA == "N" and not PSSSKIPP and not PSSZ:
            PSSZ = 1
            print("\n")
            print("This drug has been set within the National Drug File to ", end="")
            if PSSUPRA == "NN":
                print("not ", end="")
            print("auto create ", end="")
            if PSSUPRA == "NO":
                print("only one ", end="")
            if PSSUPRA == "NB":
                print("two ", end="")
            print("possible dosage", end="")
            if PSSUPRA == "NO":
                print(".", end="")
            else:
                print("s.", end="")
            print("")
        DIC() = "^PSDRUG("_PSSIEN_",""DOS1"","
        DIC(0) = "QEAMLZ"
        DLAYGO = 50
        DIC("A") = "Select DISPENSE UNITS PER DOSE: "
        Y = DIC()
        if Y<1 or DTOUT in globals() or DUOUT in globals():
            DOSLOC()
            return
        PSSDOSA = Y
        PSSOTH = 1 if $P(^PS(59.7,1,40.2),"^") else 0
        print("\n")
        DIE() = "^PSDRUG("_PSSIEN_",""DOS1"","
        DA = PSSDOSA
        DR = ".01;S:'$G(PSSOTH) Y=""@1"";2"
        DIE()
        BCMA()
        if Y in globals() or DTOUT in globals():
            DOSLOC()
            return
        DOSA()
        return

    def DOSLOC():
        PSSPCI = 0
        PSSPCO = 0
        PSSPCZ = 0
        while True:
            PSSPCZ = $O(^PSDRUG(PSSIEN,"DOS1",PSSPCZ))
            if not PSSPCZ:
                break
            if $P(^PSDRUG(PSSIEN,"DOS1",PSSPCZ,0),"^",2) not in globals():
                if $P(^PSDRUG(PSSIEN,"DOS1",PSSPCZ,0),"^",3) in ["I", "O"]:
                    PSSPCI = 1
                if $P(^PSDRUG(PSSIEN,"DOS1",PSSPCZ,0),"^",3) in ["O"]:
                    PSSPCO = 1
        if PSSPCI and PSSPCO:
            DIR(0) = "Y"
            DIR("B") = "N"
            DIR("A") = "Enter/Edit Local Possible Dosages"
            DIR("?") = " "
            DIR("?",1) = "Possible Dosages exist for both Outpatient Pharmacy and Inpatient Medications."
            DIR("?",2) = "Local Possible Dosages can be added, but will not be displayed for selection"
            DIR("?",3) = "as long as there are Possible Dosages."
            DIR("?",4) = " "
            DIR("?",5) = "Enter 'Y' to Enter/Edit Local Possible Dosages."
            DIR()
            if Y != 1:
                del PSSPCI
                del PSSPCO
                del PSSPCZ
                ULK()
                DOS()
                return
        del PSSPCI
        del PSSPCO
        del PSSPCZ
        LOC()
        return

    def STR():
        # Edit strength
        PSSIENS = ""
        print("\n")
        print("Strength from National Drug File match => ", end="")
        if $E($G(PSSNATST),1) == ".":
            print("0", end="")
        print(PSSNATST, end="")
        print("    ", end="")
        print($P($G(^PS(50.607,+$G(PSSUN),0)),"^"), end="")
        print("\n")
        print("Strength currently in the Drug File    => ", end="")
        if $E($P($G(^PSDRUG(PSSIEN,"DOS")),"^"),1) == ".":
            print("0", end="")
        print($P($G(^PSDRUG(PSSIEN,"DOS")),"^"), end="")
        print("    ", end="")
        print($S($P($G(^PS(50.607,+$G(PSSUN),0)),"^") not in globals(): $P($G(^(0)),"^"), 1: ""), end="")
        MS^PSSDSPOP()
        print("\n")
        DIR(0) = "Y"
        DIR("?") = "Changing the strength will update all possible dosages for this Drug"
        DIR("B") = "NO"
        DIR("A") = "Edit Strength"
        DIR()
        if not Y:
            return
        print("\n")
        print("Changing the strength will not change the concentration.")
        DIR(0) = "Y"
        DIR("?") = "Changes in strength do not cause changes in concentration."
        DIR("B") = "NO"
        DIR("A") = "Are you sure you need to change the strength"
        DIR()
        if not Y:
            return
        print("\n")
        DIE() = "^PSDRUG("
        DA = PSSIEN
        DR = 901
        DIE()
        print("\n")
        if $P($G(^PSDRUG(PSSIEN,"DOS")),"^") == "":
            del ^PSDRUG(PSSIEN,"DOS")
            del ^PSDRUG(PSSIEN,"DOS1")
            print("Deleting Strength has deleted all Possible Dosages!")
            print("\n")
        return

    def CHECK():
        del PSSNAT
        del PSSNATND
        del PSSNATDF
        del PSSNATUN
        del PSSNATST
        del PSSIZZ
        del PSSOZZ
        PSSNAT = +$P($G(^PSDRUG(PSSIEN,"ND")),"^",3)
        PSSNAT1 = $P($G(^("ND")),"^")
        if not PSSNAT or not PSSNAT1:
            return
        PSSNATND = $$DFSU^PSNAPIS(PSSNAT1,PSSNAT)
        PSSNATDF = $P(PSSNATND,"^")
        PSSNATST = $P(PSSNATND,"^",4)
        PSSNATUN = $P(PSSNATND,"^",5)
        PSSUPRA = $$SUPRA^PSSUTIL3(PSSNAT)
        if not PSSNATDF or not PSSNATUN or not PSSNATST:
            return
        if PSSNATST not in globals() or (PSSNATST not in globals() and PSSNATST != "."):
            return
        if not ^PS(50.606,PSSNATDF,0) or not ^PS(50.607,PSSNATUN,0):
            return
        if PSSNATST != "" and (PSSNATST not in globals() and PSSNATST != "."):
            return
        if ^PS(50.606,"ACONI",PSSNATDF,PSSNATUN) and $O(^PS(50.606,"ADUPI",PSSNATDF)):
            PSSXYZ = 1
            PSSIZZ = 1
        if ^PS(50.606,"ACONO",PSSNATDF,PSSNATUN) and $O(^PS(50.606,"ADUPO",PSSNATDF)):
            PSSXYZ = 1
            PSSOZZ = 1
        return

    def END():
        del PSSIZZ
        del PSSOZZ
        del PSSSKIPP
        del PSSNFID
        del PSSNAT
        del PSSNAT1
        del PSSNATND
        del PSSNATDF
        del PSSNATUN
        del PSSNOCON
        del PSSST
        del PSSUN
        del PSSIEN
        del PSSNAME
        del PSSIND
        del PSSDOSA
        del PSSXYZ
        del PSSNATST
        return

    def ULK():
        if not PSSIEN:
            return
        XX = ""
        if not $G(PSSHUIDG):
            DRG^PSSHUIDG(PSSIEN)
            XX = 0
            while True:
                XX = $O(^PS(59,XX))
                if not XX:
                    break
                DVER = $$GET1^DIQ(59,XX_",",105,"I")
                DMFU = $$GET1^DIQ(59,XX_",",105.2)
                if DVER == "2.4":
                    DNSNAM = $$GET1^DIQ(59,XX_",",2006)
                    DNSPORT = $$GET1^DIQ(59,XX_",",2007)
                    if DNSNAM != "" and DMFU == "YES":
                        DRG^PSSDGUPD(PSSIEN,"",DNSNAM,DNSPORT)
        L = -^PSDRUG(PSSIEN)
        return

    def BCMA():
        if $P($G(^PSDRUG(PSSIEN,2)),"^",3) not in ["I", "U"]:
            return
        if $P($G(^PSDRUG(PSSIEN,"DOS1",PSSDOSA,0)),"^",3) not in ["I"]:
            return
        DIE() = "^PSDRUG("_PSSIEN_",""DOS1"","
        DA = PSSDOSA
        DR = 3
        DIE()
        return

    def BCMA1():
        if $P($G(^PSDRUG(PSSIEN,2)),"^",3) not in ["I", "U"]:
            return
        if $P($G(^PSDRUG(PSSIEN,"DOS2",PSSDOSA,0)),"^",2) not in ["I"]:
            return
        DIE() = "^PSDRUG("_PSSIEN_",""DOS2"","
        DA = PSSDOSA
        DR = 2
        DIE()
        return

    def STUN():
        PSSST = $P($G(^PSDRUG(PSSIEN,"DOS")),"^")
        PSSUN = $P($G(^("DOS")),"^",2)
        return

    def NATND():
        PSSNAT = +$P($G(^PSDRUG(PSSIEN,"ND")),"^",3)
        PSSNAT1 = $P($G(^("ND")),"^")
        PSSNATND = $$DFSU^PSNAPIS(PSSNAT1,PSSNAT)
        PSSNATDF = $P(PSSNATND,"^")
        PSSNATST = $P(PSSNATND,"^",4)
        PSSNATUN = $P(PSSNATND,"^",5)
        return

    def PR():
        if PSSST != "" or PSSNATST != "":
            if PSSUN or PSSNATUN:
                print("\n")
                print("Strength: ", end="")
                if $E($S(PSSST != "":PSSST, 1:PSSNATST),1) == ".":
                    print("0", end="")
                print($S(PSSST != "":PSSST, 1:PSSNATST), end="")
                print("   Unit: ", end="")
                if $P($G(^PS(50.607,+$S(PSSUN:PSSUN,1:PSSNATUN),0)),"^") not in globals():
                    print($P($G(^PS(50.607,+$S(PSSUN:PSSUN,1:PSSNATUN),0)),"^"), end="")
                print("")
            else:
                print("\n")
                print("Strength: ", end="")
                print(" "*30, end="")
                print("Unit: ", end="")
                print("")
        else:
            print("\n")
            print("Strength: ", end="")
            print(" "*30, end="")
            print("Unit: ", end="")
            print("")
        return

    def XNWS():
        print("\n")
        print("Strength from National Drug File match => ", end="")
        if $E($G(PSSNATST),1) == ".":
            print("0", end="")
        print(PSSNATST, end="")
        print("    ", end="")
        print($P($G(^PS(50.607,+$G(PSSUN),0)),"^"), end="")
        print("\n")
        print("Strength currently in the Drug File    => ", end="")
        if $E($P($G(^PSDRUG(PSSIEN,"DOS")),"^"),1) == ".":
            print("0", end="")
        print($P($G(^PSDRUG(PSSIEN,"DOS")),"^"), end="")
        print("    ", end="")
        print($S($P($G(^PS(50.607,+$G(PSSUN),0)),"^") not in globals(): $P($G(^(0)),"^"), 1: ""), end="")
        MS^PSSDSPOP()
        del PSSDESTP
        return

    def MPD():
        if $P($G(^PSDRUG(PSSIEN,"DOS")),"^") == "":
            if $P(^PSDRUG(PSSIEN,"ND"),"^",2) != "":
                ^PSDRUG(PSSIEN,"DOS") = PSSNATST_"^"_PSSNATUN
        if PSSXYZ and not ^PSDRUG(PSSIEN,"DOS1") in globals():
            DIR(0) = "Y"
            DIR("B") = "N"
            DIR("A") = "Do you want to manually enter possible dosages"
            DIR("?") = " "
            DIR("?",1) = "This drug meets the criteria to have Possible Dosages, but it currently does"
            DIR("?",2) = "not have any. If you answer 'YES', Possible Dosages can be manually entered for this drug."
            print("\n\n")
            print("This drug can have Possible Dosages, but currently does not have any.")
            PSSZ = 1
            print("\n")
            print("This drug has been set within the National Drug File to ", end="")
            if PSSUPRA == "NN":
                print("not ", end="")
            print("auto create ", end="")
            if PSSUPRA == "NO":
                print("only one ", end="")
            if PSSUPRA == "NB":
                print("two ", end="")
            print("possible dosage", end="")
            if PSSUPRA == "NO":
                print(".", end="")
            else:
                print("s.", end="")
            print("")
        XNWS()
        STR()
        DOSA()
        return

    DOS()

PSSDOSER()