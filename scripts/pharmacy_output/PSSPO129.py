# PSSPO129 ;BIR/RTR-POST INIT FOR PATCH PSS*1*129 ;06/14/07
# 1.0;PHARMACY DATA MANAGEMENT;**129**;9/30/97;Build 67

import os
import filesec
import HDISVF09
import HDISVCMR
import XPDUTL
import PSSDSPOP
import XM
import XPDMENU

def PSSPO129():
    PSSFACC = {}
    PSSFACCX = {}
    del PSSFACC, PSSFACCX
    PSSFACC["RD"] = "Pp"
    filesec.FILESEC(51.23, PSSFACC, "PSSFACCX")
    del PSSFACC, PSSFACCX
    PSSFACC["RD"] = "Pp"
    filesec.FILESEC(51.24, PSSFACC, "PSSFACCX")
    del PSSFACC, PSSFACCX

    if "HDISVF09.GETIEN" in dir() and "HDISVCMR.EN" in dir():
        XPDUTL.BMES("Initializing standardization of Standard Medication Routes....")
        ST()
        XPDUTL.BMES("Standardization Initialization complete.")

    XPDUTL.BMES("Rebuilding Pharmacy Data Managent Menus....")
    BLD()
    XPDUTL.BMES("Rebuilding menus complete.")

    XPDUTL.BMES("Importing Dosage Form File Data....")
    DS()
    XPDUTL.BMES("Importing data complete.")

    XPDUTL.BMES("Mapping Local Medication Routes....")
    MEDRT()
    XPDUTL.BMES("Mapping Medication Routes complete.")

    XPDUTL.BMES("Mapping Local Possible Dosages....")
    PSSDSPOP.EN()
    XPDUTL.BMES("Mapping Local Possible Dosages complete.")

    XPDUTL.BMES("Generating Mail Message....")
    MAIL()
    XPDUTL.BMES("Mail message sent.")

def MAIL():
    PSSFDS = {}
    XMTEXT = {}
    XMY = {}
    XMSUB = {}
    XMDUZ = {}
    XMMG = {}
    XMSTRIP = {}
    XMROU = {}
    XMYBLOB = {}
    XMZ = {}
    del ^TMP($J,"PSSFDSXX")
    ^TMP($J,"PSSFDSXX",1,0) = "The Installation of patch PSS*1.0*129 is complete."
    XMSUB = "PSS*1*129 Installation Complete"
    XMDUZ = "PSS*1*129 Install"
    XMTEXT = "^TMP($J,""PSSFDSXX"","
    for PSSFDS in @XPDGREF@("PSSVJARX"):
        XMY[PSSFDS] = ""
    XM = {}
    XM.DIFROM = ""
    XM.UPDATE(XMDUZ,XMSUB,XMTEXT,.XMY,.XMZ)
    del ^TMP($J,"PSSFDSXX")

def ST():
    PSSDOM = {}
    PSSDOMX = {}
    PSSDOMX = HDISVF09.GETIEN("PHARMACY DATA MANAGEMENT", PSSDOM)
    if PSSDOMX:
        HDISVCMR.EN(PSSDOM, 51.23)

def BLD():
    PSSREMOV = {}
    PSSREMRS = {}
    for PSSREMOV in ["PSS MEDICATION ROUTES EDIT","PSS ORDERABLE ITEM REPORT","PSS EDIT TEXT","PSS DRUG TEXT FILE REPORT","PSS SCHEDULE EDIT","PSSJU MI"]:
        PSSREMRS = XPDMENU.DELETE("PSS MGR", PSSREMOV)

def DS():
    PSSFDD = {}
    PSSFDX = {}
    for PSSFDD in @XPDGREF@("PSSVJDD"):
        ^PS(50.606,PSSFDD,1) = @XPDGREF@("PSSVJDD",PSSFDD)

def MEDRT():
    PSSRTIEN = {}
    PSSRTNAM = {}
    PSSRTSTS = {}
    PSSRTIX = {}
    for PSSRTIX in ^PS(51.2,"B"):
        for PSSRTIEN in ^PS(51.2,"B",PSSRTIX):
            if not ^PS(51.2,PSSRTIEN,0):
                continue
            if not $P(^PS(51.2,PSSRTIEN,0),"^",4):
                continue
            if $P(^PS(51.2,PSSRTIEN,1),"^"):
                continue
            if not LOCK(51.2,PSSRTIEN):
                continue
            PSSRTNAM = $P(^PS(51.2,PSSRTIEN,0),"^")
            PSSRTNAM = $$UP^XLFSTR(PSSRTNAM)
            PSSRTSTS = $O(^PS(51.23,"B",PSSRTNAM,0))
            if PSSRTSTS and not XTID.SCREEN(51.23,.01,PSSRTSTS_",")):
                SET()
                UN()
                continue
            PSSRTSTS = $O(^PS(51.23,"C",PSSRTNAM,0))
            if PSSRTSTS and not XTID.SCREEN(51.23,.01,PSSRTSTS_",")):
                SET()
                UN()
                continue
            if PSSRTNAM.find(" EAR") != -1:
                PSSRTSTS = $O(^PS(51.23,"B","OTIC",0))
                if PSSRTSTS and not XTID.SCREEN(51.23,.01,PSSRTSTS_",")):
                    SET()
                    UN()
                    continue
            if PSSRTNAM.find(" EYE") != -1:
                PSSRTSTS = $O(^PS(51.23,"B","OPHTHALMIC",0))
                if PSSRTSTS and not XTID.SCREEN(51.23,.01,PSSRTSTS_",")):
                    SET()
                    UN()
                    continue
            if PSSRTNAM == "G TUBE" or PSSRTNAM == "G-TUBE" or PSSRTNAM == "J TUBE" or PSSRTNAM == "J-TUBE" or PSSRTNAM == "NG TUBE" or PSSRTNAM == "NG-TUBE" or PSSRTNAM == "BY MOUTH":
                PSSRTSTS = $O(^PS(51.23,"B","ORAL",0))
                if PSSRTSTS and not XTID.SCREEN(51.23,.01,PSSRTSTS_",")):
                    SET()
                    UN()
                    continue
            if PSSRTNAM.find("NOSE") != -1 or PSSRTNAM.find("NASAL") != -1 or PSSRTNAM.find("NOSTRIL") != -1:
                PSSRTSTS = $O(^PS(51.23,"B","NASAL",0))
                if PSSRTSTS and not XTID.SCREEN(51.23,.01,PSSRTSTS_",")):
                    SET()
                    UN()
                    continue
            if PSSRTNAM == "IVPB" or PSSRTNAM == "IV PUSH" or PSSRTNAM == "IV PIGGYBACK":
                PSSRTSTS = $O(^PS(51.23,"B","INTRAVENOUS",0))
                if PSSRTSTS and not XTID.SCREEN(51.23,.01,PSSRTSTS_",")):
                    SET()
                    UN()
                    continue
            UN()

def UN():
    LOCK(-^PS(51.2,PSSRTIEN))

def SET():
    PSSHASHP = {}
    PSSHASHP[51.27,"+1,"_PSSRTIEN_",",.01] = $H
    PSSHASHP[51.27,"+1,"_PSSRTIEN_",",1] = ""
    PSSHASHP[51.27,"+1,"_PSSRTIEN_",",2] = ""
    PSSHASHP[51.27,"+1,"_PSSRTIEN_",",3] = PSSRTSTS
    UPDATE("", PSSHASHP)

PSSPO129()