# COMPILED XREF FOR FILE #55.516 ; 03/07/23

DA[1] = 0
DA = 0

# A1
if "DIKILL" in globals():
    DIKLM = None
    if DIKM1 == 2:
        DIKLM = 1
    if DIKM1 != 2 and not DIKPUSH.get(2):
        DIKPUSH[2] = 1
        DA[2] = DA[1]
        DA[1] = DA
        DA = 0
    goto(DIKM1)

# A
DA[1] = next(i for i in range(DA[1]+1, len(^PS[55][DA[2]]["NVA"])) if ^PS[55][DA[2]]["NVA"][i] != null)
if DA[1] <= 0:
    DA[1] = 0
    goto(END)

# 1
DA = next(i for i in range(DA+1, len(^PS[55][DA[2]]["NVA"][DA[1]][3])) if ^PS[55][DA[2]]["NVA"][DA[1]][3][i] != null)
if DA <= 0:
    DA = 0
    if DIKM1 == 1:
        goto(A)
    else:
        goto(A)

# 2
DIKZ[0] = ^PS[55][DA[2]]["NVA"][DA[1]][3][DA]
X = $P(DIKZ[0],U,1)
if X != "":
    del ^PS[55][DA[2]]["NVA"][DA[1]][3]["B"][X[:30]][DA]
if not "DIKLM" in globals():
    goto(B)
if "DIKILL" in globals():
    goto(B)

# END
goto(^PSSJXR20)