#WOIFO/AV,TS - Parses a PEPS drugDrugChecks XML element ; 08 Jun 2016  5:49 PM
#1.0;PHARMACY DATA MANAGEMENT;**136,160,184**;9/30/97;Build 14

# @authors - Alex Vazquez, Tim Sabat
# @date    - September 19, 2007
# @version - 1.0

def DRUGDRUG(DOCHAND, NODE, BASE):
    # @DESC Handles putting the drugDrugChecks XML element into
    #       the DrugOrderChecks object
    #
    # @DOCHAND Handle to XML document
    # @NODE Node associated with XML element
    # @PSSHAND Handle to DrugOrderChecks object
    #
    # @RETURNS Nothing
    PSS = {}
    MSGHASH = {}
    DRUGHASH = {}
    PSMSGCNT = 0

    PSS["child"] = 0
    PSS["drugCount"] = 0
    PSMSGCNT = 0

    while PSS["child"] != 0:
        PSS["child"] = CHILD(DOCHAND, NODE, PSS["child"])
        if PSS["child"] != 0:
            PSS["childName"] = NAME(DOCHAND, PSS["child"])
            # xml can have message at the top level of drugDrugCheck as well as within drugDrugChecks
            if PSS["childName"] == "message":
                PSMSGCNT += 1
            if PSS["childName"] == "message":
                MSGREAD(DOCHAND, PSS["child"], MSGHASH, PSMSGCNT)

            if PSS["childName"] == "drugDrugCheck":
                PSS["drugCount"] += 1
            if PSS["childName"] == "drugDrugCheck":
                DRUGREAD(DOCHAND, PSS["child"], DRUGHASH, PSS["drugCount"], MSGHASH, PSMSGCNT)
    
    # Write to globals
    # MSGHASH is populated within DRUGREAD if a message exists
    MSGWRITE(MSGHASH, BASE, "DRUGDRUG")
    DRUGWRIT(DRUGHASH, BASE)
    return

def MSGREAD(DOCHAND, NODE, HASH, COUNT):
    # @DESC Handles parsing message section
    #
    # @DOCHAND Handle to XML document
    # @NODE Node associated with XML element
    # @COUNT Count of message sections
    # @HASH Where to store info
    #
    # @RETURNS Nothing
    #
    # Parse the message and store in hash
    PARSEMSG(DOCHAND, NODE, HASH, COUNT)

def MSGWRITE(HASH, BASE, SUB):
    # @DESC Handles writing message section of the XML document
    # @NOTE:Error nodes for drugsnotchecked and for drug dosing messages are set 
    # in PSSHRQ23
    # @HASH ByRef, Hash used to store response
    # @BASE Base of output global
    # @SUB Type of message --DRUGDRUG, THERAPY OR DOSE
    # @RETURNS Nothing. Stores values in output global.
    PSS = {}
    I = ""
    NODE = ""
    WARNFLG = 0
    NODECNT = 0

    I = ""
    while I != "":
        # Create the node to be used with subscript indirection
        NODE = "^TMP($JOB,BASE,\"OUT\",SUB,\"ERROR\",HASH(I,\"orderNumber\"))"
        # gets next error number
        NODECNT = int(NODECNT) + 1
        NODE = "^TMP($JOB,BASE,\"OUT\",SUB,\"ERROR\",HASH(I,\"orderNumber\"),NODECNT)"
        # Need to $G several hash entries because they are undefined coming from NOTWRITE^PSSHRQ23
        if HASH[I]["severity"] == "Information":
            continue  # If severity="information" don't save
        @NODE[0] = HASH[I]["drugName"] + "^" + HASH[I]["ien"] + "^" + HASH[I]["cprsOrderNumber"] + "^" + HASH[I]["package"]
        @NODE["SEV"] = HASH[I]["severity"]
        @NODE["TYPE"] = HASH[I]["type"]
        @NODE["TEXT"] = HASH[I]["text"]
        WARNFLG = 1 if HASH[I]["severity"] == "Warning" else 0
        # Message node to display to user
        @NODE["MSG"] = ERRMSG(SUB, HASH[I]["drugName"], HASH[I]["orderNumber"], WARNFLG)
        I = I + 1

