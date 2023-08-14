def PSSMARK():
    U = "^"
    PSXFL = 0
    TEXT()
    PSXMM = 1
    while True:
        PICK1()
        if not PSXFL:
            PSXFL = 0
        if PSXFL:
            break
    DONE()
    PSXBT = 1
    PSXF = 1
    PICK()
    PSXFL = 1
    PICK2()

def TEXT():
    print("\nThis option allows you to choose entries from your drug file and helps you")
    print("review your NDF matches and mark individual entries to send to CMOP.")
    print("\nIf you mark the entry to transmit to CMOP, it will replace your Dispense Unit")
    print("with the VA Dispense Unit. In addition, you may overwrite the local drug name")
    print("with the VA Print Name and the entry will remain uneditable.")

def DISPLAY():
    print("\nLocal Drug Generic Name: ", PSXLOC)
    print("\nORDER UNIT: ", end="")
    if '660' in PSXODE:
        PSXOU = PSXODE.split('^')[1]
        if '51.5' in globals() and PSXOU in globals()['51.5']:
            print(globals()['51.5'][PSXOU].split('^')[0])
    print("\nDISPENSE UNITS/ORDER UNITS: ", PSXODE.split('^')[5])
    print("\nDISPENSE UNIT: ", PSXODE.split('^')[8])
    print("\nPRICE PER DISPENSE UNIT: ", PSXODE.split('^')[6])
    print("\nVA Print Name: ", PSXVAP, end="")
    print("\nVA Dispense Unit: ", PSXDP)
    print("\nVA Drug Class: ", globals()['50.605'][PSXDN.split('^')[6]].split('^')[0])
    print("\nCMOP ID: ", PSXID)
    CPDATE, X, PSNCP = None, None, None
    X = CPDATE
    X = globals()['CPTIER^PSNAPIS']("", CPDATE, PSXUM)
    print("\nCOPAY Tier: ", X.split('^')[0])
    CHECK()

def CHECK():
    if 'AQ' in globals()['PSDRUG'] and PSXUM in globals()['PSDRUG']['AQ']:
        if globals()['PSDRUG'][PSXUM][3] == 1:
            UNMARK()
    if PSXBT == 1:
        return
    if PSXUM not in globals()['PSDRUG']['AQ']:
        MARK()

def MARK():
    print("\nDo you wish to mark this drug to transmit to CMOP? ", end="")
    if input().upper() == 'Y':
        globals()['PSDRUG'][PSXUM][660][8] = PSXDP
        globals()['PSDRUG'][PSXUM][3] = 1
        globals()['PSDRUG']['AQ'][PSXUM] = ""
        globals()['PSSREF']()
        IDENT()
        globals()['QDM']()
        QUEST()
        QUES2()

def UNMARK():
    print("\nDo you wish to UNmark this drug to transmit to CMOP? ", end="")
    if input().upper() == 'Y':
        globals()['PSDRUG'][PSXUM][3] = 0
        del globals()['PSDRUG']['AQ'][PSXUM]
        globals()['PSSREF']()

def QUES2():
    print("\nDo you wish to overwrite your local name? ", end="")
    if input().upper() == 'Y':
        DUP()
        if PSXVAP not in globals()['PSDRUG']['B']:
            globals()['PSDRUG'][PSXUM][0] = PSXVAP
            XREF()
            OLDNM()

def DUP():
    if PSXVAP != PSXLOC and PSXVAP in globals()['PSDRUG']['B']:
        print("\nYou cannot write over the GENERIC NAME because one already has that")
        print("VA Print Name. You cannot have duplicate names.")

def XREF():
    if PSXLOC != PSXVAP:
        del globals()['PSDRUG']['B'][PSXLOC][PSXUM]
        globals()['PSDRUG']['B'][PSXVAP][PSXUM] = ""
    if PSXUM in globals()['PSNTRAN']['END']:
        globals()['PSNTRAN'][PSXUM]['END'][2] = PSXVAP
        globals()['PSNTRAN']['END'][2] = PSXVAP

