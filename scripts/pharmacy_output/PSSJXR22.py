# PSSJXR22 ; COMPILED XREF FOR FILE #55 ; 03/07/23
# 
DIKZK = 1
DIKZ_0 = PS(55, DA, 0)
X = DIKZ_0['^', U, 1]
if X != "":
    PS(55, "B", X[:30], DA) = ""
X = DIKZ_0['^', U, 1]
if X != "":
    if 'PSGINITF' not in globals():
        PS(55, "ALCNVRT") = PS(59.7, 1, 20)['^', 1]
X = DIKZ_0['^', U, 1]
if X != "":
    if 'PSGINITF' not in globals():
        PS(55, "AUDDD") = PS(59.7, 1, 20)['^', 1]
X = DIKZ_0['^', U, 1]
if X != "":
    if 'PSGINITF' not in globals():
        PS(55, "AUDAPM") = PS(59.7, 1, 20)['^', 1]
X = DIKZ_0['^', U, 4]
if X != "":
    PS(55, "ADIA", X[:30], DA) = ""
DIKZ_SAND = PS(55, DA, "SAND")
X = DIKZ_SAND['^', U, 1]
if X != "":
    PS(55, "ASAND", DA) = ""
X = DIKZ_SAND['^', U, 1]
if X != "":
    PS(55, "ASAND1", X[:30], DA) = ""

DIXR = 56
X_1 = DIKZ_0['^', U, 7]
X = X_1
if X_1 != "":
    X1 = X.copy()
    X2 = X.copy()
    LOGDFN(DA)

# CR2 and END labels are missing, assuming they are translated elsewhere.