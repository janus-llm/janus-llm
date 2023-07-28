# COMPILED XREF FOR FILE #55.03 ; 03/07/23
DA = 0

# A1 label
while True:
    if 'DISET' in locals():
        del DIKLM
        if DIKM1 == 1:
            DIKLM = 1
        break

    # 0 label
    DA = DA + 1
    if DA <= 0:
        DA = 0
        break

    # 1 label
    DIKZ_0 = PS[55][DA(1)]["P"][DA][0]
    X = DIKZ_0.split("^")[0]

    if X != "":
        SREF()

    if 'DIKLM' not in locals():
        continue

    if 'DISET' in locals():
        break

# END label
PSSJXR28()