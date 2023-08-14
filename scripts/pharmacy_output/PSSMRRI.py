def PSSMRRI():
    """
    ALB/DRP PRINT MRR ITEMS ;06/18/15
     ;;1.0;PHARMACY DATA MANAGEMENT;**191**;9/30/97;Build 40
    """

    return


def INIT():
    """
    N PSSOIEN,PSSDRG,PSSDSG,PSSSPCE,PSSLN,PSSDDRG,PSSINACT,PSSDDIEN,PSSDSGF,PAGNO,PSSMRR,PSSDRGS,PSSINACTS,PSSDSGI
    N PSSQ,PSSVAL,TERM
    """
    PSSOIEN = None
    PSSDRG = None
    PSSDSG = None
    PSSSPCE = None
    PSSLN = None
    PSSDDRG = None
    PSSINACT = None
    PSSDDIEN = None
    PSSDSGF = None
    PAGNO = None
    PSSMRR = None
    PSSDRGS = None
    PSSINACTS = None
    PSSDSGI = None
    PSSQ = 0
    PSSVAL = None
    TERM = None

    MAIN()
    POP = None
    DTOUT = None
    DUOUT = None
    return


def MAIN():
    ASKUSR()
    if PSSQ:
        return
    # open print device
    OPEN("%ZISUTL", "PSSMRRI")
    if POP:
        print("\nNothing queued to print.\n")
        return

    TERM = 1 if IOST[:2] == "C-" else 0
    # Set output to print device
    PRNHDR()
    GET50P7()
    # close print device
    CLOSE("%ZISUTL", "PSSMRRI")
    return


def ASKUSR():
    """
    Prompt user for input values
    """
    global PSSVAL, PSSQ

    DIR = {}
    DIR[0] = "SB^A:ALL;1:1;2:2;3:3"
    DIR["B"] = "A"
    DIR["A"] = "Enter 'A' to run report for all Orderable Items. Enter '1, 2 or 3' to show only the selected values."
    DIR["?"] = "^D HELP^PSSMRRI"

    X = input()
    if X == "^" or DTOUT or DUOUT:
        print("\nNothing queued to print.\n")
        PSSQ = 1
        return

    PSSVAL = X
    if PSSVAL == "1":
        print("\nThis report will be for items requiring removal at the next administration\n")
    elif PSSVAL == "2":
        print("\nThis report will be for items with optional removal prior to next administration.\n")
    elif PSSVAL == "3":
        print("\nThis report will be for items that require removal prior to the next administration.\n")
    elif PSSVAL == "A":
        print("\nThis report will be for all items that require removal.\n")

    DIR = {"0": "Y", "A": "Is this correct", "B": "Y"}
    Y = input()
    if Y != "1":
        print("\nNothing queued to print.\n")
        PSSQ = 1
        return

    if PSSVAL == "A":
        PSSVAL = "123"

    print("\x07\nThis report is designed for 132 column output!\n")
    return


def HELP():
    """
    Q23
    """
    if len(X) < 2:
        return

    Q23()

    DIR = {"L": ""}
    return


def Q23():
    """
    Enter 'A' to run report for all Orderable Items. Enter '1, 2 or 3'
    to show only the selected values.
                      Select one of the following:
         A        ALL
         1        Removal at Next Administration
         2        Removal Period Optional Prior to Next Administration
         3        Removal Period Required Prior to Next Administration
    """
    print("\nEnter 'A' to run report for all Orderable Items. Enter '1, 2 or 3'")
    print("to show only the selected values.")
    print("                  Select one of the following:")
    print("     A        ALL")
    print("     1        Removal at Next Administration")
    print("     2        Removal Period Optional Prior to Next Administration")
    print("     3        Removal Period Required Prior to Next Administration\n")
    return


