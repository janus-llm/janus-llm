def SAVNDC(DRG, SITE, NDC, CMP):
    NDC = NDCFMT(NDC)
    if NDC == "":
        return
    if not exist(PSDRUG[DRG]["NDCOP"][SITE]):
        DIC = "^PSDRUG(" + str(DRG) + ",""NDCOP"","
        X = DINUM = SITE
        DA_1 = DRG
        DIC0 = ""
        FILE(DICN)
    DIE = "^PSDRUG(" + str(DRG) + ",""NDCOP"","
    DA_1 = DRG
    DA = SITE
    DR = (str(CMP) + "///" + NDC) if CMP else ("1///" + NDC)
    DIE(D)