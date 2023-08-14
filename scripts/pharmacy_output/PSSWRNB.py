# PSSWRNB ;BIR/EJW-NEW WARNING SOURCE CUSTOM WARNING LIST BUILDER ; 9/8/05 3:46pm
# 1.0;PHARMACY DATA MANAGEMENT;**87,98,144**;9/30/97;Build 13

# IA: 3735 ^PSNDF(50.68
# IA: 4445 ^PS(50.625
# IA: 4446 ^PS(50.626
# IA: 4448 ^PS(50.627

def PSSWRNB():
    # Call the NOTE functions
    NOTE()
    NOTE2()
    print()
    DIR = input(" Would you like to print a list of the entries in these files (Y/N): ")
    if DIR == "Y":
        SPANISH = 0
        DIR = input(" Would you like to include the Spanish translations (Y/N): ")
        if DIR == "Y":
            SPANISH = 1
        RPT()
    
    SEL()
    print()
    # Call the NOTE function again
    NOTE()
    print()
    print("Select one of the following to display drugs that match that criteria to")
    print("examine or edit their drug warnings:")
    print("1. Drug has WARNING LABEL filled in but there are no FDB warnings for the drug")
    print("2. Drug has WARNING LABEL numbers higher than 20")
    print("3. Select by range of drug names")
    print("4. Drug has more than 5 warning labels")
    print("5. Drugs containing specific WARNING LABEL number")
    print("6. Drug has WARNING LABEL that does not map to new data source")
    print("7. Drugs containing specific new data source warning number")
    print("8. Drugs containing gender-specific warnings")
    print('9. Drugs with warning mapping, but drug doesn\'t contain "mapped to" number')
    DIR = input("Enter selection or '^' to exit: ")
    SEL = int(DIR)

    if not SEL:
        KILL()
        return

    DR, ACTIVE, SKIP, QUIT, PSO9 = None, None, None, None, None

    SKIP = 1
    QUIT = 0

    # Initialize the temporary global array
    TMP = {}

    while True:
        DIR = input("Exclude drugs with NEW WARNING LABEL LIST filled in (Y/N): ")
        if DIR == "Y":
            SKIP = 0
        print()
        print("NOTE: Only the first 5 warnings will print on the yellow auxillary labels.")
        DIR = input("Do you want to see the warning text for all warnings (Y/N): ")
        if DIR == "Y":
            ENDWARN = 99
            print("  Warnings (>5) that won't print and won't be sent to CMOP")
            print("  will be marked with a \"*\" on the following screens.")
        else:
            ENDWARN = 5
        print()
        DIR = input("Press Enter to continue: ")
        if not DIR:
            break

    if SEL == 1:
        SEL1()
    elif SEL == 2:
        SEL2()
    elif SEL == 3:
        SEL3()
    elif SEL == 4:
        SEL4()
    elif SEL == 5 or SEL == 9:
        SEL59()
    elif SEL == 6:
        SEL6()
    elif SEL == 7:
        SEL7()
    elif SEL == 8:
        SEL8()

    if not QUIT:
        EDIT()

    SEL()

def NOTE():
    pass

def NOTE2():
    pass

def RPT():
    while True:
        print()
        DIR = input("You may queue the report to print, if you wish. Press Enter to continue: ")
        if not DIR:
            break

    if True:  # Replace with condition for queueing report
        PRT54()

