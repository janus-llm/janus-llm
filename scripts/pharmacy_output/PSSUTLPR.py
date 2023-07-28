def PSSUTLPR():
    print("\n\nThe current Orderable Item structure keeps Additives and Solutions matched to")
    print("Orderable Items flagged for IV use. All Dispense Drugs are currently matched to")
    print("Orderable Items that are not flagged for IV Use. This was done")
    print("to control the finishing process of IV and Unit Dose orders entered through CPRS.")
    print("The new Orderable Item structure will inactivate all IV flagged Orderable")
    print("Items. All Additives and Solutions will be re-matched to non-IV flagged")
    print("Orderable Items, based on their Dispense Drug links.")
    print()
    input("Press Enter to continue...")
    print()

    PSSTYPE = input("Print report for Additives, Solutions, or Both (A/S/B): ")
    while PSSTYPE not in ['A', 'S', 'B']:
        PSSTYPE = input("Invalid input. Print report for Additives, Solutions, or Both (A/S/B): ")
    print()


def INS():
    CHECK()
    if PSSNOCON:
        del PSSNOCON
        return
    del PSSNOCON

    print("\nThis option will move all non-numeric Instructions to the Noun field in the")
    print("Dosage Form file. If you do this, you will then need to review the Nouns and decide to mark them for Inpatient, Outpatient or both.")
    convert = input("Convert all non-numeric Instructions to Nouns (Y/N): ")
    if convert.upper() != 'Y':
        print("\nNothing converted.\n")
        return

    print("\nConverting..")
    for PSSD in range(0, len(PS_D_50_606)):
        if PS_D_50_606[PSSD]['INS']:
            for PSSI in range(0, len(PS_D_50_606[PSSD]['INS'])):
                PSSINS = PS_D_50_606[PSSD]['INS'][PSSI]
                if PSSINS and not PSSINS.isnumeric():
                    if not any(noun['NOUN'] == PSSINS for noun in PS_D_50_606[PSSD]['NOUN']):
                        PS_D_50_606[PSSD]['NOUN'].append({'NOUN': PSSINS})
    print("Finished converting Instructions to Nouns!\n")


def NOUN():
    CHECK()
    if PSSNOCON:
        del PSSNOCON
        return
    del PSSNOCON

    print()
    PSSDOSE = input("Dosage Form => ")
    while not any(dose['NAME'] == PSSDOSE for dose in PS_D_50_606):
        PSSDOSE = input("Invalid Dosage Form. Dosage Form => ")
    print()

    while True:
        print()
        print("Dosage Form => ", PSSDOSE)
        print()

        PSSNOUN = input("Select Noun: ")
        while not any(noun['NOUN'] == PSSNOUN for noun in PS_D_50_606[PSSDOSE]['NOUN']):
            if PSSNOUN == '':
                break
            PSSNOUN = input("Invalid Noun. Select Noun: ")
        if PSSNOUN == '':
            break

        PSSOTH = 1 if PS_P_59_7[1][40.2] else 0
        PS_D_50_606[PSSDOSE]['NOUN'][PSSNOUN] = {}
        PS_D_50_606[PSSDOSE]['NOUN'][PSSNOUN]['FIELD_1'] = input("Field 1: ")
        if not PSSOTH:
            continue
        PS_D_50_606[PSSDOSE]['NOUN'][PSSNOUN]['FIELD_3'] = input("Field 3: ")
        PS_D_50_606[PSSDOSE]['NOUN'][PSSNOUN]['FIELD_1'] = input("Field 1: ")
        PS_D_50_606[PSSDOSE]['NOUN'][PSSNOUN]['FIELD_2'] = input("Field 2: ")
    print()


def CHECK():
    global PSSNOCON
    PSSNOCON = 0
    PSSYSIEN = PS_P_59_7[0]
    if PS_P_59_7[PSSYSIEN][80][3] == 2:
        PSSNOCON = 1
    del PSSYSIEN
    if PSSNOCON:
        print("\a")
        print("\nCannot use this option, Dosage conversion is currently running!\n")


