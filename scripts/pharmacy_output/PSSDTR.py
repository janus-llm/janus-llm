def PSSDTR():
    # BIR/EJW-Print Drug Text Report
    pass

    # 1.0;PHARMACY DATA MANAGEMENT;**55**;9/30/97

    # Reference to $$FORMRX^PSNAPIS(DA,K,.LIST) supported by DBIA #2574

    print("\nThis report shows each selected drug text entry and lists all drugs")
    print("and orderable items linked to it.\n")

    PSSHOW = input("Print for (A)ll or (S)elect Single Entry or Range (A/S): ")
    if PSSHOW.upper() == "A":
        PSSBEG = ""
        PSSEND = "Z"
        PSSSRT = "A"
        TASK()
    elif PSSHOW.upper() == "S":
        PSSNUMB = ""
        while True:
            PSSNUMB = input("Print report for drug text entries with leading numerics? (Y/N): ")
            if PSSNUMB.upper() == "Y":
                PSSSRT = "N"
                TASK()
                break
            elif PSSNUMB.upper() == "N":
                break
            else:
                print("Invalid response. Please enter Y or N.")

    PSSBEG = input("Enter a single drug text entry or to see all drug text entries beginning with\n"
                   "the letter 'A' for example, enter 'A' or whichever letter you wish to see.\n"
                   "To see drug text entries in a range for example starting with 'H', 'I' and 'J'\n"
                   "enter in the format 'H-J': ")
    if PSSBEG:
        PSSSRT = "X"
        TASK()

def TASK():
    if PSSSRT == "X" and len(PSSBEG) > 1 and "-" not in PSSBEG:
        PSSSRT = "S"
    
    if PSSSRT == "X":
        print(f"\nReport will be for drug text starting with {PSSBEG},\n"
              f"and ending with drug text starting with {PSSEND}.\n")
    elif PSSSRT == "N":
        print("\nThis report will be for drug text with leading numerics.\n")
    elif PSSSRT == "A":
        print("\nThis report will be for all drug text entries.\n")
    elif PSSSRT == "S":
        print(f"\nThis report will be for drug text entry: {PSSBEG}\n")

    confirm = input("Is this correct? (Y/N): ")
    if confirm.upper() != "Y":
        PSSDTR()
    
    START()

def START():
    PSSOUT = 0
    PSSDV = "C" if input("Print to (C)onsole or (P)rinter (C/P): ").upper() == "C" else "P"
    PSSPGCT = 0
    PSSPGLN = 20  # Adjust to desired page length
    PSSPGCT = 1
    TITLE()
    
    if PSSSRT == "X":
        PSSX = ord(PSSBEG) - 1
        PSSLCL = chr(PSSX) + "zzzz"
    elif PSSSRT in ["N", "A"]:
        PSSLCL = ""
    
    if PSSSRT != "S":
        for PSSLCL in sorted(list(filter(lambda x: PSSSRT == "N" and not x or
                                                     PSSSRT == "X" and x > PSSEND + "zzzz" or
                                                     not x or
                                                     PSSSRT == "N" and not x or
                                                     PSSSRT == "X" and x > PSSEND + "zzzz",
                                          ^PS(51.7,"B")))):
            DTXTRPT()

    if PSSSRT == "S" and PSSBEG and PSSBEG in ^PS(51.7,"B"):
        PSSLCL = PSSBEG
        DTXTRPT()

def DTXTRPT():
    DTNAME()

    for PSSB in ^PS(51.7,"B"):
        if ^PS(51.7,PSSB,0):
            DTEXT()
            OITEXT()

def DTNAME():
    print(f"\nDRUG TEXT NAME:  {PSSLCL}")

    if ^PS(51.7,PSSB,0):
        Y = +^PS(51.7,PSSB,0)[1]
        print(f"** INACTIVE DATE:  {Y} **")

    PSSSYN = 0
    if ^PS(51.7,PSSB,1,0):
        print("\nSYNONYM(S):")
        for PSSSYN in ^PS(51.7,PSSB,1):
            print(f"  {PSSSYN[0]}")

    if ^PS(51.7,PSSB,2,0):
        print("\nDRUG TEXT:")
        for PSSTXT in ^PS(51.7,PSSB,2):
            print(f"  {PSSTXT[0]}")

    NRESTR()

def DTEXT():
    print("\nDRUG file entries:\n-----------------")
    if not ^PSDRUG("DTXT",PSSB):
        print("NONE")
    else:
        for PSSDRG in ^PSDRUG("DTXT",PSSB):
            print(f"  {^PSDRUG(PSSDRG,0)[1]}")
            if ^PSDRUG(PSSDRG,"I"):
                Y = +^PSDRUG(PSSDRG,"I")[1]
                print(f"** INACTIVE DATE:  {Y} **")

def OITEXT():
    print("\nORDERABLE ITEM file entries:\n---------------------------")
    if not ^PS(50.7,"DTXT",PSSB):
        print("NONE")
    else:
        for PSSDRG in ^PS(50.7,"DTXT",PSSB):
            print(f"  {^PS(50.7,PSSDRG,0)[1]}  {^PS(50.606,^PS(50.7,PSSDRG,0)[2],0)[1]}")
            if ^PS(50.7,PSSDRG,0)[4]:
                Y = +^PS(50.7,PSSDRG,0)[4]
                print(f"** INACTIVE DATE:  {Y} **")

def NRESTR():
    for PSSDRG in ^PSDRUG("DTXT",PSSB):
        if ^PSDRUG(PSSDRG,"ND"):
            PSXDN = ^PSDRUG(PSSDRG,"ND")
            PSXGN = PSXDN[0]
            PSXVP = PSXDN[2]
            if PSXGN and PSXVP:
                print("\nNATIONAL FORMULARY RESTRICTION TEXT:")
                XX2 = $$FORMRX^PSNAPIS(PSXGN, PSXVP, .LIST)
                if XX2 == 1 and LIST:
                    for XX2 in LIST:
                        print(f"  {XX2[0]}")

    LIST = []

def FULL():
    if PSSOUT:
        return
    if PSSDV == "C" and ($Y + 5) > PSSPGLN:
        TITLE()

def FULL2():
    if PSSOUT:
        return
    if PSSDV == "C" and ($Y + 6) > PSSPGLN:
        TITLE()

def TITLE():
    if PSSDV == "C" and PSSPGCT != 1:
        input("Press Enter to continue...")
    print("\n" + "=" * 79)
    print("PLEASE NOTE: The National Formulary Restriction Text is the original text")
    print("exported with the DRUG TEXT file (#51.7) and automatically linked to the DRUG")
    print("file (#50) entries based on the VA product match. No ORDERABLE ITEM file")
    print("(#50.7) entries were automatically linked with DRUG TEXT file (#51.7).\n")
    print("Date printed:", DT(), " " * 60, "Page:", PSSPGCT)
    print("=" * 79)
    PSSPGCT += 1

def DONE():
    if not PSSOUT and PSSDV == "C":
        print("\nEnd of Report.")
        input("Press Enter to continue...")
    print()

PSSDTR()