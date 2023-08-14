def ALL(PSSIEN, PSSFT, LIST):
    """
    PSSIEN - IEN of entry in ADMINISTRATION SHIFT file (#51.15).
    PSSFT - Free Text name in ADMINISTRATION SHIFT file (#51.15).
    LIST - Subscript of ^TMP array in the form ^TMP($J,LIST,Field Number where Field Number is the Field Number
           of the data piece being returned.
    Returns NAME field (#.01), ABBREVIATION field (#1), STANDARD START/STOP TIMES field (#2), PACKAGE field (#4),
    HOSPITAL LOCATION multiple (#51.153), HOSPITAL LOCATION field (#.01), and START/STOP TIMES field (#1)
    of ADMINISTRATION SHIFT file (#51.15).
    """
    # Variable definitions here

    if LIST == '':
        return
    ^TMP($J,LIST) = {}
    if PSSIEN <= 0 and PSSFT == '':
        ^TMP($J,LIST,0) = -1 + '^' + 'NO DATA FOUND'
        return
    if PSSIEN > 0:
        PSSIEN2 = $$FIND1^DIC(51.15,"","A","`"_PSSIEN,,,"")
        if PSSIEN2 <= 0:
            ^TMP($J,LIST,0) = -1 + '^' + 'NO DATA FOUND'
            return
        ^TMP($J,LIST,0) = 1
        GETS^DIQ(51.15,+PSSIEN2,".01;1;2;4;3*","IE","PSS5115")
        PSS(1) = 0
        PSSIEN = +PSSIEN2
        while PSS(1):
            SETZRO()
            (CNT,PSS(2)) = 0
            while PSS(2):
                SETLOC()
                CNT += 1
            ^TMP($J,LIST,+PSSIEN,"HOSP",0) = $G(CNT) if $G(CNT) > 0 else "-1^NO DATA FOUND"
    if PSSIEN <= 0 and PSSFT != '':
        if PSSFT == "??":
            LOOP(1)
            return
        FIND^DIC(51.15,,"@;.01;1","QP",PSSFT,,"B",,,"")
        if +^TMP("DILIST",$J,0) == 0:
            ^TMP($J,LIST,0) = -1 + '^' + 'NO DATA FOUND'
            return
        ^TMP($J,LIST,0) = +^TMP("DILIST",$J,0)
        PSSXX = 0
        while PSSXX:
            PSSIEN = +^TMP("DILIST",$J,PSSXX,0)
            GETS^DIQ(51.15,+PSSIEN,".01;1;2;4;3*","IE","PSS5115")
            PSS(1) = 0
            while PSS(1):
                SETZRO()
                (CNT,PSS(2)) = 0
                while PSS(2):
                    SETLOC()
                    CNT += 1
                ^TMP($J,LIST,+PSSIEN,"HOSP",0) = $G(CNT) if $G(CNT) > 0 else "-1^NO DATA FOUND"
            PSSXX += 1
    ^TMP("DILIST",$J) = {}

def ACP(PSSPK, PSSABR, LIST):
    """
    PSSPK - PACKAGE field (#4) of ADMINISTRATION SHIFT file (#51.15).
    PSSABR - ABBREVIATION field (#1) of ADMINISTRATION SHIFT file (#51.15).
    LIST - Subscript of ^TMP array in the form ^TMP($J,LIST,Field Number where Field Number is the Field Number
           of the data piece being returned.
    Returns NAME field (#.01), ABBREVIATION field (#1), and PACKAGE field (#4)
    of ADMINISTRATION SHIFT file (#51.15).
    """
    # Variable definitions here

    if LIST == '':
        return
    ^TMP($J,LIST) = {}
    if PSSPK == '' or PSSABR == '':
        ^TMP($J,LIST,0) = -1 + '^' + 'NO DATA FOUND'
        return
    if PSSPK != '' and PSSABR != '':
        SCR("S") = "I $P(^(0),""^"",4)=PSSPK"
        FIND^DIC(51.15,,"@;.01;1","QP",PSSABR,,"C",SCR("S"),,"")
        if +^TMP("DILIST",$J,0) == 0:
            ^TMP($J,LIST,0) = -1 + '^' + 'NO DATA FOUND'
            return
        ^TMP($J,LIST,0) = +^TMP("DILIST",$J,0)
        PSSXX = 0
        while PSSXX:
            PSSIEN = +^TMP("DILIST",$J,PSSXX,0)
            GETS^DIQ(51.15,+PSSIEN,".01;1;4","IE","PSS5115")
            PSS(1) = 0
            while PSS(1):
                SETZRO2()
            PSSXX += 1
    ^TMP("DILIST",$J) = {}

def SETZRO():
    """
    Sets the values of ^TMP array for the given PSS(1) index in the ALL function.
    """
    ^TMP($J,LIST,+PSS(1),.01) = $G(PSS5115(51.15,PSS(1),.01,"I"))
    ^TMP($J,LIST,"B",$G(PSS5115(51.15,PSS(1),.01,"I")),+PSS(1)) = ""
    ^TMP($J,LIST,+PSS(1),1) = $G(PSS5115(51.15,PSS(1),1,"I"))
    ^TMP($J,LIST,+PSS(1),2) = $G(PSS5115(51.15,PSS(1),2,"I"))
    ^TMP($J,LIST,+PSS(1),4) = $G(PSS5115(51.15,PSS(1),4,"I"))

def SETLOC():
    """
    Sets the values of ^TMP array for the given PSS(1) and PSS(2) indexes in the ALL function.
    """
    ^TMP($J,LIST,+PSS(1),"HOSP",+PSS(2),.01) = "" if $G(PSS5115(51.153,PSS(2),.01,"I")) == "" else PSS5115(51.153,PSS(2),.01,"I") + '^' + PSS5115(51.153,PSS(2),.01,"E")
    ^TMP($J,LIST,+PSS(1),"HOSP",+PSS(2),1) = $G(PSS5115(51.153,PSS(2),1,"I"))

def SETZRO2():
    """
    Sets the values of ^TMP array for the given PSS(1) index in the ACP function.
    """
    ^TMP($J,LIST,+PSS(1),.01) = $G(PSS5115(51.15,PSS(1),.01,"I"))
    ^TMP($J,LIST,"ACP",PSSPK,$G(PSS5115(51.15,PSS(1),.01,"I")),+PSS(1)) = ""
    ^TMP($J,LIST,+PSS(1),1) = $G(PSS5115(51.15,PSS(1),1,"I"))
    ^TMP($J,LIST,+PSS(1),4) = $G(PSS5115(51.15,PSS(1),4,"I"))

def LOOP(PSS):
    """
    Loops through all entries in the ADMINISTRATION SHIFT file (#51.15).
    """
    (CNT2,CNT) = 0
    PSSIEN = 0
    while PSSIEN:
        @(PSS)
        CNT2 += 1
    ^TMP("DILIST",$J) = {}

def 1():
    """
    Helper function for the LOOP function in the ALL function.
    """
    GETS^DIQ(51.15,+PSSIEN,".01;1;2;4;3*","IE","PSS5115")
    PSS(1) = 0
    while PSS(1):
        SETZRO()
        (CNT,PSS(2)) = 0
        while PSS(2):
            SETLOC()
            CNT += 1
        ^TMP($J,LIST,PSSIEN,"HOSP",0) = $G(CNT) if $G(CNT) > 0 else "-1^NO DATA FOUND"
    ^TMP($J,LIST,0) = $G(CNT2) if $G(CNT2) > 0 else "-1^NO DATA FOUND"