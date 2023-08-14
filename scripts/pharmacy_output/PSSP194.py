# PSSP194 ;DAL/DSK-PSS*1.0*194 POST INSTALL ROUTINE
# 1.0;PHARMACY DATA MANAGEMENT;**194**;9/30/97;Build 9
def PSSP194():
    return

# POST INSTALL ENTRY POINT.
def POSTINT():
    ZTDESC, ZTIO, ZTDTH, ZTRTN, ZTSAVE = "PSS*1*194 Post Install", "", $H, "POST^PSSP194", {"DUZ": ""}
    ^%ZTLOAD()
    ^XPDUTL("PSS*1*194 Post Install Task Queued.")
    ^XPDUTL("You will receive a MailMan message")
    ^XPDUTL("when task #" + ZTSK + " has completed.")
    ZTDESC, ZTDTH, ZTIO, ZTRTN, ZTSAVE = None, None, None, None, None
    return

# correct cross references and send mail message
def POST():
    # ^XTMP("PSSP194" used to document changes made
    # Changes are sent in MailMan message to installer
    # ^XTMP is kept for 90 days in case questions arise later
    # and mail message has been deleted
    PSSNOW = ^XLFDT("NOW")
    # in case this routine is run more than once, delete old ^XTMP entry
    K ^XTMP("PSSP194")
    ^XTMP("PSSP194", 0) = ^XLFDT("FMADD", PSSNOW, 90) + "^" + PSSNOW + "^PSS*1.0*194 Post Install Routine PSSP194"
    NAME()
    MAIL()
    return

# Search for incorrect cross references
def NAME():
    # If length is exactly 30, pre-PSS*1*194 version of PSSTXT
    # may not have deleted or changed the cross reference correctly
    # If length is more than 30, change to 30 to be consistent
    # with FileMan logic
    PSSEQ, PSSTR, PSSIEN, PSSINDEX = None, None, None, None
    CHECK()

    PSSEQ = ""
    # Delete cross references which need to be deleted
    while PSSEQ is not None:
        PSSTR = ^XTMP("PSSP194","CROSS",PSSEQ)
        PSSIEN = $P(PSSTR,"^")
        PSSINDEX = $P(PSSTR,"^",3)
        K ^PS(51.7,"B",PSSINDEX,PSSIEN)
        PSSEQ = $O(^XTMP("PSSP194","CROSS",PSSEQ))
    # Set cross references which need to be set
    PSSEQ = ""
    while PSSEQ is not None:
        PSSTR = ^XTMP("PSSP194","B_SET",PSSEQ)
        PSSIEN = $P(PSSTR,"^")
        PSSINDEX = $P(PSSTR,"^",3)
        ^PS(51.7,"B",PSSINDEX,PSSIEN) = ""
        PSSEQ = $O(^XTMP("PSSP194","B_SET",PSSEQ))
    # Kill long cross references and set truncated cross references
    PSSEQ = ""
    while PSSEQ is not None:
        PSSTR = ^XTMP("PSSP194","LONG",PSSEQ)
        PSSIEN = $P(PSSTR,"^")
        PSSINDEX = $P(PSSTR,"^",2)
        K ^PS(51.7,"B",PSSINDEX,PSSIEN)
        PSSINDEX = $P(PSSTR,"^",3)
        if PSSINDEX != "":
            ^PS(51.7,"B",PSSINDEX,PSSIEN) = ""
        PSSEQ = $O(^XTMP("PSSP194","LONG",PSSEQ))
    return

# Check cross reference and correct if necessary
def CHECK():
    PSSNAME, PSSUB = None, None
    PSSINDEX = ""
    PSSEQ = 0
    while PSSINDEX is not None:
        if $L(PSSINDEX) < 30:
            continue
        PSSIEN = ""
        while PSSIEN is not None:
            PSSNAME = $P(^PS(51.7,PSSIEN,0),"^")
            if $E(PSSNAME,1,30) != PSSINDEX:
                PSSEQ = PSSEQ + 1
                PSSUB = $S($L(PSSINDEX) == 30: "CROSS", 1: "LONG")
                ^XTMP("PSSP194",PSSUB,PSSEQ) = PSSIEN + "^" + $S(PSSUB == "CROSS":PSSNAME, 1:PSSINDEX) + "^" + $S(PSSUB == "CROSS":PSSINDEX, 1:$E(PSSNAME,1,30))
                IND()
            PSSIEN = $O(^PS(51.7,"B",PSSINDEX,PSSIEN))
        PSSINDEX = $O(^PS(51.7,"B",PSSINDEX))
    return

# Double check to make sure there is a valid index
def IND():
    if PSSNAME != "" and not (^PS(51.7,"B",PSSNAME,PSSIEN) or ^PS(51.7,"B",substr(PSSNAME,1,30),PSSIEN)):
        ^XTMP("PSSP194","B_SET",PSSEQ) = PSSIEN + "^" + PSSNAME + "^" + $E(PSSNAME,1,30)
    return

