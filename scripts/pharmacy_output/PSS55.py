def PSS431(DFN, PO, PSDATE, PEDATE, LIST):
    return PSS551()

def PSS432(DFN, PO, LIST):
    PSSPO = None
    if LIST == "":
        return
    ^TMP($J, LIST) = 0
    if DFN <= 0:
        return NODATA()
    if not exists(^PS(55, DFN)):
        return NODATA()
    if PO != "" and exists(^PS(55, DFN, 5, PO)):
        PSSPO = ^PS(55, DFN, 5, PO, 0)
        if PSSPO > 0:
            DA(55.06), IEN = PO
            return AUS2()
    if PO != "" and PSSPO == "":
        return NODATA()
    PSSDT = 0
    while True:
        PSSDT = next(^PS(55, DFN, 5, "AUS", PSSDT), 0)
        if PSSDT <= 0:
            break
        PSSIEN = 0
        while True:
            PSSIEN = next(^PS(55, DFN, 5, "AUS", PSSDT, PSSIEN), 0)
            if PSSIEN <= 0:
                break
            IEN, DA(55.06) = PSSIEN
            PSSDATA = ^PS(55, DFN, 5, PSSIEN, 0)
            if $P(PSSDATA, "^", 9) != "A":
                continue
            AUSDIQ()
    ^TMP($J, LIST, 0) = -1 if ^TMP($J, LIST, 0) == 0 else ^TMP($J, LIST, 0)
    K PSSIEN, PSSDT, PSSDATA, LIST

def AUSDIQ():
    ^UTILITY("DIQ1", $J), DIQ = {}
    DA = DFN, DIC = 55, DR = 62, DR(55.06) = ".01;.5;1;3;4;5;6;7;9;11;12;26;27;27.1;28", DIQ(0) = "IE"
    EN^DIQ1()
    PSSPO = ^UTILITY("DIQ1", $J, 55.06, IEN, .01, "E")
    for X in [.01, .5, 1, 3, 4, 5, 6, 7, 9, 11, 12, 26, 27, 27.1, 28]:
        ^TMP($J, LIST, IEN, X) = ^UTILITY("DIQ1", $J, 55.06, IEN, X, "I")
    for X in [.5, 1, 3, 4, 5, 6, 7, 9, 27, 27.1, 28]:
        ^TMP($J, LIST, IEN, X) = ^TMP($J, LIST, IEN, X) + "^" + ^UTILITY("DIQ1", $J, 55.06, IEN, X, "E")
    PSSTMP = $P(^PS(55, DFN, 5, IEN, .2), U)
    ^TMP($J, LIST, IEN, 108) = "" if PSSTMP == "" else ORDITEM(+PSSTMP)
    K ^UTILITY("DIQ1", $J), DIQ
    ^TMP($J, LIST, "B", IEN) = ""
    ^TMP($J, LIST, 0) = ^TMP($J, LIST, 0) + 1

def ORDITEM(PSSTMP):
    PSSTMP2 = ^PS(50.7, PSSTMP, 0)
    if PSSTMP2 != "":
        return PSSTMP + "^" + $P(PSSTMP2, U) + "^" + $P(PSSTMP2, U, 2) + "^" + $P(^PS(50.606, $P(PSSTMP2, U, 2), 0), U, 1)
    return PSSTMP

def AUS2():
    PSSQ = 1
    AUSDIQ()
    ^TMP($J, LIST, 0) = -1 if ^TMP($J, LIST, 0) == 0 else ^TMP($J, LIST, 0)
    AUSQ()

def AUSQ():
    K PSSDT, PSSIEN, PSSDATA, PSSPO, LIST, X, PSSQ, DA, DR, DIC

def PSS433(DFN, LIST):
    if LIST == "":
        ^TMP($J, LIST, 0) = "-1^NO DATA FOUND"
        return
    if DFN <= 0:
        ^TMP($J, LIST, 0) = "-1^NO DATA FOUND"
        return
    if not exists(^PS(55, DFN)):
        ^TMP($J, LIST, 0) = "-1^NO DATA FOUND"
        return
    PSSIEN = 0
    ^TMP($J, LIST, 0) = 0
