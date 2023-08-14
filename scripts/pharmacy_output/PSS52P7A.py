# BIR/LDT - API FOR INFORMATION FROM FILE 52.7; 5 Sep 03
# 1.0;PHARMACY DATA MANAGEMENT;**85,91**;9/30/97

def SETZERO():
    global LIST, PSS, PSS52P7
    LIST = "TMP"
    PSS = [0, 0]
    PSS52P7 = {}
    PSS52P7[52.7, PSS[1], .01, "I"] = PSS52P7[52.7, PSS[1], .01, "I"]
    PSS52P7[52.7, PSS[1], .01, "I"] = PSS52P7[52.7, PSS[1], .01, "I"]
    PSS52P7[52.7, PSS[1], .01, "I"] = PSS52P7[52.7, PSS[1], .01, "I"]
    PSS52P7[52.7, PSS[1], 1, "I"] = "" if PSS52P7[52.7, PSS[1], 1, "I"] == "" else PSS52P7[52.7, PSS[1], 1, "I"] + "^" + PSS52P7[52.7, PSS[1], 1, "E"]
    PSS52P7[52.7, PSS[1], 2, "I"] = PSS52P7[52.7, PSS[1], 2, "I"]
    PSS52P7[52.7, PSS[1], .02, "I"] = PSS52P7[52.7, PSS[1], .02, "I"]
    PSS52P7[52.7, PSS[1], 7, "I"] = PSS52P7[52.7, PSS[1], 7, "I"]
    PSS52P7[52.7, PSS[1], 9, "I"] = "" if PSS52P7[52.7, PSS[1], 9, "I"] == "" else PSS52P7[52.7, PSS[1], 9, "I"] + "^" + PSS52P7[52.7, PSS[1], 9, "E"]
    PSS52P7[52.7, PSS[1], 17] = "" if PSS52P7[52.7, PSS[1], 17, "I"] == "" else PSS52P7[52.7, PSS[1], 17, "I"] + "^" + PSS52P7[52.7, PSS[1], 17, "E"]
    PSS52P7[52.7, PSS[1], 8] = "" if PSS52P7[52.7, PSS[1], 8, "I"] == "" else PSS52P7[52.7, PSS[1], 8, "I"] + "^" + PSS52P7[52.7, PSS[1], 8, "E"]

def SETLTS():
    global LIST, PSSIEN, PSS
    LIST = "TMP"
    PSSIEN = ""
    PSS = [0, 0]
    PSS52P7[52.702, PSS[2], .01] = "" if PSS52P7[52.702, PSS[2], .01, "I"] == "" else PSS52P7[52.702, PSS[2], .01, "I"] + "^" + PSS52P7[52.702, PSS[2], .01, "E"]
    PSS52P7[52.702, PSS[2], 1] = PSS52P7[52.702, PSS[2], 1, "I"]

def SETLOOK():
    global LIST, PSS, PSS52P7
    LIST = "TMP"
    PSS = [0, 0]
    PSS52P7[52.7, PSS[1], .01] = PSS52P7[52.7, PSS[1], .01, "I"]
    PSS52P7["B", PSS52P7[52.7, PSS[1], .01, "I"], +PSS[1]] = ""
    PSS52P7[52.7, PSS[1], .02] = PSS52P7[52.7, PSS[1], .02, "I"]
    PSS52P7[52.7, PSS[1], 2] = PSS52P7[52.7, PSS[1], 2, "I"]

def LOOP(PSSLOOP):
    global CNT, PSSIEN, LIST, PSS, PSSFL, ND, PSS52P7
    CNT = 0
    PSSIEN = 0
    LIST = "TMP"
    PSS = [0, 0]
    PSSFL = ""
    ND = ""
    while PSSIEN:
        PSSIEN = PSSIEN + 1
        if PSSLOOP == "1":
            if PSSFL:
                ND = PSS52P7[+PSSIEN, "I"]
                if ND and +ND <= PSSFL:
                    continue
            PSS52P7[+PSSIEN, ".01;1;2;.02;7;8;9;17"] = ["IE"]
            PSS[1] = 0
            while PSS[1]:
                SETZERO()
                CNT = CNT + 1
                PSS52P7[+PSSIEN, "4*"] = ["IE"]
                PSS[2] = 0
                while PSS[2]:
                    SETLTS()
                    CNT2 = CNT2 + 1
                PSS52P7[+PSSIEN, "ELYTES", 0] = CNT2 if CNT2 > 0 else "-1^NO DATA FOUND"
        elif PSSLOOP == "2":
            PSS52P7[+PSSIEN, ".01;2;.02"] = ["IE"]
            PSS[1] = 0
            while PSS[1]:
                SETLOOK()
                CNT = CNT + 1
    PSS52P7[0] = CNT if CNT > 1 else "-1^NO DATA FOUND"