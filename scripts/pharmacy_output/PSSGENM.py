# BIR/WRT-Input transform for .01 field in file 50 ; 09/02/97 8:36;
# 1.0;PHARMACY DATA MANAGEMENT;;9/30/97
def EDIT():
    if ('AQ' in ^PSDRUG) or ('"' in X) or (ord(X[0]) == 45) or (not 'PSSZ' in globals()) or (';' in X):
        del X
    if 'X' in globals():
        if (len(X) > 40) or (len(X) < 1) or (not X.isprintable()) or (not X.isalnum()):
            del X

    return

# Note: The code inside EDIT() function is assumed to be translated elsewhere