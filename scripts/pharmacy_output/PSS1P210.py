# PSS1P210 ;PAW - Patch 210 Post Install Routine;4/25/2017
# ;1.0;PHARMACY DATA MANAGEMENT;**210**;9/30/97;Build 9
#
# ;This post-installation routine will identify and report free text in the NAME field
# ;(#.01) of the ADMINISTRATION SCHEDULE file (#51.1) when the TYPE OF SCHEDULE field (#5)
# ;is set to D (Day of the Week).
# Q

def EN():
    # Begin post-installation routine
    if not DUZ:
        print("Your DUZ is not defined. It must be defined to run this routine.")
        return

    NAMSP = "PSS1P210"
    JOBN = "PSS*1.0*210 Post-Installation"
    PATCH = "PSS*1.0*210"

    Y = NOW()
    ZTDTH = FMTH(Y)

    print("=============================================================")
    print("Queuing background job for " + JOBN + "...")
    print("Start time: " + HTE(ZTDTH))
    print("A MailMan message will be sent to the installer upon Post")
    print("Install Completion.")
    print("==============================================================")

    ZTRTN = "ENQN^" + NAMSP
    ZTIO = ""
    SBJM = "Background job for " + JOBN
    ZTDESC = SBJM
    ZTSAVE = {
        "JOBN": JOBN,
        "ZTDTH": ZTDTH,
        "DUZ": DUZ,
        "SBJM": SBJM,
    }

    # Call the MUMPS routine to queue the job
    ZTLOAD(ZTRTN, ZTIO, .ZTSAVE)

    if ZTSK:
        print("*** Task #" + str(ZTSK) + " Queued! ***")
        print("")
        ZTSAVE["ZTSK"] = ZTSK

    print("")

    # Clear XPDQUES variable
    XPDQUES = {}

def ENQN():
    # Loop through file 51.1 and look for Day of the Week Schedule Types with Free Text

    CNT = 8
    PSSIEN = 0
    while PSSIEN:
        if PS(51.1, PSSIEN, 0).field(5) != "D":
            continue

        PSSX = PS(51.1, PSSIEN, 0).field(1)
        PSSZX = PSSX
        PSSX = PSSX.split("@")[0]

        PSSZ2 = 1
        PSSZ4 = "-"
        if "-" not in PSSX and any(char.isdigit() or char.isalpha() for char in PSSX):
            for char in PSSX:
                if not char.isalnum():
                    PSSZ4 = char
                    break

        for PSSZ1 in range(1, len(PSSX.split(PSSZ4))+1):
            PSSZ2 = 0
            if len(PSSX.split(PSSZ4)[PSSZ1-1]) > 1:
                for PSSZ3 in ["MONDAYS", "TUESDAYS", "WEDNESDAYS", "THURSDAYS", "FRIDAYS", "SATURDAYS", "SUNDAYS"]:
                    if PSSX.split(PSSZ4)[PSSZ1-1] == "":
                        PSSZ2 = 1
                        break

        if PSSZ2 == 0:
            PSSX = None

        PSSXTIME = PSSZX.split("@")[1]
        PSSDASH = len(PSSXTIME.split("-"))

        for PSSTIMCT in range(1, PSSDASH+1):
            PSSTIME = PSSXTIME.split("-")[PSSTIMCT-1]

        if len(PSSTIME) > 4:
            PSSX = None

        if not PSSX:
            ^TMP("PSS1P210R",$J,CNT) = PSSZX
            CNT += 1

    STOP()

def STOP():
    XMAIL1()
    XMAIL2()

def XMAIL1():
    # Post-installation Notification for Installer
    XMDUZ = .5
    XMSUB = "PATCH PSS*1.0*210 INSTALLATION COMPLETE"
    XMTEXT = "PSG("
    XMY(DUZ) = ""
    Y = NOW()
    Y = ^DD("DD")(Y)
    PSG(1,0) = "  -- INSTALLER --"
    PSG(2,0) = "  The post-install for PSS*1.0*210 completed " + Y + "."
    ^XMD()

def XMAIL2():
    # Post-installation Notification for Users
    XMSUB = "PSS*1.0*210 Pharmacy Expired Order Status Change"
    XMDUZ = .5
    XMSUB = "PSS*1*210 Post-Install ADMINISTRATION SCHEDULE Report"
    if "PSA ORDERS" in XUSEC:
        for PSSDUZ in XUSEC["PSA ORDERS"]:
            XMY(PSSDUZ) = ""
    if "PSAMGR" in XUSEC:
        for PSSDUZ in XUSEC["PSAMGR"]:
            XMY(PSSDUZ) = ""
    if "PSDMGR" in XUSEC:
        for PSSDUZ in XUSEC["PSDMGR"]:
            XMY(PSSDUZ) = ""
    for PSSDUZ in XUSEC["PSNMGR"]:
        XMY(PSSDUZ) = ""

    ^TMP("PSS1P210R",$J,1) = " Patch PSS*1.0*210 post-installation routine has identified"
    ^TMP("PSS1P210R",$J,2) = " " + str(CNT-8) + " Day of the Week ADMINISTRATION SCHEDULES with free"
    ^TMP("PSS1P210R",$J,3) = " text in the NAME field. Please review."
    ^TMP("PSS1P210R",$J,4) = " "
    ^TMP("PSS1P210R",$J,5) = "Schedule Name"
    ^TMP("PSS1P210R",$J,6) = "======== ===="
    ^TMP("PSS1P210R",$J,7) = " "
    XMY(DUZ) = ""
    if CNT == 8:
        ^TMP("PSS1P210R",$J,8) = "No discrepancy found, nothing to update..."
    XMTEXT = "^TMP(""PSS1P210R"",$J,"
    ^XMD()

EN()