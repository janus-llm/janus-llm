def SDOSE(LIST, PSS):
    PSSZR, PSSZR1, PSSZRT, PSSZRT1 = "", "", "", ""
    ^TMP($J,LIST,+PSS(1),.01) = ^TMP("PSSP50",$J,50,PSS(1),.01,"I")
    ^TMP($J,LIST,"B",^TMP("PSSP50",$J,50,PSS(1),.01,"I"),+PSS(1)) = ""
    PSSZR = ^TMP("PSSP50",$J,50,PSS(1),901,"I")
    if PSSZR != "":
        PSSZR1 = LEAD(PSSZR)
    ^TMP($J,LIST,+PSS(1),901) = PSSZR1
    if ^TMP("PSSP50",$J,50,PSS(1),902,"I") != "":
        PSSZRT = ^TMP("PSSP50",$J,50,PSS(1),902,"E")
    if PSSZRT != "":
        PSSZRT1 = LEADU(PSSZRT)
    ^TMP($J,LIST,+PSS(1),902) = ^TMP("PSSP50",$J,50,PSS(1),902,"I") = "" ? "" : ^TMP("PSSP50",$J,50,PSS(1),902,"I") + "^" + PSSZRT1

def SDOSE2(LIST, PSS):
    PSSZR2, PSSZR2T = "", ""
    PSSZR2 = ^TMP("PSSP50",$J,50.0903,PSS(2),.01,"I")
    if PSSZR2 != "":
        PSSZR2T = LEAD(PSSZR2)
    ^TMP($J,LIST,+PSS(1),"POS",+PSS(2),.01) = PSSZR2T
    PSSZR3, PSSZR3T = "", ""
    PSSZR3 = ^TMP("PSSP50",$J,50.0903,PSS(2),1,"I")
    if PSSZR3 != "":
        PSSZR3T = LEAD(PSSZR3)
    ^TMP($J,LIST,+PSS(1),"POS",+PSS(2),1) = PSSZR3T
    PSSPOSIO = ^TMP("PSSP50",$J,50.0903,PSS(2),2,"I")
    ^TMP($J,LIST,+PSS(1),"POS",+PSS(2),2) = PSSPOSIO = "" ? "" : PSSPOSIO + "^" + (PSSPOSIO = "I" ? "Inpatient" : PSSPOSIO = "O" ? "Outpatient" : PSSPOSIO = "IO" ? "Both" : PSSPOSIO = "OI" ? "Both" : "")
    ^TMP($J,LIST,+PSS(1),"POS",+PSS(2),3) = ^TMP("PSSP50",$J,50.0903,PSS(2),3,"I")

def SDOSE3(LIST, PSS):
    ^TMP($J,LIST,+PSS(1),"LOC",+PSS(2),.01) = ^TMP("PSSP50",$J,50.0904,PSS(2),.01,"I")
    ^TMP($J,LIST,+PSS(1),"LOC",+PSS(2),1) = ^TMP("PSSP50",$J,50.0904,PSS(2),1,"I") = "" ? "" : ^TMP("PSSP50",$J,50.0904,PSS(2),1,"I") + "^" + ^TMP("PSSP50",$J,50.0904,PSS(2),1,"E")
    ^TMP($J,LIST,+PSS(1),"LOC",+PSS(2),2) = ^TMP("PSSP50",$J,50.0904,PSS(2),2,"I")
    ^TMP($J,LIST,+PSS(1),"LOC",+PSS(2),3) = ^TMP("PSSP50",$J,50.0904,PSS(2),3,"I")

def LOOP(PSSENCT, PSS, PSSFL, PSSRTOI, PSSPK, LIST):
    PSSENCT = 0
    PSS(1) = 0
    while PSS(1):
        if ^PSDRUG(PSS(1),0) = "":
            continue
        if PSSFL and ^PSDRUG(PSS(1),"I") and ^("I") <= PSSFL:
            continue
        if PSSRTOI = 1 and not ^PSDRUG(PSS(1),2):
            continue
        PSSZ5, PSSZ6 = 0, 1
        while PSSZ5:
            if ^PSDRUG(PSS(1),2) = $E(PSSPK,PSSZ6):
                PSSZ5 = 1
        if PSSPK and not PSSZ5:
            continue
        SETSUB7^PSS50AQM(PSS(1))
        SETSUB8^PSS50AQM(PSS(1))
        SETLP1()
        SETLP2()
        SETLP3()
        PSSENCT = PSSENCT + 1
    ^TMP($J,LIST,0) = PSSENCT ? PSSENCT : "-1^NO DATA FOUND"

