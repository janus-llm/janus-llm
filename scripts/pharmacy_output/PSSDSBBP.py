def PSSDSBBP(PSSQVIEN, PSSQVLCD):
    # PSSQVIEN = File 50 Internal Entry Number
    # PSSQVLCD = Local Possible Dosage
    # Find Dose Unit and Numeric Dose, called from PSSDSAPD
    if not PSSQVIEN:
        return 0
    if not PSSQVLCD:
        return 0
    
    # D^PSSDSBDA
    PSSQVSSS = 0
    if PSSQVIEN:
        PSSQVND1 = PSSQVND3 = 0
        PSSQVND1 = PSSDRUG[PSSQVIEN]["ND"][0]
        PSSQVND3 = PSSDRUG[PSSQVIEN]["ND"][2]
        if not PSSQVND3 or not PSSQVND1:
            return 0
        
        PSSQVNDF = PSSNAPIS.DFSU(PSSQVND1, PSSQVND3)
        PSSQVDF = PSSQVNDF[0]
        if not PSSQVDF and PSSDRUG[PSSQVIEN][2]:
            PSSQVDF = PSS50_7[PSSDRUG[PSSQVIEN][2]][1]
        
        PSSQVFZ = ""
        if PSSQVDF:
            PSSQVFZ = PSS50_606[PSSQVDF][0]
        
        if True:
            PSSQVLCD = PSSQVLCD.upper()
            PSSQVDF1 = PSSQVDF2 = PSSQVDF3 = PSSQVQT = 0
            
            # Condition Set 4 (Part 1)
            if PSSQVLCD in PSSQVCS4:
                PSSQVQT = 1
                PSSQVDF1 = PSSQVCS4[PSSQVLCD][0]
                PSSQVDF2 = PSSQVCS4[PSSQVLCD][1]
                PSSQVDF3 = DFIND(PSSQVDF2)
                if PSSQVDF3 and PSSQVDF1:
                    PSSQVSSS = [PSSQVDF3, PSSQVDF1]
            
            if PSSQVQT:
                return PSSQVSSS
            
            # Condition Set 4 (Part 2)
            CS4()
            if PSSQVQT:
                return PSSQVSSS
            
            # Condition Set 1
            if PSSQVNDF[3] and PSSQVNDF[5]:
                if PSSQVFZ in ["TAB", "CAP", "GUM,CHEWABLE", "IMPLANT", "LOZENGE", "SUPP,RTL", "TROCHE", "INJ/IMPLANT"]:
                    if PSSQVNDF[5] in ["MG", "MCG", "UNT", "GM", "MEQ"]:
                        PSSQVQT = 1
                        PSSQVDF4 = PSSDRUG[PSSQVIEN]["DOS"][0]
                        PSSQVDF5 = PSSDRUG[PSSQVIEN]["DOS"][1]
                        if PSSQVDF5:
                            X = PSS50_607[PSSQVDF5][0]
                            if X:
                                PSSQVDF6 = DFIND(X)
                        if not PSSQVDF6:
                            X = PSSQVNDF[5]
                            PSSQVDF6 = DFIND(X)
                        
                        if PSSQVDF6:
                            PSSQVDF7 = PSSQVDF4 if PSSQVDF4 else PSSQVNDF[3]
                            if isinstance(PSSQVDF7, int) or isinstance(PSSQVDF7, float):
                                PSSQVDF8 = NUM()
                                if PSSQVDF8:
                                    PSSQVMUL = PSSQVDF8 * PSSQVDF7
                                    if isinstance(PSSQVMUL, float):
                                        PSSQVMUL = round(PSSQVMUL, 6)
                                        if 0.00001 <= PSSQVMUL <= 99999999999999:
                                            PSSQVSSS = [PSSQVDF6, PSSQVMUL]
            
            if PSSQVQT:
                return PSSQVSSS
            
            # Condition Set 2
            if PSSQVNDF[3] and PSSQVNDF[5]:
                PSSQV9 = PSSQVNDF[5]
                if PSSQVFZ in ["ELIXIR", "LIQUID", "LIQUID,ORAL", "PWDR,RENST-ORAL", "SOLN,CONC", "SOLN,ORAL", "SUSP", "SUSP,ORAL", "SYRUP", "SYRUP,ORAL"]:
                    PSSQVFZA = 1
                if PSSQVFZ in ["INJ", "INJ,SOLN"]:
                    PSSQVFZA = 1
                if PSSQVFZA:
                    if PSSQV9 in ["GM/ML", "GM/1ML", "GM/5ML", "GM/10ML", "GM/15ML", "GM/30ML"]:
                        PSSQVFL8 = 1
                    if PSSQV9 in ["MG/ML", "MG/1ML", "MG/5ML", "MG/10ML", "MG/15ML", "MG/30ML", "MEQ/ML", "MEQ/1ML", "MEQ/5ML", "MEQ/10ML", "MEQ/15ML", "MEQ/30ML"]:
                        PSSQVFL8 = 1
                    if PSSQVFL8:
                        PSSQVQT = 1
                        PSSQVXF4 = PSSDRUG[PSSQVIEN]["DOS"][0]
                        PSSQVXF5 = PSSDRUG[PSSQVIEN]["DOS"][1]
                        if PSSQVXF5:
                            X = PSS50_607[PSSQVXF5][0]
                            PSSQVFL9 = 0
                            if X in ["GM/ML", "GM/1ML", "GM/5ML", "GM/10ML", "GM/15ML", "GM/30ML"]:
                                PSSQVFL9 = 1
                            if X in ["MG/ML", "MG/1ML", "MG/5ML", "MG/10ML", "MG/15ML", "MG/30ML", "MEQ/ML", "MEQ/1ML", "MEQ/5ML", "MEQ/10ML", "MEQ/15ML", "MEQ/30ML"]:
                                PSSQVFL9 = 1
                            if PSSQVFL9:
                                PSSQVXF8 = X.split("/")[0]
                                PSSQVNUM = int(X.split("/")[1])
                                PSSQVXF6 = DFIND(PSSQVXF8)
                        if not PSSQVXF6:
                            PSSQVNUM = int(PSSQV9.split("/")[1])
                            PSSQVXF9 = PSSQV9.split("/")[0]
                            PSSQVXF6 = DFIND(PSSQVXF9)
                            PSSQVNUM = int(PSSQV9.split("/")[1])
                        
                        if PSSQVXF6:
                            if PSSQVNUM in [0, 1, 5, 10, 15, 30]:
                                if PSSQVNUM == 0:
                                    PSSQVNUM = 1
                                PSSQVXF7 = PSSQVXF4 if PSSQVXF4 else PSSQVNDF[3]
                                if isinstance(PSSQVXF7, int) or isinstance(PSSQVXF7, float):
                                    PSSQVFNX = PSSQVXF7 * PSSQVNUM if PSSQVFNC == "M" else PSSQVXF7 / PSSQVNUM
                                    if isinstance(PSSQVFNX, float):
                                        PSSQVFNX = round(PSSQVFNX, 6)
                                        if 0.00001 <= PSSQVFNX <= 99999999999999:
                                            PSSQVSSS = [PSSQVXF6, PSSQVFNX]
            
            if PSSQVQT:
                return PSSQVSSS
            
            # Condition Set 3
            if PSSQVND1 and PSSQVND3 and not PSSQVNDF[3] and not PSSQVNDF[5]:
                if PSSQVLCD in PSSQVCS5:
                    PSSQVF51 = PSSQVCS5[PSSQVLCD][0]
                    PSSQVF52 = PSSQVCS5[PSSQVLCD][1]
                    PSSQVF53 = DFIND(PSSQVF52)
                    if PSSQVF51 and PSSQVF53:
                        PSSQVSSS = [PSSQVF53, PSSQVF51]
    
    return PSSQVSSS

