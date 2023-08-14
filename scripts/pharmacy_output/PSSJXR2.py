# COMPILED XREF FOR FILE #55.01 ; 03/07/23
DA[1] = DA
DA = 0

# A1
if $D(DIKILL):
    K DIKLM
    if DIKM1 == 1:
        DIKLM = 1
    G @DIKM1

# 0
K ^PS(55,DA[1],"IV","AIN")
K ^PS(55,DA[1],"IV","CIMOI")

# A
DA = $O(^PS(55,DA[1],"IV",DA))
if DA <= 0:
    DA = 0
G END

# 1
DIKZ[0] = $G(^PS(55,DA[1],"IV",DA,0))
X = $P($G(DIKZ[0]),U,2)
if X != "":
    X ^DD(55.01,.02,1,1,2)
X = $P($G(DIKZ[0]),U,2)
if X != "":
    K ^PS(55,"AIVS",$E(X,1,30),DA[1],DA)
DIKZ[0] = $G(^PS(55,DA[1],"IV",DA,0))
X = $P($G(DIKZ[0]),U,3)
if X != "":
    K ^PS(55,"AIV",+$E(X,1,30),DA[1],DA)
X = $P($G(DIKZ[0]),U,3)
if X != "":
    X ^DD(55.01,.03,1,2,2)
X = $P($G(DIKZ[0]),U,3)
if X != "":
    K ^PS(55,DA[1],"IV","AIS",+X,DA)
X = $P($G(DIKZ[0]),U,3)
if X != "":
    if $P($G(^PS(55,DA[1],"IV",DA,0)),U,4) != "":
        K ^PS(55,DA[1],"IV","AIT",$P(^(0),U,4),+X,DA)
DIKZ[0] = $G(^PS(55,DA[1],"IV",DA,0))
X = $P($G(DIKZ[0]),U,4)
if X != "":
    X ^DD(55.01,.04,1,1,2)
DIKZ[0] = $G(^PS(55,DA[1],"IV",DA,0))
X = $P($G(DIKZ[0]),U,6)
if X != "":
    X ^DD(55.01,.06,1,1,2)
DIKZ[0] = $G(^PS(55,DA[1],"IV",DA,0))
X = $P($G(DIKZ[0]),U,8)
if X != "":
    X ^DD(55.01,.08,1,1,2)
DIKZ[0] = $G(^PS(55,DA[1],"IV",DA,0))
X = $P($G(DIKZ[0]),U,9)
if X != "":
    X ^DD(55.01,.09,1,1,2)
DIKZ[1] = $G(^PS(55,DA[1],"IV",DA,1))
X = $P($G(DIKZ[1]),U,1)
if X != "":
    X ^DD(55.01,.1,1,1,2)
DIKZ[0] = $G(^PS(55,DA[1],"IV",DA,0))
X = $P($G(DIKZ[0]),U,11)
if X != "":
    X ^DD(55.01,.12,1,1,2)
DIKZ[3] = $G(^PS(55,DA[1],"IV",DA,3))
X = $P($G(DIKZ[3]),U,1)
if X != "":
    X ^DD(55.01,31,1,1,2)
DIKZ[0] = $G(^PS(55,DA[1],"IV",DA,0))
X = $P($G(DIKZ[0]),U,17)
if X != "":
    X ^DD(55.01,100,1,1,2)
X = $P($G(DIKZ[0]),U,17)
if X != "":
    K:X != "N" ^PS(55,"ANVO",DA[1],DA)
X = $P($G(DIKZ[0]),U,17)
if X != "":
    K:X != "D"&($D(^PS(55,DA[1],"IV",DA,"ADC"))) ^PS(55,"ADC",^PS(55,DA[1],"IV",DA,"ADC"),DA[1],DA)
DIKZ[4] = $G(^PS(55,DA[1],"IV",DA,4))
X = $P($G(DIKZ[4]),U,9)
if X != "":
    X ^DD(55.01,142,1,1,2)
X = $P($G(DIKZ[4]),U,9)
if X != "":
    K ^PS(55,"APIV",DA[1],DA)
DIKZ[4] = $G(^PS(55,DA[1],"IV",DA,4))
X = $P($G(DIKZ[4]),U,10)
if X != "":
    X ^DD(55.01,143,1,1,2)
X = $P($G(DIKZ[4]),U,10)
if X != "":
    K ^PS(55,"ANIV",DA[1],DA)
