#PSSSUTIL ;BIR/RTR-Utility routine for Orderable Item ;09/02/97
#;;1.0;PHARMACY DATA MANAGEMENT;**38**;9/30/97

#MAT ; Match Additive to already existing Orderable Item
DIE = "PS(52.6,"
DA = PSAIEN
DR = "15////" + ZZFLAG
^DIE

SYN1 = {}
SCOUNT = 0
for SS in ^PS(52.6,PSAIEN,3):
    SCOUNT += 1
    SYN[SCOUNT] = ^PS(52.6,PSAIEN,3,SS,0)

if SCOUNT:
    SCOUNT = 0
    for WW in SYN:
        if SYN[WW] not in ^PS(50.7,ZZFLAG,2,"B"):
            SCOUNT += 1
            SYN1[SCOUNT] = SYN[WW]

if SCOUNT:
    VV = 0
    for VVV in ^PS(50.7,ZZFLAG,2):
        VV = VVV

    VV = VV if VV else 1
    for TT in SYN1:
        ^PS(50.7,ZZFLAG,2,VV,0) = SYN1[TT]
        VV += 1

    for VV in ^PS(50.7,ZZFLAG,2):
        SYNNAM = ^PS(50.7,ZZFLAG,2,VV,0)
        ^PS(50.7,ZZFLAG,2,"B",SYNNAM,VV) = ""

    SCOUNT = 0
    SCLAST = 0
    for TT in ^PS(50.7,ZZFLAG,2):
        SCOUNT += 1
        SCLAST = TT

    ^PS(50.7,ZZFLAG,2,0) = "^50.72^" + SCLAST + "^" + SCOUNT

PSPOI = ZZFLAG
NEWFLAG = 1
DIR^PSSPOIM3

if PSSDIR:
    print("\nNow editing Orderable Item:")
    print($P(^PS(50.7,ZZFLAG,0),"^") + "   " + $P(^PS(50.606,+$P(^PS(50.7,ZZFLAG,0),"^",2),0),"^"))
    INACT^PSSADDIT

PSSDIR = ""
PSSCROSS = ""
EN^PSSPOIDT(PSPOI)

if not PSSSSS:
    EN2^PSSHL1(PSPOI,"MUP")

G EN^PSSADDIT

#SOMAT ;Match Solution to an already existing Orderable Item
DIE = "PS(52.7,"
DA = PSSIEN
DR = "9////" + ZZFLAG
^DIE

SYN1 = {}
SCOUNT = 0
for SS in ^PS(52.7,PSSIEN,3):
    SCOUNT += 1
    SYN[SCOUNT] = ^PS(52.7,PSSIEN,3,SS,0)

if SCOUNT:
    SCOUNT = 0
    for WW in SYN:
        if SYN[WW] not in ^PS(50.7,ZZFLAG,2,"B"):
            SCOUNT += 1
            SYN1[SCOUNT] = SYN[WW]

if SCOUNT:
    VV = 0
    for VVV in ^PS(50.7,ZZFLAG,2):
        VV = VVV

    VV = VV if VV else 1
    for TT in SYN1:
        ^PS(50.7,ZZFLAG,2,VV,0) = SYN1[TT]
        VV += 1

    for VV in ^PS(50.7,ZZFLAG,2):
        SYNNAM = ^PS(50.7,ZZFLAG,2,VV,0)
        ^PS(50.7,ZZFLAG,2,"B",SYNNAM,VV) = ""

    SCOUNT = 0
    SCLAST = 0
    for TT in ^PS(50.7,ZZFLAG,2):
        SCOUNT += 1
        SCLAST = TT

    ^PS(50.7,ZZFLAG,2,0) = "^50.72^" + SCLAST + "^" + SCOUNT

PSSOI = ZZFLAG
NEWFLAG = 1
DIR^PSSPOIM3

if PSSDIR:
    print("\nNow editing Orderable Item:")
    print($P(^PS(50.7,ZZFLAG,0),"^") + "   " + $P(^PS(50.606,+$P(^PS(50.7,ZZFLAG,0),"^",2),0),"^"))
    INACT^PSSSOLIT

PSSDIR = ""
PSSCROSS = ""
EN^PSSPOIDT(PSSOI)

if not PSSSSS:
    EN2^PSSHL1(PSSOI,"MUP")

G ^PSSSOLIT