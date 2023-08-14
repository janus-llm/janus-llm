def PSSTRENG():
    # BIR/RTR-Mismatch Strength Report
    # 06/28/07
    # 1.0;PHARMACY DATA MANAGEMENT;**129**;9/30/97;Build 67
    # Reference to ^PS(50.607 supported by DBIA 2221
    
    def DEV():
        nonlocal IOP, %ZIS, POP, ZTRTN, ZTDESC, ZTSK, DUOUT, DTOUT, DIRUT, DIROUT, X, Y, DIR
        print("\nThis report will print Dosage information for all entries in the DRUG (#50)")
        print("File that have a different Strength than what is in the VA PRODUCT (#50.68)")
        print("File match. If these drugs have Local Possible Dosages, you need to be careful")
        print("when populating the new Dose Unit and Numeric Dose fields to be used for Dosage")
        print("checks, because the Dosage check will be based on the VA Product. This report")
        print("can only identify Strength mismatches if the Drug qualifies for Possible")
        print("Dosages, and a Strength has been defined in the DRUG (#50) File.\n")
        print("This report is designed for 132 column format!\n")
        IOP = None
        %ZIS = "QM"
        # ^%ZIS() function call goes here
        if POP > 0:
            IOP = None
            %ZIS = None
            print("\nNothing queued to print.\n")
            DIR(0) = "E"
            DIR("A") = "Press Return to continue"
            # ^DIR() function call goes here
            DIR = None
            return
        if IO("Q"):
            ZTRTN = "START^PSSTRENG"
            ZTDESC = "Mismatch Strength Report"
            # ^%ZTLOAD() function call goes here
            %ZIS = None
            print("\nReport queued to print.\n")
            DIR(0) = "E"
            DIR("A") = "Press Return to continue"
            # ^DIR() function call goes here
            DIR = None
            return
    
    def START():
        nonlocal PSSLINE, PSSYEAR, X, X1, X2, PSSOUT, PSSNAME, PSSCT, PSSIEN, PSSA, PSSB, PSSC, PSSD, PSSDV, PSSE, PSSINA, PSSINAD, PSSSTND1, PSSSTND3, PSSSTNDS, PSSSTNDZ
        nonlocal PSSNF, PSSUNIT, PSSAPU, PSSNODE, PSSMSG, PSSSTR, PSSNWD, PSSNWDN, PSSFOUND, Y, PSSMSXXX, PSSNWDS, PSSNWDSS
        
        X1 = DT
        X2 = -365
        # ^%DTC() function call goes here
        PSSYEAR = X
        X = None
        X1 = None
        X2 = None
        PSSOUT = 0
        PSSFOUND = 0
        PSSDV = "P" if IOST[:2] != "C-" else "C"
        PSSCT = 1
        PSSLINE = "-" * 130
        HD()
        PASS()
    
    def HD():
        nonlocal PSSDV, PSSCT, PSSLINE
        if PSSDV == "C" and PSSCT != 1:
            return
        print("\nMismatched Strength Report", "PAGE:", PSSCT)
        print(PSSLINE)
        PSSCT += 1
    
    def SETD():
        nonlocal PSSVA, PSSVA1, PSSVB, PSSVB1, PSSDASH, PSSNDFS, PSSDASH2, PSSDASH3, PSSDASH4, PSSDASH5, PSSCALC
        PSSDASH = 0
        PSSNDFS = PSNAPIS.PSJST(PSSSTND1, PSSSTND3)
        PSSNDFS = PSSNDFS[1]
        if PSSNDFS and PSSSTR and int(PSSSTR) != int(PSSNDFS):
            PSSDASH = 1
        PSSVA = PSSUNIT.split("/")[0]
        PSSVB = PSSUNIT.split("/")[1]
        PSSVA1 = int(PSSVA)
        PSSVB1 = int(PSSVB)
        if PSSDASH:
            PSSDASH2 = PSSSTR / PSSNDFS
            PSSDASH3 = PSSDASH2 * PSSC
            PSSDASH4 = PSSDASH3 * (PSSVB1 if PSSVB1 else 1)
            PSSDASH5 = PSSDASH4 + PSSVB if not PSSVB1 else PSSDASH4 + PSSVB[PSSVB1:]
        PSSCALC = (PSSD if not PSSVA1 else (PSSVA1 * PSSD)) + "/" + (PSSVA if PSSVA1 else PSSVA) + "/" + (PSSDASH5 if PSSDASH else PSSD)
    
    def OUT():
        nonlocal PSSDFOI, PSSDFOIN, PSSDF, PSSDZZ, PSSDASH, PSSNWD, PSSNWDN, PSSNWDS, PSSNWDSS
        if not PSSE.startswith("O"):
            return
        PSSDFOI = int(PSDRUG.PSSDFOI)
        if not PSSDFOI:
            return
        PSSDF = int(PS.PSSDFOI[1])
        PSSDFOIN = PSS.PSSDF[1]
        if not PSSDF:
            PSSDZ = PSSDFOIN
            PSSDZ = PSSDZ if len(PSSDZ) <= 3 else ""
            return
        for PSSDZZ in PS.PSSDZZ:
            if PSSDZZ[0]:
                PSSDZ = PSSDZZ[0]
                break
        if not PSSDZ:
            PSSDZ = PSSDFOIN
        if PSSC:
            PARN()
        print("%s%s %s %s %s %s" % (("" if PSSC[0] != "." else "0") + PSSC, PSSDZN if PSSDZN else PSSDZ, "" if PSSDZN else PSSNWDN, "" if PSSDZN else PSSNWDS, PSSE[92:]))
        PSSDFOI = None
        PSSDF = None
        PSSDZ = None
        PSSDZZ = None
        PSSDZN = None
        PSSDZNX = None
    
    def PARN():
        nonlocal PSSDZN, PSSDZNX
        if not PSSDZ:
            return
        if len(PSSDZ) <= 3:
            return
        PSSDZNX = PSSDZ[-3:]
        if PSSDZNX == "(S)" or PSSDZNX == "(s)":
            if PSSC <= 1:
                PSSDZN = PSSDZ[:-3]
            if PSSC > 1:
                PSSDZN = PSSDZ[:-3] + PSSDZNX[1:]
    
    def ZERO():
        nonlocal PSSCALC, PSSDFOI, PSSDFOIN, PSSDF, PSSDZ, PSSDZZ
        if PSSCALC[0] == ".":
            PSSCALC = "0" + PSSCALC
        PSSDFOI = int(PSSCALC.split("/.")[0])
        if PSSCALC.count("/.") > 0:
            PSSDFOI = PSSCALC.split("/.")[1]
            PSSDFOI = PSSDFOI.split("/")[0]
            PSSCALC = PSSLEZ + "/0." + PSSLEZ1
    
    def PASS():
        nonlocal PSSNAME, PSSIEN, PSSINA, PSSNF, PSSAPU, PSSNODE, PSSMSG, PSSMSXXX, PSSSTND1, PSSSTND3, PSSSTNDS, PSSSTNDZ, PSSSTR
        nonlocal PSSUNIT, PSSFOUND, PSSA, PSSB, PSSC, PSSD, PSSE, PSSINAD
        PSSNAME = ""
        while PSSNAME != "" and not PSSOUT:
            PSSIEN = 0
            while PSSIEN != 0 and not PSSOUT:
                if not PSSDRUG.B[PSSNAME]:
                    continue
                PSSINA = PSSDRUG.PSSIEN["I"]
                PSSNF = 1 if PSSDRUG.PSSIEN[0][9] else 0
                PSSNODE = PSSDRUG.PSSIEN["DOS"]
                PSSMSXXX = PSSNODE[0]
                if not PSSMSXXX:
                    continue
                PSSSTND1 = PSSDRUG.PSSIEN["ND"]
                PSSSTND3 = PSSDRUG.PSSIEN["ND"][3]
                if not PSSSTND3 or not PSSSTND1:
                    continue
                PSSSTNDZ = PSNAPIS.PROD0(PSSSTND1, PSSSTND3)
                PSSSTNDS = PSSSTNDZ[3]
                if not PSSSTNDS:
                    continue
                if PSSSTNDS == PSSMSXXX:
                    continue
                PSSFOUND = 1
                PSSMSG = PSSDRUG.PSSIEN[0][10]
                PSSAPU = PSSDRUG.PSSIEN[2][3]
                if PSSINA:
                    PSSINAD = PSSINA[3:5] + "/" + PSSINA[5:7] + "/" + PSSINA[2:4]
                PSSUNIT = PSSDRUG.PSSIEN["DOS"][2]
                print("\n(%s) %s%s%s%s" % (PSSIEN, PSSNAME, "    *N/F*" if PSSNF else "", "    Inactive Date: " + PSSINAD if PSSINA else ""))
                if (PSSY + 5) > IOSL:
                    HD()
                    if PSSOUT:
                        return
                if PSSMSG:
                    print("%s%s" % (" " * 12, PSSMSG))
                if (PSSY + 5) > IOSL:
                    HD()
                    if PSSOUT:
                        return
                print("%s%s%s" % (" " * 12, "Strength: " + PSSMSXXX, " " * 43))
                if PSSUNIT != "" and len(PSSUNIT) > 15:
                    print()
                print(" " * 66 + "Application Package: " + PSSAPU)
                if (PSSY + 5) > IOSL:
                    HD()
                    if PSSOUT:
                        return
                PSSA = 0
                PSSC = None
                PSSD = None
                PSSE = None
                print(" " * 4 + "Possible Dosages: ", end="")
                while PSSB != 0 and not PSSOUT:
                    if PSSC and PSSD:
                        PSSA = 1
                        if (PSSY + 5) > IOSL:
                            HD()
                            if PSSOUT:
                                return
                        print(" " * 3 + "Dispense Units Per Dose: " + ("0" if PSSC[0] == "." else "") + PSSC + " " * 44 + "Dose: ", end="")
                        if PSSUNIT != "/":
                            print(("0" if PSSD[0] == "." else "") + PSSD + PSSUNIT, end="")
                            print(" " * 78 + "Package: " + PSSE)
                            OUT()
                    PSSB += 1
                if not PSSA:
                    print("(None)")
                PSSA = 0
                print(" " * 4 + "Local Possible Dosages: ", end="")
                while PSSB != 0 and not PSSOUT:
                    if PSSDRUG.PSSIEN["DOS2"][PSSB][0]:
                        PSSA = 1
                        if (PSSY + 5) > IOSL:
                            HD()
                            if PSSOUT:
                                return
                        PSSNWD = PSSDRUG.PSSIEN["DOS2"][PSSB][5]
                        if PSSNWD:
                            PSSNWDN = PSSNWD[51.24][0]
                        print(" " * 6 + PSSDRUG.PSSIEN["DOS2"][PSSB][0])
                        if (PSSY + 5) > IOSL:
                            HD()
                            if PSSOUT:
                                return
                        PSSNWDS = PSSDRUG.PSSIEN["DOS2"][PSSB][6]
                        PSSNWDSS = PSSNWDS if PSSNWDS[0] != "." else "0" + PSSNWDS
                        print(" " * 6 + "Numeric Dose: " + PSSNWDSS + " " * 46 + "Dose Unit: " + PSSNWDN + " " * 92 + "Package: " + PSSDRUG.PSSIEN["DOS2"][PSSB][2])
                        if (PSSY + 5) > IOSL:
                            HD()
                            if PSSOUT:
                                return
                    PSSB += 1
                if not PSSA:
                    print("(None)")
                if (PSSY + 5) > IOSL:
                    HD()
                    if PSSOUT:
                        return
                print(" " * 3 + "Note: Strength of " + PSSMSXXX + " does not match NDF strength of " + PSSSTNDS + ".")
                if (PSSY + 5) > IOSL:
                    HD()
                    if PSSOUT:
                        return
                print(" " * 3 + "VA PRODUCT MATCH: " + PSSSTNDZ[0])
                if (PSSY + 5) > IOSL:
                    HD()
                    if PSSOUT:
                        return
    
    PSSYEAR = None
    PSSOUT = None
    PSSDV = None
    PSSCT = None
    PSSLINE = None
    PSSNAME = None
    PSSIEN = None
    PSSINA = None
    PSSNF = None
    PSSINAD = None
    PSSNODE = None
    PSSMSG = None
    PSSMSXXX = None
    PSSSTND1 = None
    PSSSTND3 = None
    PSSSTNDS = None
    PSSSTNDZ = None
    PSSUNIT = None
    PSSAPU = None
    PSSA = None
    PSSB = None
    PSSC = None
    PSSD = None
    PSSE = None
    PSSNWD = None
    PSSNWDN = None
    PSSFOUND = None
    Y = None
    PSSMSXXX = None
    PSSNWDS = None
    PSSNWDSS = None
    
    X = DT
    X1 = X
    X2 = -365
    # ^%DTC() function call goes here
    PSSYEAR = X
    X = None
    X1 = None
    X2 = None
    PSSOUT = 0
    PSSFOUND = 0
    PSSDV = "P" if IOST[:2] != "C-" else "C"
    PSSCT = 1
    PSSLINE = "-" * 130
    HD()
    PASS()
    
    if not PSSOUT and not PSSFOUND:
        print("\nNo mismatches found.")
    
    if PSSDV == "P":
        print("\nEnd of Report.")
    
    if not PSSOUT and PSSDV == "C":
        DIR(0) = "E"
        DIR("A") = "Press Return to continue"
        # ^DIR() function call goes here
        DIR = None
    
    if PSSDV == "C":
        print()
    else:
        print("\f")
    
    PSSCALC = None
    PSSDFOI = None
    PSSDFOIN = None
    PSSDF = None
    PSSDZZ = None
    PSSDASH = None
    PSSNWD = None
    PSSNWDN = None
    PSSNWDS = None
    PSSNWDSS = None
    PSSLEZ = None
    PSSLEZ1 = None
    PSSLEZD = None
    PSSDZ = None
    PSSDZN = None
    PSSDZNX = None
    PSSDFOIN = None
    PSSDFOI = None
    PSSDF = None
    PSSDZ = None
    PSSDZZ = None
    PSSDZN = None
    
    # ^%ZISC() function call goes here
    if ZTQUEUED:
        ZTREQ = "@"