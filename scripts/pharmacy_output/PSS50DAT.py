def PSS50DAT(PSSIEN, PSSFT, PSSFL, PSSPK, PSSRTOI, LIST):
    """
    BHAM ISC/TSS - CONTINUATION OF API FOR INFORMATION FROM FILE 50
    """
    # Variable Definitions
    # PSSIEN - IEN of entry in 50
    # PSSFT - Free Text name in 50
    # PSSFL - Inactive flag - "" - All entries
    #                        FileMan Date - Only entries with no Inactive Date or an Inactive Date greater than this date.
    # PSSPK - Application Package's Use - "" - All entries
    #                                         Alphabetic codes that represent the DHCP packages that consider this drug to be
    #                                         part of their formulary.
    # PSSRTOI - Orderable Item - return only entries matched to a Pharmacy Orderable Item
    # LIST - Subscript of ^TMP array in the form ^TMP($J,LIST,Field Number where Field Number is the Field Number of the data
    #        piece being returned.
    # Reference to ^PSNDF(50.68 is supported by DBIA 3735
    
    # NEW UNPROTECTED FILEMAN VARIABLES
    DO, DINDEX, DISUB, DIVAL = None, None, None, None
    PSSBGCNT = 0
    PSSCNT = 0
    PSSTIEN = None
    PSSTMP = None
    PSSOLD = None
    PSSALT = None
    PSSMATCH = None
    PSSSYN = None
    PSSCAP = None

    PSSBGCNT = 0
    SCR = {"S": ""}
    
    if not LIST:
        return
    
    if PSSIEN is None and not PSSFT:
        return -1, "NO DATA FOUND"
    
    ^TMP("DILIST",$J) = {}
    ^TMP($J,LIST) = {}
    SCR["S"] = ""
    
    if PSSFL > 0 or PSSPK or PSSRTOI == 1:
        PSS5ND, PSSZ3, PSSZ4 = SETSCRN^PSS50A()
    
    if PSSIEN > 0:
        PSSIEN2 = FIND1^DIC(50, "", "A", "`" + PSSIEN, , SCR["S"], "")
        ^TMP("PSSP50",$J) = {}
        COUNTBG()
        if PSSIEN2 > 0:
            DIRREAD()
    
    if PSSIEN == 0:
        if PSSFT == "??":
            LOOPDIR()
        else:
            FIND^DIC(50, , "@;.01", "QP", PSSFT, , "B", SCR["S"], , "")
            LOOPDI()
    
    COUNTBG()
    
    return ^TMP($J,LIST,0)


def COUNTBG():
    """
    CHECKS PSSBGCNT AND FILLS COUNT IN ON 0 NODE OF ^TMP($J,LIST)
    """
    if PSSBGCNT > 0:
        ^TMP($J,LIST,0) = PSSBGCNT
    else:
        ^TMP($J,LIST,0) = -1 + "^" + "NO DATA FOUND"


def LOOPDI():
    """
    LOOPS ON "DILIST" FROM FILEMAN CALL (USED FOR RETURNING MULTIPLE DRUGS FROM PSSFT)
    """
    PSSTIEN = 0
    while PSSTIEN:
        PSSIEN2 = $P(^TMP("DILIST",$J,PSSTIEN,0),U,1)
        DIRREAD()


def LOOPDIR():
    """
    LOOP FOR A DIRECT READ.  READS ALL IENs FOR ^PSDRUG(
    """
    PSSIEN2 = 0
    while PSSIEN2:
        if $P(^PSDRUG(PSSIEN2,0),U,1):
            DIRALL()


def DIRALL():
    """
    TEST FOR PSSFL, PSSRTOI, PSSPK, BAILS IF CONDITIONS MEET TRUE
    """
    if PSSFL and $P(^PSDRUG(PSSIEN2,"I"),U) and $P(^("I"),U) <= PSSFL:
        return
    if PSSRTOI == 1 and not $P(^PSDRUG(PSSIEN2,2),U):
        return
    if PSSPK:
        PSSZ5 = 0
        for PSSZ6 in range(1, len(PSSPK)):
            if $P(^PSDRUG(PSSIEN2,2),U,3).contains(PSSPK[PSSZ6]):
                PSSZ5 = 1
        if not PSSZ5:
            return
    DIRREAD()
    
    
def DIRREAD():
    """
    MAIN DIRECT READ FOR ENTIRE ROUTINE
    """
    DIRREAD^PSS50TMP()
    SYNONYM()
    ^TMP($J,LIST,"B",^TMP($J,LIST,PSSIEN2,.01),PSSIEN2) = ""
    FORMALT()
    OLD()
    SRVCODE($P(^TMP($J,LIST,PSSIEN2,22),U,1))
    PSSBGCNT = PSSBGCNT + 1


