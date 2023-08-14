# PSSDEEA ;PBM/RMS - DRUG FILE ENTER/EDIT AUDIT ; 18 May 2018  10:55 AM
# 1.0;PHARMACY DATA MANAGEMENT;**227**;;Build 18
# ------------------------------------------------------------------
def BEFORE(TAG):
    """
    Capture the drug entry before it is edited to have to compare to
    after the user completes the editing. Email changes in
    linetag 'AFTER' (called at the end of PSSDEE).
    From: PSSDEE [PSS DRUG ENTER/EDIT]
    Output:
      1. ^UTILITY(TAG,$J,DA)=Drug file entry number DA before editing
      2. ZDA ; DA or IEN of Drug file #50 entry
      3. ZN    ; Will be equal to 1 if a new drug was entered into file
    """
    # ZEXCEPT: DA,Y,ZDA,ZN
    ^UTILITY(TAG,$J,DA) = ^PSDRUG(DA)
    ZDA = DA
    ZN = Y.split("^")[2]

def AFTER(TAG):
    """
    DOCUMENTATION AND SETUP INFORMATION

    Modifications:

    * PSSDEE calls BEFORE^PSSDEEA to create ^UTILITY("PSSDEE",$J,DA) data.
      ^UTILITY data holds all ^PSDRUG data for drug prior to any
      editing.
    * PSSDEE later calls AFTER^PSSDEEA to compare the value of the drug
      file entry after editing to the pre-snapshot values held in
      ^UTILITY. If changes have been made, a Mailman message is
      sent to members of a mail group. (See SETUP below)

    Note: USING the Drug Enter/Edit option is sufficient to trigger
    the audit email, even if a non-audited field is the only change
    made by the user.
    """
    # ZEXCEPT: PSSZMES,PSSZNOC,ANS,CHANGES,COUNT,FIELD,FLAG,LABEL,NEWVAL,OLDVAL,USER,ZDA,ZDAN,ZN,PSSZNODE,ZZJ
    if not ZDA:
        return
    COUNT = 6
    USER = ^VA(200,DUZ,0).split("^")
    ZDAN = ^PSDRUG(ZDA,0).split("^")
    HEADER()
    COMPAR()
    SEND()
    K PSSZMES,ZDA,ZDAN,LABEL,PSSZNODE,OLDVAL,NEWVAL,FIELD,CHANGES,FLAG,ZZJ,ANS,ZN,PSSZNOC
    NEWVAL = ""

def HEADER():
    """
    HEADER FOR FIELDS CHANGED IN THE DRUG ENTER/EDIT OPTION
    """
    # ZEXCEPT: PSSZMES,USER,ZDAN
    PSSZMES.append("Please Note:  The Drug Enter/Edit option was used by " + USER + ".")
    PSSZMES.append("The drug that was entered/edited was " + ZDAN + ".")
    PSSZMES.append("-------------------------------------------------------------------------------")

