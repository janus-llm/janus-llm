#PSSDDUT ;BIR/LDT-Pharmacy Data Management DD Utility ;09/15/97
# ;;1.0;PHARMACY DATA MANAGEMENT;**13,18,19,38,56,119,201**;9/30/97;Build 25

def SCH(X):
    if X.find('"') != -1 or ord(X[0]) == 45 or X.isprintable() or len(X.split()) > (4 if 'PRN' in X else 3) or len(X) > 70 or len(X) < 1 or 'P RN' in X or 'PR N' in X:
        return
    if X.islower():
        X = X.upper()
        if 'PSGOES' not in globals():
            print(f"  ({X})")
    if 'Q0' in X:
        return

def ENOS():
    PSGS0XT = ''
    PSGS0Y = ''
    XT = ''
    Y = ''
    if 'PRN' in X or X == 'ON CALL' or X == 'ONCALL' or X == 'ON-CALL':
        return 'Q'
    X0 = X
    if X and 'X' not in X and (X[:4].isdigit() or X[:5].isdigit() and X[4] == '-'):
        X = ENCHK(X)
        if X:
            Y = X
        return 'Q'
    if (X in ['NOW', 'ONCE', 'STAT', 'ONE TIME', 'ONETIME', '1TIME', '1 TIME', '1-TIME', 'ONE-TIME']):
        if 'PSGOES' not in globals():
            print("  (ONCE ONLY)")
        Y = ''
        XT = 'O'
        return 'Q'
    if PSGSCH == X:
        PSGS0Y = PSGAT
        return

def NS():
    X0 = X
    if Y <= 0:
        if 'PSGOES' not in globals():
            print("  (Nonstandard schedule)")
        X = X0
        Y = ''
    if X[:2] == 'AD':
        return 'Q'
    if X[:3] == 'BID' or X[:3] == 'TID' or X[:3] == 'QID':
        XT = 1440 / ('BTQ'.index(X[0]) + 1)
        return 'Q'
    if X[0] == 'Q':
        X = X[1:]
    if not X:
        X = '1' + X
    X1 = int(X[:-len(X.lstrip('+-'))] or 0)
    X = X[X.index(X.lstrip('+-')):]
    X2 = 0
    if X[0] == 'X':
        X2 = 1
        X = X[1:]
    XT = -1
    if X.find("'") != -1 or (X.find('D') != -1 and 'AD' not in X) or 'AM' in X or 'PM' in X or (X.find('HS') != -1 and 'THS' not in X):
        XT = 1440
    elif X.find('H') != -1 and 'TH' not in X:
        XT = 60
    elif X.find('AC') != -1 or X.find('PC') != -1:
        XT = 480
    elif X.find('W') != -1:
        XT = 10080
    elif X.find('M') != -1:
        XT = 40320
    if XT < 0 and Y <= 0:
        X = X0
        return
    X = X0
    if XT:
        if X2:
            XT = XT // X1
        else:
            if X[:2] == 'QO':
                XT = XT * 2
            XT = XT * X1

def Q():
    PSGS0XT = XT if XT else ''
    PSGS0Y = Y if Y else ''
    QX = ''
    SDW = ''
    SWD = ''
    X0 = ''
    XT = ''
    Z = ''

def ENSH5():
    if 'PSGST' not in globals():
        PSGST = str(int(globals()['^PS(55,DA(1),5,DA,0)'].split('^')[7]))
        PSGDDFLG = 1
    ENSH()

def ENSH():
    print("'STAT', 'ONCE', 'NOW', and 'DAILY' are acceptable schedules.")
    if X == '??':
        PSSHLP = []
        PSSHLP.append("This is the frequency (ONLY) with which the doses are to be")
        PSSHLP.append("administered.  Several forms of entry are acceptable, such as")
        PSSHLP.append("Q6H, 09-12-15, STAT, QOD, and MO-WE-FR@AD (where MO-WE-FR are")
        PSSHLP.append("days of the week, and AD is the admin times).  The schedule")
        PSSHLP.append("will show on the MAR, labels, etc.  No more than ONE space")
        PSSHLP.append("(Q3H 4 or Q4H PRN) in the schedule is acceptable.  If the")
        PSSHLP.append("letters PRN ;;are found as part of the schedule, no admin")
        PSSHLP.append("times will print on the MAR or labels, and the PICK LIST will")
        PSSHLP.append("always show a count of zero (0).")
        PSSHLP.append("Avoid using notation such as W/F (with food) or WM (with meals)")
        PSSHLP.append("in the schedule as it may cause erroneous calculations.  That")
        PSSHLP.append("information should be entered into the SPECIAL INSTRUCTIONS.")
        PSSHLP.append("When using the MO-WE-FR@AD schedule, please remember that")
        PSSHLP.append("this type of schedule will not work properly without the '@'")
        PSSHLP.append("character and at least one admin time, and that at least the")
        PSSHLP.append("first two letters of each weekday entered is needed.")
        print("\n".join(PSSHLP))

