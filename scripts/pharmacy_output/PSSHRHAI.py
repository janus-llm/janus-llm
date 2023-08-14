def PSSHRHAI():
    """
    BIRMINGHAM/GN-Orderable Items High Risk/High Alert Report
    """
    pass

def INIT():
    """
    Initialize Variables
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
    TERM = None
    PSSQ = None
    PSSVAL = None
    PSSDRGS = None
    PSSDSGI = None
    PSSHRA = None
    PSSINACTS = None
    
    PAGNO = 0
    PSSSPCE = " " * 30
    PSSQ = 0
    
    MAIN()
    
    POP = None
    DTOUT = None
    DUOUT = None
    del POP, DTOUT, DUOUT


def MAIN():
    ASKUSR()
    if PSSQ:
        return
    # open print device
    OPEN("%ZISUTL", "PSSMRRI")
    if POP:
        return
    TERM = 1 if IOST[:2] == "C-" else 0
    # set output to print device
    IO = "PSSMRRI"
    
    PRNHDR()
    GET50P7()
    
    # close print device
    CLOSE("%ZISUTL", "PSSMRRI")


def GET50P7():
    PSSDRG = ""
    PSSDRGS = ""
    
    while PSSDRG != "" and not PSSQ:
        PSSDSG = ""
        PSSDRGP = PSSDRG
        
        while PSSDSG != "" and not PSSQ:
            PSSOIEN = ""
            
            while PSSOIEN != "" and not PSSQ:
                PSSHRA = PSSOIEN[14]
                
                if +PSSHRA in PSSVAL:
                    PSSINACT = PSSOIEN[4]
                    PSSDSGF = PSSDSG[0]
                    PSSDSGI = PSSDSG[1]
                    PSSDDIEN = ""
                    PSSDRG = f"{PSSDRG} - {PSSDSGF}"
                    
                    while PSSDDIEN != "" and not PSSQ:
                        PSSDDRG = PSSDRUG[PSSDDIEN][0]
                        PSSDSGI = PSSDSGI if PSSDSGI != "" else " "
                        PRNLN()
                
                PSSOIEN = next(PSSOIEN)
            
            PSSDSG = next(PSSDSG)
        
        PSSDRG = next(PSSDRG)


def ASKUSR():
    global PSSQ, PSSVAL
    
    PSSQ = 0
    DIR = {}
    DIR[0] = "SB^A:ALL;1:1;2:2;3:3"
    DIR["B"] = "A"
    DIR["A"] = "Print Report for (A)ll or Specific HR/HA Flag values(1,2,3)"
    DIR["?"] = "^D HELP^PSSHRHAI"
    
    Y = input()
    if Y == "^" or DTOUT or DUOUT:
        print("\nNothing queued to print.\n")
        PSSQ = 1
        return
    
    PSSVAL = X
    if PSSVAL == "1":
        print("\nThis report will be for items that do not require a witness in BCMA\n")
    elif PSSVAL == "2":
        print("\nThis report will be for items that recommend a witness in BCMA\n")
    elif PSSVAL == "3":
        print("\nThis report will be for items that require a witness in BCMA\n")
    elif PSSVAL == "A":
        print("\nThis report will be for all High Risk/High Alert witness related items\n")
    else:
        print("\nInvalid input\n")
        PSSQ = 1
        return
    
    DIR = {}
    DIR[0] = "Y"
    DIR["A"] = "Is this correct"
    DIR["B"] = "Y"
    
    Y = input()
    if Y != "1":
        ASKUSR()
    

def PRNHDR():
    global PAGNO
    
    PAGNO = PAGNO + 1
    print(f"{FMTE(NOW(), 5):>57}")
    print(f"{'High Risk/High Alert for Orderable Items Report':>42}{'Page {PAGNO}':>125}")
    print("ORDERABLE ITEM                  OI INACTIVE   HRHA  DISPENSE DRUG (DD)              DD INACTIVE")
    print("NAME - DOSAGE FORM              DATE          VAL   NAME                            DATE ")
    print("------------------------------  ------------  ----  ------------------------------  -----------")


def PRNLN():
    global PSSDRGS
    
    PSSDRGP = PSSDRG if PSSDRGS == PSSDRG else ""
    PSSINACTP = PSSINACT if PSSDRGS == PSSDRG else ""
    PSSHRAP = f"  {PSSHRA} "
    
    print(f"{PSSDRGP + PSSSPCE[:30]:<5}{FMTE(PSSINACTP, 5) + PSSSPCE[:12]:<5}{PSSHRAP + PSSSPCE[:4]:<5}{PSSDDRG + PSSSPCE[:30]:<5}{PSSDSGI + PSSSPCE[:12]:<5}")
    
    if PSSQ:
        return
    
    if Y > IOST - 1:
        if TERM:
            PAUSE()
        PRNHDR()


def PAUSE():
    global PSSQ
    
    if not TERM:
        return
    
    print("\nPress RETURN to continue, '^' to exit")
    X = input()
    if X == "^" or not T:
        PSSQ = 1
        return


PSSHRHAI()