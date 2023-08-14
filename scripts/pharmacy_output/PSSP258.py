# PSSP258 ;HDSO/DSK - PATCH PSS*1*258 Post-Install ; Jan 19, 2023@15:30
# ;1.0;PHARMACY DATA MANAGEMENT;**258**;9/30/97;Build 9

# Reference to ^XOB(18.12 in ICR #7414

# EN ; post install actions
def EN():
    PSSLINE = 0
    ^TMP("PSS258P",$J) = {}

    # Store backup data for backing out the patch
    ^XTMP("PSSP258B") = {}
    ^XTMP("PSSP258B",0) = $$FMADD^XLFDT(DT,180)_"^"_DT_"^PSS*1.0*258 Post-Install"

    WS()
    MAIL()
    ^TMP("PSS258P",$J) = {}

# SETTXT(TXT) ; Setting Plain Text
def SETTXT(TXT):
    PSSLINE = PSSLINE + 1
    ^TMP("PSS258P",$J,PSSLINE) = TXT


# WS ; Web Service update
def WS():
    PSSIEN = 0
    PSSTYPE = XPDQUES("POS1")
    # Get the site type entered in the Installation question POS1
    # PSSTYPE will be a value of 1-4 (PRE-PROD, SQA, STAGE, DEVELOPMENT) (if no value, this is a PRODUCTION system)
    if not PSSTYPE:
        PSSTYPE = 5

    if PSSTYPE == 1:
        PSSNAME = "PRE-PROD"
    elif PSSTYPE == 2:
        PSSNAME = "SQA"
    elif PSSTYPE == 3:
        PSSNAME = "STAGING"
    elif PSSTYPE == 4:
        PSSNAME = "DEVELOPMENT"
    else:
        PSSNAME = "PRODUCTION"

    PSSFLAG = 0
    PSSCNT = 1
    while not PSSFLAG:
        PSSDATA = $P($T(WEBS+PSSCNT),";;",2)
        if PSSTYPE == PSSDATA[1]:
            PSSFLAG = 1
        PSSCNT = PSSCNT + 1

    PSSIEN = $$FIND1^DIC(18.12,,"B","PPSN")
    # not likely that PPSN not defined, but checking anyway
    if not PSSIEN:
        PSSTXT = "Update of PPSN web server not performed since PPSN web server not defined."
        BMES^XPDUTL(PSSTXT)
        SETTXT(PSSTXT)
        return

    # Some sites might have performed the updates manually without waiting for the patch (per
    # email communications). If SSL configuration was updated, server would have been also,
    # so no need to check both.
    if $$GET1^DIQ(18.12,PSSIEN,3.02) == "encrypt_only_tlsv12":
        PSSTXT = "Update of PPSN web server not needed since updates were"
        BMES^XPDUTL(PSSTXT)
        SETTXT(PSSTXT)
        PSSTXT = "already performed."
        BMES^XPDUTL(PSSTXT)
        SETTXT(PSSTXT)
        return

    # Store current settings in case backout needed.
    ^XTMP("PSSP258B","WS",18.12,PSSIEN) = ^XOB(18.12,PSSIEN)
    PSSOLDSSL = $$GET1^DIQ(18.12,PSSIEN,3.02)
    PSSOLDADR = $$GET1^DIQ(18.12,PSSIEN,.04)
    PSSIEN = PSSIEN + ","
    DISABLE("PPSN",PSSIEN)
    FDA(18.12,PSSIEN,.04) = $P(PSSDATA,";",3) # server address
    FDA(18.12,PSSIEN,.06) = 1 # status enabled
    FDA(18.12,PSSIEN,3.02) = "encrypt_only_tlsv12"
    FILE^DIE("K","FDA","PSSERR")
    K FDA

    PSSTXT = "In this " + PSSNAME + " environment, the PSS*1.0*258 post-install routine"
    BMES^XPDUTL(PSSTXT)
    SETTXT(PSSTXT)

    if not $D(PSSERR("DIERR",1,"TEXT",1)):
        PSSTXT = "successfully updated web server PPSN and enabled the server."
        BMES^XPDUTL(PSSTXT)
        SETTXT(PSSTXT)
        PSSTXT = " "
        BMES^XPDUTL(PSSTXT)
        SETTXT(PSSTXT)
        PSSTXT = "SSL configuration -"
        BMES^XPDUTL(PSSTXT)
        SETTXT(PSSTXT)
        PSSTXT = "   old: " + PSSOLDSSL
        BMES^XPDUTL(PSSTXT)
        SETTXT(PSSTXT)
        PSSTXT = "   new: encrypt_only_tlsv12"
        BMES^XPDUTL(PSSTXT)
        SETTXT(PSSTXT)
        PSSTXT = "Server address -"
        BMES^XPDUTL(PSSTXT)
        SETTXT(PSSTXT)
        PSSTXT = "   old: " + PSSOLDADR
        BMES^XPDUTL(PSSTXT)
        SETTXT(PSSTXT)
        PSSTXT = "   new: " + $P(PSSDATA,";",3)
        BMES^XPDUTL(PSSTXT)
        SETTXT(PSSTXT)
    else:
        PSSTXT = "has NOT updated WEB SERVER ""PPSN"" due to FileMan error:"
        BMES^XPDUTL(PSSTXT)
        SETTXT(PSSTXT)
        PSSTXT = $S($G(PSSERR("DIERR",1,"TEXT",1)) != "":$G(PSSERR("DIERR",1,"TEXT",1)),1:"No error text available.")
        BMES^XPDUTL(PSSTXT)
        SETTXT(PSSTXT)
        PSSTXT = "Submit a ServiceNow ticket requesting assistance in researching the error."
        BMES^XPDUTL(PSSTXT)
        SETTXT(PSSTXT)


