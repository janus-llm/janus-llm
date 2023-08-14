# PSSP170 ;DAL/RJS-PSS*1.0*170 POST INSTALL ROUTINE
# 1.0;PHARMACY DATA MANAGEMENT;**170**;9/30/97;Build 6
# Reference to $$UP^XLFST is covered by DBIA #10104

def POSTINT():
    ZTDESC = "PSS*1*170 Post Install"
    ZTIO = ""
    ZTDTH = $H
    ZTRTN = "POST^PSSP170"
    ZTSAVE = ""
    ^%ZTLOAD()

    ^XPDUTL("PSS*1*170 Post Install Task Queued!")
    K ZTDESC,ZTDTH,ZTIO,ZTRTN,ZTSAVE

def POST():
    PSSNAM = ""
    while PSSNAM != "":
        PSSINDX = $$UP^XLFST(PSSNAM)
        PSSFLG = 0
        PSSIEN = 0
        while PSSIEN:
            PSSIEN = $O(^PS(51,"B",PSSNAM,PSSIEN))
            if PSSIEN:
                PSSSYN = ""
                PSSSYN = $P(^PS(51,PSSIEN,0),"^",3)
                PSSNAME = ""
                PSSNAME = $P(^PS(51,PSSIEN,0),"^",1)
                if PSSNAME == PSSSYN:
                    ^TMP($J,"PSSP170-1","S",PSSNAM,PSSIEN) = ^PS(51,PSSIEN,0)
                if $O(^PS(51,"B",PSSNAM,PSSIEN)):
                    PSSFLG = 1
                if PSSFLG:
                    ^TMP($J,"PSSP170-1","D",PSSNAM,PSSIEN) = ^PS(51,PSSIEN,0)
                if PSSINDX != PSSNAM:
                    ^TMP($J,"PSSP170-1","M",PSSNAM,PSSIEN) = ^PS(51,PSSIEN,0)
    
    PSSIEN = 0
    PSSCNT = 1
    ^TMP($J,"PSSP170",PSSCNT) = "PSS*1*170 Duplicate/Mixedcase Medication Instructions Report"
    PSSCNT = PSSCNT + 1
    PSSTXT = ""
    for PSSCTR in range(1, 80):
        PSSTXT = PSSTXT + "-"
    ^TMP($J,"PSSP170",PSSCNT) = PSSTXT
    PSSCNT = PSSCNT + 1
    ^TMP($J,"PSSP170",PSSCNT) = ""
    PSSCNT = PSSCNT + 1
    ^TMP($J,"PSSP170",PSSCNT) = "The following Medication Instructions have been identified as having a name"
    PSSCNT = PSSCNT + 1
    ^TMP($J,"PSSP170",PSSCNT) = "or a synonym that are the same."
    PSSCNT = PSSCNT + 1
    ^TMP($J,"PSSP170",PSSCNT) = ""
    PSSCNT = PSSCNT + 1
    if not $D(^TMP($J,"PSSP170-1")):
        GOTO EXIT
    HDR()

