def PSSLDALL():
    print("This option will find all Local Possible Dosages that are eligible for Dosage")
    print("Checks that do not have either the Numeric Dosage or Dose Unit entered for the")
    print("Local Possible Dosage. This mapping is necessary to perform Dosage checks.")
    print("Searching for local Possible Dosages...")
    PSSGVNMX = ""
    PSSGVOUT = 0
    PSSGVTOT = 0

    while PSSGVNMX != "" and not PSSGVOUT:
        PSSGVNMX = next(iter(PSSGVNMX), "")
        PSSGVIEN = 0
        while PSSGVIEN != 0 and not PSSGVOUT:
            PSSGVIEN = next(iter(PSSGVIEN), 0)
            PSSGVZR = PSSDRUG.get(PSSGVIEN, {}).get("0", "")
            PSSGVND1 = PSSDRUG.get(PSSGVIEN, {}).get("ND", "").get("0", "")
            PSSGVND3 = PSSDRUG.get(PSSGVIEN, {}).get("ND", "").get("3", "")
            PSSGVTOT += 1
            if PSSGVTOT % 20 == 0:
                print(".")
            PSSGVOK = TEST()
            if not PSSGVOK:
                continue
            PSSGVLC2 = 0
            PSSGVLPX = 0
            while PSSGVLPX != 0 and not PSSGVLC2:
                PSSGVLPX = next(iter(PSSGVLPX), 0)
                PSSGVLC1 = PSSDRUG.get(PSSGVIEN, {}).get("DOS2", {}).get(PSSGVLPX, {}).get("0", "")
                if PSSGVLC1 and PSSGVLC1.get("0", "") != "" and (not PSSGVLC1.get("5", "") or PSSGVLC1.get("6", "") == ""):
                    PSSGVLC2 = 1
            if not PSSGVLC2:
                continue

            print("\nDrug: " + PSSGVZR)
            PSSGVSTN = PSSDRUG.get(PSSGVIEN, {}).get("DOS", "").get("0", "")
            PSSGVUNT = PSSDRUG.get(PSSGVIEN, {}).get("DOS", "").get("2", "")
            PSSGVUNX = PSS(50.607, PSSGVUNT, "").get("6", "")
            PSSGVUNX = PSSGVUNX if PSSGVUNX else ""
            if PSSGVIEN not in LOCKED:
                LOCKED.append(PSSGVIEN)
            else:
                print("\nAnother person is editing " + PSSGVZR + "!")
                choice = input("Press Return to Continue")
                if choice != "" or choice == "N":
                    PSSGVOUT = 1
            if PSSGVND1 and PSSGVND3:
                PSSGVSXX = PSSGVNDF.get("4", "")
                PSSGVSZZ = PSSGVNDF.get("6", "")
            if PSSGVSTN != "" and PSSGVSTN[0] == ".":
                PSSGVSTN = "0" + PSSGVSTN
            if PSSGVSXX != "" and PSSGVSXX[0] == ".":
                PSSGVSXX = "0" + PSSGVSXX
            PSSGVFLG = 0
            if PSSGVSXX != "" and PSSGVSTN != "" and PSSGVSXX != PSSGVSTN:
                PSSGVFLG = 1
                PSSGVGG1 = len(PSSGVSXX)
                PSSGVGG2 = len(PSSGVUNX)
                PSSGVGG3 = len(PSSGVSTN)
                PSSGVGG4 = len(PSSGVUNX if "/" not in PSSGVUNX else "")
                if PSSGVGG1 + PSSGVGG2 < 34:
                    print(PSSGVSXX + "   " + PSSGVUNX)
                else:
                    print("\n" + PSSGVSXX)
                    if PSSGVGG1 + PSSGVGG2 < 73:
                        print("   " + PSSGVUNX)
                    else:
                        print("\n" + PSSGVUNX)
                print("\nStrength from National Drug File match => ")
                if PSSGVGG3 + PSSGVGG4 < 34:
                    print(PSSGVSTN + "   " + (PSSGVUNX if "/" not in PSSGVUNX else ""))
                else:
                    print("\n" + PSSGVSTN)
                    if PSSGVGG3 + PSSGVGG4 < 73:
                        print("   " + (PSSGVUNX if "/" not in PSSGVUNX else ""))
                    else:
                        print("\n" + (PSSGVUNX if "/" not in PSSGVUNX else ""))
                print("\nPlease Note: Strength of drug does not match strength of VA Product it is\n" + "matched to.")
            PSSGVCNT = 0
            PSSGVLP = 0
            while PSSGVLP != 0 and not PSSGVOUT:
                PSSGVLP = next(iter(PSSGVLP), 0)
                PSSGVLOC = PSSDRUG.get(PSSGVIEN, {}).get("DOS2", {}).get(PSSGVLP, {}).get("0", "")
                if PSSGVLOC and PSSGVLOC.get("0", "") != "":
                    if PSSGVLOC.get("5", "") and PSSGVLOC.get("6", "") != "":
                        print(PSSGVLOC.get("0", ""))

                    print("\nNumeric Dose: " + (PSSGVLOC.get("6", "") if PSSGVLOC.get("6", "")[0] == "." else "0" + PSSGVLOC.get("6", "")))
                    print("Dose Unit: " + (PSS(51.24, PSSGVLOC.get("5", ""), {}).get("0", "") if PSSGVLOC.get("5", "") else ""))
                print()
                PSSGVIEN_ = PSSGVIEN
                PSSGVIEN = PSSGVLP
                PSSGVLPCX = PSSDRUG.get(PSSGVIEN_, {}).get("DOS2", {}).get(PSSGVLP, {}).get("0", "")
                PSSGVBF6 = ("0" + PSSGVLOC.get("6", "") if PSSGVLOC.get("6", "")[0] == "." else PSSGVLOC.get("6", ""))
                PSSGVAF6 = ("0" + PSSGVLPCX.get("6", "") if PSSGVLPCX.get("6", "")[0] == "." else PSSGVLPCX.get("6", ""))
                if PSSGVLOC.get("5", "") != PSSGVLPCX.get("5", "") or PSSGVBF6 != PSSGVAF6:
                    print("\n" + PSSGVLOC.get("0", ""))
                    print("Numeric Dose: " + (PSSGVLPCX.get("6", "") if PSSGVLPCX.get("6", "")[0] == "." else "0" + PSSGVLPCX.get("6", "")))
                    print("Dose Unit: " + (PSS(51.24, PSSGVLPCX.get("5", ""), {}).get("0", "") if PSSGVLPCX.get("5", "") else ""))
            print()
            UL()
        PSSGVOUT = 0
    if not PSSGVOUT:
        print("All Local Possible Dosages are mapped!")
        choice = input("Press Return to Continue")
    else:
        print("There are still Local Possible Dosages not yet mapped,")
        print("see the 'Local Possible Dosages Report' option for more details.")
        choice = input("Press Return to Continue")

