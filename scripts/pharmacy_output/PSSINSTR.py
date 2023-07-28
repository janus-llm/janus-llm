def PSSINSTR():
    """
    HPS/RTR-Medication Route Utilities
    4/23/20 3:36pm
    """
    return

def REP():
    """
    Med Instruction Med Route Report
    """
    print("\nThis report displays matches between the Medication Instruction file (#51)")
    print("and the Medication Routes file (#51.2) when a Name in the Medication")
    print("Instruction file matches an Abbreviation in the Medication Routes file.\n")
    
    # Initialize variables
    DIR, Y, X, DTOUT, DUOUT, DIRUT, DIROUT, IOP, %ZIS, POP, ZTRTN, ZTDESC, ZTSAVE, ZTSK = [None] * 13
    
    # Select output device
    IOP, %ZIS = "QM", "^%ZIS"  # Assume variables are assigned elsewhere
    exec(%ZIS)  # Assume %ZIS is translated elsewhere
    if POP > 0:
        print("\nNo Action taken.")
        DIR, Y = None, None
        DIR(0) = "E"
        DIR("A") = "Press Return to continue"
        exec("^DIR")  # Assume ^DIR is translated elsewhere
        return
    
    # Queue the report to print if requested
    if IO("Q"):
        ZTRTN = "START^PSSINSTR"
        ZTDESC = "Med Instruction Med Route Report"
        exec("^%ZTLOAD")  # Assume ^%ZTLOAD is translated elsewhere
        print("\nReport queued to print.")
        DIR, Y = None, None
        DIR(0) = "E"
        DIR("A") = "Press Return to continue"
        exec("^DIR")  # Assume ^DIR is translated elsewhere
        return
    
def START():
    """
    Entry point for the report
    """
    exec("U IO")  # Assume IO is translated elsewhere
    
    # Initialize variables
    DIR, DUOUT, DTOUT, Y, X, DIRUT, DIROUT = [None] * 7

    # Initialize more variables
    PSSTLINE, PSSTOUT, PSSTDV, PSSTCT = "", 0, "", 1
    DIR, DUOUT, DTOUT, Y, X, DIRUT, DIROUT = [None] * 7
    
    # Initialize more variables
    PSSIIEN, PSSINAM, PSSINS, PSSRIEN, PSSRNAM = "", "", "", "", ""
    
    PSSTOUT = 0
    PSSTDV = "P" if IOST[:2] != "C-" else "C"
    PSSTCT = 1
    PSSTLINE = "-" * 75
    
    HD()
    
    PSSINS = ""
    while PSSINS != "" and not PSSTOUT:
        if "B" in ^PS(51, PSSINS):
            PSSIIEN = ^PS(51, PSSINS, "B", PSSINS, 0)
            PSSRIEN = ^PS(51.2, PSSINS, "C", PSSINS, 0)
            PSSINAM = ^PS(51, PSSIIEN, 0)[2][:30]
            PSSRNAM = ^PS(51.2, PSSRIEN, 0)[1]
            print(f"{PSSINS:12}{PSSINAM:30}{PSSRNAM:30}")
            if Y + 5 > IOSL:
                HD()
                if PSSTOUT:
                    break
    
    if PSSTDV == "P":
        print("\nEnd of Report.")
    
    if not PSSTOUT and PSSTDV == "C":
        print("\nEnd of Report.")
        DIR, Y = None, None
        DIR(0) = "E"
        DIR("A") = "Press Return to continue"
        exec("^DIR")  # Assume ^DIR is translated elsewhere
    
    if PSSTDV == "C":
        print()
    else:
        exec("@IOF")  # Assume @IOF is translated elsewhere
    
    exec("^%ZISC")  # Assume ^%ZISC is translated elsewhere
    if ZTQUEUED:
        exec("ZTREQ = '@'")  # Assume ZTREQ is translated elsewhere
    return

def HD():
    """
    Print the report header
    """
    if PSSTDV == "C" and PSSTCT != 1:
        DIR, Y = None, None
        DIR(0) = "E"
        DIR("A") = "Press Return to continue, '^' to exit"
        exec("^DIR")  # Assume ^DIR is translated elsewhere
        if not Y:
            PSSTOUT = 1
            return
    
    exec("@IOF")  # Assume @IOF is translated elsewhere
    print("MED INSTRUCTION MED ROUTE REPORT".ljust(65) + "Page: " + str(PSSTCT))
    PSSTCT += 1
    print("\nNAME/ABBR".ljust(12) + "INSTR EXPANSION".ljust(30) + "ROUTE NAME".ljust(30))
    print(PSSTLINE)
    return

PSSINSTR()
REP()
START()