# Send Mail message
def MAIL():
    XMY, PSLINE, PSSPACE, XMDUZ, XMY, XMSUB, A, XMTEXT, PSFLG = None, None, None, None, None, None, None, None
    K XMY
    PSFLG, PSLINE = 0, 1
    PSSPACE = "                                        "
    # Send MailMan message to installer
    XMDUZ, XMY(DUZ), XMSUB = "POST-INSTALL,PSS*1.0*194", "", "POST-INSTALL PSS*1.0*194 INFORMATION"
    A(PSLINE) = ""
    PSLINE = PSLINE + 1
    A(PSLINE) = "    PSS*1.0*194 POST-INSTALL"
    PSLINE = PSLINE + 1
    A(PSLINE) = " "
    PSLINE = PSLINE + 1
    A(PSLINE) = "    The content of this message is informational only."
    PSLINE = PSLINE + 1
    A(PSLINE) = "    No action needs to be taken."
    PSLINE = PSLINE + 1
    A(PSLINE) = " "
    PSSEQ = ""
    while PSSEQ is not None:
        if PSSEQ == "CROSS":
            PSFLG = 1
            MCROSS()
        if PSSEQ == "B_SET":
            PSFLG = 1
            MBSET()
        if PSSEQ == "LONG":
            PSFLG = 1
            MLONG()
        PSSEQ = $O(^XTMP("PSSP194",PSSEQ))
    if not PSFLG:
        PSLINE = PSLINE + 1
        A(PSLINE) = "    The DRUG TEXT (#51.7) file was checked and no issues were found."
    # Set mail message in ^XTMP in case mail message accidentally deleted
    ^XTMP("PSSP194","MAIL") = A
    # Send mail message
    XMTEXT = "A(" ^XMD
    # Delete task from TaskManager list
    ZTREQ = "@"
    return

# Incorrect cross reference was deleted
def MCROSS():
    PSSUB, PSSTR, PSSIEN, PSSNAME, PSSCROSS = None, None, None, None, None
    # Set top level of ^XMTP subscript for ease of troubleshooting later if necessary
    ^XTMP("PSSP194",PSSEQ) = "Incorrect Cross References which were deleted by post-install routine PSSP194"
    PSLINE = PSLINE + 1
    A(PSLINE) = " "
    PSLINE = PSLINE + 1
    A(PSLINE) = "The following entries in the DRUG TEXT (#51.7) file had"
    PSLINE = PSLINE + 1
    A(PSLINE) = "incorrect cross references deleted."
    PSLINE = PSLINE + 1
    A(PSLINE) = " "
    PSLINE = PSLINE + 1
    A(PSLINE) = "    IEN          Name"
    PSLINE = PSLINE + 1
    A(PSLINE) = "    ------------ ---------------------------------------------"
    PSLINE = PSLINE + 1
    A(PSLINE) = "                      Incorrect Cross Reference Deleted"
    PSLINE = PSLINE + 1
    A(PSLINE) = "                      ---------------------------------------"
    STR()
    return

# No cross references existed, so cross references were set
def MBSET():
    PSSUB, PSSTR, PSSIEN, PSSNAME, PSSCROSS = None, None, None, None, None
    # Set top level of ^XMTP subscript for ease of troubleshooting later if necessary
    ^XTMP("PSSP194",PSSEQ) = "No cross references existed, so cross reference was set"
    PSLINE = PSLINE + 1
    A(PSLINE) = "The following entries in the DRUG TEXT (#51.7) file had no cross references,"
    PSLINE = PSLINE + 1
    A(PSLINE) = "so cross references were set."
    PSLINE = PSLINE + 1
    A(PSLINE) = ""
    PSLINE = PSLINE + 1
    A(PSLINE) = "    IEN          Name"
    PSLINE = PSLINE + 1
    A(PSLINE) = "    ------------ ---------------------------------------------"
    PSLINE = PSLINE + 1
    A(PSLINE) = "                      Cross Reference Set"
    PSLINE = PSLINE + 1
    A(PSLINE) = "                      ------------------------------"
    STR()
    return

# Long cross references which were truncated
def MLONG():
    PSSUB, PSSTR, PSSIEN, PSSNAME, PSSCROSS = None, None, None, None, None
    # Set top level of ^XMTP subscript for ease of troubleshooting later if necessary
    ^XTMP("PSSP194",PSSEQ) = "Long cross references which were truncated"
    PSLINE = PSLINE + 1
    A(PSLINE) = " "
    PSLINE = PSLINE + 1
    A(PSLINE) = "The following entries in the DRUG TEXT (#51.7) file had long"
    PSLINE = PSLINE + 1
    A(PSLINE) = "cross references deleted and truncated cross references set."
    PSLINE = PSLINE + 1
    A(PSLINE) = ""
    PSLINE = PSLINE + 1
    A(PSLINE) = "    IEN          Long Cross Reference Deleted"
    PSLINE = PSLINE + 1
    A(PSLINE) = "    ------------ ---------------------------------------------"
    PSLINE = PSLINE + 1
    A(PSLINE) = "                      Truncated Cross Reference Set"
    PSLINE = PSLINE + 1
    A(PSLINE) = "                      ------------------------------"
    STR()
    return

# Set data in mail message array
def STR():
    PSLINE = PSLINE + 1
    A(PSLINE) = " "
    PSSUB = ""
    while PSSUB is not None:
        PSSTR = ^XTMP("PSSP194",PSSEQ,PSSUB)
        PSSIEN = $P(PSSTR,"^")
        PSSNAME = $P(PSSTR,"^",2)
        PSSCROSS = $P(PSSTR,"^",3)
        PSLINE = PSLINE + 1
        A(PSLINE) = "    " + PSSIEN + $E(PSSPACE,1,14 - $L(PSSIEN)) + $S(PSSNAME != "":PSSNAME, 1:"No name on entry")
        PSLINE = PSLINE + 1
        A(PSLINE) = "                      " + $S(PSSCROSS != "":PSSCROSS, 1:"None -- no name on entry")
        PSSUB = $O(^XTMP("PSSP194",PSSEQ,PSSUB))
    return

PSSP194()