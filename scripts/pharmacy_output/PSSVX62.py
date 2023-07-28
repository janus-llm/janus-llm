# COMPILED XREF FOR FILE #52.61 ; 10/30/18

DA[1] = DA
DA = 0

# A1
if 'DIKILL' in globals():
    DIKLM = None
    if DIKM1 == 1:
        DIKLM = 1
    exec(DIKM1)

# 0
A:
DA = DA + 1
if DA <= 0:
    DA = 0
    exec(END)

# 1
DIKZ[0] = globals().get(f'^PS(52.6,{DA[1]},1,{DA},0)', {})
X = DIKZ[0].get('X', '')
if X != '':
    del globals()[f'^PS(52.6,"C",{X[:30]},{DA[1]},{DA})']
    exec('A')
    if 'DIKILL' in globals():
        exec(DIKILL)

# END
exec('^PSSVX63')