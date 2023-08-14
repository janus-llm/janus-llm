def DRUG(XX, DFN):
    """
    Return warning labels numbers associated with this drug

    Calling method: WARN = DRUG(XX, DFN)

    Input: XX = IEN from the DRUG file (50) - REQUIRED
           DFN = IEN from the PATIENT file (2) - OPTIONAL

    Output: WARN = List of warning numbers, separated by commas, associated with this drug. 
                   Warning numbers from the new data source will be followed by an "N".
    """
    PSSWRN = ""
    PSSWSITE = int(next(iter(PS[59.7])))
    if PS[59.7][PSSWSITE][10][9] == "N":
        WARNLST()
    if PSSWRN == "":
        PSSWRN = PS[DRUG][XX][0][8]
    CHECKLST()
    CHECK20()
    return PSSWRN


def CHECK20():
    """
    WARNING LABEL 20 - 'DO NOT TRANSFER' REQUIRED FOR CONTROLLED SUBSTANCES
    """
    DEA = PS[DRUG][XX][0][3]
    if DEA == "":
        return
    if DEA[0] not in "12345":
        return
    if f',{",".join(PSSWRN.split(",")[:5])},'".find(",20,") != -1:
        return
    if len(PSSWRN.split(",")) < 5:
        PSSWRN = "20" if PSSWRN == "" else f"{PSSWRN},20"
        return
    PSSWRN = f"{','.join(PSSWRN.split(',')[:4])},20,{','.join(PSSWRN.split(',')[4:])}"
    for i in range(6, len(PSSWRN.split(","))):
        if PSSWRN.split(",")[i] == "20":
            PSSWRN = f"{','.join(PSSWRN.split(',')[:i])}"
            if PSSWRN.split(",")[i+1:]:
                PSSWRN = f"{PSSWRN},{','.join(PSSWRN.split(',')[i+1:])}{','.join(PSSWRN.split(',')[i+1:])}"
            break


def WARNLST():
    """
    GET WARNING LIST FROM NEW DATA SOURCE OR USER-DEFINED NEW WARNING LABEL LIST
    """
    global PSSWRN
    PSSWRN = PS[DRUG][XX]["WARN"]
    if PSSWRN != "":
        return
    PSOPROD = PS[DRUG][XX]["ND"][3]
    if PSOPROD == "":
        return
    GCNSEQNO = DIQ[50.68][PSOPROD][11]
    if GCNSEQNO == "":
        return
    NEWWARN = {}
    for I in PS[50.627]["B"][GCNSEQNO]:
        if I:
            NEWWARN = PS[50.627][I]
            if NEWWARN[0] == GCNSEQNO:
                SEQ = int(NEWWARN[3])
                if SEQ > 0:
                    NEWWARN[SEQ] = int(NEWWARN[2])
    for SEQ in NEWWARN:
        if SEQ:
            PSSWRN = f"{PSSWRN},{NEWWARN[SEQ]}N"


def WARN54():
    """
    VERIFY ENTRY EXISTS. IF NOT, REMOVE FROM WARNING LIST
    """
    global PSSWRN
    if not PS[54][WARN][1]:
        PSSWRN = f"{','.join(PSSWRN.split(',')[:I])}{'' if I == 1 else ','}{','.join(PSSWRN.split(',')[I+1:])}"
        I -= 1


def NEWWARN():
    """
    """
    global PSSWRN
    if not PS[50.625][WARN][1]:
        PSSWRN = f"{','.join(PSSWRN.split(',')[:I])}{'' if I == 1 else ','}{','.join(PSSWRN.split(',')[I+1:])}"
        I -= 1


def CHECKLST():
    """
    """
    global PSSWRN
    for I in range(1, len(PSSWRN.split(","))):
        WARN = PSSWRN.split(",")[I]
        if WARN:
            if "N" not in WARN:
                WARN54()
            else:
                WARN = int(WARN.split("N")[0])
                GENDER()
                if WARN:
                    NEWWARN()
    if PSSWRN[-1] == ",":
        PSSWRN = PSSWRN[:-1]


def GENDER():
    """
    """
    if not DFN:
        return
    GENDER = DIQ[50.625][WARN][2]
    if GENDER == "":
        return
    if GENDER not in ["F", "M"]:
        return
    SEX = DIQ[2][DFN][.02]
    if not SEX:
        return
    if SEX not in ["F", "M"]:
        return
    if SEX != GENDER and DIQ[50][XX][8.2] == "N":
        PSSWRN = f"{','.join(PSSWRN.split(',')[:I])}{'' if I == 1 else ','}{','.join(PSSWRN.split(',')[I+1:])}"


def WTEXT(WARN, LAN):
    """
    """
    TEXT = ""
    if "N" not in WARN:
        if LAN == 2:
            if PS[54][WARN][3]:
                TEXT = PS[54][WARN][3]
        if TEXT == "":
            for JJJ in PS[54][WARN][1]:
                if JJJ:
                    TEXT = f"{TEXT} {PS[54][WARN][1][JJJ][0]}"
    if "N" in WARN:
        if LAN != 2:
            PSOWRNN = int(WARN.split("N")[0])
            if PS[50.625][PSOWRNN]:
                TEXT = ""
                for JJJ in PS[50.625][PSOWRNN][1]:
                    if JJJ:
                        TEXT = f"{TEXT} {PS[50.625][PSOWRNN][1][JJJ][0]}"
        else:
            PSOWRNN = int(WARN.split("N")[0])
            if PS[50.626][PSOWRNN]:
                TEXT = ""
                for JJJ in PS[50.626][PSOWRNN][1]:
                    if JJJ:
                        TEXT = f"{TEXT} {PS[50.626][PSOWRNN][1][JJJ][0]}"
    return TEXT


def GENDER2():
    """
    """
    global GENDER
    GENDER = ""
    if "N" not in PSSWRN:
        for I in range(1, len(PSSWRN.split(","))):
            WARN = PSSWRN.split(",")[I]
            if WARN:
                if "N" in WARN:
                    WARN = int(WARN.split("N")[0])
                    GENDER = DIQ[50.625][WARN][2]
                    break


PSSWRNA = {
    59.7: {
        0: {},
    },
    DRUG: {
        XX: {
            0: {
                3: '',
                8: '',
            },
            'ND': {
                3: '',
            },
            'WARN': '',
        },
    },
    50.68: {
        PSOPROD: {
            11: '',
        },
    },
    50.627: {
        'B': {
            GCNSEQNO: '',
        },
    },
    54: {
        WARN: {
            3: '',
            1: {
                JJJ: {
                    0: '',
                },
            },
        },
    },
    50.625: {
        WARN: {
            2: '',
            1: {
                JJJ: {
                    0: '',
                },
            },
        },
    },
    50.626: {
        PSOWRNN: {
            1: {
                JJJ: {
                    0: '',
                },
            },
        },
    },
    2: {
        DFN: {
            .02: '',
        },
    },
    50: {
        XX: {
            8.2: '',
        },
    },
}