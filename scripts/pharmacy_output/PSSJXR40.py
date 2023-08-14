# COMPILED XREF FOR FILE #55.516 ; 03/07/23

DA = 0
DA_1 = 0

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
DA_1 = next((x for x in range(DA_1 + 1, len(^PS(55, DA_2, "NVA"))) if ^PS(55, DA_2, "NVA", x) exists), 0)

if DA_1 <= 0:
    DA_1 = 0
    goto = "END"

# 1
DA = next((x for x in range(DA + 1, len(^PS(55, DA_2, "NVA", DA_1, 3))) if ^PS(55, DA_2, "NVA", DA_1, 3, x) exists), 0)

if DA <= 0:
    if DIKM1 == 1:
        goto = "A"
    else:
        goto = "A"

# 2
DIKZ_0 = ^PS(55, DA_2, "NVA", DA_1, 3, DA, 0)
X = DIKZ_0.split("^")[0]

if X != "":
    ^PS(55, DA_2, "NVA", DA_1, 3, "B", X[:30], DA) = ""

if 'DIKLM' not in globals():
    goto = "B"
    if 'DISET' in globals():
        goto = "B"

goto = "END"
goto = "PSSJXR41"