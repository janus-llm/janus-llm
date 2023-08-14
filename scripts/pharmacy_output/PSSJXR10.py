# COMPILED XREF FOR FILE #55.02 ; 03/07/23
DA[2] = DA[1]
DA[1] = 0
DA = 0

# A1
if 'DIKILL' in globals():
    del DIKLM
    if DIKM1 == 2:
        DIKLM = 1
    if DIKM1 != 2 and not DIKPUSH.get(2):
        DIKPUSH[2] = 1
        DA[2] = DA[1]
        DA[1] = DA
        DA = 0
    Goto(DIKM1)

# A
DA[1] = $O(^PS(55, DA[2], "IV", DA[1]))
if DA[1] <= 0:
    DA[1] = 0
    Goto(END)

# 1
# B
DA = $O(^PS(55, DA[2], "IV", DA[1], "AD", DA))
if DA <= 0:
    DA = 0
    if DIKM1 == 1:
        Goto(A)
    Goto(A)

# 2
DIKZ[0] = ^PS(55, DA[2], "IV", DA[1], "AD", DA, 0)
X = $P(DIKZ[0], U, 2)
if X != "":
    exec(^DD(55.02, .02, 1, 1, 2))

DIKZ[0] = ^PS(55, DA[2], "IV", DA[1], "AD", DA, 0)
X = $P(DIKZ[0], U, 3)
if X != "":
    exec(^DD(55.02, .03, 1, 1, 2))

DIKZ[0] = ^PS(55, DA[2], "IV", DA[1], "AD", DA, 0)
X = $P(DIKZ[0], U, 1)
if X != "":
    exec(^DD(55.02, .01, 1, 1, 2))

if not 'DIKLM' in globals():
    Goto(B)
if 'DIKILL' in globals():
    Goto(B)
Goto(END)

# END
Goto(^PSSJXR11)