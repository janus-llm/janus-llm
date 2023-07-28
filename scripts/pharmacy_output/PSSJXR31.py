# COMPILED XREF FOR FILE #55.02 ; 03/07/23

DA[2] = DA[1]
DA[1] = 0
DA = 0

# A1
if 'DISET' in globals():
    DIKLM = None
    if DIKM1 == 2:
        DIKLM = 1
    elif DIKM1 != 2 and not DIKPUSH[2]:
        DIKPUSH[2] = 1
        DA[2] = DA[1]
        DA[1] = DA
        DA = 0
    goto DIKM1

# A
DA[1] = $O(^PS(55,DA[2],"IV",DA[1]))
if DA[1] <= 0:
    DA[1] = 0
    goto END

# 1
# B
DA = $O(^PS(55,DA[2],"IV",DA[1],"AD",DA))
if DA <= 0:
    DA = 0
    if DIKM1 == 1:
        goto A
    goto A

# 2
DIKZ[0] = $G(^PS(55,DA[2],"IV",DA[1],"AD",DA,0))
X = $P($G(DIKZ[0]),U,1)
if X != "":
    X ^DD(55.02,.01,1,1,1)
DIKZ[0] = $G(^PS(55,DA[2],"IV",DA[1],"AD",DA,0))
X = $P($G(DIKZ[0]),U,2)
if X != "":
    X ^DD(55.02,.02,1,1,1)
DIKZ[0] = $G(^PS(55,DA[2],"IV",DA[1],"AD",DA,0))
X = $P($G(DIKZ[0]),U,3)
if X != "":
    X ^DD(55.02,.03,1,1,1)
if not 'DIKLM' in globals():
    goto B
if 'DISET' in globals():
    goto B

# END
goto ^PSSJXR32