# COMPILED XREF FOR FILE #55.6114 ; 03/07/23

DA = 0
DA_1 = 0

# A1 ;
if 'DIKILL' in globals():
    if DIKM1 == 2:
        DIKLM = 1
    elif DIKM1 != 2 and not globals().get('DIKPUSH', {}).get(2):
        DIKPUSH[2] = 1
        DA_2 = DA_1
        DA_1 = DA
        DA = 0
        eval(DIKM1)
        
# A
DA_1 = next((i for i in range(DA_1+1, len(^PS[55,DA_2,5])+1)), 0)
if DA_1 <= 0:
    DA_1 = 0
    eval('END')

# 1 ;
DA = next((i for i in range(DA+1, len(^PS[55,DA_2,5,DA_1,14])+1)), 0)
if DA <= 0:
    DA = 0
    if DIKM1 == 1:
        eval('A')

# 2 ;
DIKZ_0 = ^PS[55,DA_2,5,DA_1,14,DA,0]
X = $p(DIKZ_0, U, 1)
if X != "":
    del ^PS[55,DA_2,5,DA_1,14,"B"][$e(X, 1, 30)][DA]
if not 'DIKLM' in globals():
    eval('B')
if 'DIKILL' in globals():
    eval('B')
    
# END
eval('^PSSJXR21')