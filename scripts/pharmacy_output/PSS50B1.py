def PSS50B1():
    # BIR/LDT - API FOR INFORMATION FROM FILE 50; 5 Sep 03
    # 1.0;PHARMACY DATA MANAGEMENT;**85**;9/30/97

    # LOOP
    PSS50DD5 = None
    PSS50ER5 = None
    PSS501NX = None
    FIELD(50.1,1,"Z","POINTER",PSS50DD5,PSS50ER5)
    PSS501NX = PSS50DD5["POINTER"]
    
    PSSENCT = 0
    
    PSS_1 = 0
    while True:
        PSS_1 = PSS_1 + 1
        if PSS_1 is None:
            break
        
        if PSSENCT:
            if PSSFL:
                if PSSDRUG(PSS_1,"I"):
                    if PSSDRUG(PSS_1,"I") <= PSSFL:
                        continue
            
            if PSSRTOI:
                if not PSSDRUG(PSS_1,2):
                    continue
            
            # Naked reference below refers to ^PSDRUG(PSS(1),2)
            if PSSPK:
                PSSZ5 = 0
                PSSZ6 = 1
                while True:
                    PSSZ6 = PSSZ6 + 1
                    if PSSZ6 is None:
                        break
                    
                    if PSSZ5:
                        break
                    
                    if PSSDRUG(PSS_1,2):
                        if PSSDRUG(PSS_1,2,3):
                            if PSSDRUG(PSS_1,2,3).find(PSSPK[PSSZ6]) != -1:
                                PSSZ5 = 1
                
                if PSSPK:
                    if not PSSZ5:
                        continue
            
            SETSUB1(PSS_1)
            SETSUB4(PSS_1)
            SETINV()
            SETSYN2()
            SETIFC()
            PSSENCT = PSSENCT + 1
    
    if PSSENCT:
        ^TMP($J,LIST,0) = PSSENCT
    else:
        ^TMP($J,LIST,0) = "-1^NO DATA FOUND"

def SETINV():
    PSSZNODE = None
    PSS660 = None
    PSS6601 = None
    PSSZNODE = PSSDRUG(PSS_1,0)
    PSS660 = PSSDRUG(PSS_1,660)
    PSS6601 = PSSDRUG(PSS_1,660.1)
    
    ^TMP($J,LIST,PSS_1,.01) = PSSZNODE
    ^TMP($J,LIST,"B",PSSZNODE,PSS_1) = ""
    ^TMP($J,LIST,PSS_1,11) = PSS660
    ^TMP($J,LIST,PSS_1,12) = PSS660, PSSDIC(51.5, PSS660, 0), PSSDIC(0,2)
    ^TMP($J,LIST,PSS_1,13) = PSS660
    ^TMP($J,LIST,PSS_1,14) = PSS660
    ^TMP($J,LIST,PSS_1,15) = PSS660
    ^TMP($J,LIST,PSS_1,16) = PSS660
    ^TMP($J,LIST,PSS_1,17) = PSS660
    ^TMP($J,LIST,PSS_1,14.5) = PSS660
    Y = PSS660
    if Y:
        ^TMP($J,LIST,PSS_1,17.1) = Y
        ^DD("DD")
        ^TMP($J,LIST,PSS_1,17.1) = ^TMP($J,LIST,PSS_1,17.1) + Y
    else:
        ^TMP($J,LIST,PSS_1,17.1) = ""

    ^TMP($J,LIST,PSS_1,50) = PSS6601

def SETSYN2():
    PSS501C = 0
    
    if PSSDRUG(PSS_1,1):
        PSS501 = 0
        while True:
            PSS501 = PSS501 + 1
            if PSS501 is None:
                break

            PSS501ND = PSSDRUG(PSS_1,1,PSS501,0)
            if PSS501ND:
                if PSS501ND != "":
                    PSS501C = PSS501C + 1
                    ^TMP($J,LIST,PSS_1,"SYN",PSS501,.01) = PSS501ND
                    PSS501NN = PSS501ND, PSS501ND, 3
                    if PSS501NN:
                        if PSS501NX:
                            if PSS501NX.find(PSS501NN + ":") != -1:
                                ^TMP($J,LIST,PSS_1,"SYN",PSS501,1) = PSS501NN, PSS501NX[PSS501NX.find(PSS501NX.find(PSS501NN + ":")):] 
                            else:
                                ^TMP($J,LIST,PSS_1,"SYN",PSS501,1) = ""
                    ^TMP($J,LIST,PSS_1,"SYN",PSS501,2) = PSS501ND, 2
                    ^TMP($J,LIST,PSS_1,"SYN",PSS501,400) = PSS501ND, 4
                    ^TMP($J,LIST,PSS_1,"SYN",PSS501,401) = PSS501ND, 5, PSSDIC(51.5, PSS501ND, 0), PSSDIC(0,2)
                    ^TMP($J,LIST,PSS_1,"SYN",PSS501,402) = PSS501ND, 6
                    ^TMP($J,LIST,PSS_1,"SYN",PSS501,403) = PSS501ND, 7
                    ^TMP($J,LIST,PSS_1,"SYN",PSS501,404) = PSS501ND, 8
                    ^TMP($J,LIST,PSS_1,"SYN",PSS501,405) = PSS501ND, 9
    
    ^TMP($J,LIST,PSS_1,"SYN",0) = PSS501C if PSS501C else "-1^NO DATA FOUND"

