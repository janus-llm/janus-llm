def PSSNCPDP():
    return

def EN():
    ZZX = None
    if PSSNQM3:
        del PSSNQM3
    HDR()
    if "^PSDRUG" in globals() and DA in globals()["^PSDRUG"]:
        if globals()["^PSDRUG"][DA]["EPH"][1] == "EA":
            EACH()
        elif globals()["^PSDRUG"][DA]["EPH"][1] == "GM":
            GRAM()
        elif globals()["^PSDRUG"][DA]["EPH"][1] == "ML":
            MILL()
    print()
    return

def HDR():
    print("The value in the NCPDP QUANTITY MULTIPLIER field is multiplied by the")
    print("VISTA dispensed quantity of the drug for ePharmacy prescriptions,")
    print("resulting in the NCPDP quantity that should be electronically billed")
    print("to a Third Party Insurance Company.")
    return

def EACH():
    print()
    print("Most products with a NCPDP DISPENSE UNIT of EA (EACH) should have the")
    print("NCPDP QUANTITY MULTIPLIER field set to 1 (one) because the VA dispensed")
    print("quantity is the same quantity that should be billed to the Third Party")
    print("Insurance Companies. HOWEVER some exceptions require a value different")
    print("than 1 (one). See examples below:")
    print()
    print("Drug: ORTHO TRI-CYCLEN TAB,28    Quantity Dispensed: 3 CYCLES")
    print()
    print("The Quantity Dispensed above indicates how many 28-day cycles are")
    print("being dispensed (3). However, the Third Party Insurance Companies need")
    print("to know how many TABLETS are being dispensed. Therefore, the correct")
    print("value for the NCPDP QUANTITY MULTIPLIER would be 28. The correct quantity")
    ZZX = input("Enter to continue:  ")
    print()
    print("to submit electronically is 3 x 28 = 84 tablets.")
    print()
    print("A similar case is METHYLPREDNISOLONE 4MG TAB DOSEPAK,21, which is")
    print("dispensed in packages (PKG) and not in tablets. The NCPDP QUANTITY")
    print("MULTIPLIER for this product is 21.")
    return

def GRAM():
    print()
    print("Most products with a NCPDP DISPENSE UNIT of GM (GRAMS) should have the")
    print("NCPDP QUANTITY MULTIPLIER set to 1 (one). HOWEVER for products dispensed")
    print("in units such as TUBE, the NCPDP QUANTITY MULTIPLIER field should contain")
    print("the number of GRAMS contained in 1 TUBE. See examples below:")
    print()
    print("Drug:  GENTAMICIN SO4 0.3% OINT,OPH   Quantity Dispensed: 1 TUBE")
    print()
    print("The Quantity Dispensed above indicates how many tubes are being dispensed")
    print("(1). However, the Third Party Insurance Companies need to know how many")
    print("GRAMS are being dispensed. The correct value for the NCPDP QUANTITY")
    ZZX = input("Enter to continue:  ")
    print()
    print("MULTIPLIER field for this product is 3.5, because there are 3.5 grams in")
    print("each tube. The correct quantity to submit electronically will be")
    print("3.5 x 1 = 3.5 grams.")
    print()
    print("Another example is IPRATROPIUM BR 17MCG/SPRAY AEROSOL,INHL., which is")
    print("dispensed by the number of inhalers used to fill the prescription. Each")
    print("inhaler contains 12.9 grams of IPRATROPIUM, so the NCPDP QUANTITY")
    print("MULTIPLIER for this product will be 12.9.")
    return

def MILL():
    print()
    print("Most products with a NCPDP DISPENSE UNIT of ML (Milliliters) should have")
    print("this field set to 1 (one). HOWEVER for some drugs that are dispensed in")
    print("units such as VIAL or BOTTLE, the NCPDP QUANTITY MULTIPLIER field should")
    print("contain the number of MILILLITERS contained in 1 VIAL or BOTTLE for this")
    print("drug. See examples below:")
    print()
    print("Drug:   INSULIN,NPH,HUMAN 100UNT/ML INJ   Quantity Dispensed  3 VIALS")
    print()
    print("The Quantity Dispensed above indicates how many vials are being dispensed")
    print("(3). However, the Third Party Insurance Companies need to know how many")
    print("milliliters are being dispensed. The correct value for the NCPDP QUANTITY")
    ZZX = input("Enter to continue:  ")
    print()
    print("MULTIPLIER field for this product is 10, because there are 10 milliliters")
    print("in each vial. The correct quantity to submit electronically will be ")
    print("3 x 10 = 30 milliliters.")
    print()
    print("Another example is DARBEPOETIN ALFA,RECOMBINANT 150MCG/0.3ML SYR INJ,")
    print("SURECLICK which is dispensed by the number of syringes used for the ")
    print("prescription. Each syringe contains 0.3 ML of DARBEPOETIN, so the NCPDP")
    print("QUANTITY MULTIPLIER for this product will be 0.3. Notice in this case the")
    print("NCPDP QUANTITY MULTIPLIER is less than 1.")
    print()
    return

def _12():
    if not PSDOSE:
        PSDOSE = globals()["^PS(50.7)"][DA][0]
    if X < 1 and PSDOSE and globals()["^PS(50.606)"][PSDOSE][0] != "PATCH":
        return
    if X > 0 and PSDOSE and globals()["^PS(50.606)"][PSDOSE][0] != "PATCH":
        val = X
        print("The dosage form for this orderable item is not PATCH.")
        del DIR, DIRUT, DUOUT, DTOUT
        DIR = {"0": "Y", "B": "N", "A": "Are you sure you want to designate this medication as requiring removal", "?": "Enter Y for Yes or N for No."}
        if not DIR["0"] in ["Y", "N"]:
            return
        if not Y:
            X = globals()["^PS(50.7)"][DA][4]
            print("No Changes were recorded.")
            return
        if Y:
            X = val
    return

def D12():
    print("ENTRY OF 1, 2 OR 3 IS REQUIRED FOR DOSAGE FORM PATCH.")
    print("Enter the value that applies to this orderable item.")
    print("Choose from:")
    print("1        Removal at Next Administration")
    print("2        Removal Period Optional Prior to Next Administration")
    print("3        Removal Period Required Prior to Next Administration")
    print(" ")
    return

def D13():
    PSDOSE = globals()["^PS(50.7)"][DA][0]
    if PSDOSE and globals()["^PS(50.606)"][PSDOSE][0] == "PATCH":
        print("ENTRY OF 1, 2 OR 3 IS REQUIRED FOR DOSAGE FORM PATCH.")
    print("Enter the value that applies to this orderable item.")
    return