def DALINK():
    # check for Primary already linked to DA location
    if len(PSD[58.8]['P'][X]) > 0:
        print('\a')
        print()
        print(PSD[58.8][int(PSD[58.8]['P'][X][0])][0], "is already linked to", INVNAME(PRCPUX1(X)))
        X = None

def FI():
    PSA = next(iter(PSDRUG['AB'][int(X)]), next(iter(PSDRUG['AB'][DA], None)))
    if PSA:
        print('\a')
        print()
        print(PSDRUG[PSA], "is already linked to")
        print()
        print("Item #", X, " ", DESCR(PRCPUX1(0, X)))
        if PSA:
            X = None

def ITEM(PSA):
    # return Item Master # ^PRC(441)
    PSA1 = next(iter(PRC[441]['F'][PSA]), None)
    if not PSA1:
        if len(PSA.split('-')[0]) < 6:
            PSA1 = next(iter(PRC[441]['F']['0' + PSA]), None)
        if not PSA1 and len(PSA.split('-')) == 4:
            PSA1 = next(iter(PRC[441]['F']['00' + PSA]), None)
        if not PSA1 and not PSA[0] and len(PSA.split('-')) > 4:
            PSA1 = next(iter(PRC[441]['F'][PSA[1:14]]), None)
        if not PSA1 and not PSA[:2] and len(PSA.split('-')) == 6:
            PSA1 = next(iter(PRC[441]['F'][PSA[2:14]]), None)
    return PSA1