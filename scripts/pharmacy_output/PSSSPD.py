def PSSSPD():
    # BIR/RLW-PRINT/CREATE PHARMACY ORDERABLE ITEMS ; 09/01/98 7:13
    # 1.0;PHARMACY DATA MANAGEMENT;**15**;9/30/97
    def DOSE():
        nonlocal DF, DFNAME, DDNAME, NDF
        DF, DFNAME = "", ""
        DDNAME = pd_drug["name"]
        NDF = pd_drug.get("nd")
        DA = NDF.get("da")
        X = psnapis_vagn(DA)
        GEN = X
        K = NDF.get("k")
        X = psnapis_psjdf(DA, K)
        NDFVAGN = X
        X = psnapis_prod0(DA, K)
        PROD = X
        
        if not (NDF.get("da") or GEN == 0):
            if not (NDF.get("k") or PROD == ""):
                if GEN != 0:
                    if NDFVAGN != 0:
                        DF = NDFVAGN["df"]
                        if DF != 0:
                            DFNAME = NDFVAGN["dfname"]

    ADDIEN, ADDNAME, CHR, DDIEN, PDNAME, NDF, NDFVA, DF, DDNAME, DFNAME, SPDNAME, X, PGN, PSMATCH, SOLIEN, SOLNAME, SPD, SPDFN, CML, LIVE = 0, "", "", "", "", 0, "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""

    PDIEN = 0
    CHR = "~" if PSCREATE else " "
    tmp_pssd = {}
    tmp_pss = {}
    tmp_pssadd = {}
    tmp_pssol = {}

    while True:
        PDIEN = get_next_pdi(PDIEN)
        if not PDIEN:
            break
        PDNAME = pd_drug["name"]
        DDIEN = ""
        
        while True:
            DDIEN = get_next_ddi(PDIEN, DDIEN)
            if not DDIEN:
                break
            DOSE()
            if not DFNAME and not PSCREATE:
                tmp_pssd["ZZZZ"][DDNAME] = "NDF link missing or incomplete"
            else:
                tmp_pssd[PDNAME+CHR+DFNAME][DDNAME] = PDNAME
                tmp_pss[DDNAME] = PDNAME + " " + DFNAME

    ADDIEN = 0
    while True:
        ADDIEN = get_next_addi(ADDIEN)
        if not ADDIEN:
            break
        DDIEN = add_drug.get("ddien")
        if not DDIEN or not DDIEN in drug:
            continue
        ADDNAME = add_drug["name"]
        DOSE()
        if not DFNAME and not PSCREATE:
            tmp_pssadd["ZZZZ"][DDNAME] = "NDF link missing or incomplete"
        else:
            tmp_pssadd[ADDNAME][DDNAME] = DFNAME

    SOLNAME = ""
    SOLIEN = ""
    while True:
        SOLNAME = get_next_solname(SOLNAME)
        if not SOLNAME:
            break
        SOLIEN = get_next_solen(SOLNAME, SOLIEN)
        if not SOLIEN:
            break
        DDIEN = sol_drug.get("ddien")
        if not DDIEN or not DDIEN in drug:
            continue
        DOSE()
        if not DFNAME and not PSCREATE:
            tmp_pssol["ZZZZ"][DDNAME] = "NDF link missing or incomplete"
        else:
            tmp_pssol[SOLNAME][DFNAME][DDNAME] = SOLIEN

    if PSCREATE:
        load_poi_from_tmp()

    return

PSSSPD()