# BIR/LDT - API FOR INFORMATION FROM FILE 50.7; 5 Sep 03
# 1.0;PHARMACY DATA MANAGEMENT;**85**;9/30/97

def lookup():
    PSSSCRN = ''
    PSSLUPAR = []
    PSSLUPP = 0
    PSSLKIEN = ''
    PSSCT507 = 0
    PSSXSUB = ''
    SCR_S = PSSS if PSSS else ''
    if PSSFT == "??":
        loop(5)
        return
    PSSXSUB = ''
    set_xsub()
    TMP_DILIST_J = {}
    TMP_J_PSSLDONE = {}
    PSSSCRN = SCR_S
    PSSD = PSSD if PSSD else 'B'
    parse(PSSD)
    if not PSSLUPAR:
        TMP_J_LIST_0 = "-1^NO DATA FOUND"
        return
    for PSSLUPP in PSSLUPAR:
        SCR_S = PSSSCRN
        find(50.7, "@;.01;.02IE;.04IE", "QPB" + ("X" if PSSLUPAR[PSSLUPP][1] else ""), PSSFT, PSSLUPAR[PSSLUPP], SCR_S)
        if TMP_DILIST_J[0] <= 0:
            continue
        for PSS_2 in TMP_DILIST_J:
            PSSLKIEN = TMP_DILIST_J[PSS_2][0]
            if PSSLKIEN not in TMP_J_PSSLDONE:
                TMP_J_PSSLDONE[PSSLKIEN] = ''
                PSSCT507 += 1
                TMP_J_LIST_0 = TMP_DILIST_J[PSS_2][0]
                TMP_J_LIST[TMP_DILIST_J[PSS_2][0], .01] = TMP_DILIST_J[PSS_2][2]
                TMP_J_LIST[PSSXSUB if PSSXSUB else 'B', TMP_DILIST_J[PSS_2][2], TMP_DILIST_J[PSS_2][0]] = ''
                TMP_J_LIST[TMP_DILIST_J[PSS_2][0], .02] = TMP_DILIST_J[PSS_2][3] if TMP_DILIST_J[PSS_2][4] else ''
                TMP_J_LIST[TMP_DILIST_J[PSS_2][0], .04] = TMP_DILIST_J[PSS_2][5] if TMP_DILIST_J[PSS_2][6] else ''
    TMP_J_LIST_0 = PSSCT507 if PSSCT507 else "-1^NO DATA FOUND"
    TMP_DILIST_J.clear()
    TMP_J_PSSLDONE.clear()

def set_zro():
    TMP_J_LIST[PSS_1, .01] = PSS50P7[50.7,PSS_1,.01,"I"]
    TMP_J_LIST['B', PSS50P7[50.7,PSS_1,.01,"I"], +PSS_1] = ''
    TMP_J_LIST[PSS_1, .02] = PSS50P7[50.7,PSS_1,.02,"I"] + "^" + PSS50P7[50.7,PSS_1,.02,"E"] if PSS50P7[50.7,PSS_1,.02,"I"] else ''
    TMP_J_LIST[PSS_1, .03] = PSS50P7[50.7,PSS_1,.03,"I"] + "^" + PSS50P7[50.7,PSS_1,.03,"E"] if PSS50P7[50.7,PSS_1,.03,"I"] else ''
    TMP_J_LIST[PSS_1, .04] = PSS50P7[50.7,PSS_1,.04,"I"] + "^" + PSS50P7[50.7,PSS_1,.04,"E"] if PSS50P7[50.7,PSS_1,.04,"I"] else ''
    TMP_J_LIST[PSS_1, .05] = PSS50P7[50.7,PSS_1,.05,"I"]
    TMP_J_LIST[PSS_1, .06] = PSS50P7[50.7,PSS_1,.06,"I"] + "^" + PSS50P7[50.7,PSS_1,.06,"E"] if PSS50P7[50.7,PSS_1,.06,"I"] else ''
    TMP_J_LIST[PSS_1, .07] = PSS50P7[50.7,PSS_1,.07,"I"] + "^" + PSS50P7[50.7,PSS_1,.07,"E"] if PSS50P7[50.7,PSS_1,.07,"I"] else ''
    TMP_J_LIST[PSS_1, .08] = PSS50P7[50.7,PSS_1,.08,"I"]
    TMP_J_LIST[PSS_1, .09] = PSS50P7[50.7,PSS_1,.09,"I"] + "^" + PSS50P7[50.7,PSS_1,.09,"E"] if PSS50P7[50.7,PSS_1,.09,"I"] else ''
    TMP_J_LIST[PSS_1, 8] = PSS50P7[50.7,PSS_1,8,"I"] + "^" + PSS50P7[50.7,PSS_1,8,"E"] if PSS50P7[50.7,PSS_1,8,"I"] else ''
    TMP_J_LIST[PSS_1, 5] = PSS50P7[50.7,PSS_1,5,"I"] + "^" + PSS50P7[50.7,PSS_1,5,"E"] if PSS50P7[50.7,PSS_1,5,"I"] else ''

