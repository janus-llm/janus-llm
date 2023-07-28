# PSSXREF  ;BIR/TTH-REINDEX "AND" X-REFERENCE ON DRUG FILE (#50) ; 4-FEB-2000 14:17
# 1.0; PHARMACY DATA MANAGEMENT;**31**;9/30/97

def INDEX():
    # Re-index AND cross-reference.
    DIK = "^PSDRUG("
    DIK(1) = "20^AND"
    ENALL^DIK()
    DIK = None

def DD202():
    # Remove Field.
    if $$VFIELD^DILFD(50,202):
        for XX in 0:
            XX = $O(^PSDRUG(XX))
            if not XX:
                break
            if $D(^PSDRUG(1,"CH")):
                DA = XX
                DIE = 50
                DR = "202///@"
                ^DIE()
                DA = None
                DIE = None
                DR = None
        DIK = "^DD(50,"
        DA = 202
        DA(1) = 50
        ^DIK()