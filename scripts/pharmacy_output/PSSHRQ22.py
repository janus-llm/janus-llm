#WOIFO/AV,TS - Handles parsing a PEPS drugTherapyChecks XML element ;09/20/07
#1.0;PHARMACY DATA MANAGEMENT;**136**;9/30/97;Build 89

# @authors - Alex Vazquez, Tim Sabat
# @date    - September 19, 2007
# @version - 1.0

def THERAPY(DOCHAND,NODE,BASE):
    # @DRIVER
    # @DESC Parses the drugTherapyChecks XML elements

    # @DOCHAND Handle to XML document
    # @NODE Node associated with XML element
    # @PSSHAND Handle to DrugOrderChecks object

    # @RETURNS Nothing

    PSS = {}
    PSS["child"] = 0
    PSS["therapyCount"] = 0
    PSMSGCNT = 0

    while PSS["child"] := CHILD^MXMLDOM(DOCHAND, NODE, PSS["child"]) != 0:
        PSS["childName"] = NAME^MXMLDOM(DOCHAND, PSS["child"])
        
        # XML allows messages within both drugTherapyChecks and drugTherapyCheck
        if PSS["childName"] == "message":
            PSMSGCNT += 1
            MSGREAD(DOCHAND, PSS["child"], MSGHASH, PSMSGCNT)
            
        if PSS["childName"] == "drugTherapyCheck":
            PSS["therapyCount"] += 1
            THERREAD(DOCHAND, PSS["child"], DRUGHASH, PSS["therapyCount"], MSGHASH, PSMSGCNT)

    #MSGHASH is set in THEREAD
    MSGWRITE^PSSHRQ21(MSGHASH, BASE, "THERAPY")
    THERWRIT(DRUGHASH, BASE)
    return

def MSGREAD(DOCHAND, NODE, HASH, COUNT):
    # @DESC Handles parsing message section

    # @DOCHAND Handle to XML document
    # @NODE Node associated with XML element
    # @COUNT Count of message sections
    # @HASH Where to store info

    # @RETURNS Nothing

    # Parse the message and store in hash
    PARSEMSG^PSSHRCOM(DOCHAND, NODE, HASH, COUNT)
    return

def THERREAD(DOCHAND, NODE, HASH, COUNT, MSGHASH, MSGCNT):
    # @DESC Handles parsing and storage of drugTherapyCheck element

    # @DOCHAND Handle to XML document
    # @NODE Node associated with XML element
    # @COUNT Count of drug sections
    # @HASH Where to store info
    # @MSGHASH Where message (alert) from FDB is stored
    # @MSGCNT-The current count of the number of messages (messages can occur in both places)

    # @RETURNS Nothing

    PSS = {}
    PSS["child"] = 0
    PSS["messageCount"] = MSGCNT

    while PSS["child"] := CHILD^MXMLDOM(DOCHAND, NODE, PSS["child"]) != 0:
        PSS["childName"] = NAME^MXMLDOM(DOCHAND, PSS["child"])

        if PSS["childName"] == "message":
            PSS["messageCount"] += 1
            MSGREAD(DOCHAND, PSS["child"], MSGHASH, PSS["messageCount"])

        if PSS["childName"] == "interactedDrugList":
            DRUGLIST^PSSHRCOM(DOCHAND, PSS["child"], HASH, COUNT)

        if PSS["childName"] == "classification":
            HASH[COUNT]["classification"] = GETTEXT^PSSHRCOM(DOCHAND, PSS["child"])

        if PSS["childName"] == "duplicateAllowance":
            HASH[COUNT]["duplicateAllowance"] = GETTEXT^PSSHRCOM(DOCHAND, PSS["child"])

        if PSS["childName"] == "shortText":
            HASH[COUNT]["shortText"] = GETTEXT^PSSHRCOM(DOCHAND, PSS["child"])

    return

def THERWRIT(HASH, BASE):
    # @DESC Handles writing drugDrugChecks drugTherapy section of the XML document

    # @HASH ByRef, Hash used to store response
    # @BASE Base of output global

    # @RETURNS Nothing. Stores values in output global.

    PSS = {}
    I = ""
    DRUGNUM = ""
    NODE = ""
    COUNT = 0
    INDX = {}

    while I := HASH[I] != "":
        COUNT = 0

        # Creates the index of drug combinations
        # Each unique drug combination has the corresponding count
        MAKEINDX(INDX, HASH)

        while I := HASH[I] != "":
            COUNT = INDX[DLISTID(HASH, I)]

            NODE = "^TMP($JOB, BASE, ""OUT"", ""THERAPY"", COUNT)"

            while DRUGNUM := HASH[I]["drugList"][DRUGNUM] != "":
                TMPGLOB(HASH, I, COUNT, DRUGNUM, BASE)

            PSS["subCount"] = SUBCOUNT(COUNT, BASE)
            NODE[PSS["subCount"]]["ALLOW"] = HASH[I]["duplicateAllowance"]
            NODE[PSS["subCount"]]["CLASS"] = HASH[I]["classification"]
            NODE[PSS["subCount"]]["SHORT"] = HASH[I]["shortText"]

    return

