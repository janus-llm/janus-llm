def HOSP():
    global PSSIEN, PSSFT, LIST
    LIST = "^TMP($J,LIST)"
    ^TMP($J,LIST) = {}
    if int(PSSIEN) <= 0 and PSSFT == "":
        ^TMP($J,LIST,0) = -1 + "^" + "NO DATA FOUND"
        return
    if int(PSSIEN) > 0:
        PSSIEN2 = $$FIND1^DIC(51.1,"","A","`" + PSSIEN,,,)
        if int(PSSIEN2) <= 0:
            ^TMP($J,LIST,0) = -1 + "^" + "NO DATA FOUND"
            return
        ^TMP($J,"PSS51P1") = {}
        $$GETS^DIQ(51.1, +PSSIEN2, ".01;7*", "IE", "^TMP($J,""PSS51P1"")")
        PSS(1) = 0
        CNT = 0
        PSSIEN = +PSSIEN2
        while PSS(1) in ^TMP($J,"PSS51P1",51.17):
            SETLOC^PSS51P1B()
            CNT = CNT + 1
        if CNT > 0:
            ^TMP($J,LIST,+PSSIEN,"HOSP",0) = CNT
        else:
            ^TMP($J,LIST,+PSSIEN,"HOSP",0) = -1 + "^" + "NO DATA FOUND"
        PSS(2) = 0
        while PSS(2) in ^TMP($J,"PSS51P1",51.1):
            ^TMP($J,LIST,+PSS(2),.01) = $G(^TMP($J,"PSS51P1",51.1,PSS(2),.01,"I"))
            ^TMP($J,LIST,"B",$G(^TMP($J,"PSS51P1",51.1,PSS(2),.01,"E")),+PSS(2)) = ""
    if int(PSSIEN) <= 0 and PSSFT != "":
        if PSSFT["??":
            LOOP^PSS51P1B(3)
            return
        $$FIND^DIC(51.1,,"@;.01","QP",PSSFT,,"B",,,"")
        if int(^TMP("DILIST",$J,0)) == 0:
            ^TMP($J,LIST,0) = -1 + "^" + "NO DATA FOUND"
            return
        if int(^TMP("DILIST",$J,0)) > 0:
            ^TMP($J,LIST,0) = +^TMP("DILIST",$J,0)
            PSSXX = 0
            while PSSXX in ^TMP("DILIST",$J,PSSXX):
                PSSIEN = +^TMP("DILIST",$J,PSSXX,0)
                ^TMP($J,"PSS51P1") = {}
                $$GETS^DIQ(51.1, +PSSIEN, ".01;7*", "IE", "^TMP($J,""PSS51P1"")")
                PSS(1) = 0
                CNT = 0
                while PSS(1) in ^TMP($J,"PSS51P1",51.17):
                    SETLOC^PSS51P1B()
                    CNT = CNT + 1
                if CNT > 0:
                    ^TMP($J,LIST,+PSSIEN,"HOSP",0) = CNT
                else:
                    ^TMP($J,LIST,+PSSIEN,"HOSP",0) = -1 + "^" + "NO DATA FOUND"
                PSS(2) = 0
                while PSS(2) in ^TMP($J,"PSS51P1",51.1):
                    ^TMP($J,LIST,+PSS(2),.01) = $G(^TMP($J,"PSS51P1",51.1,PSS(2),.01,"I"))
                    ^TMP($J,LIST,"B",$G(^TMP($J,"PSS51P1",51.1,PSS(2),.01,"E")),+PSS(2)) = ""
    K ^TMP("DILIST",$J),^TMP($J,"PSS51P1")


def SCRFREQ():
    global SCR, PSSFREQ
    if SCR("S") == "" and PSSFREQ != "":
        SCR("S") = "I ($P($G(^PS(51.1,+Y,0)),""^"",3)'>PSSFREQ)&($P($G(^PS(51.1,+Y,0)),""^"",3)'="""")"
    elif SCR("S") != "" and PSSFREQ != "":
        SCR("S") = SCR("S") + "&($P($G(^PS(51.1,+Y,0)),""^"",3)'>PSSFREQ)&($P($G(^PS(51.1,+Y,0)),""^"",3)'="""")"


def AP():
    global PSSPP, PSSFT, LIST, PSSIEN
    LIST = "^TMP($J,LIST)"
    ^TMP($J,LIST) = {}
    SCR("S") = ""
    if PSSTYP != "":
        SCR("S") = "I ($P($G(^PS(51.1,+Y,0)),""^"",5)[PSSTYP)"
    SCRFREQ()
    if PSSPP == "":
        ^TMP($J,LIST,0) = -1 + "^" + "NO DATA FOUND"
        return
    if PSSPP != "" and PSSFT == "":
        $$LIST^DIC(51.1,"","@;.01;1;2;2.5;4;5IE;8","P",,,,,"AP"_PSSPP,SCR("S"),,)
        if +^TMP("DILIST",$J,0) <= 0:
            ^TMP($J,LIST,0) = -1 + "^" + "NO DATA FOUND"
            return
        if +^TMP("DILIST",$J,0) > 0:
            ^TMP($J,LIST,0) = +^TMP("DILIST",$J,0)
            PSSXX = 0
            while PSSXX in ^TMP("DILIST",$J,PSSXX):
                PSSIEN = +^TMP("DILIST",$J,PSSXX,0)
                ^TMP($J,LIST,+PSSIEN,.01) = $P($G(^TMP("DILIST",$J,PSSXX,0)),"^",2)
                ^TMP($J,LIST,"AP"_PSSPP,$P($G(^TMP("DILIST",$J,PSSXX,0)),"^",2),+$G(^TMP("DILIST",$J,PSSXX,0))) = ""
                ^TMP($J,LIST,+PSSIEN,1) = $P($G(^TMP("DILIST",$J,PSSXX,0)),"^",3)
                ^TMP($J,LIST,+PSSIEN,2) = $P($G(^TMP("DILIST",$J,PSSXX,0)),"^",4)
                ^TMP($J,LIST,+PSSIEN,2.5) = $P($G(^TMP("DILIST",$J,PSSXX,0)),"^",5)
                ^TMP($J,LIST,+PSSIEN,4) = $P($G(^TMP("DILIST",$J,PSSXX,0)),"^",6)
                ^TMP($J,LIST,+PSSIEN,5) = $S($P($G(^TMP("DILIST",$J,PSSXX,0)),"^",7)="":"",$P($G(^TMP("DILIST",$J,PSSXX,0)),"^",7)_"^"_$P($G(^TMP("DILIST",$J,PSSXX,0)),"^",8))
                ^TMP($J,LIST,+PSSIEN,8) = $P($G(^TMP("DILIST",$J,PSSXX,0)),"^",9)
                HOSPLOC(LIST,+PSSIEN)
                if int(PSSWDIEN) <= 0:
                    ^TMP($J,"PSS51P1") = {}
                    $$GETS^DIQ(51.1,+PSSIEN,".01;3*","IE","^TMP($J,""PSS51P1""") 
                    PSS(1) = +PSSIEN
                    CNT = 0
                    while PSS(1) in ^TMP($J,"PSS51P1",51.11):
                        SETWARD^PSS51P1B()
                        CNT = CNT + 1
                    if CNT > 0:
                        ^TMP($J,LIST,+PSSIEN,"WARD",0) = CNT
                    else:
                        ^TMP($J,LIST,+PSSIEN,"WARD",0) = -1 + "^" + "NO DATA FOUND"
                if int(PSSWDIEN) > 0:
                    ^TMP($J,"PSS51P1") = {}
                    $$GETS^DIQ(51.1,+PSSIEN,".01;3*","IE","^TMP($J,""PSS51P1""") 
                    if +$D(^TMP($J,"PSS51P1",51.11)) <= 0:
                        ^TMP($J,LIST,+PSSIEN,"WARD",0) = -1 + "^" + "NO DATA FOUND"
                        return
                    PSS(2) = 0
                    while PSS(2) in ^TMP($J,"PSS51P1",51.11):
                        if PSSWDIEN == $P($G(^TMP($J,"PSS51P1",51.11,PSS(2),.01,"I")),"^"):
                            SETWRD2^PSS51P1B()
                        else:
                            ^TMP($J,LIST,+PSSIEN,"WARD",0) = -1 + "^" + "NO DATA FOUND FOR PSSWDIEN #" + PSSWDIEN
    if PSSPP != "" and PSSFT != "":
        if PSSFT["??":
            LOOP^PSS51P1B(5)
            return
        $$FIND^DIC(51.1,,"@;.01;1;2;2.5;4;5IE;8",,PSSFT,,"AP"_PSSPP,SCR("S"),,"")
        if int(^TMP("DILIST",$J,0)) <= 0:
            ^TMP($J,LIST,0) = -1 + "^" + "NO DATA FOUND"
            return
        if int(^TMP("DILIST",$J,0)) > 0:
            ^TMP($J,LIST,0) = +^TMP("DILIST",$J,0)
            PSSXX = 0
            while PSSXX in ^TMP("DILIST",$J,2):
                PSSIEN = +^TMP("DILIST",$J,2,PSSXX)
                ^TMP($J,LIST,+PSSIEN,.01) = $G(^TMP("DILIST",$J,"ID",PSSXX,.01))
                ^TMP($J,LIST,"AP"_PSSPP,$G(^TMP("DILIST",$J,"ID",PSSXX,.01)),+PSSIEN) = ""
                ^TMP($J,LIST,+PSSIEN,1) = $G(^TMP("DILIST",$J,"ID",PSSXX,1))
                ^TMP($J,LIST,+PSSIEN,2) = $G(^TMP("DILIST",$J,"ID",PSSXX,2))
                ^TMP($J,LIST,+PSSIEN,2.5) = $G(^TMP("DILIST",$J,"ID",PSSXX,2.5))
                ^TMP($J,LIST,+PSSIEN,4) = $G(^TMP("DILIST",$J,"ID",PSSXX,4))
                ^TMP($J,LIST,+PSSIEN,5) = $S($G(^TMP("DILIST",$J,"ID",PSSXX,5,"I"))="":"",$G(^TMP("DILIST",$J,"ID",PSSXX,5,"I")) + "^" + $G(^TMP("DILIST",$J,"ID",PSSXX,5,"E")))
                ^TMP($J,LIST,+PSSIEN,8) = $G(^TMP("DILIST",$J,"ID",PSSXX,8))
                HOSPLOC(LIST,+PSSIEN)
                if int(PSSWDIEN) <= 0:
                    ^TMP($J,"PSS51P1") = {}
                    $$GETS^DIQ(51.1,+PSSIEN,".01;3*","IE","^TMP($J,""PSS51P1""") 
                    PSS(1) = +PSSIEN
                    CNT = 0
                    while PSS(1) in ^TMP($J,"PSS51P1",51.11):
                        SETWARD^PSS51P1B()
                        CNT = CNT + 1
                    if CNT > 0:
                        ^TMP($J,LIST,+PSSIEN,"WARD",0) = CNT
                    else:
                        ^TMP($J,LIST,+PSSIEN,"WARD",0) = -1 + "^" + "NO DATA FOUND"
                if int(PSSWDIEN) > 0:
                    ^TMP($J,"PSS51P1") = {}
                    $$GETS^DIQ(51.1,+PSSIEN,".01;3*","IE","^TMP($J,""PSS51P1""") 
                    if +$D(^TMP($J,"PSS51P1",51.11)) <= 0:
                        ^TMP($J,LIST,+PSSIEN,"WARD",0) = -1 + "^" + "NO DATA FOUND"
                        return
                    PSS(2) = 0
                    while PSS(2) in ^TMP($J,"PSS51P1",51.11):
                        if PSSWDIEN == $P($G(^TMP($J,"PSS51P1",51.11,PSS(2),.01,"I")),"^"):
                            SETWRD2^PSS51P1B()
                        else:
                            ^TMP($J,LIST,+PSSIEN,"WARD",0) = -1 + "^" + "NO DATA FOUND FOR PSSWDIEN #" + PSSWDIEN
    K ^TMP("DILIST",$J),^TMP($J,"PSS51P1")


def HOSPLOC(LIST,PSSIEN):
    global PSSHOSP
    PSSHOSP = {}
    $$GETS^DIQ(51.1,+PSSIEN,"7*","IE","PSSHOSP")
    PSSCNT = 0
    PSSTIM = 0
    while PSSTIM in PSSHOSP(51.17):
        ^TMP($J,LIST,+PSSIEN,"HOSPITAL LOCATION",+PSSTIM,.01) = PSSHOSP(51.17,PSSTIM,.01,"I") + "^" + PSSHOSP(51.17,PSSTIM,.01,"E")
        ^TMP($J,LIST,+PSSIEN,"HOSPITAL LOCATION",+PSSTIM,1) = $S(PSSHOSP(51.17,PSSTIM,1,"I")="":"",1:PSSHOSP(51.17,PSSTIM,1,"I"))
        PSSCNT = PSSCNT + 1
    ^TMP($J,LIST,+PSSIEN,"HOSPITAL LOCATION",0) = $S(PSSCNT>0:PSSCNT,1:"-1^" + "NO DATA FOUND")


def IX():
    global PSSPP, PSSFT, LIST, PSSIEN
    LIST = "^TMP($J,LIST)"
    ^TMP($J,LIST) = {}
    if PSSPP == "":
        ^TMP($J,LIST,0) = -1 + "^" + "NO DATA FOUND"
        return
    if PSSFT == "":
        ^TMP($J,LIST,0) = -1 + "^" + "NO DATA FOUND"
        return
    if PSSPP != "" and PSSFT != "":
        if PSSFT["??":
            LOOP^PSS51P1B(6)
            return
        $$FIND^DIC(51.1,,"@;.01","QP",PSSFT,,"AP"_PSSPP,,,"")
        if int(^TMP("DILIST",$J,0)) <= 0:
            ^TMP($J,LIST,0) = -1 + "^" + "NO DATA FOUND"
            return
        if int(^TMP("DILIST",$J,0)) > 0:
            ^TMP($J,LIST,0) = +^TMP("DILIST",$J,0)
            PSSXX = 0
            CNT = 0
            while PSSXX in ^TMP("DILIST",$J,PSSXX):
                PSSIEN = +^TMP("DILIST",$J,PSSXX,0)
                PSS51P1 = {}
                $$GETS^DIQ(51.1, +PSSIEN, ".01;1;2;2.5;4;5;6;8;8.1","IE","PSS51P1")
                PSSXX = 0
                while PSSXX in PSS51P1(51.1):
                    ^TMP($J,LIST,+PSSXX,.01) = $G(PSS51P1(51.1,PSSXX,.01,"E"))
                    ^TMP($J,LIST,"AP"_PSSPP,$G(PSS51P1(51.1,PSSXX,.01,"E")),+PSSXX) = ""
                    ^TMP($J,LIST,+PSSXX,1) = $G(PSS51P1(51.1,PSSXX,1,"E"))
                    ^TMP($J,LIST,+PSSXX,2) = $G(PSS51P1(51.1,PSSXX,2,"E"))
                    ^TMP($J,LIST,+PSSXX,2.5) = $G(PSS51P1(51.1,PSSXX,2.5,"E"))
                    ^TMP($J,LIST,+PSSXX,4) = $G(PSS51P1(51.1,PSSXX,4,"E"))
                    ^TMP($J,LIST,+PSSXX,5) = $S($G(PSS51P1(51.1,PSSXX,5,"I"))'="":$G(PSS51P1(51.1,PSSXX,5,"I")) + "^" + $G(PSS51P1(51.1,PSSXX,5,"E")),"")
                    ^TMP($J,LIST,+PSSXX,6) = $G(PSS51P1(51.1,PSSXX,6,"E"))
                    ^TMP($J,LIST,+PSSXX,8) = $G(PSS51P1(51.1,PSSXX,8,"E"))
                    ^TMP($J,LIST,+PSSXX,8.1) = $G(PSS51P1(51.1,PSSXX,8.1,"E"))
                    CNT = CNT + 1
                ^TMP($J,LIST,0) = $S(CNT>0:CNT,1:"-1^" + "NO DATA FOUND")
    K PSS51P1
    K ^TMP("DILIST",$J)


def IEN():
    global PSSFT, LIST
    LIST = "^TMP($J,LIST)"
    ^TMP($J,LIST) = {}
    if PSSFT != "":
        if PSSFT["??":
            LOOP^PSS51P1B(4)
            return
        $$FIND^DIC(51.1,,"@;.01;1","QP",PSSFT,,"B",,,"PSS51P1")
        if +PSS51P1("DILIST",0) == 0:
            ^TMP($J,LIST,0) = -1 + "^" + "NO DATA FOUND"
            return
        if +PSS51P1("DILIST",0) > 0:
            ^TMP($J,LIST,0) = +PSS51P1("DILIST",0)
            PSSXX = 0
            while PSSXX in PSS51P1("DILIST",PSSXX):
                ^TMP($J,LIST,+$G(PSS51P1("DILIST",PSSXX,0)),.01) = $P($G(PSS51P1("DILIST",PSSXX,0)),"^",2)
                ^TMP($J,LIST,+$G(PSS51P1("DILIST",PSSXX,0)),1) = $P($G(PSS51P1("DILIST",PSSXX,0)),"^",3)
                ^TMP($J,LIST,"B",$P($G(PSS51P1("DILIST",PSSXX,0)),"^",2),+$G(PSS51P1("DILIST",PSSXX,0))) = ""
    K ^TMP("DILIST",$J)