def PEPSPOST(DOCHAND, XML):
    """
    Sends an HTTP request to PEPS as a POST

    :param DOCHAND: Handle to XML document
    :param XML: XML request as string
    :return: A handle to response XML document
             1 for success, 0 for failure
    """

    PSS = {}
    PSSERR = {}
    $ETRAP = "ERROR"

    PSS["server"] = "PEPS"
    PSS["webserviceName"] = "ORDER_CHECKS"
    PSS["path"] = "ordercheck"

    PSS["parameterName"] = "xmlRequest"
    PSS["parameterValue"] = XML

    PSS["restObject"] = GETREST(PSS["webserviceName"], PSS["server"])
    if len(^TMP($JOB, "OUT", "EXCEPTION")) > 0:
        return 0

    PSS["restObject"].InsertFormData(PSS["parameterName"], PSS["parameterValue"])
    if len(^TMP($JOB, "OUT", "EXCEPTION")) > 0:
        return 0

    PSS["postResult"] = POST(PSS["restObject"], PSS["path"], PSSERR)
    if len(^TMP($JOB, "OUT", "EXCEPTION")) > 0:
        return 0

    if PSS["postResult"]:
        PSS["result"] = gov.va.med.pre.ws.XMLHandler.getHandleToXmlDoc(PSS["restObject"].HttpResponse.Data, DOCHAND)
    else:
        ^TMP($JOB, "OUT", "EXCEPTION") = "Unable to make http request."
        PSS["result"] = 0

    return PSS["result"]

def ERROR():
    """
    Handles error during request to PEPS via webservice.
    Depends on GLOBAL variable PSSERR to be set in previous call.
    """

    ERRARRAY = {}

    if PSSERR == "":
        PSSERR = EOFAC()

    ERR2ARR(PSSERR, ERRARRAY)

    ^TMP($JOB, "OUT", "EXCEPTION") = GETTEXT(ERRARRAY)

    if PSSFDBRT and len(^TMP($JOB, "OUT", "EXCEPTION")) > 0:
        PSSOUT(0) = "-1^" + ^TMP($JOB, "OUT", "EXCEPTION")
        del ^TMP($JOB, "OUT", "EXCEPTION")

    $ECODE = ""

def GETTEXT(ERRARRAY):
    """
    Gets the error text from the array

    :param ERRARRAY: Error array stores error in format defined by web service product.
    :return: Error info as a single string
    """

    PSS = {}
    PSS["errorText"] = ""
    PSS["I"] = ""

    for PSS["I"] in ERRARRAY["text"]:
        PSS["errorText"] += ERRARRAY["text"][PSS["I"]]

    return PSS["errorText"]