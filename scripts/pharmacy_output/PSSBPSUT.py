def NCPDPQTY(DRUG, RXQTY):
    """
    Return the NCPDP quantity (Billing Quantity)
    Input: (r) DRUG  - DRUG file (#50) IEN
           (r) RXQTY - Quantity dispensed from the PRESCRIPTION file (#52)) 
    Output: NCPDPQTY - Billing Quantity (3 decimal places)^NCPDP Dispense Unit (EA, GM or ML)
    """
    UNIT, MULTIP = None, None
    
    DRUG = int(DRUG)
    RXQTY = int(RXQTY)
    
    # Invalid DRUG IEN or DRUG not on file
    if not DRUG or not ^PSDRUG(DRUG,0):
        return "-1^INVALID DRUG"
    
    # Invalid NCPDP Dispense Unit
    UNIT = GET1^DIQ(50, DRUG, 82, "I")
    if UNIT != "EA" and UNIT != "GM" and UNIT != "ML":
        return str(RXQTY)
    
    # Invalid NCPDP Conversion Multiplier
    MULTIP = int(GET1^DIQ(50, DRUG, 83))
    if MULTIP <= 0:
        return str(RXQTY) + "^" + UNIT
    
    return "{:.3f}^{}".format(RXQTY * MULTIP, UNIT)


def EPHARM(PSSDRUG):
    """
    ePharmacy Billable fields check
    Check if the ePharmacy Billable fields are all nil. 
    If so, give the user the opportunity to input a value into the fields.
    Input: (r) PSSDRUG - DRUG file (#50) IEN
    """
    ARRAY, DA, DATA, DIE, DIR, DR, I, PSSDRUG1, TODAY, Y = {}, None, "", None, None, "", None, None, None
    
    PSSDRUG1 = str(PSSDRUG) + ","
    
    # Pull existing values from ^PSDRUG, for ePharmacy Billable fields, and put into ARRAY.
    GETS^DIQ(50, PSSDRUG1, "84;85;86;100", "I", ARRAY)
    
    # If INACTIVE DATE is not greater than today, QUIT. Do not check ePharmacy Billable Fields.
    TODAY = DT^XLFDT()
    if ARRAY[50, PSSDRUG1, 100, "I"] != "" and ARRAY[50, PSSDRUG1, 100, "I"] <= TODAY:
        return
    
    # Check the 3 fields in ARRAY. If any field has a value defined, QUIT.
    for I in [84, 85, 86]:
        if ARRAY[50, PSSDRUG1, I, "I"] != "":
            DATA = "1"
    
    if DATA == "1":
        return
    
    # All 3 fields were nil. Prompt user if they would like to enter values.
    DIR["A", 1] = " "
    DIR["A", 2] = "  None of the ePharmacy Billable fields are marked. ePharmacy claims"
    DIR["A", 3] = "  will not be billed if not marked. Do you wish to mark any of the"
    DIR["A"] = "  fields (Y/N)"
    DIR["0"] = "Y"
    ^DIR
    
    if Y != 1:
        return
    
    print()
    # Display the 3 ePharmacy Billable fields to the user.
    DIE = "^PSDRUG("
    DA = PSSDRUG
    DR = "84ePharmacy Billable;85  ePharmacy Billable (TRICARE);86  ePharmacy Billable (CHAMPVA)"
    ^DIE
    
    return