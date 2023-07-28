def PSSDSEXD():
    # BIR/CMF-Exceptions for Dose call Continuation ;02/24/09
    # 1.0;PHARMACY DATA MANAGEMENT;**178,206,224**;9/30/97;Build 3

    # Called from PSSDSEXC, this routine takes the results from the call to First DataBank and creates displayable TMP
    # globals for the calling applications. Typically, PSSDBASA indicates a CPRS call, and PSSDBASB indicates a pharmacy call

    # PSSDBCAR ARRAY pieces, set mostly in PSSDSAPD are described in PSSDSEXC:

    # PSSDBCAX holds the errors to show

    # CONTINUE ;;
    if PSSDBDS.get("CONTEXT", "") == "":
        PSSDBDS["CONTEXT"] = "CPRS-UD" if PSSDSWHE == 1 else "OP-UD"
    TWEAK4()
    TWEAK0()
    if PSSDBDS["CONTEXT"][:7] == "IP-IV" or PSSDBDS["CONTEXT"][:6] == "IP-UD":
        TWEAK1()
    if PSSDBDS["CONTEXT"][:7] == "CPRS-IV" or PSSDBDS["CONTEXT"][:7] == "CPRS-UD":
        TWEAK2()
    if PSSDBDS["CONTEXT"][2:5] == "IV-I":
        TWEAK3()

def TWEAK0():
    # loop through ERROR global remove/convert certain duplicates
    for PSSDWLP in ^TMP($J,PSSDBASE,"OUT","DOSE","ERROR"):
        for PSSDWL1 in ^TMP($J,PSSDBASE,"OUT","DOSE","ERROR",PSSDWLP):
            if TWEAK001(PSSDWLP,PSSDWL1):
                continue
            if TWEAK01(PSSDWLP,PSSDWL1):
                continue
            if TWEAK02(PSSDWLP,PSSDWL1):
                continue
            if TWEAK03(PSSDWLP,PSSDWL1):
                continue
            if TWEAK04(PSSDWLP,PSSDWL1):
                continue

def TWEAK001(PSSDWLP,PSSDWL1):
    return TWEAK27(PSSDWLP,PSSDWL1)

def TWEAK01(PSSDWLP,PSSDWL1):
    REASON = ^TMP($J,PSSDBASE,"OUT","DOSE","ERROR",PSSDWLP,PSSDWL1,"TEXT").split(".")[0]
    FLAG, FLAG[1] = 0, 0
    if REASON == "Weight required":
        if PSSDBCAR[PSSDWLP].split("^")[5] == 1:
            del ^TMP($J,PSSDBASE,"OUT","DOSE","ERROR",PSSDWLP,PSSDWL1)
            FLAG = 1
        else:
            MESSAGE = ^TMP($J,PSSDBASE,"OUT","DOSE","ERROR",PSSDWLP,PSSDWL1,"MSG")
            PSSDWLX = PSSDWL1
            while PSSDWLX:
                REASON[1] = ^TMP($J,PSSDBASE,"OUT","DOSE","ERROR",PSSDWLP,PSSDWLX,"TEXT").split(".")[0]
                if REASON != REASON[1]:
                    MESSAGE[1] = ^TMP($J,PSSDBASE,"OUT","DOSE","ERROR",PSSDWLP,PSSDWLX,"MSG")
                    del ^TMP($J,PSSDBASE,"OUT","DOSE","ERROR",PSSDWLP,PSSDWLX)
                    del ^TMP($J,PSSDBASF,"OUT","DOSE","ERROR",PSSDWLP,PSSDWLX)
                    del ^TMP($J,PSSDBASG,"OUT",PSSDWLP,"ERROR",PSSDWLX)
                    FLAG = 1
                PSSDWLX = PSSDWLX + 1
            if PSSDBASA:
                ^TMP($J,PSSDBASF,"OUT","DOSE","ERROR",PSSDWLP,PSSDWL1,"MSG") = MESSAGE
                ^TMP($J,PSSDBASF,"OUT","DOSE","ERROR",PSSDWLP,PSSDWL1,"TEXT") = "Reason(s): " + REASON
            if PSSDBASB:
                ^TMP($J,PSSDBASG,"OUT",PSSDWLP,"ERROR",PSSDWL1,"MSG") = MESSAGE
                ^TMP($J,PSSDBASG,"OUT",PSSDWLP,"ERROR",PSSDWL1,"TEXT") = "Reason(s): " + REASON
        if SHOGEN(PSSDWLP):
            GETGNRL(PSSDWLP)
        PSSDBCAR[PSSDWLP].split("^")[24] = 1
        PSSDBCAR[PSSDWLP].split("^")[26] = 1
    return FLAG