def DRUGREAD(DOCHAND, NODE, HASH, COUNT, MSGHASH, MSGCNT):
    # @DESC Handles parsing and storage of drugDrugCheck element
    #
    # @DOCHAND Handle to XML document
    # @NODE Node associated with XML element
    # @COUNT Count of message sections
    # @HASH Where to store info (by ref)
    # @MSGHASH-Where message information is stored (by ref)
    # @MSGCNT-counter for messages
    # 
    # @RETURNS Nothing
    PSS = {}
    PSS["child"] = 0
    PSS["messageCount"] = MSGCNT

    while PSS["child"] != 0:
        PSS["child"] = CHILD(DOCHAND, NODE, PSS["child"])
        if PSS["child"] != 0:
            PSS["childName"] = NAME(DOCHAND, PSS["child"])

            if PSS["childName"] == "message":
                PSS["messageCount"] += 1
                MSGREAD(DOCHAND, PSS["child"], MSGHASH, PSS["messageCount"])

            if PSS["childName"] == "interactedDrugList":
                DRUGLIST(DOCHAND, PSS["child"], HASH, COUNT)

            if PSS["childName"] == "severity":
                # Translate the peps severity into a vista specific severity
                HASH[COUNT]["severity"] = TRANSEV(GETTEXT(DOCHAND, PSS["child"]))

            if PSS["childName"] == "interaction":
                HASH[COUNT]["interaction"] = GETTEXT(DOCHAND, PSS["child"])

            if PSS["childName"] == "shortText":
                HASH[COUNT]["shortText"] = GETTEXT(DOCHAND, PSS["child"])

            if PSS["childName"] == "professionalMonograph":
                MONOGRAF(DOCHAND, PSS["child"], HASH, "ProfessionalMonograph", COUNT)

            if PSS["childName"] == "consumerMonograph":
                MONOGRAF(DOCHAND, PSS["child"], HASH, "ConsumerMonograph", COUNT)

def MONOGRAF(DOCHAND, NODE, HASH, MONOTYPE, COUNT):
    # @DESC Parses and stores the monograph of the monograph type
    #
    # @DOCHAND Handle to XML document
    # @NODE Node associated with XML element
    # @HASH Handle to DrugOrderChecks object
    # @MONOTYPE Type of monograph either ProfessionalMonograph or ConsumerMonograph
    #
    # @RETURNS Nothing
    PSS = {}
    PSS["child"] = 0
    PSS["i"] = 0

    while PSS["child"] != 0:
        # Get the sub elements of the monograph type section
        PSS["child"] = CHILD(DOCHAND, NODE, PSS["child"])
        if PSS["child"] != 0:
            PSS["childName"] = NAME(DOCHAND, PSS["child"])
            if PSS["childName"] == "monographSource":
                HASH[COUNT]["monographSource"] = GETTEXT(DOCHAND, PSS["child"])
                continue

            PSS["i"] = PSS["i"] + 1

            # if this is references element get reference sub-element.
            if PSS["childName"] == "references":
                REF(DOCHAND, PSS["child"], HASH, MONOTYPE, COUNT)
            
            # Get text of element
            PSS["sectionText"] = GETTEXT(DOCHAND, PSS["child"])
            HASH[COUNT][MONOTYPE][PSS["childName"]] = PSS["sectionText"]

    # Set the total count of monograph sections
    HASH[COUNT][MONOTYPE][0] = PSS["i"]

def REF(DOCHAND, NODE, HASH, MONOTYPE, COUNT):
    # @DESC Parses and stores the reference element of references element.
    #
    # @DOCHAND Handle to XML document
    # @NODE Node associated with XML element
    # @HASH Handle to DrugOrderChecks object
    # @MONOTYPE Type of monograph either ProfessionalMonograph or ConsumerMonograph
    #
    # @RETURNS Nothing
    PSS = {}
    PSS["child"] = 0
    PSS["i"] = 0

    while PSS["child"] != 0:
        # Get the sub elements of the references type section
        PSS["child"] = CHILD(DOCHAND, NODE, PSS["child"])
        if PSS["child"] != 0:
            PSS["childName"] = NAME(DOCHAND, PSS["child"])
            if PSS["childName"] == "reference":
                HASH[COUNT][MONOTYPE]["references"][PSS["i"]] = GETTEXT(DOCHAND, PSS["child"])
                PSS["i"] = PSS["i"] + 1

    if PSS["i"] > 0:
        HASH[COUNT][MONOTYPE]["references"] = PSS["i"]  # if >0 means references have reference elements

