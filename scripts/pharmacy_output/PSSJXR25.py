# COMPILED XREF FOR FILE #55.0108 ; 03/07/23

# Initialize DA variable
DA = 0

# Label A1
def A1():
    global DA
    # Check if DISET variable is defined
    if '$D(DISET)':
        # Clear DIKLM variable
        del DIKLM
        # Set DIKLM to 1 if DIKM1 is 1
        if DIKM1 == 1:
            DIKLM = 1
        # Go to label specified by DIKM1
        return eval(DIKM1)

# Label 0
def _0():
    global DA
    # Set DA to the next entry in ^PS(55,DA(1),"SCTALK") global
    DA = $O(^PS(55,DA(1),"SCTALK",DA))
    # If DA is less than or equal to 0, set DA to 0 and go to END label
    if DA <= 0:
        DA = 0
        return END

# Label A
def A():
    global DA
    # Get DIKZ(0) value from ^PS(55,DA(1),"SCTALK",DA,0) global
    DIKZ(0) = ^PS(55,DA(1),"SCTALK",DA,0)
    # Get X value from DIKZ(0)
    X = $P(DIKZ(0),U,2)
    # If X is not empty, set ^PS(55,"ASTALK",DA(1)) to X
    if X != "":
        ^PS(55,"ASTALK",DA(1)) = X
    # If DIKLM is not defined, go to label A
    if not '$D(DIKLM)':
        return A
    # Quit if DISET is defined
    if '$D(DISET)':
        return
    # Go to END label
    return END

# Label 1
def _1():
    global DA
    # Get DIKZ(0) value from ^PS(55,DA(1),"SCTALK",DA,0) global
    DIKZ(0) = ^PS(55,DA(1),"SCTALK",DA,0)
    # Get X value from DIKZ(0)
    X = $P(DIKZ(0),U,2)
    # If X is not empty, set ^PS(55,"ASTALK",DA(1)) to X
    if X != "":
        ^PS(55,"ASTALK",DA(1)) = X
    # If DIKLM is not defined, go to label A
    if not '$D(DIKLM)':
        return A
    # Quit if DISET is defined
    if '$D(DISET)':
        return
    # Go to END label
    return END

# Label END
def END():
    return ^PSSJXR26()