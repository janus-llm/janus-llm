def PSS50LAB(PSSIEN, PSSFT, PSSFL, PSSPK, PSSRTOI, LIST):
    """
    BIR/LDT - API FOR LAB INFORMATION FROM FILE 50; 5 Sep 03
    Version: 1.0
    """
    import os
    import tempfile
    import subprocess
    
    # PSSIEN - IEN of entry in 50
    # PSSFT - Free Text name in 50
    # PSSFL - Inactive flag - "" - All entries
    #                        FileMan Date - Only entries with no Inactive Date or an Inactive Date greater than this date.
    # PSSPK - Application Package's Use - "" - All entries
    #                                     Alphabetic codes that represent the DHCP packages that consider this drug to be
    #                                     part of their formulary.
    # PSSRTOI - Orderable Item - return only entries matched to a Pharmacy Orderable Item                                   
    # LIST - Subscript of ^TMP array in the form ^TMP($J,LIST,Field Number where Field Number is the Field Number of the data
    #        piece being returned.
    DIERR = None
    ZZERR = None
    PSSP50 = None
    SCR = {}
    PSS = {}
    PSSMLCT = None
    
    if LIST == "":
        return
    
    tmp_file = os.path.join(tempfile.gettempdir(), "PSSP50.tmp")
    if os.path.exists(tmp_file):
        os.remove(tmp_file)
    
    with open(tmp_file, "w") as f:
        f.write("")
    
    if (PSSIEN is None or PSSIEN <= 0) and (PSSFT is None or PSSFT == ""):
        return [-1, "NO DATA FOUND"]
    
    SCR["S"] = ""
    
    if (PSSFL is not None and PSSFL > 0) or (PSSPK is not None and PSSPK != "") or (PSSRTOI == 1):
        PSS5ND = None
        PSSZ3 = None
        PSSZ4 = None
        SETSCRN(PSS5ND, PSSZ3, PSSZ4)
    
    if PSSIEN is not None and PSSIEN > 0:
        PSSIEN2 = FIND1(50, "`" + str(PSSIEN), "", SCR["S"], "")
        if PSSIEN2 <= 0:
            return [-1, "NO DATA FOUND"]
        
        PSSP50 = GETS(50, PSSIEN2, ".01;17.2:17.6", "IE", tmp_file)
        with open(tmp_file, "r") as f:
            lines = f.readlines()
            if len(lines) > 0:
                PSS[1] = 0
                for line in lines:
                    PSS[1] = PSS[1] + 1
                    SETLAB(line)
    
    if PSSIEN != "":
        return [-1, "NO DATA FOUND"]
    
    if PSSFT != "":
        if "??":
            LOOP()
        else:
            FIND(50, "@;.01", "QP", PSSFT, "", "B", SCR["S"], "", "", tmp_file)
            with open(tmp_file, "r") as f:
                lines = f.readlines()
                if len(lines) > 0:
                    PSSXX = 0
                    for line in lines:
                        PSSXX = PSSXX + 1
                        PSSIEN = int(line.split("^")[0])
                        PSSP50 = GETS(50, PSSIEN, ".01;17.2:17.6", "IE", tmp_file)
                        with open(tmp_file, "r") as f:
                            lines = f.readlines()
                            if len(lines) > 0:
                                PSS[1] = 0
                                for line in lines:
                                    PSS[1] = PSS[1] + 1
                                    SETLAB(line)
    
    os.remove(tmp_file)
    return

def SETLAB(line):
    """
    Helper function for PSS50LAB
    """
    data = line.split("^")
    PSS[1] = data[0]
    ^TMP(J,LIST,+PSS(1),.01) = data[1]
    ^TMP(J,LIST,"B",data[1],+PSS(1)) = ""
    ^TMP(J,LIST,+PSS(1),17.2) = data[2] + "^" + data[3]
    ^TMP(J,LIST,+PSS(1),17.3) = data[4]
    ^TMP(J,LIST,+PSS(1),17.4) = data[5] + "^" + data[6]
    ^TMP(J,LIST,+PSS(1),17.5) = data[7]
    ^TMP(J,LIST,+PSS(1),17.6) = data[8] + "^" + data[9]
    return

def LOOP():
    """
    Helper function for PSS50LAB
    """
    PSS50D12 = None
    PSS50E12 = None
    PSS176D = None
    FIELD(50, 17.6, "Z", "POINTER", PSS50D12, PSS50E12)
    PSS176D = PSS50D12["POINTER"]
    PSSENCT = 0
    
    PSS[1] = 0
    while True:
        PSS[1] = PSS[1] + 1
        if PSS[1] not in range(1, len(PSDRUG)):
            break
        if PSDRUG[PSS[1]] == "":
            continue
        if PSSFL is not None and PSDRUG[PSS[1]]["I"] != "" and PSDRUG[PSS[1]]["I"] <= PSSFL:
            continue
        if PSSRTOI == 1 and PSDRUG[PSS[1]]["2"] == "":
            continue
        PSSZ5 = 0
        for PSSZ6 in range(1, len(PSSPK)):
            if PSDRUG[PSS[1]]["2"]["3"].find(PSSPK[PSSZ6]) != -1:
                PSSZ5 = 1
                break
        if PSSPK != "" and not PSSZ5:
            continue
        SETLABL()
        PSSENCT = PSSENCT + 1
    
    return [PSSENCT, "NO DATA FOUND"]

def SETLABL():
    """
    Helper function for LOOP
    """
    PSSZNODE = PSDRUG[PSS[1]]
    PSS50CL = PSSZNODE["CLOZ"]
    PSS50CL1 = PSSZNODE["CLOZ1"]
    ^TMP(J,LIST,+PSS(1),.01) = PSSZNODE
    ^TMP(J,LIST,"B",PSSZNODE,+PSS(1)) = ""
    PSSCLZAR = GETS(50, +PSS[1], "17.2;17.4", "IE")
    ^TMP(J,LIST,+PSS(1),17.2) = PSSCLZAR[+PSS[1]]["17.2"]["I"] + "^" + PSSCLZAR[+PSS[1]]["17.2"]["E"]
    ^TMP(J,LIST,+PSS(1),17.3) = PSS50CL["2"]
    ^TMP(J,LIST,+PSS(1),17.4) = PSSCLZAR[+PSS[1]]["17.4"]["I"] + "^" + PSSCLZAR[+PSS[1]]["17.4"]["E"]
    ^TMP(J,LIST,+PSS(1),17.5) = PSS50CL1
    PSS176 = PSS50CL1["2"]
    if PSS176 != "" and PSS176D != "" and PSS176D.find(PSS176 + ":") != -1:
        ^TMP(J,LIST,+PSS(1),17.6) = PSS176 + "^" + PSS176D[PSS176D.find(PSS176 + ":"):].split(";")[0]
    else:
        ^TMP(J,LIST,+PSS(1),17.6) = ""
    
    return

PSS50LAB(PSSIEN, PSSFT, PSSFL, PSSPK, PSSRTOI, LIST)