# BIR/LDT - CONTINUATION OF API FOR INFORMATION FROM FILE 50; 5 Sep 03
# 1.0;PHARMACY DATA MANAGEMENT;**85**;9/30/97
# External reference to PS(50.605 supported by DBIA 2138

def SETND():
    global PSS
    global LIST
    global PSSFL
    global PSSRTOI
    global PSSPK
    global PSSENCT
    global PSS50NCL
    global PSSZNODE
    global PSS50NDN
    global PSS50NDA
    global PSS50NLL

    ^TMP[$J,LIST,+PSS(1),.01] = ^TMP[PSSP50,$J,50,PSS(1),.01,"I"]
    ^TMP[$J,LIST,"B",^TMP[PSSP50,$J,50,PSS(1),.01,"I"),+PSS(1)] = ""
    ^TMP[$J,LIST,+PSS(1),20] = $S(^TMP[PSSP50,$J,50,PSS(1),20,"I"]="", "", ^TMP[PSSP50,$J,50,PSS(1),20,"I"]_"^"_^TMP[PSSP50,$J,50,PSS(1),20,"E"])
    ^TMP[$J,LIST,+PSS(1),21] = ^TMP[PSSP50,$J,50,PSS(1),21,"I"]
    ^TMP[$J,LIST,+PSS(1),22] = $S(^TMP[PSSP50,$J,50,PSS(1),22,"I"]="", "", ^TMP[PSSP50,$J,50,PSS(1),22,"I"]_"^"_^TMP[PSSP50,$J,50,PSS(1),22,"E"])
    ^TMP[$J,LIST,+PSS(1),23] = $S(^TMP[PSSP50,$J,50,PSS(1),23,"I"]="", "", ^TMP[PSSP50,$J,50,PSS(1),23,"I"]_"^"_^TMP[PSSP50,$J,50,PSS(1),23,"E"])
    ^TMP[$J,LIST,+PSS(1),24] = $S(^TMP[PSSP50,$J,50,PSS(1),24,"I"]="", "", ^TMP[PSSP50,$J,50,PSS(1),24,"I"]_"^"_^TMP[PSSP50,$J,50,PSS(1),24,"E"])
    PSS50NCL = $S(^TMP[PSSP50,$J,50,PSS(1),25,"I"]="", "", ^TMP[PSSP50,$J,50,PSS(1),25,"I"])
    ^TMP[$J,LIST,+PSS(1),25] = $S(^TMP[PSSP50,$J,50,PSS(1),25,"I"]="", "", ^TMP[PSSP50,$J,50,PSS(1),25,"I"]_"^"_^TMP[PSSP50,$J,50,PSS(1),25,"E"])
    if PSS50NCL:
        ^TMP[$J,LIST,+PSS(1),25] = ^TMP[$J,LIST,+PSS(1),25] + "^" + $P(^PS(50.605,PSS50NCL,0),"^",2)
    ^TMP[$J,LIST,+PSS(1),27] = ^TMP[PSSP50,$J,50,PSS(1),27,"I"]
    ^TMP[$J,LIST,+PSS(1),29] = $S(^TMP[PSSP50,$J,50,PSS(1),29,"I"]="", "", ^TMP[PSSP50,$J,50,PSS(1),29,"I"]_"^"_^TMP[PSSP50,$J,50,PSS(1),29,"E"])