def COMPAR():
    """
    # ZEXCEPT: PSSZMES,ANS,FLAG,LABEL,NEWVAL,OLDVAL,ZDA,TAG,PSSZNOC
    """
    PSSZNOC = 0
    PSSZNODE = 0
    while PSSZNODE in [0, 2, 3, 8.5, 660, 660.1, "EPH", "I", "ND"]:
        if ZDA:
            ^UTILITY(TAG,$J,ZDA,PSSZNODE) = ""
        if not (^PSDRUG(ZDA, PSSZNODE) or ^UTILITY(TAG,$J,ZDA,PSSZNODE)):
            continue
        if not ^UTILITY(TAG,$J,ZDA,PSSZNODE) and ^PSDRUG(ZDA, PSSZNODE):
            CHANGES(PSSZNODE) = ^PSDRUG(ZDA, PSSZNODE)
        if not ^PSDRUG(ZDA, PSSZNODE) and ^UTILITY(TAG,$J,ZDA,PSSZNODE):
            CHANGES(PSSZNODE) = ^UTILITY(TAG,$J,ZDA,PSSZNODE)
        if not (CHANGES(PSSZNODE) or ^PSDRUG(ZDA, PSSZNODE) or ^UTILITY(TAG,$J,ZDA,PSSZNODE)):
            continue
        if ^UTILITY(TAG,$J,ZDA,PSSZNODE) != ^PSDRUG(ZDA,PSSZNODE):
            CHANGES(PSSZNODE) = ""
            ZZJ = 1
            while ZZJ in range(1, 11):
                FLAG = 0
                ANS = ""
                if ^PSDRUG(ZDA,PSSZNODE).split("^")[ZZJ] != ^UTILITY(TAG,$J,ZDA,PSSZNODE).split("^")[ZZJ]:
                    ANS = ^UTILITY(TAG,$J,ZDA,PSSZNODE).split("^")[ZZJ]
                    FLAG = 1
                if FLAG == 1 and ANS == "":
                    ANS = "NULL"
                CHANGES(PSSZNODE) = CHANGES(PSSZNODE) + ANS + "^"
                ZZJ += 1
    if not CHANGES:
        PSSZNOC = 1
        PSSZMES.append("     ***   No Audited Changes Made  ***")
    FLAG = 0
    for PSSZNODE in [0, 2, 3, 8.5, 660, 660.1, "EPH", "I", "ND"]:
        LABEL = "SUB" + PSSZNODE
        if CHANGES(PSSZNODE):
            ZZJ = 1
            while ZZJ in range(1, 12):
                if "^^^^^^^^^^^^^^^^^" in CHANGES(PSSZNODE).split("^")[ZZJ:11]:
                    break
                if CHANGES(PSSZNODE).split("^")[ZZJ:11] == "" or not CHANGES(PSSZNODE).split("^")[ZZJ:11]:
                    continue
                if TAG not in ^UTILITY(TAG,$J,ZDA):
                    SETLB()
                OLDVAL = CHANGES(PSSZNODE).split("^")[ZZJ]
                if OLDVAL == "":
                    continue
                OLDVAL = OLDVAL + OLDEXT(OLDVAL, PSSZNODE, ZZJ)
                if ^PSDRUG(ZDA, PSSZNODE):
                    NEWVAL = ^PSDRUG(ZDA, PSSZNODE).split("^")[ZZJ] + NEWEXT(ZDA, PSSZNODE, ZZJ)
                STOR()

def OLDEXT(OLDVAL, PSSZNODE, PIECE):
    """
    COMPUTE EXTERNAL 'OLD' VALUE WHERE NECESSARY
    """
    FIELDNUM = ^DD(50,"GL",PSSZNODE,PIECE).split("^")[0]
    if not FIELDNUM:
        return ""
    FIELDTYP = ^DD(50,FIELDNUM,0).split("^")[1]
    if FIELDTYP[0] != "P":
        return ""
    PTRFILE = int(FIELDTYP[2:])
    return " (" + $$GET1^DIQ(PTRFILE, OLDVAL, ".01") + ")"

def NEWEXT(ZDA, PSSZNODE, PIECE):
    """
    COMPUTE EXTERNAL 'NEW' VALUE WHERE NECESSARY
    """
    FIELDNUM = ^DD(50,"GL",PSSZNODE,PIECE).split("^")[0]
    if not FIELDNUM:
        return ""
    EXTERNAL = $$GET1^DIQ(50,ZDA,FIELDNUM)
    INTERNAL = $$GET1^DIQ(50,ZDA,FIELDNUM,"I")
    if INTERNAL == EXTERNAL:
        return ""
    return " (" + EXTERNAL + ")"

def SEND():
    """
    # ZEXCEPT: ZDA,ZDAN,PSSZNOC
    """
    XMSUB = ("DRUG ENTER/EDIT ACCESS (" if PSSZNOC else "DRUG ENTER/EDIT AUDIT (") + str(ZDA) + ":" + ZDAN + ")"
    XMDUZ = DUZ if DUZ else 0.5
    XMTEXT = "PSSZMES"
    XMY("G.PSS DEE AUDIT") = ""
    XMY(DUZ) = ""
    ^XMD()