def SEL():
    print()
    # Call the NOTE function again
    NOTE()
    print()
    print("Select one of the following to display drugs that match that criteria to")
    print("examine or edit their drug warnings:")
    print("1. Drug has WARNING LABEL filled in but there are no FDB warnings for the drug")
    print("2. Drug has WARNING LABEL numbers higher than 20")
    print("3. Select by range of drug names")
    print("4. Drug has more than 5 warning labels")
    print("5. Drugs containing specific WARNING LABEL number")
    print("6. Drug has WARNING LABEL that does not map to new data source")
    print("7. Drugs containing specific new data source warning number")
    print("8. Drugs containing gender-specific warnings")
    print('9. Drugs with warning mapping, but drug doesn\'t contain "mapped to" number')
    DIR = input("Enter selection or '^' to exit: ")
    SEL = int(DIR)

    if not SEL:
        KILL()
        return

    DR, ACTIVE, SKIP, QUIT, PSO9 = None, None, None, None, None

    SKIP = 1
    QUIT = 0

    # Initialize the temporary global array
    TMP = {}

    while True:
        DIR = input("Exclude drugs with NEW WARNING LABEL LIST filled in (Y/N): ")
        if DIR == "Y":
            SKIP = 0
        print()
        print("NOTE: Only the first 5 warnings will print on the yellow auxillary labels.")
        DIR = input("Do you want to see the warning text for all warnings (Y/N): ")
        if DIR == "Y":
            ENDWARN = 99
            print("  Warnings (>5) that won't print and won't be sent to CMOP")
            print("  will be marked with a \"*\" on the following screens.")
        else:
            ENDWARN = 5
        print()
        DIR = input("Press Enter to continue: ")
        if not DIR:
            break

    if SEL == 1:
        SEL1()
    elif SEL == 2:
        SEL2()
    elif SEL == 3:
        SEL3()
    elif SEL == 4:
        SEL4()
    elif SEL == 5 or SEL == 9:
        SEL59()
    elif SEL == 6:
        SEL6()
    elif SEL == 7:
        SEL7()
    elif SEL == 8:
        SEL8()

    if not QUIT:
        EDIT()

    SEL()

def SEL1():
    pass

def SEL2():
    pass

def SEL3():
    pass

def SEL4():
    pass

def SEL59():
    pass

def SEL6():
    pass

def SEL7():
    pass

def SEL8():
    pass

def EDIT():
    pass

def PRT54():
    pass

def TITLE():
    pass

def END():
    pass

def RXCON():
    pass

def FULL():
    pass

def TITLE():
    pass

def END():
    pass

def PRTNEW():
    pass

def RPTNEW():
    pass

def FDBWARN():
    pass

def KILL():
    pass

def DRUG():
    pass

def WARN():
    pass

def ACTIVE():
    pass

def WARN():
    pass

def ACTIVE():
    pass

def PSSWRNB():
    pass

def NOTE():
    pass

def NOTE2():
    pass

def RPT():
    pass

def SEL():
    pass

def SEL1():
    pass

def SEL2():
    pass

def SEL3():
    pass

def SEL4():
    pass

def SEL59():
    pass

def SEL6():
    pass

def SEL7():
    pass

def SEL8():
    pass

def EDIT():
    pass

def SEL():
    pass

def FULL():
    pass

def TITLE():
    pass

def END():
    pass

def FULL():
    pass

def TITLE():
    pass

def END2():
    pass

def PRTNEW():
    pass

def FULL():
    pass

def TITLE():
    pass

def END2():
    pass

def KILL():
    pass

def DRUG():
    pass

def WARN():
    pass

def ACTIVE():
    pass

def PSSWRNB():
    pass

def NOTE():
    pass

def NOTE2():
    pass

def RPT():
    pass

def SEL():
    pass

def SEL1():
    pass

def SEL2():
    pass

def SEL3():
    pass

def SEL4():
    pass

def SEL59():
    pass

def SEL6():
    pass

def SEL7():
    pass

def SEL8():
    pass

def EDIT():
    pass

def KILL():
    pass

def DRUG():
    pass

def ACTIVE():
    pass

def PSSWRNB():
    pass

def NOTE():
    pass

def NOTE2():
    pass

def RPT():
    pass

def SEL():
    pass

def SEL1():
    pass

def SEL2():
    pass

def SEL3():
    pass

def SEL4():
    pass

def SEL59():
    pass

def SEL6():
    pass

def SEL7():
    pass

def SEL8():
    pass

def EDIT():
    pass

def SEL():
    pass

def FULL():
    pass

def TITLE():
    pass

def END():
    pass

