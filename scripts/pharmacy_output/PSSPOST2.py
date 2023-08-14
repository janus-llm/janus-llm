# BIR/LDT-Post install routine
# 08/01/00
# 1.0;PHARMACY DATA MANAGEMENT;**38**;9/30/97
# External reference to ORY94 supported by DBIA 3415

# POST-INSTALL ROUTINE
if $$PATCH^XPDUTL("PSS*1.0*38"):
    G END

RES:
if '$G(DT):
    DT = $$DT^XLFDT()

# Delete AD cross references on Orderable Items in Files 52.6 and 52.7
DELIX^DDMOD(52.7,9,2)
DELIX^DDMOD(52.6,15,2)

# Delete CHANGE TYPE OF ORDER FROM OERR field (#20.412) and IV IDENTIFIER field (#32) from the PHARMACY SYSTEM file (#59.7)
BMES^XPDUTL("Deleting obsolete fields...")
DA = 20.412
DIK = "^DD(59.7,"
DA(1) = 59.7
^DIK

# Delete CORRESPONDING UD ITEM field (#3) and CORRESPONDING IV ITEM field (#4) from the PHARMACY ORDERABLE ITEM file (#50.7)
for DA in [3, 4]:
    DIK = "^DD(50.7,"
    DA(1) = 50.7
    ^DIK

# Delete Instructions multiple and Pre-Ordering Enhancement field
DA = 2
DA(1) = 50.6066
DIK = "^DD(50.6066,"
^DIK

DA = 4
DIK = "^DD(50.606,"
DA(1) = 50.606
^DIK

DIU = 50.6062
DIU(0) = "S"
EN^DIU2

BMES^XPDUTL("Deleting obsolete data...")
for PSSDF in 0:0:
    PSSDF = $O(^PS(50.606,PSSDF))
    if 'PSSDF:
        break
    K ^PS(50.606,PSSDF,"INS")
    if $D(^PS(50.606,PSSDF,"MISC")):
        $P(^PS(50.606,PSSDF,"MISC"),"^",2)=""
    for PSSDF1 in 0:0:
        PSSDF1 = $O(^PS(50.606,PSSDF,"NOUN",PSSDF1))
        if 'PSSDF1:
            break
        if $D(^PS(50.606,PSSDF,"NOUN",PSSDF1,0)):
            $P(^(0),"^",3)=""

for PSSPSF in $O(^PS(59.7,PSSPSF)):
    $P(^PS(59.7,PSSPSF,20.4),"^",16)=""

for PSSOI in $O(^PS(50.7,PSSOI)):
    $P(^PS(50.7,PSSOI,0),"^",10)=""
    $P(^PS(50.7,PSSOI,0),"^",11)=""

# fix options (matching) DISABLE A/SMATCHING, MODIFY DD, FIX FROM DRIG ENTER.EDIT
# QUICK^ORUPDATE ; loop through orders, call PSSQORD

# This quick order update may take a while, can CPRS write dots
CON:
for PSSL in 0:0:
    PSSL = $O(^PS(52.6,PSSL))
    if 'PSSL:
        break
    if $D(^PS(52.6,PSSL,0)):
        PSSOLDOI = $P($G(^PS(52.6,PSSL,0)),"^",11)
        $P(^PS(52.6,PSSL,0),"^",11)=""
        if PSSOLDOI:
            K ^PS(52.6,"AOI",PSSOLDOI,PSSL)
        PSSDRG = $P($G(^PS(52.6,PSSL,0)),"^",2)
        if 'PSSDRG:
            continue
        PSSNEWOI = $P($G(^PSDRUG(PSSDRG,2)),"^")
        if PSSOLDOI and PSSNEWOI:
            if '$D(^PSDRUG("A526",PSSDRG,PSSL)):
                ^XTMP("PSSCONA",PSSOLDOI,PSSL) = PSSNEWOI
        if '$D(^PS(50.7,PSSNEWOI,0)):
            continue
        $P(^PS(52.6,PSSL,0),"^",11) = PSSNEWOI
        ^PS(52.6,"AOI",PSSNEWOI,PSSL) = ""
        ^PSDRUG("A526",PSSDRG,PSSL) = ""

