# BIR/WRT-Edit DRUG TEXT file routine ; 11/15/01 8:11
# 1.0;PHARMACY DATA MANAGEMENT;**29,55,194**;9/30/97;Build 9

def BEGIN():
    PSSNFI = 1
    PSSFG = 0
    print("\nThis option enables you to edit entries in the DRUG TEXT file.\n")
    PSSQQ = 1
    while True:
        DA = None
        ASK()
        if PSSFG:
            break

def DONE():
    global DA, PSSFG, PSSQQ, PSSNFI, NAME, PSSENT, PSSBEG, PSSEND, PSSSRT, PSSXX
    DA = None
    PSSFG = None
    PSSQQ = None
    PSSNFI = None
    NAME = None
    PSSENT = None
    PSSBEG = None
    PSSEND = None
    PSSSRT = None
    PSSXX = None
    # Clear variables
    for var in ['%', 'D', 'D0', 'DI', 'DIE', 'DLAYGO', 'DQ', 'DR', 'X', 'Y']:
        exec(f"{var} = None")
    return

def ASK():
    global PSSFG, PSSENT, DA, DIE, DR
    print()
    DIC = "^PS(51.7,"
    DIC(0) = "QEALMN"
    DLAYGO = 51.7
    DIC = input(DIC)
    if DIC < 0:
        PSSFG = 1
        return
    PSSENT = int(DIC)
    WRIT()
    REVW()
    print()
    DA = PSSENT
    DIE = "^PS(51.7,"
    NAME()
    if PSSFG:
        return
    TEXT()
    if PSSFG:
        return
    print()
    DR = "1;2"
    exec("^DIE")
    CHECKI()

def CHECK():
    global DA, DIK
    if not any([DA, '^PS(51.7,DA,2,0)', '^PS(50.7,"DTXT",DA)', '^PSDRUG("DTXT",DA)']):
        DIK = "^PS(51.7,"
        exec("^DIK")
    return

def WRIT():
    print("\nThere may be entries in your DRUG file and PHARMACY ORDERABLE ITEM file linked")
    print("to this Drug Text Name. Editing information related to this Drug Text entry")
    print("will affect the display of information related to these.")
    print()
    return

def REVW():
    global PSSSRT, PSSXX, PSSBEG, PSSEND
    DIR = {}
    DIR("A") = "Do you want to review the list of drugs and orderable items linked to this Drug Text entry? "
    DIR(0) = "Y"
    DIR("B") = "YES"
    DIR("?",1) = "Answering 'Yes' will list all entries in the Drug file or Orderable Item file"
    DIR("?",2) = "that are linked to this drug text entry.  The list could be long, so a "
    DIR("?") = "device can be entered to print a hard copy, if desired."
    Y = input(DIR)
    if Y == 1:
        PSSSRT = "S"
        PSSXX = PSSBEG = PSSEND = "^PS(51.7,PSSENT,0)".split("^")[1]
    return

def OUTMSG():
    print("\nIMPORTANT!! After editing the Drug Text Name OR Text, review the drugs and")
    print("orderable items linked to this entry for accuracy.")
    return

def CHECKI():
    if "^PS(51.7,DA,0)".split("^")[2]:
        MSG()
    return

def MSG():
    print("\nBecause this entry was inactivated, drugs and orderable items that are linked")
    print("to this entry will no longer display the text associated with this entry.")
    print("You should review all drugs and orderable items associated with this Drug Text")
    print("entry and update appropriately.")
    print()
    return

def NAME():
    global PSSFG
    print()
    DIR = {}
    DIR(0)="Y"
    DIR("A")="Do you want to edit the Drug Text Name"
    DIR("B")="NO"
    X = input(DIR)
    if X == "^":
        PSSFG = 1
        return
    OUTMSG()
    if not X:
        return
    PSSNAME = "^PS(51.7,DA,0)".split("^")[1]
    DIR(0) = "FO^1:75"
    DIR("A") = "Drug Text Name: "
    DIR("B") = PSSNAME
    X = input(DIR)
    if X == "^":
        PSSFG = 1
        return
    if X and X != PSSNAME:
        if "@" in X:
            print("  **DELETIONS ARE NOT ALLOWED!")
            return
        exec("^PS(51.7,""B"",$E(X,1,30),DA) = ''")
        exec("del ^PS(51.7,""B"",$E(PSSNAME,1,30),DA)")
        exec("^PS(51.7,DA,0) = X")
    return

def TEXT():
    print()
    DIR = {}
    DIR(0) = "Y"
    DIR("A") = "Do you want to edit the text for this entry"
    DIR("B") = "YES"
    X = input(DIR)
    if X == "^":
        PSSFG = 1
        return
    if not X:
        return
    print("\nWARNING: The absence of text lines will cause this Drug Text entry")
    print("         to be completely deleted.")
    print()
    DIR(0) = "E"
    DIR("A") = "Press Return to continue"
    X = input(DIR)
    print()
    DR = "3"
    exec("^DIE")
    CHECK()
    if not any(["^PS(51.7,DA,2,0)", "^PS(51.7,DA,2,0)"]):
        PSSFG = 1
        print("   **** **** **** **** **** **** **** **** **** **** ****")
        print("\n   The absence of text lines caused this Drug Text entry")
        print("   to be completely deleted.")
        print("\n   Therefore, Synonym and Inactivation Date")
        print("   will not be asked.")
        print("\n   **** **** **** **** **** **** **** **** **** **** ****\n")
        DIR(0) = "E"
        DIR("A") = "   Press Return to continue"
        X = input(DIR)
        print()
    return

BEGIN()
DONE()