def UL():
    LOCKED.remove(PSSGVIEN)

def TEST():
    if not PSSGVND3 or not PSSGVND1:
        return 0
    if PSSDRUG.get(PSSGVIEN, {}).get("I", "").get("0", "") and PSSDRUG.get(PSSGVIEN, {}).get("I", "").get("0", "") < DT:
        return 0
    PSSGVDOV = ""
    if PSSGVND1 and PSSGVND3 and PSSGVNDF:
        PSSGVDOV = OVRIDE(PSSGVND1, PSSGVND3)
    if not PSSDRUG.get(PSSGVIEN, {}).get("DOS2", ""):
        return 0
    if PSSDRUG.get(PSSGVIEN, {}).get("3", "") == "S" or PSSDRUG.get(PSSGVIEN, {}).get("2", "")[:2] == "XA":
        return 0
    if PSSGVND1 and PSSGVND3:
        PSSGVNDF = DFSU(PSSGVND1, PSSGVND3)
        PSSGVDF = PSSGVNDF.get("0", "")
    if (not PSSGVDF or PSSGVDF <= 0) and PSSDRUG.get(PSSGVIEN, {}).get("2", ""):
        PSSGVDF = PSS.get(50.7, PSSDRUG.get(PSSGVIEN, {}).get("2", ""), {}).get("2", "")
    if PSSGVDOV == "" or not PSSGVDF or PSS.get(50.606, PSSGVDF, {}).get("1", "") == "":
        return 1
    if PSS.get(50.606, PSSGVDF, {}).get("1", "") and not PSSGVDOV:
        return 0
    if not PSS.get(50.606, PSSGVDF, {}).get("1", "") and PSSGVDOV:
        return 0
    return 1