def PRT54():
    pass

def PRTRPT():
    pass

def RXCON():
    pass

def FULL():
    pass

def FULL():
    pass

def TITLE():
    pass

def END():
    pass

def FULL():
    pass

def TITLE():
    pass

def END():
    pass

def DONE():
    pass

def PRT54():
    pass

def FULL():
    pass

def TITLE():
    pass

def END():
    pass

def PRTRPT():
    pass

def RXCON():
    pass

def FULL():
    pass

def FULL():
    pass

def TITLE():
    pass

def END():
    pass

def FULL():
    pass

def TITLE():
    pass

def END():
    pass

def DONE():
    pass

def PSSWRNB():
    pass

def SEQ():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def PSSPGLN():
    pass

def PSSPGCT():
    pass

def TITLE():
    pass

def SEQ():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def SEQ():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def END():
    pass

def PRTRPT():
    pass

def PSSPGCT():
    pass

def PSSPGLN():
    pass

def TITLE():
    pass

def SEQ():
    pass

def RXCON():
    pass

def FULL():
    pass

def FULL():
    pass

def FULL():
    pass

def FULL():
    pass

def FULL():
    pass

def TITLE():
    pass

def FULL():
    pass

def TITLE():
    pass

def END():
    pass

def FULL():
    pass

def TITLE():
    pass

def END2():
    pass

def TITLE():
    pass

def FULL():
    pass

def TITLE():
    pass

def END2():
    pass

def DONE():
    pass

def TITLE():
    pass

def FULL():
    pass

def DONE():
    pass

def TITLE():
    pass

def FULL():
    pass

def DONE():
    pass

def PRTNEW():
    pass

def FULL():
    pass

def TITLE():
    pass

def END2():
    pass

def FULL():
    pass

def TITLE():
    pass

def END2():
    pass

def KILL():
    pass

def SEQ():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def PSSPGLN():
    pass

def Y():
    pass

def SEQ():
    pass

def TITLE():
    pass

def FULL():
    pass

def TITLE():
    pass

def PSSPGCT():
    pass

def TITLE():
    pass

def PSSPGCT():
    pass

def PSSPGCT():
    pass

def SEQ():
    pass

def PSSPGCT():
    pass

def TITLE():
    pass

def END():
    pass

def FULL():
    pass

def TITLE():
    pass

def END():
    pass

def FULL():
    pass

def TITLE():
    pass

def END2():
    pass

def FULL():
    pass

def TITLE():
    pass

def END2():
    pass

def KILL():
    pass

def SEQ():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def PSSPGLN():
    pass

def Y():
    pass

def DIR():
    pass

def SEQ():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def SEQ():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def END():
    pass

def FULL():
    pass

def TITLE():
    pass

def END():
    pass

def PRTRPT():
    pass

def RXCON():
    pass

def FULL():
    pass

def FULL():
    pass

def TITLE():
    pass

def PSSPGCT():
    pass

def TITLE():
    pass

def END():
    pass

def FULL():
    pass

def TITLE():
    pass

def END():
    pass

def DONE():
    pass

def SEQ():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def PSSPGLN():
    pass

def Y():
    pass

def DIR():
    pass

def SEQ():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def SEQ():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def END():
    pass

def FULL():
    pass

def TITLE():
    pass

def END():
    pass

def PRTRPT():
    pass

def RXCON():
    pass

def FULL():
    pass

def FULL():
    pass

def TITLE():
    pass

def PSSPGCT():
    pass

def TITLE():
    pass

def END():
    pass

def FULL():
    pass

def TITLE():
    pass

def END():
    pass

def DONE():
    pass

def SEQ():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def PSSPGLN():
    pass

def Y():
    pass

def DIR():
    pass

def SEQ():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def SEQ():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def END():
    pass

def FULL():
    pass

def TITLE():
    pass

def END():
    pass

def PRTRPT():
    pass

def RXCON():
    pass

def FULL():
    pass

def FULL():
    pass

def TITLE():
    pass

def PSSPGCT():
    pass

