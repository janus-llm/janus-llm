def PSSMIRPT():
    """
    BIR/RTR-Medication Instruction Report
    07/03/07
    1.0;PHARMACY DATA MANAGEMENT;**129,201**;9/30/97;Build 25
    """
    # Prompts for Medication Instruction File Report
    print("\nThis report displays entries from the MEDICATION INSTRUCTION (#51) File. It")
    print("can be run for all Medication Instructions or only Medication Instructions")
    print("without a FREQUENCY (IN MINUTES). If a FREQUENCY (IN MINUTES) cannot be")
    print("determined for an order, the daily dosage check cannot occur for that order.")
    
    # Prompt for all or only medication instructions with a missing frequency
    PSSMXRP = input("\nPrint All Medication Instructions, or Only Medication Instructions without a frequency (A/O): ")
    if PSSMXRP not in ['A', 'O']:
        print("\nInvalid option. Please try again.")
        return
    
    # Prompt for 80 or 132 column format
    PSSMXLNG = input("\nPrint report in 80 or 132 column format (80/132): ")
    if PSSMXLNG not in ['80', '132']:
        print("\nInvalid option. Please try again.")
        return
    
    # Print report
    START(PSSMXRP, PSSMXLNG)
    
    
def START(PSSMXRP, PSSMXLNG):
    """
    Print Medication Instruction File report
    """
    PSSMXOUT = 0
    PSSMXNOF = 0
    PSSMXDEV = 'P' if not sys.stdout.isatty() else 'C'
    PSSMXCT = 1
    
    PSSMXLIN = "-" * 130 if PSSMXLNG == '132' else "-" * 78
    
    HD(PSSMXRP, PSSMXLNG, PSSMXCT, PSSMXLIN)
    
    # Loop through Medication Instructions
    for PSSMXQ in sorted(PS(51, "B")):
        if PSSMXOUT:
            break
        
        for PSSMXQEN in sorted(PS(51, "B", PSSMXQ)):
            if not PS(51, "B", PSSMXQ, PSSMXQEN):
                PSSMXRA = PSSMXQEN
                PSSMXRAA = GETS(51, PSSMXRA, [".01", ".5", "1", "1.1", "9", "30", "31", "32", "32.1*", "33*"], "E")

                if PSSMXRP == "O" and PSSMXRAA.get(51, PSSMXRA, 31, "E"):
                    continue

                PSSMXNOF = 1

                print()
                print(PSSMXRAA.get(51, PSSMXRA, ".01", "E"))
                if len(PSSMXRAA.get(51, PSSMXRA, ".01", "E")) + 5 > os.get_terminal_size().lines:
                    HD(PSSMXRP, PSSMXLNG, PSSMXCT, PSSMXLIN)
                
                print(f"{' ' * 25}SYNONYM: {PSSMXRAA.get(51, PSSMXRA, ".5", "E")}")
                if len(PSSMXRAA.get(51, PSSMXRA, ".5", "E")) + 5 > os.get_terminal_size().lines:
                    HD(PSSMXRP, PSSMXLNG, PSSMXCT, PSSMXLIN)
                
                print(f"{' ' * 23}EXPANSION: ")
                PSSMXREP = PSSMXRAA.get(51, PSSMXRA, "1", "E")
                if PSSMXLNG == '132':
                    print(PSSMXREP)
                else:
                    if len(PSSMXREP) < 46:
                        print(PSSMXREP)
                    else:
                        wrapper = textwrap.TextWrapper(width=79, initial_indent=' ' * 35, subsequent_indent=' ' * 35)
                        paragraphs = wrapper.wrap(text=PSSMXREP)
                        for paragraph in paragraphs:
                            print(paragraph)
                if len(PSSMXREP) + 5 > os.get_terminal_size().lines:
                    HD(PSSMXRP, PSSMXLNG, PSSMXCT, PSSMXLIN)
                    print()
                
                print(f"{' ' * 8}OTHER LANGUAGE EXPANSION: ")
                PSSMXROO = PSSMXRAA.get(51, PSSMXRA, "1.1", "E")
                if PSSMXLNG == '132':
                    if len(PSSMXROO) < 98:
                        print(PSSMXROO)
                    else:
                        wrapper = textwrap.TextWrapper(width=131, initial_indent=' ' * 35, subsequent_indent=' ' * 35)
                        paragraphs = wrapper.wrap(text=PSSMXROO)
                        for paragraph in paragraphs:
                            print(paragraph)
                else:
                    if len(PSSMXROO) < 46:
                        print(PSSMXROO)
                    else:
                        wrapper = textwrap.TextWrapper(width=79, initial_indent=' ' * 35, subsequent_indent=' ' * 35)
                        paragraphs = wrapper.wrap(text=PSSMXROO)
                        for paragraph in paragraphs:
                            print(paragraph)
                if len(PSSMXROO) + 5 > os.get_terminal_size().lines:
                    HD(PSSMXRP, PSSMXLNG, PSSMXCT, PSSMXLIN)
                    print()
                
                print(f"{' ' * 26}PLURAL: {PSSMXRAA.get(51, PSSMXRA, "9", "E")}")
                if len(PSSMXRAA.get(51, PSSMXRA, "9", "E")) + 5 > os.get_terminal_size().lines:
                    HD(PSSMXRP, PSSMXLNG, PSSMXCT, PSSMXLIN)
                
                print(f"{' ' * 20}INTENDED USE: {PSSMXRAA.get(51, PSSMXRA, "30", "E")}")
                if len(PSSMXRAA.get(51, PSSMXRA, "30", "E")) + 5 > os.get_terminal_size().lines:
                    HD(PSSMXRP, PSSMXLNG, PSSMXCT, PSSMXLIN)
                
                print(f"{' ' * 10}DOSING CHECK FREQUENCY: {PSSMXRAA.get(51, PSSMXRA, "32", "E")}")
                if len(PSSMXRAA.get(51, PSSMXRA, "32", "E")) + 5 > os.get_terminal_size().lines:
                    HD(PSSMXRP, PSSMXLNG, PSSMXCT, PSSMXLIN)
                
                print(f"{' ' * 5}DRUG(S) FOR DOSING CHK FREQ: ")
                if PSSMXRAA.get(51, 0, "32.1*", ""):
                    PSSFD = 1
                    PSSDFS = 0
                    while True:
                        if PSSFD not in PSSMXRAA.get(51, 0, "32.1*", {}):
                            break
                        print(' ' * 34, PSSMXRAA.get(51, PSSFD, ".01", "E"), sep='')
                        if PSSDFS:
                            print()
                        PSSDFS = 1
                        PSSFD += 1
                        if len(PSSMXRAA.get(51, PSSFD, ".01", "E")) + 5 > os.get_terminal_size().lines:
                            HD(PSSMXRP, PSSMXLNG, PSSMXCT, PSSMXLIN)
                            print()
                
                print(f"{' ' * 10}FREQUENCY (IN MINUTES): {PSSMXRAA.get(51, PSSMXRA, "31", "E")}")
                if len(PSSMXRAA.get(51, PSSMXRA, "31", "E")) + 5 > os.get_terminal_size().lines:
                    HD(PSSMXRP, PSSMXLNG, PSSMXCT, PSSMXLIN)
                
                print(f"{' ' * 5}OLD MED INSTRUCTION NAME(S): ")
                if PSSMXRAA.get(51, 0, "33*", ""):
                    PSSFD = 1
                    PSSDFS = 0
                    while True:
                        if PSSFD not in PSSMXRAA.get(51, 0, "33*", {}):
                            break
                        print(' ' * 34, PSSMXRAA.get(51, PSSFD, ".01", "E"), sep='')
                        if PSSDFS:
                            print()
                        PSSDFS = 1
                        PSSFD += 1
                        if len(PSSMXRAA.get(51, PSSFD, ".01", "E")) + 5 > os.get_terminal_size().lines:
                            HD(PSSMXRP, PSSMXLNG, PSSMXCT, PSSMXLIN)
                            print()
                else:
                    if len(PSSMXRAA.get(51, PSSMXRA, "31", "E")) + 5 > os.get_terminal_size().lines:
                        HD(PSSMXRP, PSSMXLNG, PSSMXCT, PSSMXLIN)
                        print()
    
    # End of Report
    END(PSSMXOUT, PSSMXRP, PSSMXDEV, PSSMXCT)


