def PSSUNMSI():
    if not XPDENV:
        return

    print()
    DIR["A"] = "Unmark Supply Items as Non-VA Meds? "
    DIR[0] = "SA^Y:YES;N:NO"
    DIR["B"] = "YES"
    DIR()
    print()

    if DTOUT or DUOUT:
        XPDQUIT = 1
        return

    if Y != "N" and Y != "Y":
        PSSUNMSI()
        return
    
    print(f"   Supply items will {'NOT ' if Y == 'N' else ''}be unmarked as Non-VA Med")
    print("   with the installation of this patch.\n")
    ^XTMP["PSS*1*69"] = Y


def EN():
    OI = None
    APPUSE = None
    DGIEN = None
    X = None
    PSSCROSS = None
    PSSTEST = None

    if ^XTMP["PSS*1*69"] != "Y":
        del ^XTMP["PSS*1*69"]
        return

    del ^XTMP["PSS*1*69"]
    del ^TMP["PSSOI"][$J]

    print("Unmarking supply items as Non-VA Meds...")
    APPUSE = ""
    while APPUSE != "":
        if APPUSE != "X":
            continue
        DGIEN = ""
        while DGIEN != "":
            if ^PSDRUG[DGIEN,"I"] and (^PSDRUG[DGIEN,"I"] < DT):
                continue

            OI = ^PSDRUG[DGIEN,2]
            if not OI:
                continue

            if not ^PS[50.7,OI,0][9]:
                continue

            OINAM = ^PS[50.7,OI,0]
            ^PS[50.7,OI,0][10] = 0
            XREFS(DGIEN, APPUSE)
            ^TMP["PSSOI"][$J,OI] = ""

    print("Done!")

    print("Updating CPRS Orderable Item File...")
    OI = 0
    PSSCROSS = 1
    while OI != 0:
        PSSTEST = OI
        EN1^PSSPOIDT()
    
    print("Done!")


def XREFS(DGIEN, APPUSE):
    DGNAME = None
    NEWAPP = None

    if not ^PSDRUG[DGIEN,0]:
        return

    DGNAME = ^PSDRUG[DGIEN,0]
    NEWAPP = APPUSE.replace("X", "")
    ^PSDRUG[DGIEN,2][3] = NEWAPP
    del ^PSDRUG["AIUX",DGNAME,DGIEN]
    if APPUSE:
        del ^PSDRUG["IU",APPUSE,DGIEN]
    if NEWAPP:
        ^PSDRUG["IU",NEWAPP,DGIEN] = ""


PSSUNMSI()
EN()