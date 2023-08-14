def PSSPOIM():
    # BIR/RTR-Orderable Items by VA Generic Name only
    # 09/01/98 7:11
    # 1.0;PHARMACY DATA MANAGEMENT;**15**;9/30/97
    
    # K ^TMP("PSSD",$J)
    if not PSMATCH:
        return
    
    # VA Generic Name only that can match
    RRR = 0
    while True:
        RRR = RRR + 1
        if not RRR in PSDRUG:
            break
        
        # K NODE,PSONAME,PSOPTR
        NODE = PSDRUG[RRR]["ND"]
        PSONAME = PSDRUG[RRR][0]
        PSOPTR = PSDRUG[RRR][2]
        DA = NODE[0]
        K = NODE[2]
        X = PSJDF(PSNAPIS(DA, K))
        DOSE1 = X
        
        if PSONAME == "":
            continue
        
        if PSOPTR:
            continue
        
        if not NODE[0]:
            continue
        
        # Next 5 lines of code could only apply if this report is run and
        # there are Dispensed drugs that are already matched
        PSSUP = {}
        if NODE[0] and NODE[2]:
            GG = 0
            while True:
                GG = GG + 1
                if not GG in PSDRUG["AND"][NODE[0]]:
                    break
                
                if PSDRUG[GG][2] and PS50_7[PSDRUG[GG][2]]:
                    ONO = PSDRUG[GG]["ND"]
                    if ONO[0] and ONO[2] and DOSE1 != 0:
                        DA = ONO[0]
                        K = ONO[2]
                        X = PSJDF(PSNAPIS(DA, K))
                        DOSE2 = X
                        if DOSE2 != 0 and DOSE1 == DOSE2:
                            PSSUP[GG] = PSDRUG[GG][2]
        
        COM = 0
        COMSUP = 0
        if PSSUP:
            COM = 1
            FF = next(iter(PSSUP))
            SUPER = PSSUP[FF]
            for FF in PSSUP:
                if SUPER != PSSUP[FF]:
                    COMSUP = 1
        
        if COM and COMSUP:
            continue
        
        if COM and not COMSUP:
            SSS = next(iter(PSSUP))
            SSS = PSSUP[SSS]
            PSSD[P50_7[SUPER][0] + " " + P50_606[P50_7[SSS][1]][0]][PSONAME] = ""
        
        if NODE[0] and NODE[2]:
            DA = NODE[0]
            X = VAGN(PSNAPIS(DA))
            VAG = X
            if VAG != 0 and DOSE1 != 0:
                if len(VAG) < 41:
                    PSSD[DOSE1[1]][PSONAME] = ""
    
    # END
    del PSSUP, APPL, COM, COMSUP, FF, GG, NODE, ONO, POINAME, PSOPTR, PSPTR, RRR, SSS, SUPER

def CANT():
    # Generic name only, cannot match
    del PSSD["ZZZZ"]
    ZZ = 0
    while True:
        ZZ = ZZ + 1
        if not ZZ in PSDRUG:
            break
        
        # K PTDOS,DOSEF,REASON
        PSND = PSDRUG[ZZ]["ND"]
        PSDNAME = PSDRUG[ZZ][0]
        PSOPRT = PSDRUG[ZZ][2]
        TMPFLAG = 0
        DA = PSND[0]
        K = PSND[2]
        X = PSJDF(PSNAPIS(DA, K))
        DSE = X
        X = VAGN(PSNAPIS(DA))
        GN1 = X
        
        if PSOPRT:
            continue
        
        PSQFLAG = 0
        if PSND[0] and PSND[2] and GN1 != 0 and DSE != 0:
            if DSE != 0 and P50_606[DSE[0]]:
                if len(GN1) < 41:
                    PSQFLAG = 1
        
        if PSQFLAG:
            continue
        
        TMPFLAG = 1
        if PSND[0] == "":
            REASON = "NDF link missing or incomplete"
            continue
        
        if PSND[2] == "":
            REASON = "No PSNDF VA Product Name Entry"
            continue
        
        if GN1 == 0:
            REASON = "Invalid National Drug File entry"
            continue
        
        PSVA = PSND[2]
        DA = PSND[0]
        K = PSVA
        X = PROD0(PSNAPIS(DA, K))
        if not X:
            REASON = "Invalid PSNDF VA Product Name Entry"
            continue
        
        if DSE == 0:
            REASON = "No Dosage Form Entry in NDF"
            continue
        
        if DSE == 0:
            REASON = "Missing Dosage Form in NDF"
            continue
        
        if DSE == 0:
            REASON = "Invalid entry in Dosage Form File"
            continue
        
        if len(GN1) > 40:
            REASON = "Generic name greater than 40 characters"
            continue
        
        REASON = "Undertermined problem"
    
    # DONE
    del DOSEFORM, DOSEPTR, PSAPP, PSDNAME, PSND, PSQFLAG, PSVA, TMPFLAG, ZZ