# COMPILED XREF FOR FILE #55.0105 ; 03/07/23
# 
DA = 0

# A1
if 'DIKILL' in locals():
    del DIKLM
    if DIKM1 == 1:
        DIKLM = 1
    exec(DIKM1)

# 0
del ^PS(55,DA(1),"BCMA")

# A
DA = 0
while True:
    DA = DA + 1
    if DA > 0:
        break
DA = 0
goto A1

# 1
DIKZ(0) = ^PS(55,DA(1),"IVBCMA",DA)
X = $P($G(DIKZ(0)),U,2)
if X != "":
    del ^PS(55,DA(1),"IV",X,"BCMA",DA)

DIXR = 159
X(1) = $P(DIKZ(0),U,1)
X(2) = $P(DIKZ(0),U,2)
X = X(1)
if X(1) != "" and X(2) != "":
    del X1, X2
    X1 = X
    X2 = X
    if 'DIKIL' in locals():
        X2 = ""
        X2(1) = ""
        X2(2) = ""
    del ^PS(55,DA(1),"BCMA",X(1),X(2))

# CR2
del X
if not 'DIKLM' in locals():
    goto A
if 'DIKILL' in locals():
    goto A
goto END

# END
goto ^PSSJXR4