def TWEAK02(PSSDWLP,PSSDWL1):
    REASON = ^TMP($J,PSSDBASE,"OUT","DOSE","ERROR",PSSDWLP,PSSDWL1,"TEXT").split(".")[0]
    FLAG, FLAG[1] = 0, 0
    if REASON == "Body surface area required":
        if PSSDBCAR[PSSDWLP].split("^")[5] == 1:
            del ^TMP($J,PSSDBASE,"OUT","DOSE","ERROR",PSSDWLP,PSSDWL1)
            FLAG = 1
        else:
            MESSAGE = ^TMP($J,PSSDBASE,"OUT","DOSE","ERROR",PSSDWLP,PSSDWL1,"MSG")
            PSSDWLX = PSSDWL1
            while PSSDWLX:
                REASON[1] = ^TMP($J,PSSDBASE,"OUT","DOSE","ERROR",PSSDWLP,PSSDWLX,"TEXT").split(".")[0]
                if REASON != REASON[1]:
                    MESSAGE[1] = ^TMP($J,PSSDBASE,"OUT","DOSE","ERROR",PSSDWLP,PSSDWLX,"MSG")
                    del ^TMP($J,PSSDBASE,"OUT","DOSE","ERROR",PSSDWLP,PSSDWLX)
                    del ^TMP($J,PSSDBASF,"OUT","DOSE","ERROR",PSSDWLP,PSSDWLX)
                    del ^TMP($J,PSSDBASG,"OUT",PSSDWLP,"ERROR",PSSDWLX)
                    FLAG = 1
                PSSDWLX = PSSDWLX + 1
            if PSSDBASA:
                ^TMP($J,PSSDBASF,"OUT","DOSE","ERROR",PSSDWLP,PSSDWL1,"MSG") = MESSAGE
                ^TMP($J,PSSDBASF,"OUT","DOSE","ERROR",PSSDWLP,PSSDWL1,"TEXT") = "Reason(s): " + REASON
            if PSSDBASB:
                ^TMP($J,PSSDBASG,"OUT",PSSDWLP,"ERROR",PSSDWL1,"MSG") = MESSAGE
                ^TMP($J,PSSDBASG,"OUT",PSSDWLP,"ERROR",PSSDWL1,"TEXT") = "Reason(s): " + REASON
        if SHOGEN(PSSDWLP):
            GETGNRL(PSSDWLP)
        PSSDBCAR[PSSDWLP].split("^")[25] = 1
        PSSDBCAR[PSSDWLP].split("^")[26] = 1
    return FLAG

def TWEAK03(PSSDWLP,PSSDWL1):
    SEVERITY = ^TMP($J,PSSDBASE,"OUT","DOSE","ERROR",PSSDWLP,PSSDWL1,"SEV").split(".")[0]
    FLAG = 0
    if SEVERITY == "NotScreened":
        PSSDBCAR[PSSDWLP].split("^")[29] = 1
        MESSAGE = CHECKMSG(PSSDWLP) + " could not be " + ("done" if PSSDSWHE == 1 else "performed") + " for Drug: " + PSSDBCAR[PSSDWLP].split("^")[1]
        if PSSDSWHE == 1:
            PSSREPL["performed"] = "done"
            MESSAGE = REPLACE(MESSAGE, PSSREPL) + "."
            PSSREPL[":."] = "."
            MESSAGE = REPLACE(MESSAGE, PSSREPL)
        REASON = "Weight required." if PSSDSWHE == 0 else "No weight documented for patient."
        ^TMP($J,PSSDBASE,"OUT","DOSE","ERROR",PSSDWLP,PSSDWL1,"MSG") = MESSAGE
        ^TMP($J,PSSDBASE,"OUT","DOSE","ERROR",PSSDWLP,PSSDWL1,"TEXT") = REASON
        if PSSDBASA:
            ^TMP($J,PSSDBASF,"OUT","DOSE","ERROR",PSSDWLP,PSSDWL1,"MSG") = MESSAGE
            ^TMP($J,PSSDBASF,"OUT","DOSE","ERROR",PSSDWLP,PSSDWL1,"TEXT") = "Reason(s): " + REASON
        if PSSDBASB:
            ^TMP($J,PSSDBASG,"OUT",PSSDWLP,"ERROR",PSSDWL1,"MSG") = MESSAGE
            ^TMP($J,PSSDBASG,"OUT",PSSDWLP,"ERROR",PSSDWL1,"TEXT") = "Reason(s): " + REASON
        FLAG = 1
        PSSDBCAR[PSSDWLP].split("^")[26] = 1
    return FLAG

