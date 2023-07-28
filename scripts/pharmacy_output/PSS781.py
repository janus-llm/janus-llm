def PSS(PSSDFN, PSSNUM, LIST):
    # PSSDFN: IEN of Patient [REQUIRED]
    # PSSNUM: CLOZAPINE REGISTRATION NUMBER
    # LIST: Subscript name used in ^TMP global [REQUIRED]
    if LIST == "":
        return
    ^TMP($J,LIST) = {}
    PSSIEN, DA, DR, DIC = None, None, None, None
    if PSSDFN <= 0 and PSSNUM == "":
        ^TMP($J,LIST,0) = "-1^NO DATA FOUND"
        return
    if PSSNUM != "" and PSSDFN <= 0:
        PSSDFN = $O(^PS(55,"ASAND1",PSSNUM,0))
        if PSSDFN <= 0:
            NODATA()
            return
    PSSIEN = PSSDFN
    ^UTILITY("DIQ1",$J), DIQ = {}, {}
    DA, IEN = PSSDFN, PSSDFN
    DIC = 55
    DR = "53:58"
    DIQ(0) = "IE"
    EN^DIQ1()
    if not ^UTILITY("DIQ1",$J):
        NODATA()
        return
    for PSSIEN in range(53, 59):
        ^TMP($J,LIST,PSSDFN,PSSIEN) = ^UTILITY("DIQ1",$J,55,IEN,PSSIEN,"I")
    for PSSIEN in [54, 55, 56, 57, 58]:
        if ^UTILITY("DIQ1",$J,55,IEN,PSSIEN,"I") == ^UTILITY("DIQ1",$J,55,IEN,PSSIEN,"E"):
            ^TMP($J,LIST,PSSDFN,PSSIEN) = "" + "^" + ^UTILITY("DIQ1",$J,55,IEN,PSSIEN,"E")
        else:
            ^TMP($J,LIST,PSSDFN,PSSIEN) = ^TMP($J,LIST,PSSDFN,PSSIEN) + "^" + ^UTILITY("DIQ1",$J,55,IEN,PSSIEN,"E")
    for X in range(53, 59):
        if ^TMP($J,LIST,PSSDFN,X) == "^":
            ^TMP($J,LIST,PSSDFN,X) = ""
    ^UTILITY("DIQ1",$J), DIQ, DIC, DA = {}, {}, {}, {}

def NODATA():
    ^TMP($J,LIST,0) = "-1^NO DATA FOUND"

def WRT(PSSDFN, PSSSTAT, LIST):
    # Sets Clozapine Status field for Mental Health
    # PSSDFN = DFN of Patient (REQUIRED)
    # PSSSTAT = Clozapine Status (REQUIRED)
    # LIST: Subscript name used in ^TMP global [REQUIRED]
    if PSSDFN <= 0:
        return
    if PSSSTAT == "":
        return
    if LIST == "":
        return
    if not ^PS(55,PSSDFN):
        ^TMP($J,LIST,0) = 0
        return
    if PSSSTAT != "D" and PSSSTAT != "H" and PSSSTAT != "A":
        ^TMP($J,LIST,0) = 0
        return
    ^PS(55,PSSDFN,"SAND") = ^TMP($J,LIST,0) = 1