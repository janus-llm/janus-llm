def PSSMRRDG():
    """
    BIRMINGHAM/GN/DRP-Diagnostic Report only, does not update
    9/25/15 10:03am
    """
    pass


def EN(P1):
    """
    Check for MRR meds missing the 2.1 node which is new and would be
    there if an order was created and Finished after patch PSJ*3*315
    Input param: P1 = default is null and checks for 2.1 node
                       = if pass in a value, then it will not check 2.1
    """
    print()
    # Assigning values to %ZIS and IOP
    %ZIS = {"B": ""}
    IOP = None
    ZTSK = None
    %ZIS["B"] = ""
    %ZIS = "QM"
    ^%ZIS()
    if POP:
        return
    if IOST[0:2] == "C-":
        print(chr(7), "\n", "It is recommended to Queue this report to a printer for Large sites, enter Q at Device prompt", "\n")
    if not IO["Q"]:
        TERM = 1 if IOST[0:2] == "C-" else 0
        MAIN()
        ^%ZISC()
    ZTRTN = MAIN
    ZTDESC = "Orders for MRRs With Removal Properties"
    ^%ZTLOAD()
    IO["Q"] = None


def MAIN():
    """
    main control
    """
    DFN = None
    MRR = None
    MRRAR = None
    ORD = None
    STP = None
    ORDTOT = None
    DDOI = None
    DDTXT = None
    QQ = None
    YY = None
    STS = None
    PSSID = None
    PSSLOC = None
    PSSQ = None
    PSSPATCH = None
    ORDSDT = None
    CLNODE = None
    LIN = None
    MRRFL = None
    OI = None
    PAGNO = None
    POP = None
    $ESTACK = None
    $ETRAP = "D ERRTRP^PSSMRRDG"
    P1 = P1 if P1 is not None else ""
    PSSPATCH = 1 if P2 else 1 if not $$PATCH^XPDUTL("PSJ*5.0*315") else 0
    # build array of OI's that are mrr and their flag value
    QQ = 0
    while True:
        QQ = $O(^PSDRUG("ASP", QQ))
        if not QQ:
            break
        YY = 0
        while True:
            YY = $O(^PSDRUG("ASP", QQ, YY))
            if not YY:
                break
            OI = $P(^PSDRUG(YY, 2), U)
            MRRFL = $P($G(^PS(50.7, OI, 4)), U, 1)
            if MRRFL:
                MRRAR(OI) = MRRFL
    # Use Ord Stop Date XREF to look for current orders
    ORDTOT = 0
    PSSQ = 0
    PAGNO = 0
    ORDSDT = DT
    while True:
        ORDSDT = $O(^PS(55, "AUD", ORDSDT))
        if not ORDSDT:
            break
        DFN = 0
        while True:
            DFN = $O(^PS(55, "AUD", ORDSDT, DFN))
            if not DFN:
                break
            ORD = 0
            while True:
                ORD = $O(^PS(55, "AUD", ORDSDT, DFN, ORD))
                if not ORD:
                    break
                STS = $P($G(^PS(55, DFN, 5, ORD, 0)), U, 9)
                CLNODE = $G(^PS(55, DFN, 5, ORD, 8), 0)
                # non Active type order, quit dont include
                if STS in ["D", "E", "DE", "DR"]:
                    continue
                PSSID = "NONE" if not $D(^DPT(DFN, 0)) else $E($P($G(^DPT(DFN, 0)), U, 1), 1) + $E($P($G(^DPT(DFN, 0)), U, 9), 6, 9)
                CHKORD()  # check and then set ^TMP for sort
    if $D(^TMP("PSSMRRDG")):
        PRINT()
    if ORDTOT == 0:
        HDR()
    if not PSSQ:
        print("\n", "Total Orders found: ", ORDTOT, "\n")
    print("\n", "Press RETURN to continue.....")
    X = input()
    ^TMP("PSSMRRDG") = None


def CHKORD():
    """
    check if Order qualifies and then print on report
    return mrrfl which is positive or true  (1,2,3)
    """
    QQ = 0
    while True:
        QQ = $O(^PS(55, DFN, 5, ORD, 1, QQ))
        if not QQ:
            break
        DDOI = +$P($G(^PS(55, DFN, 5, ORD, .2)), U)
        MRR = $G(MRRAR(DDOI))
        if not MRR:  # don't report not a MRR med
            continue
        # don't report if has a 2.1 node, unless P1 overrides
        if not P1 and $D(^PS(55, DFN, 5, ORD, 2.1)):
            continue
        PSSLOC = $P(^SC(+^PS(55, DFN, 5, ORD, 8), 0), U, 1) if $$CLINIC(CLNODE) else $G(^DPT(DFN, .1)) if $G(^DPT(DFN, .1)) else "UNKNOWN"
        DDTXT = $$GET1^DIQ(55.07, QQ_","_ORD_","_DFN, "DISPENSE DRUG")
        ^TMP("PSSMRRDG", PSSLOC, PSSID) = DDTXT_U_STS_U_MRR


