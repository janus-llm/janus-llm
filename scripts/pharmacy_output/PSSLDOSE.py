def PSSLDOSE():
    print("\nThis report will print Local Possible Dosage information only for Drugs for")
    print("which Dosage Checks can be performed. Drugs that are inactive, marked and/or")
    print("classed as supply items, not matched to NDF or excluded from dosage checks (due")
    print("to dosage form or VA Product override) will not be included in this report.")
    print("\nUsers will be able to print Local Possible Dosage information for all eligible")
    print("drugs or only for drugs with missing data in the Numeric Dose and Dose Unit")
    print("fields. These two fields must be populated to perform Dosage Checks for a Local")
    print("Possible Dosage selected when placing a Pharmacy order.")

    PSSKZTPE = input("\nEnter 'A' for All, 'O' for Only [O]: ").upper()
    
    if PSSKZTPE != "A" and PSSKZTPE != "O":
        print("\nInvalid input. Exiting...")
        return
    
    print("\nThis report is designed for 132 column format!")

    if input("\nPress Enter to continue or 'Q' to quit: ").upper() == "Q":
        print("\nExiting...")
        return
    
    # Print Local Possible Dosages Report
    PSSKZOUT = False
    PSSKZNOF = False
    PSSKZDEV = "P" if not os.isatty(0) else "C"
    PSSKZCT = 1
    PSSKZLIN = "-" * 130
    HD(PSSKZTPE, PSSKZCT, PSSKZLIN)

    for PSSKZNM in sorted(drug_list, key=str.lower):
        PSSKZIEN = drug_list[PSSKZNM]

        PSSKZOK, PSSKZDAT, PSSKZLIP, PSSKZZR, PSSKZNDF, PSSKZDF, PSSKZDT1, PSSKZLP1, PSSKZNFL, PSSKZMSG, PSSKZSTR, PSSKZUNT, PSSKZUNZ, PSSKZAPU, PSSKZ1, PSSKZ2, PSSKZ3, PSSKZND1, PSSKZND3 = False, False, 0, "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""
        PSSKZZR = drug_data[PSSKZIEN]["DRUG"]
        PSSKZSTR = drug_data[PSSKZIEN]["DOSAGE"]["STRENGTH"]
        PSSKZUNT = drug_data[PSSKZIEN]["DOSAGE"]["UNIT"]
        PSSKZNFL = drug_data[PSSKZIEN]["N/F"]
        PSSKZMSG = drug_data[PSSKZIEN]["MESSAGE"]
        PSSKZAPU = drug_data[PSSKZIEN]["PACKAGE"]
        PSSKZND1 = drug_data[PSSKZIEN]["ND"]["ND1"]
        PSSKZND3 = drug_data[PSSKZIEN]["ND"]["ND3"]

        PSSKZOK = TEST(PSSKZIEN, PSSKZND1, PSSKZND3)

        if not PSSKZOK:
            continue

        PSSKZDAT = False
        for PSSKZLIP in range(len(drug_data[PSSKZIEN]["DOSAGE"]["DOSES"])):
            if drug_data[PSSKZIEN]["DOSAGE"]["DOSES"][PSSKZLIP]:
                PSSKZDAT = True
                break

        if not PSSKZDAT:
            continue

        PSSKZDT1 = False
        if PSSKZTPE == "O":
            for PSSKZLP1 in range(len(drug_data[PSSKZIEN]["DOSAGE"]["DOSES"])):
                if drug_data[PSSKZIEN]["DOSAGE"]["DOSES"][PSSKZLP1]:
                    if not drug_data[PSSKZIEN]["DOSAGE"]["DOSES"][PSSKZLP1]["NUMERIC_DOSE"] or not drug_data[PSSKZIEN]["DOSAGE"]["DOSES"][PSSKZLP1]["DOSE_UNIT"]:
                        PSSKZDT1 = True
                        break
        
        if PSSKZTPE == "O" and not PSSKZDT1:
            continue
        
        PSSKZNOF = True
        print(f"\n({_PSSKZIEN})", "{:<16}".format(PSSKZZR + "  *N/F*" if PSSKZNFL else ""))
        
        if len(PSSKZMSG) > 0:
            print("{:>12}".format(PSSKZMSG))
        
        print("{:>12}".format(f"Strength: {PSSKZSTR}"), end="")
        if PSSKZUNT:
            print("{:>31}".format(f"Units: {PSSKZUNT}"))
            if len(PSSKZUNT) > 15:
                print()
        else:
            print("{:>31}".format("Units:"))
        print("{:>66}".format(f"Application Package: {PSSKZAPU}"))

        PSSKZ3 = False
        print("\n{:<20}".format("Local Possible Dosages:"), end="")
        for PSSKZ1 in range(len(drug_data[PSSKZIEN]["DOSAGE"]["DOSES"])):
            dose = drug_data[PSSKZIEN]["DOSAGE"]["DOSES"][PSSKZ1]
            if dose:
                if dose["NUMERIC_DOSE"] and dose["DOSE_UNIT"] and PSSKZTPE == "O":
                    continue
                PSSKZ3 = True
                print("\n{:<22}".format(dose["DOSE_NAME"]))
                print(f"\n{dose['NUMERIC_DOSE']}\t\t{dose['DOSE_UNIT']}\t\t{dose['PACKAGE']}")
        
        if not PSSKZ3:
            print("(None)")
        
        PSSKZNN1, PSSKZNN2 = "", ""
        if PSSKZND1 and PSSKZND3:
            PSSKZNN1 = PROD0(PSSKZND1, PSSKZND3)
            PSSKZNN2 = PSSKZNN1.split("^")[2]
            if PSSKZSTR and PSSKZNN2 and PSSKZNN2 != PSSKZSTR:
                print(f"\nNote: Strength of {PSSKZSTR} does not match NDF strength of {PSSKZNN2}.")
        
        print(f"\nVA PRODUCT MATCH: {PSSKZNN1.split('^')[0]}")
        HD(PSSKZTPE, PSSKZCT, PSSKZLIN)
        
        if PSSKZOUT:
            break
    
    if not PSSKZOUT and PSSKZTPE == "O" and not PSSKZNOF:
        print("\nNo local possible dosage missing data found.")
    
    if PSSKZDEV == "P":
        print("\nEnd of Report.")
    elif not PSSKZOUT and PSSKZDEV == "C":
        print("\nEnd of Report.")
        input("\nPress Enter to continue")
    
    if PSSKZDEV == "C":
        print()
    else:
        os.system("clear")

