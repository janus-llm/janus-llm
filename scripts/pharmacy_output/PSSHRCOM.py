def PARSEMSG(DOCHAND, NODE, HASH, COUNT):
    """
    Parses the message XML element and stores severity, type, drugName and text in HASH parameter
    :param DOCHAND: Handle to XML document
    :param NODE: Node associated with XML element
    :param HASH: Passed by ref. Used to store return values
    :param COUNT: Count of messages
    :return: Nothing, Values stored in HASH variable
    """
    PSS = {}
    PSS["child"] = 0

    while PSS["child"] := CHILD^MXMLDOM(DOCHAND, NODE, PSS["child"]) > 0:
        NAME = NAME^MXMLDOM(DOCHAND, PSS["child"])

        if NAME == "drug":
            PARSEDRG(DOCHAND, PSS["child"], HASH, COUNT)
        elif NAME == "severity":
            HASH[COUNT]["severity"] = GETTEXT(DOCHAND, PSS["child"])
        elif NAME == "type":
            HASH[COUNT]["type"] = GETTEXT(DOCHAND, PSS["child"])
        elif NAME == "drugName":
            HASH[COUNT]["drugName"] = GETTEXT(DOCHAND, PSS["child"])
        elif NAME == "text":
            HASH[COUNT]["text"] = GETTEXT(DOCHAND, PSS["child"])

def DRUGLIST(DOCHAND, NODE, HASH, COUNT):
    """
    Handles reading the interacted drug list and stores to a Hash
    :param DOCHAND: Handle to XML document
    :param NODE: Represents the interactedDrugList XML element
    :param HASH: Passed by ref. Used to store return values
    :param COUNT: Count of drugs
    :return: Nothing, Values stored in HASH variable
    """
    PSS = {}
    VAL = ""
    DRUGS = {}
    PSS["child"] = 0
    PSS["interactedCount"] = 1

    while PSS["child"] := CHILD^MXMLDOM(DOCHAND, NODE, PSS["child"]) > 0:
        DRUGS = {}
        PARSEDRG(DOCHAND, PSS["child"], DRUGS, PSS["interactedCount"])
        VAL = ""

        while VAL := ORDER^DRUGS:
            HASH[COUNT]["drugList"][PSS["interactedCount"]]["vuid"] = DRUGS[VAL]["vuid"]
            HASH[COUNT]["drugList"][PSS["interactedCount"]]["ien"] = DRUGS[VAL]["ien"]
            HASH[COUNT]["drugList"][PSS["interactedCount"]]["gcn"] = DRUGS[VAL]["gcn"]
            HASH[COUNT]["drugList"][PSS["interactedCount"]]["orderNumber"] = DRUGS[VAL]["orderNumber"]
            HASH[COUNT]["drugList"][PSS["interactedCount"]]["drugName"] = DRUGS[VAL]["drugName"]
            HASH[COUNT]["drugList"][PSS["interactedCount"]]["cprsOrderNumber"] = DRUGS[VAL].get("cprsOrderNumber", "")
            HASH[COUNT]["drugList"][PSS["interactedCount"]]["package"] = DRUGS[VAL].get("package", "")

        PSS["interactedCount"] += 1

def PARSEDRG(DOCHAND, NODE, HASH, COUNT):
    """
    Parses a drug element and stores values in HASH parameter
    :param DOCHAND: Handle to XML document
    :param NODE: Node associated with XML element
    :param HASH: Passed by ref. Used to store return values.
    :param COUNT: Count of drugs
    :return: Nothing, Values stored in HASH values
    """
    HASH[COUNT]["vuid"] = VALUE^MXMLDOM(DOCHAND, NODE, "vuid")
    HASH[COUNT]["ien"] = VALUE^MXMLDOM(DOCHAND, NODE, "ien")
    HASH[COUNT]["gcn"] = VALUE^MXMLDOM(DOCHAND, NODE, "gcnSeqNo")
    HASH[COUNT]["drugName"] = VALUE^MXMLDOM(DOCHAND, NODE, "drugName")

    orderNumber = VALUE^MXMLDOM(DOCHAND, NODE, "orderNumber")
    HASH[COUNT]["orderNumber"] = orderNumber.split("|")[0]
    HASH[COUNT]["cprsOrderNumber"] = orderNumber.split("|")[1]
    HASH[COUNT]["package"] = orderNumber.split("|")[2]

def UPPER(PSSTEXT):
    """
    Converts lowercase characters to uppercase
    :param PSSTEXT: Text to be converted
    :return: Text in all UPPPERCASE
    """
    PSS = {}
    PSS["lower"] = "abcdefghijklmnopqrstuvwxyz"
    PSS["upper"] = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    PSS["upperText"] = PSSTEXT.translate(str.maketrans(PSS["lower"], PSS["upper"]))
    return PSS["upperText"]

def GETTEXT(DOCHAND, NODE):
    """
    Gets text from XML element as a single string
    :param DOCHAND: Handle to XML document
    :param NODE: Node associated with XML element
    :return: Text of XML element as a single string
    """
    TEXT = []
    TEXT^MXMLDOM(DOCHAND, NODE, TEXT)
    return UNPARSE(TEXT)

def UNPARSE(ARRY):
    """
    Creates a single string from an array
    :param ARRY: Array to be looped through for text
    :return: Text of array as a single string
    """
    return "".join(ARRY)

def ATRIBUTE(NAME, VALUE):
    """
    Builds a valid encoded attribute from the name/value pair passed in
    :param NAME: The left side of the "name=value" relationship
    :param VALUE: The right side of the "name=value" relationship
    :return: A valid/encoded name value pair
    """
    QT = '"'
    return f"{NAME}={QT}{VALUE}{QT}"

def ISPROF(ORDERNUM):
    """
    Determines if a drug is a profile drug according to its orderNumber
    :param ORDERNUM: Order number of the drug
    :return: 1 if is a profile, 0 if not a profile
    """
    return "PROFILE" in UPPER(ORDERNUM)

def STACK():
    """
    Prints a stack trace
    :return: Nothing
    """
    for PSSLOOP in range(0, $STACK(-1)+1):
        print(f"Context level: {PSSLOOP}\tContext type: {$STACK(PSSLOOP)}")
        print(f"Current place: {$STACK(PSSLOOP, 'PLACE')}")
        print(f"Current source: {$STACK(PSSLOOP, 'MCODE')}")
        print()