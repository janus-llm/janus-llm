# COMPILED XREF FOR FILE #55.051 ; 03/07/23

DA[1] = 0
DA = 0

# A1
if 'DISET' in locals():
    del DIKLM
    if DIKM1 == 2:
        DIKLM = 1
    else:
        if DIKM1 != 2 and not DIKPUSH[2]:
            DIKPUSH[2] = 1
            DA[2] = DA[1]
            DA[1] = DA
            DA = 0
        goto DIKM1

# A
DA[1] = next((i for i in range(DA[1] + 1, len(^PS[55, DA[2], "NVA"]) + 1) if ^PS[55, DA[2], "NVA"][i]), default=0)
if DA[1] <= 0:
    DA[1] = 0
    goto END

# 1
DA = next((i for i in range(DA + 1, len(^PS[55, DA[2], "NVA", DA[1], "OCK"]) + 1) if ^PS[55, DA[2], "NVA", DA[1], "OCK"][i]), default=0)
if DA <= 0:
    DA = 0
    if DIKM1 == 1:
        goto A
    else:
        goto A

# 2
DIKZ[0] = ^PS[55, DA[2], "NVA", DA[1], "OCK", DA, 0]
X = $P(DIKZ[0], U, 1)
if X != "":
    ^PS[55, DA[2], "NVA", DA[1], "OCK", "B", $E(X, 1, 30)] = DA

if not 'DIKLM' in locals():
    goto B
if 'DISET' in locals():
    goto B

# END
goto ^PSSJXR33