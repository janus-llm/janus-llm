# COMPILED XREF FOR FILE #55.6132 ; 03/07/23
DA = [0, 0]
while True:
    if "DISET" in locals():
        DIKLM = {}
        if DIKM1 == 2:
            DIKLM = 1
        elif DIKM1 != 2 and not DIKPUSH.get(2):
            DIKPUSH[2] = 1
            DA[2] = DA[1]
            DA[1] = DA[0]
            DA[0] = 0
        if DIKM1 in locals():
            break
    DA[1] = next(iter(filter(lambda x: x > 0, ^PS[55, DA[2], 5, DA[1]])), 0)
    if DA[1] <= 0:
        DA[1] = 0
        break
    while True:
        DA[0] = next(iter(filter(lambda x: x > 0, ^PS[55, DA[2], 5, DA[1], 10, DA])), 0)
        if DA[0] <= 0:
            DA[0] = 0
            if DIKM1 == 1:
                break
            else:
                continue
        DIKZ = {"0": ^PS[55, DA[2], 5, DA[1], 10, DA, 0]}
        X = DIKZ["0"].split("^")[0]
        if X != "":
            ^PS[55, DA[2], 5, DA[1], 10, "B", X[:30]] = DA[0]
        if "DIKLM" not in locals():
            continue
        else:
            break
    if "DISET" in locals():
        break