TMP: 
    PSSNAM = ""
    while PSSNAM != "":
        PSSTXT = ""
        TXT(PSSNAM_" **",1)
        PSSIEN = 0
        while PSSIEN:
            PSSIEN = $O(^TMP($J,"PSSP170-1","D",PSSNAM,PSSIEN))
            if PSSIEN:
                K PSSNM,PSSSYN
                PSSNM = $P(^TMP($J,"PSSP170-1","D",PSSNAM,PSSIEN),"^",1)
                if PSSNM == PSSNAM:
                    PSSNM = PSSNM + "**"
                TXT(PSSNM,20)
                TXT($P(^TMP($J,"PSSP170-1","D",PSSNAM,PSSIEN),"^",2),40)
                PSSSYN = $P(^TMP($J,"PSSP170-1","D",PSSNAM,PSSIEN),"^",3)
                if PSSSYN == PSSNAM:
                    PSSSYN = PSSSYN + "**"
                TXT(PSSSYN,60)
                ^TMP($J,"PSSP170",PSSCNT) = PSSTXT
                PSSCNT = PSSCNT + 1
                PSSTXT = ""
    
    ^TMP($J,"PSSP170",PSSCNT) = ""
    PSSCNT = PSSCNT + 1
    ^TMP($J,"PSSP170",PSSCNT) = "The duplicate** items will need to be changed to a unique name or synonym"
    PSSCNT = PSSCNT + 1
    ^TMP($J,"PSSP170",PSSCNT) = ""
    PSSCNT = PSSCNT + 1
    PSSTXT = ""
    for PSSCTR in range(1, 80):
        PSSTXT = PSSTXT + "="
    ^TMP($J,"PSSP170",PSSCNT) = PSSTXT
    PSSCNT = PSSCNT + 1
    PSSTXT = ""
    ^TMP($J,"PSSP170",PSSCNT) = ""
    PSSCNT = PSSCNT + 1
    ^TMP($J,"PSSP170",PSSCNT) = "The following Medication Instructions have been identified as having a Synonym"
    PSSCNT = PSSCNT + 1
    ^TMP($J,"PSSP170",PSSCNT) = "containing lowercase letters."
    PSSCNT = PSSCNT + 1
    PSSTXT = ""
    for PSSCTR in range(1, 80):
        PSSTXT = PSSTXT + "-"
    ^TMP($J,"PSSP170",PSSCNT) = PSSTXT
    PSSCNT = PSSCNT + 1
    PSSTXT = ""
    ^TMP($J,"PSSP170",PSSCNT) = PSSTXT
    PSSCNT = PSSCNT + 1
    PSSTXT = ""
    TXT("Lowercase **",1)
    TXT("Name",20)
    TXT("Expansion",40)
    TXT("Synonym",60)
    ^TMP($J,"PSSP170",PSSCNT) = PSSTXT
    PSSCNT = PSSCNT + 1
    PSSTXT = ""
    PSSNAM = ""
    while PSSNAM != "":
        PSSTXT = ""
        TXT(PSSNAM_" **",1)
        PSSIEN = 0
        while PSSIEN:
            PSSIEN = $O(^TMP($J,"PSSP170-1","M",PSSNAM,PSSIEN))
            if PSSIEN:
                K PSSNM,PSSSYN
                PSSNM = $P(^TMP($J,"PSSP170-1","M",PSSNAM,PSSIEN),"^",1)
                if PSSNM == PSSNAM:
                    PSSNM = PSSNM + "**"
                TXT(PSSNM,20)
                TXT($P(^TMP($J,"PSSP170-1","M",PSSNAM,PSSIEN),"^",2),40)
                PSSSYN = $P(^TMP($J,"PSSP170-1","M",PSSNAM,PSSIEN),"^",3)
                if PSSSYN == PSSNAM:
                    PSSSYN = PSSSYN + "**"
                TXT(PSSSYN,60)
                ^TMP($J,"PSSP170",PSSCNT) = PSSTXT
                PSSCNT = PSSCNT + 1
                PSSTXT = ""
    
    PXRMINDX()
    MAIL()

EXIT: 
    K ^TMP($J),PSSCNT,PSSCTR,PSSIEN,PSSDAS,PSSDFN,PSSINS,PSSNAM,PSSPOI,PSSSDT,PSSSTOP,PSSSTRT,PSSTXT,PSSFLG,PSSINDX,PSSNAME,PSSUSER,XMDUZ,XMSUB,XMTEXT,XMY

def TXT(PSSVAL,PSSCAL):
    if '$D(PSSTXT):
        PSSTXT = ""
    PSSTXT = $$SETSTR^VALM1(PSSVAL,PSSTXT,PSSCAL,len(PSSVAL))

def MAIL():
    PSSCNT = PSSCNT + 1
    ^TMP($J,"PSSP170",PSSCNT) = "***** End Of Report *****"
    XMSUB = "PSS*1*170 Duplicate/Mixedcase Medication Instructions Report"
    XMTEXT = "^TMP($J,""PSSP170"","
    XMDUZ = "PSS*1*170 Post Install"
    for PSSUSER in range(0, len(^XUSEC("PSNMGR"))):
        if PSSUSER != 0.5:
            XMY(PSSUSER) = ""
    XMY(DUZ) = ""
    ^XMD()