def HD(PSSKZTPE, PSSKZCT, PSSKZLIN):
    if PSSKZDEV == "C" and PSSKZCT != 1:
        if input("\nPress Enter to continue or '^' to exit: ").upper() == "^":
            print("\nExiting...")
            PSSKZOUT = True
            return
    print("\033c", end="")
    print(f"\nLocal Possible Dosages Report ({'All' if PSSKZTPE == 'A' else 'Missing Data Only'})")
    print(f"{'PAGE: '+str(PSSKZCT):>118}\n{PSSKZLIN}\n")
    PSSKZCT += 1

def TEST(PSSKZIEN, PSSKZND1, PSSKZND3):
    if not PSSKZND1 or not PSSKZND3:
        return False
    
    if DRUGS[PSSKZIEN]["I"]:
        if DRUGS[PSSKZIEN]["I"] < DT:
            return False
    
    PSSKZDOV = ""
    if PSSKZND1 and PSSKZND3 and hasattr(PSNAPIS, "OVRIDE"):
        PSSKZDOV = PSNAPIS.OVRIDE(PSSKZND1, PSSKZND3)
    
    if PSSKZZZR in ("S", "XA"):
        return False
    
    PSSKZDF = DRUGS[PSSKZIEN]["DF"]
    if not PSSKZDF and DRUGS[PSSKZIEN]["2"]:
        PSSKZDF = DRUGS[PSSKZIEN]["2"]
    
    if not PSSKZDF or not DRUGS[PSSKZIEN]["DF"]:
        return True
    
    if (DRUGS[PSSKZIEN]["DF"] and not PSSKZDOV) or (not DRUGS[PSSKZIEN]["DF"] and PSSKZDOV):
        return False
    
    return True

PSSLDOSE()