def TWEAK04(PSSDWLP,PSSDWL1):
    SEVERITY = ^TMP($J,PSSDBASE,"OUT","DOSE","ERROR",PSSDWLP,PSSDWL1,"SEV").split(".")[0]
    FLAG = 0
    if SEVERITY == "Warning":
        MESSAGE = DOSEMSG(PSSDBCAR[PSSDWLP].split("^")[1], "S" if (PSSDBCAR[PSSDWLP].split("^")[1] == "S" and PSSDBCAR[PSSDWLP].split("^")[8] == 0) else "S" if PSSDBCAR[PSSDWLP].split("^")[15] == 1 else "", "W")
        ^TMP($J,PSSDBASE,"OUT","DOSE","ERROR",PSSDWLP,PSSDWL1,"MSG") = MESSAGE
        REASON = ^TMP($J,PSSDBASE,"OUT","DOSE","ERROR",PSSDWLP,PSSDWL1,"TEXT")
        if PSSDBASA:
            ^TMP($J,PSSDBASF,"OUT","DOSE","ERROR",PSSDWLP,PSSDWL1,"MSG") = MESSAGE
            ^TMP($J,PSSDBASF,"OUT","DOSE","ERROR",PSSDWLP,PSSDWL1,"TEXT") = REASON
        if PSSDBASB:
            ^TMP($J,PSSDBASG,"OUT",PSSDWLP,"ERROR",PSSDWL1,"MSG") = MESSAGE
            ^TMP($J,PSSDBASG,"OUT",PSSDWLP,"ERROR",PSSDWL1,"TEXT") = REASON
        FLAG = 1
        PSSDBCAR[PSSDWLP].split("^")[26] = 1
    return FLAG

def SHOGEN(PSSDWE5):
    PSSDWGFB = 0
    return SHOGEN()

def GETGNRL(PSSDWLP):
    DRUGNAME = PSSDBCAR[PSSDWLP].split("^")[2]
    DRUGIEN = PSSDBCAR[PSSDWLP].split("^")[3]
    if DRUGNAME != "" and DRUGIEN != "":
        if "^TMP($J,PSSDBASE,\"OUT\",\"DOSE\",PSSDWLP,DRUGNAME,\"GENERAL\",\"MESSAGE\",DRUGIEN" not in globals():
            globals()["^TMP($J,PSSDBASE,\"OUT\",\"DOSE\",PSSDWLP,DRUGNAME,\"GENERAL\",\"MESSAGE\",DRUGIEN"] = globals()["^TMP($J,PSSDSEXD,\"OUT\",\"DOSE\",PSSDWLP,DRUGNAME,\"GENERAL\",\"MESSAGE\",DRUGIEN"]
        if PSSDBASA:
            ^TMP($J,PSSDBASF,"OUT","DOSE",PSSDWLP,DRUGNAME,"3_GENERAL","MESSAGE",DRUGIEN,1) = globals()["^TMP($J,PSSDSEXD,\"OUT\",\"DOSE\",PSSDWLP,DRUGNAME,\"GENERAL\",\"MESSAGE\",DRUGIEN"]
        if PSSDBASB:
            ^TMP($J,PSSDBASG,"OUT",PSSDWLP,"MESSAGE","3_GENERAL",DRUGIEN,1) = globals()["^TMP($J,PSSDSEXD,\"OUT\",\"DOSE\",PSSDWLP,DRUGNAME,\"GENERAL\",\"MESSAGE\",DRUGIEN"]
    del globals()["^TMP($J,PSSDSEXD"]

def TWEAK1():
    # loop through EXCEPTION global, test for five IV related tweaks
    for PSSDWEX2 in ^TMP($J,PSSDBASE,"OUT","EXCEPTIONS","DOSE"):
        for PSSDWE2 in ^TMP($J,PSSDBASE,"OUT","EXCEPTIONS","DOSE",PSSDWEX2):
            NODE = ^TMP($J,PSSDBASE,"OUT","EXCEPTIONS","DOSE",PSSDWEX2,PSSDWE2)
            if TWEAK11(NODE):
                continue
            if TWEAK12(NODE):
                continue
            if TWEAK13(NODE):
                continue
            if TWEAK14(NODE):
                continue
            if TWEAK15(NODE):
                continue

