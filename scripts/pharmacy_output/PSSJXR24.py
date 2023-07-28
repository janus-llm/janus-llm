# COMPILED XREF FOR FILE #55.0105 ; 03/07/23

DA = 0

# A1
if 'DISET' in locals():
    del DIKLM
    if DIKM1 == 1:
        DIKLM = 1
    exec(DIKM1)

# 0
while True:
    DA = next((i for i in range(DA + 1, len(^PS(55,DA(1),"IVBCMA"))) if ^PS(55,DA(1),"IVBCMA",i) is not None), 0)
    if DA <= 0:
        DA = 0
        break

# 1
DIKZ = {"0": ^PS(55,DA(1),"IVBCMA",DA,0)}
X = $P($G(DIKZ(0)),U,2)
if X != "":
    ^PS(55,DA(1),"IV",X,"BCMA",DA) = ""

DIXR = 159
X = {"1": $P(DIKZ(0),U,1), "2": $P(DIKZ(0),U,2)}
if X(1) != "" and X(2) != "":
    X1 = X.copy()
    X2 = X.copy()
    ^PS(55,DA(1),"BCMA",X(1),X(2)) = ""

if not 'DIKLM' in locals():
    break

exec(DIKLM)
if 'DISET' in locals():
    break

# END
exec(^PSSJXR25)