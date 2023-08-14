def OUT(DOCHAND, BASE):
    """
    Parses the PEPSResponse XML and stores in object

    :param DOCHAND: Handle to XML document
    :param BASE: Base of output global
    """
    PSS = {}
    PSS["rootName"] = NAME(DOCHAND, 1)

    if PSS["rootName"] == "exception":
        # Read error into hash variable
        ERREAD(DOCHAND, PSS)

        if PSS["code"] == "FDBUPDATE":
            MESSAGE = "Vendor database updates are being processed."
        elif "^TMP($J,BASE,"IN","DOSE")" in globals():
            MESSAGE = "An unexpected error has occurred."
        else:
            MESSAGE = "An unexpected error has occurred."

        ^TMP(JOB,BASE,"OUT",0) = "-1^" + MESSAGE

        # Cleanup the out.exception global
        globals()["^TMP"]($J,"OUT","EXCEPTION") = {}

    if PSS["rootName"] == "PEPSResponse":
        HNDLCK(DOCHAND, BASE)

    # Clean up after using the handle
    DELETE(DOCHAND)
    globals()["^TMP"]($J,"OUT XML") = {}


def HNDLCK(DOCHAND, BASE):
    """
    Handles the parsing of the PEPSResponse XML element

    :param DOCHAND: Handle to XML document
    :param BASE: Base of output global
    """
    PSS = {}

    # if ping get the vendor database info and exit.
    if "^TMP($J,BASE,"IN","PING")" in globals():
        globals()["^TMP"]($J,BASE,"OUT",0) = 0
        GTDBINFO(DOCHAND, BASE)
        return

    # Get handle to drugCheck XML element
    PSS["drugCheck"] = GTHANDLE(DOCHAND)
    PSS["child"] = 0

    # Loop through elements of drugCheck
    while True:
        PSS["child"] = CHILD(DOCHAND, PSS["drugCheck"], PSS["child"])
        if PSS["child"] == 0:
            break

        PSS["childName"] = NAME(DOCHAND, PSS["child"])

        # Build executable string
        PSS["tag"] = SELTAG(PSS["childName"])
        PSS["executable"] = "DO " + PSS["tag"] + "(DOCHAND,PSS["child"],BASE)"

        exec(PSS["executable"])

    # Set top level node to 1 or 0
    if len(globals()["^TMP"]($J,BASE,"OUT")) > 1:
        globals()["^TMP"]($J,BASE,"OUT",0) = 1
    if len(globals()["^TMP"]($J,BASE,"OUT")) < 10:
        globals()["^TMP"]($J,BASE,"OUT",0) = 0


def GTDBINFO(DOCHAND, BASE):
    """
    Get the Vendor database info.

    :param DOCHAND: Handle to XML document
    :param BASE: Base of output global
    """
    PSS = {}
    PSS["child"] = 0
    PSS["childName"] = ""

    # get <Header> child
    while True:
        PSS["child"] = CHILD(DOCHAND, 1, PSS["child"])
        PSS["childName"] = NAME(DOCHAND, PSS["child"])
        if PSS["childName"] == "Header":
            break

    PSS["child"] = 0

    # get <PEPSVersion> child of <Header> element
    while True:
        PSS["child"] = CHILD(DOCHAND, PSS["child"], PSS["child"])
        PSS["childName"] = NAME(DOCHAND, PSS["child"])
        if PSS["childName"] == "PEPSVersion":
            break

    globals()["^TMP"]($J,BASE,"OUT","difIssueDate") = VALUE(DOCHAND, PSS["child"], "difIssueDate")
    globals()["^TMP"]($J,BASE,"OUT","difBuildVersion") = VALUE(DOCHAND, PSS["child"], "difBuildVersion")
    globals()["^TMP"]($J,BASE,"OUT","difDbVersion") = VALUE(DOCHAND, PSS["child"], "difDbVersion")
    globals()["^TMP"]($J,BASE,"OUT","customIssueDate") = VALUE(DOCHAND, PSS["child"], "customIssueDate")
    globals()["^TMP"]($J,BASE,"OUT","customBuildVersion") = VALUE(DOCHAND, PSS["child"], "customBuildVersion")
    globals()["^TMP"]($J,BASE,"OUT","customDbVersion") = VALUE(DOCHAND, PSS["child"], "customDbVersion")