def ENDLP():
    PSGION = globals()['ION'] if 'ION' in globals() else 'HOME'
    import sys
    sys.stdout.write(f"{ION[len(X):]}")
    X = ION
    sys.stdout.flush()

def ENSTH():
    if X == '??':
        PSSHLP = []
        PSSHLP.append("The TYPE OF SCHEDULE determines how the schedule will be processed.")
        PSSHLP.append("A CONTINUOUS schedule is one in which an action is to take place on a")
        PSSHLP.append("regular basis, such as 'three times a day' or 'once every two days'.")
        PSSHLP.append("A DAY OF THE WEEK schedule is one in which the action is to take")
        PSSHLP.append("place only on specific days of the week.  This type of schedule")
        PSSHLP.append("should have admin times entered with it.  If not, the start time of")
        PSSHLP.append("the order is used as the admin time.  Whenever this type is chosen,")
        PSSHLP.append("the name of the schedule must be in the form of 'MO-WE-FR'.")
        if 'PSJPP' in globals() and PSJPP != '':
            PSSHLP.append("A DAY OF THE WEEK-RANGE schedule is one in which the action to take")
            PSSHLP.append("place only on specific days of the week, but at no specific time of")
            PSSHLP.append("day (no admin times).  Whenever this type is chosen, the name of the")
            PSSHLP.append("schedule must be in the form of 'MO-WE-FR'.")
        PSSHLP.append("A ONE-TIME schedule is one in which the action is to take place once")
        PSSHLP.append("only at a specific date and time.")
        if 'PSJPP' in globals() and PSJPP != '':
            PSSHLP.append("A RANGE schedule is one in which the action will take place within a")
            PSSHLP.append("given date range.")
            PSSHLP.append("A SHIFT schedule is one in which the action will take place within a")
            PSSHLP.append("given range of times of day.")
        print("\n".join(PSSHLP))

def ENDLP():
    if X == '??':
        PSSHLP = []
        PSSHLP.append("This field allows a dispense drug from the DRUG (#50) file to be")
        PSSHLP.append("associated with the DOSING CHECK FREQUENCY (#60.1) field value within the")
        PSSHLP.append("PHARMACY SYSTEM (#59.7) file.")
        if 'PSJPP' in globals() and PSJPP != '':
            PSSHLP.append("A value entered in this field will override the value entered in the")
            PSSHLP.append("DOSING CHECK FREQUENCY field for the selected drug.")
        print("\n".join(PSSHLP))

def ENMEDI():
    if X == '??':
        PSSHLP = []
        PSSHLP.append("This field allows a dispense drug from the DRUG (#50) file to be")
        PSSHLP.append("associated with the DOSING CHECK FREQUENCY (#32) field value within the")
        PSSHLP.append("MEDICATION INSTRUCTION (#51) file.")
        if 'PSJPP' in globals() and PSJPP != '':
            PSSHLP.append("A value entered in this field will override the value entered in the")
            PSSHLP.append("DOSING CHECK FREQUENCY field for the selected drug.")
        print("\n".join(PSSHLP))

def ENADMSCH():
    if X == '??':
        PSSHLP = []
        PSSHLP.append("This field allows a dispense drug from the DRUG (#50) file to be")
        PSSHLP.append("associated with the DOSING CHECK FREQUENCY (#11.1) field value within the")
        PSSHLP.append("ADMINISTRATION SCHEDULE (#51.1) file.")
        if 'PSJPP' in globals() and PSJPP != '':
            PSSHLP.append("A value entered in this field will override the value entered in the")
            PSSHLP.append("DOSING CHECK FREQUENCY field for the selected drug.")
        print("\n".join(PSSHLP))