def SYNONYM():
    """
    FILLS SYNONYM MULTIPLE
    """
    PSSCNT = 0
    PSSTMP = ""
    PSSSYN = ""
    while PSSSYN:
        if $P(^PSDRUG(PSSIEN2,1,PSSSYN,0),U,1):
            ^TMP($J,LIST,PSSIEN2,"SYN",PSSSYN,.01) = $P(^PSDRUG(PSSIEN2,1,PSSSYN,0),U,1)
            PSSTMP = $P(^PSDRUG(PSSIEN2,1,PSSSYN,0),U,3)
            if PSSTMP == "0":
                ^TMP($J,LIST,PSSIEN2,"SYN",PSSSYN,1) = PSSTMP + "U" + "TRADE NAME"
            elif PSSTMP == "1":
                ^TMP($J,LIST,PSSIEN2,"SYN",PSSSYN,1) = PSSTMP + "U" + "QUICK CODE"
            elif PSSTMP == "D":
                ^TMP($J,LIST,PSSIEN2,"SYN",PSSSYN,1) = PSSTMP + "U" + "DRUG ACCOUNTABILITY"
            elif PSSTMP == "C":
                ^TMP($J,LIST,PSSIEN2,"SYN",PSSSYN,1) = PSSTMP + "U" + "CONTROLLED SUBSTANCES"
            elif not PSSTMP:
                ^TMP($J,LIST,PSSIEN2,"SYN",PSSSYN,1) = ""
            ^TMP($J,LIST,PSSIEN2,"SYN",PSSSYN,2) = $P(^PSDRUG(PSSIEN2,1,PSSSYN,0),U,2)
            ^TMP($J,LIST,PSSIEN2,"SYN",PSSSYN,403) = $P(^PSDRUG(PSSIEN2,1,PSSSYN,0),U,7)
            PSSCNT = PSSCNT + 1
    if PSSCNT == 0:
        ^TMP($J,LIST,PSSIEN2,"SYN",0) = "-1" + "^" + "NO DATA FOUND"
    else:
        ^TMP($J,LIST,PSSIEN2,"SYN",0) = PSSCNT


def FORMALT():
    """
    FILLS FORMULARY ALTERATIVE MULTIPLE
    """
    PSSCNT = 0
    PSSALT = 0
    while PSSALT:
        if $P(^PSDRUG(PSSIEN2,65,PSSALT,0),U,1):
            ^TMP($J,LIST,PSSIEN2,"FRM",PSSALT,2) = $P(^PSDRUG(PSSIEN2,65,PSSALT,0),U,1) + "U" + $P(^PSDRUG($P(^PSDRUG(PSSIEN2,65,PSSALT,0),U,1),0),U,1)
            PSSCNT = PSSCNT + 1
    if PSSCNT == 0:
        ^TMP($J,LIST,PSSIEN2,"FRM",0) = "-1" + "^" + "NO DATA FOUND"
    else:
        ^TMP($J,LIST,PSSIEN2,"FRM",0) = PSSCNT


def OLD():
    """
    FILLS THE OLD NAME MULTIPLE
    """
    PSSCNT = 0
    PSSOLD = 0
    while PSSOLD:
        if $P(^PSDRUG(PSSIEN2,900,PSSOLD,0),U,2):
            PSSCAP = $UPPER($FMTE($P(^PSDRUG(PSSIEN2,900,PSSOLD,0),U,2)))
            ^TMP($J,LIST,PSSIEN2,"OLD",PSSOLD,.02) = $P(^PSDRUG(PSSIEN2,900,PSSOLD,0),U,2) + "U" + PSSCAP
        else:
            ^TMP($J,LIST,PSSIEN2,"OLD",PSSOLD,.02) = ""
        if $P(^PSDRUG(PSSIEN2,900,PSSOLD,0),U,1):
            ^TMP($J,LIST,PSSIEN2,"OLD",PSSOLD,.01) = $P(^PSDRUG(PSSIEN2,900,PSSOLD,0),U,1)
            PSSCNT = PSSCNT + 1
        else:
            ^TMP($J,LIST,PSSIEN2,"OLD",PSSOLD,.01) = ""
    if PSSCNT == 0:
        ^TMP($J,LIST,PSSIEN2,"OLD",0) = "-1" + "^" + "NO DATA FOUND"
    else:
        ^TMP($J,LIST,PSSIEN2,"OLD",0) = PSSCNT


