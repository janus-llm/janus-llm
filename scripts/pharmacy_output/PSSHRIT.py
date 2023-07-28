#WOIFO/SG,PO - Transmits a "ping" to determine if FDB server is down and record the down time ; 01 Mar 2016  3:34 PM
#1.0;PHARMACY DATA MANAGEMENT;**136,168,164,173,180,184,178**;9/30/97;Build 14

#External reference to IN^PSSHRQ2 supported by DBIA 5369
#External reference to File 18.12 supported by DBIA 5891

def PINGCHK():
    # do ping test, if not passed record it and send a message.
    # Called from PSS INTERFACE SCHEDULER option
    STATUS = PINGTST()
    STATUS = PINGFILE(STATUS)
    if STATUS == -1:
        SMSGDWN()   # if failed for the first time (a new entry created) send a message that interface is down.

def PINGTST():
    # test the ping by sending a ping request.
    #return 0 - ping successful,  -1^reason  ping failed
    BASE = "PINGTST^" + __name__
    TMP = {}
    TMP[BASE] = {}
    TMP[BASE]["IN"] = {}
    TMP[BASE]["IN"]["PING"] = ""
    IN_PSSHRQ2(BASE)
    STATUS = TMP[BASE]["OUT"][0]
    del TMP[BASE]
    return STATUS

def PINGFILE(STATUS):
    #  file the ping results
    # Input
    #   Status - Ping results
    # Return 
    #     -1 - if creates an entry - means the first it noticed PEPS is unavailable
    #      0 - if does not create/update a record, 
    #      1 - if updates the last entry
    LIEN = max(PS(59.74, ":"))           # get last entry
    LASTAVL = PS(59.74, LIEN, 0)[1]      # get last available date/time
    if STATUS == 0 and not LIEN:
        return 0                          # do nothing
    elif STATUS == 0 and LIEN and LASTAVL:
        return 0                          # do nothing
    elif STATUS == 0 and LIEN and not LASTAVL:
        UPDATENT(LIEN)
        return 1                          # update file
    elif STATUS == -1 and LIEN and LASTAVL:
        NEWENT()
        return -1                         # create new entry
    elif STATUS == -1 and not LIEN:
        NEWENT()
        return -1                         # create new entry
    else:
        return 0

def NEWENT():
    # create a new entry in FDB INTERFACE DATA (#59.74) file.
    X = NOW()
    DIC = "PS(59.74,"
    DIC(0) = "Z"
    FILE^DICN(DIC, X)
    del X, Y

def UPDATENT(LAST):
    # update the last entry in FDB INTERFACE DATA (#59.74) file.
    #edit flag once it is created.
    DA = LAST
    NEWVAL = NOW()   #NOW()
    DWNTIME = PS(59.74, DA, 0)
    if not DWNTIME:
        return
    DIFF = FMDIFF(NEWVAL, DWNTIME, 2)
    DIFF = DIFF // 60  #IN MINUTES
    DIE = "PS(59.74,"
    DR = "1///^S X=NEWVAL;2///^S X=DIFF"
    DIE^DR
    SMSGRST()  # send a message that interface connection is restored

def SMSGDWN():
    # send a bulletin that Interface connection is down.
    XMDUZ = "PSS INTERFACE SCHEDULER"
    XMB = "PSS FDB INTERFACE"
    XMTEXT = "PSFDB"
    if DS^PSSDSAPI and DS^PSSDSAPI() == True:
        PSFDB = ["Connection to Vendor Database is down!  No Drug-Drug Interaction, Duplicate",
                 "Therapy or Dosing Order Checks will be performed until the connection is",
                 "reestablished!!!"]
    else:
        PSFDB = ["Connection to Vendor Database is down!  No Drug-Drug Interaction or Duplicate",
                 "Therapy Order Checks will be performed until the connection is reestablished!!!"]
    XMY = ["G.PSS ORDER CHECKS"]
    XMB^XMTEXT^XMY

