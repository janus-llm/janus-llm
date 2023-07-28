# BIR/DMA - ENTER/EDIT INTERACTIONS
# 02/11/15 12:53
# 1.0;PHARMACY DATA MANAGEMENT;**17,20,43,190**;9/30/97;Build 1

# Reference to $$KSP^XUPARAM("INST") supported by DBIA #2541
# Reference to ^PS(56 supported by DBIA #2133
# Reference to ^XMD supported by DBIA #10070

def GO():
    print()
    PSNDF = 1
    PSN = None
    PSN1 = None
    PSN2 = None
    PSNN = {}
    PSNNN = None

    DIC = "50.416"
    DIC(0) = "AEMQZ"
    DIC("A") = "Choose first ingredient "
    DIC("S") = "I '$P(^(0),""^"",2)"
    Y = DIC()
    if Y < 0:
        OUT()
    else:
        PSN1 = +Y
        PSNN[$P(Y(0), "^")] = ""

    DIC("A") = "Choose second ingredient "
    DIC("S") = DIC("S") + ",+Y'=PSN1"
    Y = DIC()
    if Y < 0:
        OUT()
    else:
        PSN2 = +Y
        PSNN[$P(Y(0), "^")] = ""

    DA = $O(^PS(56,"AE",PSN1,PSN2,0))
    if DA:
        PSN = ^PS(56,DA,0)
        PSNL = $G(^PS(56,DA,"L"))
        if DA <= 15000 or (DA > 50000 and $P(PSN, "^", 4) == 1 and not PSNL):
            print()
            print("That interaction is nationally entered and may not be edited.")
        else:
            DIR(0) = "Y"
            DIR("A") = "That interaction already exists.  Do you wish to edit it"
            Y = DIR()
            if not Y:
                GO()
            else:
                DIR(0) = "56,3"
                Y = DIR()
                if not Y:
                    GO()
                else:
                    DIE = "^PS(56,"
                    DR = "3////"_Y+";6////1;"
                    if DA > 15000 and DA < 50001:
                        DR = DR + "7;"
                    DIE()
                    SEVMSG()
    else:
        PSNNN = $O(PSNN("")) + "/" + $O(PSNN($O(PSNN("")))
        DA = None
        DIR(0) = "56,3"
        Y = DIR()
        if Y:
            PSN = Y
            print(PSNNN, "Severity:", Y(0))
            DIR(0) = "Y"
            DIR("A") = "OK to add "
            Y = DIR()
            if not Y:
                PSNN = {}
                PSNNN = None
                GO()
            else:
                while not L + ^PS(56):
                    pass
                DINUM = $O(^PS(56,50000),-1)+1
                if DINUM <= 15000:
                    DINUM = 15001
                DIC("DR") = "1////"_PSN1_";2////"_PSN2_";3////"_PSN_";6////1"
                DIC = "^PS(56,"
                DIC(0) = "L"
                X = PSNNN
                FILE^DICN
                L - ^PS(56)
                ADDMSG()
                PSN = None
                PSN1 = None
                PSN2 = None
                PSNN = {}
                PSNNN = None
                GO()

def OUT():
    PSN = None
    PSN1 = None
    PSN2 = None
    PSNDF = None
    PSNL = None
    PSNN = {}
    PSNNN = None
    DA = None
    DIC = None
    DIR = None
    DIRUT = None
    DR = None
    X = None
    Y = None
    PSNIFN = None
    PSNSEV = None
    PSSFLTY = None
    PSSIIEN = None
    XMDUZ = None
    XMSUB = None
    XMTEXT = None
    XMY = None
    DIE = None
    DINUM = None
    DTOUT = None
    DUOUT = None
    ^TMP($J,"PSS") = None

def SEVMSG():
    if PSNL:
        pass
    PSNIFN = ^PS(56,DA,0)
    if $P(PSNIFN,U,4) != 2:
        HEADER()
        XMSUB = "Drug Interaction Severity Change from "_PSSFLTY_"."
        ^TMP($J,"PSS",1) = "The severity of a nationally entered drug interaction has been edited."
        ^TMP($J,"PSS",2) = ""
        ^TMP($J,"PSS",3) = ""_$P(PSNIFN,U)_" Drug Interaction severity"
        ^TMP($J,"PSS",4) = "changed from SIGNIFICANT to CRITICAL."
        XMTEXT = "^TMP($J,""PSS"","
        ^XMD()

def ADDMSG():
    HEADER()
    XMSUB = "Local Drug Interaction Added from "_PSSFLTY_"."
    ^TMP($J,"PSS",1) = "Local "_PSNNN_" Drug Interaction"
    ^TMP($J,"PSS",2) = "with a severity of "_$S($P(^PS(56,+Y,0),U,4)=2:"SIGNIFICANT",1:"CRITICAL")_" has been added."
    XMTEXT = "^TMP($J,""PSS"","
    ^XMD()

def HEADER():
    PSSIIEN = $$KSP^XUPARAM("INST")
    PSSFLTY = $$GET1^DIQ(4,PSSIIEN,.01)
    XMDUZ = DUZ
    XMY("G.NDF SUPPORT@ISCPNDF.ISC-BIRM.DOMAIN.EXT") = ""

GO()

OUT()