# PSS52P6A ;BIR/LDT - SETS ARRAYS AND INACTIVE SCREEN CALLED FROM PSS52P6; 5 Sep 03
# 1.0;PHARMACY DATA MANAGEMENT;**85**;9/30/97

def SETSCRN():
    # Naked reference below refers to ^PS(52.6,+Y,"I")
    SCR_S = "S ND=$P($G(^(""I"")),U) I ND=""""!(ND>PSSFL)"
    return

def SETZRO():
    global PSS52P6, PSS, LIST
    LIST = "^TMP($J,LIST"
    ^TMP($J,LIST,+PSS(1),.01) = $G(PSS52P6(52.6,PSS(1),.01,"I"))
    ^TMP($J,LIST,"B",$G(PSS52P6(52.6,PSS(1),.01,"I")),+PSS(1)) = ""
    ^TMP($J,LIST,+PSS(1),1) = $S($G(PSS52P6(52.6,PSS(1),1,"I"))=="":"",$G(PSS52P6(52.6,PSS(1),1,"I"))+"^"+$G(PSS52P6(52.6,PSS(1),1,"E")))
    ^TMP($J,LIST,+PSS(1),2) = $S($G(PSS52P6(52.6,PSS(1),2,"I"))=="":"",$G(PSS52P6(52.6,PSS(1),2,"I"))+"^"+$G(PSS52P6(52.6,PSS(1),2,"E")))
    ^TMP($J,LIST,+PSS(1),3) = $G(PSS52P6(52.6,PSS(1),3,"I"))
    ^TMP($J,LIST,+PSS(1),4) = $G(PSS52P6(52.6,PSS(1),4,"I"))
    ^TMP($J,LIST,+PSS(1),5) = $G(PSS52P6(52.6,PSS(1),5,"I"))
    ^TMP($J,LIST,+PSS(1),7) = $G(PSS52P6(52.6,PSS(1),7,"I"))
    ^TMP($J,LIST,+PSS(1),14) = $G(PSS52P6(52.6,PSS(1),14,"I"))
    ^TMP($J,LIST,+PSS(1),13) = $G(PSS52P6(52.6,PSS(1),13,"I"))
    ^TMP($J,LIST,+PSS(1),15) = $S($G(PSS52P6(52.6,PSS(1),15,"I"))=="":"",$G(PSS52P6(52.6,PSS(1),15,"I"))+"^"+$G(PSS52P6(52.6,PSS(1),15,"E")))
    ^TMP($J,LIST,+PSS(1),17) = $S($G(PSS52P6(52.6,PSS(1),17,"I"))=="":"",$G(PSS52P6(52.6,PSS(1),17,"I"))+"^"+$G(PSS52P6(52.6,PSS(1),17,"E")))
    ^TMP($J,LIST,+PSS(1),12) = $S($G(PSS52P6(52.6,PSS(1),12,"I"))=="":"",$G(PSS52P6(52.6,PSS(1),12,"I"))+"^"+$G(PSS52P6(52.6,PSS(1),12,"E")))
    return

def SETZRO2():
    global PSS, LIST
    LIST = "^TMP($J,LIST"
    ^TMP($J,LIST,+PSS(1),.01) = $G(^TMP("PSS52P6",$J,52.6,PSS(1),.01,"I"))
    ^TMP($J,LIST,"B",$G(^TMP("PSS52P6",$J,52.6,PSS(1),.01,"I")),+PSS(1)) = ""
    ^TMP($J,LIST,+PSS(1),14) = $G(^TMP("PSS52P6",$J,52.6,PSS(1),14,"I"))
    return

def SETQCD():
    global PSS, LIST, PSSIEN
    LIST = "^TMP($J,LIST"
    ^TMP($J,LIST,+PSSIEN,"QCODE",+PSS(1),.01) = $G(^TMP("PSS52P6",$J,52.61,PSS(1),.01,"I"))
    ^TMP($J,LIST,+PSSIEN,"QCODE",+PSS(1),1) = $G(^TMP("PSS52P6",$J,52.61,PSS(1),1,"I"))
    ^TMP($J,LIST,+PSSIEN,"QCODE",+PSS(1),2) = $G(^TMP("PSS52P6",$J,52.61,PSS(1),2,"I"))
    ^TMP($J,LIST,+PSSIEN,"QCODE",+PSS(1),3) = $G(^TMP("PSS52P6",$J,52.61,PSS(1),3,"I"))
    ^TMP($J,LIST,+PSSIEN,"QCODE",+PSS(1),4) = $G(^TMP("PSS52P6",$J,52.61,PSS(1),4,"I"))
    ^TMP($J,LIST,+PSSIEN,"QCODE",+PSS(1),5) = $G(^TMP("PSS52P6",$J,52.61,PSS(1),5,"I"))
    ^TMP($J,LIST,+PSSIEN,"QCODE",+PSS(1),6) = $S($G(^TMP("PSS52P6",$J,52.61,PSS(1),6,"I"))=="":"",$G(^TMP("PSS52P6",$J,52.61,PSS(1),6,"I"))+"^"+^TMP("PSS52P6",$J,52.61,PSS(1),6,"E"))
    ^TMP($J,LIST,+PSSIEN,"QCODE",+PSS(1),7) = $S($G(^TMP("PSS52P6",$J,52.61,PSS(1),7,"I"))=="":"",$G(^TMP("PSS52P6",$J,52.61,PSS(1),7,"I"))+"^"+^TMP("PSS52P6",$J,52.61,PSS(1),7,"E"))
    return

def SETQCD2():
    global PSS, LIST, PSSIEN
    LIST = "^TMP($J,LIST"
    ^TMP($J,LIST,+PSSIEN,"QCODE",+PSS(2),.01) = $G(^TMP("PSS52P6",$J,52.61,PSS(2),.01,"I"))
    return

def SETLTS():
    global PSS, LIST, PSSIEN
    LIST = "^TMP($J,LIST"
    ^TMP($J,LIST,+PSSIEN,"ELYTES",+PSS(1),.01) = $S($G(^TMP("PSS52P6",$J,52.62,PSS(1),.01,"I"))=="":"",$G(^TMP("PSS52P6",$J,52.62,PSS(1),.01,"I"))+"^"+^TMP("PSS52P6",$J,52.62,PSS(1),.01,"E"))
    ^TMP($J,LIST,+PSSIEN,"ELYTES",+PSS(1),1) = $G(^TMP("PSS52P6",$J,52.62,PSS(1),1,"I"))
    return

def SETSYN():
    global PSS, LIST, PSSIEN
    LIST = "^TMP($J,LIST"
    ^TMP($J,LIST,+PSSIEN,"SYN",+PSS(1),.01) = $G(^TMP("PSS52P6",$J,52.63,PSS(1),.01,"I"))
    return

def SETSYN2():
    global PSS, LIST, PSSIEN
    LIST = "^TMP($J,LIST"
    ^TMP($J,LIST,+PSSIEN,"SYN",+PSS(3),.01) = $G(^TMP("PSS52P6",$J,52.63,PSS(3),.01,"I"))
    return

def SETDRI():
    global PSS, LIST, PSSIEN
    LIST = "^TMP($J,LIST"
    ^TMP($J,LIST,+PSS(1),"DRGINF",+PSS(3),.01) = $G(^TMP("PSS52P6",$J,52.6,PSS(1),10,PSS(3)))
    return

def SETIACT():
    global PSS, LIST
    LIST = "^TMP($J,LIST"
    ^TMP($J,LIST,+PSS(1),12) = $S($G(PSS52P6(52.6,PSS(1),12,"I"))=="":"",$G(PSS52P6(52.6,PSS(1),12,"I"))+"^"+PSS52P6(52.6,PSS(1),12,"E"))
    return

def LOOP(PSSNUM):
    global PSS, LIST, PSSFL, CNT
    CNT = 0
    PSS(2) = 0
    while PSS(2):
        PSS(2) = $O(^PS(52.6,PSS(2)))
        if not PSS(2): break
        if PSSNUM == 1:
            PSSIEN = +PSS(2)
            K PSS52P6
            ND = $P($G(^PS(52.6,+PSSIEN,"I")),U)
            if ND == "" or (ND > PSSFL):
                GETS^DIQ(52.6,+PSSIEN,".01;1;2;3;4;5;7;12;13;14;15;17","IE","PSS52P6")
                PSS(1) = 0
                while PSS(1):
                    PSS(1) = $O(PSS52P6(52.6,PSS(1)))
                    if not PSS(1): break
                    SETZRO()
                    CNT = CNT + 1
        elif PSSNUM == 2:
            PSSIEN = +PSS(2)
            K ^TMP("PSS52P6",$J)
            ND = $P($G(^PS(52.6,+PSSIEN,"I")),U)
            if ND == "" or (ND > PSSFL):
                GETS^DIQ(52.6,+PSSIEN,".01;6*","IE","^TMP(""PSS52P6"",$J)")
                PSS(3) = 0
                while PSS(3):
                    PSS(3) = $O(^TMP("PSS52P6",$J,52.6,PSS(3)))
                    if not PSS(3): break
                    ^TMP($J,LIST,+PSSIEN,.01) = $G(^TMP("PSS52P6",$J,52.6,PSS(3),.01,"I"))
                    ^TMP($J,LIST,"B",$G(^TMP("PSS52P6",$J,52.6,PSS(3),.01,"E")),+PSSIEN) = ""
                    CNT = CNT + 1
                if not $D(^TMP("PSS52P6",$J,52.61)):
                    ^TMP($J,LIST,+PSSIEN,"QCODE",0) = "-1^NO DATA FOUND"
                PSS(1) = 0
                CNT2 = 0
                while PSS(1):
                    PSS(1) = $O(^TMP("PSS52P6",$J,52.61,PSS(1)))
                    if not PSS(1): break
                    SETQCD()
                    CNT2 = CNT2 + 1
                ^TMP($J,LIST,+PSSIEN,"QCODE",0) = $S(CNT2>0:CNT2,1:"-1^NO DATA FOUND")
        elif PSSNUM == 3:
            PSSIEN = +PSS(2)
            K ^TMP("PSS52P6",$J)
            ND = $P($G(^PS(52.6,+PSSIEN,"I")),U)
            if ND == "" or (ND > PSSFL):
                GETS^DIQ(52.6,+PSSIEN,".01;8*","IE","^TMP(""PSS52P6"",$J)")
                PSS(3) = 0
                while PSS(3):
                    PSS(3) = $O(^TMP("PSS52P6",$J,52.6,PSS(3)))
                    if not PSS(3): break
                    ^TMP($J,LIST,+PSSIEN,.01) = $G(^TMP("PSS52P6",$J,52.6,PSS(3),.01,"I"))
                    ^TMP($J,LIST,"B",$G(^TMP("PSS52P6",$J,52.6,PSS(3),.01,"E")),+PSSIEN) = ""
                    CNT = CNT + 1
                    PSS(1) = 0
                    CNT2 = 0
                    while PSS(1):
                        PSS(1) = $O(^TMP("PSS52P6",$J,52.62,PSS(1)))
                        if not PSS(1): break
                        SETLTS()
                        CNT2 = CNT2 + 1
                    ^TMP($J,LIST,+PSSIEN,"ELYTES",0) = $S(CNT2>0:CNT2,1:"-1^NO DATA FOUND")
        elif PSSNUM == 4:
            PSSIEN = +PSS(2)
            K ^TMP("PSS52P6",$J)
            ND = $P($G(^PS(52.6,+PSSIEN,"I")),U)
            if ND == "" or (ND > PSSFL):
                GETS^DIQ(52.6,+PSSIEN,".01;9*","IE","^TMP(""PSS52P6"",$J)")
                PSS(3) = 0
                while PSS(3):
                    PSS(3) = $O(^TMP("PSS52P6",$J,52.6,PSS(3)))
                    if not PSS(3): break
                    ^TMP($J,LIST,+PSSIEN,.01) = $G(^TMP("PSS52P6",$J,52.6,PSS(3),.01,"I"))
                    ^TMP($J,LIST,"B",$G(^TMP("PSS52P6",$J,52.6,PSS(3),.01,"E")),+PSSIEN) = ""
                    CNT = CNT + 1
                    PSS(1) = 0
                    CNT2 = 0
                    while PSS(1):
                        PSS(1) = $O(^TMP("PSS52P6",$J,52.63,PSS(1)))
                        if not PSS(1): break
                        SETSYN()
                        CNT2 = CNT2 + 1
                    ^TMP($J,LIST,+PSSIEN,"SYN",0) = $S(CNT2>0:CNT2,1:"-1^NO DATA FOUND")
        elif PSSNUM == 5:
            PSSIEN = +PSS(2)
            K ^TMP("PSS52P6",$J)
            ND = $P($G(^PS(52.6,+PSSIEN,"I")),U)
            if ND == "" or (ND > PSSFL):
                GETS^DIQ(52.6,+PSSIEN,".01;10","E","^TMP(""PSS52P6"",$J)")
                PSS(1) = 0
                while PSS(1):
                    PSS(1) = $O(^TMP("PSS52P6",$J,52.6,PSS(1)))
                    if not PSS(1): break
                    ^TMP($J,LIST,+PSS(1),.01) = $G(^TMP("PSS52P6",$J,52.6,PSS(1),.01,"E"))
                    ^TMP($J,LIST,"B",$G(^TMP("PSS52P6",$J,52.6,PSS(1),.01,"E")),+PSS(1)) = ""
                    CNT = CNT + 1
                    PSS(3) = 0
                    CNT2 = 0
                    while PSS(3):
                        PSS(3) = $O(^TMP("PSS52P6",$J,52.6,PSS(1),10,PSS(3)))
                        if not PSS(3): break
                        SETDRI()
                        CNT2 = CNT2 + 1
                    ^TMP($J,LIST,+PSSIEN,"DRGINF",0) = $S(CNT2>0:CNT2,1:"-1^NO DATA FOUND")
    ^TMP($J,LIST,0) = $S(CNT>0:CNT,1:"-1^NO DATA FOUND")
    return

def PSS52P6A_1():
    global PSS, LIST, PSSFL, PSSIEN
    PSSIEN = +PSS(2)
    K PSS52P6
    ND = $P($G(^PS(52.6,+PSSIEN,"I")),U)
    if ND == "" or (ND > $G(PSSFL)):
        GETS^DIQ(52.6,+PSSIEN,".01;1;2;3;4;5;7;12;13;14;15;17","IE","PSS52P6")
        PSS(1) = 0
        while PSS(1):
            PSS(1) = $O(PSS52P6(52.6,PSS(1)))
            if not PSS(1): break
            SETZRO()
            CNT = CNT + 1
    return

def PSS52P6A_2():
    global PSS, LIST, PSSFL, PSSIEN
    PSSIEN = +PSS(2)
    K ^TMP("PSS52P6",$J)
    ND = $P($G(^PS(52.6,+PSSIEN,"I")),U)
    if ND == "" or (ND > $G(PSSFL)):
        GETS^DIQ(52.6,+PSSIEN,".01;6*","IE","^TMP(""PSS52P6"",$J)")
        PSS(3) = 0
        while PSS(3):
            PSS(3) = $O(^TMP("PSS52P6",$J,52.6,PSS(3)))
            if not PSS(3): break
            ^TMP($J,LIST,+PSSIEN,.01) = $G(^TMP("PSS52P6",$J,52.6,PSS(3),.01,"I"))
            ^TMP($J,LIST,"B",$G(^TMP("PSS52P6",$J,52.6,PSS(3),.01,"E")),+PSSIEN) = ""
            CNT = CNT + 1
        if not $D(^TMP("PSS52P6",$J,52.61)):
            ^TMP($J,LIST,+PSSIEN,"QCODE",0) = "-1^NO DATA FOUND"
        PSS(1) = 0
        CNT2 = 0
        while PSS(1):
            PSS(1) = $O(^TMP("PSS52P6",$J,52.61,PSS(1)))
            if not PSS(1): break
            SETQCD()
            CNT2 = CNT2 + 1
        ^TMP($J,LIST,+PSSIEN,"QCODE",0) = $S(CNT2>0:CNT2,1:"-1^NO DATA FOUND")
    return

def PSS52P6A_3():
    global PSS, LIST, PSSFL, PSSIEN
    PSSIEN = +PSS(2)
    K ^TMP("PSS52P6",$J)
    ND = $P($G(^PS(52.6,+PSSIEN,"I")),U)
    if ND == "" or (ND > $G(PSSFL)):
        GETS^DIQ(52.6,+PSSIEN,".01;8*","IE","^TMP(""PSS52P6"",$J)")
        PSS(3) = 0
        while PSS(3):
            PSS(3) = $O(^TMP("PSS52P6",$J,52.6,PSS(3)))
            if not PSS(3): break
            ^TMP($J,LIST,+PSSIEN,.01) = $G(^TMP("PSS52P6",$J,52.6,PSS(3),.01,"I"))
            ^TMP($J,LIST,"B",$G(^TMP("PSS52P6",$J,52.6,PSS(3),.01,"E")),+PSSIEN) = ""
            CNT = CNT + 1
            PSS(1) = 0
            CNT2 = 0
            while PSS(1):
                PSS(1) = $O(^TMP("PSS52P6",$J,52.62,PSS(1)))
                if not PSS(1): break
                SETLTS()
                CNT2 = CNT2 + 1
            ^TMP($J,LIST,+PSSIEN,"ELYTES",0) = $S(CNT2>0:CNT2,1:"-1^NO DATA FOUND")
    return

def PSS52P6A_4():
    global PSS, LIST, PSSFL, PSSIEN
    PSSIEN = +PSS(2)
    K ^TMP("PSS52P6",$J)
    ND = $P($G(^PS(52.6,+PSSIEN,"I")),U)
    if ND == "" or (ND > $G(PSSFL)):
        GETS^DIQ(52.6,+PSSIEN,".01;9*","IE","^TMP(""PSS52P6"",$J)")
        PSS(1) = 0
        while PSS(1):
            PSS(1) = $O(^TMP("PSS52P6",$J,52.63,PSS(1)))
            if not PSS(1): break
            SETSYN()
            CNT2 = CNT2 + 1
        PSS(3) = 0
        while PSS(3):
            PSS(3) = $O(^TMP("PSS52P6",$J,52.6,PSS(3)))
            if not PSS(3): break
            ^TMP($J,LIST,+PSSIEN,.01) = $G(^TMP("PSS52P6",$J,52.6,PSS(3),.01,"I"))
            ^TMP($J,LIST,"B",$G(^TMP("PSS52P6",$J,52.6,PSS(3),.01,"E")),+PSSIEN) = ""
            CNT = CNT + 1
        ^TMP($J,LIST,+PSSIEN,"SYN",0) = $S(CNT2>0:CNT2,1:"-1^NO DATA FOUND")
    return

def PSS52P6A_5():
    global PSS, LIST, PSSFL, PSSIEN
    PSSIEN = +PSS(2)
    K ^TMP("PSS52P6",$J)
    ND = $P($G(^PS(52.6,+PSSIEN,"I")),U)
    if ND == "" or (ND > $G(PSSFL)):
        GETS^DIQ(52.6,+PSSIEN,".01;10","E","^TMP(""PSS52P6"",$J)")
        PSS(1) = 0
        while PSS(1):
            PSS(1) = $O(^TMP("PSS52P6",$J,52.6,PSS(1)))
            if not PSS(1): break
            ^TMP($J,LIST,+PSS(1),.01) = $G(^TMP("PSS52P6",$J,52.6,PSS(1),.01,"E"))
            ^TMP($J,LIST,"B",$G(^TMP("PSS52P6",$J,52.6,PSS(1),.01,"E")),+PSS(1)) = ""
            CNT = CNT + 1
            PSS(3) = 0
            CNT2 = 0
            while PSS(3):
                PSS(3) = $O(^TMP("PSS52P6",$J,52.6,PSS(1),10,PSS(3)))
                if not PSS(3): break
                SETDRI()
                CNT2 = CNT2 + 1
            ^TMP($J,LIST,+PSSIEN,"DRGINF",0) = $S(CNT2>0:CNT2,1:"-1^NO DATA FOUND")
    return

def QCODE():
    global PSS, LIST, PSSFL, PSSIEN, PSSFT
    LIST = "^TMP($J,LIST"
    if $G(PSSFL) > 0:
        N ND
        ND = ""
        SETSCRN()
    if +$G(PSSIEN) > 0:
        N PSSIEN2
        S PSSIEN2 = $$FIND1^DIC(52.6,"","A","`"_PSSIEN,,SCR("S"),"")
        if +PSSIEN2 <= 0:
            ^TMP($J,LIST,0) = -1 + "^" + "NO DATA FOUND"
        else:
            ^TMP($J,LIST,0) = 1
            GETS^DIQ(52.6,+PSSIEN2,".01;6*","IE","^TMP(""PSS52P6"",$J)")
            PSS(1) = 0
            while PSS(1):
                PSS(1) = $O(^TMP("PSS52P6",$J,52.6,PSS(1)))
                if not PSS(1): break
                ^TMP($J,LIST,+PSSIEN2,.01) = ^TMP("PSS52P6",$J,52.6,PSS(1),.01,"I")
                ^TMP($J,LIST,"B",^TMP("PSS52P6",$J,52.6,PSS(1),.01,"I"),+PSSIEN2) = ""
            N CNT
            S (PSS(1),CNT) = 0
            while PSS(1):
                PSS(1) = $O(^TMP("PSS52P6",$J,52.61,PSS(1)))
                if not PSS(1): break
                SETQCD()
                S CNT = CNT + 1
            ^TMP($J,LIST,+PSSIEN,"QCODE",0) = $S(CNT>0:CNT,1:"-1^NO DATA FOUND")
    elif +$G(PSSIEN)'>0,$G(PSSFT)]"":
        if PSSFT["??":
            LOOP^PSS52P6A(2)
        else:
            FIND^DIC(52.6,,"@;.01;2","QP",PSSFT,,"B^C",SCR("S"),,"")
            if +$G(^TMP("DILIST",$J,0))=0:
                ^TMP($J,LIST,0) = -1 + "^" + "NO DATA FOUND"
            elif +^TMP("DILIST",$J,0)>0:
                ^TMP($J,LIST,0) = +^TMP("DILIST",$J,0)
                S PSSXX = 0
                while PSSXX:
                    PSSXX = $O(^TMP("DILIST",$J,PSSXX))
                    if not PSSXX: break
                    PSSIEN = +^TMP("DILIST",$J,PSSXX,0)
                    K ^TMP("PSS52P6",$J)
                    GETS^DIQ(52.6,+PSSIEN,"6*","IE","^TMP(""PSS52P6"",$J)")
                    ^TMP($J,LIST,+PSSIEN,.01) = $P(^TMP("DILIST",$J,PSSXX,0),"^",2)
                    ^TMP($J,LIST,"B",$P(^TMP("DILIST",$J,PSSXX,0),"^",2),+PSSIEN) = ""
                    N CNT
                    S (PSS(1),CNT) = 0
                    while PSS(1):
                        PSS(1) = $O(^TMP("PSS52P6",$J,52.61,PSS(1)))
                        if not PSS(1): break
                        SETQCD()
                        S CNT = CNT + 1
                    ^TMP($J,LIST,+PSSIEN,"QCODE",0) = $S(CNT>0:CNT,1:"-1^NO DATA FOUND")
    K ^TMP("DILIST",$J),^TMP("PSS52P6",$J)
    return

SETSCRN()
SETZRO()
SETZRO2()
SETQCD()
SETQCD2()
SETLTS()
SETSYN()
SETSYN2()
SETDRI()
SETIACT()
LOOP(1)
LOOP(2)
LOOP(3)
LOOP(4)
LOOP(5)
PSS52P6A_1()
PSS52P6A_2()
PSS52P6A_3()
PSS52P6A_4()
PSS52P6A_5()
QCODE()