def SMSGRST():
    # send a bulletin that Interface connection is restored
    XMDUZ = "PSS INTERFACE SCHEDULER"
    XMB = "PSS FDB INTERFACE RESTORED"
    XMTEXT = "PSFDB"
    if DS^PSSDSAPI and DS^PSSDSAPI() == True:
        PSFDB = ["Connection to Vendor Database has been restored! Drug-Drug Interactions,",
                 "Duplicate Therapy and Dosing Order Checks can now be performed."]
    else:
        PSFDB = ["Connection to Vendor Database has been restored! Drug-Drug Interactions or",
                 "Duplicate Therapy Order Checks can now be performed."]
    XMY = ["G.PSS ORDER CHECKS"]
    XMB^XMTEXT^XMY

def TASKIT(FREQ=15, START=NOW()):
    # create/update scheduling option start time and frequency
    # Input:
    #   FREQ  - Optional - rescheduling frequency in minutes (default 15 minutes)
    #  START  - Optional - start time (default is current time + 4 minutes)
    # Note: if START is less than 4 minutes in future,  it will be defaulted to 
    #       current time + 4 minutes.
    PSERROR = []
    FREQ = FREQ * 60 + "S"
    if FMDIFF(START, NOW(), 2) < 240:
        START = FMADD(NOW(), 0, 0, 4)
    RESCH^XUTMOPT("PSS INTERFACE SCHEDULER", START, "", FREQ, "L", PSERROR)

def SCHDOPT():
    # edit option scheduling
    # Called from "PSS SCHEDULE PEPS INTERFACE CK" option to create and/or edit the scheduling
    # parameters for "PSS INTERFACE SCHEDULER" option in OPTION SCHEDULING file. 
    # The "PSS SCHEDULE PEPS INTERFACE CK" option is installed by PAS*1.0*117 package.
    PSSROOT = {}
    OPTSTAT^XUTMOPT("PSS INTERFACE SCHEDULER", PSSROOT)
    if not PSSROOT[1]:
        TASKIT(15)
    print("\n", "The PSS INTERFACE SCHEDULER task is scheduled to run next on ")
    PSSTIME = PSSROOT[1][2]
    print("\n", PSSTIME if PSSTIME else "*** NOT SCHEDULED ***", "\n")
    print("\n", "The recommended ""Rescheduling Frequency"" is 15 minutes (900 seconds).")
    print("\n", "It is currently set to ", PSSROOT[1][3] if PSSROOT[1] else "*** NOT SET ***", ".")
    print("\n", "WARNING: Do not decrease the ""Rescheduling Frequency"" below 5 minutes.")
    print("\n", "         System issues could occur after a downtime due to")
    print("\n", "         multiple jobs being tasked.", "\n")
    if input("Continue to the TaskMan Schedule/Unschedule Option (Y/N)? ") == "Y":
        EDIT^XUTMOPT("PSS INTERFACE SCHEDULER")

def SLASTRUN(LASTRUN):
    # set last run time
    SUB = "PSSRUN"
    PURGE = FMADD(NOW(), 30)
    DESC = "This stores the latest data on FDB interface"
    ^XTMP(SUB, 0) = PURGE + "^" + NOW() + "^" + DESC
    ^XTMP(SUB, "LASTRUN") = LASTRUN

def GLASTRUN():
    # get last run time
    return ^XTMP("PSSRUN", "LASTRUN")

def RUNTEST():
    # run interaction test to PEPS server
    # called from PSS CHECK PEPS SERVICES SETUP option
    KILL^XUSCLEAN
    STATUS = CONCHK()
    PRSRTN()
    if STATUS == 0 or X == "^":
        return
    STATUS = INTERACT()
    PRSRTN()
    if X == "^":
        return
    STATUS = DUPTHRPY()
    PRSRTN()
    if X == "^":
        return
    STATUS = DOSECHK()
    PRSRTN()
    if X == "^":
        return
    STATUS = CUSTOM()
    PRSRTN()
    if X == "^":
        return

def QTESTS():
    # queued interaction tests to PEPS server
    N = NOW()
    PSSTIME = FMTE(N, "1P")
    print("\n", "-"*15, "Check PEPS Services Setup", "-"*15, PSSTIME, "\n")
    for i in range(79):
        print("-", end="")
    print("\n\n")
    STATUS = CONCHK()
    STATUS = INTERACT()
    STATUS = DUPTHRPY()
    STATUS = DOSECHK()
    STATUS = CUSTOM()

