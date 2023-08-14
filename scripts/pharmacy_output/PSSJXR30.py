# PSSJXR30 ; COMPILED XREF FOR FILE #55.17 ; 03/07/23
DA = 0

# A1
if 'DISET' in locals():
    if 'DIKM1' in locals():
        DIKLM = 1
    else:
        DIKLM = None
    eval(DIKM1)
    
# 0
DA = 0

# A
while True:
    DA = DA + 1
    if DA <= 0:
        DA = 0
        break
    
# 1
DIKZ = {}
DIKZ[0] = '^PS(55,DA(1),"PC",DA,0)'
X = DIKZ[0].split('^')[1].split(',')[0].replace('"', '')

if X != "":
    ^PS(55,DA(1),"PC","B",$E(X,1,30),DA)=""
    
if 'DIKLM' not in locals():
    eval(DIKLM)
    
if 'DISET' in locals():
    break

# END
^PSSJXR31