def SETIFC():
    PSS441C = 0
    
    if PSSDRUG(PSS_1,441):
        PSS441 = 0
        while True:
            PSS441 = PSS441 + 1
            if PSS441 is None:
                break

            PSS441ND = PSSDRUG(PSS_1,441,PSS441,0)
            if PSS441ND:
                if PSS441ND != "":
                    PSS441C = PSS441C + 1
                    ^TMP($J,LIST,PSS_1,"IFC",PSS441,.01) = PSS441ND
    
    ^TMP($J,LIST,PSS_1,"IFC",0) = PSS441C if PSS441C else "-1^NO DATA FOUND"

def AVSN(PSSVAL, PSSFL, PSSPK, LIST):
    # PSSVAL - ITEM NUMBER sub-field (#.01) of the IFCAP ITEM NUMBER multiple of the DRUG file (#50)
    # PSSFL - Inactive flag - "" - All entries
    #                        FileMan Date - Only entries with no Inactive Date or an Inactive Date greater than this date.
    # PSSPK - Application Package's Use - "" - All entries
    #                                         Alphabetic codes that represent the DHCP packages that consider this drug to be
    #                                         part of their formulary.
    # LIST - Subscript of ^TMP array in the form ^TMP($J,LIST,Field Number where Field Number is the Field Number of the data
    #       piece being returned.
    # Returns zero node of 50
    if not LIST:
        return
    ^TMP($J,LIST) = ""

    if not PSSVAL:
        ^TMP($J,LIST,0) = "-1^NO DATA FOUND"
        return
    
    PSS = 0
    CNT = 0
    while True:
        PSS = PSS + 1
        if PSS is None:
            break
        
        if ^PSDRUG("AVSN", PSSVAL, PSS):
            if PSSFL:
                INODE = ^PSDRUG(PSS,2)
                if INODE:
                    if INODE <= PSSFL:
                        continue
            
            if PSSPK:
                # Naked reference below refers to ^PSDRUG(PSS,2)
                if ^PSDRUG(PSS,2,3):
                    if ^PSDRUG(PSS,2,3).find(PSSPK) != -1:
                        continue
            
            SETSUB1(PSS)
            SETSUB4(PSS)
            SETINV()
            SETSYN2()
            SETIFC()
            CNT = CNT + 1
    
    if CNT:
        ^TMP($J,LIST,0) = CNT
    else:
        ^TMP($J,LIST,0) = "-1^NO DATA FOUND"

def SETINV():
    PSSZNODE = None
    PSS660 = None
    PSS6601 = None
    PSSZNODE = ^PSDRUG(PSS,0)
    PSS660 = ^PSDRUG(PSS,660)
    PSS6601 = ^PSDRUG(PSS,660.1)
    
    ^TMP($J,LIST,PSS,.01) = PSSZNODE
    ^TMP($J,LIST,"B",PSSZNODE,PSS) = ""
    ^TMP($J,LIST,PSS,11) = PSS660
    ^TMP($J,LIST,PSS,12) = PSS660, ^DIC(51.5, PSS660, 0), ^DIC(0,2)
    ^TMP($J,LIST,PSS,13) = PSS660
    ^TMP($J,LIST,PSS,14) = PSS660
    ^TMP($J,LIST,PSS,15) = PSS660
    ^TMP($J,LIST,PSS,16) = PSS660
    ^TMP($J,LIST,PSS,17) = PSS660
    ^TMP($J,LIST,PSS,14.5) = PSS660
    Y = PSS660, 9
    if Y:
        ^TMP($J,LIST,PSS,17.1) = Y
        ^DD("DD")
        ^TMP($J,LIST,PSS,17.1) = ^TMP($J,LIST,PSS,17.1) + Y
    else:
        ^TMP($J,LIST,PSS,17.1) = ""

    ^TMP($J,LIST,PSS,50) = PSS6601

