# COMPILED XREF FOR FILE #55.174 ; 03/07/23

DA = [0, 0]
while True:
    if 'DIKILL' in locals():
        del DIKLM
        if DIKM1 == 2:
            DIKLM = 1
        elif DIKM1 != 2 and not DIKPUSH.get(2):
            DIKPUSH[2] = 1
            DA[2], DA[1], DA[0] = DA[1], DA[0], 0
        goto = DIKM1

    DA[1] = next(iter(filter(lambda x: x > 0, [DA1 for DA1 in range(DA[1] + 1, len(PS[55][DA[2]]['PC']) + 1)])), 0)
    if DA[1] <= 0:
        DA[1] = 0
        break

    while True:
        DA = next(iter(filter(lambda x: x > 0, [DA for DA in range(DA[0] + 1, len(PS[55][DA[2]]['PC'][DA[1]]['PCH']) + 1)])), 0)
        if DA <= 0:
            if DIKM1 == 1:
                break
            else:
                goto = 'A'
                break

        DIKZ = PS[55][DA[2]]['PC'][DA[1]]['PCH'][DA]
        X = DIKZ.get(0, {}).get('field1')
        if X != "":
            del PS[55][DA[2]]['PC'][DA[1]]['PCH']['B'][X[:30]][DA]

        if 'DIKLM' not in locals():
            break
        if 'DIKILL' in locals():
            break

goto = 'PSSJXR19'