def TITLE():
    pass

def END():
    pass

def FULL():
    pass

def TITLE():
    pass

def END():
    pass

def DONE():
    pass

def KILL():
    pass

def SEQ():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def PSSPGLN():
    pass

def Y():
    pass

def DIR():
    pass

def SEQ():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def SEQ():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def END():
    pass

def FULL():
    pass

def TITLE():
    pass

def END():
    pass

def PRTRPT():
    pass

def RXCON():
    pass

def FULL():
    pass

def FULL():
    pass

def TITLE():
    pass

def PSSPGCT():
    pass

def TITLE():
    pass

def END():
    pass

def FULL():
    pass

def TITLE():
    pass

def DONE():
    pass

def SEQ():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def PSSPGLN():
    pass

def Y():
    pass

def DIR():
    pass

def SEQ():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def SEQ():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def END():
    pass

def FULL():
    pass

def TITLE():
    pass

def END():
    pass

def PRTRPT():
    pass

def RXCON():
    pass

def FULL():
    pass

def FULL():
    pass

def TITLE():
    pass

def PSSPGCT():
    pass

def TITLE():
    pass

def END():
    pass

def FULL():
    pass

def TITLE():
    pass

def END():
    pass

def DONE():
    pass

def SEQ():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def PSSPGLN():
    pass

def Y():
    pass

def DIR():
    pass

def SEQ():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def SEQ():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def END():
    pass

def FULL():
    pass

def TITLE():
    pass

def END():
    pass

def PRTRPT():
    pass

def RXCON():
    pass

def FULL():
    pass

def FULL():
    pass

def TITLE():
    pass

def PSSPGCT():
    pass

def TITLE():
    pass

def END():
    pass

def FULL():
    pass

def TITLE():
    pass

def END():
    pass

def DONE():
    pass

def PSSWRNB():
    pass

def NOTE():
    pass

def NOTE2():
    pass

def RPT():
    pass

def SEL():
    pass

def SEL1():
    pass

def SEL2():
    pass

def SEL3():
    pass

def SEL4():
    pass

def SEL59():
    pass

def SEL6():
    pass

def SEL7():
    pass

def SEL8():
    pass

def EDIT():
    pass

def KILL():
    pass

def DRUG():
    pass

def ACTIVE():
    pass

def PSSWRNB():
    pass

def NOTE():
    pass

def NOTE2():
    pass

def RPT():
    pass

def SEL():
    pass

def SEL1():
    pass

def SEL2():
    pass

def SEL3():
    pass

def SEL4():
    pass

def SEL59():
    pass

def SEL6():
    pass

def SEL7():
    pass

def SEL8():
    pass

def EDIT():
    pass

def KILL():
    pass

def DRUG():
    pass

def ACTIVE():
    pass

def PSSWRNB():
    pass

def NOTE():
    pass

def NOTE2():
    pass

def RPT():
    pass

def SEL():
    pass

def SEL1():
    pass

def SEL2():
    pass

def SEL3():
    pass

def SEL4():
    pass

def SEL59():
    pass

def SEL6():
    pass

def SEL7():
    pass

def SEL8():
    pass

def EDIT():
    pass

def SEL():
    pass

def FULL():
    pass

def TITLE():
    pass

def END():
    pass

def PRT54():
    pass

def PRTRPT():
    pass

def RXCON():
    pass

def FULL():
    pass

def FULL():
    pass

def TITLE():
    pass

def END():
    pass

def FULL():
    pass

def TITLE():
    pass

def END():
    pass

def DONE():
    pass

def PRT54():
    pass

def FULL():
    pass

def TITLE():
    pass

def END():
    pass

def PRTRPT():
    pass

def RXCON():
    pass

def FULL():
    pass

def FULL():
    pass

def TITLE():
    pass

def END():
    pass

def FULL():
    pass

def TITLE():
    pass

def END():
    pass

def DONE():
    pass

def PRT54():
    pass

def FULL():
    pass

def TITLE():
    pass

