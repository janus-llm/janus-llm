def ENSV():
    PSSPKG = None
    if 'PSJPP' in globals():
        PSSPKG = FIND1('DIC', '9.4', '', 'O', PSJPP, 'C')
    if 'PSJPP' not in globals() or not PSJPP or PSJPP.endswith('E') or not PSSPKG:
        return
    if 'PSJX' not in globals():
        return
    if 'PSJW' in globals() and (not PSJW or not globals()['^SC'](PSJW, 0)):
        del globals()['PSJW']
    D, DIC, DIE, Q, QX, SDW, SWD, X, X0, X1, X2, XT, Y, Z = None, None, None, None, None, None, None, None, None, None, None, None, None, None
    EN('PSSJSV')

def ENSVI():
    PSSPKG = None
    if 'PSJPP' in globals():
        PSSPKG = FIND1('DIC', '9.4', '', 'O', 'PSJPP', 'C')
    if 'PSJPP' not in globals() or not PSJPP or PSJPP.endswith('E') or not PSSPKG:
        return
    ENI('PSSJSV0')

def ENSPU():
    if 'PSJAT' not in globals() or 'PSJM' not in globals() or 'PSJSCH' not in globals() or 'PSJSD' not in globals() or 'PSJFD' not in globals():
        return
    global PSJC
    PSJC = -1
    if not PSJAT or not PSJM or not PSJSCH or not PSJSD or not PSJFD:
        return
    if 'PSJOSD' not in globals():
        globals()['PSJOSD'] = PSJSD
    if 'PSJOFD' not in globals():
        globals()['PSJOFD'] = PSJFD
    AM, CD, H, HCD, I, J, M, MID, OD, PDL, PLSD, ST, Q, QQ, WD, WDT, WS, WS1, X, X1, X2, XX = None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None
    EN('PSSJSPU')

def ENSPSE():
    PSJPP = 'PSJ'
    PSSTSVZP, PSSTSVXP, PSSTSVXX, PSSTSVYY, PSSTSVZZ, PSSTSVZ1, PSSTSVX1, PSSTSVX2, PSSTSVY1, PSSTSVZ2, PSSDOW = None, None, None, None, None, None, None, None, None, None, None
    ENS()

def ENSE():
    PSSPKG, PSSON, DICATTZ = None, None, None
    if 'PSJPP' in globals():
        PSSPKG = FIND1('DIC', '9.4', '', 'O', PSJPP, 'C')
    if 'PSJPP' not in globals() or not PSJPP or PSJPP.endswith('E') or not PSSPKG:
        return
    if 'PSJW' in globals() and (not PSJW or not globals()['^SC'](PSJW, 0)):
        del globals()['PSJW']
    FQ = 0
    while True:
        DIC = {'DIC': '^PS(51.1', 'DIC(0)': 'EASL', 'DLAYGO': 51.1, 'DIC("DR")': '4////' + PSJPP, 'DIC("W")': 'DICW^PSSJSV0', 'D': 'AP' + PSJPP}
        if 'DIE' in globals():
            DIC['DIE'] = DIE
        if 'DA' in globals():
            DIC['DA'] = DA
        if 'DR' in globals():
            DIC['DR'] = DR
        if 'DIE("NO^")' in globals():
            DIC['DIE("NO^")'] = 'OUTOK'
        if 'XQOR' in globals():
            DIC['XQOR'] = 'EN1^XQOR'
        IX(DIC)
        if Y <= 0:
            break
        PSSON = UP($P(Y, U, 2))
        DIE = {'DIE': '^PS(51.1', 'DA': +Y, 'DR': '[PSSJ ' + ('' if PSJPP == 'PSJ' else 'EXT ') + 'SCHEDULE EDIT]', 'DIE("NO^")': 'OUTOK'}
        ^DIE
    if 'PSJHLDA' in globals():
        EN2('PSSHLSCH')
    if PSJPP == 'PSJ':
        del globals()['PSJPP']
    D0, DI, DISYS, DQ, FQ, X, Y = None, None, None, None, None, None, None