def SETSYN2():
    PSS501C = 0
    
    if ^PSDRUG(PSS,1):
        PSS501 = 0
        while True:
            PSS501 = PSS501 + 1
            if PSS501 is None:
                break

            PSS501ND = ^PSDRUG(PSS,1,PSS501,0)
            if PSS501ND:
                if PSS501ND != "":
                    PSS501C = PSS501C + 1
                    ^TMP($J,LIST,PSS,"SYN",PSS501,.01) = PSS501ND
                    PSS501NN = PSS501ND, 3
                    if PSS501NN:
                        if PSS501NX:
                            if PSS501NX.find(PSS501NN + ":") != -1:
                                ^TMP($J,LIST,PSS,"SYN",PSS501,1) = PSS501NN, PSS501NX[PSS501NX.find(PSS501NX.find(PSS501NN + ":")):] 
                            else:
                                ^TMP($J,LIST,PSS,"SYN",PSS501,1) = ""
                    ^TMP($J,LIST,PSS,"SYN",PSS501,2) = PSS501ND, 2
                    ^TMP($J,LIST,PSS,"SYN",PSS501,400) = PSS501ND, 4
                    ^TMP($J,LIST,PSS,"SYN",PSS501,401) = PSS501ND, 5, ^DIC(51.5, PSS501ND, 0), ^DIC(0,2)
                    ^TMP($J,LIST,PSS,"SYN",PSS501,402) = PSS501ND, 6
                    ^TMP($J,LIST,PSS,"SYN",PSS501,403) = PSS501ND, 7
                    ^TMP($J,LIST,PSS,"SYN",PSS501,404) = PSS501ND, 8
                    ^TMP($J,LIST,PSS,"SYN",PSS501,405) = PSS501ND, 9
    
    ^TMP($J,LIST,PSS,"SYN",0) = PSS501C if PSS501C else "-1^NO DATA FOUND"

def SETIFC():
    PSS441C = 0
    
    if ^PSDRUG(PSS,441):
        PSS441 = 0
        while True:
            PSS441 = PSS441 + 1
            if PSS441 is None:
                break

            PSS441ND = ^PSDRUG(PSS,441,PSS441,0)
            if PSS441ND:
                if PSS441ND != "":
                    PSS441C = PSS441C + 1
                    ^TMP($J,LIST,PSS,"IFC",PSS441,.01) = PSS441ND
    
    ^TMP($J,LIST,PSS,"IFC",0) = PSS441C if PSS441C else "-1^NO DATA FOUND"

def AVSN(PSSVAL, PSSFL, PSSPK, LIST):
    # PSSVAL - ITEM NUMBER sub-field (#.01) of the IFCAP ITEM NUMBER multiple of the DRUG file (#50)
    # PSSFL - Inactive flag - "" - All entries
    #                        FileMan Date - Only entries with no Inactive Date or an Inactive Date greater than this date.
    # PSSPK - Application Package's Use - "" - All entries
    #                                         Alphabetic codes that represent the DHCP packages that consider this drug to be
    #                                         part of their formulary.
    # LIST - Subscript of ^TMP array in the form ^TMP($J,LIST,Field Number where Field Number is the Field Number of the data
    #       piece being returned.
    # Returns zero node of 50
    if not LIST:
        return
    ^TMP($J,LIST) = ""

    if not PSSVAL:
        ^TMP($J,LIST,0) = "-1^NO DATA FOUND"
        return
    
    PSS = 0
    CNT = 0
    while True:
        PSS = PSS + 1
        if PSS is None:
            break
        
        if ^PSDRUG("AVSN", PSSVAL,PSS):
            if PSSFL:
                INODE = ^PSDRUG(PSS,2)
                if INODE:
                    if INODE <= PSSFL:
                        continue
            
            if PSSPK:
                # Naked reference below refers to ^PSDRUG(PSS,2)
                if ^PSDRUG(PSS,2,3):
                    if ^PSDRUG(PSS,2,3).find(PSSPK) != -1:
                        continue
            
            ^TMP($J,LIST,PSS) = ^PSDRUG(PSS,.01)
            CNT = CNT + 1
    
    if CNT:
        ^TMP($J,LIST,0) = CNT
    else:
        ^TMP($J,LIST,0) = "-1^NO DATA FOUND"