def GET50P7():
    """
    S (PSSDRG,PSSDRGS)=""
    F  S PSSDRG=$O(^PS(50.7,"ADF",PSSDRG)) Q:(PSSDRG="")!PSSQ  D
    .S PSSDSG=""
    . F  S PSSDSG=$O(^PS(50.7,"ADF",PSSDRG,PSSDSG)) Q:(PSSDSG="")!PSSQ  D
    .. S PSSOIEN=""
    .. F  S PSSOIEN=$O(^PS(50.7,"ADF",PSSDRG,PSSDSG,PSSOIEN)) Q:(PSSOIEN="")!PSSQ  D
    ... S PSSMRR=$G(^PS(50.7,PSSOIEN,4))
    ... I PSSVAL[+PSSMRR S PSSINACT=$P(^PS(50.7,PSSOIEN,0),U,4) D
    .... S PSSDSGF=$P(^PS(50.606,PSSDSG,0),U),PSSDDIEN="",PSSDRG=PSSDRG_" - "_PSSDSGF
    .... F  S PSSDDIEN=$O(^PS(50.7,"A50",PSSOIEN,PSSDDIEN)) Q:(PSSDDIEN="")!PSSQ  D
    ..... S:$G(PSSDDIEN)]"" PSSDDRG=$P(^PSDRUG(PSSDDIEN,0),"^"),PSSDSGI=$G(^PSDRUG(PSSDDIEN,"I")),PSSDSGI=$S(PSSDSGI="":" ",1:PSSDSGI)
    ..... D PRNLN
    .....Q
    ....Q
    ...Q
    ..Q
    Q
    """
    PSSDRG = ""
    while PSSDRG != "" and not PSSQ:
        PSSDSG = ""
        while PSSDSG != "" and not PSSQ:
            PSSOIEN = ""
            while PSSOIEN != "" and not PSSQ:
                PSSMRR = None
                if PSSVAL[PSSMRR]:
                    PSSINACT = None
                    PSSDSGF = None
                    PSSDDIEN = ""
                    PSSDRG = PSSDRG + " - " + PSSDSGF
                    while PSSDDIEN != "" and not PSSQ:
                        if PSSDDIEN:
                            PSSDDRG = None
                            PSSDSGI = None
                            if PSSDSGI == "":
                                PSSDSGI = " "
                            PRNLN()
    return


def PRNHDR():
    """
    Heading
    """
    global PAGNO

    PAGNO = PAGNO + 1
    print(f"{chr(27)}[H")
    print(f"{chr(27)}[2J")
    print(f"{chr(27)}[3J")
    print(f"{chr(27)}[5;1H")
    print(" " * 57 + f"{FMTE(NOW(), 1)[:18]: <18}")
    print(f"Orderable Items Report on Medications Requiring Removal (MRR) Prompt for Removal in BCMA Value".ljust(132))
    print("Page " + str(PAGNO).rjust(125))
    print("ORDERABLE ITEM                  OI INACTIVE   MRR  DISPENSE DRUG (DD)              DD INACTIVE")
    print("NAME - DOSAGE FORM              DATE          VAL  NAME                            DATE ")
    print("------------------------------  ------------  ---  ------------------------------  -----------")
    return


def PRNLN():
    """
    Write line on report
    """
    global PSSDRGS, PSSDRGP, PSSINACTP, PSSMRRP

    if PSSDRGS == PSSDRG:
        PSSDRGP = PSSINACTP = PSSMRRP = " "
    else:
        PSSDRGS = PSSDRG
        PSSDRGP = PSSDRG
        PSSINACTP = PSSINACT
        PSSMRRP = " " + PSSMRR + " "

    print(
        f"{PSSDRGP + PSSSPCE: <35}"
        f"{FMTE(PSSINACTP, 5) + PSSSPCE: <15}"
        f"{PSSMRRP + PSSSPCE: <6}"
        f"{PSSDDRG + PSSSPCE: <35}"
        f"{FMTE(PSSDSGI, 5) + PSSSPCE: <15}"
    )

    if Y > (IOSL - 1):
        PAUSE()
        if TERM:
            return
        PRNHDR()
    return


def PAUSE():
    """
    Pause
    """
    global PSSQ

    print("\nPress RETURN to continue, '^' to exit")
    X = input()
    if X == "^" or not T:
        PSSQ = 1
    return