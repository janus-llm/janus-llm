# COMPILED XREF FOR FILE #55.05 ; 03/07/23

DA = 0

# A1
if 'DIKILL' in locals():
    if 'DIKM1' in locals():
        DIKLM = 1
    goto DIKM1

# 0
A:
DA = next((x for x in range(DA + 1, len(PS[55][DA(1)]["NVA"])) if x in PS[55][DA(1)]["NVA"]), 0)
if DA <= 0:
    DA = 0
    goto END

# 1
DIKZ_0 = PS[55][DA(1)]["NVA"][DA][0]
X = DIKZ_0[6]
if X != "":
    if 'PSODEATH' in globals():
        del PS[55][DA(1)]["NVA"]["APSOD"][DA]
X = DIKZ_0[10]
if X != "":
    del PS[55]["ADCDT"][X[:30]][DA(1)][DA]
X = DIKZ_0[1]
if X != "":
    del PS[55][DA(1)]["NVA"]["B"][X[:30]][DA]

# CR1
DIXR = 452
X = [DIKZ_0[1], DIKZ_0[10], DIKZ_0[9], DIKZ_0[7]]
if X[0] != "" and X[1] != "":
    X1, X2 = X, X
    if 'DIKIL' in locals():
        X2 = ["", "", "", "", ""]
    KNVA(X, DA)

# CR2
if 'DIKLM' not in locals():
    goto A
if 'DIKILL' in locals():
    goto END

# END
goto PSSJXR8