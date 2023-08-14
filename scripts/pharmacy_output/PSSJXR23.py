# PSSJXR23 ; COMPILED XREF FOR FILE #55.01 ; 03/07/23
# 
DA[1] = DA
DA = 0

# A1 ;
if 'DISET:
    del DIKLM
    if DIKM1 == 1:
        DIKLM = 1
    goto DIKM1

# 0 ;
A:
DA = next(iter(^PS[55,DA[1],"IV",DA]), 0)
if DA <= 0:
    DA = 0
    goto END

# 1 ;
DIKZ[0] = ^PS[55,DA[1],"IV",DA,0]
X = $piece(DIKZ[0],U,1)
if X != "":
    ^PS[55,DA[1],"IV","B",$extract(X,1,30),DA] = ""
X = $piece(DIKZ[0],U,2)
if X != "":
    execute(^DD[55.01,.02,1,1,1])
X = $piece(DIKZ[0],U,2)
if X != "":
    ^PS[55,"AIVS",$extract(X,1,30),DA[1],DA] = ""
DIKZ[0] = ^PS[55,DA[1],"IV",DA,0]
X = $piece(DIKZ[0],U,3)
if X != "":
    ^PS[55,"AIV",+$extract(X,1,30),DA[1],DA] = ""
X = $piece(DIKZ[0],U,3)
if X != "":
    execute(^DD[55.01,.03,1,2,1])
X = $piece(DIKZ[0],U,3)
if X != "":
    ^PS[55,DA[1],"IV","AIS",+X,DA] = ""
X = $piece(DIKZ[0],U,3)
if X != "":
    if $piece(^PS[55,DA[1],"IV",DA,0],U,4) != "":
        ^PS[55,DA[1],"IV","AIT",$piece(^(0),U,4),+X,DA] = ""
DIKZ[0] = ^PS[55,DA[1],"IV",DA,0]
X = $piece(DIKZ[0],U,4)
if X != "":
    execute(^DD[55.01,.04,1,1,1])
DIKZ[0] = ^PS[55,DA[1],"IV",DA,0]
X = $piece(DIKZ[0],U,6)
if X != "":
    execute(^DD[55.01,.06,1,1,1])
X = $piece(DIKZ[0],U,6)
if X != "":
    if '$D(DIU[0]),$S($D(^PS[55,DA[1],5.1)):$piece(^(5.1),"^",2)'=X,1:1):
        $piece(^(5.1),"^",2) = X
DIKZ[0] = ^PS[55,DA[1],"IV",DA,0]
X = $piece(DIKZ[0],U,8)
if X != "":
    execute(^DD[55.01,.08,1,1,1])
DIKZ[0] = ^PS[55,DA[1],"IV",DA,0]
X = $piece(DIKZ[0],U,9)
if X != "":
    execute(^DD[55.01,.09,1,1,1])
DIKZ[1] = ^PS[55,DA[1],"IV",DA,1]
X = $piece(DIKZ[1],U,1)
if X != "":
    execute(^DD[55.01,.1,1,1,1])
DIKZ[0] = ^PS[55,DA[1],"IV",DA,0]
X = $piece(DIKZ[0],U,11)
if X != "":
    execute(^DD[55.01,.12,1,1,1])
DIKZ[3] = ^PS[55,DA[1],"IV",DA,3]
X = $piece(DIKZ[3],U,1)
if X != "":
    execute(^DD[55.01,31,1,1,1])
DIKZ[0] = ^PS[55,DA[1],"IV",DA,0]
X = $piece(DIKZ[0],U,17)
if X != "":
    execute(^DD[55.01,100,1,1,1])
X = $piece(DIKZ[0],U,17)
if X != "":
    if $D(DIU[0]):
        if X = "N":
            ^PS[55,"ANVO",DA[1],DA] = ""
X = $piece(DIKZ[0],U,17)
if X != "":
    if X = "D"&($D(^PS[55,DA[1],"IV",DA,"ADC"))):
        ^PS[55,"ADC",^PS[55,DA[1],"IV",DA,"ADC"],DA[1],DA] = ""
DIKZ[4] = ^PS[55,DA[1],"IV",DA,4]
X = $piece(DIKZ[4],U,9)
if X != "":
    execute(^DD[55.01,142,1,1,1])
