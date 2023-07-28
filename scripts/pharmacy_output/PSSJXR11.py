# COMPILED XREF FOR FILE #55.051 ; 03/07/23

DA[1] = 0
DA = 0

# A1
if 'DIKILL' in globals():
    del DIKLM
    if DIKM1 == 2:
        DIKLM = 1
    elif DIKM1 != 2 and not globals().get('DIKPUSH', {}).get(2):
        DIKPUSH[2] = 1
        DA[2] = DA[1]
        DA[1] = DA
        DA = 0
    exec(DIKM1)

# A
DA[1] = next((da for da in range(DA[1] + 1, len(^PS[55, DA[2], "NVA"]) + 1)), 0)
if DA[1] <= 0:
    DA[1] = 0
    exec("END")

# 1
DA = next((da for da in range(DA + 1, len(^PS[55, DA[2], "NVA", DA[1], "OCK"]) + 1)), 0)
if DA <= 0:
    DA = 0
    if DIKM1 == 1:
        exec("A")
    else:
        exec("A1")

# 2
DIKZ[0] = ^PS[55, DA[2], "NVA", DA[1], "OCK", DA, 0]
X = $PIECE(DIKZ[0], U, 1)
if X != "":
    del ^PS[55, DA[2], "NVA", DA[1], "OCK", "B", X[:30], DA]
if not 'DIKLM' in globals():
    exec("B")
if 'DIKILL' in globals():
    exec("B")

exec("^PSSJXR12")