def STOR():
    """
    STORES VALUES INTO MAILMAN VARIABLES
    # ZEXCEPT: PSSZMES,COUNT,FIELD,LABEL,NEWVAL,OLDVAL,SPACES
    """
    if "660.1" in LABEL:
        LABEL = "SUB6601"
    FIELD = $P($T(@(LABEL)+ZZJ),";",3)
    PSSZMES.append(FIELD)
    COUNT += 1
    PSSZMES.append(SPACES[:30-len(FIELD)] + OLDVAL)
    COUNT += 1
    PSSZMES.append(SPACES[:30-len("OLD: ")] + "OLD: " + OLDVAL)
    COUNT += 1
    PSSZMES.append(SPACES[:30-len("NEW: ")] + "NEW: " + NEWVAL)
    COUNT += 1
    PSSZMES.append(" ")
    COUNT += 1

def SETLB():
    """
    SETS $TEXT LABEL
    # ZEXCEPT: LABEL,PSSZNODE
    """
    if PSSZNODE == 0:
        LABEL = "SUB0"
    elif PSSZNODE == 2:
        LABEL = "SUB2"
    elif PSSZNODE == 3:
        LABEL = "SUB3"
    elif PSSZNODE == 8.5:
        LABEL = "SUB85"
    elif PSSZNODE == 660:
        LABEL = "SUB660"
    elif PSSZNODE == 660.1:
        LABEL = "SUB6601"
    elif PSSZNODE == "EPH":
        LABEL = "SUBEPH"
    elif PSSZNODE == "ND":
        LABEL = "SUBND"
    else:
        LABEL = "SUBI"

def SUB0():
    """
    FIELDS FOR ^PSDRUG(ZDA,0)
    """
    return ["GENERIC NAME", "VA CLASSIFICATION", "DEA, SPECIAL HDLG", "MAXIMUM DOSE PER DAY", "STANDARD SIG", "FSN", "DRUG GROUP/INTERACTION", "WARNING LABEL", "NON-FORMULARY", "MESSAGE"]

def SUB2():
    """
    FIELDS FOR ^PSDRUG(ZDA,2)
    """
    return ["PHARMACY ORDERABLE ITEM", "RESTRICTION", "APPLICATION PACKAGES' USE", "NDC", "*PRIMARY DRUG"]

def SUB3():
    """
    FIELDS FOR ^PSDRUG(ZDA,3)
    """
    return ["CMOP DISPENSE"]

def SUB85():
    """
    FIELDS FOR ^PSDRUG(ZDA,8.5)
    """
    return ["*ATC CANISTER", "ATC MNEMONIC"]

def SUB660():
    """
    FIELDS FOR ^PSDRUG(ZDA,660)
    """
    return ["REORDER LEVEL", "ORDER UNIT", "PRICE PER ORDER UNIT", "NORMAL AMOUNT TO ORDER", "DISPENSE UNITS PER ORDER UNIT", "PRICE PER DISPENSE UNIT", "SOURCE OF SUPPLY", "DISPENSE UNIT"]

def SUB6601():
    """
    FIELDS FOR ^PSDRUG(ZDA,660.1)
    """
    return ["CURRENT INVENTORY"]

def SUBEPH():
    """
    FIELDS FOR ^PSDRUG(ZDA,'EPH')
    """
    return ["DAW CODE", "NCPDP DISPENSE UNIT", "NCPDP QUANTITY MULTIPLIER", "EPHARMACY BILLABLE", "EPHARMACY BILLABLE (TRICARE)", "EPHARMACY BILLABLE (CHAMPVA)", "SENSITIVE DIAGNOSIS DRUG"]

def SUBI():
    """
    FIELDS FOR ^PSDRUG(ZDA,'I')
    """
    return ["INACTIVE DATE"]

def SUBND():
    """
    FIELDS FOR ^PSDRUG(ZDA,'ND')
    """
    return ["NATIONAL DRUG FILE ENTRY", "VA PRODUCT NAME", "PSNDF VA PRODUCT NAME ENTRY", "PACKAGE SIZE", "PACKAGE TYPE", "NATIONAL DRUG CLASS", "CMOP ID", "NATIONAL FORMULARY INDICATOR"]

# Call the functions
BEFORE(TAG)
AFTER(TAG)