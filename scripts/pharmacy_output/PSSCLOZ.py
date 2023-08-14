def PSSCLOZ():
    # Reference to ^LAB(60 supported by DBIA #10054
    # Reference to ^LAB(61 supported by DBIA #10055

    if 'DISPDRG' not in globals():
        return

    # Variable Definitions
    DA = None
    DIC = None
    DIE = None
    DIK = None
    DINUM = None
    DIR = None
    DR = None
    PSSANS = None
    PSSANS2 = None
    PSSCIM = None
    PSSCLO = None
    PSSCNT = None
    PSSCRN = None
    PSSIEN = None
    PSSLAB1 = None
    PSSLAB2 = None
    PSSLT = None
    PSSLTN = None
    PSSNN = None
    PSSNUM = None
    PSSOPP = None
    PSSPTY = None
    PSSPTYN = None
    PSSSUB = None
    PSSTOT = None
    PSSTUFF = None
    PSSTYP0 = None
    PSSXX = None
    X = None
    Y = None

    DIRUT = False
    DUOUT = False

    # Mark drug for Clozapine and create "ACLOZ" cross-reference.
    DA = DISPDRG
    DIE = 50
    DR = "17.5///^S X=""PSOCLO1"""
    DIE.execute(DA, DR)

CLOZBEG()

# Kill variables.
DIC = None
DIE = None
DIK = None
DIR = None
DR = None
PSSANS = None
PSSANS2 = None
PSSCNT = None
PSSSUB = None
PSSXX = None
X = None
Y = None