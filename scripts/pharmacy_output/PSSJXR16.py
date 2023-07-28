# PSSJXR16 ; COMPILED XREF FOR FILE #55.1138 ; 03/07/23
# 
DA = [0, 0]
while True:
    if 'DIKILL' in globals():
        DIKLM = globals().get('DIKLM', None)
        if DIKM1 == 2:
            DIKLM = 1
        elif DIKM1 != 2 and not globals().get('DIKPUSH', {}).get(2):
            DIKPUSH[2] = 1
            DA[2] = DA[1]
            DA[1] = DA[0]
            DA[0] = 0
        if DIKM1 in globals():
            break
    DA[1] = next((i for i in range(DA[1] + 1, len(^PS(55, DA[2], "IV")) + 1)), 0)
    if DA[1] <= 0:
        DA[1] = 0
        break

while True:
    DA[0] = next((i for i in range(DA[0] + 1, len(^PS(55, DA[2], "IV", DA[1], 14)) + 1)), 0)
    if DA[0] <= 0:
        DA[0] = 0
        if DIKM1 == 1:
            break
        else:
            continue
    DIKZ = [0] * 1
    DIKZ[0] = ^PS(55, DA[2], "IV", DA[1], 14, DA[0], 0)
    X = DIKZ[0].split("^", 2)[0]
    if X != "":
        del ^PS(55, DA[2], "IV", DA[1], 14, "B", X[:30], DA[0])
    if not globals().get('DIKLM'):
        continue
    if 'DIKILL' in globals():
        break

return PSSJXR17()