def CONCHK():
    # check connection
    # Return 1 if OK, 0 if not OK.
    BASE = "PSPRE"
    PSSCKWER = {}
    PSSCKW1 = FIND1^DIC(18.12, "", "X", "PEPS", "B", , "PSSCKWER")
    if PSSCKW1:
        PSSCKW2 = GET1^DIQ(18.12, PSSCKW1_",", .04, "I", , "PSSCKWER")
    PSSCKW2 = PSSCKW2 if PSSCKW2 else "Unknown Database"
    del PSSCKWER
    TMP = {}
    TMP[BASE] = {}
    TMP[BASE]["IN"] = {}
    TMP[BASE]["IN"]["PING"] = ""
    IN_PSSHRQ2(BASE)
    STATUS = TMP[BASE]["OUT"][0]
    if STATUS == 0:
        print("\n", "Database Version:", TMP[BASE]["OUT"]["difBuildVersion"])
        print("\n", "Build Version:", TMP[BASE]["OUT"]["difDbVersion"])
        Y = TMP[BASE]["OUT"]["difIssueDate"]
        Y = Y[4:6] + "/" + Y[6:8] + "/" + Y[0:4] if len(Y) == 8 and Y.isdigit() else ""
        print("\n", "Issue Date:", Y, "\n")
        print("\n", "Custom Database Version:", TMP[BASE]["OUT"]["customBuildVersion"])
        print("\n", "Custom Build Version:", TMP[BASE]["OUT"]["customDbVersion"])
        Y = TMP[BASE]["OUT"]["customIssueDate"]
        Y = Y[4:6] + "/" + Y[6:8] + "/" + Y[0:4] if len(Y) == 8 and Y.isdigit() else ""
        print("\n", "Custom Issue Date:", Y, "\n")
        Y = NOW()
        print("\n", "Connected to", PSSCKW2, "successfully @", Y[0:18])
    else:
        print("\n", "Connection could not be made to", "!"*PSSCKW3, PSSCKW2 + ".")
        Y = GLASTRUN()
        if Y:
            print("\n", "Last reached @" + Y[0:18])
    del TMP[BASE]
    return 1 if STATUS == 0 else 0

def INTERACT():
    # check drug-drug interaction.
    # Return 1 if OK, 0 if not OK.
    PSORDER = "I;1464P;PROSPECTIVE;2"
    PSDRUG1 = "WARFARIN NA (GOLDEN STATE) 5MG TAB"
    PSDRUG2 = "CIPROFLOXACIN HCL 250MG TAB"
    BASE = "PSPRE"
    TMP = {}
    TMP[BASE] = {}
    TMP[BASE]["IN"] = {}
    TMP[BASE]["IN"]["DRUGDRUG"] = ""
    TMP[BASE]["IN"]["PROSPECTIVE"] = {}
    TMP[BASE]["IN"]["PROSPECTIVE"]["I;1464P;PROSPECTIVE;2"] = "006562^4029336^^WARFARIN NA (GOLDEN STATE) 5MG TAB"
    TMP[BASE]["IN"]["PROSPECTIVE"]["I;91464P;PROSPECTIVE;2"] = "009509^4008322^^CIPROFLOXACIN HCL 250MG TAB"
    IN_PSSHRQ2(BASE)
    INTRO = "Performing Drug-Drug Interaction Order Check for " + PSDRUG2 + " and " + PSDRUG1
    INFO = TMP[BASE]["OUT"]["DRUGDRUG"]["C"][PSDRUG1][PSORDER][1]["PMON"][9][0]
    INTRO = INTRO + "...OK" if INFO else INTRO + "...Not OK"
    if not INFO:
        print(INTRO)
        print("\n", "Drug-Drug Interaction Order Check could not be performed.")
    else:
        print(INTRO)
        print("\n")
        PSSPEC = {"CLINICAL EFFECTS:  "}
        INFO = REPLACE(INFO, PSSPEC)
        INFO = "Critical Drug Interaction: " + INFO
        print(INFO)
    del TMP[BASE]
    return 1 if INFO else 0