def TRAC():
    PSZZ1 = PS_P_59_7[0]
    PSZZ2 = PS_P_59_7[PSZZ1][80][3]
    if PSZZ2:
        PSZSTA = PS_P_59_7[PSZZ1][80][4].strftime("%m/%d/%Y")
        PSZSTO = PS_P_59_7[PSZZ1][80][5].strftime("%m/%d/%Y")
        PSZWHO = PS_P_59_7[PSZZ1][80][6]
    print("\n\nDosage Conversion Tracker Status")
    print("=" * 77)
    if not PSZZ2:
        print("The Dosage conversion has never been run!")
    elif PSZZ2 == 1:
        print(f"The Dosage conversion is queued to run at {PSZSTA}")
        print(f"It was queued by {PSZWHO}")
    elif PSZZ2 == 2:
        print(f"The Dosage conversion is currently running.")
        print(f"It started at {PSZSTA}")
    elif PSZZ2 == 3:
        print(f"The Dosage conversion was last run by {PSZWHO}")
        print(f"It started on {PSZSTA} and ended on {PSZSTO}")
    print()
    input("Press Enter to continue\n")


def FRE():
    print()
    PSSMED = input("Select Medication Instruction: ")
    while not any(med['NAME'] == PSSMED for med in PS_P_51):
        PSSMED = input("Invalid Medication Instruction. Select Medication Instruction: ")
    print()
    print()
    PSSFREQ = input("Enter Frequency: ")
    while not PSSFREQ.isnumeric():
        PSSFREQ = input("Invalid Frequency. Enter Frequency: ")
    print()


def FRRP():
    print("\nThis report shows the MEDICATION INSTRUCTION file entries, along with the")
    print("Synonym, Frequency and Expansion. Use the Edit Medication Instruction")
    print("Frequency option to enter appropriate frequencies.\n")

    if not PS_P_51:
        print("No MEDICATION INSTRUCTION file entries found.\n")
        return

    print("NAME".ljust(30), "SYNONYM".ljust(40), "FREQUENCY".ljust(25), "EXPANSION")
    print("=" * 79)

    for med in PS_P_51:
        print(med['NAME'].ljust(30), med['SYNONYM'].ljust(40), med['FREQUENCY'].ljust(25), med['EXPANSION'])

    print("\n")
    input("Press Enter to continue\n")


def SLS():
    if '/' not in PS_X[PSSA][PL3][1]:
        PS_X[PSSA][PL3][4] = PS_X[PSSA][PL3][0] + PS_X[PSSA][PL3][1]
        return

    PSSJ = PS_X[PSSA][PL3][0]
    PSSI = PS_X[PSSA][PL3][1]
    PSSWZI = PS_X[PSSA][PL3][5]
    PSSWZ50 = PS_D_50[PSSWZI]['DOS']
    PSSWZND = PSNAPIS(PS_D_50[PSSWZI]['ND'][0], PS_D_50[PSSWZI]['ND'][2])[1]
    PSSWZND = int(PSSWZND) if PSSWZND else 0

    PSSJA = PSSI.split('/')[0]
    PSSJB = PSSI.split('/')[1]

    if not PSSWZND:
        PS_X[PSSA][PL3][4] = PS_X[PSSA][PL3][0]
        return

    PSSWZSL2 = PSSWZ50 / PSSWZND
    PSSWZSL3 = PSSWZSL2 * int(PS_X[PSSA][PL3][2])
    PSSWZSL4 = PSSWZSL3 * (int(PSSJB) if PSSJB else 1)
    PSSWZSL5 = str(PSSWZSL4) + (PSSJB if PSSJB else '')

    PSSJ2 = str(int(PSSJA) * int(PSSJ)) + PSSJA + "/" + PSSWZSL5
    PSSJZUNT = PSSI.split('/')[0] + "/" + str(PSSWZSL4) + (PSSJB if PSSJB else '')
    PS_X[PSSA][PL3][1] = PSSJZUNT
    PS_X[PSSA][PL3][4] = PSSJ2


def ADDRP():
    PSSTYPE = input("Print report for Additives, Solutions, or Both (A/S/B): ")
    while PSSTYPE not in ['A', 'S', 'B']:
        PSSTYPE = input("Invalid input. Print report for Additives, Solutions, or Both (A/S/B): ")
    print()

    PSSYRX = (datetime.now() - timedelta(days=365)).strftime("%m/%d/%Y")

    if not PSSTYPE:
        return

    print("Orderable Item re-matching report")
    print("=" * 132)
    print()
    # Print the report based on PSSTYPE and PSSYRX
    print()
    print("End of Report.\n")


def PSNAPIS(PS1, PS2):
    # Implementation of PSNAPIS
    pass


PSSUTLPR()
INS()
NOUN()
TRAC()
FRE()
FRRP()
SLS()
ADDRP()