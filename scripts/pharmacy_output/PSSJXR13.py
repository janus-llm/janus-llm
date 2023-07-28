# COMPILED XREF FOR FILE #55.07 ; 03/07/23

DA[1] = 0
DA = 0

# A1
if DIKILL:
    if DIKM1 == 2:
        DIKLM = 1
    else:
        if not DIKM1 != 2 and not DIKPUSH[2]:
            DIKPUSH[2] = 1
            DA[2] = DA[1]
            DA[1] = DA
            DA = 0
        goto DIKM1

# A
DA[1] = $O(^PS(55, DA[2], 5, DA[1]))
if DA[1] <= 0:
    DA[1] = 0
    goto END

# 1
DA = $O(^PS(55, DA[2], 5, DA[1], 1, DA))
if DA <= 0:
    DA = 0
    if DIKM1 == 1:
        goto A
    else:
        goto END

# 2
DIKZ[0] = ^PS(55, DA[2], 5, DA[1], 1, DA, 0)
X = $P(DIKZ[0], U, 2)
if X != "":
    if not DIU[0] and not PSGPO:
        PSGAL[702] = X
        PSGAL["C"] = 6000
        PSGALFF = .02
        PSGALFN = 55.07
        ^PSGAL5()

X = $P(DIKZ[0], U, 5)
if X != "":
    if not DIU[0] and not PSGPO:
        PSGAL[705] = X
        PSGAL["C"] = 6000
        PSGALFF = .05
        PSGALFN = 55.07
        ^PSGAL5()

X = $P(DIKZ[0], U, 6)
if X != "":
    if not DIU[0] and not PSGPO:
        PSGAL[706] = X
        PSGAL["C"] = 6000
        PSGALFF = .06
        PSGALFN = 55.07
        ^PSGAL5()

X = $P(DIKZ[0], U, 7)
if X != "":
    if not PSGRET and not DIU[0] and not PSGPO:
        PSGAL[707] = X
        PSGAL["C"] = 6000
        PSGALFF = .07
        PSGALFN = 55.07
        ^PSGAL5()

X = $P(DIKZ[0], U, 9)
if X != "":
    if not DIU[0] and not PSGPO:
        PSGAL[709] = X
        PSGAL["C"] = 6000
        PSGALFF = .09
        PSGALFN = 55.07
        ^PSGAL5()

X = $P(DIKZ[0], U, 10)
if X != "":
    if not DIU[0] and not PSGPO:
        PSGAL[710] = X
        PSGAL["C"] = 6000
        PSGALFF = .1
        PSGALFN = 55.07
        ^PSGAL5()

X = $P(DIKZ[0], U, 12)
if X != "":
    if not PSGPEN and not DIU[0] and not PSGPO:
        PSGAL[712] = X
        PSGAL["C"] = 6000
        PSGALFF = .12
        PSGALFN = 55.07
        ^PSGAL5()

X = $P(DIKZ[0], U, 1)
if X != "":
    if not DIU[0] and not PSGPO:
        PSGAL[701] = X
        PSGAL["C"] = 6000
        PSGALFF = .01
        PSGALFN = 55.07
        ^PSGAL5()

X = $P(DIKZ[0], U, 1)
if X != "":
    kill ^PS(55, DA[2], 5, DA[1], 1, "B", $E(X, 1, 30), DA)

if not DIKLM:
    goto B
if DIKILL:
    goto B
goto Q

END:
goto ^PSSJXR14