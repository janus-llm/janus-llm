# COMPILED XREF FOR FILE #55.6114 ; 03/07/23

DA[1] = 0
DA = 0

# A1
if "DISET" in locals():
    del DIKLM
    if DIKM1 == 2:
        DIKLM = 1
    if DIKM1 != 2 and not DIKPUSH.get(2):
        DIKPUSH[2] = 1
        DA[2] = DA[1]
        DA[1] = DA
        DA = 0
    goto DIKM1

# A
DA[1] = $O(^PS(55,DA[2],5,DA[1]))
if DA[1] <= 0:
    DA[1] = 0
    goto END

# 1
# B
DA = $O(^PS(55,DA[2],5,DA[1],14,DA))
if DA <= 0:
    DA = 0
    if DIKM1 == 1:
        goto A

# 2
DIKZ[0] = ^PS(55,DA[2],5,DA[1],14,DA,0)
X = $P(DIKZ[0],U,1)
if X != "":
    ^PS(55,DA[2],5,DA[1],14,"B",X[:30],DA) = ""
if not "DIKLM" in locals():
    goto B
if "DISET" in locals():
    goto B

goto END

goto ^PSSJXR42