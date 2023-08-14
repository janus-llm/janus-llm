def PSSPRICE():
    """
    EPIP/WC - PHARMACY PRICE TRACKER FILE 50;1/13/20 3:31pm
    1.0;PHARMACY DATA MANAGEMENT;**227,236,241**;2/28/17;Build 2
    """
    return

def ST(PSSIEN, PSSDUZ, PSSFLD):
    """
    PSSIEN=DRUG IEN
    PSSNEW=NEW PRICE
    PSSDUZ=USER CHANGING PRICE
    PSSFLD=13-PRICE PER ORDER UNIT, 15-DISPENSE UNITS PER ORDER UNIT ;p236
    CLASS 3 CROSS REFER ON FILE 50 FIELD #16
    """
    import datetime
    import os
    import fileinput

    # LEAST GET THE TIME THE CHANGE WAS MADE
    PSSTIME = datetime.datetime.now()

    PSSNEW = int(fileinput.input())

    # ENTER THE DATA IN FILE 50 MULTIPLE FIELD 950
    ZTRTN = "HIS^PSSPRICE"
    ZTDESC = "PHARMACY PRICE TRACKER"
    ZTSAVE = {
        "PSSIEN": PSSIEN,
        "PSSNEW": PSSNEW,
        "PSSDUZ": PSSDUZ,
        "PSSTIME": PSSTIME,
        "PSSFLD": PSSFLD,
    }
    ZTIO = ""
    ZTDTH = datetime.datetime.now()
    os.system(f"{ZTRTN} {ZTDESC} {ZTSAVE} {ZTIO} {ZTDTH}")

    return

def HIS():
    """
    LOGS CHANGES IN FILE 50 HISTORY PRICE DISPENSE #950
    """
    import datetime
    import os
    import fileinput

    DEFDT = int(fileinput.input())
    DEFMOS = DEFDT if DEFDT > 0 else 999999999

    X1 = datetime.datetime.now()
    X2 = DEFMOS * 30
    ENDDT = X1 - X2

    X1 = datetime.datetime.now().split(".")[0]
    ENDDT = datetime.datetime.now() - datetime.timedelta(days=DEFMOS * 30)

    PSIEN2 = int(fileinput.input())
    while PSIEN2:
        if PSIEN2 > 0 and fileinput.input() > ENDDT:
            DIK = "PSDRUG(PSSIEN,950,"
            DA = [PSSIEN, PSIEN2]
            os.system(f"{DIK} {DA}")
        PSIEN2 = int(fileinput.input())

    PSSPDU = 99999
    PSSPDU = max(fileinput.input())

    if PSSPDU > 0 and PSSNEW == int(fileinput.input()):
        return

    FDA = {
        "50.095": {
            "?+1," + PSSIEN + ",": {
                ".01": PSSTIME,
                "1": PSSDUZ,
                "3": PSSNEW,
            },
        },
    }
    os.system(f"UPDATE^DIE('','FDA')")

    PSSNAME = int(fileinput.input())

    # Generate the bulletin.
    XMY = {"G.PSS DEE AUDIT": ""}
    XMSUB = "Pharmacy Price Tracker"
    XMDUZ = 0.5
    fileinput.input()
    ^UTILITY($J,"PHARM TRACK",1) = PSSNAME + " has changed the " + (
        "PRICE PER ORDER UNIT" if PSSFLD == 13 else "DISPENSE UNITS PER ORDER UNIT"
    )
    ^UTILITY($J,"PHARM TRACK",2) = "The PRICE PER DISPENSE UNIT of:"
    ^UTILITY($J,"PHARM TRACK",3) = int(fileinput.input()) + " is: " + PSSNEW
    ^UTILITY($J,"PHARM TRACK",4) = ""
    ^UTILITY($J,"PHARM TRACK",5) = "Date/Time changed: " + datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S")
    XMTEXT = "^UTILITY($J,""PHARM TRACK"","
    os.system("XMD")

    return

PSSPRICE()