# DISABLE(SRVNAME,PSSIEN) ; Disable PPSN server if it exists-will set it back to enabled
def DISABLE(SRVNAME,PSSIEN):
    PSSERVER = {}
    # Set STATUS to DISABLED
    PSSERVER(18.12,PSSIEN,.06) = 0
    FILE^DIE("","PSSERVER","PSSERR") # update existing entry
    if not $D(PSSERR("DIERR",1,"TEXT",1)):
        BMES^XPDUTL("o WEB SERVER '" + SRVNAME + "' server temporarily disabled.")
    # Not aborting install if PSSERR("DIERR" is returned since the update
    # should be instaneous, so it doesn't matter if disabling did not occur first.


# MAIL ; Sends Mailman message
def MAIL():
    PSSMGR = 0
    while PSSMGR:
        XMY(PSSMGR) = ""
        PSSMGR = $O(^XUSEC("PSNMGR",PSSMGR))

    XMY(DUZ) = ""
    XMSUB = "PSS*1*258 Post-Install Complete"
    XMDUZ = "PSS*1*258 Install"
    XMTEXT = "^TMP(""PSS258P"",$J,"
    ^XMD = {}


# WEBS ;  Map the system type to the SERVER endpoint
def WEBS():
    # 1;PRE-PROD;vaausapppps401.aac.domain.ext
    # 2;SQA;vaausppsapp93.aac.domain.ext
    # 3;STAGE;vaausapppps901.aac.domain.ext
    # 4;DEV;vaausppsapp91.aac.domain.ext
    # 5;PROD;vaww.ppsn.domain.ext
    return [
        [1, "PRE-PROD", "vaausapppps401.aac.domain.ext"],
        [2, "SQA", "vaausppsapp93.aac.domain.ext"],
        [3, "STAGE", "vaausapppps901.aac.domain.ext"],
        [4, "DEV", "vaausppsapp91.aac.domain.ext"],
        [5, "PROD", "vaww.ppsn.domain.ext"]
    ]