def set_zr2():
    TMP_J_LIST[PSS_2, .01] = PSS50P7[50.7,PSS_2,.01,"I"]
    TMP_J_LIST['B', PSS50P7[50.7,PSS_2,.01,"I"], +PSS_2] = ''
    TMP_J_LIST[PSS_2, .02] = PSS50P7[50.7,PSS_2,.02,"I"] + "^" + PSS50P7[50.7,PSS_2,.02,"E"] if PSS50P7[50.7,PSS_2,.02,"I"] else ''

def set_syn():
    TMP_J_LIST[PSSIEN, "SYN", +PSS_1, .01] = PSS50P7[50.72,PSS_1,.01,"I"]

def set_pti():
    TMP_J_LIST[PSS_1, .01] = PSS50P7[50.7,PSS_1,.01,"I"]
    TMP_J_LIST['B', PSS50P7[50.7,PSS_1,.01,"I"], +PSS_1] = ''
    TMP_J_LIST[PSS_1, .02] = PSS50P7[50.7,PSS_1,.02,"I"] + "^" + PSS50P7[50.7,PSS_1,.02,"E"] if PSS50P7[50.7,PSS_1,.02,"I"] else ''
    TMP_J_LIST[PSS_1, 7] = PSS50P7[50.7,PSS_1,7,"I"]
    TMP_J_LIST[PSS_1, 7.1] = PSS50P7[50.7,PSS_1,7.1,"I"]

def loop(PSS):
    CNT = 0
    PSSIEN = 0
    while True:
        PSSIEN = next((PSSIEN for PSSIEN in range(PSSIEN, len(PS[50.7]))), False)
        if not PSSIEN:
            break
        ND = PS[50.7][PSSIEN][0][3]
        if not ND or ND > PSSFL:
            globals()[PSS](5)
            CNT += 1
    TMP_J_LIST_0 = CNT if CNT else "-1^NO DATA FOUND"

def one():
    PSS50P7 = {}
    GETS_DIQ(50.7, +PSSIEN, ".01;.02;.03;.04;.05;.06;.07;.08;.09;8;5", "IE", PSS50P7)
    for PSS_1 in PSS50P7[50.7]:
        set_zro()
        CNT += 1

def two():
    CNT2 = 0
    PSS50P7 = {}
    GETS_DIQ(50.7, +PSSIEN, ".01;.02;2*", "IE", PSS50P7)
    for PSS_1 in PSS50P7[50.72]:
        set_syn()
        CNT2 += 1
    for PSS_2 in PSS50P7[50.7]:
        set_zr2()
        CNT += 1
    TMP_J_LIST[PSSIEN, "SYN", 0] = CNT2 if CNT2 else "-1^NO DATA FOUND"

def three():
    PSS50P7 = {}
    GETS_DIQ(50.7, +PSSIEN, ".01;.02;7;7.1", "IE", PSS50P7)
    for PSS_1 in PSS50P7[50.7]:
        set_pti()
        CNT += 1

def four():
    PSS50P7 = {}
    GETS_DIQ(50.7, +PSSIEN, ".01;.02", "IE", PSS50P7)
    for PSS_2 in PSS50P7[50.7]:
        set_zr2()
        CNT += 1

def five():
    FIND_DIC(50.7, "@;.01;.02IE;.04IE", "QP", "`" + PSSIEN, "B", SCR("S"))
    TMP_J_LIST_0 = TMP_DILIST_J[0]
    CNT += 1
    for PSS_2 in TMP_DILIST_J:
        TMP_J_LIST[PSS_2, .01] = TMP_DILIST_J[PSS_2][0]
        TMP_J_LIST['B', TMP_DILIST_J[PSS_2][0], +TMP_DILIST_J[PSS_2][0]] = ''
        TMP_J_LIST[PSS_2, .02] = TMP_DILIST_J[PSS_2][2] if TMP_DILIST_J[PSS_2][3] else ''
        TMP_J_LIST[PSS_2, .04] = TMP_DILIST_J[PSS_2][4] if TMP_DILIST_J[PSS_2][5] else ''
    TMP_DILIST_J.clear()

def set_xsub():
    if not PSSD:
        return
    PSSLSXCT = 0
    for PSSLSX in range(1, len(PSSD) + 1):
        if PSSD[PSSLSX - 1] == "^":
            PSSLSXCT += 1
    PSSLSXCT += 1
    PSSLCNT = 0
    for PSSLSX in range(1, PSSLSXCT + 1):
        PSSDSUB = PSSD.split("^")[PSSLSX - 1]
        if PSSLCNT > 1:
            PSSXSUB = ""
        else:
            PSSXSUB = PSSDSUB if PSSDSUB else PSSXSUB
            PSSLCNT += 1
    if PSSLCNT > 1:
        PSSXSUB = ""