BMES^XPDUTL("Updating IV Solution Orderable Items...")
for PSSL in 0:0:
    PSSL = $O(^PS(52.7,PSSL))
    if 'PSSL:
        break
    if $D(^PS(52.7,PSSL,0)):
        PSSOLDOI = $P($G(^PS(52.7,PSSL,0)),"^",11)
        $P(^PS(52.7,PSSL,0),"^",11)=""
        if PSSOLDOI:
            K ^PS(52.7,"AOI",PSSOLDOI,PSSL)
        PSSDRG = $P($G(^PS(52.7,PSSL,0)),"^",2)
        if 'PSSDRG:
            continue
        PSSNEWOI = $P($G(^PSDRUG(PSSDRG,2)),"^")
        if PSSOLDOI and PSSNEWOI:
            if '$D(^PSDRUG("A527",PSSDRG,PSSL)):
                ^XTMP("PSSCONS",PSSOLDOI,PSSL) = PSSNEWOI
        if '$D(^PS(50.7,PSSNEWOI,0)):
            continue
        $P(^PS(52.7,PSSL,0),"^",11) = PSSNEWOI
        ^PS(52.7,"AOI",PSSNEWOI,PSSL) = ""
        ^PSDRUG("A527",PSSDRG,PSSL) = ""

# Updating CPRS with new Orderable Item information
OI:
D BMES^XPDUTL("Setting new Orderable Item cross reference...")
PSSCONTX = 0
for PSSRD1 in 0:0:
    PSSRD1 = $O(^PSDRUG(PSSRD1))
    if 'PSSRD1:
        break
    S PSSRD2 = $P($G(^PSDRUG(PSSRD1,2)),"^")
    if 'PSSRD2:
        continue
    ^PS(50.7,"A50",PSSRD2,PSSRD1) = ""
    if not PSSCONTX%50:
        print(".")
    PSSCONTX += 1

PSSCONTX = 0
BMES^XPDUTL("Updating Pharmacy Orderable Items...")
if not $G(DT):
    DT = $$DT^XLFDT()

for PSSRI in 0:0:
    PSSRI = $O(^PS(50.7,PSSRI))
    if 'PSSRI:
        break
    if $D(^PS(50.7,PSSRI,0)):
        PSSORITM = PSSRI
        $P(^PS(50.7,PSSORITM,0),"^",12) = ""
        if $P(^PS(50.7,PSSORITM,0),"^",3):
            PSSORIDT = $P(^PS(50.7,PSSORITM,0),"^",4)
            if PSSORIDT and PSSORIDT <= DT:
                $P(^PS(50.7,PSSORITM,0),"^",4) = DT
        PSSCROSS = 1
        PSSTEST = PSSORITM
        EN1^PSSPOIDT
        K PSSTEST,PSSCROSS
        if not PSSCONTX%10:
            print(".")
        PSSCONTX += 1

POST^ORY94

MAIL:
NOW^%DTC
PSSTIMEB = %
Y = $G(^XTMP("PSSTIMEX","START"))
D ^%DT
PSSTIMEA = Y
Y = $G(PSSTIMEB)
D ^%DT
PSSTIMEB = Y
XMDUZ = "PHARMACY DATA MANAGEMENT PACKAGE"
XMY(DUZ) = ""
XMSUB = "Pharmacy Ordering Enhancements Install"
K PSSTEXT
PSSTEXT(1) = "The Pharmacy Ordering Enhancements installation is complete."
PSSTEXT(2) = "It started on " + $G(PSSTIMEA) + "."
PSSTEXT(3) = "It ended on " + $G(PSSTIMEB) + "."
XMTEXT = "PSSTEXT("
D ^XMD

END:
Q

RESTART:
G RES
Q