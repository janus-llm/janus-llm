def OIDEA(PSSXOI, PSSXOIP):
    """
    CPRS Orderable Item call
    Returns the CS Federal Schedule code in the VA PRODUCT file (#50.68)
    or the DEA Special Hndl code depending on the "ND" node of the
    drugs associated to the Orderable Item, and Usage passed in

    1  Sch. I Nar.
    2  II
    2n II Non-Nar.
    3  III
    3n III Non-Nar.
    4  IV
    5  V
    0  there are other active drugs
    "" no active drugs

    :param PSSXOI: Orderable Item
    :param PSSXOIP: Usage
    :return: CS Federal Schedule code or DEA Special Hndl code
    """
    PSSXOLPD = 0
    PSSXNODD = 0
    if PSSXOIP == "X":
        return OIQ()
    if not PSSXOI or not PSSXOIP:
        return OIQ()
    PSSPKLX = 1 if PSSXOIP in ["I", "U"] else 0
    for PSSXOLP in range(len(PSDRUG)):
        if (
            PSSDRUG[PSSXOLP]["I"]
            and PSSDRUG[PSSXOLP]["I"] < DT
        ):
            continue
        if (
            not PSSPKLX
            and "O" not in PSSDRUG[PSSXOLP][2]
        ):
            continue
        if (
            PSSPKLX
            and "U" not in PSSDRUG[PSSXOLP][2]
            and "I" not in PSSDRUG[PSSXOLP][2]
        ):
            continue
        PSSXNODD = 1
        PSSJ = PSSDRUG[PSSXOLP][0][2]
        if PSSJ:
            PSSGD[PSSJ] = ""
        if PSSDRUG[PSSXOLP]["ND"][3]:
            PSSK = PSSDRUG[PSSXOLP]["ND"][3]
            if PSSNDF[PSSK][7]:
                PSSK = PSSNDF[PSSK][7]
                PSSI[PSSK[0] + ".5" if PSSK[1] == "n" else PSSK] = ""
    if PSSI:
        return CSS()
    PSSXOLPX = ""
    for PSSXOLPX in PSSGD:
        if PSSXOLPX[1]:
            PSSI[1] = ""
            continue
        if PSSXOLPX[2] and "C" not in PSSXOLPX:
            PSSI[2] = ""
            continue
        if PSSXOLPX[2] and "C" in PSSXOLPX:
            PSSI[2.5] = ""
            continue
        if PSSXOLPX[3] and "C" not in PSSXOLPX:
            PSSI[3] = ""
            continue
        if PSSXOLPX[3] and "C" in PSSXOLPX:
            PSSI[3.5] = ""
            continue
        if PSSXOLPX[4]:
            PSSI[4] = ""
            continue
        if PSSXOLPX[5]:
            PSSI[5] = ""
    if PSSK in PSSI:
        PSSXOLPD = PSSK[0] + ("n" if len(PSSK) > 1 else "")
    return OIQ() if PSSXOLPD == 0 else (
        "1;" + PSSXOLPD if PSSXOLPD in [1, 2] else "2;" + PSSXOLPD
    )


def DEAPKI(PSSDIENM):
    """
    Return CS Federal Sch or the DEA Special Hndl for CPRS Dose Call - PKI Project

    :param PSSDIENM: Drug IEN
    """
    if not PSSDIENM:
        return
    PSSDEAX = PSSDEAXV = None
    if PSSDRUG[PSSDIENM]["ND"][3]:
        PSSDEAX = PSSDRUG[PSSDIENM]["ND"][3]
        if PSSNDF[PSSDEAX][7]:
            PSSDEAXV = PSSNDF[PSSDEAX][7]
            PSSJ = 1
    if PSSJ:
        return DSET()
    PSSDEAX = PSSDRUG[PSSDIENM][0][3]
    if PSSDEAX[1]:
        PSSDEAXV = 1
    elif PSSDEAX[2] and "C" not in PSSDEAX:
        PSSDEAXV = 2
    elif PSSDEAX[2] and "C" in PSSDEAX:
        PSSDEAXV = "2n"
    elif PSSDEAX[3] and "C" not in PSSDEAX:
        PSSDEAXV = 3
    elif PSSDEAX[3] and "C" in PSSDEAX:
        PSSDEAXV = "3n"
    elif PSSDEAX[4]:
        PSSDEAXV = 4
    elif PSSDEAX[5]:
        PSSDEAXV = 5
    else:
        PSSDEAXV = 0
    return DSET()


def DETOX(PSSDIEN):
    """
    BUPREN drug check to determine if drug is a detox medication

    :param PSSDIEN: Drug IEN
    :return: 1 if the drug is a Detox medication, otherwise 0
    """
    if not PSSDIEN:
        return 0
    if "BUPREN" not in PSSDRUG[PSSDIEN][0]:
        return 0
    PSSJ = 1
    PKGLIST = {}
    SYSLIST = {}
    GETLST(PKGLIST, "PKG", "PSS BUPRENORPHINE PAIN VAPRODS", "N")
    DETINDEX(PKGLIST)
    GETLST(SYSLIST, "SYS", "PSS BUPRENORPHINE PAIN VAPRODS", "N")
    DETINDEX(SYSLIST)
    if PSSDRUG[PSSDIEN]["ND"][3]:
        PSSNDF = PSSDRUG[PSSDIEN]["ND"][3]
        PSSY = GET1(50.68, PSSNDF, 4)
        if PSSY and (PSSY in PKGLIST or PSSY in SYSLIST):
            PSSJ = 0
    return PSSJ


def DETINDEX(LIST):
    """
    Helper function for DETOX

    :param LIST: List
    """
    for I in range(len(LIST)):
        IEN = LIST[I][0]
        LIST["B"][GET1(50.68, IEN, 4)] = ""


def OIDETOX(PSSXOI, PSSXOIP):
    """
    CPRS Orderable Item to check if a drug is a DETOX or not

    :param PSSXOI: Orderable Item IEN
    :param PSSXOIP: Package
    :return: 1 if the drugs associated to the Orderable Item contains the text "BUPREN" as part of the name, otherwise 0
    """
    if not PSSXOI or PSSXOIP != "O":
        return 0
    PSSDTOX = 0
    for PSSLP in range(len(PSDRUG)):
        if (
            PSSDRUG[PSSLP]["I"]
            and PSSDRUG[PSSLP]["I"] < DT
        ):
            continue
        PSSDPK = PSSDRUG[PSSLP][2]
        if not PSSDPK or "O" not in PSSDPK:
            continue
        if DETOX(PSSLP):
            PSSDTOX = 1
            break
    return PSSDTOX


def BUPARED():
    """
    Manage Buprenorphine Tx of Pain using VA Product file (#50.68)
    """
    EDITPAR("PSS BUPRENORPHINE PAIN VAPRODS")


def DSET():
    """
    Helper function for OIDEA and DEAPKI
    """
    PSSX["DD"][PSSDIENM] = (
        PSSX["DD"][PSSDIENM]
        + "^"
        + PSSDEAXV
        + "^"
        + ("1" if PSSHLF[PSSDIENM] else "0")
    )
    return


def OIQ():
    """
    Helper function for OIDEA
    """
    if PSSXOLPD == 0:
        if not PSSXNODD:
            PSSXOLPD = ""
    elif PSSXOLPD in [1, 2]:
        PSSXOLPD = "1;" + str(PSSXOLPD)
    else:
        PSSXOLPD = "2;" + str(PSSXOLPD)
    return PSSXOLPD