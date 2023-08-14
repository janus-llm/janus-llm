def PSSPRUTL():
    # BIR/RTR-Edit IV Solution ;04/19/08
    # 1.0;PHARMACY DATA MANAGEMENT;**129**;9/30/07;Build 67

    def EDIT():
        # Edit IV Solution
        X, Y, DIR, DTOUT, DUOUT, DIRUT, DIROUT, DIC, DA, DR, DLAYGO, DIDEL, PSSEDSDA, PSSEDSXX, PSSEDSZZ, PSSEDSDR, PSSEDSGG, PSSEDSAR, DRUGEDIT = (
            None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None
        )
        # Newing D in next line because FileMan is leaving it defined to a zero node upon option exit
        %, %DT, D0, I, J, MSG, PSJCLEAR, PSPOINT, PSSIVID, SYNIEN, XX, PSSCROSS, D = (
            None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None
        )

        if not '^XUSEC("PSJI MGR", DUZ) in globals()':
            print("\nSorry, you need the 'PSJI MGR' key to access this option.\n")
            MESS()
            return

        if not L + ^PS(52.7):
            print("\nSorry, someone else is editing entries in the IV SOLUTIONS (#52.7) File.\n")
            MESS()
            return

        EDITM()

    def EDITM():
        X, Y, DIR, DTOUT, DUOUT, DIRUT, DIROUT, DIC, DA, DR, DLAYGO, DIDEL, %, %DT, D0, I, J, MSG, PSJCLEAR, PSPOINT, PSSIVID, SYNIEN, XX, PSSCROSS, D = (
            None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None
        )
        # Setting DRUGEDIT in next line because cross reference on GENERIC DRUG #1 Field of IV SOLUTION (#52.7) File needs it defined
        PSSEDSDA, PSSEDSXX, PSSEDSZZ, PSSEDSDR, PSSEDSGG, PSSEDSAR = None, None, None, None, None, None
        DRUGEDIT = 1

        print()
        DIC, X, DTOUT, DUOUT = "^PS(52.7,", None, None, None
        DIC(0) = "AEQMZ"
        ^DIC, DIC, X = None, None, None
        if Y < 0 or DUOUT or DTOUT:
            UN()
            return

        PSSEDSDA = +Y
        PSSEDSXX = $P($G(^PS(52.7, PSSEDSDA, 0)), "^", 11)

        DIE, DA, DR = "^PS(52.7,", PSSEDSDA, ".01;.02;1;D GETD^PSSPRUTL;2;8;17;18"
        ^DIE
        DIE, DA, DR = None, None, None

        # Change the Generic Drug could automatically change the Orderable Item of the IV Solution
        # Now doing what MSF^PSSDFEE does, updating Orderable Items, though cross reference on 52.,7,1 should have already done it
        # Just as a safeguard, we'll look to update all Orderable Items again, note that PSSEDSZZ and PSSEDSGG should never be different
        PSSEDSZZ = $P($G(^PS(52.7, PSSEDSDA, 0)), "^", 11)
        PSSEDSDR = $P($G(^PS(52.7, PSSEDSDA, 0)), "^", 2)
        PSSEDSGG = $P($G(^PSDRUG(+PSSEDSDR, 2)), "^")

        if PSSEDSZZ:
            PSSCROSS = None
            EN^PSSPOIDT(PSSEDSZZ)
            EN2^PSSHL1(PSSEDSZZ, "MUP")

        if PSSEDSGG and PSSEDSGG != PSSEDSZZ:
            PSSCROSS = None
            EN^PSSPOIDT(PSSEDSGG)
            EN2^PSSHL1(PSSEDSGG, "MUP")

        print()
        EDITM()

    def UN():
        # Unlock File
        L - ^PS(52.7)

    def GETD():
        # See if generic drug is inactive in file 50, code cloned from line tag GETD Of routine PSSVIDRG
        if $D(^PSDRUG(X, "I")) and ^("I") and (DT + 1 > +^("I")):
            print("\a\a\nThis drug is inactive and will not be selectable during IV order entry.\n")
            $P(^PS(52.7, PSSEDSDA, "I"), "^") = $P(^PSDRUG(X, "I"), "^")

    def MESS():
        print()
        DIR(0) = "E"
        DIR("A") = "Press Return to Continue"
        ^DIR
        DIR = None

    EDIT()
    return

PSSPRUTL()