# PSSJXR28 ; COMPILED XREF FOR FILE #55.05 ; 03/07/23

DA = 0

# A1
if 'DISET' in globals():
    del DIKLM
    if DIKM1 == 1:
        DIKLM = 1
    exec(DIKM1)

# 0
A:
DA = next((i for i in range(DA + 1, len(^PS(55, DA(1), "NVA"))) if i > DA), 0)

# 1
DIKZ(0) = ^PS(55,DA(1),"NVA",DA,0)
X = $P($G(DIKZ(0)),U,1)
if X != "":
    ^PS(55,DA(1),"NVA","B",$E(X,1,30),DA) = ""
X = $P($G(DIKZ(0)),U,6)
if X != "":
    if "PSODEATH" in globals():
        ^PS(55,DA(1),"NVA","APSOD",DA) = ""
X = $P($G(DIKZ(0)),U,10)
if X != "":
    ^PS(55,"ADCDT",$E(X,1,30),DA(1),DA) = ""

# CR1
DIXR = 452
X(1) = $P(DIKZ(0),U,1)
X(2) = $P(DIKZ(0),U,10)
X(3) = $P(DIKZ(0),U,9)
X(4) = $P(DIKZ(0),U,7)
X = X(1)
if X(1) != "" and X(2) != "":
    X1 = X.copy()
    X2 = X.copy()
    SNVA^PSOPXRMU(.X, .DA)

# CR2
del X
if 'DIKLM' not in globals():
    exec(A)
    if 'DISET' in globals():
        raise Exception
else:
    raise Exception

# END
^PSSJXR29