def AQ1(PSSVAL, PSSFL, PSSPK, LIST):
    # PSSVAL - ITEM NUMBER sub-field (#.01) of the IFCAP ITEM NUMBER multiple of the DRUG file (#50)
    # PSSFL - Inactive flag - "" - All entries
    #                        FileMan Date - Only entries with no Inactive Date or an Inactive Date greater than this date.
    # PSSPK - Application Package's Use - "" - All entries
    #                                         Alphabetic codes that represent the DHCP packages that consider this drug to be
    #                                         part of their formulary.
    # LIST - Subscript of ^TMP array in the form ^TMP($J,LIST,Field Number where Field Number is the Field Number of the data
    #       piece being returned.
    # Returns NAME field (#.01) of DRUG file (#50).
    if not LIST:
        return
    ^TMP($J,LIST) = ""

    if not PSSVAL:
        ^TMP($J,LIST,0) = "-1^NO DATA FOUND"
        return
    
    PSS = 0
    CNT = 0
    while True:
        PSS = PSS + 1
        if PSS is None:
            break
        
        if ^PSDRUG("AQ1", PSSVAL,PSS):
            if PSSFL:
                INODE = ^PSDRUG(PSS,2)
                if INODE:
                    if INODE <= PSSFL:
                        continue
            
            if PSSPK:
                # Naked reference below refers to ^PSDRUG(PSS,2)
                if ^PSDRUG(PSS,2,3):
                    if ^PSDRUG(PSS,2,3).find(PSSPK) != -1:
                        continue
            
            ^TMP($J,LIST,PSS) = ^PSDRUG(PSS,.01)
            CNT = CNT + 1
    
    if CNT:
        ^TMP($J,LIST,0) = CNT
    else:
        ^TMP($J,LIST,0) = "-1^NO DATA FOUND"

def AIU(PSSFT, PSSPK, PSSFL, LIST):
    # PSSFT - NAME field (#.01) of the DRUG file (#50)
    # PSSPK - Application Package's Use - "" - All entries
    #                                         Alphabetic codes that represent the DHCP packages that consider this drug to be
    #                                         part of their formulary.
    # PSSFL - Inactive flag - "" - All entries
    #                        FileMan Date - Only entries with no Inactive Date or an Inactive Date greater than this date.
    # LIST - Subscript of ^TMP array in the form ^TMP($J,LIST,Field Number where Field Number is the Field Number of the data
    #       piece being returned.
    # Returns NAME field (#.01) of DRUG file (#50).
    if not LIST:
        return
    ^TMP($J,LIST) = ""

    if not PSSFT:
        ^TMP($J,LIST,0) = "-1^NO DATA FOUND"
        return
    
    if not PSSPK:
        ^TMP($J,LIST,0) = "-1^NO DATA FOUND"
        return
    
    PSS = 0
    CNT = 0
    while True:
        PSS = PSS + 1
        if PSS is None:
            break
        
        if ^PSDRUG("AIU", PSS):
            INODE = ^PSDRUG(PSS,"I")
            if PSSFL:
                if INODE:
                    if INODE <= PSSFL:
                        continue
            
            if ^PSDRUG(PSS,2):
                if ^PSDRUG(PSS,2,3):
                    if ^PSDRUG(PSS,2,3).find(PSSPK) != -1:
                        continue
            
            if ^PSDRUG(PSS,0).startswith(PSSFT):
                ^TMP($J,LIST,PSS) = ^PSDRUG(PSS,.01)
                CNT = CNT + 1
    
    if CNT:
        ^TMP($J,LIST,0) = CNT
    else:
        ^TMP($J,LIST,0) = "-1^NO DATA FOUND"

def IU(PSSFL, LIST):
    # PSSFL - Inactive flag - "" - All entries
    #                        FileMan Date - Only entries with no Inactive Date or an Inactive Date greater than this date.
    # LIST - Subscript of ^TMP array in the form ^TMP($J,LIST,Field Number where Field Number is the Field Number of the data
    #       piece being returned.
    # Returns NAME field (#.01) of DRUG file (#50).
    if not LIST:
        return
    ^TMP($J,LIST) = ""

    PSS = 0
    CNT = 0
    while True:
        PSS = PSS + 1
        if PSS is None:
            break
        
        if ^PSDRUG("IU", PSS):
            INODE = ^PSDRUG(PSS,"I")
            if PSSFL:
                if INODE:
                    if INODE <= PSSFL:
                        continue
            
            if ^PSDRUG(PSS,0).find("O") == -1:
                if ^PSDRUG(PSS,0).find("U") == -1:
                    if ^PSDRUG(PSS,0).find("I") == -1:
                        if ^PSDRUG(PSS,0).find("N") == -1:
                            ^TMP($J,LIST,PSS) = ^PSDRUG(PSS,.01)
                            CNT = CNT + 1
    
    if CNT:
        ^TMP($J,LIST,0) = CNT
    else:
        ^TMP($J,LIST,0) = "-1^NO DATA FOUND"