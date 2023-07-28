def PSSCMOPE():
    # BIR-TTH ENVIRONMENT CHECK CMOP CS PROJECT ; 2/3/2000 15:19
    # 1.0; PHARMACY DATA MANAGEMENT;**28**;9/30/97
    #
    # Reference to $$VERSION^XPDUTL supported by DBIA #10141
    # Reference to $$PATCH^XPDUTL  supported by DBIA #10141
    if not VERSION^XPDUTL("CMOP").startswith("2") or not PATCH^XPDUTL("PSX*2.0*23"):
        BMES^XPDUTL("You must install patch PSX*2*23")
        XPDQUIT = 1