def HDR():
    PSSTXT = ""
    TXT("Duplicate **",1)
    TXT("Name",20)
    TXT("Expansion",40)
    TXT("Synonym",60)
    ^TMP($J,"PSSP170",PSSCNT) = PSSTXT
    PSSCNT = PSSCNT + 1
    PSSTXT = ""
    for PSSCTR in range(1, 80):
        PSSTXT = PSSTXT + "-"
    ^TMP($J,"PSSP170",PSSCNT) = PSSTXT

def PXRMINDX():
    PSSPOI = 0
    while PSSPOI:
        PSSPOI = $O(^PXRMINDX("55NVA","IP",PSSPOI))
        if PSSPOI:
            PSSDFN = 0
            while PSSDFN:
                PSSDFN = $O(^PXRMINDX("55NVA","IP",PSSPOI,PSSDFN))
                if PSSDFN:
                    PSSSTRT = 0
                    while PSSSTRT:
                        PSSSTRT = $O(^PXRMINDX("55NVA","IP",PSSPOI,PSSDFN,PSSSTRT))
                        if PSSSTRT:
                            PSSSTOP = ""
                            while PSSSTOP != "":
                                PSSSTOP = $O(^PXRMINDX("55NVA","IP",PSSPOI,PSSDFN,PSSSTRT,PSSSTOP))
                                if PSSSTOP != "":
                                    if PSSSTOP["U":
                                        PSSSDT = $P(PSSSTOP,"U",2)
                                        if len(PSSDFN) != len(PSSSDT):
                                            PSSSDT = "U" + PSSDFN
                                        PSSDAS = ""
                                        while PSSDAS != "":
                                            PSSDAS = $O(^PXRMINDX("55NVA","IP",PSSPOI,PSSDFN,PSSSTRT,PSSSTOP,PSSDAS))
                                            if PSSDAS != "":
                                                K ^PXRMINDX("55NVA","IP",PSSPOI,PSSDFN,PSSSTRT,PSSSTOP,PSSDAS)
                                                ^PXRMINDX("55NVA","IP",PSSPOI,PSSDFN,PSSSTRT,PSSSDT,PSSDAS) = ""

    PSSDFN = 0
    while PSSDFN:
        PSSDFN = $O(^PXRMINDX("55NVA","PI",PSSDFN))
        if PSSDFN:
            PSSPOI = 0
            while PSSPOI:
                PSSPOI = $O(^PXRMINDX("55NVA","PI",PSSDFN,PSSPOI))
                if PSSPOI:
                    PSSSTRT = 0
                    while PSSSTRT:
                        PSSSTRT = $O(^PXRMINDX("55NVA","PI",PSSDFN,PSSPOI,PSSSTRT))
                        if PSSSTRT:
                            PSSSTOP = ""
                            while PSSSTOP != "":
                                PSSSTOP = $O(^PXRMINDX("55NVA","PI",PSSDFN,PSSPOI,PSSSTRT,PSSSTOP))
                                if PSSSTOP != "":
                                    if PSSSTOP["U":
                                        PSSSDT = $P(PSSSTOP,"U",2)
                                        if len(PSSDFN) != len(PSSSDT):
                                            PSSSDT = "U" + PSSDFN
                                        PSSDAS = ""
                                        while PSSDAS != "":
                                            PSSDAS = $O(^PXRMINDX("55NVA","PI",PSSDFN,PSSPOI,PSSSTRT,PSSSTOP,PSSDAS))
                                            if PSSDAS != "":
                                                K ^PXRMINDX("55NVA","PI",PSSDFN,PSSPOI,PSSSTRT,PSSSTOP,PSSDAS)
                                                ^PXRMINDX("55NVA","PI",PSSDFN,PSSPOI,PSSSTRT,PSSSDT,PSSDAS) = ""

POSTINT()