def END():
    pass

def PRTRPT():
    pass

def RXCON():
    pass

def FULL():
    pass

def FULL():
    pass

def TITLE():
    pass

def END():
    pass

def FULL():
    pass

def TITLE():
    pass

def END():
    pass

def DONE():
    pass

def PSSWRNB():
    pass

def NOTE():
    pass

def NOTE2():
    pass

def RPT():
    pass

def SEL():
    pass

def SEL1():
    pass

def SEL2():
    pass

def SEL3():
    pass

def SEL4():
    pass

def SEL59():
    pass

def SEL6():
    pass

def SEL7():
    pass

def SEL8():
    pass

def EDIT():
    pass

def KILL():
    pass

def SEL():
    pass

def FULL():
    pass

def TITLE():
    pass

def END():
    pass

def PRT54():
    pass

def PRTRPT():
    pass

def RXCON():
    pass

def FULL():
    pass

def FULL():
    pass

def FULL():
    pass

def FULL():
    pass

def FULL():
    pass

def TITLE():
    pass

def FULL():
    pass

def TITLE():
    pass

def END():
    pass

def FULL():
    pass

def TITLE():
    pass

def END2():
    pass

def TITLE():
    pass

def FULL():
    pass

def TITLE():
    pass

def END2():
    pass

def DONE():
    pass

def TITLE():
    pass

def FULL():
    pass

def DONE():
    pass

def TITLE():
    pass

def FULL():
    pass

def DONE():
    pass

def PRTNEW():
    pass

def FULL():
    pass

def TITLE():
    pass

def END2():
    pass

def FULL():
    pass

def TITLE():
    pass

def END2():
    pass

def KILL():
    pass

def SEQ():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def PSSPGLN():
    pass

def Y():
    pass

def SEQ():
    pass

def TITLE():
    pass

def FULL():
    pass

def TITLE():
    pass

def PSSPGCT():
    pass

def TITLE():
    pass

def PSSPGCT():
    pass

def PSSPGCT():
    pass

def SEQ():
    pass

def PSSPGCT():
    pass

def TITLE():
    pass

def END():
    pass

def FULL():
    pass

def TITLE():
    pass

def END():
    pass

def FULL():
    pass

def TITLE():
    pass

def END2():
    pass

def FULL():
    pass

def TITLE():
    pass

def END2():
    pass

def KILL():
    pass

def SEQ():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def PSSPGLN():
    pass

def Y():
    pass

def SEQ():
    pass

def TITLE():
    pass

def FULL():
    pass

def TITLE():
    pass

def PSSPGCT():
    pass

def TITLE():
    pass

def END():
    pass

def FULL():
    pass

def TITLE():
    pass

def END():
    pass

def DONE():
    pass

def SEQ():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def PSSPGLN():
    pass

def Y():
    pass

def DIR():
    pass

def SEQ():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def SEQ():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def END():
    pass

def FULL():
    pass

def TITLE():
    pass

def END():
    pass

def PRTRPT():
    pass

def RXCON():
    pass

def FULL():
    pass

def FULL():
    pass

def TITLE():
    pass

def PSSPGCT():
    pass

def TITLE():
    pass

def END():
    pass

def FULL():
    pass

def TITLE():
    pass

def END():
    pass

def DONE():
    pass

def SEQ():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def PSSPGLN():
    pass

def Y():
    pass

def DIR():
    pass

def SEQ():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def SEQ():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def END():
    pass

def FULL():
    pass

def TITLE():
    pass

def END():
    pass

def PRTRPT():
    pass

def RXCON():
    pass

def FULL():
    pass

def FULL():
    pass

def TITLE():
    pass

def PSSPGCT():
    pass

def TITLE():
    pass

def END():
    pass

def FULL():
    pass

def TITLE():
    pass

def END2():
    pass

def TITLE():
    pass

def FULL():
    pass

def TITLE():
    pass

def END2():
    pass

def DONE():
    pass

def TITLE():
    pass

def FULL():
    pass

def DONE():
    pass

