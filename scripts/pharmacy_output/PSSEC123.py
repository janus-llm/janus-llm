# JD-Environment check routine for PSS*1*123 ; 6/6/07 2:27pm
# 1.0;PHARMACY DATA MANAGEMENT;**123**;9/30/97;Build 6
# Reference to $$PATCH^XPDUTL(X) supported by DBIA #10141
# Reference to ^XMB("NETNAME") supported by DBIA #1131

import XPDUTL

PSSFL1 = ""
PSSFL2 = ""
PSSSTR = ""
PSSSTR = PSSSTR + "*"*77

if XMB("NETNAME").startswith("CMOP-"):
    print("\n", " "*10, "Consolidated Mail Outpatient Pharmacy Install.", "\n")
    exit()

# Not a CMOP site. Check for required patches.
# Required patches are PSJ*5.0*134 and OR*3.0*243
if not XPDUTL.PATCH("PSJ*5.0*134"):
    PSSFL1 = 1  # Required patch

if not XPDUTL.PATCH("OR*3.0*243"):
    PSSFL2 = 1  # Required patch

if PSSFL1 == 1 or PSSFL2 == 1:
    # Logic to notify the IRM
    print("\n", " "*2, PSSSTR)
    print(" ", "*", " "*34, "WARNING", " "*77, "*", "\n", " ", "*", " "*77, "*")
    
    if PSSFL1 == 1:
        print(" ", "*", " "*14, "Required patch PSJ*5.0*134 is not installed.", " "*77, "*")
    if PSSFL2 == 1:
        print(" ", "*", " "*14, "Required patch OR*3.0*243 is not installed.", " "*77, "*", "\n", " ", "*", " "*77, "*")
    
    print(" ", "*", " "*10, "Please install the above mentioned required patch(es).", " "*77, "*")
    print(" ", "*", "Once the required patch(es) are installed, you can reinstall", " "*77, "*")
    print(" ", "*", "patch PSS*1.0*123.", " "*77, "*")
    print(" ", PSSSTR)
    exit()