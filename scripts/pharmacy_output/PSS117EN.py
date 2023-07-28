# PSS117EN ;BIR/RTR-Environment check routine for patch PSS*1*117 ;11/20/08
# ;1.0;PHARMACY DATA MANAGEMENT;**117**;9/30/97;Build 101
if not XPDENV:
    pass

#USE PSSMRM,PSSMLM,PSSMGP
#Check to see if all Local Med Routes are mapped
import os
def EN():
    PSSMRMFM = None
    PSSMRMLP = None
    PSSMRMNM = None
    PSSMRMFD = None
    PSSMRMAR = None
    DIR = None
    X = None
    Y = None
    DTOUT = None
    DUOUT = None
    DIRUT = None
    DIROUT = None
    DIC = None
    DA = None
    DLAYGO = None
    PSSMRMCT = None
    PSSMRMXX = None
    PSSMRMIN = None
    PSSMRMZR = None
    PSSMRMN1 = None
    PSSMRMN3 = None
    PSSMRMOK = None
    PSSMRM22 = None
    PSSMRMBB = None
    PSSMRMT1 = None
    PSSMRMD1 = None
    PSSMRMD2 = None
    PSSMRMTC = None
    PSSMGPNM = None
    PSSMGPTP = None
    PSSMGPOR = None
    PSSMGPSL = None
    PSSMGPMY = None
    PSSMGPDS = None
    PSSMGPQT = None
    PSSMGPAR = None
    PSSMGPRS = None
    PSSMRMPF = None
    PSSMRMER = None

    #This Mail Group should have been added with PSS*1*136, so this code should be bypasses by the FIND1 check
    if os.system("$$FIND1^DIC(3.8,'','X','PSS ORDER CHECKS','B')"):
        KTM()
        return

    KTM()
    PSSMGPAR = ["A 'PSS ORDER CHECKS' Mail Group is now being created. Mail Group members will",
                 "receive various notifications that impact Enhanced Order Checks (drug-drug",
                 "interactions, duplicate therapy and dosing) introduced with PRE V. 0.5. Please",
                 "enter the Pharmacy ADPAC or a designee to be the Mail Group Organizer.",
                 " ",
                 "To continue this install, you must now enter a Mail Group organizer.",
                 " "]

    print(PSSMGPAR)
    DIC = 200
    DIC(0) = "QEAMZ"
    DIC("A") = "Enter Mail Group Organizer: "
    os.system("^DIC")
    if DTOUT or DUOUT or not +Y:
        XPDABORT = 2
        return
    PSSMGPOR = +Y
    PSSMGPMY[+Y] = ""
    PSSMGPNM = "PSS ORDER CHECKS"
    PSSMGPTP = 0
    PSSMGPSL = 0
    PSSMGPQT = 1
    PSSMGPDS = ["Members of this mail group will receive various notifications that impact",
                 "Enhanced Order Checks (drug-drug interactions, duplicate therapy and dosing",
                 "checks) introduced with PRE V. 0.5 utilizing a COTS database."]
    os.system("$$MG^XMBGRP(PSSMGPNM,PSSMGPTP,PSSMGPOR,PSSMGPSL,.PSSMGPMY,.PSSMGPDS,PSSMGPQT)")
    if not PSSMGPRS:
        print(" ")
        print("Unable to create PSS ORDER CHECKS Mail Group, aborting install.")
        XPDABORT = 2
        return
    print("PSS ORDER CHECKS Mail Group successfully created.")

    #AIT ;Add Interventions types

    print("Adding new Intervention Types.")
    if os.system("$$FIND1^DIC(9009032.3,'','X','MAX SINGLE DOSE','B')"):
        ADDMX()
        if os.system("$$FIND1^DIC(9009032.3,'','X','MAX SINGLE DOSE','B')"):
            AITX(1)
            XPDABORT = 2
            KTM()
            return
    if os.system("$$FIND1^DIC(9009032.3,'','X','DAILY DOSE RANGE','B')"):
        ADDMXA()
        if os.system("$$FIND1^DIC(9009032.3,'','X','DAILY DOSE RANGE','B')"):
            AITX(2)
            XPDABORT = 2
            KTM()
            return
    if os.system("$$FIND1^DIC(9009032.3,'','X','MAX SINGLE DOSE & DAILY DOSE RANGE','B')"):
        ADDMXB()
        if os.system("$$FIND1^DIC(9009032.3,'','X','MAX SINGLE DOSE & DAILY DOSE RANGE','B')"):
            AITX(3)
            XPDABORT = 2
            KTM()
            return
    KTM()
    print("New Intervention Types successfully added.")

    #DOS ;Check to see if all Local Possible Dosages are mapped
    #Local Possible Dosage check, using PSSMRMFD as flag
    print("Checking for any remaining Local Possible Dosages missing data...")

    PSSMRMFD = 0
    PSSMRMCT = 0
    PSSMRMXX = 0
    while True:
        PSSMRMXX += 1
        if PSSMRMXX == 2000:
            print("...Still checking Local Possible Dosages...")
        if not PSSMRMOK():
            continue
        PSSMRM22 = 0
        for PSSMRMBB in range(1, 100):
            PSSMRMT1 = PSSMRMXX[PSSMRMBB]
            if PSSMRMT1[0] != "" and (not PSSMRMT1[4] or PSSMRMT1[5] == ""):
                PSSMRM22 = 1
        if not PSSMRM22:
            break
        PSSMRMFD = 1

    if not PSSMRMFD:
        print("Population of data for eligible Local Possible Dosages has been completed!!")
        print(" ")
        KTM()
        return
    PSSMRMAR = [" ",
                 "There are still local possible dosages eligible for dosage checks that have",
                 "missing data in the Numeric Dose and Dose Unit fields. Any orders containing",
                 "such local possible dosages will not have dosage checks performed. Please",
                 "refer to the 'Local Possible Dosages Report' option for more details.",
                 " "]

    print(PSSMRMAR)
    KTM()
    #K DIR,X,Y,DTOUT,DUOUT,DIRUT,DIROUT
    #S DIR(0)="Y",DIR("B")="Y",DIR("A")="Do you want to continue to install this patch" D ^DIR
    #I Y'=1!($D(DUOUT))!($D(DTOUT)) S XPDABORT=2 Q
    #K DIR,X,Y,DTOUT,DUOUT,DIRUT,DIROUT

