def PSSUTLPZ():
    print("The current Orderable Item structure keeps Additives and Solutions matched to")
    print("Orderable Items flagged for IV use. All Dispense Drugs are currently matched to")
    print("Orderable Items that are not flagged for IV Use. This was done")
    print("to control the finishing process of IV and Unit Dose orders entered through CPRS.")
    print("The new Orderable Item structure will inactivate all IV flagged Orderable")
    print("Items. All Additives and Solutions will be re-matched to non-IV flagged")
    print("Orderable Items, based on their Dispense Drug links.")

    input("Press Enter to continue...")

    PSSTYPE = input("Print report for Additives, Solutions, or Both (A/S/B): ")

def INS():
    CHECK()
    if PSSNOCON:
        del PSSNOCON
        return

    del PSSNOCON
    print("This option will move all non-numeric Instructions to the Noun field in the")
    print("Dosage Form file. If you do this, you will then need to review the Nouns and decide to mark them for Inpatient, Outpatient or both.")

    if input("Convert all non-numeric Instructions to Nouns (Y/N): ") != 'Y':
        print("Nothing converted.")
        return

    print("Converting...")
    for PSSD in range(0, len(PS50_606)):
        if PS50_606[PSSD]['INS']:
            for PSSI in range(0, len(PS50_606[PSSD]['INS'])):
                PSSINS = PS50_606[PSSD]['INS'][PSSI]
                if PSSINS and not PSSINS.isnumeric() and not PSSINS.replace('.', '').isnumeric():
                    if not PSS50_606[PSSD]['NOUN'].get(PSSINS):
                        PSS50_606[PSSD]['NOUN'][PSSINS] = {}
    print("Finished converting Instructions to Nouns!")

def NOUN():
    CHECK()
    if PSSNOCON:
        del PSSNOCON
        return

    del PSSNOCON
    PSSDOSE = int(input("Enter Dosage Form ID: "))
    print("Dosage Form =>", PS50_606[PSSDOSE]['NAME'])
    while True:
        PSSNOUN = int(input("Enter/edit Noun ID: "))
        if PSSNOUN < 1:
            break
        PSS50_606[PSSDOSE]['NOUN'][PSSNOUN]['NAME'] = input("Noun Name: ")
        PSS50_606[PSSDOSE]['NOUN'][PSSNOUN]['INPATIENT'] = input("Inpatient (Y/N): ") == 'Y'
        PSS50_606[PSSDOSE]['NOUN'][PSSNOUN]['OUTPATIENT'] = input("Outpatient (Y/N): ") == 'Y'
    PSS50_606[PSSDOSE]['PROMPT'] = input("Enter Prompt: ")

def CHECK():
    global PSSNOCON
    PSSYSIEN = PS59_7[0]
    if PS59_7[PSSYSIEN]['DOSAGE_CONVERSION_STATUS'] == 2:
        PSSNOCON = 1
        print("Cannot use this option, Dosage conversion is currently running!")