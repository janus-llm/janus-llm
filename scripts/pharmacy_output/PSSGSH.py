# BIR/CML3-SCHEDULE HELP TEXT ; 09/09/97 8:03
# 1.0;PHARMACY DATA MANAGEMENT;;9/30/97

def ENSH3():
    global PSGST, PSGDDFLG
    if not PSGST:
        PSGST = $P($G(^PS(53.1,DA,0)),"^",7)
        PSGDDFLG = 1
    ENSH()

def ENSH5():
    global PSGST, PSGDDFLG
    if not PSGST:
        PSGST = $P($G(^PS(55,DA(1),5,DA,0)),"^",7)
        PSGDDFLG = 1
    ENSH()

def ENQ():
    if $D(^DD(53.1,26,3)):
        print('    ', ^(3))

def ENSH():
    global D, DA, DIC, DIE, DZ, Y
    print("'STAT', 'ONCE', 'NOW', and 'DAILY' are acceptable schedules.")
    if X?1"???".E:
        for Q in range(1, len($T(HT)) + 1):
            print('    ', $P($T(HT+Q),";",3))
    if X?1"???".E:
        Q = input("(Press RETURN to continue.) ")
        if not Q:
            if not $T:
                print('\x07')
            Q = "^"
        if Q == "^":
            if $D(PSGDDFLG):
                del PSGDDFLG, PSGST
    DIC = "^PS(51.1,"
    DIC(0) = "E"
    D = "APPSJ"
    DIC("W") = "W ""  "","""
    if $D(PSJPWD),PSJPWD:
        DIC("W") = DIC("W") + "$S($D(^PS(51.1,+Y,1,PSJPWD,0)):$P(^(0),""^"",2),1:$P(^PS(51.1,+Y,0),""^"",2))"
    else:
        DIC("W") = DIC("W") + "$P(^(0),""^"",2)"
    if $D(PSGST):
        DIC("S") = "I $P(^(0),""^"",5)" + "'" + (PSGST != "O") + "'=""O"""
    IX^DIC
    if $D(PSGDDFLG):
        del PSGDDFLG, PSGST

def HT():
    return [
        "  This is the frequency (ONLY) with which the doses are to be administered.",
        "Several forms of entry are acceptable, such as Q6H, 09-12-15, STAT, QOD,",
        "and MO-WE-FR@AD (where MO-WE-FR are days of the week, and AD is the admin",
        "times).  The schedule will show on the MAR, labels, etc.  No more than ONE",
        "space (Q3H 4 or Q4H PRN) in the schedule is acceptable.  If the letters PRN",
        "are found as part of the schedule, no admin times will print on the MAR or",
        "labels, and the PICK LIST will always show a count of zero (0).",
        "Avoid using notation such as W/F (with food) or WM (with meals) in the",
        "schedule as it may cause erroneous calculations.  That information should",
        "be entered into the SPECIAL INSTRUCTIONS.",
        "When using the MO-WE-FR@AD schedule, please remember that this type of",
        "schedule will not work properly without the "@" character and at least one",
        "admin time, and that at least the first two letters of each weekday entered",
        "is needed."
    ]