def DUPTHRPY():
    # check duplicate therapy
    # Return 1 if OK, 0 if not OK.
    PSORDER = "O;403931;PROFILE;3"
    PSDRUG1 = "CIMETIDINE 300MG TAB"
    PSDRUG2 = "RANITIDINE 150MG TAB"
    BASE = "PSPRE"
    TMP = {}
    TMP[BASE] = {}
    TMP[BASE]["IN"] = {}
    TMP[BASE]["IN"]["THERAPY"] = ""
    TMP[BASE]["IN"]["PROFILE"] = {}
    TMP[BASE]["IN"]["PROFILE"]["O;403931;PROFILE;3"] = "11666^4006826^^CIMETIDINE 300MG TAB^O"
    TMP[BASE]["IN"]["PROSPECTIVE"] = {}
    TMP[BASE]["IN"]["PROSPECTIVE"]["Z;1;PROSPECTIVE;1"] = "11673^4007038^^RANITIDINE 150MG TAB"
    IN_PSSHRQ2(BASE)
    CLAS1 = TMP[BASE]["OUT"]["THERAPY"][1][1]["CLASS"]
    CLAS2 = TMP[BASE]["OUT"]["THERAPY"][1][2]["CLASS"]
    INTRO = "Performing Duplicate Therapy Order Check for " + PSDRUG1 + " and " + PSDRUG2
    INTRO = INTRO + "...OK" if CLAS1 else INTRO + "...Not OK"
    if not CLAS1:
        print(INTRO)
        print("\n", "Duplicate Therapy Order Check could not be performed.")
    else:
        LINE1 = "Therapeutic Duplication with " + PSDRUG1 + " and " + PSDRUG2
        LINE2 = "Duplicate Therapy Class(es): " + CLAS1 + "," + CLAS2
        print(INTRO)
        print("\n", LINE1)
        print("\n", LINE2)
    del TMP[BASE]
    return 1 if CLAS1 else 0

def DOSECHK():
    # check dosing
    # Return 1 if OK, 0 if not OK.
    TOTAL, SINGLE, INTRO, ORDER, PSDRUG1, PSDRUG2, BASE = ""
    PSDRUG1 = "ACETAMINOPHEN 500MG TAB"
    BASE = "PSPRE"
    TMP = {}
    TMP[BASE] = {}
    TMP[BASE]["IN"] = {}
    TMP[BASE]["IN"]["DOSE"] = ""
    TMP[BASE]["IN"]["DOSE"]["AGE"] = 5000
    TMP[BASE]["IN"]["DOSE"]["WT"] = 83.01
    TMP[BASE]["IN"]["DOSE"]["BSA"] = 1.532
    TMP[BASE]["IN"]["DOSE"]["O;1464P;PROSPECTIVE;2"] = "4490^4007154^^ACETAMINOPHEN 500MG TAB^3000^MILLIGRAMS^DAY^Q4H^10^DAY^ORAL^MAINTENANCE^1"
    TMP[BASE]["IN"]["PROSPECTIVE"] = {}
    TMP[BASE]["IN"]["PROSPECTIVE"]["O;1464P;PROSPECTIVE;2"] = "4490^4007154^^ACETAMINOPHEN 500MG TAB^O"
    IN_PSSHRQ2(BASE)
    TOTAL = TMP[BASE]["OUT"]["DOSE"][ORDER][PSDRUG1]["DAILYMAX"]["MESSAGE"][0]
    SINGLE = TMP[BASE]["OUT"]["DOSE"][ORDER][PSDRUG1]["SINGLE"]["MESSAGE"][0]
    INTRO = "Performing Dosing Order Check for " + PSDRUG1 + " - 3000MG Q4H" + ("...OK" if TOTAL else "...Not OK")
    if not TOTAL:
        print(INTRO)
        print("\n", "Dosing Order Check could not be performed.")
    else:
        print(INTRO)
        print("\n", SINGLE)
        print("\n", TOTAL)
    del TMP[BASE]
    return 1 if TOTAL else 0

