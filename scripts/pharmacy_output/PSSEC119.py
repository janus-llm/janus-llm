# PSSEC119 ;RJS-Environment check routine for PSS*1*119 ; 05/30/07
# 1.0;PHARMACY DATA MANAGEMENT;**119**;9/30/97;Build 9

PSSFL1 = ""
PSSFL2 = ""
if any(x for x in ^PSX(550,"C") if x != 0) or ^XMB("NETNAME").startswith("CMOP-"):
    print("\n\n\tConsolidated Mail Outpatient Pharmacy Install.\n\n")
    XPDQUIT = 1
else:
    if not $$PATCH^XPDUTL("PSJ*5.0*194"):
        PSSFL1 = 1  # Required patch
    if not $$PATCH^XPDUTL("PSO*7.0*282"):
        PSSFL2 = 1  # Required patch

    if PSSFL1 == 1 or PSSFL2 == 1:
        # Logic to notify the IRM
        print("\n\n\t****************************************************************************")
        print("\t*", "\tWARNING", "\t\t\t\t\t\t\t\t\t\t\t\t\t", "*")
        print("\t*", "\t\t\t\t\t\t\t\t\t\t\t\t\t", "*")
        if PSSFL1 == 1:
            print("\t*", "\tRequired patch PSJ*5.0*194 is not installed.", "\t\t\t\t\t", "*")
        if PSSFL2 == 1:
            print("\t*", "\tRequired patch PSO*7.0*282 is not installed.", "\t\t\t\t\t", "*")
            print("\t*", "\t\t\t\t\t\t\t\t\t\t\t\t\t", "*")
        print("\t*", "\tPlease install the above mentioned required patch(es).", "\t\t\t\t*", "")
        print("\t*", "\tOnce the required patch(es) are installed, you can reinstall(PSS*1.0*119).*", "\t\t\t", "*")
        print("\t****************************************************************************")
        XPDQUIT = 1  # This will cause the install to quit and delete the transport global.