BGN433:
    PSSIEN = next(^PS(55, DFN, 5, PSSIEN), 0)
    if PSSIEN <= 0:
        ^TMP($J, LIST, 0) = -1 if ^TMP($J, LIST, 0) == 0 else ^TMP($J, LIST, 0)
        return
    PSSPO = ^PS(55, DFN, 5, PSSIEN, 0)
    IEN, DA(55.06) = PSSIEN
    DIC = 55, DA = DFN, DR = 62, DR(55.06) = ".5;9;25;26;34;41;42;70", DIQ(0) = "IE"
    EN^DIQ1()
    for X in [.5, 9, 25, 26, 34, 41, 42, 70]:
        ^TMP($J, LIST, +PSSIEN, X) = ^UTILITY("DIQ1", $J, 55.06, IEN, X, "I")
    PSSTMP = $P(^PS(55, DFN, 5, PSSIEN, .2), U)
    ^TMP($J, LIST, IEN, 108) = "" if PSSTMP == "" else ORDITEM(+PSSTMP)
    for X in [.5, 9, 25, 34, 70]:
        ^TMP($J, LIST, +PSSIEN, X) = ^TMP($J, LIST, +PSSIEN, X) + "^" + ^UTILITY("DIQ1", $J, 55.06, IEN, X, "E")
    ^TMP($J, LIST, 0) = ^TMP($J, LIST, 0) + 1
    ^TMP($J, LIST, "B", +PSSIEN) = ""
    goto BGN433

def PSS435(DFN, PO, LIST):
    if LIST == "":
        ^TMP($J, LIST, 0) = "-1^NO DATA FOUND"
        return
    if DFN <= 0:
        ^TMP($J, LIST, 0) = "-1^NO DATA FOUND"
        return
    if not exists(^PS(55, DFN, "IV", "AIT", "H")):
        ^TMP($J, LIST, 0) = "-1^NO DATA FOUND"
        return
    PSSDT = 0
AIT:
    PSSDT = next(^PS(55, DFN, "IV", "AIT", "H", PSSDT), 0)
    if PSSDT <= 0:
        AITQ()
        return
    PSSIEN = 0
AIT1:
    PSSIEN = next(^PS(55, DFN, "IV", "AIT", "H", PSSDT, PSSIEN), 0)
    if PSSIEN <= 0:
        goto AIT
    PSSDATA = ^PS(55, DFN, "IV", PSSIEN, 0)
    PSSSTAT = $P(PSSDATA, "^", 17)
    if PSSSTAT != "A" and PO <= 0:
        goto AIT1
    if PO > 0 and PSSIEN != PO:
        goto AIT1
    PSSPO = $P(PSSDATA, "^", 1)
    ^TMP($J, LIST, "B", +PSSIEN) = ""
AITDIQ:
    ^UTILITY("DIQ1", $J) = {}
    DA = DFN, IEN, DA(55.01) = PSSIEN, DIC = 55, DR = 100, DIQ(0) = "IE", DR(55.01) = ".01;.02;.03;.04;.06;.08;.09;.12;.17;.24;9;31;100;104;106;108;110;112;120;121;132"
    EN^DIQ1()
    for X in [.01, .02, .03, .04, .06, .08, .09, .12, .17, .24, 9, 31, 100, 104, 106, 108, 110, 112, 120, 121, 132]:
        ^TMP($J, LIST, PSSPO, X) = ^UTILITY("DIQ1", $J, 55.01, IEN, X, "I")
    for X in [.02, .03, .04, .06, 9, 100, 106, 108, 112, 120, 121, 132]:
        ^TMP($J, LIST, PSSPO, X) = ^TMP($J, LIST, PSSPO, X) + "^" + ^UTILITY("DIQ1", $J, 55.01, IEN, X, "E")
    PSSTMP = $P(^PS(55, DFN, "IV", PSSIEN, .2), U)
    ^TMP($J, LIST, IEN, 130) = "" if PSSTMP == "" else ORDITEM(+PSSTMP)
    K ^UTILITY("DIQ1", $J)
    ^TMP($J, LIST, 0) = ^TMP($J, LIST, 0) + 1
    goto AIT1

def PSS436(DFN, ORDER, LIST):
    if LIST == "":
        ^TMP($J, LIST, 0) = "-1^NO DATA FOUND"
        return
    if DFN <= 0:
        ^TMP($J, LIST, 0) = "-1^NO DATA FOUND"
        return
    if not exists(^PS(55, DFN)):
        ^TMP($J, LIST, 0) = "-1^NO DATA FOUND"
        return
    ^TMP($J, LIST, 0) = 0
    if ORDER == "":
        PSSLOOP = 1
        ORDER = 0
        goto LOOP436
    else:
        PSSPO = next(^PS(55, DFN, "IV", "B", ORDER), 0)
        if PSSPO <= 0:
            PSS436Q()
            return
        else:
            DIQ436()

