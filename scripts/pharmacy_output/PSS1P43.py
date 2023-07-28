# BIR/DMA-fix bad interaction names
# 03/15/01 12:52
# 1.0; PHARMACY DATA MANAGEMENT;**43**;9/30/97

# Reference to ^PS(56 supported by DBIA #2133
# Reference to ^PS(50.416 supported by DBIA #2196

DA = 0
while DA:
    DA = DA + 1
    X = ^PS(56,DA,0)
    PSN = {}
    PSNN = {}

    NAM = X[0]
    PSN[0] = X[1]
    PSN[0] = ^PS(50.416,PSN[0],0)[0]
    PSNN[PSN[0]] = ""
    PSN[0] = X[2]
    PSN[0] = ^PS(50.416,PSN[0],0)[0]
    PSNN[PSN[0]] = ""

    NA1 = ""
    NA1 = PSNN[0] + "/" + PSNN[PSNN[0]]

    if NA1 != NAM:
        print(".")
        DIE = "^PS(56,"
        DR = ".01////" + NA1
        ^DIE
    DA = DA - 1

DA = ""
DIE = ""
DR = ""
NA1 = ""
NAM = ""
PSN = {}
PSNN = {}
X = ""