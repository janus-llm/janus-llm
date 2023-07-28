def PSS(PSSIEN, PSSTXT, LIST):
    # PSSIEN - INTERNAL ENTRY NUMBER (optional)
    # PSSTXT - Free Text site name (optional)
    # LIST: Subscript name used in ^TMP global [REQUIRED]
    import os
    import sys
    import subprocess

    # Variable Definitions
    X = None
    DA = None
    DR = None
    DIC = None
    DIQ = None

    if PSSIEN == "" and PSSTXT == "":
        return
    if LIST == "":
        return

    # Clean up global variables
    subprocess.run(["KILL", "^TMP($J," + LIST + ")"])
    DA = None
    subprocess.run(["KILL", "^UTILITY(\"DIQ1\",$J)"])
    DIQ = None

    if PSSIEN != "":
        DA = PSSIEN
        if not os.path.exists("^PS(59.7," + DA + ",0)"):
            RET0()
            return

    if PSSTXT != "" and PSSIEN <= 0 and not os.path.exists("^PS(59.7,\"B\"," + PSSTXT + ")"):
        RET0()
        return

    if PSSTXT != "" and DA <= 0:
        DA = os.popen("FIND ^PS(59.7,\"B\"," + PSSTXT + ")").read()
        DA = DA.strip()
        if DA == "":
            DA = 0
        else:
            DA = int(DA)

    subprocess.run(["KILL", "^UTILITY(\"DIQ1\",$J)"])
    DIC = 59.7
    DR = ".01;40.1;49.99;81"
    DIQ = "IE"
    subprocess.run(["EN^DIQ1"])

    if not os.path.exists("^UTILITY(\"DIQ1\",$J)"):
        RET0()
        return

    if PSSTXT == "":
        PSSTXT = os.popen("GET VALUE ^UTILITY(\"DIQ1\",59.7," + DA + ",.01,\"E\")").read()
        PSSTXT = PSSTXT.strip()

    for X in [40.1, 49.99, 81]:
        value = os.popen("GET VALUE ^UTILITY(\"DIQ1\",59.7," + DA + "," + str(X) + ",\"I\")").read()
        value = value.strip()
        ^TMP($J, LIST, DA, X) = value

    value = os.popen("GET VALUE ^UTILITY(\"DIQ1\",59.7," + DA + ",40.1,\"E\")").read()
    value = value.strip()
    if value != "":
        value = ^TMP($J, LIST, DA, 40.1) + "^" + value
    else:
        value = ""
    ^TMP($J, LIST, DA, 40.1) = value

    value = os.popen("GET VALUE ^UTILITY(\"DIQ1\",59.7," + DA + ",81,\"E\")").read()
    value = value.strip()
    if value != "":
        value = ^TMP($J, LIST, DA, 81) + "^" + value
    else:
        value = ""
    ^TMP($J, LIST, DA, 81) = value

    ^TMP($J, LIST, "B", PSSTXT, DA) = ""

    # Clean up all variables
    PSSIEN = None
    DA = None
    X = None
    PSSTXT = None
    DR = None
    DIC = None
    subprocess.run(["KILL", "^UTILITY(\"DIQ1\",$J)"])
    return

def RET0():
    # return no data
    ^TMP($J, LIST, 0) = "-1^NO DATA FOUND"
    return