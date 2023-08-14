# COMPILED XREF FOR FILE #55.1138 ; 03/07/23

DA[1] = 0
DA = 0

# A1
if 'DISET' in globals():
    DIKLM = None
    if DIKM1 == 2:
        DIKLM = 1
    elif DIKM1 != 2 and 'DIKPUSH' not in globals():
        DIKPUSH[2] = 1
        DA[2] = DA[1]
        DA[1] = DA
        DA = 0
    goto DIKM1

# A
DA[1] = $O(^PS(55, DA[2], "IV", DA[1]))
if DA[1] <= 0:
    DA[1] = 0
    goto END

# 1
DA = $O(^PS(55, DA[2], "IV", DA[1], 14, DA))
if DA <= 0:
    DA = 0
    if DIKM1 == 1:
        goto A

# 2
DIKZ[0] = $G(^PS(55, DA[2], "IV", DA[1], 14, DA, 0))
X = $P($G(DIKZ[0]), U, 1)
if X != "":
    ^PS(55, DA[2], "IV", DA[1], 14, "B", $E(X, 1, 30), DA) = ""

if 'DIKLM' not in globals():
    goto B
if 'DISET' in globals():
    goto B

# END
goto ^PSSJXR38