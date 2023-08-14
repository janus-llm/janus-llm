# COMPILED XREF FOR FILE #55.0611 ; 03/07/23
DA[1] = 0
DA = 0

# A1
if 'DIKILL' in locals():
    del DIKLM
    if DIKM1 == 2:
        DIKLM = 1
    elif DIKM1 != 2 and not DIKPUSH[2]:
        DIKPUSH[2] = 1
        DA[2] = DA[1]
        DA[1] = DA
        DA = 0
    # jump to DIKM1

# A
DA[1] = next((i for i in range(DA[1], len(^PS[55, DA[2], 5]))), 0)
if DA[1] <= 0:
    DA[1] = 0
    # jump to END

# 1
DA = next((i for i in range(DA, len(^PS[55, DA[2], 5, DA[1], 11]))), 0)
if DA <= 0:
    DA = 0
    if DIKM1 == 1:
        # jump to A
    # jump to A

# 2
DIKZ[0] = ^PS[55, DA[2], 5, DA[1], 11, DA, 0]
X = $P($G(DIKZ[0]), U, 2)
if X != "":
    if not DIU[0] and not PSGPO:
        PSGAL[1102] = X
        PSGAL["C"] = 6000
        PSGALFF = .02
        PSGALFN = 55.0611
        ^PSGAL5()
X = $P($G(DIKZ[0]), U, 3)
if X != "":
    if not DIU[0] and not PSGPO:
        PSGAL[1103] = X
        PSGAL["C"] = 6000
        PSGALFF = .03
        PSGALFN = 55.0611
        ^PSGAL5()
X = $P($G(DIKZ[0]), U, 4)
if X != "":
    if not DIU[0] and not PSGPO:
        PSGAL[1104] = X
        PSGAL["C"] = 6000
        PSGALFF = .04
        PSGALFN = 55.0611
        ^PSGAL5()
X = $P($G(DIKZ[0]), U, 5)
if X != "":
    if not DIU[0] and not PSGPO:
        PSGAL[1105] = X
        PSGAL["C"] = 6000
        PSGALFF = .05
        PSGALFN = 55.0611
        ^PSGAL5()
X = $P($G(DIKZ[0]), U, 6)
if X != "":
    if not DIU[0] and not PSGPO:
        PSGAL[1106] = X
        PSGAL["C"] = 6000
        PSGALFF = 1106
        PSGALFN = 55.0611
        ^PSGAL5()
X = $P($G(DIKZ[0]), U, 7)
if X != "":
    if not DIU[0] and not PSGPO:
        PSGAL[1107] = X
        PSGAL["C"] = 6000
        PSGALFF = 1107
        PSGALFN = 55.0611
        ^PSGAL5()
X = $P($G(DIKZ[0]), U, 8)
if X != "":
    if not DIU[0] and not PSGPO:
        PSGAL[1108] = X
        PSGAL["C"] = 6000
        PSGALFF = 1108
        PSGALFN = 55.0611
        ^PSGAL5()
X = $P($G(DIKZ[0]), U, 1)
if X != "":
    del ^PS[55, DA[2], 5, DA[1], 11, "B", $E(X, 1, 30), DA
if X != "":
    if not DIU[0] and not PSGPO:
        PSGAL[1101] = X
        PSGAL["C"] = 6000
        PSGALFF = .01
        PSGALFN = 55.0611
        ^PSGAL5()
if 'DIKLM' not in locals():
    # jump to B
if 'DIKILL' in locals():
    # jump to END

# END
^PSSJXR13()