def TITLE():
    pass

def FULL():
    pass

def DONE():
    pass

def PRTNEW():
    pass

def FULL():
    pass

def TITLE():
    pass

def END2():
    pass

def FULL():
    pass

def TITLE():
    pass

def END2():
    pass

def KILL():
    pass

def SEQ():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def PSSPGLN():
    pass

def Y():
    pass

def DIR():
    pass

def SEQ():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def SEQ():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def END():
    pass

def FULL():
    pass

def TITLE():
    pass

def END():
    pass

def PRTRPT():
    pass

def RXCON():
    pass

def FULL():
    pass

def FULL():
    pass

def TITLE():
    pass

def PSSPGCT():
    pass

def TITLE():
    pass

def END():
    pass

def FULL():
    pass

def TITLE():
    pass

def END():
    pass

def DONE():
    pass

def SEQ():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def PSSPGLN():
    pass

def Y():
    pass

def DIR():
    pass

def SEQ():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def SEQ():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def END():
    pass

def FULL():
    pass

def TITLE():
    pass

def END():
    pass

def PRTRPT():
    pass

def RXCON():
    pass

def FULL():
    pass

def FULL():
    pass

def TITLE():
    pass

def PSSPGCT():
    pass

def TITLE():
    pass

def END():
    pass

def FULL():
    pass

def TITLE():
    pass

def END():
    pass

def DONE():
    pass

def SEQ():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def PSSPGLN():
    pass

def Y():
    pass

def DIR():
    pass

def SEQ():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def SEQ():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def END():
    pass

def FULL():
    pass

def TITLE():
    pass

def END():
    pass

def PRTRPT():
    pass

def RXCON():
    pass

def FULL():
    pass

def FULL():
    pass

def TITLE():
    pass

def PSSPGCT():
    pass

def TITLE():
    pass

def END():
    pass

def FULL():
    pass

def TITLE():
    pass

def END():
    pass

def DONE():
    pass

def KILL():
    pass

def SEQ():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def PSSPGLN():
    pass

def Y():
    pass

def DIR():
    pass

def SEQ():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def SEQ():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def END():
    pass

def FULL():
    pass

def TITLE():
    pass

def END():
    pass

def PRTRPT():
    pass

def RXCON():
    pass

def FULL():
    pass

def FULL():
    pass

def TITLE():
    pass

def PSSPGCT():
    pass

def TITLE():
    pass

def END():
    pass

def FULL():
    pass

def TITLE():
    pass

def END():
    pass

def DONE():
    pass

def SEQ():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def PSSPGLN():
    pass

def Y():
    pass

def DIR():
    pass

def SEQ():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def SEQ():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def END():
    pass

def FULL():
    pass

def TITLE():
    pass

def END():
    pass

def PRTRPT():
    pass

def RXCON():
    pass

def FULL():
    pass

def FULL():
    pass

def TITLE():
    pass

def PSSPGCT():
    pass

def TITLE():
    pass

def END():
    pass

def FULL():
    pass

def TITLE():
    pass

def END():
    pass

def DONE():
    pass

def SEQ():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def PSSPGLN():
    pass

def Y():
    pass

def DIR():
    pass

def SEQ():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def SEQ():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def END():
    pass

def FULL():
    pass

def TITLE():
    pass

def END():
    pass

def PRTRPT():
    pass

def RXCON():
    pass

def FULL():
    pass

def FULL():
    pass

def TITLE():
    pass

def PSSPGCT():
    pass

def TITLE():
    pass

def END():
    pass

def FULL():
    pass

def TITLE():
    pass

def END():
    pass

def DONE():
    pass

def PSSWRNB():
    pass

def SEQ():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def PSSPGLN():
    pass

def Y():
    pass

def DIR():
    pass

def SEQ():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def SEQ():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def END():
    pass

def FULL():
    pass

def TITLE():
    pass

def END():
    pass

def PRTRPT():
    pass

def RXCON():
    pass

def FULL():
    pass

def FULL():
    pass

