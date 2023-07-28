# PSSJXR36 ; COMPILED XREF FOR FILE #55.11 ; 03/07/23

DA = [0, 0]

# A1
if 'DISET' in globals():
    del DIKLM
    if DIKM1 == 2:
        DIKLM = 1
    elif DIKM1 != 2 and not DIKPUSH.get(2):
        DIKPUSH[2] = 1
        DA[2] = DA[1]
        DA[1] = DA[0]
        DA[0] = 0
        eval(DIKM1)
# A
DA[1] = next((x for x in range(DA[1] + 1, len(^PS(55, DA[2], "IV"))) if x), 0)
if DA[1] <= 0:
    DA[1] = 0
    eval(END)
# 1
DA[0] = next((x for x in range(DA[0] + 1, len(^PS(55, DA[2], "IV", DA[1], "SOL"))) if x), 0)
if DA[0] <= 0:
    return
    eval(A)
# 2
DIKZ = [0, 0]
DIKZ[0] = ^PS(55, DA[2], "IV", DA[1], "SOL", DA[0], 0)
X = $piece(DIKZ[0], "^", 1)
if X != "":
    eval(^DD(55.11, .01, 1, 1, 1))
DIKZ[0] = ^PS(55, DA[2], "IV", DA[1], "SOL", DA[0], 0)
X = $piece(DIKZ[0], "^", 2)
if X != "":
    eval(^DD(55.11, 1, 1, 1, 1))
if not 'DIKLM' in globals():
    eval(B)
    if 'DISET' in globals():
        eval(END)
eval(^PSSJXR37)