def PSSMRMOK():
    if (not PSSMRMN3) or (not PSSMRMN1):
        return 0
    if PSSMRMN1 and PSSMRMN3 and (os.system("$$OVRIDE^PSNAPIS(PSSMRMN1,PSSMRMN3)")):
        return 1
    PSSMRMD1 = os.system("$$DFSU^PSNAPIS(PSSMRMN1,PSSMRMN3)")
    PSSMRMD2 = PSSMRMD1[0]
    if PSSMRMD2 <= 0:
        if PSSMRMZR[2]:
            PSSMRMD2 = os.system("$$PSS(50.7,+$P(^PSDRUG(PSSMRMIN,2),U),0)")
    if PSSMRMVV or (not PSSMRMD2) or (os.system("$$PSS(50.606,+$G(PSSMRMD2),1)")):
        return 1
    if not os.system("$$PSS(50.606,+$G(PSSMRMD2),1)") and PSSMRMVV:
        return 0
    if os.system("$$PSS(50.606,+$G(PSSMRMD2),1)") and (not PSSMRMVV):
        return 0
    return 1
    
def AITX(PSSMRMIT):
    print(" ")
    if PSSMRMIT == 1:
        print("Cannot create 'MAX SINGLE DOSE' intervention type, aborting install.")
    elif PSSMRMIT == 2:
        print("Cannot create 'DAILY DOSE RANGE' intervention type, aborting install.")
    else:
        print("Cannot create 'MAX SINGLE DOSE & DAILY DOSE RANGE' intervention type,")
        print("aborting install.")

def ADDMX():
    os.system("$$FIND1^DIC(9009032.3,'','X','MAX SINGLE DOSE','B')")
    PSSMRMPD = [9009032.3]
    PSSMRMPD[0] = [".01":"MAX SINGLE DOSE"]
    os.system("$$UPDATE^DIE('','PSSMRMPD(1)','','PSSMRMER(1)')")

def ADDMXA():
    os.system("$$FIND1^DIC(9009032.3,'','X','DAILY DOSE RANGE','B')")
    PSSMRMPD = [9009032.3]
    PSSMRMPD[0] = [".01":"DAILY DOSE RANGE"]
    os.system("$$UPDATE^DIE('','PSSMRMPD(1)','','PSSMRMER(1)')")

def ADDMXB():
    os.system("$$FIND1^DIC(9009032.3,'','X','MAX SINGLE DOSE & DAILY DOSE RANGE','B')")
    PSSMRMPD = [9009032.3]
    PSSMRMPD[0] = [".01":"MAX SINGLE DOSE & DAILY DOSE RANGE"]
    os.system("$$UPDATE^DIE('','PSSMRMPD(1)','','PSSMRMER(1)')")

def MNU():
    PSSMNUXX = os.system("$$LKOPT^XPDMENU('PSS DRG INTER MANAGEMENT')")
    if not PSSMNUXX:
        return
    PSSMNUR = os.system("$$DELETE^XPDMENU('PSS MGR','PSS DRG INTER MANAGEMENT')")
    if PSSMNUR:
        print("Unable to remove PSS DRG INTER MANAGEMENT option from PSS MGR Menu option.")
        PRMP()
        @XPDGREF["PSSMLMSG"][PSSMRMTC] = "Unable to remove PSS DRG INTER MANAGEMENT option from PSS MGR Menu option."
        PSSMRMTC += 1
        @XPDGREF["PSSMLMSG"][PSSMRMTC] = "Please log a Remedy Ticket and refer to this message."
        INC()

    PSSMNUXX = os.system("$$LKOPT^XPDMENU('PSS ENHANCED ORDER CHECKS')")
    if PSSMNUXX:
        return
    PSSMNUR = os.system("$$DELETE^XPDMENU('PSS MGR','PSS ENHANCED ORDER CHECKS')")
    if PSSMNUR:
        print("Unable to remove PSS ENHANCED ORDER CHECKS option from PSS MGR Menu option.")
        PRMP()
        @XPDGREF["PSSMLMSG"][PSSMRMTC] = "Unable to remove PSS ENHANCED ORDER CHECKS option from PSS MGR Menu option."
        PSSMRMTC += 1
        @XPDGREF["PSSMLMSG"][PSSMRMTC] = "Please log a Remedy Ticket and refer to this message."
        INC()
    return