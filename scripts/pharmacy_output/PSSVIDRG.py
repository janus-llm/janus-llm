#PSSVIDRG ;BIR/PR,WRT-ADD OR EDIT IV DRUGS ;June 3, 2018@20:00
# ;;1.0;PHARMACY DATA MANAGEMENT;**2,10,32,38,125,146,174,189,229**;9/30/97;Build 1
# ;
# ;Reference to ENIVKV^PSGSETU is supported by DBIA # 2153.
# ;Reference to ^PSIV is supported by DBIA # 2155.
# ;Reference to ^PSIVHLP1 is supported by DBIA # 2156.
# ;Reference to ^PSIVXU is supported by DBIA # 2157.
# ;
# ENS ;Enter here to enter/edit solutions
# N FI,PSPRNM S DRUGEDIT=1,FI=52.7
# L +^PS(FI):$S($G(DILOCKTM)>0:DILOCKTM,1:3) E  W $C(7),!!,"Someone else is entering drugs ... try later !",!! G K
# ENS1 ;
# ; PSS*1*146 Compare and confirm SOLUTION Print name change
# N DA,DIC,DLAYGO,II,PSDA,PSI,PSSY,PSSDG,PSSEL1,PSSDRG
# NS2 S PSI=0 I $G(DISPDRG),$O(^PS(52.7,"AC",DISPDRG,0)) S PSSY=0 F  S PSSY=$O(^PS(52.7,"AC",DISPDRG,PSSY)) Q:'PSSY  S PSI=PSI+1,PSSY(PSI)=PSSY
# ;I PSI=1 S DIC("B")=$G(PSSY(1)) S DIC=FI,DIC(0)="QEALMNTV",DLAYGO=52.7,DIC("T")="" D ^DIC I Y<0 K PSFLGA G K1
# if PSI == 0:
#     DIC = FI
#     DIC(0) = "QEALMNTV"
#     DLAYGO = 52.7 
#     result = DIC
#     result += ^DIC 
#     if result < 0:
#         K PSFLGA 
#         G K1
# ENS2 ; IV Solutions Editing
# N PSSQOX
# S PSSQUIT=0,PSSQOX=1
# if not PSFLGA and PSI>0:
#     while true:
#         print(" ",GET1^DIQ(50,DISPDRG,.01)," currently linked to IV Solutions:")
#         PSDA = 0
#         while true:
#             PSDA = $O(PSSY(PSDA))
#             if not PSDA:
#                 break
#             II = II + 1
#             print("\n",II,". ",$P(^PS(52.7,$G(PSSY(PSDA)),0),"^"),"   ",$P(^PS(52.7,$G(PSSY(PSDA)),0),"^",3))
#         print("\n","Select ",(1 if PSI==1 else "1-"+PSI)," from list above or type 'NEW' to link to a new IV Solution: ")
#         X = input()
#         if not X or X=="^":
#             Y = -1
#             break
#         if X.upper()=="NEW":
#             NEW(52.7)
#             continue
#         if not PSSY(X):
#             print("\n","Select the number corresponding to the IV SOLUTION you want to edit","\n","or type 'NEW' to link ",GET1^DIQ(50,DISPDRG,.01)," to a new IV SOLUTION.",$C(7))
#             continue
#         if PSSY(X):
#             Y = $G(PSSY(X))
#         break
# if Y<0:
#     K1
# print("\n")
# K PSSEL1
# PSSASK = "SOLUTIONS"
# DRUG = +Y
# DIE = FI
# (DA,ENTRY) = +Y
# DR = ".01"
# EECK
# if PSSEL1 = "^":
#     K1
# if PSSEL1 = 2:
#     Y = 0
#     print("\n")
#     NS2
# N PSSQUIT,PSSINADT
# PSSQUIT = 0
# PSSINADT = GET1^DIQ(52.7,ENTRY,8,"I")
# PSSDRG = $P($G(^PS(52.7,ENTRY,0)),"^",2)
# DA = ENTRY
# DIE = "^PS(52.7,"
# DR = "D PRNMHD^PSSVIDRG;.01;.01///^S X=$$PRNM^PSSVIDRG();.02;"
# DR += "1///^S X=$$GEND^PSSVIDRG($S($G(DISPDRG):DISPDRG,$G(PSSDRG):PSSDRG,1:""""));D GETD^PSSVIDRG;"
# DR += "2:7;@8;8;D IVSOLINA^PSSVIDRG;10:15;17:99999"
# PSSENTRY = DA
# ^DIE
# if PSQUIT is not set:
#     PSSQOX = 0
#     MFS^PSSDEE
# K PSFLGA,PSSY
# Q

def ENS():
    FI = 52.7
    DRUGEDIT = 1

    result = L + ^PS(FI)
    if result:
        print("\nSomeone else is entering drugs ... try later !\n")
        G K
    ENS1()

def ENS1():
    PSI = 0
    if DISPDRG and ^PS(52.7,"AC",DISPDRG,0):
        PSSY = 0
        while True:
            PSSY = $O(^PS(52.7,"AC",DISPDRG,PSSY))
            if not PSSY:
                break
            PSI = PSI + 1
            PSSY(PSI) = PSSY
    if PSI == 0:
        DIC = FI
        DIC(0) = "QEALMNTV"
        DLAYGO = 52.7
        result = DIC
        result += ^DIC
        if result < 0:
            K PSFLGA
            G K1
    ENS2()

