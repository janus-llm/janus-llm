# BIR/RTR-API FOR CLINICAL REMINDERS; 21 Jan 08
# 1.0;PHARMACY DATA MANAGEMENT;**133**;9/30/97;Build 1

# Return AND or VAC index of File 50
# PSSCRIX = AND or VAC
# PSSCRIV = Data value for Index
def IX(PSSCRIX, PSSCRIV):
    if PSSCRIX != "AND" and PSSCRIX != "VAC":
        return
    if not PSSCRIV:
        return
    ^TMP($J,PSSCRIX,PSSCRIV) = ^PSDRUG(PSSCRIX,PSSCRIV)

# Return Drug Name from File 50
# PSSCLID = File 50 IEN
def DRUG(PSSCLID):
    return $P(^PSDRUG(+PSSCLID,0),"^")

# Return Pharmacy Orderable Item Pointer from File 50
# PSSCLII = File 50 IEN
def ITEM(PSSCLII):
    return $P(^PSDRUG(+PSSCLII,2),"^")

# Return Drug ingredient Name
def ING(PSSING):
    return $P(^PS(50.416,PSSING,0),"^")

# Return Drug Ingredient IEN
def IEN(PSSING):
    if not ^PS(50.416,"B",PSSING):
        return -1
    return $O(^PS(50.416,"B",PSSING,0))

# Return number of entries in PS(55).
def NEPS():
    ADD = 0
    DA = 0
    DA1 = 0
    DFN = 0
    DRUG = 0
    IND = 0
    NE = 0
    SDATE = 0
    SOL = 0
    STARTD = 0
    TEMP = 0

    # DBIA #4181
    (DFN, IND, NE) = (0, 0, 0)
    while DFN != 0:
        DFN = +$O(^PS(55, DFN))
        if DFN == 0:
            break

        # Process Unit Dose.
        DA = 0
        while DA != 0:
            DA = +$O(^PS(55, DFN, 5, DA))
            if DA == 0:
                break

            TEMP = ^PS(55, DFN, 5, DA, 2)
            STARTD = $P(TEMP, U, 2)
            if STARTD == "":
                continue

            # If the order is purged then SDATE is 1.
            SDATE = $P(TEMP, U, 4)
            if SDATE == 1:
                continue

            DA1 = 0
            while DA1 != 0:
                DA1 = +$O(^PS(55, DFN, 5, DA, 1, DA1))
                if DA1 == 0:
                    break

                DRUG = $P(^PS(55, DFN, 5, DA, 1, DA1, 0), U, 1)
                if DRUG == "":
                    continue

                NE = NE + 1

        # Process the IV mutiple.
        DA = 0
        while DA != 0:
            DA = +$O(^PS(55, DFN, "IV", DA))
            if DA == 0:
                break

            TEMP = ^PS(55, DFN, "IV", DA, 0)
            STARTD = $P(TEMP, U, 2)
            if STARTD == "":
                continue

            SDATE = $P(TEMP, U, 3)
            if SDATE == 1:
                continue

            # Process Additives
            DA1 = 0
            while DA1 != 0:
                DA1 = +$O(^PS(55, DFN, "IV", DA, "AD", DA1))
                if DA1 == 0:
                    break

                ADD = $P(^PS(55, DFN, "IV", DA, "AD", DA1, 0), U, 1)
                if ADD == "":
                    continue

                DRUG = $P(^PS(52.6, ADD, 0), U, 2)
                if DRUG == "":
                    continue

                NE = NE + 1

            # Process Solutions
            DA1 = 0
            while DA1 != 0:
                DA1 = +$O(^PS(55, DFN, "IV", DA, "SOL", DA1))
                if DA1 == 0:
                    break

                SOL = $P(^PS(55, DFN, "IV", DA, "SOL", DA1, 0), U, 1)
                if SOL == "":
                    continue

                DRUG = $P(^PS(52.7, SOL, 0), U, 2)
                if DRUG == "":
                    continue

                NE = NE + 1

    return NE