def PRINT():
    """
    Print the report
    """
    PSSLOC = ""
    while True:
        PSSLOC = $O(^TMP("PSSMRRDG", PSSLOC))
        if not PSSLOC or PSSQ:
            break
        HDR()
        PSSID = ""
        while True:
            PSSID = $O(^TMP("PSSMRRDG", PSSLOC, PSSID))
            if not PSSID or PSSQ:
                break
            STR = ^TMP("PSSMRRDG", PSSLOC, PSSID)
            DDTXT = $P(STR, U)
            STS = $P(STR, U, 2)
            MRR = $P(STR, U, 3)
            WRITELN()
            ORDTOT = ORDTOT + 1
            if $Y > (IOSL - 1):
                PAUSE()
        PAUSE()


def HDR():
    """
    Write a heading on report
    """
    PAGNO = PAGNO + 1
    print("@IOF")
    print("\n", $E($$FMTE^XLFDT($$NOW^XLFDT), 1, 18), "?", 125, "Page ", PAGNO)
    if not PSSPATCH:
        H1()
        BODY()
    else:
        H2()
        BODY()


def H1():
    """
    Heading for Pre-PSJ315 install
    """
    print("\n", " "*2, "The following ACTIVE Orders are for Medications Requiring Removal (MRR). Prior to Installation of PSJ*5*315 these orders")
    print(" "*2, "should be reviewed for planning purposes, but no action taken. Once PSJ*5*315 is installed they will need to be d/c'd and")
    print(" "*2, "re-entered after coordinating with your ADPAC.")


def H2():
    """
    Heading for Post-PSJ315 install
    """
    print("\n", " "*2, "The following ACTIVE orders for medications that Require Removal (MRR) were finished prior to install of Patch PSJ*5*315.")
    print(" "*2, "These orders must be re-entered. They may not be copied, renewed or edited to create new orders.")
    print(" "*2, "Any changes to these orders should be coordinated with your ADPAC.")


def BODY():
    """
    Write the body of the report
    """
    print("\n"*2, " "*50, " Sort by Patient within Ward  ", $G(PSSLOC, "NONE FOUND"))
    print("\n", "Patient", " "*10, "Patient", " "*20, "Orderable", " "*45, "Ordr", " "*50, "MRR")
    print("ID", " "*10, "Loc", " "*20, "Item Name", " "*45, "Sts", " "*50, "Val")
    LIN = "-"*132
    print("\n", LIN)


def WRITELN():
    """
    Write line on report
    """
    print("\n", PSSID, " "*10, PSSLOC, " "*20, DDTXT, " "*45, STS, " "*50, MRR)


def PAUSE():
    """
    Pause the report
    """
    if not TERM:
        return
    print("\n", "Press RETURN to continue, '^' to exit")
    X = input()
    if X == "^" or not X:
        PSSQ = 1
    IO = None


def CLINIC(CL):
    """
    Is this a Clinic order that would show on the VDL in CO mode also?
    """
    if not ($P(CL, "^", 2).isnumeric() and ($P(CL, "^", 2).isnumeric() or $P(CL, "^", 2) == 7N1"."N)):
        return 0  # no appt date, IM ord
    if not $D(^PS(53.46, "B", +CL)):
        return 0  # no PTR to 44, IM ord
    A = $O(^PS(53.46, "B", +CL, ""))
    if not A:
        return 0  # no 53.46 ien, IM ord
    return $P(^PS(53.46, A, 0), "^", 4)  # Send to BCMA? flag


def TST(P2):
    P2 = P2 if P2 is not None else None
    P1 = 1
    EN(P1)


def ERRTRP():
    Z = []  # mumps error location and description
    Z[0][0] = $$EC^%ZOSV()
    Z = "A SYSTEM ERROR HAS BEEN DETECTED AT THE FOLLOWING LOCATION"
    PROBLEM = 7
    ^%ZTER()
    UNWIND^%ZTER()


PSSMRRDG()