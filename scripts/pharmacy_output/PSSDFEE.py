def PSSDFEE():
    # BIR/ASJ-VARIOUS FILES ENTER EDIT ROUTINE ;01/21/00
    # 1.0;PHARMACY DATA MANAGEMENT;**38,48,125,129**;9/30/97;Build 67
    DF()  # Dosage File Enter/Edit
    MR()  # Medication Routes File Enter/Edit
    CF()  # Rx Consult File


def DF():
    # Dosage File Enter/Edit
    PSSDEE2()
    DIC, PSSDF, DLAYGO, PSSREC, X, Y, D, %, %X, %Y, DIE, DA, DR, DIR, DTOUT, DUOUT, DIROUT, DIRUT, D0 = (
        None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None
    )
    
    while True:
        print()
        DIC(0) = "QEAMZ"
        DIC = "^PS(50.606,"
        DIC("S") = "I '$P(^(0),""^"",2)!($P(^(0),""^"",2)>DT)"
        Y = DIC()
        PSSREC = +Y
        if PSSREC < 0:
            break
        print()
        print("NAME: ", Y(0,0))
        EDT(DIC, PSSREC, "[PSS DOSAGE FORM]", 50.606)
    print()


def MR():
    # Medication Routes File Enter/Edit
    PSSDEE2()
    DIC, PSSDF, DLAYGO, PSSDMRA, PSSREC, X, Y, D, %, %X, %Y, PSSDMRQT, DIE, DA, DR, DIR, DTOUT, DUOUT, DIROUT, DIRUT, PSSDMREN, D0 = (
        None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None
    )
    
    PSSDMRQT = 0
    while not PSSDMRQT:
        print()
        DIC(0) = "QEAMZIL"
        DIC = "^PS(51.2,"
        DLAYGO = 51.2
        Y = DIC()
        if Y < 0:
            break
        PSSREC = +Y
        PSSDMREN = PSSREC
        PSSDMRA = $P($G(^PS(51.2,PSSREC,1)),"^")
        EDT(DIC, PSSREC, "[PSS MEDICATION ROUTES]", 51.2)
    print()


def CF():
    # Rx Consult File
    # It was decided not to put this functionality in PSS*1*38
    PSSDEE2()
    DIC, PSSDF, DLAYGO = None, None, None
    
    while True:
        print()
        DIC(0) = "QEAMZIL"
        DIC = "^PS(54,"
        DLAYGO = 54
        Y = DIC()
        if Y < 0:
            break
        PSSREC = +Y
        EDT(DIC, PSSREC, "[PSS RX CONSULT]", 54)
    print()


def EDT(DIE,DA,DR,PSFILE):
    PSREC = DA
    L + ^PS(PSFILE,PSREC) : $S($G(DILOCKTM) > 0:DILOCKTM, 1:3)
    
    if not $T:
        print()
        print($C(7), "Another person is editing this entry.")
        return
    
    DTOUT = None
    DIE()
    
    if PSFILE == 51.2 and (Y or DTOUT):
        if not $P($G(^PS(51.2,PSSDMREN,1)),"^") and $P($G(^PS(51.2,PSSDMREN,0)),"^",4):
            MESS()
        L - ^PS(PSFILE,PSREC)
        return
    
    DIE, DR, DA, Y = None, None, None, None
    
    if PSFILE == 51.2:
        STN()
    
    L - ^PS(PSFILE,PSREC)


def STN():
    PSSDMRX, PSSDMRNW, PSSDMRFL = None, None, None
    
    if not $P($G(^PS(51.2,PSSDMREN,0)),"^",4):
        return
    
    if PSSDMRA:
        PSSDMRX = 0
        if PSSDMRQT:
            if PSSDMRX:
                if PSSDMRQT:
                    print()
                    print("Mapping Remains Unchanged.")
                    DIR(0) = "E"
                    DIR("A") = "Press Return to continue, '^' to exit"
                    DIR()
                    if DTOUT or DUOUT:
                        PSSDMRQT = 1
                    return
    
    DA = PSSDMREN
    DIE = "^PS(51.2,"
    DR = 10
    DIE()
    
    if Y or DTOUT:
        if not $P($G(^PS(51.2,PSSDMREN,1)),"^"):
            MESSA()
        DIR(0) = "E"
        DIR("A") = "Press Return to continue, '^' to exit"
        DIR()
        if DTOUT or DUOUT:
            PSSDMRQT = 1


def MESS():
    print()
    print("*** No dosing checks will be performed on orders containing this local")
    print("  medication route until it is mapped to a standard medication route.***")
    DIR(0) = "E"
    DIR("A") = "Press Return to continue, '^' to exit"
    DIR()


def MESSA():
    print()
    print("*** No dosing checks will be performed on orders containing this local")
    print("  medication route until it is mapped to a standard medication route.***")