def DRUGWRIT(HASH, BASE):
    # @DESC Handles writing drugDrugChecks drugDrugCheck section of the XML document
    #
    # @HASH ByRef, Hash used to store response
    # @BASE Base of output global
    #
    # @RETURNS Nothing. Stores values in output global.
    PSS = {}
    I = ""
    NODE = ""
    FIRST = ""
    SECOND = ""
    SUB = ""
    IPMON = 16
    L = ""
    PSSCLIN = ""
    PSSDRGNM = ""
    PSSCHK = {}

    SUB = "ProfessionalMonograph"

    I = ""
    while I != "":
        # If Severity equals 0 ignore this drug drug check and move onto next
        if int(HASH[I]["severity"]) == -1:
            continue

        IPMON = 16  # PMON index before starting to write references

        # A profile drug should always take precedent in the subscript over a prospective drug
        # If two prospective or two profile drugs then precedence doesn't matter
        # Set the values to default values
        FIRST = 1
        SECOND = 2

        if ISPROF(HASH[I]["drugList"][2]["orderNumber"]) == 1:
            FIRST = 2
            SECOND = 1

        # Create the node to use with subscript indirection
        NODE = "^TMP($JOB,BASE,\"OUT\",\"DRUGDRUG\",SEVCODE(HASH[I,\"severity\"])"
        NODE = NODE + ",HASH[I,\"drugList\",FIRST,\"drugName\"),HASH[I,\"drugList\",FIRST,\"orderNumber\"),I)"

        # Value on right of = should be as follows
        # 2nd Order Number^2nd Drug IEN^1st Drug IEN^2nd Drug Name^CPRS Order Number^Package
        PSS["value"] = HASH[I]["drugList"][SECOND]["orderNumber"] + "^" + HASH[I]["drugList"][SECOND]["ien"] + "^" + HASH[I]["drugList"][FIRST]["ien"]
        PSS["value"] = PSS["value"] + "^" + HASH[I]["drugList"][SECOND]["drugName"] + "^" + HASH[I]["drugList"][FIRST]["cprsOrderNumber"] + "^" + HASH[I]["drugList"][FIRST]["package"]
        @NODE = PSS["value"]

        if CHKHASH(HASH, I, "severity"):
            @NODE["SEV"] = HASH[I]["severity"]
        if CHKHASH(HASH, I, "shortText"):
            @NODE["SHORT"] = HASH[I]["shortText"]
        if CHKHASH(HASH, I, "interaction"):
            @NODE["INT"] = HASH[I]["interaction"]
        if CHKHASH(HASH, I, SUB, "clinicalEffects"):
            # prevent string length error due to message being duplicated when same drug ordered multiple times
            PSSCLIN = HASH[I]["ProfessionalMonograph"]["clinicalEffects"]
            PSSDRGNM = HASH[I]["drugList"][FIRST]["drugName"]
            if (PSSDRGNM != "" and PSSCLIN != ""):
                # Do not repeat text if drug is ordered multiple times
                if PSSCHK[PSSDRGNM][PSSCLIN[:500]] is True:
                    continue
                # save text for drug if being checked again in this session
                PSSCHK[PSSDRGNM][PSSCLIN[:500]] = True
                @NODE["CLIN"] = HASH[I]["ProfessionalMonograph"]["clinicalEffects"]

        # Write professional monograph
        # Professional monograph MUST be in order specified by code with a single
        # line of space between each section
        if CHKHASH(HASH, I, SUB, 0):
            @NODE["PMON"] = HASH[I]["ProfessionalMonograph"][0]
        if CHKHASH(HASH, I, SUB, "disclaimer"):
            @NODE["PMON", 1, 0] = HASH[I]["ProfessionalMonograph"]["disclaimer"]
            @NODE["PMON", 2, 0] = ""
        if CHKHASH(HASH, I, SUB, "monographTitle"):
            @NODE["PMON", 3, 0] = HASH[I]["ProfessionalMonograph"]["monographTitle"]
            @NODE["PMON", 4, 0] = ""
        if CHKHASH(HASH, I, SUB, "severityLevel"):
            @NODE["PMON", 5, 0] = HASH[I]["ProfessionalMonograph"]["severityLevel"]
            @NODE["PMON", 6, 0] = ""
        if CHKHASH(HASH, I, SUB, "mechanismOfAction"):
            @NODE["PMON", 7, 0] = HASH[I]["ProfessionalMonograph"]["mechanismOfAction"]
            @NODE["PMON", 8, 0] = ""
        if CHKHASH(HASH, I, SUB, "clinicalEffects"):
            @NODE["PMON", 9, 0] = HASH[I]["ProfessionalMonograph"]["clinicalEffects"]
            @NODE["PMON", 10, 0] = ""
        if CHKHASH(HASH, I, SUB, "predisposingFactors"):
            @NODE["PMON", 11, 0] = HASH[I]["ProfessionalMonograph"]["predisposingFactors"]
            @NODE["PMON", 12, 0] = ""
        if CHKHASH(HASH, I, SUB, "patientManagement"):
            @NODE["PMON", 13, 0] = HASH[I]["ProfessionalMonograph"]["patientManagement"]
            @NODE["PMON", 14, 0] = ""
        if CHKHASH(HASH, I, SUB, "discussion"):
            @NODE["PMON", 15, 0] = HASH[I]["ProfessionalMonograph"]["discussion"]
            @NODE["PMON", 16, 0] = ""
        if CHKHASH(HASH, I, SUB, "references"):
            L = ""
            while L != "":
                L = next(HASH[I]["ProfessionalMonograph"]["references"], "")
                if L != "":
                    IPMON = IPMON + 1
                    @NODE["PMON", IPMON, 0] = HASH[I]["ProfessionalMonograph"]["references"][L]
            IPMON = IPMON + 1
            @NODE["PMON", IPMON, 0] = ""

        if CHKHASH(HASH, I, "monographSource"):
            IPMON = IPMON + 1
            @NODE["PMON", IPMON, 0] = COPYRITE(HASH[I]["monographSource"])

        # Write consumer monograph
        # consumer monograph NOT currently available TODO add when available
        I = I + 1