def ENDSD():
    if 'PSJSCH' not in globals() or 'PSJAT' not in globals() or 'PSJTS' not in globals():
        PSJX = ''
        return
    ENDSD()

def ENPSJSHE():
    PSJPP = 'PSJ'
    ENSHE()

def ENSHE():
    PSSPKG = None
    if 'PSJPP' in globals():
        PSSPKG = FIND1('DIC', '9.4', '', 'O', PSJPP, 'C')
    if 'PSJPP' not in globals() or not PSJPP or not PSJPP.isalnum() or not PSSPKG:
        return
    if 'PSJW' in globals() and (not PSJW or not globals()['^SC'](PSJW, 0)):
        del globals()['PSJW']
    FQ = 0
    while True:
        DIC = {'DIC': '^PS(51.15', 'DIC(0)': 'AEQLS', 'DLAYGO': 51.15, 'DIC("DR")': '4////' + PSJPP, 'D': 'AP' + PSJPP}
        if 'DIE' in globals():
            DIC['DIE'] = DIE
        if 'DA' in globals():
            DIC['DA'] = DA
        if 'DR' in globals():
            DIC['DR'] = DR
        IX(DIC)
        if Y <= 0:
            break
        DIE = {'DIE': '^PS(51.15', 'DA': +Y, 'DR': '[PSJ SHIFT EDIT]'}
        ^DIE
    FQ, PSSPKG, X, Y = None, None, None, None

def ENATV():
    ENCHK()

def ENSHV():
    ENSHV()

def OTHLAN():
    DIK, DIC, DIRUT, DIE, DA, DR = None, None, None, None, None, None
    DIE = {'DIE': '^PS(59.7', 'DA': 1, 'DR': '40.2;S:\'$G(X) Y=""@1"";40.21:40.45;@1'}
    ^DIE
    D, DIC, DIRUT, DIE, DA, DR, D, D0, DDER, DI, DQ, % = None, None, None, None, None, None, None, None, None, None, None, None

def TEMSF():
    if 'X' in globals():
        PSSTSVXX = X
    if 'Y' in globals():
        PSSTSVYY = Y
    if 'PSJS' in globals():
        PSSTSVZZ = PSJS
    if 'ZPSJS' in globals():
        PSSTSVZP = ZPSJS
    if 'XPSJS' in globals():
        PSSTSVXP = XPSJS

def TEMSFR():
    X, Y, PSJS, ZPSJS, XPSJS = None, None, None, None, None
    if 'PSSTSVXX' in globals():
        X = PSSTSVXX
    if 'PSSTSVYY' in globals():
        Y = PSSTSVYY
    if 'PSSTSVZZ' in globals():
        PSJS = PSSTSVZZ
    if 'PSSTSVZP' in globals():
        ZPSJS = PSSTSVZP
    if 'PSSTSVXP' in globals():
        XPSJS = PSSTSVXP

def TEMSFX():
    if 'X' in globals():
        PSSTSVX1 = X
    if 'Y' in globals():
        PSSTSVY1 = Y
    if 'PSJS' in globals():
        PSSTSVZ1 = PSJS
    if 'ZPSJS' in globals():
        PSSTSVZ2 = ZPSJS
    if 'XPSJS' in globals():
        PSSTSVX2 = XPSJS

def TEMSFRX():
    X, Y, PSJS, ZPSJS, XPSJS = None, None, None, None, None
    if 'PSSTSVX1' in globals():
        X = PSSTSVX1
    if 'PSSTSVY1' in globals():
        Y = PSSTSVY1
    if 'PSSTSVZ1' in globals():
        PSJS = PSSTSVZ1
    if 'PSSTSVZ2' in globals():
        ZPSJS = PSSTSVZ2
    if 'PSSTSVX2' in globals():
        XPSJS = PSSTSVX2