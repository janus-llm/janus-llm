def ZERO(PSSIEN,PSSFT,PSSFL,LIST):
    """
    PSSIEN - IEN of entry in IV ADDITIVES file (#52.6).
    PSSFT - Free Text name in IV ADDITIVES file (#52.6).
    PSSFL - Inactive flag - "" - All entries.
            FileMan Date - Only entries with no Inactive Date or an Inactive Date greater than this date.
    LIST - Subscript of ^TMP array in the form ^TMP($J,LIST,Field Number where Field Number is the
           Field Number of the data piece being returned.
    """
    # Returns PRINT NAME field (#.01), GENERIC DRUG field (#1), DRUG UNIT field (#2),
    # NUMBER OF DAYS FOR IV ORDER field (#3), USUAL IV SCHEDULE field (#4), ADMINISTRATION TIMES field (#5),
    # AVERAGE DRUG COST PER UNIT field (#7), INACTIVATION DATE field (#12), CONCENTRATION field (#13),
    # MESSAGES field (#14), PHARMACY ORDERABLE ITEM field (#15), and USED IN IV FLUID ORDER ENTRY FIELD (#17)
    # of IV ADDITIVES file (#52.6).
    pass

def QCODE(PSSIEN,PSSFT,PSSFL,LIST):
    """
    PSSIEN - IEN of entry in IV ADDITIVES file (#52.6).
    PSSFT - Free Text name in IV ADDITIVES file (#52.6).
    PSSFL - Inactive flag - 0 or "" - All entries.
            FileMan Date - Only entries with no Inactive Date or an Inactive Date greater than this date.
    LIST - Subscript of ^TMP array in the form ^TMP($J,LIST,Field Number where Field Number is the
           Field Number of the data piece being returned.
    """
    # Returns PRINT NAME field (#.01), QUICK CODE subfile (#52.61), QUICK CODE field (#.01), STRENGTH field (#1),
    # USUAL INFUSION RATE field (#2), OTHER PRINT INFO field (#3), USUAL IV SCHEDULE field (#4), ADMINISTRATION TIMES
    # field (#5), USUAL IV SOLUTION field (#6), and MED ROUTE field (#7) of IV ADDITIVES file (#52.6).
    pass

def ELYTES(PSSIEN,PSSFT,PSSFL,LIST):
    """
    PSSIEN - IEN of entry in IV ADDITIVES file (#52.6).
    PSSFT - Free Text name in IV ADDITIVES file (#52.6).
    PSSFL - Inactive flag - 0 or "" - All entries.
            FileMan Date - Only entries with no Inactive Date or an Inactive Date greater than this date.
    LIST - Subscript of ^TMP array in the form ^TMP($J,LIST,Field Number where Field Number is the
           Field Number of the data piece being returned.
    """
    # Returns PRINT NAME field (#.01), ELECTROLYTES subfile (#52.62), ELECTROLYTE field (#.01),
    # and CONCENTRATION field (#1) of IV ADDITIVES file (#52.6).
    pass

def SYNONYM(PSSIEN,PSSFT,PSSFL,LIST):
    """
    PSSIEN - IEN of entry in IV ADDITIVES file (#52.6).
    PSSFT - Free Text name in IV ADDITIVES file (#52.6).
    PSSFL - Inactive flag - 0 or "" - All entries.
            FileMan Date - Only entries with no Inactive Date or an Inactive Date greater than this date.
    LIST - Subscript of ^TMP array in the form ^TMP($J,LIST,Field Number where Field Number is the
           Field Number of the data piece being returned.
    """
    # Returns PRINT NAME field (#.01), SYNONYM subfile (#52.63), SYNONYM field (#.01) of IV ADDITIVES file (#52.6).
    pass

def INACTDT(PSSIEN):
    """
    PSSIEN - IEN of entry in IV ADDITIVES file (#52.6).
    Returns INACTIVATION DATE field (#12) of IV ADDITIVES file (#52.6).
    """
    pass

def DRGINFO(PSSIEN,PSSFT,PSSFL,LIST):
    """
    PSSIEN - IEN of entry in IV ADDITIVES file (#52.6).
    PSSFT - Free Text name in IV ADDITIVES file (#52.6).
    PSSFL - Inactive flag - 0 or "" - All entries.
            FileMan Date - Only entries with no Inactive Date or an Inactive Date greater than this date.
    LIST - Subscript of ^TMP array in the form ^TMP($J,LIST,Field Number where Field Number is the
           Field Number of the data piece being returned.
    """
    # Returns PRINT NAME field (#.01), DRUG INFORMATION subfile (#52.64), DRUG INFORMATION field (#.01)
    # of IV ADDITIVES file (#52.6).
    pass

def DRGIEN(PSS50,PSSFL,LIST):
    """
    PSS50 - IEN of entry in the DRUG file (#50) [required].
    PSSFL - Inactive flag - 0 or "" - All entries.
            FileMan Date - Only entries with no Inactive Date or an Inactive Date greater than this date.
    LIST - Subscript of ^TMP array in the form ^TMP($J,LIST,Field Number where Field Number is the
           Field Number of the data piece being returned.
    """
    # Returns PRINT NAME field (#.01) of IV ADDITIVES file (#52.6).
    pass

def LOOKUP(PSS50P7,PSSFL,LIST):
    """
    PSS50P7 - IEN of entry in PHARMACY ORDERABLE ITEM file (#50.7).
    PSSFL - Inactive flag - 0 or "" - All entries.
            FileMan Date - Only entries with no Inactive Date or an Inactive Date greater than this date.
    LIST - Subscript of ^TMP array in the form ^TMP($J,LIST,Field Number where Field Number is the
           Field Number of the data piece being returned.
    """
    # Returns PRINT NAME field (#.01), MESSAGES field (#14), QUICK CODE subfile (#52.61), QUICK CODE field (#.01),
    # STRENGTH field (#1), USUAL INFUSION RATE field (#2), OTHER PRINT INFO field (#3), USUAL IV SCHEDULE field (#4),
    # ADMINISTRATION TIMES field (#5), USUAL IV SOLUTION field (#6), MED ROUTE field (#7), SYNONYM subfile (#52.63),
    # SYNONYM field (#.01) of IV ADDITIVES file (#52.6).
    pass

def POI(PSSOI,PSSFL,LIST):
    """
    PSSOI - IEN of entry in the PHARMACY ORDERABLE ITEM file (#50.7) [required].
    PSSFL - Inactive flag - 0 or "" - All entries.
            FileMan Date - Only entries with no Inactive Date or an Inactive Date greater than this date.
    LIST - Subscript of ^TMP array in the form ^TMP($J,LIST,Field Number where Field Number is the
           Field Number of the data piece being returned.
    """
    # Returns PRINT NAME field (#.01) of IV ADDITIVES file (#52.6).
    pass

def C(PSSQCODE,PSSIEN):
    """
    PSSQCODE - Text name of QUICKCODE [required].
    PSSIEN - IEN of entry in the IV ADDITIVES file (#52.6) [required].
    Returns 1 if there's an entry in the C x-ref, otherwise a 0.
    """
    pass