def CHKHASH(HASH, CNT, SUB1, SUB2=None):
    # CHECKS if hash node has data
    # inputs: HASH-ARRAY PASSED IN BY REF
    #         CNT-The hash number passed in
    #         SUB1--First subscript
    #         SUB2 (OPTIONAL)-SECOND SUBSCRIPT
    # RETURNS LENGTH OF DATA IN NODE OR 0 IF DOESN'T EXIST
    if SUB2 is not None:
        return len(HASH[CNT][SUB1][SUB2])
    return len(HASH[CNT][SUB1])

def TRANSEV(SEV):
    # @DESC Translates the severity attribute returned by the XML into
    # a VistA specific severity
    #
    # @SEV Severity returned from the XML
    #
    # @RETURNS VistA specific severity
    #
    # DrugDrugChecks with an FDB severity of "Contraindicated Drug Combination"
    # will be displayed as "Critical".
    # DrugDrugChecks with an FDB severity of "Severe Interaction" will be displayed as "Significant".
    # IMPORTANT:
    # DrugDrugChecks that are not 'critical' or 'significant' are not included in output global.
    return "Critical" if SEV == "Contraindicated Drug Combination" else "Significant" if SEV == "Severe Interaction" else -1

def SEVCODE(SEV):
    # @DESC Returns the proper severity code depending on the VistA specific severity
    #
    # @SEV VistA specific severity.
    #
    # @RETURNS Returns severity code. 'C' for Critical. 'S' for Significant.
    return "C" if SEV == "Critical" else "S" if SEV == "Significant" else ""

def COPYRITE(SOURCE):
    # @DESC Returns correct copyright disclaimer for FDB OR VA PBM in format
    # @Copyright [Current Year] First DataBank, Inc.
    # @Information provided by VA PBM-SHG
    # @INPUT: source FDB OR Custom
    # @RETURNS FDB copyright OR va pbm information
    PSS = {}
    PSS["fileManYear"] = str(get_current_year())
    PSS["year"] = int(PSS["fileManYear"]) + 1700

    if SOURCE == "Custom":
        PSS["source"] = "Information provided by VA PBM-SHG"
    else:
        PSS["source"] = "Copyright " + str(PSS["year"]) + " First Databank, Inc."
    
    return PSS["source"]

# Helper functions (not present in the original code)

def CHILD(DOCHAND, NODE, CHILD):
    # Helper function to get the child element at a given index
    # Not present in the original code
    return 0  # Placeholder implementation

def NAME(DOCHAND, CHILD):
    # Helper function to get the name of an XML element
    # Not present in the original code
    return ""  # Placeholder implementation

def PARSEMSG(DOCHAND, NODE, HASH, COUNT):
    # Helper function to parse the message section
    # Not present in the original code
    pass  # Placeholder implementation

def GETTEXT(DOCHAND, CHILD):
    # Helper function to get the text of an XML element
    # Not present in the original code
    return ""  # Placeholder implementation

def DRUGLIST(DOCHAND, NODE, HASH, COUNT):
    # Helper function to handle parsing of the drug list
    # Not present in the original code
    pass  # Placeholder implementation

def ISPROF(ORDER_NUMBER):
    # Helper function to check if the given order number is a profile drug
    # Not present in the original code
    return False  # Placeholder implementation

def ERRMSG(SUB, DRUG_NAME, ORDER_NUMBER, WARNFLG):
    # Helper function to generate an error message
    # Not present in the original code
    return ""  # Placeholder implementation

def get_current_year():
    # Helper function to get the current year
    # Not present in the original code
    import datetime
    return datetime.datetime.now().year

# Main code
DOCHAND = None  # Placeholder value
NODE = None  # Placeholder value
BASE = None  # Placeholder value

DRUGDRUG(DOCHAND, NODE, BASE)