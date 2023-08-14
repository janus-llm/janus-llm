# COMPILED XREF FOR FILE #55.11 ; 03/07/23

DA = [0]
DA.append(0)

# A1 ;
if "DIKILL" in locals():
    del DIKLM
    if DIKM1 == 2:
        DIKLM = 1
    elif DIKM1 != 2 and not DIKPUSH.get(2):
        DIKPUSH[2] = 1
        DA[2] = DA[1]
        DA[1] = DA[0]
        DA[0] = 0
        exec(DIKM1)
        
# A
DA[1] = next((i for i in range(DA[1]+1, len(^PS(55, DA[2], "IV")))), 0)
if DA[1] <= 0:
    DA[1] = 0
    exec("END")

# 1 ;
# B
DA = next((i for i in range(DA+1, len(^PS(55, DA[2], "IV", DA[1], "SOL")))), 0)
if DA <= 0:
    DA = 0
    if DIKM1 == 1:
        exec("A")
    else:
        exec("A1")

# 2 ;
DIKZ[0] = ^PS(55, DA[2], "IV", DA[1], "SOL", DA, 0)
X = $P(DIKZ[0], U, 2)
if X != "":
    exec(^DD(55.11, 1, 1, 1, 2))

DIKZ[0] = ^PS(55, DA[2], "IV", DA[1], "SOL", DA, 0)
X = $P(DIKZ[0], U, 1)
if X != "":
    exec(^DD(55.11, .01, 1, 1, 2))

if not "DIKLM" in locals():
    exec("B")
if "DIKILL" in locals():
    exec("END")
else:
    exec("^PSSJXR16")