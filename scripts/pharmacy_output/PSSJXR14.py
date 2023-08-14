# PSSJXR14 ; COMPILED XREF FOR FILE #55.09 ; 03/07/23
# 
DA = [0, 0]
# A1 ;
if 'DIKILL' in globals():
    DIKLM = {}
    if DIKM1 == 2:
        DIKLM = 1
    elif DIKM1 != 2 and not DIKPUSH.get(2):
        DIKPUSH[2] = 1
        DA[2] = DA[1]
        DA[1] = DA
        DA = 0
    exec(DIKM1)
# A
DA[1] = next((i for i, _ in enumerate(PS[55][DA[2]][5], 1)), 0)
if DA[1] <= 0:
    DA[1] = 0
    # G END
# 1 ;
DA = next((i for i, _ in enumerate(PS[55][DA[2]][5][DA[1]][9], 1)), 0)
if DA <= 0:
    DA = 0
    if DIKM1 == 1:
        exec('A')
    exec('A')
# 2 ;
DIKZ[0] = PS[55][DA[2]][5][DA[1]][9][DA]
X = DIKZ[0][2]
if X != "":
    if 'DIU' not in globals() and 'PSGPO' not in globals():
        PSGAL[36] = X
        PSGAL["C"] = 6000
        PSGALFF = 1
        PSGALFN = 55.09
        exec('^PSGAL5')
X = DIKZ[0][3]
if X != "":
    if 'DIU' not in globals() and 'PSGPO' not in globals():
        PSGAL[37] = X
        PSGAL["C"] = 6000
        PSGALFF = 2
        PSGALFN = 55.09
        exec('^PSGAL5')
X = DIKZ[0][4]
if X != "":
    if 'DIU' not in globals() and 'PSGPO' not in globals():
        PSGAL[78] = X
        PSGAL["C"] = 6000
        PSGALFF = 3
        PSGALFN = 55.09
        exec('^PSGAL5')
X = DIKZ[0][5]
if X != "":
    if 'DIU' not in globals() and 'PSGPO' not in globals():
        PSGAL[79] = X
        PSGAL["C"] = 6000
        PSGALFF = 4
        PSGALFN = 55.09
        exec('^PSGAL5')
X = DIKZ[0][1]
if X != "":
    if 'DIU' not in globals() and 'PSGPO' not in globals():
        PSGAL[35] = X
        PSGAL["C"] = 6000
        PSGALFF = .01
        PSGALFN = 55.09
        exec('^PSGAL5')
if not 'DIKLM' in globals():
    exec('B')
    if 'DIKILL' in globals():
        quit()
# END
exec('^PSSJXR15')