def TWEAK11(NODE):
    REASON = str.upper(^TMP($J,PSSDBASE,"OUT","EXCEPTIONS","DOSE",PSSDWEX2,PSSDWE2,"TEXT"))
    if REASON != "DRUG NOT MATCHED TO NDF":
        return 0
    MESSAGE = CHECKMSG(PSSDWEX2) + " could not be performed for Drug: " + PSSDBCAR[PSSDWEX2].split("^")[2]
    ^TMP($J,PSSDBASE,"OUT","EXCEPTIONS","DOSE",PSSDWEX2,PSSDWE2,"MSG") = MESSAGE
    if PSSDBASA:
        ^TMP($J,PSSDBASF,"OUT","EXCEPTIONS","DOSE",PSSDWEX2,1) = MESSAGE
    if PSSDBASB:
        ^TMP($J,PSSDBASG,"OUT",PSSDWEX2,"EXCEPTIONS",1) = MESSAGE
    PSSDBCAR[PSSDWEX2].split("^")[27] = 1
    return 1

def TWEAK12(NODE):
    REASON = str.upper(^TMP($J,PSSDBASE,"OUT","EXCEPTIONS","DOSE",PSSDWEX2,PSSDWE2,"TEXT"))
    if REASON != "NO GCNSEQNO EXISTS FOR VA PRODUCT":
        return 0
    if EXMT(PSSDBCAR[PSSDWEX2].split("^")[3]) == 0:
        del ^TMP($J,PSSDBASE,"OUT","EXCEPTIONS","DOSE",PSSDWEX2,PSSDWE2)
        if PSSDBASA:
            del ^TMP($J,PSSDBASF,"OUT","EXCEPTIONS","DOSE",PSSDWEX2)
        if PSSDBASB:
            del ^TMP($J,PSSDBASG,"OUT",PSSDWEX2,"EXCEPTIONS")
        PSSDBCAR[PSSDWEX2].split("^")[27] = 1
        return 1

def TWEAK13(NODE):
    REASON = str.upper(^TMP($J,PSSDBASE,"OUT","EXCEPTIONS","DOSE",PSSDWEX2,PSSDWE2,"TEXT"))
    if REASON != "NO GCNSEQNO EXISTS FOR VA PRODUCT":
        return 0
    if EXMT(PSSDBCAR[PSSDWEX2].split("^")[3]) == 1:
        MESSAGE = CHECKMSG(PSSDWEX2) + " could not be performed for Drug: " + PSSDBCAR[PSSDWEX2].split("^")[2] + ", please complete a manual check for appropriate Dosing."
        ^TMP($J,PSSDBASE,"OUT","EXCEPTIONS","DOSE",PSSDWEX2,PSSDWE2,"MSG") = MESSAGE
        ^TMP($J,PSSDBASE,"OUT","EXCEPTIONS","DOSE",PSSDWEX2,PSSDWE2,"TEXT") = ""
        if PSSDBASA:
            ^TMP($J,PSSDBASF,"OUT","EXCEPTIONS","DOSE",PSSDWEX2,1) = MESSAGE
            ^TMP($J,PSSDBASF,"OUT","EXCEPTIONS","DOSE",PSSDWEX2,2) = ""
        if PSSDBASB:
            ^TMP($J,PSSDBASG,"OUT",PSSDWEX2,"EXCEPTIONS",1) = MESSAGE
            ^TMP($J,PSSDBASG,"OUT",PSSDWEX2,"EXCEPTIONS",2) = ""
        PSSDBCAR[PSSDWEX2].split("^")[27] = 1
        return 1

def TWEAK14(NODE):
    REASON = str.upper(^TMP($J,PSSDBASE,"OUT","EXCEPTIONS","DOSE",PSSDWEX2,PSSDWE2,"TEXT"))
    if REASON != "BAD GCNSEQNO ASSIGNED TO VA PRODUCT":
        return 0
    if EXMT(PSSDBCAR[PSSDWEX2].split("^")[3]) == 0:
        del ^TMP($J,PSSDBASE,"OUT","EXCEPTIONS","DOSE",PSSDWEX2,PSSDWE2)
        if PSSDBASA:
            del ^TMP($J,PSSDBASF,"OUT","EXCEPTIONS","DOSE",PSSDWEX2)
        if PSSDBASB:
            del ^TMP($J,PSSDBASG,"OUT",PSSDWEX2,"EXCEPTIONS")
        PSSDBCAR[PSSDWEX2].split("^")[27] = 1
        return 1

