# PSSINDRP ;BIR/MA - Indication Usage Report ;Apr 19, 2022@08:36:25
# ;1.0;PHARMACY DATA MANAGEMENT;**187**;9/30/97;Build 27
# ;External Reference to ^ORINDRP is supported by DBIA 7335

def PSSINDRP():
    # External Reference to ^ORINDRP is supported by DBIA 7335
    pass

def EN():
    # Call the EN^ORINDRP subroutine
    ORINDRP.EN()

EN()