def CUSTOM():
    # check custom drug-drug interaction
    # Return 1 if OK, 0 if not OK.
    INFO, INTRO, ORDER, DRUG1, DRUG2, BASE, STATUS, PSSPEC = ""
    BASE = "PSPRE"
    ORDER = "Z;1;PROSPECTIVE;1"
    DRUG1 = "CLARITHROMYCIN 250MG TAB"
    DRUG2 = "DIAZEPAM 5MG TAB"
    TMP = {}
    TMP[BASE] = {}
    TMP[BASE]["IN"] = {}
    TMP[BASE]["IN"]["DRUGDRUG"] = ""
    TMP[BASE]["IN"]["PROSPECTIVE"] = {}
    TMP[BASE]["IN"]["PROSPECTIVE"]["Z;1;PROSPECTIVE;1"] = "16373^4010075F^^CLARITHROMYCIN 250MG TAB"
    TMP[BASE]["IN"]["PROFILE"] = {}
    TMP[BASE]["IN"]["PROFILE"]["I;10U;PROFILE;10"] = "3768^40002216^^DIAZEPAM 5MG TAB"
    IN_PSSHRQ2(BASE)
    STATUS = TMP[BASE]["OUT"][0]
    INTRO = "Performing Custom Drug-Drug Interaction Order Check for " + DRUG1 + " and " + DRUG2
    SCUST()
    INTRO = INTRO + "...OK" if INFO else INTRO + "...Not OK"
    if not INFO:
        print(INTRO)
        if STATUS != 0:
            print("\n", "Custom Drug-Drug Interaction Order Check could not be performed.")
    else:
        print(INTRO)
        PSSPEC = {"CLINICAL EFFECTS:  "}
        INFO = REPLACE(INFO, PSSPEC)
        INFO = "Significant Drug Interaction: " + INFO
        print(INFO)
    del TMP[BASE]
    return 1 if STATUS == 0 or not INFO else 0

def SCUST():
    #Set Custom info
    INFO = TMP[BASE]["OUT"]["DRUGDRUG"]["S"][DRUG1][ORDER][1]["PMON"][9][0] if DRUG1 in TMP[BASE]["OUT"]["DRUGDRUG"]["S"] and ORDER in TMP[BASE]["OUT"]["DRUGDRUG"]["S"][DRUG1] else ""
    if not INFO:
        INFO = TMP[BASE]["OUT"]["DRUGDRUG"]["S"][DRUG2]["I;10U;PROFILE;10"][1]["PMON"][9][0] if DRUG2 in TMP[BASE]["OUT"]["DRUGDRUG"]["S"] and "I;10U;PROFILE;10" in TMP[BASE]["OUT"]["DRUGDRUG"]["S"][DRUG2] else ""
    return INFO if INFO else ""

def INTACT():
    # check vendor data base link
    # Called from CHECK VENDOR DATABASE LINK  option
    BASE = "PSPRE"
    PSSCKWER = {}
    PSSCKW1 = FIND1^DIC(18.12,"","X","PEPS","B",,"PSSCKWER")
    if PSSCKW1:
        PSSCKW2 = GET1^DIQ(18.12,PSSCKW1_",",.04,"I",,"PSSCKWER")
    PSSCKW2 = PSSCKW2 if PSSCKW2 else "Unknown Database"
    del PSSCKWER
    TMP = {}
    TMP[BASE] = {}
    TMP[BASE]["IN"] = {}
    TMP[BASE]["IN"]["PING"] = ""
    IN_PSSHRQ2(BASE)
    STATUS = TMP[BASE]["OUT"][0]
    if STATUS == 0:
        print("\n", "Database Version:", TMP[BASE]["OUT"]["difBuildVersion"])
        print("\n", "Build Version:", TMP[BASE]["OUT"]["difDbVersion"])
        Y = TMP[BASE]["OUT"]["difIssueDate"]
        Y = Y[4:6] + "/" + Y[6:8] + "/" + Y[0:4] if len(Y) == 8 and Y.isdigit() else ""
        print("\n", "Issue Date:", Y, "\n")
        print("\n", "Custom Database Version:", TMP[BASE]["OUT"]["customBuildVersion"])
        print("\n", "Custom Build Version:", TMP[BASE]["OUT"]["customDbVersion"])
        Y = TMP[BASE]["OUT"]["customIssueDate"]
        Y = Y[4:6] + "/" + Y[6:8] + "/" + Y[0:4] if len(Y) == 8 and Y.isdigit() else ""
        print("\n", "Custom Issue Date:", Y, "\n")
        Y = NOW()
        print("\n", "Connected to", PSSCKW2, "successfully @", Y[0:18])
    else:
        print("\n", "Connection could not be made to", "!"*PSSCKW3, PSSCKW2 + ".")
        Y = GLASTRUN()
        if Y:
            print("\n", "Last reached @" + Y[0:18])
    del TMP[BASE]
    return

