def PSSMEDCH():
    print("\n\nThis report displays changes made to the mapping of Medication Routes in the")
    print("MEDICATION ROUTES (#51.2) File to Medication Routes in the STANDARD")
    print("MEDICATION ROUTES (#51.23) File.\n")
    PSSHTYPE = input("Print report for a Single Med Route, or All Med Routes (S/A): ")
    if PSSHTYPE != "S" and PSSHTYPE != "A":
        print("\nInvalid input. Exiting...")
        return

    if PSSHTYPE == "S":
        PSSMDONE = input("Select Med Route: ")
    else:
        PSSMDONE = None

    print()
    PSSMHRSI = input("Beginning Date: ")
    if not PSSMHRSI:
        print("\nInvalid input. Exiting...")
        return

    PSSMHRSE = PSSMHRSI
    PSSMHRSI += ".9999"

    print()
    PSSMHREI = input("Ending Date: ")
    if not PSSMHREI:
        print("\nInvalid input. Exiting...")
        return

    PSSMHREE = PSSMHREI
    PSSMHREI = str(int(PSSMHREI) + 1)

    print()
    if input("Do you want to print the report? (Y/N): ") != "Y":
        print("\nReport not printed.")
        return

    PSSMHDEV = "P"
    PSSMHCT = 1

    if PSSHTYPE == "S":
        PSSMHNAM = ""
        PSSMHLEN = 0

    HD()

    if PSSHTYPE == "S":
        # TODO: Implement logic for single med route report
        pass
    else:
        # TODO: Implement logic for all med routes report
        pass

    if not PSSMHOUT and not PSSMHRG9:
        print("\nNo mapping changes to report.")

    if PSSMHDEV == "P":
        print("\nEnd of Report.")
    elif not PSSMHOUT and PSSMHDEV == "C":
        print("\nEnd of Report.")
        input("Press Return to continue")

    if PSSMHDEV == "C":
        print("\n")
    else:
        print("\x0c")

def HD():
    if PSSMHDEV == "C" and PSSMHCT != 1:
        input("Press Return to continue, '^' to exit")

    print("\x0c")
    if PSSHTYPE == "A":
        print("Medication Route mapping changes for ALL Medication Routes")
    elif PSSHTYPE == "S":
        print("Medication Route mapping changes for", end=" ")
        if len(PSSMHNAM) < 43:
            print(PSSMHNAM)
        else:
            print("\n" + " " * 34 + PSSMHNAM)
    print("made between", PSSMHRSE, "and", PSSMHREE, "PAGE:", PSSMHCT, "\n" + "-" * 79 + "\n")
    PSSMHCT += 1