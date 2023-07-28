def PSSLDEDT():
    # BIR/RTR-Edit Local Possible Dosage Unit/Dosage ;06/23/07
     #1.0;PHARMACY DATA MANAGEMENT;**129**;9/30/07;Build 67
    #
    #Reference to 50.607 supported by DBIA 2221
    
    def EDT():
        nonlocal PSSLVIEN, PSSLVOK, PSSLVTST, PSSLVZR, PSSLVND1, PSSLVND3, PSSLVDF, PSSLVSTN, PSSLVUNT, PSSLVNDF, PSSLVSXX, PSSLVSZZ, PSSLVUNX, PSSLVLP, PSSLVLPN, PSSLVOUT, PSSLVLOC, PSSLVLCX, PSSLVFLG, PSSLVCNT
        nonlocal PSSLVGG1, PSSLVGG2, PSSLVGG3, PSSLVGG4, PSSLVGG5, PSSLVGG6, PSSLVAF6, PSSLVBF6, DIR, DIDEL
        EDTX = lambda: None
        
        PSSLVIEN = None
        PSSLVOK = None
        PSSLVTST = None
        PSSLVZR = None
        PSSLVND1 = None
        PSSLVND3 = None
        PSSLVDF = None
        PSSLVSTN = None
        PSSLVUNT = None
        PSSLVNDF = None
        PSSLVSXX = None
        PSSLVSZZ = None
        PSSLVUNX = None
        PSSLVLP = None
        PSSLVLPN = None
        PSSLVOUT = None
        PSSLVLOC = None
        PSSLVLCX = None
        PSSLVFLG = None
        PSSLVCNT = None
        PSSLVGG1 = None
        PSSLVGG2 = None
        PSSLVGG3 = None
        PSSLVGG4 = None
        PSSLVGG5 = None
        PSSLVGG6 = None
        PSSLVAF6 = None
        PSSLVBF6 = None
        
        PSSLVOUT = 0
        print()
        DIC = 50
        DIC(0) = "QEAMZ"
        DIC("A") = "Select Drug: "
        DIC_result = DIC
        PSSLVIEN = DIC_result
        if DTOUT or DUOUT or not PSSLVIEN > 0:
            print()
            return
        PSSLVZR = PS(50)(PSSLVIEN, 0)
        PSSLVND1 = PS(50)(PSSLVIEN, "ND")[0]
        PSSLVND3 = PS(50)(PSSLVIEN, "ND")[2]
        PSSLVSTN = PS(50)(PSSLVIEN, "DOS")[0]
        PSSLVUNT = PS(50)(PSSLVIEN, "DOS")[1]
        PSSLVOK = TEST(PSSLVIEN)
        if not PSSLVOK:
            EDTX()
            return
        PSSLVUNX = PSSLVUNT if PSSLVUNT else PS(50.607)(int(PSSLVNDF[5])) if PSSLVNDF[5] != "" else ""
        if not PSSLVND3 or not PSSLVND1:
            print()
            print("This drug is not matched to NDF and therefore will be excluded from dosing")
            print("checks.")
            return
        if PSSLVSTN != "" and PSSLVSTN[0] == ".":
            PSSLVSTN = "0" + PSSLVSTN
        if PSSLVSXX != "" and PSSLVSXX[0] == ".":
            PSSLVSXX = "0" + PSSLVSXX
        PSSLVFLG = 0
        if PSSLVSXX != "" and PSSLVSTN != "" and PSSLVSXX != PSSLVSTN:
            PSSLVFLG = 1
            PSSLVGG1 = len(PSSLVSXX)
            PSSLVGG2 = len(PSSLVUNX)
            PSSLVGG3 = len(PSSLVSTN)
            PSSLVGG4 = len(PSSLVUNX) if PSSLVUNX.find("/") == -1 else ""
            print()
            if PSSLVGG1 + PSSLVGG2 < 34:
                print(PSSLVSXX, "   ", PSSLVUNX)
            else:
                print()
                print(PSSLVSXX)
                if PSSLVGG1 + PSSLVGG2 < 73:
                    print("   ", PSSLVUNX)
                else:
                    print()
                    print(PSSLVUNX)
            print()
            print("Strength from National Drug File match => ", end="")
            if PSSLVGG3 + PSSLVGG4 < 34:
                print(PSSLVSTN, "   ", PSSLVUNX)
            else:
                print()
                print(PSSLVSTN)
                if PSSLVGG3 + PSSLVGG4 < 73:
                    print("   ", PSSLVUNX)
                else:
                    print()
                    print(PSSLVUNX)
            print()
            print("Strength currently in the Drug File    => ", end="")
            if PSSLVGG3 + PSSLVGG4 < 34:
                print(PSSLVSTN, "   ", PSSLVUNX)
            else:
                print()
                print(PSSLVSTN)
                if PSSLVGG3 + PSSLVGG4 < 73:
                    print("   ", PSSLVUNX)
                else:
                    print()
                    print(PSSLVUNX)
            print()
            print("Please Note: Strength of drug does not match strength of VA Product it is")
            print("matched to.")
        PSSLVCNT = 0
        PSSLVLP = 0
        while True:
            PSSLVLP = PS(50)(PSSLVIEN, "DOS2", PSSLVLP)
            if not PSSLVLP:
                break
            PSSLVLOC = PS(50)(PSSLVIEN, "DOS2", PSSLVLP, 0)
            if PSSLVLOC[0] != "":
                if not PSSLVCNT and not PSSLVFLG and (PSSLVSXX != "" or PSSLVSTN != "" or PSSLVUNX != ""):
                    PSSLVGG5 = len(PSSLVSTN if PSSLVSTN != "" else PSSLVSXX)
                    PSSLVGG6 = len(PSSLVUNX)
                    print()
                    print("Strength: ", PSSLVSTN if PSSLVSTN != "" else PSSLVSXX)
                    if PSSLVGG5 + PSSLVGG6 < 60:
                        print("   Unit: ", PSSLVUNX)
                    else:
                        print()
                        print("Unit: ", PSSLVUNX)
                PSSLVCNT = 1
                print()
                print(PSSLVLOC[0])
                if PSSLVLOC[4] or PSSLVLOC[5] != "":
                    print("Numeric Dose: ", "0" + PSSLVLOC[5] if PSSLVLOC[5][0] == "." else PSSLVLOC[5], end="")
                    print("   ", "Dose Unit: ", "" if not PSSLVLOC[4] else PS(51.24)(PSSLVLOC[4], 0))
                print()
                DIE = "^PSDRUG(" + str(PSSLVIEN) + ",""DOS2"","
                DR = "4;5"
                DA = PSSLVLP
                DIE_result = DIE
                DR_result = DR
                DA_result = DA
                PS(DIE_result, DR_result, DA_result)
                if DTOUT or Y:
                    print()
                    DIR_0 = "Y"
                    DIR("A") = "Do you want to exit this option"
                    DIR("B") = "Y"
                    DIR("?") = "Enter 'Y' to exit this option, enter 'N' to continue editing."
                    DIR_result = DIR
                    if DTOUT or DUOUT or DIR_result:
                        PSSLVOUT = 1
            PSSLVLCX = PS(50)(PSSLVIEN, "DOS2", PSSLVLP, 0)
            PSSLVBF6 = "0" + PSSLVLOC[5] if PSSLVLOC[5][0] == "." else PSSLVLOC[5]
            PSSLVAF6 = "0" + PSSLVLCX[5] if PSSLVLCX[5][0] == "." else PSSLVLCX[5]
            if PSSLVLCX[4] != PSSLVLOC[4] or PSSLVBF6 != PSSLVAF6:
                print()
                print(PSSLVLCX[0])
                print("Numeric Dose: ", "0" + PSSLVLCX[5] if PSSLVLCX[5][0] == "." else PSSLVLCX[5], end="")
                print("   ", "Dose Unit: ", "" if not PSSLVLCX[4] else PS(51.24)(PSSLVLCX[4], 0))
        UL()
        if not PSSLVOUT:
            EDTX()
        return
    
    def UL():
        nonlocal PSSLVIEN
        L - "^PSDRUG(" + str(PSSLVIEN)
        return
    
    def TEST(PSSLVTST):
        nonlocal PSSLVDOV, PSSLVND1, PSSLVND3, PSSLVNDF, PSSLVDF
        PSSLVDOV = ""
        if PSSLVND1 and PSSLVND3 and "OVRIDE^PSNAPIS" in globals():
            PSSLVDOV = OVRIDE^PSNAPIS(PSSLVND1, PSSLVND3)
        if not PS(50)("DOS2", 0):
            print()
            print("No local possible dosages exist for this drug.")
            return 0
        if PSSLVZR[2].find("S") != -1 or PSSLVZR[1][:2] == "XA":
            print()
            print("This drug is marked as a supply and therefore excluded from dosing checks.")
            print("Population of the numeric dose and dose unit for this drug's local possible")
            print("dosages is not required.")
            return 0
        if PSSLVND1 and PSSLVND3:
            PSSLVNDF = DFSU^PSNAPIS(PSSLVND1, PSSLVND3)
            PSSLVDF = PSSLVNDF[0]
        if PSSLVDF <= 0 and PS(50)(2) and PS(50)(2) != "":
            PSSLVDF = PS(50.7)(int(PS(50)(2)), 0)[1]
        if not PSSLVDOV or not PSSLVDF or PS(50.606)(int(PSSLVDF), 1)[0] == "":
            return 1
        if PS(50.606)(int(PSSLVDF), 1)[0] and not PSSLVDOV:
            print()
            print("The dosage form '", PS(50.606)(int(PSSLVDF), 0), "' associated with the drug has")
            print("been excluded from dosage checks. Population of the numeric dose and dose")
            print("unit for this drug's local possible dosages is not required.")
            return 0
        if not PS(50.606)(int(PSSLVDF), 1)[0] and PSSLVDOV:
            print()
            print("The VA product that this drug is matched to has been excluded from dosage")
            print("checks. Population of the numeric dose and dose unit for this drug's local")
            print("possible dosages is not required.")
            return 0
        return 1
    
    EDT()
    if not PSSLVOUT:
        EDTX()
    return
    
PSSLDEDT()