def SUBCOUNT(COUNT, BASE):
    # @DESC Returns the next subcount for drug therapy output global
    # Format is ^TMP($JOB,BASE,"OUT","THERAPY",COUNT,SUBCOUNT)

    # @COUNT The main count of drug therapy
    # @BASE The base of output global

    # @RETURNS The last subcount of drug therapy output global.

    PSS = {}
    PSS["subCount"] = ""
    PSS["highCount"] = 0

    while PSS["subCount"] := ^TMP($JOB, BASE, "OUT", "THERAPY", COUNT, PSS["subCount"]) != "":
        if int(PSS["subCount"]) > PSS["highCount"]:
            PSS["highCount"] = int(PSS["subCount"])

    return PSS["highCount"] + 1

def MAKEINDX(INDX, HASH):
    # @DESC Creates index of drug list combinations. Uses gcn as the
    # unique identifier of drug.

    # @HASH ByRef, Holds the list of drugs
    # @INDX ByRef, Used to store count of drug list

    # @RETURNS Nothing.  Values returned in INDX hash

    PSS = {}
    PSS["uniqueDrugCombinationCount"] = 0

    while I := HASH[I] != "":
        PSS["uniqueDrugCombination"] = DLISTID(HASH, I)

        if INDX[PSS["uniqueDrugCombination"]] == 0:
            PSS["uniqueDrugCombinationCount"] += 1
            INDX[PSS["uniqueDrugCombination"]] = PSS["uniqueDrugCombinationCount"]

    return

def DLISTID(HASH, I):
    # @DESC Returns the id of the drug list. The id of the drug list
    # consist of the gcn in sorted order separated by '^'.

    # @HASH ByRef, Holds the list of drugs
    # @I    The current count on the hash

    # @RETURNS Id of drug list.

    PSS = {}
    J = ""
    K = ""
    ARRAY = {}

    while J := HASH[I]["drugList"][J] != "":
        PSS["uniqueDrugID"] = HASH[I]["drugList"][J]["gcn"]
        ARRAY[PSS["uniqueDrugID"]] = 1

    K = ""
    PSS["tempCount"] = 0
    PSS["uniqueDrugCombination"] = ""

    while K := ARRAY[K] != "":
        if PSS["tempCount"] > 0:
            PSS["uniqueDrugCombination"] = PSS["uniqueDrugCombination"] + "^" + K

        if PSS["tempCount"] == 0:
            PSS["tempCount"] += 1
            PSS["uniqueDrugCombination"] = K

    return PSS["uniqueDrugCombination"]

def TMPGLOB(HASH, MAINCNT, CHEKCNT, DRUGNUM, BASE):
    # @DESC Writes the drugList to the proper global

    # @HASH ByRef, Has used to store response
    # @CHECKCNT The current TherapyCheck result
    # @DRUGNUM The current drug interaction
    # @BASE Base of the output global

    # @RETURNS Nothing.  Stores values in output global.

    NODE = "^TMP($JOB, BASE, ""OUT"", ""THERAPY"", CHEKCNT, ""DRUGS"", DRUGNUM)"
    NODE = VALUE(HASH, MAINCNT, DRUGNUM)
    return

def VALUE(HASH, MAINCNT, DRUGNUM):
    # @DESC Provides the ""piece" data we use when creating the output global.

    # @HASH ByRef, Has used to store response
    # @MAINCNT The current TherapyCheck result
    # @DRUGNUM The current drug interaction

    # @RETURNS The right side of the global for therapy.

    # PharmacyOrderNumber ^
    # Drug IEN ^
    # Drug Name ^
    # CPRS Order Number ^
    # Package

    OUT = HASH[MAINCNT]["drugList"][DRUGNUM]["orderNumber"] + "^"
    OUT = OUT + HASH[MAINCNT]["drugList"][DRUGNUM]["ien"] + "^"
    OUT = OUT + HASH[MAINCNT]["drugList"][DRUGNUM]["drugName"] + "^"
    OUT = OUT + HASH[MAINCNT]["drugList"][DRUGNUM]["cprsOrderNumber"] + "^"
    OUT = OUT + HASH[MAINCNT]["drugList"][DRUGNUM]["package"]
    return OUT