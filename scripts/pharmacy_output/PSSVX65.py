# COMPILED XREF FOR FILE #52.61 ; 10/30/18
# 
DA[1] = DA
DA = 0

# A1 ;
if "DISET" in globals():
    del DIKLM
    if DIKM1 == 1:
        DIKLM = 1
        # G @DIKM1

# 0 ;
# A
DA = next((DA for DA in range(1, len(^PS(52.6, DA[1], 1))) if ^PS(52.6, DA[1], 1, DA) != ""), 0)

# 1 ;
DIKZ[0] = ^PS(52.6, DA[1], 1, DA, 0)
X = DIKZ[0].split("^")[0]
if X != "":
    ^PS(52.6, "C", X[:30], DA[1], DA) = ""

if "DIKLM" not in globals():
    # G A
    pass

# Q:$D(DISET)
# END
# G ^PSSVX66