def TWEAK15(NODE):
    REASON = str.upper(^TMP($J,PSSDBASE,"OUT","EXCEPTIONS","DOSE",PSSDWEX2,PSSDWE2,"TEXT"))
    if REASON != "BAD GCNSEQNO ASSIGNED TO VA PRODUCT":
        return 0
    if EXMT(PSSDBCAR[PSSDWEX2].split("^")[3]) == 1:
        MESSAGE = CHECKMSG(PSSDWEX2) + " could not be performed for Drug: " + PSSDBCAR[PSSDWEX2].split("^")[2] + ", please complete a manual check for appropriate Dosing."
        ^TMP($J,PSSDBASE,"OUT","EXCEPTIONS","DOSE",PSSDWEX2,PSSDWE2,"MSG") = MESSAGE
        ^TMP($J,PSSDBASE,"OUT","EXCEPTIONS","DOSE",PSSDWEX2,PSSDWE2,"TEXT") = ""
        if PSSDBASA:
            ^TMP($J,PSSDBASF,"OUT","EXCEPTIONS","DOSE",PSSDWEX2,1) = MESSAGE
            ^TMP($J,PSSDBASF,"OUT","EXCEPTIONS","DOSE",PSSDWEX2,2) = ""
        if PSSDBASB:
            ^TMP($J,PSSDBASG,"OUT",PSSDWEX2,"EXCEPTIONS",1) = MESSAGE
            ^TMP($J,PSSDBASG,"OUT",PSSDWEX2,"EXCEPTIONS",2) = ""
        PSSDBCAR[PSSDWEX2].split("^")[27] = 1
        return 1

def TWEAK2():
    # loop through exception global, look for OR related tweaks
    TWEAK2()

def TWEAK3():
    # ensure intermittent with certain exceptions have general dosing info
    for PSSDWEX2 in ^TMP($J,PSSDBASE,"OUT","EXCEPTIONS","DOSE"):
        for PSSDWE2 in ^TMP($J,PSSDBASE,"OUT","EXCEPTIONS","DOSE",PSSDWEX2):
            NODE = ^TMP($J,PSSDBASE,"OUT","EXCEPTIONS","DOSE",PSSDWEX2,PSSDWE2)
            if TWEAK31(NODE):
                continue

def TWEAK31(NODE):
    REASON = str.upper(^TMP($J,PSSDBASE,"OUT","EXCEPTIONS","DOSE",PSSDWEX2,PSSDWE2,"TEXT"))
    if REASON != "INVALID OR UNDEFINED FREQUENCY":
        return 0
    if PSSDBASA:
        MESSAGE = "Max Daily Dose Check could not be done for Drug: " + PSSDBCAR[PSSDWEX2].split("^")[2] + ", please complete a manual check for appropriate Dosing."
        ^TMP($J,PSSDBASE,"OUT","EXCEPTIONS","DOSE",PSSDWEX2,PSSDWE2,"MSG") = MESSAGE
        ^TMP($J,PSSDBASE,"OUT","EXCEPTIONS","DOSE",PSSDWEX2,PSSDWE2,"TEXT") = ""
        ^TMP($J,PSSDBASF,"OUT","EXCEPTIONS","DOSE",PSSDWEX2,1) = MESSAGE
        ^TMP($J,PSSDBASF,"OUT","EXCEPTIONS","DOSE",PSSDWEX2,2) = ""
    if SHOGEN(PSSDWEX2):
        GETGNRL3(PSSDWEX2)
    PSSDBCAR[PSSDWEX2].split("^")[27] = 1
    return 1

def CHECKMSG(PSSLOOP):
    return "Maximum Single Dose Check" if PSSDBCAR[PSSLOOP].split("^")[4] == 0 or PSSDBCAR[PSSLOOP].split("^")[14] == 1 or ISCMPLEX(PSSLOOP) else "Dosing Order Checks" if PSSDBCAR[PSSLOOP].split("^")[29] == 1 else ISCMPLET(PSSLOOP)

def ISCMPLEX(PSSLOOP):
    return 1 if PSSDBCAR[PSSLOOP].split("^")[15] == 1 or int(PSSLOOP.split(";")[4]) else 0