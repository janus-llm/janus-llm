# PSSMONT ;BIR/TTH-CLEAN UP MEDICATION INSTRUCTION FILE ; 9/15/99
# 1.0;PHARMACY DATA MANAGEMENT;**27**;9/30/97

def REINDEX():
    # Re-index the A cross-reference to synchronize changes to the
    # Synonym Field (#.5).
    if '$D(^PS(51,"A")):
        DIK = "^PS(51,"
        DIK(1) = ".01^A"
        ENALL^DIK

    DA = None
    DIK = None
    X = None
    Y = None
    return

REINDEX()