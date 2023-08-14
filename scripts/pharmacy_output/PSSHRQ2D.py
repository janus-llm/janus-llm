def PARSEDSP(DOCHAND, NODE, HASH, COUNT):
    """
    Parses a dose percent element and stores values in HASH parameter
    :param DOCHAND: Handle to XML document
    :param NODE: Node associated with XML element
    :param HASH: Passed by ref. Used to store return values.
    :param COUNT: Count of drugs
    :return: Nothing, Values stored in HASH values
    """
    NAME = NAME^MXMLDOM(DOCHAND, NODE)
    if NAME^MXMLDOM(DOCHAND, NODE+1) == "databaseValue":
        HASH(COUNT, NAME, "databaseValue") = GETTEXT^PSSHRCOM(DOCHAND, NODE+1)
    if NAME^MXMLDOM(DOCHAND, NODE+2) == "doseValue":
        HASH(COUNT, NAME, "doseValue") = GETTEXT^PSSHRCOM(DOCHAND, NODE+2)
    if NAME^MXMLDOM(DOCHAND, NODE+3) == "percentError":
        HASH(COUNT, NAME, "percentError") = GETTEXT^PSSHRCOM(DOCHAND, NODE+3)
    if NAME^MXMLDOM(DOCHAND, NODE+4) == "unitOfMeasure":
        HASH(COUNT, NAME, "unitOfMeasure") = GETTEXT^PSSHRCOM(DOCHAND, NODE+4)


def WRITEDSP(NODE, HASH, COUNT, IEN, NAME, ALTNAME, ALTNODE):
    """
    Writes a dose percent element from HASH parameter to output global
    :param NODE: Node associated with XML element
    :param HASH: Passed by ref. Used to store return values.
    :param COUNT: Count of drugs
    :param IEN: 
    :param NAME: 
    :param ALTNAME: 
    :param ALTNODE: 
    :return: Nothing, Values stored in HASH values
    """
    ALTNAME = ALTNAME
    ALTNAME = ALTNAME if ALTNAME != "" else NAME
    ALTNODE = ALTNODE
    SUB = ""
    for SUB in ["databaseValue","doseValue","percentError","unitOfMeasure"]:
        if HASH(COUNT, NAME, SUB) != "":
            if ALTNODE != "":
                NODE(ALTNODE, UP^XLFSTR(ALTNAME), UP^XLFSTR(SUB), IEN) = HASH(COUNT, NAME, SUB)
            else:
                NODE(UP^XLFSTR(ALTNAME), UP^XLFSTR(SUB), IEN) = HASH(COUNT, NAME, SUB)