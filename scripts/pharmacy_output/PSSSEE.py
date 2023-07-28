# BIR/ASJ-SYNONYM DRUG ENTER/EDIT ROUTINE ; 01/21/00 13:30
# 1.0;PHARMACY DATA MANAGEMENT;**37,57,70,77,82,125**;09/30/97;Build 2
# Reference to ^PS(59 supported by DBIA #1976

import os

PSDRUG = None
PSSFLAG = None
XX = None
DVER = None
DMFU = None
DNSNAM = None
DNSPORT = None
XX = ""

def BEGIN():
    global PSSFLAG
    PSSFLAG = 0
    PSSDEE2()
    PSSXX = 1
    while True:
        DA = None
        ASK()
        if PSSFLAG:
            break

    DONE()
    PSSDEE2()
    PSSFLAG = None
    os.system('clear')

def ASK():
    global PSSFLAG
    print()
    DIC = "^PSDRUG("
    DIC(0) = "QEAMN"
    DIC()
    if Y < 0:
        PSSFLAG = 1
        return
    DA = +Y
    DISPDRG = DA
    if not +^PSDRUG(DISPDRG):
        print(f"{chr(7)}Another person is editing this one.")
        return

    COMMON()
    if not PSSHUIDG():
        DRG(DISPDRG)
        -^PSDRUG(DISPDRG)

    for XX in range(0, len(^PS(59))):
        DVER = GET1(59, XX, 105, "I")
        DMFU = GET1(59, XX, 105.2)
        if DVER == "2.4":
            DNSNAM = GET1(59, XX, 2006)
            DNSPORT = GET1(59, XX, 2007)
            if DNSNAM != "" and DMFU == "YES":
                DRG(DISPDRG, "", DNSNAM, DNSPORT)

def COMMON():
    DIE = "^PSDRUG("
    DR = "[PSS SYNONYM]"
    DIE()
    ^DIE
    DIE = None
    DR = None
    DA = None
    Y = None

BEGIN()