DIKZ[0] = $G(^PS(55,DA[1],"IV",DA,0))
X = $P($G(DIKZ[0]),U,1)
if X != "":
    K ^PS(55,DA[1],"IV","B",$E(X,1,30),DA)

CR1 D
    S DIXR = 406
    K X
    DIKZ(.2) = $G(^PS(55,DA[1],"IV",DA,.2))
    X(1) = $P(DIKZ(.2),U,8)
    X(2) = $P(DIKZ(0),U,21)
    X = $G(X(1))
    if $G(X(1)) != "",$G(X(2)) != "":
        K X1,X2
        M X1 = X,X2 = X
        if $D(DIKIL):
            X2,X2(1),X2(2) = ""
        N DIKXARR
        M DIKXARR = X
        S DIKCOND = 1
        S X = 1
        S DIKCOND = $G(X)
        K X
        M X = DIKXARR
        Q:'DIKCOND
        K ^PS(55,"ACX",$E(X1,1,30),$E(X2,1,30),DA_"V")

CR2 D
    S DIXR = 454
    K X
    DIKZ[0] = $G(^PS(55,DA[1],"IV",DA,0))
    X(1) = $P(DIKZ[0],U,2)
    X(2) = $P(DIKZ[0],U,3)
    X = $G(X(1))
    if $G(X(1)) != "",$G(X(2)) != "":
        K X1,X2
        M X1 = X,X2 = X
        if $D(DIKIL):
            X2,X2(1),X2(2) = ""
        N DIKXARR
        M DIKXARR = X
        S DIKCOND = 1
        S X = $$PATCH^XPDUTL("PXRM*1.5*12")
        S DIKCOND = $G(X)
        K X
        M X = DIKXARR
        Q:'DIKCOND
        D KPSPA^PSJXRFK(.X,.DA,"IV")

CR3 D
    S DIXR = 513
    K X
    DIKZ[0] = $G(^PS(55,DA[1],"IV",DA,0))
    X(1) = $P(DIKZ[0],U,3)
    DIKZ("DSS") = $G(^PS(55,DA[1],"IV",DA,"DSS"))
    X(2) = $P(DIKZ("DSS"),U,1)
    X = $G(X(1))
    if $G(X(1)) != "",$G(X(2)) != "":
        K X1,X2
        M X1 = X,X2 = X
        if $D(DIKIL):
            X2,X2(1) = ""
        K ^PS(55,"AIVC",$E(X1,1,20),$E(X2,1,20),DA[1],DA)

CR4 D
    S DIXR = 515
    K X
    DIKZ[0] = $G(^PS(55,DA[1],"IV",DA,0))
    X(1) = $P(DIKZ[0],U,3)
    DIKZ("DSS") = $G(^PS(55,DA[1],"IV",DA,"DSS"))
    X(2) = $P(DIKZ("DSS"),U,1)
    X = $G(X(1))
    if $G(X(1)) != "",$G(X(2)) != "":
        K X1,X2
        M X1 = X,X2 = X
        if $D(DIKIL):
            X2,X2(1) = ""
        K ^PS(55,DA[1],"IV","AIN",X(1),X(2),DA)

CR5 D
    S DIXR = 1122
    K X
    DIKZ("DSS") = $G(^PS(55,DA[1],"IV",DA,"DSS"))
    X(1) = $P(DIKZ("DSS"),U,1)
    X = $G(X(1))
    if $G(X(1)) != "":
        K X1,X2
        M X1 = X,X2 = X
        if $D(DIKIL):
            X2 = ""
        K ^PS(55,"CIMOCLI",X,DA[1],DA)

CR6 D
    S DIXR = 1125
    K X
    DIKZ("DSS") = $G(^PS(55,DA[1],"IV",DA,"DSS"))
    X(1) = $P(DIKZ("DSS"),U,1)
    DIKZ[0] = $G(^PS(55,DA[1],"IV",DA,0))
    X(2) = $P(DIKZ[0],U,3)
    X = $G(X(1))
    if $G(X(1)) != "",$G(X(2)) != "":
        K X1,X2
        M X1 = X,X2 = X
        if $D(DIKIL):
            X2,X2(1),X2(2) = ""
        K ^PS(55,DA[1],"IV","CIMOI",X(1),X(2),DA)

CR7 K X
G:'$D(DIKLM) A
Q:$D(DIKILL)
G ^PSSJXR3