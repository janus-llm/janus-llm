# COMPILED XREF FOR FILE #55.174 ; 03/07/23
DA = [0, 0]
while True:
    if 'DISET' in locals():
        if DIKM1 == 2:
            DIKLM = 1
        elif DIKM1 != 2 and not DIKPUSH.get(2):
            DIKPUSH[2] = 1
            DA[2] = DA[1]
            DA[1] = DA[0]
            DA[0] = 0
        if DIKM1 in locals():
            break
    DA[1] = next((i for i in range(DA[1] + 1, len(^PS(55, DA[2], "PC")))), 0)
    if DA[1] <= 0:
        DA[1] = 0
        break
    DA[0] = next((i for i in range(DA[0] + 1, len(^PS(55, DA[2], "PC", DA[1], "PCH")))), 0)
    if DA[0] <= 0:
        DA[0] = 0
        if DIKM1 == 1:
            break
        else:
            continue
    DIKZ = {}
    DIKZ[0] = ^PS(55, DA[2], "PC", DA[1], "PCH", DA[0], 0)
    X = DIKZ[0].split("^")[0]
    if X != "":
        ^PS(55, DA[2], "PC", DA[1], "PCH", "B", X[:30], DA[0]) = ""
    if 'DIKLM' not in locals():
        continue
    if 'DISET' in locals():
        break
^PSSJXR40()