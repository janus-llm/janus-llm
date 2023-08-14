# BIR/WRT-Pre-transport routine ; 09/02/97 8:48
# 1.0;PHARMACY DATA MANAGEMENT;;9/30/97
# PRE-TRANSPORT ROUTINE
ROOT = ""
DA = 0
I = 1
LINE = ""
TOT = 0

def BUILDIT():
    global ROOT, DA, I, LINE, TOT
    ROOT = eval(f"@XPDGREF@('DATA')")
    while True:
        DA = DA + 1
        if not (DA in ^PS(51.2)):
            break
        X = ^PS(51.2)[DA]
        if $P(X, "^", 2):
            I = I + 1
            @ROOT@(I) = $P(X, "^", 1) + "^" + $P(X, "^", 2)
    return

BUILDIT()