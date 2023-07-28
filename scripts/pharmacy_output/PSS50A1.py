def SETDRG():
    global LIST, PSS
    ^TMP[$J,LIST,+PSS(1),.01] = ^TMP["PSSP50",$J,50,PSS(1),.01,"I"]
    ^TMP[$J,LIST,"B",^TMP["PSSP50",$J,50,PSS(1),.01,"I"],+PSS(1)] = ""
    ^TMP[$J,LIST,+PSS(1),62.01] = ^TMP["PSSP50",$J,50,PSS(1),62.01,"I"]
    ^TMP[$J,LIST,+PSS(1),62.02] = $G(^TMP["PSSP50",$J,50,PSS(1),62.02,"I")) + "^" + $G(^TMP["PSSP50",$J,50,PSS(1),62.02,"E")) if $G(^TMP["PSSP50",$J,50,PSS(1),62.02,"I")) != "" else ""
    ^TMP[$J,LIST,+PSS(1),62.03] = $G(^TMP["PSSP50",$J,50,PSS(1),62.03,"I")) + "^" + $G(^TMP["PSSP50",$J,50,PSS(1),62.03,"E")) if $G(^TMP["PSSP50",$J,50,PSS(1),62.03,"I")) != "" else ""
    ^TMP[$J,LIST,+PSS(1),62.04] = ^TMP["PSSP50",$J,50,PSS(1),62.04,"I"]
    ^TMP[$J,LIST,+PSS(1),62.05] = $G(^TMP["PSSP50",$J,50,PSS(1),62.05,"I")) + "^" + $G(^TMP["PSSP50",$J,50,PSS(1),62.05,"E")) if $G(^TMP["PSSP50",$J,50,PSS(1),62.05,"I")) != "" else ""
    ^TMP[$J,LIST,+PSS(1),905] = $G(^TMP["PSSP50",$J,50,PSS(1),905,"I")) + "^" + $G(^TMP["PSSP50",$J,50,PSS(1),905,"E")) if $G(^TMP["PSSP50",$J,50,PSS(1),905,"I")) != "" else ""

