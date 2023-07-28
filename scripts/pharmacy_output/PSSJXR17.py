# PSSJXR17 ; COMPILED XREF FOR FILE #55.1153 ; 03/07/23

DA = 0
DA_1 = 0

# A1 ;
if "DIKILL" in locals():
    del DIKLM
    if DIKM1 == 2:
        DIKLM = 1
    if DIKM1 != 2 and not DIKPUSH.get(2):
        DIKPUSH[2] = 1
        DA_2 = DA_1
        DA_1 = DA
        DA = 0
    goto(DIKM1)

# A
DA_1 = next((x for x in range(DA_1 + 1, len(^PS(55, DA_2, "IV"))) if ^PS(55, DA_2, "IV", x))
if DA_1 <= 0:
    DA_1 = 0
    goto(END)

# 1 ;
# B
DA = next((x for x in range(DA + 1, len(^PS(55, DA_2, "IV", DA_1, 8))) if ^PS(55, DA_2, "IV", DA_1, 8, x))
if DA <= 0:
    DA = 0
    if DIKM1 == 1:
        goto(A)
    goto(A1)

# 2 ;
DIKZ_0 = ^PS(55, DA_2, "IV", DA_1, 8, DA, 0)
X = $P(DIKZ_0, U, 1)
if X != "":
    del ^PS(55, DA_2, "IV", DA_1, 8, "B", X[:30], DA)
if "DIKLM" not in locals():
    goto(B)
if "DIKILL" in locals():
    goto(B)
goto(B)

END:
goto(^PSSJXR18)