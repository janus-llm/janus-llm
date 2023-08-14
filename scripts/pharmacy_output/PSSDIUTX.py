def DELDISC():
    if "DISCONTINUED" in PSOSD:
        CKSV = CKDRG = CKON = CKCT = CKVAL = CKNM = DCRCMN = ""
        for CKNM in PSOSD["DISCONTINUED"]:
            DCRCNM = PSOSD["DISCONTINUED"][CKNM].split("^")[0]
            for CKSV in ^TMP($J, LIST, "OUT", "DRUGDRUG"):
                for CKDRG in ^TMP($J, LIST, "OUT", "DRUGDRUG", CKSV):
                    for CKON in ^TMP($J, LIST, "OUT", "DRUGDRUG", CKSV, CKDRG):
                        for CKCT in ^TMP($J, LIST, "OUT", "DRUGDRUG", CKSV, CKDRG, CKON):
                            CKVAL = ^TMP($J, LIST, "OUT", "DRUGDRUG", CKSV, CKDRG, CKON, CKCT).split("^")[0]
                            if DCRCNM == CKVAL:
                                del ^TMP($J, LIST, "OUT", "DRUGDRUG", CKSV, CKDRG, CKON, CKCT)
                            if DCRCNM == CKON.split(";")[1]:
                                del ^TMP($J, LIST, "OUT", "DRUGDRUG", CKSV, CKDRG, CKON, CKCT)
    CKSV = CKDRG = CKON = CKCT = CKVAL = CKNM = DCRCMN = ""

DELDISC()