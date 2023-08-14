def PSS127PT():
    # PSS*1*127 Post-install routine ;05/11/07
    # 1.0;PHARMACY DATA MANAGEMENT;**127**;9/30/97;Build 41
    globals()[XPDGREF + "^XTMP(""PSSNCPDP"")"] = globals()["^XTMP(""PSSNCPDP"")"]
    return