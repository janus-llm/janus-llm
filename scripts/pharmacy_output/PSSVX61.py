# COMPILED XREF FOR FILE #52.6 ; 10/30/18
DIKZK = 2
DIKZ_0 = ^PS(52.6,DA,0)
X = $P($G(DIKZ_0),U,2)
if X != "":
    K ^PS(52.6,"AC",$E(X,1,30),DA)
    if X != "" and not $D(^PS(52.7,"AC",X)):
        XX = $O(^PS(52.6,"AC",X,0))
        if XX == DA:
            XX = $O(^(XX))
        if XX and $P($G(^PSDRUG(X,2)),"^",3)["I":
            PSIUDA = X
            PSIUX = "I"
            END^PSSGIU()
X = $P($G(DIKZ_0),U,2)
if X != "":
    N DIK,DIV,DIU,DIN
    DIU = $P($G(^PS(52.6,DA,0)),U,12)
    if DIU != "":
        $P(^(0),U,12) = ""
        if $O(^DD(52.6,16,1,0)):
            K DIV
            DIV = X
            (DIV,X) = ""
            (D0,DIV(0)) = DA
            DIH = 52.6
            DIG = 16
            ^DICR()
X = $P($G(DIKZ_0),U,2)
if X != "":
    K526^PSSPOID1()
DIKZ_I = ^PS(52.6,DA,"I")
X = $P($G(DIKZ_I),U,1)
if X != "":
    ^DD(52.6,12,1,1,2)()
DIKZ_0 = ^PS(52.6,DA,0)
X = $P($G(DIKZ_0),U,11)
if X != "":
    K ^PS(52.6,"AOI",$E(X,1,30),DA)
X = $P($G(DIKZ_0),U,12)
if X != "":
    K ^PS(52.6,"APD",$E(X,1,30),DA)
X = $P($G(DIKZ_0),U,13)
if X != "":
    ^DD(52.6,17,1,1,2)()
DIKZ_0 = ^PS(52.6,DA,0)
X = $P($G(DIKZ_0),U,1)
if X != "":
    K ^PS(52.6,"B",$E(X,1,30),DA)
Goto ^PSSVX62