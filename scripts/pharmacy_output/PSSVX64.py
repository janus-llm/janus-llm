# COMPILED XREF FOR FILE #52.6 ; 10/30/18

DIKZK = 1
DIKZ_0 = PS(52.6, DA, 0)
X = $P($G(DIKZ_0), U, 1)
if X != "":
    PS(52.6, "B", $E(X, 1, 30), DA) = ""

X = $P($G(DIKZ_0), U, 2)
if X != "":
    PS(52.6, "AC", $E(X, 1, 30), DA) = ""

if X != "":
    if $P($G(^PSDRUG(X, 2)), "^", 3) does not contain "I":
        PSIUDA = X
        PSIUX = "I"
        ENS^PSSGIU

if X != "":
    DIK, DIV, DIU, DIN = None
    K DIV
    (DIV, X) = $P($G(^PSDRUG(X, 2)), U, 6)
    if DIV:
        DIU = $P($G(^PS(52.6, DA, 0)), U, 12)
        if DIV != DIU:
            $P(^PS(52.6, DA, 0), U, 12) = DIV
            if $O(^DD(52.6, 16, 1, 0)):
                D0, DIV(0) = DA
                DIH = 52.6
                DIG = 16
                ^DICR

if X != "":
    S526^PSSPOID1

DIKZ_I = ^PS(52.6, DA, "I")
X = $P($G(DIKZ_I), U, 1)
if X != "":
    ^DD(52.6, 12, 1, 1, 1)

DIKZ_0 = ^PS(52.6, DA, 0)
X = $P($G(DIKZ_0), U, 11)
if X != "":
    ^PS(52.6, "AOI", $E(X, 1, 30), DA) = ""

X = $P($G(DIKZ_0), U, 12)
if X != "":
    ^PS(52.6, "APD", $E(X, 1, 30), DA) = ""

X = $P($G(DIKZ_0), U, 13)
if X != "":
    ^DD(52.6, 17, 1, 1, 1)

END
G ^PSSVX65