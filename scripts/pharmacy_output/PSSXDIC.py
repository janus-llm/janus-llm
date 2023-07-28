# PSSXDIC ;;OIFIO BAY PINES/ELR - UPDATE DESCRIPTION OF FILE 54 - 3/2/2004
# 1.0; PHARMACY DATA MANAGEMENT;**84**;9/30/97
def START():
    if '$D(^PS(54,"B","NO TRANSFER")):
        ZTQUE()
        return
    DA = $O(^PS(54,"B","NO TRANSFER",0))
    if not DA:
        ZTQUE()
        return
    PSSDA = None
    PSSDIC = {}
    PSSI = None
    PSSIENS = None
    FDA = None
    PSSDIC[1] = "CAUTION: Federal law prohibits the"
    PSSDIC[2] = "transfer of this drug to any person"
    PSSDIC[3] = "other than the patient for whom it"
    PSSDIC[4] = "was prescribed."
    LOCK +^PS(54,DA)
    for PSSI in range(1, 5):
        PSSDA = [PSSI, DA]
        FDA()
        SET()
    LOCK -^PS(54,DA)
    DA = None
    XMDUZ = None

def FDA():
    PSSIENS = $$IENS^DILF(.PSSDA)
    FDA^DILF(54.1,PSSIENS,.01,"",PSSDIC(PSSI),"FDA(54)")

def SET():
    FILE^DIE("","FDA(54)","PSSIENS")
    if $G(^TMP("DIERR",$J,1)):
        ZTQUE()

def BULL():
    PSSLN = 0
    K ^TMP("PSSDIC",$J)
    XMSUB = "DICITONARY MAINTENANCE (FILE 54) "
    XMY = []
    XMTEXT = "^TMP(""PSSDIC"",$J,"
    XMY.append(DUZ) if DUZ else XMY.append(.5)
    XMDUZ = .5
    NOW^%DTC()
    PSSMSG = " "
    SETLN()
    PSSMSG = "The update of file RX CONSULT, NO TRANSFER description failed."
    SETLN()
    PSSMSG = " "
    SETLN()
    ^XMD()

def SETLN():
    PSSLN += 1
    ^TMP("PSSDIC",$J,PSSLN) = PSSMSG

def ZTQUE():
    ZTIO = ""
    ZTDTH = $H
    $P(ZTDTH,",",2) = $P(ZTDTH,",",2) + 60
    ZTDESC = "PDM UPDATE ERROR"
    ZTRTN = "BULL^PSSXDIC"
    ^%ZTLOAD()