def ENS2():
    PSSQOX = 1
    PSSQUIT = 0
    if not PSFLGA and PSI > 0:
        while True:
            print(" ",GET1^DIQ(50,DISPDRG,.01)," currently linked to IV Solutions:")
            PSDA = 0
            while True:
                PSDA = $O(PSSY(PSDA))
                if not PSDA:
                    break
                II = II + 1
                print("\n",II,". ",$P(^PS(52.7,$G(PSSY(PSDA)),0),"^"),"   ",$P(^PS(52.7,$G(PSSY(PSDA)),0),"^",3))
            print("\n","Select ",(1 if PSI==1 else "1-"+PSI)," from list above or type 'NEW' to link to a new IV Solution: ")
            X = input()
            if not X or X=="^":
                Y = -1
                break
            if X.upper()=="NEW":
                NEW(52.7)
                continue
            if not PSSY(X):
                print("\n","Select the number corresponding to the IV SOLUTION you want to edit","\n","or type 'NEW' to link ",GET1^DIQ(50,DISPDRG,.01)," to a new IV SOLUTION.",$C(7))
                continue
            if PSSY(X):
                Y = $G(PSSY(X))
            break
    if Y<0:
        K1()
    print("\n")
    K PSSEL1
    PSSASK = "SOLUTIONS"
    DRUG = +Y
    DIE = FI
    (DA,ENTRY) = +Y
    DR = ".01"
    EECK()
    if PSSEL1 == "^":
        K1()
    if PSSEL1 == 2:
        Y = 0
        print("\n")
        NS2()
    PSSQUIT = 0
    PSSINADT = GET1^DIQ(52.7,ENTRY,8,"I")
    PSSDRG = $P($G(^PS(52.7,ENTRY,0)),"^",2)
    DA = ENTRY
    DIE = "^PS(52.7,"
    DR = "D PRNMHD^PSSVIDRG;.01;.01///^S X=$$PRNM^PSSVIDRG();.02;"
    DR += "1///^S X=$$GEND^PSSVIDRG($S($G(DISPDRG):DISPDRG,$G(PSSDRG):PSSDRG,1:""""));D GETD^PSSVIDRG;"
    DR += "2:7;@8;8;D IVSOLINA^PSSVIDRG;10:15;17:99999"
    PSSENTRY = DA
    ^DIE
    if PSQUIT == 0:
        PSSQOX = 0
        MFS^PSSDEE
    K PSFLGA,PSSY

def K1():
    L - ^PS(FI)

def K():
    X="PSGSETU" X ^%ZOSF("TEST") I  D ENIVKV^PSGSETU

def ECK():
    print("\nYou are editing a Additive or Solution which is linked to a different","\ndispense drug from the one you are currently editing.")

def SOI():
    if ^PS(59.7,1,80) and $P(^PS(59.7,1,80),"^",2) > 1:
        print("\nYou are NOW in the ORDERABLE ITEM matching for Solutions.")
        Y = ENTRY_"^"_$P(^PS(52.7,ENTRY,0),"^",1)
        PSMASTER = 1
        MAS^PSSSOLIT
        K PSMASTER

def ADDOI():
    if ^PS(59.7,1,80) and $P(^PS(59.7,1,80),"^",2) > 1:
        print("\nYou are NOW in the ORDERABLE ITEM matching for Additives.")
        Y = ENTRY_"^"_$P(^PS(52.6,ENTRY,0),"^",1)
        PSMASTER = 1
        MAS^PSSADDIT
        K PSMASTER

def EECK():
    if PSSZ:
        FILE = $S(PSSASK="ADDITIVES":$G(^PS(52.6,ENTRY,0)),1:$G(^PS(52.7,ENTRY,0)))
        PSSIEN = $P(FILE,"^",2)
        if PSSIEN == '':
            PASSIN()
    if PSSIEN != DISPDRG:
        if $D(^PSDRUG(PSSIEN)):
            ECK()
            EECK1()
    print("\nDo you really want to link this ",$S(PSSASK="ADDITIVES":"Additive",1:"Solution")," to ",$P(^PSDRUG(DISPDRG,0),"^",1))
    while true:
        %=2
        YN^DICN
        if %Y == "^":
            PSSEL1 = "^"
            break
        if %:
            PSSEL1 = %
        if %Y == " ":
            print("  (A 'YES' or 'NO' response is required.)")
        if PSSEL1:
            break

def EECK1():
    if not $D(^PSDRUG(PSSIEN)):
        return
    print("\nThis Additive or Solution is linked to ",$P(^PSDRUG(PSSIEN,0),"^",1),".","\nYou are editing dispense drug ",$P(^PSDRUG(DISPDRG,0),"^",1),".",)

def ECK():
    print("\nYou are editing a Additive or Solution which is linked to a different","\ndispense drug from the one you are currently editing.")

def IVSOLINA():
    if not X or PSSINADT and (X and X!=PSSINADT):
        if (not X or X>DT):
            if $$GET1^DIQ(52.7,DA,17,"I"):
                OI = +$$GET1^DIQ(52.7,DA,9,"I")
                if $$CKDUPSOL^PSSDDUT2(OI,DA,+$$GET1^DIQ(52.7,DA,2),1):
                    $P(^PS(52.7,DA,"I"),"^") = PSSINADT
                    Y = "@8"
                else:
                    PSSINADT = X
        else:
            PSSINADT = X 