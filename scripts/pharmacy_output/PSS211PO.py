def PSS211PO():
    # DAL/JCH - PATCH PSS*1.0*211 POST INSTALL - 09/13/2017
    # 1.0;PHARMACY DATA MANAGEMENT;**211**;09/30/97;Build 20
    # This routine uses the following IAs:
    # #4640 - ^HDISVF01 calls (supported)
    # #4639 - ^HDISVCMR calls     (supported)
    # #4651 - ^HDISVF09 calls     (supported)
    
    # MAIN ENTRY POINT
    SUCCESS, DEMFAC, X, Y, DA, X1, X2, ZTRTN, ZTDESC, ZTDTH, TMP, DOMPTR, DIE, DA, DR, FIL, DOMPTR, DOMAIN = [None] * 15
    DEMFAC = KSP^XUPARAM("INST")
    DOMAIN = "PHARMACY DATA MANAGEMENT"
    SUCCESS, DOMPTR = GETIEN^HDISVF09(DOMAIN, .DOMPTR)
    if not SUCCESS or not DOMPTR:
        MES^XPDUTL("***** Error retrieving the IEN for the " + DOMAIN + " domain.")
        PSTHALT("Seeding for file #50.60699 was not performed.")
    FIL = 50.60699
    HDIS(FIL, DOMPTR, DOMAIN)
    return

def HDIS(FIL, DOMPTR, DOMAIN):
    TMP, HDIMSG, B, C = [None] * 4
    
    # New file can't be seeded if there is no data?
    if FIL == 50.60699:
        if not $O(^PSMDF(50.60699,0)):
            DUMSEED(50.60699, "SEEDOSF")
        PSEED(50.60699, DOMPTR, DOMAIN)
    return

def PSEED(FIL, DOMPTR, DOMAIN):
    # Check for previous "seeding"(deployment), quit if already done.
    ASTATUS, TMP, XPROD, PSSITE, XMSUB, XMDUZ, XMY, HDITEXT, FILNAM, MSG, XMTEXT, XMZ = [None] * 12
    
    ASTATUS = $P($$GETSTAT^HDISVF01(FIL),U)
    if ASTATUS > 3:
        MSG = "File: " + FIL + " Has already been seeded. Status is: " + ASTATUS
        PSTHALT(MSG)
        return
    
    # set the seeding status to complete for data deployments.
    SETSTAT^HDISVF01(FIL,,4)
    
    # send message to STS that patch is installed and the current status
    FILE^DID(FIL,,"NAME","FILNAM","ERR")
    FILNAM = $G(FILNAM("NAME"))
    XPROD = $$PROD^XUPROD()
    PSSITE = $$SITE^VASITE()
    XMSUB = "Site: " + $P(PSSITE,"^",2) + " File: " + FIL + " in " + ($S(XPROD:"PRODUCTION",1:"TEST")) + " ready for ERT Update"
    XMY("G.HDIS ERT NOTIFICATION@FORUM.DOMAIN.EXT")=""
    XMDUZ = "Site: " + $P(PSSITE,"^",3) + " Patch Install PSS*1.0*211 is Complete"
    XMY(DUZ)=""
    K HDITEXT
    HDITEXT(1)=""
    HDITEXT(2) = "Site: " + $P(PSSITE,"^",2) + " - " + $P(PSSITE,"^",3)
    HDITEXT(2) = HDITEXT(2) + " with Domain/IP Address of " + $G(^XMB("NETNAME"))  # facility name
    HDITEXT(3) = "Has Installed Patch PSS*1.0*211 into their " + ($S(XPROD:"PRODUCTION",1:"TEST")) + " System Environment"
    HDITEXT(4) = "The Patch was Installed on: "
    B = $$NOW^XLFDT N Y S Y=B D DD^%DT S HDITEXT(4) = HDITEXT(4) + Y  # date/time
    HDITEXT(5)=""
    HDITEXT(6) = "Patch PSS*1.0*211 has standardized file: " + FILNAM + " (#" + FIL + ")"
    HDITEXT(7)=""
    HDITEXT(8) = "The current HDIS status of file #" + FIL + "is:  " + $P($$GETSTAT^HDISVF01(FIL),U)
    HDITEXT(9)=""
    HDITEXT(10) = "Site: " + $P(PSSITE,"^",2) + " - " + $P(PSSITE,"^",3) + "  needs full file update of the " + FILNAM + " file (#" + FIL + " as soon as possible."
    HDITEXT(11)=""
    N DIFROM S XMTEXT = "HDITEXT(" D ^XMD K DIFROM
    MSG = "File: " + FIL + " Has been 'seeded'. Message Number: " + $G(XMZ)
    PSTDONE(MSG)
    return

def PSTDONE(MSG):
    HDIMSG = [None] * 5
    HDIMSG(1)=""
    HDIMSG(2) = MSG
    HDIMSG(3)="***** Post-installation of Patch PSS*1.0*211 HDIS 'seeding' " + FILNAM + " file (#" + FIL + ") has Completed."
    HDIMSG(4)="***** An update message has been sent to Enterprise VistA Support."
    HDIMSG(5)=""
    MES^XPDUTL(.HDIMSG)
    return

def DUMSEED(PSMFILE, PSDTAG):
    # New file <#nn.99> contains no data, can't be seeded unless there is at least one entry
    # MASTER DOSAGE FORM (#50.60699) file initial population data elements from DAT99 line tag
    
    #   PSDATA ";" PIECE - FIELD # - FIELD NAME
    #          PIECE #1  -   n/a   - IEN 
    #          PIECE #2  -  .01    - RxNorm Name
    #          PIECE #3  -    1    - RxNorm Code
    #          PIECE #4  -    2    - RxNorm Term Type
    
    PSMFI, PSDATA, PSDATLN, PSFDA, PSRSLT, XUMF = [None] * 6
    XUMF = 1
    PSDATLN = 1
    while True:
        PSDATA = $P($T(@PSDTAG+PSDATLN),";",3,10)
        if not PSDATA:
            break
        PSMFI = $P(PSDATA,";")
        PSFDA(PSMFILE,"+1,",.01) = $P(PSDATA,";",2)
        PSFDA(PSMFILE,"+1,",1) = $P(PSDATA,";",3)
        PSFDA(PSMFILE,"+1,",2) = $P(PSDATA,";",4)
        PSRSLT = INSREC(PSMFILE, PSMFI, .PSFDA)
    return

def INSREC(PSFILE, PSIEN, PSFDA):
    # Insert PSIEN into file PSFILE with data in PSFDA
    if not PSFILE:
        return "0^Invalid parameter"
    PSDERR = UPDATE^DIE("", PSFDA, "", PSDERR)
    if $D(PSDERR):
        return -1
    return +$G(PSFDA)

def PSTHALT(MSG):
    # display error message
    HDIMSG = [None] * 5
    HDIMSG(1)=""
    HDIMSG(2) = MSG
    HDIMSG(3)="***** Post-installation of Patch PS*5.3*933 HDIS 'seeding' has been halted."
    HDIMSG(4)="***** Please contact Enterprise VistA Support."
    HDIMSG(5)=""
    MES^XPDUTL(.HDIMSG)
    return

def SEEDOSF():
    # Data to populated the MASTER DOSAGE FORM (#50.60699) file.
    # 1;24 Hour Extended Release Tablet;316936;DF
    # 2;Aerosol;324049;ET
    # 3;Bar;317692;DF
    # 4;Beads;316993;DF
    # 5;Buccal Film;858080;DF
    return