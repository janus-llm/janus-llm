# COMPILED XREF FOR FILE #55.0109 ; 03/07/23

DA = 0

# A1
if 'DIKILL' in locals():
    del DIKLM
    if DIKM1 == 1:
        DIKLM = 1
    exec(f"{DIKM1}")  # Assuming @DIKM1 is translated elsewhere

# 0
A:
DA = DA(1).2.DA + 1
if DA <= 0:
    DA = 0
    GOTO END

# 1
DIKZ_0 = PS(55, DA(1), 2, DA, 0)
X = DIKZ_0.U.1
if X != "":
    del PS(55, DA(1), 2, "B", X[:30], DA)

if 'DIKLM' not in locals():
    GOTO A
if 'DIKILL' in locals():
    GOTO A
GOTO END

END:
GOTO PSSJXR6