def LOOP():
    global PSS
    global LIST
    global PSSFL
    global PSSRTOI
    global PSSPK
    global PSSENCT
    global PSSZNODE
    global PSS50NDN
    global PSS50NDA
    global PSS50NLL

    PSSENCT = 0
    PSS(1) = 0
    while PSS(1):
        if $P(^PSDRUG(PSS(1),0),"^") == "":
            continue
        if PSSFL and $P(^PSDRUG(PSS(1),"I"),"^") and $P(^("I"),"^") <= PSSFL:
            continue
        if PSSRTOI == 1 and '$P(^PSDRUG(PSS(1),2),"^"):
            continue
        # Naked reference below refers to ^PSDRUG(PSS(1),2)
        if PSSPK:
            PSSZ5 = 0
            PSSZ6 = 1
            while PSSZ6 <= $L(PSSPK):
                if $P(^PSDRUG(PSS(1),2),"^",3)[$E(PSSPK,PSSZ6):
                    PSSZ5 = 1
                PSSZ6 = PSSZ6 + 1
            if PSSPK and not PSSZ5:
                continue
        SETNDL()
        PSSENCT = PSSENCT + 1
    ^TMP[$J,LIST,0] = $S($G(PSSENCT):$G(PSSENCT),1:"-1^NO DATA FOUND")

def SETNDL():
    global PSS
    global LIST
    global PSSFL
    global PSSRTOI
    global PSSPK
    global PSSZNODE
    global PSS50NDN
    global PSS50NDA
    global PSS50NLL

    PSSZNODE = ^PSDRUG(PSS(1),0)
    PSS50NDN = ^("ND")
    ^TMP[$J,LIST,+PSS(1),.01] = $P(PSSZNODE,"^")
    ^TMP[$J,LIST,"B",$P(PSSZNODE,"^"),+PSS(1)] = ""
    PSS50NDA = $$GETS^DIQ(50,+PSS(1),"20;21;22;23;24;25;27;29","IE")
    ^TMP[$J,LIST,+PSS(1),20] = $S($G(PSS50NDA(50,+PSS(1)_",",20,"I"))="":"",1:$G(PSS50NDA(50,+PSS(1)_",",20,"I"))_"^"_$G(PSS50NDA(50,+PSS(1)_",",20,"E")))
    ^TMP[$J,LIST,+PSS(1),21] = $G(PSS50NDA(50,+PSS(1)_",",21,"I"))
    ^TMP[$J,LIST,+PSS(1),22] = $S($G(PSS50NDA(50,+PSS(1)_",",22,"I"))="":"",1:$G(PSS50NDA(50,+PSS(1)_",",22,"I"))_"^"_$G(PSS50NDA(50,+PSS(1)_",",22,"E")))
    ^TMP[$J,LIST,+PSS(1),23] = $S($G(PSS50NDA(50,+PSS(1)_",",23,"I"))="":"",1:$G(PSS50NDA(50,+PSS(1)_",",23,"I"))_"^"_$G(PSS50NDA(50,+PSS(1)_",",23,"E")))
    ^TMP[$J,LIST,+PSS(1),24] = $S($G(PSS50NDA(50,+PSS(1)_",",24,"I"))="":"",1:$G(PSS50NDA(50,+PSS(1)_",",24,"I"))_"^"_$G(PSS50NDA(50,+PSS(1)_",",24,"E")))
    PSS50NLL = $S($G(PSS50NDA(50,+PSS(1)_",",25,"I"))="":"",1:$G(PSS50NDA(50,+PSS(1)_",",25,"I")))
    ^TMP[$J,LIST,+PSS(1),25] = $S($G(PSS50NDA(50,+PSS(1)_",",25,"I"))="":"",1:$G(PSS50NDA(50,+PSS(1)_",",25,"I"))_"^"_$G(PSS50NDA(50,+PSS(1)_",",25,"E")))
    if PSS50NLL:
        ^TMP[$J,LIST,+PSS(1),25] = ^TMP[$J,LIST,+PSS(1),25] + "^"_$P(^PS(50.605,PSS50NLL,0),"^",2)
    ^TMP[$J,LIST,+PSS(1),27] = $G(PSS50NDA(50,+PSS(1)_",",27,"I"))
    ^TMP[$J,LIST,+PSS(1),29] = $S($G(PSS50NDA(50,+PSS(1)_",",29,"I"))="":"",1:$G(PSS50NDA(50,+PSS(1)_",",29,"I"))_"^"_$G(PSS50NDA(50,+PSS(1)_",",29,"E")))

SETND()
LOOP()