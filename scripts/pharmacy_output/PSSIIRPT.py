def PSSIIRPT():
    print("\nThis report displays entries from the INFUSION INSTRUCTION (#53.47) File.")
    
    PSSMXLNG = input("Print report in 80 or 132 column format (80/132): ")
    if PSSMXLNG != "80" and PSSMXLNG != "132":
        print("\nInvalid input. Report will be printed in 80 column format by default.")
        PSSMXLNG = "80"
    
    print()
    
    PSSMXOUT = 0
    PSSMXNOF = 0
    PSSMXDEV = "P" if not sys.stdout.isatty() else "C"
    PSSMXCT = 1
    
    if PSSMXLNG == "132":
        PSSMXLIN = "-" * 130
    else:
        PSSMXLIN = "-" * 78
    
    HD()
    
    PSSMXQ = ""
    while not PSSMXOUT:
        PSSMXQ = input("Enter INFUSION INSTRUCTION: ")
        if not PSSMXQ:
            break
        
        PSSMXQEN = 0
        while PSSMXQEN is not None and not PSSMXOUT:
            PSSMXQEN = next((i for i, x in enumerate(PSSMXQ) if x.startswith(PSSMXQ)), None)
            
            if PSSMXQEN is not None:
                PSSMXRA = PSSMXQEN
                
                PSSMXRAA = {
                    "53.47": {
                        PSSMXRA: {
                            ".01": {
                                "E": PSSMXQ
                            }
                        }
                    }
                }
                
                PSSMXNOF = 1
                print(f"\n{PSSMXRAA['53.47'][PSSMXRA]['.01']['E']}")
                
                if PSSMXLNG == "132":
                    PSSMXREP = PSSMXRAA["53.47"][PSSMXRA]["1"]["E"]
                    if len(PSSMXREP) < 104:
                        print(PSSMXREP)
                    else:
                        for line in textwrap.wrap(PSSMXREP, width=104):
                            print(line)
                else:
                    PSSMXREP = PSSMXRAA["53.47"][PSSMXRA]["1"]["E"]
                    if len(PSSMXREP) < 52:
                        print(PSSMXREP)
                    else:
                        for line in textwrap.wrap(PSSMXREP, width=52):
                            print(line)
                
                if PSSMXCT > 1 and PSSMXDEV == "C":
                    response = input("Press Return to continue, '^' to exit: ")
                    if response == "^":
                        PSSMXOUT = 1
                
                if not PSSMXOUT and PSSMXDEV == "C":
                    print()
                    if PSSMXCT > 1:
                        response = input("Press Return to continue, '^' to exit: ")
                        if response == "^":
                            PSSMXOUT = 1
                    else:
                        response = input("Press Return to continue: ")
        else:
            print("Invalid INFUSION INSTRUCTION.")
    
    if PSSMXDEV == "P":
        print("\nEnd of Report.")
    elif not PSSMXOUT and PSSMXDEV == "C":
        print("\nEnd of Report.")
        input("Press Return to continue")
    
    if PSSMXDEV == "C":
        print()
    else:
        print("\f")
    
    PSSMXLNG = None


def HD():
    if PSSMXDEV == "C" and PSSMXCT != 1:
        input("Press Return to continue, '^' to exit: ")
    
    print("\f")
    print("INFUSION INSTRUCTION FILE REPORT")
    print("PAGE:", PSSMXCT)
    print(PSSMXLIN)
    print()
    PSSMXCT += 1


def MESS():
    print("\nNothing queued to print.")


PSSIIRPT()