def CS4():
    global PSSQVQT
    if PSSQVLCD.endswith(" UNITS") or PSSQVLCD.endswith(" UNIT") or PSSQVLCD.endswith(" UNIT(S)") or PSSQVLCD.endswith(" UNT") or PSSQVLCD.endswith(" UNT(S)") or PSSQVLCD.endswith(" UNTS") or PSSQVLCD.endswith(". UNITS") or PSSQVLCD.endswith(". UNIT") or PSSQVLCD.endswith(". UNIT(S)") or PSSQVLCD.endswith(". UNT") or PSSQVLCD.endswith(". UNT(S)") or PSSQVLCD.endswith(". UNTS"):
        CS4ST()
    else:
        COMMA()

def CS4ST():
    global PSSQVQT
    PSSQVXXX = int(PSSQVLCD.split()[0].replace(",", ""))
    if 0.00001 <= PSSQVXXX <= 99999999999999:
        PSSQVD12 = "UNIT(S)"
        PSSQVD11 = DFIND(PSSQVD12)
        if PSSQVD11:
            return [PSSQVD11, PSSQVXXX]
    
    return 0

def COMMA():
    if " " in PSSQVLCD:
        PSSQVCM1 = PSSQVLCD.split()[0]
        PSSQVCM3 = PSSQVLCD.find(" ")
        PSSQVCM2 = PSSQVCM1.replace(",", "")
        PSSQVCM4 = PSSQVCM2 + PSSQVLCD[PSSQVCM3:]
        if PSSQVCM4.endswith(" UNITS") or PSSQVCM4.endswith(" UNIT") or PSSQVCM4.endswith(" UNIT(S)") or PSSQVCM4.endswith(" UNT") or PSSQVCM4.endswith(" UNT(S)") or PSSQVCM4.endswith(" UNTS"):
            CS4ST1()

def CS4ST1():
    global PSSQVQT
    PSSQVCM5 = int(PSSQVCM4.split()[0].replace(",", ""))
    if 0.00001 <= PSSQVCM5 <= 99999999999999:
        PSSQVCM7 = "UNIT(S)"
        PSSQVCM6 = DFIND(PSSQVCM7)
        if PSSQVCM6:
            return [PSSQVCM6, PSSQVCM5]
    
    return 0

def DFIND(PSSQVFND):
    PSSQVFN1 = PSS51_24_B[PSSQVFND][0] if PSS51_24_B.get(PSSQVFND) and not SCREEN(51.24, .01, PSSQVFN1) else 0
    PSSQVFN1 = PSS51_24_C[PSSQVFND][0] if PSS51_24_C.get(PSSQVFND) and not SCREEN(51.24, .01, PSSQVFN1) else 0
    PSSQVFN1 = PSS51_24_D[PSSQVFND][0] if PSS51_24_D.get(PSSQVFND) and not SCREEN(51.24, .01, PSSQVFN1) else 0
    return PSSQVFN1

def SCREEN(file, field, ien):
    # Placeholder for SCREEN function
    return False

def NUM():
    # Placeholder for NUM function
    return 0

# Initialize global variables
PSSQVCS4 = {}
PSSQVCS5 = {}
PSSDRUG = {}
PSSNAPIS = {}
PSS50_606 = {}
PSS50_7 = {}
PSS50_607 = {}
PSS51_24_B = {}
PSS51_24_C = {}
PSS51_24_D = {}
PSSQVSSS = PSSDSBBP(PSSQVIEN, PSSQVLCD)