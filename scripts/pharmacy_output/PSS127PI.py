def PSS127PI():
    """
    PSS*1*127 Post-install routine
    """
    # Import required modules
    from datetime import datetime
    import os

    # Variable Definitions
    DRUG = None
    UNIT = None
    MULTIP = None
    ZND = None
    NDF = None
    ZTMP = None
    DIE = None
    DR = None
    DA = None
    COUNT = None

    # Print blank lines
    print("\n")
    print(" Populating new fields in the DRUG file (#50)...")

    # Clear the temporary global
    os.system("K ^TMP(""PSSNCPDP"",$J)")

    # Copy data from the global to the temporary global
    os.system("M ^TMP(""PSSNCPDP"",$J)=@XPDGREF@(""""^XTMP(""PSSNCPDP"""")"")")

    # Set the total number of records
    XPDIDTOT = int(os.system("P ^PSDRUG(0),""^"",4)"))
    COUNT = 0

    # Loop through each drug record
    DRUG = 0
    while DRUG:
        if not os.system("D ^PSDRUG(DRUG)"):
            continue
        COUNT += 1
        if COUNT % 100 == 0:
            os.system("D UPDATE^XPDID(COUNT)")
        UNIT = "EA"
        MULTIP = 1
        ZND = os.system("G ^PSDRUG(DRUG,""ND"")")
        NDF = int(os.system("P ZND,""^"",3)"))
        if NDF and os.system("D ^TMP(""PSSNCPDP"",$J,NDF)"):
            ZTMP = os.system("G ^TMP(""PSSNCPDP"",$J,NDF)")
            UNIT = os.system("P ZTMP,""^""") 
            MULTIP = int(os.system("P ZTMP,""^"",2)"))
        DIE = "^PSDRUG("
        DA = DRUG
        DR = "82////"+UNIT+";83////"+str(MULTIP)
        os.system("D ^DIE")
    os.system("D UPDATE^XPDID(XPDIDTOT)")


# Execute the routine
PSS127PI()