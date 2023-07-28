# PSS164P ;BIR/WRT-Post install routine for 164 patch ;08/01/00
# ;1.0;PHARMACY DATA MANAGEMENT;**164**;9/30/97;Build 9
# ; POST-INSTALL ROUTINE-reindex FILE 51.24

def BEGIN():
    DIK = "^PS(51.24,"
    IXALL^DIK

def KILLIT():
    DIK = ""

BEGIN()
KILLIT()