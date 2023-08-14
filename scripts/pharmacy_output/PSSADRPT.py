def PSSADRPT():
    # IV Additive report
    print("\nThis report displays entries in the IV ADDITIVES (#52.6) File. You can select")
    print("to display only entries marked with '1 BAG/DAY' in the ADDITIVE FREQUENCY (#18)")
    print("Field, or only those entries with nothing entered in the ADDITIVE FREQUENCY")
    print("(#18) Field, or all entries can be displayed.")
    PSSKFTP = input("Print which IV Additives (1: Print entries marked as '1 BAG/DAY' for ADDITIVE FREQUENCY; N: Print entries marked as Null for ADDITIVE FREQUENCY; A: Print all IV Additives): ")
    
    print("\nThis report is designed for 80 column format!\n")
    
    # Check if report should be printed or queued
    print_queued = False
    if input("Print immediately or queue? (P: Print immediately; Q: Queue): ") == "Q":
        print_queued = True

    if print_queued:
        print("Report queued to print.")
    else:
        print("Printing report...")

    # Start report
    print("\nIV Additives Report")
    print("-" * 79)

    # Loop through IV Additives
    for PSSKFMXX in sorted(PSSKFMXX_list):
        # Get IV Additive details
        PSSKFMIN = get_IV_additive_id(PSSKFMXX)
        PSSKFMAR = get_IV_additive_data(PSSKFMIN)

        # Filter IV Additives based on selection
        if PSSKFTP == "1" and PSSKFMAR["ADDITIVE FREQUENCY"] != "1 BAG/DAY":
            continue
        if PSSKFTP == "N" and PSSKFMAR["ADDITIVE FREQUENCY"] != "":
            continue

        # Print IV Additive details
        print("\nPrint Name:", PSSKFMAR[".01"])
        print("Drug Unit:", PSSKFMAR["2"])
        print("Synonyms:")
        PSSKFMSY_list = get_synonyms(PSSKFMIN)
        for PSSKFMSY in PSSKFMSY_list:
            print(" " * 10, PSSKFMSY)
        print("Generic Drug:", PSSKFMAR["1"])
        print("Pharmacy Orderable Item:", PSSKFMAR["15"])
        print("Inactivation Date:", PSSKFMAR["12"])
        print("Used in IV Fluid Order Entry:", PSSKFMAR["17"])
        print("Additive Frequency:", PSSKFMAR["18"])

    # End of report
    if PSSKFTP == "1":
        print("\nNo IV Additives marked as '1 BAG/DAY'.")
    elif PSSKFTP == "N":
        print("\nNo IV Additives marked as null.")
    else:
        print("\nNo IV Additives to print.")

    if not print_queued:
        input("Press Enter to continue")

PSSADRPT()