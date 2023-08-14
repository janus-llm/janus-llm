# PSS102RP ;OIFO BAY PINES/VGF - TEMP RTN TO UPDATE PLACE OF VISIT IN FILE 1020.2;3/30/04
# ;;1.0;PHARMACY DATA MANAGEMENT;**102**;9/30/97
import os
import datetime

PSSIEN = ""
PSSDRG = ""
PSSDRUGT = ""
PSSSPCE = ""
PSSDUZ = ""
PSSLN = ""
PSSDRUG = ""
XMDUZ = ""
XMSUB = ""
XMTEXT = ""
XMY = ""

PSSDUZ = os.getenv("DUZ")
os.system("rm -rf /tmp/PSS102")
os.system("rm -rf /tmp/PSS102")

PSSIEN = ""
while PSSIEN != "":
    PSSIEN = getNextIEN(PSSIEN)
    PSSDRG = ""
    while PSSDRG != "":
        PSSDRG = getNextDRG(PSSIEN, PSSDRG)
        PSSDRUGT = getDrugText(PSSDRG)
        if not isSynonym(PSSIEN, PSSDRUGT):
            addXTMPEntry(PSSIEN, PSSDRUGT)

if noXTMPEntries():
    addXTMPNoDrugs()

addTMPEntry()

PSSLN = 11
PSSIEN = ""
while PSSIEN != "":
    PSSIEN = getNextXTMPIEN(PSSIEN)
    PSSDRUG = getDrugName(PSSIEN)
    PSSDRUGT = ""
    while PSSDRUGT != "":
        PSSDRUGT = getNextXTMPDrugText(PSSIEN, PSSDRUGT)
        addTMPEntry(PSSDRUG, PSSDRUGT)
        PSSLN = PSSLN + 1

sendReport()

os.system("rm -rf /tmp/PSS102")
os.system("rm -rf /tmp/PSS102")

def getNextIEN(PSSIEN):
    # Code to get the next IEN
    return ""

def getNextDRG(PSSIEN, PSSDRG):
    # Code to get the next DRG
    return ""

def getDrugText(PSSDRG):
    # Code to get the drug text
    return ""

def isSynonym(PSSIEN, PSSDRUGT):
    # Code to check if it is a synonym
    return False

def addXTMPEntry(PSSIEN, PSSDRUGT):
    # Code to add XTMP entry
    return ""

def noXTMPEntries():
    # Code to check if there are no XTMP entries
    return False

def addXTMPNoDrugs():
    # Code to add XTMP no drugs entry
    return ""

def addTMPEntry():
    # Code to add TMP entry
    return ""

def getNextXTMPIEN(PSSIEN):
    # Code to get the next XTMP IEN
    return ""

def getDrugName(PSSIEN):
    # Code to get the drug name
    return ""

def getNextXTMPDrugText(PSSIEN, PSSDRUGT):
    # Code to get the next XTMP drug text
    return ""

def sendReport():
    XMSUB = "PHARMACY DATA MANAGEMENT"
    XMTEXT = "^TMP("_$J_","_"""PSS102"""_","
    XMDUZ = "PATCH PSS*1.0*102"
    XMY(PSSDUZ) = ""
    SENDMSG(PSSDUZ, XMSUB, "^TMP("_$J_","_"""PSS102"""_")", PSSDUZ)
    os.system("rm -rf /tmp/PSS102")
    return ""

def SENDMSG(PSSDUZ, XMSUB, XMTEXT, PSSDUZ):
    # Code to send message
    return ""