def VENDRPT():
    #**Prints out the VENDOR INTERFACE DATA FILE (#59.74) sorted by most recent downtime first**
    #The report retrieves the output using the Fileman EN1^DIP data retrieval call
    print("\n", "-"*15, "Check PEPS Services Setup", "-"*15, "\n")
    print("\n", "This report will print out all information related to when and for how long the")
    print("\n", "vendor interface is unavailable (sorted by most recent down time first).")
    print("\n", "This information comes from the VENDOR INTERFACE DATA FILE.")
    print("\n", "You may queue the report to print if you wish. You may also \"^\" to halt the")
    print("\n", "report at any time.", "\n")
    DIC = "^PS(59.74,"
    BY = "-.01"
    L = 0
    DIPCRIT = 1
    FR = "?,"
    TO = "?,"
    DHD = "VENDOR INTERFACE DATA LIST"
    DIOBEG = "W @IOF"
    FLDS = ".01;\"DATE/TIME UNAVAILABLE\",1;\"DATE/TIME AVAILABLE\"\"\";C26\",2;\"TOTAL DOWNTIME\""
    EN1^DIP()

def HRSMIN(MIN):
    # Called from output transform of VENDOR INTERFACE DATA FILE (#59.54) field TOTAL TIME NOT AVAILABLE (field# 2)
    #INPUTS: MIN-TIME IN MINUTES
    #RETURNS HRS AND MINUTES
    HRS, MINHR, HRSMIN = "", 60, ""
    HRS = MIN // MINHR
    MIN = MIN % MINHR
    HRSMIN = str(HRS) + " HR" + ("S" if HRS > 1 else "") if HRS else ""
    HRSMIN = HRSMIN + (", " if HRSMIN else "") + str(MIN) + " MINUTE" + ("S" if MIN > 1 else "") if MIN else HRSMIN
    return HRSMIN

def OUTPUT(INFO, DIWL):
    TMP = {}
    DIWR, DIWF, DIW = 60, "W", {}
    TMP[DIWL] = INFO
    DIWF(DIWL, DIWR, DIWF)
    DIWW()
    del TMP[DIWL]
    return

def SCUST():
    #Set Custom info
    if DRUG1 in TMP[BASE]["OUT"]["DRUGDRUG"]["S"] and ORDER in TMP[BASE]["OUT"]["DRUGDRUG"]["S"][DRUG1]:
        INFO = TMP[BASE]["OUT"]["DRUGDRUG"]["S"][DRUG1][ORDER][1]["PMON"][9][0]
    elif DRUG2 in TMP[BASE]["OUT"]["DRUGDRUG"]["S"] and "I;10U;PROFILE;10" in TMP[BASE]["OUT"]["DRUGDRUG"]["S"][DRUG2]:
        INFO = TMP[BASE]["OUT"]["DRUGDRUG"]["S"][DRUG2]["I;10U;PROFILE;10"][1]["PMON"][9][0]
    else:
        INFO = ""
    return INFO if INFO else ""

