# PSS1P201 ;BP/CMF - PATCH PSS*1*201 Pre/Post-Init Rtn ;09/13/2016
# ;1.0;PHARMACY DATA MANAGEMENT;**201**;9/30/97;Build 25

def ENV():
    XPDABORT = ""
    # PRODCHK(.XPDABORT) I XPDABORT=2 Q  restriction removed after sprint 3
    PROGCHK(XPDABORT)
    if XPDABORT == "":
        del XPDABORT

def PRODCHK(XPDABORT):
    if PROD():
        print("******")
        print("PSS*1*201 is not yet ready for production accounts.")
        print("Installation aborted.")
        print("******")
        XPDABORT = 2

def PROGCHK(XPDABORT):
    if not DUZ or (DUZ(0) != "@") or not DT or U != "^":
        print("******")
        print("Your programming variables are not set up properly.")
        print("Installation aborted.")
        print("******")
        XPDABORT = 2

def POST():
    APSP()  # add entries to Intervention Type file
    DOSEUNIT()  # edit entry 40

def APSP():
    FDA = {}
    FDERROR = ""
    LIST = {}
    LISTERR = ""
    IEN = ""
    print("Adding entries to APSP Intervention Type file")
    FIND(9009032.3, "", "", "X", "MAX DAILY DOSE", "", "", "", "", "LIST", "LISTERR")
    if LIST["DILIST", 0] == 0:
        FDA[1, 9009032.3, "+1,", .01] = "MAX DAILY DOSE"
        UPDATE("E", "FDA(1)", "", "FDERROR")
        if not FDERROR:
            print("MAX DAILY DOSE added.")
    if LIST["DILIST", 0] > 1:
        I = 1
        while I:
            I = LIST["DILIST", 2, I]
            IEN = LIST["DILIST", 2, I]
            KILLAPSP(IEN)
    FDA = {}
    FDERROR = ""
    LIST = {}
    LISTERR = ""
    I = ""
    IEN = ""
    FIND(9009032.3, "", "", "X", "MAX SINGLE DOSE & MAX DAILY DOSE", "", "", "", "", "LIST", "LISTERR")
    if LIST["DILIST", 0] == 0:
        FDA[1, 9009032.3, "+1,", .01] = "MAX SINGLE DOSE & MAX DAILY DOSE"
        UPDATE("E", "FDA(1)", "", "FDERROR")
        if not FDERROR:
            print("MAX SINGLE DOSE & MAX DAILY DOSE added.")
    if LIST["DILIST", 0] > 1:
        I = 1
        while I:
            I = LIST["DILIST", 2, I]
            IEN = LIST["DILIST", 2, I]
            KILLAPSP(IEN)
    FDA = {}
    FDERROR = ""
    LIST = {}
    LISTERR = ""
    return

def KILLAPSP(IEN):
    DIK = "^APSPQA(32.3,"
    DA = IEN
    ^DIK

def DOSEUNIT():
    XUMF = ""
    DA = ""
    DIE = ""
    DR = ""
    if FIND1(51.24, "", "MX", "SUPPOSITORY(IES)") > 0:
        return
    DA = FIND1(51.24, "", "MX", "SUPPOSITOR(IES)")
    if DA < 1:
        return
    XUMF = 1
    DR = ".01////SUPPOSITORY(IES)"
    DIE = 51.24
    ^DIE
    if FIND1(51.24, "", "MX", "SUPPOSITORY(IES)") > 0:
        print("Dose Unit Entry Modified")

ENV()
POST()