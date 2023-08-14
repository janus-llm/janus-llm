def ZERO(PSSIEN, PSSFT, PSSPP, PSSTSCH, LIST):
    """
    PSSIEN - IEN of entry in ADMINISTRATION SCHEDULE file (#51.1).
    PSSFT - Free Text name in ADMINISTRATION SCHEDULE file (#51.1).
    PSSPP - PACKAGE PREFIX field (#4) in ADMINISTRATION SCHEDULE file (#51.1). Screens for Administration
    Schedules for the Package Prefix passed.
    PSSTSCH - TYPE OF SCHEDULE field (#5) of ADMINISTRATION SCHEDULE file (#51.1). Screens for
              One-time "O" if PSSTSCH passed in.
    LIST - Subscript of ^TMP array in the form ^TMP($J,LIST,Field Number where Field Number is the
           Field Number of the data piece being returned.
    Returns NAME field (#.01), STANDARD ADMINISTRATION TIMES field (#1), FREQUENCY (IN MINUTES) field (#2),
    MAXIMUM DAYS FOR ORDERS field (#2.5), PACKAGE PREFIX field (#4), TYPE OF SCHEDULE field (#5),
    STANDARD SHIFTS field (#6), OUTPATIENT EXPANSION field (#8), and OTHER LANGUAGE EXPANSIONS field (#8.1)
    of ADMINISTRATION SCHEDULE file (#51.1).
    """
    # Python code here

def WARD(PSSIEN, PSSFT, PSSIEN2, LIST):
    """
    PSSIEN - IEN of entry in ADMINISTRATION SCHEDULE file (#51.1).
    PSSFT - Free Text name in ADMINISTRATION SCHEDULE file (#51.1).
    PSSIEN2 - IEN of entry in WARD sub-file (#51.11)
    LIST - Subscript of ^TMP array in the form ^TMP($J,LIST,Field Number where Field Number is the
           Field Number of the data piece being returned.
    Returns NAME field (#.01), WARD multiple (#51.11) WARD field (#.01), and WARD ADMINISTRATION TIMES field (#1)
    of ADMINISTRATION SCHEDULE file (#51.1).
    """
    # Python code here

def HOSP(PSSIEN, PSSFT, LIST):
    """
    PSSIEN - IEN of entry in ADMINISTRATION SCHEDULE file (#51.1).
    PSSFT - Free Text name in ADMINISTRATION SCHEDULE file (#51.1).
    LIST - Subscript of ^TMP array in the form ^TMP($J,LIST,Field Number where Field Number is the
           Field Number of the data piece being returned.
    Returns NAME field (#.01), HOSPITAL LOCATION multiple (#51.17) HOSPITAL LOCATION field (#.01), ADMINISTRATION TIMES field (#1),
    and SHIFTS field (#2) of ADMINISTRATION SCHEDULE file (#51.1).
    """
    # Python code here

def IEN(PSSFT, LIST):
    """
    PSSFT - Free Text name in ADMINISTRATION SCHEDULE file (#51.1).
    LIST - Subscript of ^TMP array in the form ^TMP($J,LIST,Field Number where Field Number is the
           Field Number of the data piece being returned.
    Returns NAME field (#.01) and STANDARD ADMINISTRATION TIMES field (#1) of ADMINISTRATION SCHEDULE file (#51.1).
    """
    # Python code here

def AP(PSSPP, PSSFT, PSSWDIEN, PSSTYP, LIST, PSSFREQ):
    """
    PSSPP - PACKAGE PREFIX in ADMINISTRATION SCHEDULE file (#51.1).
    PSSFT - Free Text name in ADMINISTRATION SCHEDULE file (#51.1).
    PSSWDIEN - IEN of entry of WARD multiple in ADMINISTRATION SCHEDULE file (#51.1).
    PSSSTYP - TYPE OF SCHEDULE field (#5) in ADMINISTRATION SCHEDULE file (#51.1).
    LIST - Subscript of ^TMP array in the form ^TMP($J,LIST,Field Number where Field Number is the
           Field Number of the data piece being returned.
    Returns NAME field (#.01), STANDARD ADMINISTRATION TIMES field (#1), and PACKAGE PREFIX field (#4)
    of ADMINISTRATION SCHEDULE file (#51.1).
    If PSSWDIEN is passed in then the WARD multiple (#51.11) WARD field (#.01), and WARD ADMINISTRATION TIMES field (#1)
    of ADMINISTRATION SCHEDULE file (#51.1) is returned.
    """
    # Python code here

def IX(PSSFT, PSSPP, LIST):
    """
    PSSFT - Free Text name in ADMINISTRATION SCHEDULE file (#51.1).
    PSSPP - PACKAGE PREFIX in ADMINISTRATION SCHEDULE file (#51.1).
    LIST - Subscript of ^TMP array in the form ^TMP($J,LIST,Field Number where Field Number is the
           Field Number of the data piece being returned.
    Returns NAME field (#.01), STANDARD ADMINISTRATION TIMES field (#1), FREQUENCY (IN MINUTES) field (#2),
    MAXIMUM DAYS FOR ORDERS field (#2.5),PACKAGE PREFIX field (#4), TYPE OF SCHEDULE field (#5), STANDARD
    SHIFTS field (#6), OUTPATIENT EXPANSION field (#8), and OTHER LANGUAGE EXPANSION field (#8.1) of
    ADMINISTRATION SCHEDULE file (#51.1).
    """
    # Python code here

def ADM(PSSADM):
    """
    PSSADM - admin times
    """
    # Python code here

def ALL(PSSIEN, PSSFT, LIST):
    """
    PSSIEN - IEN of entry in ADMINISTRATION SCHEDULE file (#51.1).
    PSSFT - Free Text name in ADMINISTRATION SCHEDULE file (#51.1).
    LIST - Subscript of ^TMP array in the form ^TMP($J,LIST,Field Number where Field Number is the
           Field Number of the data piece being returned.
    Returns NAME field (#.01), STANDARD ADMINISTRATION TIMES field (#1), FREQUENCY (IN MINUTES) field (#2),
    MAXIMUM DAYS FOR ORDERS field (#2.5), PACKAGE PREFIX field (#4), TYPE OF SCHEDULE field (#5),
    STANDARD SHIFTS field (#6), OUTPATIENT EXPANSION field (#8), OTHER LANGUAGE EXPANSIONS field (#8.1),
    HOSPITAL LOCATION multiple (#51.17) HOSPITAL LOCATION field (#.01), ADMINISTRATION TIMES field (#1),
    SHIFTS field (#2), WARD multiple (#51.11) WARD field (#.01), and WARD ADMINISTRATION TIMES field (#1)
    of ADMINISTRATION SCHEDULE file (#51.1).
    """
    # Python code here

def SETSCR():
    # Python code here

def FREQ(PSSVAL, PSSFREQ):
    """
    VALIDATES FREQUNCY FIELD
    """
    # Python code here

def PSSDQ():
    # Python code here

def SCHED(PSSWIEN, PSSARRY):
    """
    PSSWIEN - 
    PSSARRY - 
    """
    # Python code here