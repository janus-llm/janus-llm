def KILL1():
    # Kill x-ref from field 2.1 of File 50
    del ^PS(50.7,"A50",X,DA)
    PSSCROSS = 1
    PSPOINT = None
    PSSZA = None
    PSSZS = None
    PSSZOI = None
    PSSTEST = None
    PSSTEST = X
    HOLD()
    PSSPOIDT.EN1()
    UNHOLD()
    PSSZA = 0
    while PSSZA:
        PSSZA = PSSZA + 1
        PSSZOI = $P($G(^PS(52.6,PSSZA,0)),"^",11)
        if PSSZOI:
            $P(^PS(52.6,PSSZA,0),"^",11) = ""
            del ^PS(52.6,"AOI",PSSZOI,PSSZA)
    PSSZS = 0
    while PSSZS:
        PSSZS = PSSZS + 1
        PSSZOI = $P($G(^PS(52.7,PSSZS,0)),"^",11)
        if PSSZOI:
            $P(^PS(52.7,PSSZS,0),"^",11) = ""
            del ^PS(52.7,"AOI",PSSZOI,PSSZS)
    del PSSCROSS


def SET1():
    # Set x-ref from field 2.1 of File 50
    ^PS(50.7,"A50",X,DA) = ""
    PSSCROSS = 1
    PSPOINT = None
    PSSZA = None
    PSSZS = None
    PSSTEST = None
    PSSTEST = X
    HOLD()
    PSSPOIDT.EN1()
    UNHOLD()
    PSSZA = 0
    while PSSZA:
        PSSZA = PSSZA + 1
        $P(^PS(52.6,PSSZA,0),"^",11) = X
        ^PS(52.6,"AOI",X,PSSZA) = ""
    PSSZS = 0
    while PSSZS:
        PSSZS = PSSZS + 1
        $P(^PS(52.7,PSSZS,0),"^",11) = X
        ^PS(52.7,"AOI",X,PSSZS) = ""
    del PSSCROSS


def K526():
    # Kill x-ref from generic pointer in IV Additives file
    del ^PSDRUG("A526",X,DA)
    PSSTEST = None
    PSSVAR = None
    PSSCROSS = 1
    PSSTEST = $P($G(^PS(52.6,DA,0)),"^",11)
    if PSSTEST:
        HOLD()
        PSSPOIDT.EN1()
        UNHOLD()
    PSSVAR = $P($G(^PS(52.6,DA,0)),"^",11)
    if PSSVAR:
        $P(^PS(52.6,DA,0),"^",11) = ""
        del ^PS(52.6,"AOI",PSSVAR,DA)
    del PSSCROSS


def S526():
    # Set x-ref from generic pointer in IV Additives file
    ^PSDRUG("A526",X,DA) = ""
    PSSTEST = None
    PSSCROSS = 1
    PSSTEST = $P($G(^PSDRUG(X,2)),"^")
    if PSSTEST:
        HOLD()
        PSSPOIDT.EN1()
        UNHOLD()
    if PSSTEST:
        $P(^PS(52.6,DA,0),"^",11) = PSSTEST
        ^PS(52.6,"AOI",PSSTEST,DA) = ""
    del PSSTESTX,PSSCROSS


def K527():
    # Kill x-ref from Generic pointer in IV Solutions file
    del ^PSDRUG("A527",X,DA)
    PSSTEST = None
    PSSVAR = None
    PSSCROSS = 1
    PSSTEST = $P($G(^PS(52.7,DA,0)),"^",11)
    if PSSTEST:
        HOLD()
        PSSPOIDT.EN1()
        UNHOLD()
    PSSVAR = $P($G(^PS(52.7,DA,0)),"^",11)
    if PSSVAR:
        $P(^PS(52.7,DA,0),"^",11) = ""
        del ^PS(52.7,"AOI",PSSVAR,DA)
    del PSSCROSS


def S527():
    # Set x-ref from Generic pointer in IV Solutions file
    ^PSDRUG("A527",X,DA) = ""
    PSSTEST = None
    PSSCROSS = 1
    PSSTEST = $P($G(^PSDRUG(X,2)),"^")
    if PSSTEST:
        HOLD()
        PSSPOIDT.EN1()
        UNHOLD()
    if PSSTEST:
        $P(^PS(52.7,DA,0),"^",11) = PSSTEST
        ^PS(52.7,"AOI",PSSTEST,DA) = ""
    del PSSTESTX,PSSCROSS


def HOLD():
    PSSHDZX = X
    PSSHDZDA = DA


def UNHOLD():
    X = PSSHDZX
    DA = PSSHDZDA
    del PSSHDZX,PSSHDZDA