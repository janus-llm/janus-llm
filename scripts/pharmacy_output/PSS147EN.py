# BIR/RTR-Environment check routine for patch PSS*1*147 ;07/17/09
# 1.0;PHARMACY DATA MANAGEMENT;**147**;9/30/97;Build 16

if not XPDENV:
    pass

def EN():
    X = None
    Y = None
    DTOUT = None
    DUOUT = None
    DIRUT = None
    DIROUT = None
    DIC = None
    DA = None
    DLAYGO = None
    PSSMGPAR = None
    PSSMGPOR = None
    PSSMGPMY = None
    PSSMGPNM = None
    PSSMGPDS = None
    PSSMGPRS = None
    PSSMGPQT = None
    PSSMGPTP = None
    PSSMGPSL = None

    XPDGREF["PSS147IN"]["INSTALL"] = 0
    if PATCH_XPDUTL("PSS*1.0*147"):
        XPDGREF["PSS147IN"]["INSTALL"] = 1

    if FIND1_DIC(3.8, "", "X", "PSS ORDER CHECKS", "B"):
        KTM()
        REC()
    
    KTM()
    PSSMGPAR = [
        "A 'PSS ORDER CHECKS' Mail Group is now being created. Mail Group members will",
        "receive various notifications that impact Enhanced Order Checks (drug-drug",
        "interactions, duplicate therapy and dosing) introduced with PRE V. 0.5. Please",
        "enter the Pharmacy ADPAC or a designee to be the Mail Group Organizer.",
        " ",
        "To continue this install, you must now enter a Mail Group organizer.",
        " "
    ]
    MES_XPDUTL(PSSMGPAR)
    DIC = 200
    DIC[0] = "QEAMZ"
    DIC["A"] = "Enter Mail Group Organizer: "
    Y = DIC()
    if DTOUT or DUOUT or Y <= 0:
        XPDABORT = 2
        return

    PSSMGPOR = +Y
    PSSMGPMY[+Y] = ""
    PSSMGPNM = "PSS ORDER CHECKS"
    PSSMGPTP = 0
    PSSMGPSL = 0
    PSSMGPQT = 1
    PSSMGPDS = [
        "Members of this mail group will receive various notifications that impact",
        "Enhanced Order Checks (drug-drug interactions, duplicate therapy and dosing",
        "checks) introduced with PRE V. 0.5 utilizing a COTS database."
    ]
    PSSMGPRS = MG_XMBGRP(PSSMGPNM, PSSMGPTP, PSSMGPOR, PSSMGPSL, PSSMGPMY, PSSMGPDS, PSSMGPQT)
    if not PSSMGPRS:
        BMES_XPDUTL(" ")
        BMES_XPDUTL("Unable to create PSS ORDER CHECKS Mail Group, aborting install.")
        XPDABORT = 2
        return

    BMES_XPDUTL("PSS ORDER CHECKS Mail Group successfully created.")

def REC():
    XPDGREF["PSS147DZ"][DUZ] = ""
    XPDGREF["PSS147DZ"]["G.PSS ORDER CHECKS"] = ""

def KTM():
    del TMP["DIERR"]

EN()