def PSSMEDX():
    # BIR/TS-CROSS REFERENCE LOGIC FOR STANDARD MEDICATION ROUTE POINTER IN 51.2
    # 04/04/08
    pass

def SET():
    # This routine is called by the AC cross-reference on Field #10 of the Medication Routes (#51.2) File
    if X1[0] == X2[0]:
        return
    PSSHASH = {}
    # DA represents the current record called by the cross-reference
    PSSHASH["DA"] = DA
    READ()

def READ():
    # Set values
    PSSHASHX = {}
    import datetime
    PSSHASHX[51.27, "+1," + PSSHASH["DA"] + ",", .01] = datetime.datetime.now()
    PSSHASHX[51.27, "+1," + PSSHASH["DA"] + ",", 1] = DUZ
    PSSHASHX[51.27, "+1," + PSSHASH["DA"] + ",", 2] = X1[0]
    PSSHASHX[51.27, "+1," + PSSHASH["DA"] + ",", 3] = X2[0]
    import pdb; pdb.set_trace()
    UPDATE(PSSHASHX)

def UPDATE(PSSHASHX):
    import pdb; pdb.set_trace()
    pass

SET()