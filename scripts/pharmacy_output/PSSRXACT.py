def PSSRXACT(DFN):
    FLAG = None
    EXPD = DT - 1

    while EXPD:
        EXPD = next(iter(filter(lambda x: x > EXPD, ^PS(55, DFN, "P", "A"))))
        if not EXPD or FLAG:
            break

        RX = 0
        while RX:
            RX = next(iter(filter(lambda x: x > RX, ^PS(55, DFN, "P", "A", EXPD))))
            if not RX or FLAG:
                break

            EN^PSOORDER(DFN, RX)
            if not ^TMP("PSOR", $J, RX, 0):
                continue

            STAT = ^TMP("PSOR", $J, RX, 0).split("^")[3].split(";")[0]
            FLAG = 1 if STAT in ["A", "N", "H", "S"] else 0
            ^TMP("PSOR", $J) = {}

    return int(FLAG) if FLAG else 0