def SETLP1(LIST, PSS):
    PSSZNODE = ^PSDRUG(PSS(1),0)
    PSS50NOD = ^("DOS")
    ^TMP($J,LIST,+PSS(1),.01) = $P(PSSZNODE,"^")
    ^TMP($J,LIST,"B",$P(PSSZNODE,"^"),+PSS(1)) = ""
    PSSZR, PSSZR1 = "", ""
    PSSZR = $P(PSS50NOD,"^")
    if PSSZR != "":
        PSSZR1 = LEAD(PSSZR)
    ^TMP($J,LIST,+PSS(1),901) = PSSZR1
    PSSZRT, PSSZRT1 = "", ""
    if $P(PSS50NOD,"^",2):
        PSSZRT = $P($G(^PS(50.607,+$P(PSS50NOD,"^",2),0)),"^")
    if PSSZRT != "":
        PSSZRT1 = LEADU(PSSZRT)
    ^TMP($J,LIST,+PSS(1),902) = $P(PSS50NOD,"^",2) ? $P(PSS50NOD,"^",2) + "^" + PSSZRT1 : ""

def SETLP2(LIST, PSS):
    PSS903C = 0
    if $O(^PSDRUG(PSS(1),"DOS1",0)):
        PSS903 = 0
        while PSS903:
            PSS903ND = ^PSDRUG(PSS(1),"DOS1",PSS903,0)
            if $P(PSS903ND,"^") != "":
                PSS903C = PSS903C + 1
                PSSZR5, PSSZR6 = "", ""
                PSSZR5 = $P(PSS903ND,"^")
                if PSSZR5 != "":
                    PSSZR6 = LEAD(PSSZR5)
                ^TMP($J,LIST,+PSS(1),"POS",PSS903,.01) = PSSZR6
                PSSZR7, PSSZR8 = "", ""
                PSSZR7 = $P(PSS903ND,"^",2)
                if PSSZR7 != "":
                    PSSZR8 = LEAD(PSSZR7)
                ^TMP($J,LIST,+PSS(1),"POS",PSS903,1) = PSSZR8
                PSS903IO = $P(PSS903ND,"^",3)
                ^TMP($J,LIST,+PSS(1),"POS",PSS903,2) = PSS903IO = "" ? "" : PSS903IO + "^" + (PSS903IO = "I" ? "Inpatient" : PSS903IO = "O" ? "Outpatient" : PSS903IO = "IO" ? "Both" : PSS903IO = "OI" ? "Both" : "")
                ^TMP($J,LIST,+PSS(1),"POS",PSS903,3) = $P(PSS903ND,"^",4)
    ^TMP($J,LIST,+PSS(1),"POS",0) = PSS903C ? PSS903C : "-1^NO DATA FOUND"

def SETLP3(LIST, PSS):
    PSS904C = 0
    if $O(^PSDRUG(PSS(1),"DOS2",0)):
        PSS904 = 0
        while PSS904:
            PSS904ND = ^PSDRUG(PSS(1),"DOS2",PSS904)
            if $P(PSS904ND,"^") != "":
                PSS904C = PSS904C + 1
                ^TMP($J,LIST,+PSS(1),"LOC",PSS904,.01) = $P(PSS904ND,"^")
                PSS904IO = $P(PSS904ND,"^",2)
                ^TMP($J,LIST,+PSS(1),"LOC",PSS904,1) = PSS904IO = "" ? "" : PSS904IO + "^" + (PSS904IO = "I" ? "Inpatient" : PSS904IO = "O" ? "Outpatient" : PSS904IO = "IO" ? "Both" : PSS904IO = "OI" ? "Both" : "")
                ^TMP($J,LIST,+PSS(1),"LOC",PSS904,2) = $P(PSS904ND,"^",3)
                ^TMP($J,LIST,+PSS(1),"LOC",PSS904,3) = $P(PSS904ND,"^",4)
    ^TMP($J,LIST,+PSS(1),"LOC",0) = PSS904C ? PSS904C : "-1^NO DATA FOUND"

def LEAD(PSSLEAD):
    return "0" + PSSLEAD if PSSLEAD[0] == "." else PSSLEAD

def LEADU(PSSLEADU):
    if "/" not in PSSLEADU:
        return "0" + PSSLEADU if PSSLEADU[0] == "." else PSSLEADU
    PSSLDU1, PSSLDU2 = PSSLEADU.split("/")
    PSSLDU1 = "0" + PSSLDU1 if PSSLDU1[0] == "." else PSSLDU1
    PSSLDU2 = "0" + PSSLDU2 if PSSLDU2[0] == "." else PSSLDU2
    return PSSLDU1 + "/" + PSSLDU2

LOOP(PSSENCT, PSS, PSSFL, PSSRTOI, PSSPK, LIST)