def HD(PSSMXRP, PSSMXLNG, PSSMXCT, PSSMXLIN):
    """
    Report Header
    """
    if PSSMXDEV == 'C' and PSSMXCT != 1:
        if input("Press Return to continue, '^' to exit: ") != '':
            global PSSMXOUT
            PSSMXOUT = 1
            return
    
    os.system('cls' if os.name == 'nt' else 'clear')
    print("MEDICATION INSTRUCTION FILE REPORT (All)" if PSSMXRP == 'A' else "MEDICATION INSTRUCTIONS WITHOUT FREQUENCY REPORT", end='')
    print(f"{' ' * (68 if PSSMXLNG == '80' else 120)}PAGE: {PSSMXCT}\n{PSSMXLIN}\n")
    PSSMXCT += 1


def END(PSSMXOUT, PSSMXRP, PSSMXDEV, PSSMXCT):
    """
    End of Report
    """
    if not PSSMXOUT and PSSMXRP == "O" and not PSSMXNOF:
        print("\nNo Medication Instructions found without frequencies.")
    
    if PSSMXDEV == "P":
        print("\nEnd of Report.")
    elif not PSSMXOUT and PSSMXDEV == "C":
        print("\nEnd of Report.")
        input("Press Return to continue")
        print()
    else:
        print()
    
    if PSSMXDEV != "C":
        os.system('cls' if os.name == 'nt' else 'clear')
    
    global PSSMXRP, PSSMXLNG
    PSSMXRP = None
    PSSMXLNG = None


def MESS():
    """
    Display message when nothing is queued to print
    """
    print("\nNothing queued to print.")


PSSMIRPT()