def TITLE():
    pass

def PSSPGCT():
    pass

def TITLE():
    pass

def END():
    pass

def FULL():
    pass

def TITLE():
    pass

def END():
    pass

def DONE():
    pass

def SEQ():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def PSSPGLN():
    pass

def Y():
    pass

def DIR():
    pass

def SEQ():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def SEQ():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def END():
    pass

def FULL():
    pass

def TITLE():
    pass

def END():
    pass

def PRTRPT():
    pass

def RXCON():
    pass

def FULL():
    pass

def FULL():
    pass

def TITLE():
    pass

def PSSPGCT():
    pass

def TITLE():
    pass

def END():
    pass

def FULL():
    pass

def TITLE():
    pass

def END():
    pass

def DONE():
    pass

def KILL():
    pass

def SEQ():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def PSSPGLN():
    pass

def Y():
    pass

def DIR():
    pass

def SEQ():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def SEQ():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def END():
    pass

def FULL():
    pass

def TITLE():
    pass

def END():
    pass

def PRTRPT():
    pass

def RXCON():
    pass

def FULL():
    pass

def FULL():
    pass

def TITLE():
    pass

def PSSPGCT():
    pass

def TITLE():
    pass

def END():
    pass

def FULL():
    pass

def TITLE():
    pass

def END():
    pass

def DONE():
    pass

def SEQ():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def PSSPGLN():
    pass

def Y():
    pass

def DIR():
    pass

def SEQ():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def SEQ():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def END():
    pass

def FULL():
    pass

def TITLE():
    pass

def END():
    pass

def PRTRPT():
    pass

def RXCON():
    pass

def FULL():
    pass

def FULL():
    pass

def TITLE():
    pass

def PSSPGCT():
    pass

def TITLE():
    pass

def END():
    pass

def FULL():
    pass

def TITLE():
    pass

def END():
    pass

def DONE():
    pass

def SEQ():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def PSSPGLN():
    pass

def Y():
    pass

def DIR():
    pass

def SEQ():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def SEQ():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def END():
    pass

def FULL():
    pass

def TITLE():
    pass

def END():
    pass

def PRTRPT():
    pass

def RXCON():
    pass

def FULL():
    pass

def FULL():
    pass

def TITLE():
    pass

def PSSPGCT():
    pass

def TITLE():
    pass

def END():
    pass

def FULL():
    pass

def TITLE():
    pass

def END():
    pass

def DONE():
    pass

def SEQ():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def PSSPGLN():
    pass

def Y():
    pass

def DIR():
    pass

def SEQ():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def SEQ():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def END():
    pass

def FULL():
    pass

def TITLE():
    pass

def END():
    pass

def PRTRPT():
    pass

def RXCON():
    pass

def FULL():
    pass

def FULL():
    pass

def TITLE():
    pass

def PSSPGCT():
    pass

def TITLE():
    pass

def END():
    pass

def FULL():
    pass

def TITLE():
    pass

def END():
    pass

def DONE():
    pass

def KILL():
    pass

def SEQ():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def PSSPGLN():
    pass

def Y():
    pass

def DIR():
    pass

def SEQ():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def SEQ():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def END():
    pass

def FULL():
    pass

def TITLE():
    pass

def END():
    pass

def PRTRPT():
    pass

def RXCON():
    pass

def FULL():
    pass

def FULL():
    pass

def TITLE():
    pass

def PSSPGCT():
    pass

def TITLE():
    pass

def END():
    pass

def FULL():
    pass

def TITLE():
    pass

def END():
    pass

def DONE():
    pass

def SEQ():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def PSSPGLN():
    pass

def Y():
    pass

def DIR():
    pass

def SEQ():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def SEQ():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def END():
    pass

def FULL():
    pass

def TITLE():
    pass

def END():
    pass

def PRTRPT():
    pass

def RXCON():
    pass

def FULL():
    pass

def FULL():
    pass

def TITLE():
    pass

def PSSPGCT():
    pass

def TITLE():
    pass

