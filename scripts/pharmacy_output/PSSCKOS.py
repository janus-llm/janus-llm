def THOSTAT(DRG, THR, TCTR):
    DRGN = ""
    PSOSTA = ""
    PSONM = ""
    PSOPON = ""
    PSOCFLG = ""
    PSOFLG = ""
    DRGN = DRG
    PSOPON = TMP[J][LIST]["OUT"]["THERAPY"][THR]["DRUGS"][TCTR][1]
    PSOCFLG = PSOPON.split(";")[0]
    PSOPON = PSOPON.split(";")[1]
    if "C" in PSOCFLG:
        DRGN = DRG + " (Clinic order)"
        return DRGN
    for PSOSTA in PSOSD:
        if DRG not in PSOSD[PSOSTA] and DRG == PSODRUG["NAME"]:
            DRGN = DRG + " (Prospective)"
            PSOFLG = 1
        for PSONM in PSOSD[PSOSTA]:
            if DRG == PSONM[0]:
                if PSOSTA == "ACTIVE" and PSOPON == PSOSD[PSOSTA][PSONM][0]:
                    DRGN = DRG + " (Local Rx)"
                    PSOFLG = 1
                if PSOSTA == "ZNONVA" and PSOPON == PSOSD[PSOSTA][PSONM][9]:
                    DRGN = DRG + " (Non-VA)"
                    PSOFLG = 1
                if PSOSTA == "DISCONTINUED" and PSOPON == PSOSD[PSOSTA][PSONM][0]:
                    DRGN = DRG + " (Discontinued)"
                    PSOFLG = 1
                if PSOSTA == "PENDING" and PSOPON == PSOSD[PSOSTA][PSONM][9]:
                    DRGN = DRG + " (Pending)"
                    PSOFLG = 1
    return DRGN


def OSTAT(DRG, ON):
    DRGN = ""
    PSOSTA = ""
    PSONM = ""
    PSOPON = ""
    PSOCFLG = ""
    PSOFLG = ""
    DRGN = DRG
    PSOCFLG = ON.split(";")[0]
    PSOPON = ON.split(";")[1]
    if "C" in PSOCFLG:
        DRGN = DRG + " (Clinic order)"
        return DRGN
    for PSOSTA in PSOSD:
        if DRG not in PSOSD[PSOSTA] and DRG == PSODRUG["NAME"]:
            DRGN = DRG + " (Prospective)"
            PSOFLG = 1
        for PSONM in PSOSD[PSOSTA]:
            if DRG == PSONM[0]:
                if PSOSTA == "ACTIVE" and PSOPON == PSOSD[PSOSTA][PSONM][0]:
                    DRGN = DRG + " (Local Rx)"
                    PSOFLG = 1
                if PSOSTA == "ZNONVA" and PSOPON == PSOSD[PSOSTA][PSONM][9]:
                    DRGN = DRG + " (Non-VA)"
                    PSOFLG = 1
                if PSOSTA == "PENDING" and PSOPON == PSOSD[PSOSTA][PSONM][9]:
                    DRGN = DRG + " (Pending)"
                    PSOFLG = 1
    return DRGN


def POSTAT(DRG, PDRG, SV, ON, CT):
    PDRGN = ""
    PSOSTA = ""
    PSONM = ""
    PSOPON = ""
    PSOCFLG = ""
    PSOFLG = ""
    PDRGN = PDRG
    PSOPON = TMP[J][LIST]["OUT"]["DRUGDRUG"][SV][DRG][ON][CT][1]
    PSOCFLG = PSOPON.split(";")[0]
    PSOPON = PSOPON.split(";")[1]
    if "C" in PSOCFLG:
        PDRGN = PDRG + " (Clinic order)"
        return PDRGN
    for PSOSTA in PSOSD:
        if PDRG not in PSOSD[PSOSTA] and PDRG == PSODRUG["NAME"]:
            PDRGN = PDRG + " (Prospective)"
            PSOFLG = 1
        for PSONM in PSOSD[PSOSTA]:
            if PDRG == PSONM[0]:
                if PSOSTA == "ACTIVE" and PSOPON == PSOSD[PSOSTA][PSONM][0]:
                    PDRGN = PDRG + " (Local Rx)"
                    PSOFLG = 1
                if PSOSTA == "ZNONVA" and PSOPON == PSOSD[PSOSTA][PSONM][9]:
                    PDRGN = PDRG + " (Non-VA)"
                    PSOFLG = 1
                if PSOSTA == "PENDING" and PSOPON == PSOSD[PSOSTA][PSONM][9]:
                    PDRGN = PDRG + " (Pending)"
                    PSOFLG = 1
    return PDRGN