# COMPILED XREF FOR FILE #55.09 ; 03/07/23

DA[1] = 0
DA = 0

# A1
if 'DISET' in locals():
    del DIKLM
    if DIKM1 == 2:
        DIKLM = 1
    if DIKM1 != 2 and not DIKPUSH[2]:
        DIKPUSH[2] = 1
        DA[2] = DA[1]
        DA[1] = DA
        DA = 0
    goto(DIKM1)

# A
DA[1] = $O(^PS(55, DA[2], 5, DA[1]))
if DA[1] <= 0:
    DA[1] = 0
    goto(END)

# 1
DA = $O(^PS(55, DA[2], 5, DA[1], 9, DA))
if DA <= 0:
    DA = 0
    if DIKM1 == 1:
        goto(A)
    goto(END)

# 2
DIKZ[0] = ^PS(55, DA[2], 5, DA[1], 9, DA, 0)
X = $P(DIKZ[0], U, 1)
if X != "":
    if 'DIU' not in locals():
        if 'PSGAL' in locals():
            if PSGAL[35] == X:
                PSGAL5.KILL(PSGAL[35])
    PSGAL = locals().get('PSGAL', {})
X = $P(DIKZ[0], U, 2)
if X != "":
    if 'DIU' not in locals():
        if 'PSGAL' in locals():
            if PSGAL[36] == X:
                PSGAL5.KILL(PSGAL[36])
    PSGAL = locals().get('PSGAL', {})
X = $P(DIKZ[0], U, 3)
if X != "":
    if 'DIU' not in locals():
        if 'PSGAL' in locals():
            if PSGAL[37] == X:
                PSGAL5.KILL(PSGAL[37])
    PSGAL = locals().get('PSGAL', {})
X = $P(DIKZ[0], U, 4)
if X != "":
    if 'DIU' not in locals():
        if 'PSGAL' in locals():
            if PSGAL[78] == X:
                PSGAL5.KILL(PSGAL[78])
    PSGAL = locals().get('PSGAL', {})
X = $P(DIKZ[0], U, 5)
if X != "":
    if 'DIU' not in locals():
        if 'PSGAL' in locals():
            if PSGAL[79] == X:
                PSGAL5.KILL(PSGAL[79])
    PSGAL = locals().get('PSGAL', {})

if 'DIKLM' not in locals():
    goto(B)
if 'DISET' in locals():
    goto(B)

# END
goto(^PSSJXR36)