def END():
    pass

def FULL():
    pass

def TITLE():
    pass

def END():
    pass

def DONE():
    pass

def KILL():
    pass

def SEQ():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def PSSPGLN():
    pass

def Y():
    pass

def DIR():
    pass

def SEQ():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def SEQ():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def END():
    pass

def FULL():
    pass

def TITLE():
    pass

def END():
    pass

def PRTRPT():
    pass

def RXCON():
    pass

def FULL():
    pass

def FULL():
    pass

def TITLE():
    pass

def PSSPGCT():
    pass

def TITLE():
    pass

def END():
    pass

def FULL():
    pass

def TITLE():
    pass

def END():
    pass

def DONE():
    pass

def SEQ():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def PSSPGLN():
    pass

def Y():
    pass

def DIR():
    pass

def SEQ():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def SEQ():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def END():
    pass

def FULL():
    pass

def TITLE():
    pass

def END():
    pass

def PRTRPT():
    pass

def RXCON():
    pass

def FULL():
    pass

def FULL():
    pass

def TITLE():
    pass

def PSSPGCT():
    pass

def TITLE():
    pass

def END():
    pass

def FULL():
    pass

def TITLE():
    pass

def END():
    pass

def DONE():
    pass

def SEQ():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def PSSPGLN():
    pass

def Y():
    pass

def DIR():
    pass

def SEQ():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def SEQ():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def END():
    pass

def FULL():
    pass

def TITLE():
    pass

def END():
    pass

def PRTRPT():
    pass

def RXCON():
    pass

def FULL():
    pass

def FULL():
    pass

def TITLE():
    pass

def PSSPGCT():
    pass

def TITLE():
    pass

def END():
    pass

def FULL():
    pass

def TITLE():
    pass

def END():
    pass

def DONE():
    pass

def KILL():
    pass

def SEQ():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def PSSPGLN():
    pass

def Y():
    pass

def DIR():
    pass

def SEQ():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def SEQ():
    pass

def MJT():
    pass

def PSSPGCT():
    pass

def END():
    pass

def FULL():
    pass

def TITLE():
    pass

def END():
    pass

def PRTRPT():
    pass

def RXCON():
    pass

def FULL():
    pass

def FULL():
    pass

def TITLE():
    pass

def PSSPGCT():
    pass

def TITLE():
    pass

def END():
    pass

def FULL():
    pass

def TITLE():
    pass

def END():
    pass

def DONE():
    pass

def KILL():
    pass

def DRUG():
    pass

def ACTIVE():
    pass

def PSSWRN():
    pass

def DRUG():
    pass

def WARN():
    pass

def WARN():
    pass

def ACTIVE():
    pass

def WARN():
    pass

def ACTIVE():
    pass

def PSSWRN():
    pass

def DRUG():
    pass

def WARN():
    pass

def WARN():
    pass

def ACTIVE():
    pass

def PSSWRN():
    pass

def DRUG():
    pass

def WARN():
    pass

def ACTIVE():
    pass

def PSSWRN():
    pass

def DRUG():
    pass

def WARN():
    pass

def ACTIVE():
    pass

def PSSWRN():
    pass

def DRUG():
    pass

def WARN():
    pass

def ACTIVE():
    pass

def PSSWRN():
    pass

def DRUG():
    pass

def WARN():
    pass

def ACTIVE():
    pass

def PSSWRN():
    pass

def DRUG():
    pass

def WARN():
    pass

def ACTIVE():
    pass

def PSSWRN():
    pass

def DRUG():
    pass

def WARN():
    pass

def ACTIVE():
    pass

def PSSWRN():
    pass

def DRUG():
    pass

def WARN():
    pass

def ACTIVE():
    pass

def PSSWRN():
    pass

def DRUG():
    pass

def WARN():
    pass

def ACTIVE():
    pass

def PSSWRN():
    pass

def DRUG():
    pass

def WARN():
    pass

def ACTIVE():
    pass

def PSSWRN():
    pass

PSSWRNB()