def LOOP():
    global LIST, PSS, PSSFL, PSSRTOI, PSSPK, PSSENCT
    PSS50DD, PSS50ERR = FIELD^DID(50,62.03,"Z","POINTER","PSS50DD","PSS50ERR")
    PSS8UDS = $G(PSS50DD["POINTER")
    PSSENCT = 0
    PSS(1) = 0
    while PSS(1):
        if $P($G(^PSDRUG(PSS(1),0)),"^") == "":
            continue
        if $G(PSSFL) and $P($G(^PSDRUG(PSS(1),"I")),"^") and $P($G(^("I")),"^") <= PSSFL:
            continue
        if $G(PSSRTOI) == 1 and not $P($G(^PSDRUG(PSS(1),2)),"^"):
            continue
        PSSZ5 = 0
        if $G(PSSPK) != "":
            PSSZ5 = 0
            PSSZ6 = 1
            while PSSZ6 <= $L(PSSPK):
                if $P($G(^(2)),"^",3)[$E(PSSPK,PSSZ6):
                    PSSZ5 = 1
                PSSZ6 += 1
        if $G(PSSPK) != "" and not PSSZ5:
            continue
        SETDRGL()
        PSSENCT += 1
        PSS(1) += 1
    ^TMP[$J,LIST,0] = $G(PSSENCT) if $G(PSSENCT) else "-1^NO DATA FOUND"

def SETDRGL():
    global LIST, PSS
    PSSZNODE = $G(^PSDRUG(PSS(1),0))
    PSS8ND = $G(^(8))
    ^TMP[$J,LIST,+PSS(1),.01] = $P(PSSZNODE,"^")
    ^TMP[$J,LIST,"B",$P(PSSZNODE,"^"),+PSS(1)] = ""
    ^TMP[$J,LIST,+PSS(1),62.01] = $P(PSS8ND,"^")
    ^TMP[$J,LIST,+PSS(1),62.02] = $P(PSS8ND,"^",2) + "^" + $P($G(^PS(51.2,+$P(PSS8ND,"^",2),0)),"^") if $P(PSS8ND,"^",2) else ""
    PSS8UD = $P(PSS8ND,"^",3)
    if PSS8UD != "" and PSS8UDS != "" and PSS8UDS[PSS8UD + ":"]:
        ^TMP[$J,LIST,+PSS(1),62.03] = PSS8UD + "^" + $P($E(PSS8UDS,$F(PSS8UDS,(PSS8UD + ":")),999),";")
    else:
        ^TMP[$J,LIST,+PSS(1),62.03] = ""
    ^TMP[$J,LIST,+PSS(1),62.04] = $P(PSS8ND,"^",4)
    ^TMP[$J,LIST,+PSS(1),62.05] = $P(PSS8ND,"^",5) + "^" + $P($G(^PSDRUG(+$P(PSS8ND,"^",5),0)),"^") if $P(PSS8ND,"^",5) else ""
    ^TMP[$J,LIST,+PSS(1),905] = $P(PSS8ND,"^",6) + "^" + $P($G(^PSDRUG(+$P(PSS8ND,"^",6),0)),"^") if $P(PSS8ND,"^",6) else ""

def LABEL():
    global LIST, PSSIEN, PSS
    if $G(LIST) == "":
        return
    ^TMP[$J,LIST] = ""
    if +$G(PSSIEN) <= 0:
        ^TMP[$J,LIST,0] = -1 + "^" + "NO DATA FOUND"
        return
    PSSIEN2 = $$FIND1^DIC(50,"","A","`"_PSSIEN,,,"")
    if +PSSIEN2 <= 0:
        ^TMP[$J,LIST,0] = -1 + "^" + "NO DATA FOUND"
        return
    ^TMP[$J,LIST,0] = 1
    K PSS50
    D GETS^DIQ(50,+PSSIEN2,".01;25;51;100;101;102","IE","PSS50")
    PSS(1) = 0
    while PSS(1):
        SLABEL()
        PSS(1) += 1
    K ^TMP["DILIST",$J]

def SLABEL():
    global LIST, PSS, PSS50
    ^TMP[$J,LIST,+PSS(1),.01] = $G(PSS50[50,PSS(1),.01,"I"])
    ^TMP[$J,LIST,"B",$G(PSS50[50,PSS(1),.01,"I"]),+PSS(1)] = ""
    ^TMP[$J,LIST,+PSS(1),25] = $G(PSS50[50,PSS(1),25,"I"]) + "^" + $G(PSS50[50,PSS(1),25,"E"]) + "^" + $P($G(^PS(50.605,+PSS50[50,PSS(1),25,"I"),0)),"^",2) if $G(PSS50[50,PSS(1),25,"I"]) != "" else ""
    ^TMP[$J,LIST,+PSS(1),51] = $G(PSS50[50,PSS(1),51,"I"]) + "^" + $G(PSS50[50,PSS(1),51,"E"]) if $G(PSS50[50,PSS(1),51,"I"]) != "" else ""
    ^TMP[$J,LIST,+PSS(1),100] = $G(PSS50[50,PSS(1),100,"I"]) + "^" + $G(PSS50[50,PSS(1),100,"E"]) if $G(PSS50[50,PSS(1),100,"I"]) != "" else ""
    ^TMP[$J,LIST,+PSS(1),101] = $G(PSS50[50,PSS(1),101,"E"])
    ^TMP[$J,LIST,+PSS(1),102] = $G(PSS50[50,PSS(1),102,"E"])

def SORT():
    global LIST, PSSIEN, PSS
    if $G(LIST) == "":
        return
    ^TMP[$J,LIST] = ""
    if +$G(PSSIEN) <= 0:
        ^TMP[$J,LIST,0] = -1 + "^" + "NO DATA FOUND"
        return
    PSSIEN2 = $$FIND1^DIC(50,"","A","`"_PSSIEN,,,"")
    if +PSSIEN2 <= 0:
        ^TMP[$J,LIST,0] = -1 + "^" + "NO DATA FOUND"
        return
    ^TMP[$J,LIST,0] = 1
    K PSS50
    D GETS^DIQ(50,+PSSIEN2,".01","IE","PSS50")
    PSS(1) = 0
    while PSS(1):
        ^TMP[$J,LIST,$G(PSS50[50,PSS(1),.01,"I"]),+PSS(1)] = ""
        PSS(1) += 1
    K ^TMP["DILIST",$J]