def DIQ436():
    DA, DR = DFN, DIC = 55, DR = 100, DR(55.01) = ".01;.02;.03;.04;.06;.08;.09;.12;.17;.24;9;31;100;104;106;108;110;112;120;121;132;147", DIQ(0) = "IE"
    EN^DIQ1()
    for X in [.01, .02, .03, .04, .06, .08, .09, .12, .17, .24, 9, 31, 100, 104, 106, 108, 110, 112, 120, 121, 132, 147]:
        ^TMP($J, LIST, PSSPO, X) = ^UTILITY("DIQ1", $J, 55.01, IEN, X, "I")
    for X in [.02, .03, .04, .06, 9, 100, 106, 108, 112, 120, 121, 132, 147]:
        ^TMP($J, LIST, PSSPO, X) = ^TMP($J, LIST, PSSPO, X) + "^" + ^UTILITY("DIQ1", $J, 55.01, IEN, X, "E")
    PSSTMP = $P(^PS(55, DFN, "IV", PSSPO, .2), U)
    ^TMP($J, LIST, IEN, 130) = "" if PSSTMP == "" else ORDITEM(+PSSTMP)
    ^TMP($J, LIST, "B", PSSPO) = ""
    ^TMP($J, LIST, 0) = ^TMP($J, LIST, 0) + 1
    PSSA = 0
    ^TMP($J, LIST, PSSPO, "ADD", 0) = 0
PSSA:
    PSSA = next(^PS(55, DFN, "IV", PSSPO, "AD", PSSA), 0)
    if PSSA <= 0:
        PSSS = 0
        ^TMP($J, LIST, PSSPO, "SOL", 0) = 0
        goto PSSS
    PSSDATA = ^PS(55, DFN, "IV", PSSPO, "AD", PSSA, 0)
    X1 = $P(PSSDATA, "^")
    X2 = $P(PSSDATA, "^", 2)
    ^TMP($J, LIST, PSSPO, "ADD", PSSA, .01) = X1 + "^" + $P(^PS(52.6, X1, 0), "^")
    ^TMP($J, LIST, PSSPO, "ADD", PSSA, .02) = X2
    ^TMP($J, LIST, PSSPO, "ADD", PSSA, .03) = X3
    ^TMP($J, LIST, PSSPO, "ADD", 0) = ^TMP($J, LIST, PSSPO, "ADD", 0) + 1
    goto PSSA
PSSS:
    if ^TMP($J, LIST, PSSPO, "ADD", 0) <= 0:
        ^TMP($J, LIST, PSSPO, "ADD", 0) = "-1^NO DATA FOUND"
    PSSS = next(^PS(55, DFN, "IV", PSSPO, "SOL", PSSS), 0)
    if PSSS <= 0:
        if ^TMP($J, LIST, PSSPO, "SOL", 0) <= 0:
            ^TMP($J, LIST, PSSPO, "SOL", 0) = "-1^NO DATA FOUND"
        LOOP436()
        return
    PSSDATA = ^PS(55, DFN, "IV", PSSPO, "SOL", PSSS, 0)
    X1 = $P(PSSDATA, "^")
    X2 = $P(PSSDATA, "^", 2)
    ^TMP($J, LIST, PSSPO, "SOL", PSSS, .01) = X1 + "^" + $P(^PS(52.7, X1, 0), "^")
    ^TMP($J, LIST, PSSPO, "SOL", PSSS, 1) = X2
    ^TMP($J, LIST, PSSPO, "SOL", 0) = ^TMP($J, LIST, PSSPO, "SOL", 0) + 1
    goto PSSS

def PSS436Q():
    ^UTILITY("DIQ1", $J) = {}
    if not exists(^TMP($J, LIST, "B")):
        ^TMP($J, LIST, 0) = "-1^NO DATA FOUND"
    K PSSPO, PSSA, PSSDATA, X, LIST, X1, X2, PSSS, ORDER, PSSLOOP, DA, DR, DIC

def NODATA():
    ^TMP($J, LIST, 0) = "-1^NO DATA FOUND"

def Q():
    K IEN, PSSA, PSSS, PSSSTAT, X, LIST, X1, X2, X3, PSSDIY