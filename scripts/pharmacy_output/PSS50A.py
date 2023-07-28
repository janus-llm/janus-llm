#PSS50A ;BIR/LDT - CONTINUATION OF API FOR INFORMATION FROM FILE 50 ;5 Sep 03
##1.0;PHARMACY DATA MANAGEMENT;**85,91,92**;9/30/97
#;External reference to PS(50.605 supported by DBIA 2138

def SETSCRN():
    #Set Screen for inactive Drugs
    #Naked reference below refers to ^PSDRUG(+Y,"I")
    if PSSFL > 0:
        SCR["S"] = "S PSS5ND=$P($G(^(""I"")),""^"") I PSS5ND=""""!(PSS5ND>PSSFL)"
    if PSSRTOI == 1:
        #Naked reference below refers to ^PSDRUG(+Y,2)
        if SCR["S"]:
            SCR["S"] = SCR["S"] + " I $P($G(^(2)),""^"")"
        else:
            SCR["S"] = "I $P($G(^(2)),""^"")"
    if PSSPK:
        #Naked reference below refers to ^PSDRUG(+Y,2)
        if SCR["S"]:
            SCR["S"] = SCR["S"] + " S PSSZ3=0 F PSSZ4=1:1:$L(PSSPK) Q:PSSZ3  I $P($G(^(2)),""^"",3)[$E(PSSPK,PSSZ4) S PSSZ3=1"
        else:
            SCR["S"] = "S PSSZ3=0 F PSSZ4=1:1:$L(PSSPK) Q:PSSZ3  I $P($G(^(2)),""^"",3)[$E(PSSPK,PSSZ4) S PSSZ3=1"

def SETALL():
    ^TMP($J, LIST, +PSS(1), .01) = ^TMP("PSSP50", $J, 50, PSS(1), .01, "I")
    ^TMP($J, LIST, "B", ^TMP("PSSP50", $J, 50, PSS(1), .01, "I"), +PSS(1)) = ""
    ^TMP($J, LIST, +PSS(1), 2) = ^TMP("PSSP50", $J, 50, PSS(1), 2, "I")
    ^TMP($J, LIST, +PSS(1), 2.1) = $S(^TMP("PSSP50", $J, 50, PSS(1), 2.1, "I")="":"",1:^TMP("PSSP50", $J, 50, PSS(1), 2.1, "I")_"^"_^TMP("PSSP50", $J, 50, PSS(1), 2.1, "E"))
    if $P(^TMP($J, LIST, +PSS(1), 2.1), "^"):
        PSSADDF = $$SETDF^PSS50AQM($P(^TMP($J, LIST, +PSS(1), 2.1), "^"))
        ^TMP($J, LIST, +PSS(1), 2.1) = ^TMP($J, LIST, +PSS(1), 2.1)_$S($P(PSSADDF, "^")>0:"^"_$P(PSSADDF, "^", 3)_"^"_$P(PSSADDF, "^", 4),1:"")
    ^TMP($J, LIST, +PSS(1), 3) = ^TMP("PSSP50", $J, 50, PSS(1), 3, "I")
    ^TMP($J, LIST, +PSS(1), 4) = ^TMP("PSSP50", $J, 50, PSS(1), 4, "I")
    ^TMP($J, LIST, +PSS(1), 5) = ^TMP("PSSP50", $J, 50, PSS(1), 5, "I")
    ^TMP($J, LIST, +PSS(1), 6) = ^TMP("PSSP50", $J, 50, PSS(1), 6, "I")
    ^TMP($J, LIST, +PSS(1), 8) = ^TMP("PSSP50", $J, 50, PSS(1), 8, "I")
    PSSUTN = ^TMP("PSSP50", $J, 50, PSS(1), 12, "I")
    ^TMP($J, LIST, +PSS(1), 12) = $S(PSSUTN="":"",1:^TMP("PSSP50", $J, 50, PSS(1), 12, "I")_"^"_^TMP("PSSP50", $J, 50, PSS(1), 12, "E"))
    if PSSUTN:
        ^TMP($J, LIST, +PSS(1), 12) = ^TMP($J, LIST, +PSS(1), 12)_"^"_$P(^DIC(51.5, PSSUTN, 0), "^", 2)
    ^TMP($J, LIST, +PSS(1), 13) = ^TMP("PSSP50", $J, 50, PSS(1), 13, "I")
    ^TMP($J, LIST, +PSS(1), 14.5) = ^TMP("PSSP50", $J, 50, PSS(1), 14.5, "I")
    ^TMP($J, LIST, +PSS(1), 15) = ^TMP("PSSP50", $J, 50, PSS(1), 15, "I")
    ^TMP($J, LIST, +PSS(1), 16) = ^TMP("PSSP50", $J, 50, PSS(1), 16, "I")
    ^TMP($J, LIST, +PSS(1), 20) = $S(^TMP("PSSP50", $J, 50, PSS(1), 20, "I")="":"",1:^TMP("PSSP50", $J, 50, PSS(1), 20, "I")_"^"_^TMP("PSSP50", $J, 50, PSS(1), 20, "E"))
    ^TMP($J, LIST, +PSS(1), 21) = ^TMP("PSSP50", $J, 50, PSS(1), 21, "I")
    ^TMP($J, LIST, +PSS(1), 22) = $S(^TMP("PSSP50", $J, 50, PSS(1), 22, "I")="":"",1:^TMP("PSSP50", $J, 50, PSS(1), 22, "I")_"^"_^TMP("PSSP50", $J, 50, PSS(1), 22, "E"))
    ^TMP($J, LIST, +PSS(1), 25) = $S(^TMP("PSSP50", $J, 50, PSS(1), 25, "I")="":"",1:^TMP("PSSP50", $J, 50, PSS(1), 25, "I")_"^"_^TMP("PSSP50", $J, 50, PSS(1), 25, "E")_"^"_$P(^PS(50.605,+^TMP("PSSP50", $J, 50, PSS(1), 25, "I"), 0), "^", 2))
    ^TMP($J, LIST, +PSS(1), 27) = ^TMP("PSSP50", $J, 50, PSS(1), 27, "I")
    ^TMP($J, LIST, +PSS(1), 31) = ^TMP("PSSP50", $J, 50, PSS(1), 31, "I")
    ^TMP($J, LIST, +PSS(1), 40) = ^TMP("PSSP50", $J, 50, PSS(1), 40, "I")
    ^TMP($J, LIST, +PSS(1), 51) = $S(^TMP("PSSP50", $J, 50, PSS(1), 51, "I")="":"",1:^TMP("PSSP50", $J, 50, PSS(1), 51, "I")_"^"_^TMP("PSSP50", $J, 50, PSS(1), 51, "E"))
    ^TMP($J, LIST, +PSS(1), 52) = $S(^TMP("PSSP50", $J, 50, PSS(1), 52, "I")="":"",1:^TMP("PSSP50", $J, 50, PSS(1), 52, "I")_"^"_^TMP("PSSP50", $J, 50, PSS(1), 52, "E"))
    ^TMP($J, LIST, +PSS(1), 63) = ^TMP("PSSP50", $J, 50, PSS(1), 63, "I")
    ^TMP($J, LIST, +PSS(1), 64) = $S('$P(^TMP("PSSP50", $J, 50, PSS(1), 64, "I"), "^"):"",1:$P(^TMP("PSSP50", $J, 50, PSS(1), 64, "I"), "^")_"^"_$P(^TMP("PSSP50", $J, 50, PSS(1), 64, "E"), "^"))
    ^TMP($J, LIST, +PSS(1), 100) = $S(^TMP("PSSP50", $J, 50, PSS(1), 100, "I")="":"",1:^TMP("PSSP50", $J, 50, PSS(1), 100, "I")_"^"_^TMP("PSSP50", $J, 50, PSS(1), 100, "E"))
    ^TMP($J, LIST, +PSS(1), 101) = ^TMP("PSSP50", $J, 50, PSS(1), 101, "I")
    ^TMP($J, LIST, +PSS(1), 102) = ^TMP("PSSP50", $J, 50, PSS(1), 102, "I")
    ^TMP($J, LIST, +PSS(1), 301) = $S(^TMP("PSSP50", $J, 50, PSS(1), 301, "I")="":"",1:^TMP("PSSP50", $J, 50, PSS(1), 301, "I")_"^"_^TMP("PSSP50", $J, 50, PSS(1), 301, "E"))
    ^TMP($J, LIST, +PSS(1), 302) = ^TMP("PSSP50", $J, 50, PSS(1), 302, "I")
    SRVCODE()

def SETSYN():
    ^TMP($J, LIST, +PSS(1), "SYN", +PSS(2), .01) = ^TMP("PSSP50", $J, 50.1, PSS(2), .01, "I")
    ^TMP($J, LIST, +PSS(1), "SYN", +PSS(2), 1) = $S(^TMP("PSSP50", $J, 50.1, PSS(2), 1, "I")="":"",1:^TMP("PSSP50", $J, 50.1, PSS(2), 1, "I")_"^"_^TMP("PSSP50", $J, 50.1, PSS(2), 1, "E"))
    ^TMP($J, LIST, +PSS(1), "SYN", +PSS(2), 2) = ^TMP("PSSP50", $J, 50.1, PSS(2), 2, "I")
    ^TMP($J, LIST, +PSS(1), "SYN", +PSS(2), 403) = ^TMP("PSSP50", $J, 50.1, PSS(2), 403, "I")

def SETFMA():
    ^TMP($J, LIST, +PSS(1), "FRM", +PSS(2), .01) = $S(^TMP("PSSP50", $J, 50.065, PSS(2), .01, "I")="":"",1:^TMP("PSSP50", $J, 50.065, PSS(2), .01, "I")_"^"_^TMP("PSSP50", $J, 50.065, PSS(2), .01, "E"))

def SETOLD():
    ^TMP($J, LIST, +PSS(1), "OLD", +PSS(2), .01) = ^TMP("PSSP50", $J, 50.01, PSS(2), .01, "I")
    ^TMP($J, LIST, +PSS(1), "OLD", +PSS(2), .02) = $S(^TMP("PSSP50", $J, 50.01, PSS(2), .02, "I")="":"",1:^TMP("PSSP50", $J, 50.01, PSS(2), .02, "I")_"^"_^TMP("PSSP50", $J, 50.01, PSS(2), .02, "E"))

def SRVCODE():
    #PFSS retrieve correct service code from file #50.68/#50 or set to 600000
    ^TMP($J, LIST, +PSS(1), 400) = ^TMP("PSSP50", $J, 50, PSS(1), 400, "I")
    PSSNDSC = GET1^DIQ(50, PSSIEN_",", "22:2000", "I")
    if PSSNDSC:
        ^TMP($J, LIST, +PSS(1), 400) = PSSNDSC
    if not ^TMP($J, LIST, +PSS(1), 400):
        ^TMP($J, LIST, +PSS(1), 400) = 600000

SETSCRN()
SETALL()
SETSYN()
SETFMA()
SETOLD()
SRVCODE()