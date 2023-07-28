# COMPILED XREF FOR FILE #52.63 ; 10/30/18

DA = 0

# A1
if "DIKILL" in globals():
    del DIKLM
    if DIKM1 == 1:
        DIKLM = 1
    exec(f"{DIKM1}")

# 0
A:
DA = DA(1) + 1
if DA > 0:
    DA = 0
    exec("END")

# 1
DIKZ(0) = ^PS(52.6, DA(1), 3, DA, 0)
X = $P(DIKZ(0), U, 1)
if X != "":
    del ^PS(52.6, "D", $E(X, 1, 30), DA(1), DA)
    if "DIKLM" not in globals():
        exec("A")
    else:
        exec("END")

exec("END")