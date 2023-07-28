# PSSP191A ;BIRMINGHAM/GN/DRP-Diagnostic Report only, does not update ; 9/25/15 2:36pm
# ;;1.0;PHARMACY DATA MANAGEMENT;**191**;9/30/97;Build 40
def PSSP191A():
    return

def QUE():
    NAMSP="PSSP191A"
    JOBN="PSS*1*191 Post Install Diagnostic Report"
    PATCH="PSS*1*191"
    Y=NOW()
    ZTDTH=FMTH(Y)

    BMES("=============================================================")
    MES("Queuing background job for " + JOBN + "...")
    MES("Start time: " + HTE(ZTDTH))
    MES("A MailMan message will be sent to the installer upon Post")
    MES("Install Completion.  This may take an hour.")
    MES("==============================================================")

    ZTRTN="EN^"+NAMSP
    ZTIO=""
    SBJM=JOBN
    ZTDESC="Background job for "+JOBN
    ZTSAVE("JOBN")=""
    ZTSAVE("ZTDTH")=""
    ZTSAVE("DUZ")=""
    ZTSAVE("SBJM")=""
    ZTLOAD()
    if ZTSK:
        MES("*** Task #" + ZTSK + " Queued! ***")
        BMES("")
        ZTSAVE("ZTSK")=""
    BMES("")
    XPDQUES = None

def EN(P1=""):
    PSSDUZ=DUZ
    ORDSDT=NOW()
    ^TMP($J,"PSSP191A")=""
    ^TMP($J,"PSSP191A",0)=" "
    ^TMP($J,"PSSP191A",1)=" "
    ^TMP($J,"PSSP191A",2)="Active Orders for Medications Requiring Removal (MRR)."
    ^TMP($J,"PSSP191A",3)="Prior to Installation of PSJ*5*315 these orders should be "
    ^TMP($J,"PSSP191A",4)="reviewed for planning purposes, but no action taken."
    ^TMP($J,"PSSP191A",5)=" Once PSJ*5*315 is installed they will need to be Discontinued"
    ^TMP($J,"PSSP191A",6)=" and re-entered after coordinating with your Pharmacy ADPAC."
    ^TMP($J,"PSSP191A",7)=" This report can be recalled from the PSS MGR Menu."
    ^TMP($J,"PSSP191A",8)=" "
    ^TMP($J,"PSSP191A",9)="             Sorted by Patient within Ward"
    ^TMP($J,"PSSP191A",10)="Pat    Patient               Orderable             Ordr  MRR"
    ^TMP($J,"PSSP191A",11)="ID     Loc                   Item Name             Sts   Val"
    ^TMP($J,"PSSP191A",12)="-----  --------------------  --------------------  ----  ---"
    ^TMP($J,"PSSP191A",13)=" "
    PSSLN=14
    PSSSPCE=" "*20
    LOC=""
    while LOC != "":
        ID=""
        while ID != "":
            STR=^XTMP("PSSP191A",$J,LOC,ID)
            DDTXT=$P(STR,U)
            STS=$P(STR,U,2)
            MRR=$P(STR,U,3)
            ^TMP($J,"PSSP191A",PSSLN)=ID_PSSSPCE[:5] + "  " + FMTE(LOC,5)_PSSSPCE[:20] + "  " + DDTXT_PSSSPCE[:20] + "  " + STS_PSSSPCE[:4] + "  " + MRR_PSSSPCE[:3]
            ORDTOT=ORDTOT+1
            PSSLN=PSSLN+1
        PSSLN=PSSLN+1
    ^TMP($J,"PSSP191A",PSSLN)="Total Orders found: "+ORDTOT

def MAKERPT():
    # omitted for brevity

def SENDRPT():
    XMY(PSSDUZ)=""
    X=""
    while X != "":
        XMY(X)=""
    X=""
    while X != "":
        XMY(X)=""
    X=""
    while X != "":
        XMY(X)=""
    X=""
    while X != "":
        XMY(X)=""
    XMSUB="PHARMACY ORDERABLE ITEM MANAGEMENT"
    XMTEXT="^TMP("_$J_","_"""PSSP191A"""_","
    XMDUZ=.5
    XMY(PSSDUZ)=""
    ^XTMP("PSSP191A") = None

def TST():
    P1 = 1
    EN(P1)