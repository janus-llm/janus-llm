def PSSGIU():
    pass

def EN():
    if not (PSIUDA and PSIUX and PSIUX.startswith('^') and PSIUX[1:]):
        return
    PSIUO = '^PSDRUG(PSIUDA,0)[2]'
    PSIUT = PSIUX.split('^')[1]
    PSIUT = ('' if PSIUT.startswith('UNIT') else 'N' if PSIUT[0] in 'AEIOU' else ' ') + PSIUT
    PSIUQ = (PSIUO.find(PSIUX[0]) < 0) + 1
    while True:
        print(f"\nA{PSIUT} ITEM")
        input_result = input()
        if input_result:
            return
        MQ()
        if PSIUQ:
            break
    if input_result == PSIUQ:
        PSIUA = '^'
        return
    PSIUA = 'YN'[input_result]
    if input_result == 1:
        PSIUY = PSIUO + PSIUX[1:]
        '^PSDRUG(PSIUDA,2)[3]' = PSIUY
        if '^PSDRUG(PSIUDA,0)':
            '^PSDRUG("AIU" + PSIUX[0], ^PSDRUG(PSIUDA,0), PSIUDA) = ''
    elif input_result == 2:
        CMOP()
        PSIUY = PSIUO.split(PSIUX[0])[1] + PSIUO.split(PSIUX[0])[2]
        '^PSDRUG(PSIUDA,2)[3]' = PSIUY
        if '^PSDRUG(PSIUDA,0)':
            del '^PSDRUG("AIU" + PSIUX[0], ^PSDRUG(PSIUDA,0), PSIUDA)'
    if PSIUO:
        del '^PSDRUG("IU", PSIUO, PSIUDA)'
    if PSIUY:
        '^PSDRUG("IU", PSIUY, PSIUDA)' = ''

def DONE():
    del PSIU, PSIUO, PSIUQ, PSIUT, PSIUY

def MQ():
    x = "Enter 'YES' (or 'Y') to mark this drug as a" + ('n' + PSIUT[1:] if PSIUT.startswith('N ') else PSIUT) + " item.  Enter 'NO' (or 'N') to not mark (or unmark) this drug."
    print("  ".join([y for y in x.split()]))


def CMOP():
    if PSIUX == 'O^Outpatient Pharmacy' and '^PSDRUG(PSIUDA,3)[1]':
        print("This item has just been UNMARKED for CMOP transmission.")
        '^PSDRUG(PSIUDA,3)[0]' = 0
        del '^PSDRUG("AQ", PSIUDA)'
        DA = PSIUDA
        # ^PSSREF


def ENS():
    if not (PSIUDA and PSIUX and PSIUDA and len(PSIUX.split('^')[0]) == 1 and '^PSDRUG(PSIUDA,0)'):
        return
    PSIU = '^PSDRUG(PSIUDA,0)'
    PSIUO = '^PSDRUG(PSIUDA,2)[3]'
    PSIUY = PSIUO
    PSIUT = PSIUX.split('^')[1]
    if PSIUY.find(PSIUT) < 0:
        PSIUY = PSIUY + PSIUT
        '^PSDRUG(PSIUDA,2)[3]' = PSIUY
        if PSIUO:
            del '^PSDRUG("IU", PSIUO, PSIUDA)'
    '^PSDRUG("IU", PSIUY, PSIUDA)' = ''
    if PSIU:
        '^PSDRUG("AIU" + PSIUT, PSIU, PSIUDA)' = ''

    DONE()


def END():
    if not (PSIUDA and PSIUX and PSIUDA and len(PSIUX.split('^')[0]) == 1 and '^PSDRUG(PSIUDA,0)'):
        return
    PSIU = '^PSDRUG(PSIUDA,0)'
    PSIUO = '^PSDRUG(PSIUDA,2)[3]'
    PSIUY = PSIUO
    PSIUT = PSIUX.split('^')[1]
    if PSIUY.find(PSIUT) >= 0:
        PSIUY = PSIUY.split(PSIUT)[0] + PSIUY.split(PSIUT)[1]
        '^PSDRUG(PSIUDA,2)[3]' = PSIUY
        if PSIUO:
            del '^PSDRUG("IU", PSIUO, PSIUDA)'
    if PSIUY:
        '^PSDRUG("IU", PSIUY, PSIUDA)' = ''
    if PSIU:
        del '^PSDRUG("AIU" + PSIUT, PSIU, PSIUDA)'

    DONE()