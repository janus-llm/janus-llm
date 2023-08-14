def PSSHRENV():
    PSSMGPNM = ""
    PSSMGPOR = ""
    PSSMGPDS = ""
    PSSMGPRS = ""
    PSSMGPMY = ""
    PSSMGPNM = ""
    PSSMGPSL = ""
    PSSMGPQT = ""
    PSSMGPTP = ""
    DTOUT = ""
    DUOUT = ""
    Y = ""
    XPDABORT = ""
    PSSMGPAR = ""

    # If mail group already exists quit.
    if FIND1("3.8", "", "X", "PSS ORDER CHECKS", "B"):
        return

    PSSMGPAR = [
        "A 'PSS ORDER CHECKS' Mail Group is now being created. Mail Group members will",
        "receive various notifications that impact Enhanced Order Checks (drug-drug",
        "interactions, duplicate therapy and dosing) introduced with PRE V. 0.5. Please",
        "enter the Pharmacy ADPAC or a designee to be the Mail Group Organizer.",
        "",
        "To continue this install, you must now enter a Mail Group organizer.",
        ""
    ]
    MES(PSSMGPAR)

    DIC = 200
    DIC[0] = "QEAMZ"
    DIC["A"] = "Enter Mail Group Organizer: "
    # Abort install if user does not enter a coordinator
    Y = DIC()
    if DTOUT or DUOUT or not Y:
        PSSMGPAR = ""
        XPDABORT = 2
        return

    PSSMGPOR = Y
    PSSMGPMY[Y] = ""

    PSSMGPNM = "PSS ORDER CHECKS"
    PSSMGPTP = 0
    PSSMGPSL = 0
    PSSMGPQT = 1

    PSSMGPDS = [
        "Members of this mail group will receive various notifications that impact",
        "Enhanced Order Checks (drug-drug interactions, duplicate therapy and dosing",
        "checks) introduced with PRE V. 0.5 utilizing a COTS database."
    ]

    PSSMGPRS = MG(PSSMGPNM, PSSMGPTP, PSSMGPOR, PSSMGPSL, PSSMGPMY, PSSMGPDS, PSSMGPQT)

    if not PSSMGPRS:
        BMES(" ")
        BMES("Unable to create PSS ORDER CHECKS Mail Group, aborting install.")
        XPDABORT = 2

    PSSMGPAR = ""
    return

# Helper functions
def FIND1(a, b, c, d, e):
    # Code translated elsewhere
    pass

def MES(a):
    # Code translated elsewhere
    pass

def DIC():
    # Code translated elsewhere
    pass

def BMES(a):
    # Code translated elsewhere
    pass

def MG(a, b, c, d, e, f, g):
    # Code translated elsewhere
    pass