# COMPILED XREF FOR FILE #55.1153 ; 03/07/23

DA_1 = 0
DA = 0

# A1
if 'DISET' in globals():
    del DIKLM
    if DIKM1 == 2:
        DIKLM = 1
    elif DIKM1 != 2 and not DIKPUSH.get(2):
        DIKPUSH[2] = 1
        DA_2 = DA_1
        DA_1 = DA
        DA = 0
    goto = DIKM1

# A
DA_1 = next((i for i in range(DA_1+1, len(^PS(55, DA_2, "IV"))) if i > 0), 0)
if DA_1 <= 0:
    DA_1 = 0
    goto = "END"

# 1
DA = next((i for i in range(DA+1, len(^PS(55, DA_2, "IV", DA_1, 8))) if i > 0), 0)
if DA <= 0:
    DA = 0
    if DIKM1 == 1:
        goto = "A"

# 2
DIKZ_0 = ^PS(55, DA_2, "IV", DA_1, 8, DA, 0)
X = $P(DIKZ_0, U, 1)
if X != "":
    ^PS(55, DA_2, "IV", DA_1, 8, "B", $E(X, 1, 30), DA) = ""

if 'DIKLM' not in globals():
    goto = "B"
    if 'DISET' in globals():
        pass

# END
goto = "^PSSJXR39"