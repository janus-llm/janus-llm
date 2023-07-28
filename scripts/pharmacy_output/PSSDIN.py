def PSSDIN(PSSOI=None, PSSDD=None):
    global PSSDIN
    PSSDIN = {}
    if PSSOI is not None:
        OITM()
    if PSSDD is not None:
        DPDRG()

def OITM():
    if not any(a for a in ^PS(50.7,PSSOI,1,0)):
        return
    TY = "OI"
    TD = PSSOI
    for IDX in ^PS(50.7,TD,1,0):
        IEN = ^PS(50.7,PSSOI,1,IDX,0)
        FTX()

def FTX():
    global PSSDIN
    if IEN and ^PS(51.7,IEN):
        if ^PS(51.7,IEN,0)[2] or ^PS(51.7,IEN,0)[2] > (DT - 1):
            for WP in ^PS(51.7,IEN,2,0):
                if ^PS(51.7,IEN,2,WP,0):
                    PSSDIN[TY, TD, IEN, WP] = ^PS(51.7,IEN,2,WP,0)

def DPDRG():
    if not any(a for a in ^PSDRUG(PSSDD,9,0)):
        return
    TY = "DD"
    TD = PSSDD
    for IDX in ^PSDRUG(TD,9,0):
        IEN = ^PSDRUG(PSSDD,9,IDX,0)
        FTX()

def PROMPT():
    global PSSDIN
    if not any(a for a in ^TMP("PSSDIN",$J,"OI",0)) and not any(a for a in ^TMP("PSSDIN",$J,"DD",0)):
        return ""
    PSSOI = ^TMP("PSSDIN",$J,"OI",0)
    PSSDD = ^TMP("PSSDIN",$J,"DD",0)
    READ1()

def READ1():
    global PSSDD, PSSOI
    if PSSDD and PSSOI:
        DIR(0) = "SB^N:NO;D:DISPENSE DRUG;O:ORDERABLE ITEM;B:ORDERABLE ITEM AND DISPENSE DRUG"
    elif PSSOI:
        DIR(0) = "SB^N:NO;O:ORDERABLE ITEM"
    elif PSSDD:
        DIR(0) = "SB^N:NO;D:DISPENSE DRUG"
    else:
        return

    DIR("A") = "  Restriction/Guideline(s) exist.  Display? "
    DIR("B") = "No"
    ^TMP("PSSDIN",$J,"OI",0) = PSSOI
    ^TMP("PSSDIN",$J,"DD",0) = PSSDD
    PSSOI = None
    PSSDD = None
    ^TMP("PSSDIN",$J) = {}
    ^TMP("PSSDIN",$J) = ""