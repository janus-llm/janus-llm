def PSSPOST6():
    # Initializing NON-VA MED field (#8) on File #50.7
    OI = ""
    while OI:
        OI = next(iter(^PS(50.7,OI)))
        ^PS(50.7,OI,0)[10] = ""

    # Updating APPL PCKGS' USE (File #50) and NON-VA MED (File #50.7)
    APPUSE = ""
    while APPUSE:
        APPUSE = next(iter(^PSDRUG("IU",APPUSE)))
        if "O" not in APPUSE:
            continue
        if "X" in APPUSE:
            continue
        DGIEN = ""
        while DGIEN:
            DGIEN = next(iter(^PSDRUG("IU",APPUSE,DGIEN)))
            if ^PSDRUG(DGIEN,"I") and (^("I")[1] < DT):
                continue
            OI = ^PSDRUG(DGIEN,2)[1]
            if OI:
                ^PS(50.7,OI,0)[10] = 1
            XREFS(DGIEN,APPUSE)
            print(f"Updating Drug {DGIEN}")

def XREFS(DGIEN,APPUSE):
    # Updating existing x-references for the Application Use field (#63) - DRUG File
    DGNAME = ^PSDRUG(DGIEN,0)[1]
    NEWAPP = APPUSE + "X"
    ^PSDRUG(DGIEN,2)[3] = NEWAPP
    ^PSDRUG("AIUX",DGNAME,DGIEN) = ""
    if APPUSE:
        del ^PSDRUG("IU",APPUSE,DGIEN)
    ^PSDRUG("IU",NEWAPP,DGIEN) = ""