def INTACT():
    # check vendor data base link
    # Called from CHECK VENDOR DATABASE LINK  option
    BASE = "PSPRE"
    PSSCKWER = {}
    PSSCKW1 = FIND1^DIC(18.12,"","X","PEPS","B",,"PSSCKWER")
    if PSSCKW1:
        PSSCKW2 = GET1^DIQ(18.12,PSSCKW1_",",.04,"I",,"PSSCKWER")
    PSSCKW2 = PSSCKW2 if PSSCKW2 else "Unknown Database"
    del PSSCKWER
    TMP = {}
    TMP[BASE] = {}
    TMP[BASE]["IN"] = {}
    TMP[BASE]["IN"]["PING"] = ""
    IN_PSSHRQ2(BASE)
    STATUS = TMP[BASE]["OUT"][0]
    if STATUS == 0:
        print("\n", "Database Version:", TMP[BASE]["OUT"]["difBuildVersion"])
        print("\n", "Build Version:", TMP[BASE]["OUT"]["difDbVersion"])
        Y = TMP[BASE]["OUT"]["difIssueDate"]
        Y = Y[4:6] + "/" + Y[6:8] + "/" + Y[0:4] if len(Y) == 8 and Y.isdigit() else ""
        print("\n", "Issue Date:", Y, "\n")
        print("\n", "Custom Database Version:", TMP[BASE]["OUT"]["customBuildVersion"])
        print("\n", "Custom Build Version:", TMP[BASE]["OUT"]["customDbVersion"])
        Y = TMP[BASE]["OUT"]["customIssueDate"]
        Y = Y[4:6] + "/" + Y[6:8] + "/" + Y[0:4] if len(Y) == 8 and Y.isdigit() else ""
        print("\n", "Custom Issue Date:", Y, "\n")
        Y = NOW()
        print("\n", "Connected to", PSSCKW2, "successfully @", Y[0:18])
    else:
        print("\n", "Connection could not be made to", "!"*PSSCKW3, PSSCKW2 + ".")
        Y = GLASTRUN()
        if Y:
            print("\n", "Last reached @" + Y[0:18])
    del TMP[BASE]
    return

def VENDRPT():
    #**Prints out the VENDOR INTERFACE DATA FILE (#59.74) sorted by most recent downtime first**
    #The report retrieves the output using the Fileman EN1^DIP data retrieval call
    print("\n", "-"*15, "Check PEPS Services Setup", "-"*15, "\n")
    print("\n", "This report will print out all information related to when and for how long the")
    print("\n", "vendor interface is unavailable (sorted by most recent down time first).")
    print("\n", "This information comes from the VENDOR INTERFACE DATA FILE.")
    print("\n", "You may queue the report to print if you wish. You may also \"^\" to halt the")
    print("\n", "report at any time.", "\n")
    DIC = "^PS(59.74,"
    BY = "-.01"
    L = 0
    DIPCRIT = 1
    FR = "?,"
    TO = "?,"
    DHD = "VENDOR INTERFACE DATA LIST"
    DIOBEG = "W @IOF"
    FLDS = ".01;\"DATE/TIME UNAVAILABLE\",1;\"DATE/TIME AVAILABLE\"\"\";C26\",2;\"TOTAL DOWNTIME\""
    EN1^DIP()

def HRSMIN(MIN):
    # Called from output transform of VENDOR INTERFACE DATA FILE (#59.54) field TOTAL TIME NOT AVAILABLE (field# 2)
    #INPUTS: MIN-TIME IN MINUTES
    #RETURNS HRS AND MINUTES
    HRS, MINHR, HRSMIN = "", 60, ""
    HRS = MIN // MINHR
    MIN = MIN % MINHR
    HRSMIN = str(HRS) + " HR" + ("S" if HRS > 1 else "") if HRS else ""
    HRSMIN = HRSMIN + (", " if HRSMIN else "") + str(MIN) + " MINUTE" + ("S" if MIN > 1 else "") if MIN else HRSMIN
    return HRSMIN

def OUTPUT(INFO, DIWL):
    TMP = {}
    DIWR, DIWF, DIW = 60, "W", {}
    TMP[DIWL] = INFO
    DIWF(DIWL, DIWR, DIWF)
    DIWW()
    del TMP[DIWL]
    return

def PRSRTN():
    #calls std routine to ask user to hit return 
    input("Press Enter to continue...")
    return

def PING(BASE):
    TMP = {}
    TMP[BASE] = {}
    TMP[BASE]["IN"] = {}
    TMP[BASE]["IN"]["PING"] = ""
    IN_PSSHRQ2(BASE)
    del TMP[BASE]
    return

def PING(BASE):
    TMP = {}
    TMP[BASE] = {}
    TMP[BASE]["IN"] = {}
    TMP[BASE]["IN"]["PING"] = ""
    IN_PSSHRQ2(BASE)
    del TMP[BASE]
    return

def PING(BASE):
    TMP = {}
    TMP[BASE] = {}
    TMP[BASE]["IN"] = {}
    TMP[BASE]["IN"]["PING"] = ""
    IN_PSSHRQ2(BASE)
    del TMP[BASE]
    return