def PSS13():
    if 'CAPTION' in globals() and CAPTION == 'CLINIC':
        if globals()['^PS(51.1,"AC","PSJ",X)'] or X[:len(globals()['$O(^PS(51.1,X))'])] == globals()['$O(^PS(51.1,X))']:
            return 1
        if X.find('@') != -1:
            return 2
        if Y <= 0:
            return 3

def PSS19():
    import sys
    sys.stdout.write(f"Delete DRUG GROUP/INTERACTION field #7\n")
    sys.stdout.flush()
    import sys
    sys.stdout.write(f"Delete \"I\" node if it is null.\n")
    sys.stdout.flush()
    for PSSIEN in range(0, len(globals()['^PSDRUG'])):
        if 'I' in globals()['^PSDRUG'][PSSIEN] and globals()['^PSDRUG'][PSSIEN]['I'] == '':
            del globals()['^PSDRUG'][PSSIEN]['I']

def ENMEDI():
    import sys
    sys.stdout.write(f"This field allows a dispense drug from the DRUG (#50) file to be\n")
    sys.stdout.write(f"associated with the DOSING CHECK FREQUENCY (#32) field value within the\n")
    sys.stdout.write(f"MEDICATION INSTRUCTION (#51) file.\n")
    sys.stdout.write(f"\n")
    sys.stdout.write(f"When a value is entered for \"DOSING CHECK FREQUENCY:\" and NO drug(s) is\n")
    sys.stdout.write(f"entered for \"Select DRUG(S) FOR DOSING CHK FREQ:\", the dosing check will\n")
    sys.stdout.write(f"use the value for \"DOSING CHECK FREQUENCY:\" to derive a frequency for\n")
    sys.stdout.write(f"all orders that have that medication instruction.\n")
    sys.stdout.write(f"\n")
    sys.stdout.write(f"When a value is entered for \"DOSING CHECK FREQUENCY:\" and a drug(s) is\n")
    sys.stdout.write(f"entered for \"Select DRUG(S) FOR DOSING CHK FREQ:\", the Daily Dose Order\n")
    sys.stdout.write(f"Check will ONLY use the value in \"DOSING CHECK FREQUENCY:\" to derive a\n")
    sys.stdout.write(f"frequency if the order that has that medication instruction also matches\n")
    sys.stdout.write(f"one of the drug(s) entered. If the drug found in the order does not\n")
    sys.stdout.write(f"match a drug listed in the DRUG(S) FOR DOSING CHK FREQ field, then the\n")
    sys.stdout.write(f"value of the DOSING CHECK FREQUENCY will not be used for the Daily Dose\n")
    sys.stdout.write(f"Order Check.\n")
    sys.stdout.write(f"\n")
    sys.stdout.flush()

def ENADMSCH():
    import sys
    sys.stdout.write(f"This field allows a dispense drug from the DRUG (#50) file to be\n")
    sys.stdout.write(f"associated with the DOSING CHECK FREQUENCY (#11.1) field value within the\n")
    sys.stdout.write(f"ADMINISTRATION SCHEDULE (#51.1) file.\n")
    sys.stdout.write(f"\n")
    sys.stdout.write(f"When a value is entered for \"DOSING CHECK FREQUENCY:\" and NO drug(s) is\n")
    sys.stdout.write(f"entered for \"Select DRUG(S) FOR DOSING CHK FREQ:\", the dosing check will\n")
    sys.stdout.write(f"use the value for \"DOSING CHECK FREQUENCY:\" to derive a frequency for\n")
    sys.stdout.write(f"all orders that have that schedule.\n")
    sys.stdout.write(f"\n")
    sys.stdout.write(f"When a value is entered for \"DOSING CHECK FREQUENCY:\" and a drug(s) is\n")
    sys.stdout.write(f"entered for \"Select DRUG(S) FOR DOSING CHK FREQ:\", the Daily Dose Order\n")
    sys.stdout.write(f"Check will ONLY use the value in \"DOSING CHECK FREQUENCY:\" to derive a\n")
    sys.stdout.write(f"frequency if the order that has that medication instruction also matches\n")
    sys.stdout.write(f"one of the drug(s) entered. If the drug found in the order does not\n")
    sys.stdout.write(f"match a drug listed in the DRUG(S) FOR DOSING CHK FREQ field, then the\n")
    sys.stdout.write(f"value of the DOSING CHECK FREQUENCY will not be used for the Daily Dose\n")
    sys.stdout.write(f"Order Check.\n")
    sys.stdout.write(f"\n")
    sys.stdout.flush()