def SRVCODE(PSSMATCH):
    """
    FILLS SERVICE CODE MULTIPLE
    """
    if PSSMATCH:
        ^TMP($J,LIST,PSSIEN2,400) = $P(^PSNDF(50.68,PSSMATCH,"PFS"),U,1)
    if not $P(^TMP($J,LIST,PSSIEN2,400),U,1):
        ^TMP($J,LIST,PSSIEN2,400) = $P(^PSDRUG(PSSIEN2,"PFS"),U,1)
    if not $P(^TMP($J,LIST,PSSIEN2,400),U,1):
        ^TMP($J,LIST,PSSIEN2,400) = 600000


def DRG(PSSIEN, PSSFT, PSSFL, PSSPK, PSSRTOI, LIST):
    """
    PSSIEN - IEN of entry in 50
    PSSFT - Free Text name in 50
    PSSFL - Inactive flag - "" - All entries
                           FileMan Date - Only entries with no Inactive Date or an Inactive Date greater than this date.
    PSSPK - Application Package's Use - "" - All entries
                                        Alphabetic codes that represent the DHCP packages that consider this drug to be
                                        part of their formulary.
    PSSRTOI - Orderable Item - return only entries matched to a Pharmacy Orderable Item
    LIST - Subscript of ^TMP array in the form ^TMP($J,LIST,Field Number where Field Number is the Field Number of the data
           piece being returned.
    """
    DIERR, ZZERR, PSSP50, SCR, PSS, PSSMLCT = None, None, None, None, None, None

    if not LIST:
        return
    
    ^TMP($J,LIST) = {}
    
    if PSSIEN <= 0 and not PSSFT:
        return -1, "NO DATA FOUND"
    
    PSSP50 = {}
    SCR["S"] = ""
    
    if PSSFL > 0 or PSSPK or PSSRTOI == 1:
        PSS5ND, PSSZ3, PSSZ4 = SETSCRN^PSS50A()
    
    if PSSIEN > 0:
        PSSIEN2 = FIND1^DIC(50, "", "A", "`" + PSSIEN, , SCR["S"], "")
        ^TMP("PSSP50",$J) = {}
        COUNTBG()
        if PSSIEN2 > 0:
            GETS^DIQ(50, +PSSIEN2, ".01;62.01:62.05;905", "IE", "^TMP(""PSSP50"",$J)")
            PSS[1] = 0
            while PSS[1]:
                SETDRG^PSS50A1()
    
    if PSSIEN == 0:
        if PSSFT == "??":
            LOOP^PSS50A1()
        else:
            FIND^DIC(50, , "@;.01", "QP", PSSFT, , "B", SCR["S"], , "")
            LOOPDI()
    
    COUNTBG()
    
    return ^TMP($J,LIST,0)


def LOOP():
    """
    Loop through all drugs in ^PSDRUG
    """
    PSS50DD1, PSS50DD2, PSS50DD3, PSS50DD4, PSS50ER1, PSS50ER2, PSS50ER3, PSS50ER4, PSS51NFD, PSS52NFD, PSSG2N, PSS501NX = {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}
    FIELD^DID(50, 51, "Z", "POINTER", PSS50DD1, PSS50ER1)
    PSS51NFD = PSS50DD1["POINTER"]
    FIELD^DID(50, 52, "Z", "POINTER", PSS50DD2, PSS50ER2)
    PSS52NFD = PSS50DD2["POINTER"]
    FIELD^DID(50, 301, "Z", "POINTER", PSS50DD3, PSS50ER3)
    PSSG2N = PSS50DD3["POINTER"]
    FIELD^DID(50.1, 1, "Z", "POINTER", PSS50DD4, PSS50ER4)
    PSS501NX = PSS50DD4["POINTER"]
    PSSENCT = 0

    PSS[1] = 0
    while PSS[1]:
        if not $P(^PSDRUG(PSS[1],0),U):
            continue
        if PSSFL and $P(^PSDRUG(PSS[1],"I"),U) and $P(^("I"),U) <= PSSFL:
            continue
        if PSSRTOI == 1 and not $P(^PSDRUG(PSS[1],2),U):
            continue
        if PSSPK:
            PSSZ5 = 0
            for PSSZ6 in range(1, len(PSSPK)):
                if $P(^PSDRUG(PSS[1],2),U,3).contains(PSSPK[PSSZ6]):
                    PSSZ5 = 1
            if not PSSZ5:
                continue
        SETSUB1^PSS50AQM(PSS[1])
        SETSUB2^PSS50AQM(PSS[1])
        SETSUB3^PSS50AQM(PSS[1])
        SETALL^PSS50AQM()
        SETOLD^PSS50AQM()
        SETSYN^PSS50AQM()
        SETFMA^PSS50AQM()
        PSSENCT = PSSENCT + 1
    
    ^TMP($J,LIST,0) = PSSENCT if PSSENCT else "-1" + "^" + "NO DATA FOUND"