def BLD():
    if PSXUM in globals()['PSDRUG'] and globals()['PSDRUG'][PSXUM]['I']:
        X1 = globals()['PSDRUG'][PSXUM]['I']
        X2 = globals()['DT']
        X = X2 - X1
        if X < 1:
            PSSEXP[1] = "It has been inactivated."
    if PSXUM in globals()['PSDRUG'] and '2' in globals()['PSDRUG'][PSXUM][2] and 'O' not in globals()['PSDRUG'][PSXUM][2][3]:
        PSSEXP[2] = "It is not marked for outpatient pharmacy use."
    if '1' in globals()['PSDRUG'][PSXUM][0][3] or '2' in globals()['PSDRUG'][PSXUM][0][3]:
        PSSEXP[3] = "It is a schedule I or schedule II controlled substance."
    if PSXUM not in globals()['PSDRUG']['ND']:
        PSSEXP[4] = "It is not matched to NDF."
    if PSXUM in globals()['PSDRUG'] and globals()['PSDRUG'][PSXUM]['ND'][2] == "":
        PSSEXP[5] = "It is not matched to NDF."
    if PSXUM in globals()['PSDRUG'] and globals()['PSDRUG'][PSXUM]['ND'] and globals()['PSDRUG'][PSXUM]['ND'][1] == 1:
        PSXDN = globals()['PSDRUG'][PSXUM]['ND']
        PSXGN = PSXDN[0]
        PSXVP = PSXDN[2]
        PSSXX = globals()['PROD2^PSNAPIS'](PSXGN, PSXVP)
        if PSSXX[2] != 1:
            PSSEXP[6] = "It is not marked for CMOP in NDF."
        if not PSSEXP:
            PSXVAP = PSSXX[0]
            PSXDP = PSSXX[3]

def PICK1():
    globals()['DIC'] = globals()['PSDRUG']
    globals()['DIC'][0] = "QEAM"
    Y = globals()['DIC'][globals()['PSDRUG']][PSXUM]
    if Y < 0:
        PSXFL = 1
    else:
        PSSEXP = {}
        PSXUM = Y
        PSXLOC = Y[1]
        PSSEXP[0] = ""
        PSXF = 0
        PSXBT = 0
        BLD()

def IDENT():
    PSXNDF = globals()['PSDRUG'][PSXUM]['ND'][0]
    PSXVAPN = globals()['PSDRUG'][PSXUM]['ND'][2]
    DA = PSXNDF
    K = PSXVAPN
    X = globals()['PROD2^PSNAPIS'](DA, K)
    PSXIDENT = X[1]
    globals()['PSDRUG'][PSXUM]['ND'][10] = PSXIDENT
    globals()['PSDRUG']['AQ1'][PSXIDENT][PSXUM] = ""

def QUEST():
    if globals()['PSDRUG'][PSXUM][660][8] != PSXDP:
        print("\nYour old Dispense Unit  ", globals()['PSDRUG'][PSXUM][660][8], "  does not match the new one  ", PSXDP, ".")
        print("You may wish to edit the Price Per Order Unit and/or The Dispense")
        print("Units Per Order Unit.")

def QUES2():
    print("\nDo you wish to overwrite your local name? ", end="")
    if input().upper() == 'Y':
        DUP()
        if PSXVAP not in globals()['PSDRUG']['B']:
            globals()['PSDRUG'][PSXUM][0] = PSXVAP
            XREF()
            OLDNM()

def OLDNM():
    OLD()
    if NONCE:
        OLD1()

def OLD():
    X = globals()['NOW^%DTC']()
    if globals()['PSDRUG'][PSXUM][900][1]:
        NONCE = 0
        PSXLAST = 0
        RTC = 0
        while True:
            RTC += 1
            PSXLAST += 1
            PSXNEXT = PSXLAST + 1
            if RTC not in globals()['PSDRUG'][PSXUM][900]:
                break
    if not globals()['PSDRUG'][PSXUM][900][1]:
        globals()['PSDRUG'][PSXUM][900][1] = []
        globals()['PSDRUG'][PSXUM][900][1][0] = PSXLOC + "^" + X

def OLD1():
    if not NONCE:
        globals()['PSDRUG'][PSXUM][900][PSXNEXT][0] = PSXLOC + "^" + X
        NONCE = 1

def SYN():
    if PSXUM in globals()['PSDRUG'] and not globals()['PSDRUG'][PSXUM][1]:
        globals()['PSDRUG'][PSXUM][1][0] = "^50.1A^0^0"
    if PSXVAP not in globals()['PSDRUG']['C'][PSXUM]:
        PSXNOW = globals()['PSDRUG'][PSXUM][1][0][3] + 1
        globals()['PSDRUG'][PSXUM][1][PSXNOW][0] = PSXVAP
        globals()['PSDRUG']['C'][PSXVAP][PSXUM][PSXNOW] = ""
        globals()['PSDRUG'][PSXUM][1][0][3] = PSXNOW
        globals()['PSDRUG'][PSXUM][1][0][4] += 1

def QDM():
    globals()['DIE'] = globals()['PSDRUG']
    DA = PSXUM
    DR = 215
    globals()['DIE'][DA][DR] = ""

PSSMARK()