def PSSCLDRG():
    if "^PSDRUG(DISPDRG,\"CLOZ1\")" in globals() and globals()["^PSDRUG(DISPDRG,\"CLOZ1\")"]["^",2] == 1:
        print("\a\a\nThis drug is marked for Lab Monitor purposes. You must unmark it as a")
        print("Lab Monitor before you can mark it as a Clozapine drug.")
        MONCLOZ()

    print()
    DA = DISPDRG
    if DISPDRG in globals()["^PSDRUG(\"ACLOZ\")"]:
        if CLFLAG:
            UNMARK()

    if LMFLAG:
        return
    if NFLAG:
        return
    if "DIRUT" in globals():
        return
    if "DUOUT" in globals():
        return
    if "DTOUT" in globals():
        return

    PSSFLG = None
    if not globals()["^PSDRUG(DISPDRG,\"I\")"] or int(globals()["^PSDRUG(DISPDRG,\"I\")"]) > int(DT):
        PSSFLG = 1
        PSSCLOZ()

    if PSSFLG is None:
        DR = "D CHECK^PSSCLDRG;100///@;W !,\"Drug is now re-activated\" S Y=\"@2\";@1;W !!,\"No change\";@2"
        DA = DISPDRG
        DIE = DIC
        DIE()

        if globals()["Y"] == 1:
            DUOUT = 1

    if not DUOUT and not globals()["DIRUT"] and not globals()["DTOUT"]:
        PSIU()
        print(f"{globals()[\"^PSDRUG(DA,0)\"]}\" is now marked as a Clozapine drug")
        CLFLAG = 1
        NFLAG = 1

    X = None
    Y = None
    DIR = None
    DR = None
    DIC = None
    DIE = None
    PSIUA = None
    PSIUX = None
    percent = None
    D0 = None
    D1 = None
    DQ = None
    I = None
    Z = None
    DTOUT = None
    DUOUT = None
    DIROUT = None
    DIROUT = None

def CHECK():
    DP = None
    DQ = None
    DIR["A"] = "THIS DRUG IS INACTIVE - DO YOU WISH TO REACTIVATE IT"
    DIR["B"] = "N"
    DIR["0"] = "Y"
    DIR()

    if X in "^N":
        Y = "@1"
    else:
        Y = 100

def PSIU():
    PSIUO = globals()["^PSDRUG(DA,2)"]["^",3]
    PSIUY = PSIUO if PSIUO in "O" else PSIUO + "O"
    globals()["^PSDRUG(DA,2)"]["^",3] = PSIUY

    if globals()["^PSDRUG(DA,0)"]["^"]:
        globals()["^PSDRUG(\"AIUO\",$P(^PSDRUG(DA,0),\"^\"),DA)"] = ""

    if PSIUO:
        del globals()["^PSDRUG(\"IU\",PSIUO,DA)"]

    if PSIUY:
        globals()["^PSDRUG(\"IU\",PSIUY,DA)"] = ""

    del PSIUO
    del PSIUY
    print()

def UNMARK():
    if DISPDRG in globals()["^PSDRUG(\"ACLOZ\")"]:
        DA = DISPDRG

    if DA:
        DIR["0"] = "Y"
        DIR["A",1] = ""
        DIR["A",2] = f"Are you sure you want to unmark {globals()[\"^PSDRUG(DISPDRG,0)\"]}"
        DIR["A"] = "as a Clozapine drug"
        DIR["B"] = "N"
        DIR()

        if X in "Yy":
            CLFLAG = 0
            DR = "17.5///@"
            DIE = DIC
            DIE()

            if CLFLAG == 0:
                print(f"\n{globals()[\"^PSDRUG(DA,0)\"]}\" is now unmarked as a Clozapine drug")
                ASKIT()

    print()

def ASKIT():
    DIR = None
    print("Do you wish to mark this drug as a Lab Monitor drug?")
    DIR["0"] = "Y"
    DIR()

    if DIRUT in globals() or DTOUT in globals() or DUOUT in globals():
        return

    if X in "Nn":
        NFLAG = 1
        del X
        del Y
        del DIR
        return

    if X in "Yy":
        PSSLAB()

def END():
    X = None
    Y = None
    DIR = None
    DR = None
    DIC = None
    DIE = None
    PSIUA = None
    PSIUX = None
    percent = None
    D0 = None
    D1 = None
    DQ = None
    I = None
    Z = None
    DTOUT = None
    DUOUT = None
    DIROUT = None
    DIROUT = None
    del X
    del Y
    del DIR
    del DR
    del DIC
    del DIE
    del PSIUA
    del PSIUX
    del percent
    del D0
    del D1
    del DQ
    del I
    del Z
    del DTOUT
    del DUOUT
    del DIROUT
    del DIROUT

def PSSCLOZ():
    pass

def MONCLOZ():
    pass

def PSSLAB():
    pass