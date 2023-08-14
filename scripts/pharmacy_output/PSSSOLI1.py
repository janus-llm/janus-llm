# BIR/RTR-Manual match Solutions to Orderable Items continued ; 09/01/98 7:13
# 1.0;PHARMACY DATA MANAGEMENT;**15**;9/30/97

def ADD():
    global PSND, PSND1, PSND3, DA, K, X, PSDOSPTR, PSDOSNM, PSDOSPTR, PSOIDOSE, PSSNAME, PSSVOL, PPFLAG, HOLDOI, QQ, ZZFLAG, SYN, PSNEWOI, SCOUNT, SS, WW, PSSIEN, PSSOI, PSSDIR, PSSSSS
    PSND = PSND1 = PSND3 = DA = K = X = PSDOSPTR = PSDOSNM = PSDOSPTR = PSOIDOSE = PSSNAME = PSSVOL = PPFLAG = HOLDOI = QQ = ZZFLAG = SYN = PSNEWOI = SCOUNT = SS = WW = PSSIEN = PSSOI = PSSDIR = PSSSSS = None

    PSND = "^PSDRUG(PSDISP,\"ND\")"
    PSND1 = "$P(PSND,\"^\")"
    PSND3 = "$P(PSND,\"^\",3)"
    DA = PSND1
    K = PSND3
    
    if PSND1 and PSND3:
        X = "$$PSJDF^PSNAPIS(DA,K)"
        PSDOSPTR = "$P(X,\"^\")"
    
    if PSDOSPTR and "^PS(50.606,PSDOSPTR,0)" in "$D":
        PSDOSNM = "$P(^PS(50.606,PSDOSPTR,0),\"^\")"
        print(f"!!?3,\"*** Dose Form from NDF:  {PSDOSNM}")
        print("PASS")
    
    print("! K DIC S DIC=\"^PS(50.606,\",DIC(0)=\"QEAMZ\",DIC(\"A\")=\"Select Dose Form: \"")
    print("^DIC K DIC")
    print("if Y<1!($D(DTOUT))!($D(DUOUT)) G ^PSSSOLIT")
    
    PSDOSPTR = "+Y"
    PSDOSNM = "$P(^PS(50.606,PSDOSPTR,0),\"^\")"
    
    PSOIDOSE = PSDOSPTR
    
    print(f"!!,\"Solution Name ->  {PSSNAME}")
    print(f"       Volume ->  {PSSVOL}")
    print(f"    Dose Form ->  {PSDOSNM}")
    
    XXX = PSSNAME
    CHECK()
    
    PSANS = 0
    print(f"if ZZFLAG W $C(7),!!,\"There is already an Orderable Item named:\",!?5,$P($G(^PS(50.7,ZZFLAG,0)),\"^\")_\"   \"_$P($G(^PS(50.606,+$P(^(0),\"^\",2),0)),\"^\")")
    print("K DIR S DIR(0)=\"Y\",DIR(\"B\")=\"YES\",DIR(\"A\")=\"Match to this Orderable Item\" D ^DIR")
    print("PSANS=Y K DIR")
    print(f"if Y[\"^\"!($D(DTOUT)) G ^PSSSOLIT")
    
    if PSANS:
        print(f"!!,\"Matching: {PSSNAME}   {PSSVOL}")
        print("   to")
        print(f"{PSDOSNM} W ! K DIR S DIR(0)=\"Y\",DIR(\"B\")=\"YES\",DIR(\"A\")=\"Is this OK\" D ^DIR")
        print("G:Y=1 SOMAT^PSSSUTIL")
        print(f"G:Y[\"^\"!($D(DTOUT)) ^PSSSOLIT")
    
    print("XDIR")
    print("K DIR S DIR(0)=\"F^3:40\",DIR(\"A\")=\"Enter Orderable Item Name\" S X=PSSNAME D INPUT")
    print("if $L(PSSNAME)>2,$L(PSSNAME)<41,'INFLAG S DIR(\"B\")=PSSNAME")
    print("^DIR K DIR")
    print(f"if Y[\"^\"!(Y=\"\")!($D(DUOUT))!($D(DTOUT)) G ^PSSSOLIT")
    
    HOLDOI = "X"
    print("INPUT")
    print(f"if INFLAG W $C(7),!?5,\"??\",! G XDIR")
    
    PPFLAG = 0
    print("for QQ=0:0 S QQ=$O(^PS(50.7,\"ADF\",HOLDOI,PSOIDOSE,QQ)) Q:'QQ!(PPFLAG)  I QQ,$P($G(^PS(50.7,QQ,0)),\"^\",3) S PPFLAG=QQ")
    
    if PPFLAG:
        print(f"!!,\"Matching: {PSSNAME}   {PSSVOL}")
        print("   to")
        print(f"{PPFLAG}   $P($G(^PS(50.606,+$P($G(^(0)),\"^\",2),0)),\"^\")")
        print("W ! K DIR S DIR(0)=\"Y\",DIR(\"B\")=\"YES\",DIR(\"A\")=\"Is this OK\" D ^DIR K DIR W !")
        print(f"G:Y[\"^\"!($D(DTOUT)) ^PSSSOLIT")
        print("G:Y=0 XDIR")
    
    if PPFLAG:
        ZZFLAG = PPFLAG
        print("SOMAT^PSSSUTIL")
    
    print("NEW")
    print(f"!!,\"Matching: {PSSNAME}   {PSSVOL}")
    print("   to")
    print(f"{HOLDOI}   {PSDOSNM}")
    print("W ! K DIR S DIR(0)=\"Y\",DIR(\"B\")=\"YES\",DIR(\"A\")=\"Is this OK\" D ^DIR K DIR W !")
    print("if Y'=1 G XDIR")
    print("K DIC,DD,DO S DIC=\"^PS(50.7,\",DIC(0)=\"L\",X=HOLDOI,DIC(\"DR\")=\".02////\"_PSOIDOSE_\";.03////\"_1 D FILE^DICN K DIC")
    print("if Y<1 W !!,\"Unable to create entry, try again!\",! G XDIR")
    
    PSNEWOI = "+Y"
    
    SCOUNT = 0
    print("for SS=0:0 S SS=$O(^PS(52.7,PSSIEN,3,SS)) Q:'SS  S SCOUNT=SCOUNT+1,SYN(SCOUNT)=^(SS,0)")
    
    print("K DIE S DIE=\"^PS(52.7,\",DA=PSSIEN,DR=\"9////\"_PSNEWOI D ^DIE K DIE")
    
    if SCOUNT:
        print(f"^PS(50.7,{PSNEWOI},2,0)=\"^50.72^{SCOUNT}^{SCOUNT}\"")
        print("for WW=0:0 S WW=$O(SYN(WW)) Q:'WW  S ^PS(50.7,PSNEWOI,2,WW,0)=SYN(WW)")
    
    NEWFLAG = 1
    PSSOI = PSNEWOI
    print("DIR^PSSPOIM3")
    print("if $G(PSSDIR) W !!?3,\"Now editing Orderable Item:\",!?3,$P(^PS(50.7,PSSOI,0),\"^\")")
    print(f"   $P($G(^PS(50.606,+$P(^(0),\"^\",2),0)),\"^\") D INACT^PSSSOLIT")
    
    del NEWFLAG, PSSDIR
    
    print("EN^PSSPOIDT(PSSOI)")
    print("if '$G(PSSSSS) EN2^PSSHL1(PSSOI,\"MAD\")")
    print("^PSSSOLIT")


def INPUT():
    global INFLAG
    INFLAG = 0
    print("if X[\"\"\"\"!($A(X)=45)!('(X'?1P.E))!(X?2\"z\".E) S INFLAG=1")


def CHECK():
    global ZZFLAG, ZZXFLAG, VV
    ZZFLAG = ZZXFLAG = 0
    print("for VV=0:0 S VV=$O(^PS(50.7,\"ADF\",XXX,PSOIDOSE,VV)) Q:'VV  S:VV&($P($G(^PS(50.7,VV,0)),\"^\",3)) (ZZFLAG,ZZXFLAG)=VV")


ADD()