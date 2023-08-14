# BIR/EJW-Post install routine
# 1.0;PHARMACY DATA MANAGEMENT;**55**;9/30/97
# External reference to PSNMGR supported by DBIA 2106
# External reference to ^XUSEC supported by DBIA 10076

# POST-INSTALL ROUTINE FOR PATCH PSS*1*55 - TO POPULATE THE "DTXT" CROSS-REFERENCES IN THE DRUG AND PHARMACY ORDERABLE ITEMS FILE

ZTDTH = ""
if 'ZTQUEUED':
    ZTDTH = $H

if ZTDTH == "":
    print("The background job to populate the 'DTXT' (drug text) cross-reference in the")
    print("PHARMACY ORDERABLE ITEM file (#50.7) and the DRUG file (#50) must be queued.")
    print("If no start date/time is entered when prompted, the background job will be")
    print("queued to run NOW.")
    print()
    BMES^XPDUTL("Queuing background job to populate the 'DTXT' (drug text) cross-reference...")

ZTRTN = "RES^PSSPOST5"
ZTIO = ""
ZTDESC = "Background job to populate 'DTXT' cross-reference"
^%ZTLOAD
ZTDTH, ZTRTN, ZTIO, ZTDESC = None, None, None, None

if 'ZTSK' and not 'ZTQUEUED':
    print("Task Queued !")

def RES():
    if not 'DT':
        DT = $$DT^XLFDT()

    NOW^%DTC
    ^XTMP("PSSTIMEX","START") = %

    BMES^XPDUTL("Populating 'DTXT' cross-references...")

OI:
    BMES^XPDUTL("Populating 'DTXT' x-ref for Pharmacy Orderable Items...")

    PSSOI, PSSTXP, PSSSQ, PSSOICT, PSSDCT = None, None, None, 0, 0

    PSSOI = 0
    while PSSOI:
        if 'PSSOI,^PS(50.7,PSSOI':
            PSSTXP = ""
            while PSSTXP:
                if 'PSSTXP,^PS(50.7,PSSOI,1,"B",PSSTXP':
                    PSSSQ = ""
                    while PSSSQ:
                        if 'PSSSQ,^PS(50.7,PSSOI,1,"B",PSSTXP,PSSSQ':
                            if not 'PSSTXP,^PS(50.7,"DTXT",PSSTXP,PSSOI':
                                ^PS(50.7,"DTXT",PSSTXP,PSSOI,PSSSQ) = ""
                                PSSOICT = PSSOICT + 1

DRUG:
    BMES^XPDUTL("Populating 'DTXT' x-ref for Drug file...")

    PSSDRG = 0
    while PSSDRG:
        PSSTXP = ""
        while PSSTXP:
            if 'PSSTXP,^PSDRUG(PSSDRG,9,"B",PSSTXP':
                PSSSQ = ""
                while PSSSQ:
                    if 'PSSSQ,^PSDRUG(PSSDRG,9,"B",PSSTXP,PSSSQ':
                        " ", PSSDRG, "-", PSSTXP
                        if not 'PSSTXP,^PSDRUG("DTXT",PSSTXP,PSSDRG':
                            ^PSDRUG("DTXT",PSSTXP,PSSDRG,PSSSQ) = ""
                            PSSDCT = PSSDCT + 1

MAIL:
    NOW^%DTC
    PSSTIMEB = %

    Y = ^XTMP("PSSTIMEX","START")
    DD^%DT
    PSSTIMEA = Y

    Y = PSSTIMEB
    DD^%DT
    PSSTIMEB = Y

    XMDUZ = "PHARMACY DATA MANAGEMENT PACKAGE"
    XMY(DUZ) = ""
    XMSUB = "Drug Text Cross Reference Creation"

    PSOCXPDA = 0
    while PSOCXPDA:
        if 'PSOCXPDA,^XUSEC("PSNMGR",PSOCXPDA':
            XMY(PSOCXPDA) = ""

    PSSTEXT = [None] * 16
    PSSTEXT(1) = "Patch PSS*1*55 Drug Text Cross Reference creation is complete."
    PSSTEXT(2) = "It started on " + PSSTIMEA + "."
    PSSTEXT(3) = "It ended on " + PSSTIMEB + "."
    PSSTEXT(4) = " "
    PSSTEXT(5) = PSSOICT + " entries were added to the 'DTXT' cross-reference for the PHARMACY ORDERABLE"
    PSSTEXT(6) = "ITEM file (#50.7)."
    PSSTEXT(7) = " "
    PSSTEXT(8) = PSSDCT + " entries were added to the 'DTXT' cross-reference for the DRUG file (#50)."
    PSSTEXT(9) = " "
    PSSTEXT(10) = "This message is being sent to the installer of the patch and holders of the"
    PSSTEXT(11) = "PSNMGR key. The new Drug Text File Report [PSS DRUG TEXT FILE REPORT] option"
    PSSTEXT(12) = "should be run for all drug text entries in the DRUG TEXT file (#51.7)"
    PSSTEXT(13) = "to verify that the correct drug text is associated with the correct entries"
    PSSTEXT(14) = "in the PHARMACY ORDERABLE ITEM file (#50.7) and the DRUG file (#50)."
    PSSTEXT(15) = "A listing of the original drug text file entries distributed with"
    PSSTEXT(16) = "Patch PSS*1*29 is provided in the Pharmacy Data Management user manual."

    XMTEXT = "PSSTEXT("
    DIFROM^XMD

    PSSTIMEA, PSSTIMEB, XMDUZ, XMSUB, PSSTEXT, XMTEXT = None, None, None, None, None, None

    if 'ZTQUEUED':
        ZTREQ = "@"

    return