def GTHANDLE(DOCHAND):
    """
    Get handle to drugCheck element from PEPSResponse element

    :param DOCHAND: Handle to XML document
    :return: Handle to drugCheck XML element
    """
    PSS = {}
    PSS["child"] = 0

    # Get next child of root element
    while True:
        PSS["child"] = CHILD(DOCHAND, 1, PSS["child"])
        PSS["childName"] = NAME(DOCHAND, PSS["child"])
        if PSS["childName"] == "Body":
            PSS["drugCheckElement"] = CHILD(DOCHAND, PSS["child"])
            break

    return PSS["drugCheckElement"]


def SELTAG(NAME):
    """
    Returns the appropriate tag to handle the XML element

    :param NAME: Name of the current XML element
    :return: Returns the appropriate tag to handle the XML element
    """
    if NAME == "drugsNotChecked":
        return "DRGNTCK^PSSHRQ23"

    if NAME == "drugDrugChecks":
        return "DRUGDRUG^PSSHRQ21"

    if NAME == "drugTherapyChecks":
        return "THERAPY^PSSHRQ22"

    if NAME == "drugDoseChecks":
        return "DRGDOSE^PSSHRQ23"


def ALTERROR(BASE):
    """
    Handles alternate PEPS errors like being unable to connect to PEPS.
    Reads info from global in format

    ^TMP($JOB,"OUT","EXCEPTION")=MESSAGE

    :param BASE: Base of global to be written to
    """
    globals()["^TMP"]($J,BASE,"OUT",0) = "-1^Vendor Database cannot be reached."

    # Cleanup the out.exception global
    globals()["^TMP"]($J,"OUT","EXCEPTION") = {}


def ERREAD(DOCHAND, HASH):
    """
    Handles parsing the exception XML element and storing it in a hash variable

    :param DOCHAND: Handle to XML document
    :param HASH: ByRef, Hash variable used to store error info
    """
    PSS = {}
    PSS["child"] = 0

    # Get next child of root element
    while True:
        PSS["child"] = CHILD(DOCHAND, 1, PSS["child"])
        PSS["childName"] = NAME(DOCHAND, PSS["child"])
        if PSS["childName"] == "code":
            HASH["code"] = GETTEXT(DOCHAND, PSS["child"])
        elif PSS["childName"] == "message":
            HASH["message"] = GETTEXT(DOCHAND, PSS["child"])


def CLEXP():
    """
    Delete Profile drug exceptions for CPRS if all Prospective drugs have exceptions
    """
    PSSPEX1 = ""
    PSSPEX2 = ""
    PSSPEXDL = 0

    if "^TMP($J,PSSRBASE,"IN","DRUGDRUG")" not in globals() and "^TMP($J,PSSRBASE,"IN","THERAPY")" not in globals():
        return

    if "^TMP($J,PSSRBASE,"OUT","EXCEPTIONS")" not in globals():
        return

    for PSSPEX1 in globals()["^TMP"]($J,PSSRBASE,"IN","PROSPECTIVE"):
        if PSSPEX1 not in globals()["^TMP"]($J,PSSRBASE,"OUT","EXCEPTIONS"):
            PSSPEXDL = 1

    if PSSPEXDL:
        CLPAR()
        return

    for PSSPEX2 in globals()["^TMP"]($J,PSSRBASE,"OUT","EXCEPTIONS"):
        if "^TMP($J,PSSRBASE,"OUT","EXCEPTIONS",PSSPEX2)" in globals() and PSSPEX2.split(";")[2] == "PROFILE":
            del globals()["^TMP"]($J,PSSRBASE,"OUT","EXCEPTIONS",PSSPEX2)


def CLPAR():
    """
    Some Exceptions exist, but not all prospective drugs have an exception
    """
    PSSPEX3 = ""
    PSSPEX4 = ""
    PSSPEX5 = ""
    PSSPEX6 = ""
    PSSPEX7 = ""
    PSSPEX8 = ""
    PSSPEXAR = {}

    for PSSPEX3 in globals()["^TMP"]($J,PSSRBASE,"OUT","EXCEPTIONS"):
        if PSSPEX3.split(";")[2] == "PROSPECTIVE":
            PSSPEXAR[PSSPEX3.split(";")[3]] = ""

    for PSSPEX6 in globals()["^TMP"]($J,PSSRBASE,"OUT","EXCEPTIONS"):
        if PSSPEX6.split(";")[2] == "PROFILE" and PSSPEX6.split(";")[3] in PSSPEXAR:
            del globals()["^TMP"]($J,PSSRBASE,"OUT","EXCEPTIONS",PSSPEX6)