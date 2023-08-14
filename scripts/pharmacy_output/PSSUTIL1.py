def EN(PSSDRIEN):
    PSSMASH = None
    PSSMNDFS = None
    PSSMSSTR = None
    PSSMUNIT = None
    PSSUNZ = None
    PSSMA = None
    PSSMB = None
    PSSMA1 = None
    PSSMB1 = None
    PSSUNX = None
    PSSMASH2 = None
    PSSMASH3 = None
    PSSNAT1 = None
    PSSNAT3 = None
    PSSNODEU = None

    if not PSSDRIEN:
        return "|^^^^^99PSU"
    
    PSSMSSTR = ^PSDRUG(PSSDRIEN,"DOS")["^"]
    PSSMUNIT = ^("DOS")["^", 2
    PSSNAT1 = ^PSDRUG(PSSDRIEN,"ND")["^"
    PSSNAT3 = ^("ND")["^", 3
    
    if PSSNAT1 and PSSNAT3:
        PSSNODEU = DFN^PSNAPIS(PSSNAT1, PSSNAT3)
        PSSMNDFS = ^PSSNODEU["^", 4
        if not PSSMUNIT:
            PSSMUNIT = ^PSSNODEU["^", 5
    
    PSSUNZ = ^PS(50.607, +PSSMUNIT, 0)["^"
    
    if PSSUNZ != "/":
        if PSSMSSTR:
            return PSSMSSTR + "|" + "^^^" + (PSSMUNIT if PSSMUNIT else "") + "^" + PSSUNZ + "^" + "99PSU"
        elif PSSMNDFS:
            return PSSMNDFS + "|" + "^^^" + (PSSMUNIT if PSSMUNIT else "") + "^" + PSSUNZ + "^" + "99PSU"
        else:
            return ""
    
    PSSMASH = 0
    
    if PSSMSSTR and PSSMNDFS and int(PSSMSSTR) != int(PSSMNDFS):
        PSSMASH = 1
    
    if not PSSMASH:
        return PSSMSSTR + "|" + "^^^" + (PSSMUNIT if PSSMUNIT else "") + "^" + PSSUNZ + "^" + "99PSU"
    
    PSSMA = ^PSSUNZ.split("/")[0]
    PSSMB = ^PSSUNZ.split("/")[1]
    PSSMA1 = int(PSSMA) if PSSMA else 0
    PSSMB1 = int(PSSMB) if PSSMB else 0
    PSSMASH2 = int(PSSMSSTR) / int(PSSMNDFS)
    PSSMASH3 = PSSMASH2 * (int(PSSMB1) if PSSMB1 else 1)
    PSSUNX = PSSMA + "/" + str(PSSMASH3) + (PSSMB if not PSSMB1 else PSSMB.split(PSSMB1)[1])
    
    return (PSSMSSTR if PSSMSSTR else "") + "|" + "^^^^" + PSSUNX + "^" + "99PSU"

def DRG(PSSDD, PSSOI, PSSPK):
    PSSL = None
    PSSAP = None
    PSSIN = None
    PSSND = None
    
    if not PSSOI:
        return
    
    if PSSPK != "O" and PSSPK != "I" and PSSPK != "X":
        return
    
    PSSL = 0
    while True:
        PSSL = ^PSDRUG("ASP", PSSOI, PSSL)
        if not PSSL:
            break
        
        PSSIN = ^PSDRUG(PSSL,"I")["^"
        PSSAP = ^("2")["^", 3
        
        if PSSIN and int(PSSIN) < int(DT):
            continue
        
        PSSND = ^PSDRUG(PSSL,"ND")["^"
        
        if PSSPK == "O" or PSSPK == "X":
            if PSSAP and PSSAP.contains(PSSPK):
                PSSDD[str(PSSL) + ";" + PSSND] = ^PSDRUG(PSSL, 0)["^"]
        else:
            if PSSAP.contains("I") or PSSAP.contains("U"):
                PSSDD[str(PSSL) + ";" + PSSND] = ^PSDRUG(PSSL, 0)["^"]

def ITEM(PSSIT, PSSDR):
    PSSNEW = None
    
    if not PSSIT or not PSSDR:
        return -1
    
    if not ^PS(50.7, +PSSIT, 0) or not ^PSDRUG(+PSSDR, 0):
        return -1
    
    PSSNEW = int(^PSDRUG(+PSSDR, "2")["^"])
    
    if PSSNEW and PSSNEW == int(PSSIT):
        return 0
    elif PSSNEW and PSSNEW != int(PSSIT):
        return str(1) + "^" + str(PSSNEW)
    else:
        return -1

def EN1(PSSOA, PSSOAP):
    PSSOAL = None
    PSSOALD = None
    PSSOAN = None
    PSSOAIT = None
    PSSOADT = None
    PSSOAZ = None
    
    if not PSSOA:
        return
    
    if PSSOAP != "O" and PSSOAP != "I":
        return
    
    PSSOAL = ""
    while True:
        PSSOAL = ^PSDRUG("ASP", PSSOA, PSSOAL)
        if not PSSOAL:
            break
        
        PSSOALD = ""
        while True:
            PSSOALD = ^PSDRUG(PSSOAL,65,PSSOALD)
            if not PSSOALD:
                break
            
            PSSOAN = ^PSDRUG(PSSOAL,65,PSSOALD,0)["^"
            if PSSOAN:
                PSSOAIT = int(^PSDRUG(PSSOAN,2)["^"])
                if PSSOAIT:
                    if PSSOAIT == int(PSSOA):
                        PSSOA(PSSOAIT) = ""
                    elif not ^PS(50.7, PSSOAIT, 0)["^", 12 and (not ^PS(50.7, PSSOAIT, 0)["^", 4 or int(^PS(50.7, PSSOAIT, 0)["^", 4) > int(DT)):
                        PSSOAZ = ""
                        while True:
                            PSSOAZ = ^PSDRUG("ASP", PSSOAIT, PSSOAZ)
                            if not PSSOAZ or PSSOA(PSSOAIT):
                                break
                            
                            if ^PSDRUG(PSSOAZ,"I")["^" and int(^("I")["^") <= int(DT):
                                continue
                            
                            if not ^PSDRUG(PSSOAZ,0)["^", 9:
                                if PSSOAP == "O":
                                    if ^PSDRUG(PSSOAZ,2)["^", 3].contains("O"):
                                        PSSOA(PSSOAIT) = ""
                                else:
                                    if ^PSDRUG(PSSOAZ,2)["^", 3].contains("I") or ^PSDRUG(PSSOAZ,2)["^", 3].contains("U"):
                                        PSSOA(PSSOAIT) = ""

def SCH(SCH):
    SQFLAG = None
    SCLOOP = None
    SCLP = None
    SCLPS = None
    SCLHOLD = None
    SCIN = None
    SODL = None
    SST = None
    SCHEX = None
    
    SCHEX = SCH
    SQFLAG = 0
    
    if not SCH:
        return SCHEX
    
    SCLOOP = 0
    while True:
        SCLOOP = ^PS(51.1,"B", SCH, SCLOOP)
        if not SCLOOP or SQFLAG:
            break
        
        if ^PS(51.1,SCLOOP,0)["^", 8]:
            SCHEX = ^PS(51.1,SCLOOP,0)["^", 8]
            SQFLAG = 1
    
    if SQFLAG:
        return SCHEX
    
    if ^PS(51,"A",SCH)["^"]:
        SCHEX = ^PS(51,"A",SCH)["^"]
    
    SCLOOP = 0
    SCLHOLD = []
    while True:
        SCIN = ^SCH.split(" ")[SCLOOP]
        if not SCIN:
            break
        
        SODL = SCIN
        SQFLAG = 0
        SST = 0
        while True:
            SST = ^PS(51.1,"B",SODL,SST)
            if not SST or SQFLAG:
                break
            
            if ^PS(51.1,SST,0)["^", 8]:
                SCLHOLD[SCLOOP] = ^PS(51.1,SST,0)["^", 8]
                SQFLAG = 1
        
        if SQFLAG:
            continue
        
        if ^PS(51,"A",SODL)["^"]:
            SCLHOLD[SCLOOP] = ^PS(51,"A",SODL)["^"]
    
    SCHEX = ""
    SQFLAG = 0
    SST = 0
    while True:
        SCHEX = SCHEX + ("" if SQFLAG else " ") + SCLHOLD[SST]
        SQFLAG = 1
        SST = SST + 1
        if SST >= SCLOOP:
            break
    
    return SCHEX

def IVDEA(PSSIVOI, PSSIVOIP):
    PSSIVDO = None
    PSSIVDD = None
    PSSIVL = None
    PSSIVLP = None
    PSSIVDEA = None
    PSSIVLPX = None
    PSSK = None
    PSSI = None
    PSSGD = None
    
    PSSIVDO = 0
    PSSIVDD = 0
    
    if PSSIVOIP != "S":
        PSSIVOIP = "A"
    
    if not PSSIVOI:
        return PSSIVDO
    
    PSSIVL = ""
    while True:
        PSSIVL = ^PSDRUG("ASP", PSSIVOI, PSSIVL)
        if not PSSIVL:
            break
        
        PSSIVDD = 1
        
        if PSSIVOIP == "A":
            PSSIVLP = 0
            while True:
                PSSIVLP = ^PSDRUG("A526", PSSIVL, PSSIVLP)
                if not PSSIVLP or PSSIVLPX:
                    break
                
                if ^PS(52.6,PSSIVLP,0)["^"]:
                    if not ^("I")["^"] or int(^("I")["^"]) > int(DT):
                        IVX()
        
        PSSIVLP = 0
        while True:
            PSSIVLP = ^PSDRUG("A527", PSSIVL, PSSIVLP)
            if not PSSIVLP or PSSIVLPX:
                break
            
            if ^PS(52.7,PSSIVLP,0)["^"]:
                if not ^("I")["^"] or int(^("I")["^"]) > int(DT):
                    IVX()
    
    IVQ()
    
    if PSSI:
        PSSK = 0
        while True:
            PSSK = PSSI(PSSK)
            if not PSSK:
                break
            
            PSSIVDO = PSSK[0] + ("n" if len(PSSK) > 1 else "")
    
    IVQ1()
    
    if PSSIVDO == 0 and not PSSIVDD:
        PSSIVDO = ""
    
    return PSSIVDO

def IVQ():
    PSSI = []
    PSSK = 0
    
    PSSK = PSSI(PSSK)
    if PSSK:
        if PSSK.contains(1):
            PSSI[1] = ""
        elif PSSK.contains(2) and not PSSK.contains("C"):
            PSSI[2] = ""
        elif PSSK.contains(2) and PSSK.contains("C"):
            PSSI[2.5] = ""
        elif PSSK.contains(3) and not PSSK.contains("C"):
            PSSI[3] = ""
        elif PSSK.contains(3) and PSSK.contains("C"):
            PSSI[3.5] = ""
        elif PSSK.contains(4):
            PSSI[4] = ""
        elif PSSK.contains(5):
            PSSI[5] = ""

def IVQ1():
    if PSSIVDO == 0 and not PSSIVDD:
        PSSIVDO = ""

def IVX():
    PSSIVDD = 1
    PSSIVDEA = ^PSDRUG(PSSIVL, 0)["^", 3]
    if PSSIVDEA:
        PSSGD[PSSIVDEA] = ""
    
    if int(^PSDRUG(PSSIVL,"ND")["^", 3]):
        PSSK = ^PSDRUG(PSSIVL,"ND")["^", 3]
        if int(^PSNDF(50.68,PSSK,7)["^"]):
            PSSK = ^PSNDF(50.68,PSSK,7)["^"]
            if PSSK:
                PSSI[(PSSK[0] + ".5") if PSSK[1] == "n" else PSSK] = ""

def MAXDS(INPUT):
    MAXDS = None
    DRG = None
    DRGMAXDS = None
    
    if INPUT["DRUG"]:
        return MXDAYSUP(INPUT["DRUG"])
    
    MAXDS = 90
    if INPUT["PSOI"]:
        DRG = 0
        while True:
            DRG = ^PSDRUG("ASP", INPUT["PSOI"], DRG)
            if not DRG:
                break
            
            DRGMAXDS = GET1^DIQ(50, DRG, 66)
            if DRGMAXDS:
                if DRGMAXDS < MAXDS:
                    MAXDS = DRGMAXDS
    
    return MAXDS

def MXDAYSUP(DRUG):
    MXDAYSUP = 90
    if not ^PSDRUG(DRUG, 0):
        return MXDAYSUP
    
    DRGMAXDS = GET1^DIQ(50, DRUG, 66)
    if DRGMAXDS:
        MXDAYSUP = DRGMAXDS
    
    VAPRDIEN = +GET1^DIQ(50, DRUG, 22)
    if VAPRDIEN:
        NDFMAXDS = GET1^DIQ(50.68, VAPRDIEN, 32)
        if NDFMAXDS and (not DRGMAXDS or NDFMAXDS < DRGMAXDS):
            MXDAYSUP = NDFMAXDS
    
    DEASPHLG = GET1^DIQ(50, DRUG, 3)
    if DEASPHLG.contains("2") and MXDAYSUP > 30:
        MXDAYSUP = 30
    elif (DEASPHLG.contains("3") or DEASPHLG.contains("4") or DEASPHLG.contains("5")) and MXDAYSUP > 90:
        MXDAYSUP = 90
    
    if GET1^DIQ(50, DRUG, "CLOZ1") == "PSOCLO1":
        MXDAYSUP = 28
    
    return MXDAYSUP