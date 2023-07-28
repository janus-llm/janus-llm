def CNVA():
    """
    Create non-VA med cross-reference in Pharmacy Patient file.
    """
    import os

    IND = None
    MSG = None
    NAME = None
    RESULT = None
    XREF = {}

    os.system("BMES^XPDUTL('Creating Pharmacy Patient non-VA med cross-reference.')")

    XREF["FILE"] = 55
    XREF["WHOLE KILL"] = "K ^PXRMINDX(""55NVA"")"
    XREF["TYPE"] = "MU"
    XREF["SHORT DESCR"] = "Clinical Reminders index."
    XREF["DESCR"] = [
        "This cross-reference builds two indexes, one for finding",
        "all patients with a pharmacy orderable item and one for",
        "finding all the pharmacy orderable items a patient has. The indexes are",
        "stored in the Clinical Reminders index global as:",
        " ^PXRMINDX(""55NVA"",""IP"",POI,DFN,START DATE,STOP DATE,DAS)",
        " ^PXRMINDX(""55NVA"",""PI"",DFN,POI,START DATE,STOP DATE,DAS)",
        "respectively. POI is the pharmacy orderable item.",
        "If there is no START DATE then the DOCUMENTED DATE is used in its place.",
        "For all the details, see the Clinical Reminders Index Technical Guide/Programmer's Manual."
    ]
    XREF["USE"] = "ACTION"
    XREF["EXECUTION"] = "R"
    XREF["ACTIVITY"] = "IR"
    XREF["ROOT FILE"] = 55.05
    XREF["NAME"] = "ACRNVA"
    XREF["SET"] = "D SNVA^PSOPXRMU(.X,.DA)"
    XREF["KILL"] = "D KNVA^PSOPXRMU(.X,.DA)"
    XREF["VAL"] = {
        1: 0.01,
        2: 11,
        3: 8,
        4: 6
    }

    os.system("CREIXN^DDMOD(.XREF,'k',.RESULT,'','MSG')")

    if RESULT == "":
        os.system("DCERRMSG^PXRMP12I(.MSG,.XREF)")

def CPSPA():
    """
    Create cross-references for Pharmacy Patient.
    """
    import os

    IND = None
    MSG = None
    NAME = None
    RESULT = None
    XREF = {}

    os.system("BMES^XPDUTL('Creating Pharmacy Patient cross-references.')")

    XREF["FILE"] = 55
    XREF["SET CONDITION"] = "S X=$$PATCH^XPDUTL('PXRM*1.5*12')"
    XREF["KILL CONDITION"] = "S X=$$PATCH^XPDUTL('PXRM*1.5*12')"
    XREF["WHOLE KILL"] = "K ^PXRMINDX(55)"
    XREF["TYPE"] = "MU"
    XREF["SHORT DESCR"] = "Clinical Reminders index."
    XREF["DESCR"] = [
        "This cross-reference builds two indexes, one for finding",
        "all patients with a particular drug and one for",
        "finding all the drugs a patient has. The indexes are",
        "stored in the Clinical Reminders index global as:",
        " ^PXRMINDX(55,'IP',DRUG,DFN,START,STOP,DAS)",
        " ^PXRMINDX(55,'PI',DFN,DRUG,START,STOP,DAS)",
        "respectively. START is the start date and STOP is the stop date.",
        "For all the details, see the Clinical Reminders Index Technical Guide/Programmer's Manual."
    ]
    XREF["USE"] = "ACTION"
    XREF["EXECUTION"] = "R"
    XREF["ACTIVITY"] = "IR"

    # Unit Dose
    XREF["ROOT FILE"] = 55.06
    XREF["NAME"] = "ACRUD"
    XREF["SET"] = "D SPSPA^PSJXRFS(.X,.DA,'UD')"
    XREF["KILL"] = "D KPSPA^PSJXRFK(.X,.DA,'UD')"
    XREF["VAL"] = {
        1: 10,
        2: 34
    }

    os.system("CREIXN^DDMOD(.XREF,'k',.RESULT,'','MSG')")

    if RESULT == "" and os.path.exists("DCERRMSG^PXRMP12I"):
        os.system("DCERRMSG^PXRMP12I(.MSG,.XREF)")

    # IV node
    XREF["ROOT FILE"] = 55.01
    XREF["NAME"] = "ACRIV"
    XREF["SET"] = "D SPSPA^PSJXRFS(.X,.DA,'IV')"
    XREF["KILL"] = "D KPSPA^PSJXRFK(.X,.DA,'IV')"
    XREF["VAL"] = {
        1: 0.02,
        2: 0.03
    }

    os.system("CREIXN^DDMOD(.XREF,'k',.RESULT,'','MSG')")

    if RESULT == "" and os.path.exists("DCERRMSG^PXRMP12I"):
        os.system("DCERRMSG^PXRMP12I(.MSG,.XREF)")

def POST():
    """
    Post-init
    """
    CNVA()
    CPSPA()