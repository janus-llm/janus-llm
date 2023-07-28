def PSSHLSCH():
    """
    BIR/RLW/MV-BUILD HL7 MESSAGE TO POPULATE ADMIN. SCHEDULE FILE ; 09/02/97 8:38
    1.0;PHARMACY DATA MANAGEMENT;;9/30/97
    PSJEC=event code from HL7 table 8.4.2.1
    PSJIEN=ien to Administration Schedule file (#51.1)
    SPDNAME=.01 field (name) of super-primary drug
    DDIEN=ien to drug file (#50)
    LIMIT=number of fields in HL7 segment being built
    """

    def EN1():
        """
        start here for pre-install auto load
        """
        return

    def EN2():
        """
        start here for "manual" update
        """
        return

    def INIT():
        """
        initialize HL7 variables, set master file identification segment fields
        """
        nonlocal PSJI, LIMIT, HLMTN, PSJCLEAR
        PSJI = 0
        LIMIT = 6
        HLMTN = "MFN"
        INIT^PSSHLU()
        PSJCLEAR()

        FIELD[0] = "MFI"
        FIELD[1] = "^^^51.1^ADMINSTRATION SCHEDULE FILE"
        FIELD[3] = CODE
        FIELD[6] = "NE"
        SEGMENT(LIMIT)

    def LOOP():
        """
        loop through SCHEDULE file
        """
        nonlocal PSJIEN
        PSJIEN = 0
        while PSJIEN:
            MFE()

    def MFE():
        """
        set master file entry segment fields
        """
        nonlocal LIMIT
        LIMIT = 4
        PSJCLEAR()

        X = ^PS(51.1, PSJIEN, 0)
        FIELD[0] = "MFE"
        FIELD[1] = PSJEC
        FIELD[4] = "^^^" + PSJIEN + "^" + $P(X,"^") + "~" + $P(X,"^",4) + "^99PSS"
        SEGMENT(LIMIT)

    # We no longer send schedules to OERR
    APPL = None
    CODE = "REP"
    INIT()
    LOOP()
    SCH^PSSHLU(PSJI)
    del PSJEC, PSJIEN, PSJCLEAR

    # We no longer send schedules to OERR
    del ^TMP("HLS",$J)
    CODE = "UPD"
    INIT()
    PSJIEN = 0
    while PSJIEN:
        PSJEC = PSJHLDA(PSJIEN)
        MFE()
        CALL^PSSHLU(PSJI)
    del PSJEC, PSJIEN, PSJHLDA

PSSHLSCH()