X = $piece(DIKZ[4],U,9)
if X != "":
    if X:
        ^PS[55,"APIV",DA[1],DA] = ""
    else:
        ^PS[55,"APIV",DA[1],DA] = ""
DIKZ[4] = ^PS[55,DA[1],"IV",DA,4]
X = $piece(DIKZ[4],U,10)
if X != "":
    execute(^DD[55.01,143,1,1,1])
X = $piece(DIKZ[4],U,10)
if X != "":
    if X:
        ^PS[55,"ANIV",DA[1],DA] = ""
    else:
        ^PS[55,"ANIV",DA[1],DA] = ""

# CR1 S DIXR=406
del X
DIKZ(.2) = ^PS[55,DA[1],"IV",DA,.2]
X(1) = $piece(DIKZ(.2),U,8)
DIKZ[0] = ^PS[55,DA[1],"IV",DA,0]
X(2) = $piece(DIKZ[0],U,21)
X = X(1)
if X(1) != "" and X(2) != "":
    del X1,X2
    X1 = X,X2 = X
    DIKXARR = X
    DIKCOND = 1
    X = 1
    DIKCOND = X
    if DIKCOND:
        ^PS[55,"ACX",$extract(X1,1,30),$extract(X2,1,30),DA_"V"] = ""

# CR2 S DIXR=454
del X
DIKZ[0] = ^PS[55,DA[1],"IV",DA,0]
X(1) = $piece(DIKZ[0],U,2)
X(2) = $piece(DIKZ[0],U,3)
X = X(1)
if X(1) != "" and X(2) != "":
    del X1,X2
    X1 = X,X2 = X
    DIKXARR = X
    DIKCOND = 1
    X = $$PATCH^XPDUTL("PXRM*1.5*12")
    DIKCOND = X
    if DIKCOND:
        D SPSPA^PSJXRFS(.X,.DA,"IV")

# CR3 S DIXR=513
del X
DIKZ[0] = ^PS[55,DA[1],"IV",DA,0]
X(1) = $piece(DIKZ[0],U,3)
DIKZ("DSS") = ^PS[55,DA[1],"IV",DA,"DSS"]
X(2) = $piece(DIKZ("DSS"),U,1)
X = X(1)
if X(1) != "" and X(2) != "":
    del X1,X2
    X1 = X,X2 = X
    ^PS[55,"AIVC",$extract(X1,1,20),$extract(X2,1,20),DA[1],DA] = ""

# CR4 S DIXR=515
del X
DIKZ[0] = ^PS[55,DA[1],"IV",DA,0]
X(1) = $piece(DIKZ[0],U,3)
DIKZ("DSS") = ^PS[55,DA[1],"IV",DA,"DSS"]
X(2) = $piece(DIKZ("DSS"),U,1)
X = X(1)
if X(1) != "" and X(2) != "":
    del X1,X2
    X1 = X,X2 = X
    ^PS[55,DA[1],"IV","AIN",X(1),X(2),DA] = ""

# CR5 S DIXR=1122
del X
DIKZ("DSS") = ^PS[55,DA[1],"IV",DA,"DSS"]
X(1) = $piece(DIKZ("DSS"),U,1)
X = X(1)
if X(1) != "":
    del X1,X2
    X1 = X,X2 = X
    DIKXARR = X
    DIKCOND = 1
    X = $$CHECK2^PSJIMO1() I X
    DIKCOND = X
    if DIKCOND:
        ^PS[55,"CIMOCLI",X,DA[1],DA] = ""

# CR6 S DIXR=1125
del X
DIKZ("DSS") = ^PS[55,DA[1],"IV",DA,"DSS"]
X(1) = $piece(DIKZ("DSS"),U,1)
DIKZ[0] = ^PS[55,DA[1],"IV",DA,0]
X(2) = $piece(DIKZ[0],U,3)
X = X(1)
if X(1) != "" and X(2) != "":
    del X1,X2
    X1 = X,X2 = X
    DIKXARR = X
    DIKCOND = 1
    X = $$CHECK2^PSJIMO1() I X
    DIKCOND = X
    if DIKCOND:
        ^PS[55,DA[1],"IV","CIMOI",X(1),X(2),DA] = ""

CR7:
goto A
goto END

END:
goto ^PSSJXR24