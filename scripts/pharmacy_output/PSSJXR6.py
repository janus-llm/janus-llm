# COMPILED XREF FOR FILE #55.03 ; 03/07/23

DA = 0

# A1
if 'DIKILL' in locals():
    if DIKM1 == 1:
        DIKLM = 1
    # G @DIKM1

# 0
DA = DA(1) + 1
if DA <= 0:
    DA = 0
    # G END

# 1
DIKZ(0) = ^PS(55,DA(1),"P",DA,0)
X = DIKZ(0)[0]
if X != "":
    KREF^PSOHELP1()

if 'DIKLM' not in locals():
    # G A
    pass
# Q:$D(DIKILL)

# END
# G ^PSSJXR7