def HLP(PSSFILE, LIST):
    """
    PSSFILE - File number for which the user would like the description.
    LIST - Subscript of ^TMP array in the form ^TMP($J,LIST,1)=HELP TEXT.
    """
    if not LIST:
        return
    ^TMP($J, LIST) = {}
    if PSSFILE and int(PSSFILE) <= 0:
        ^TMP($J, LIST, 0) = "-1^NO DATA FOUND"
        return
    X = $$GET1^DID(PSSFILE, "", "", "NAME", "", "")
    ^TMP($J, LIST, 1) = "Answer with " + X