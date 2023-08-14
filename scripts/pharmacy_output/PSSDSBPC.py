def NUMC():
    global PSSDBV1, PSSDBV2, PSSDBV9, PSSDBIFL
    PSSDBV1 = PSSDBV9[:4]
    if PSSDBV1 == "5-6 ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[4:]
        return 6 if _8() else 0

    PSSDBV1 = PSSDBV9[:6]
    if PSSDBV1 == "5 - 6 ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[6:]
        return 6 if _8() else 0

    PSSDBV1 = PSSDBV9[:7]
    if PSSDBV1 == "5 TO 6 ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[7:]
        return 6 if _8() else 0

    PSSDBV1 = PSSDBV9[:7]
    if PSSDBV1 == "5 OR 6 ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[7:]
        return 6 if _8() else 0

    PSSDBV1 = PSSDBV9[:12]
    if PSSDBV1 == "FIVE TO SIX ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[12:]
        return 6 if _8() else 0

    PSSDBV1 = PSSDBV9[:12]
    if PSSDBV1 == "FIVE OR SIX ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[12:]
        return 6 if _8() else 0

    PSSDBV1 = PSSDBV9[:9]
    if PSSDBV1 == "FIVE-SIX ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[9:]
        return 6 if _8() else 0

    PSSDBV1 = PSSDBV9[:11]
    if PSSDBV1 == "FIVE - SIX ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[11:]
        return 6 if _8() else 0

    PSSDBV1 = PSSDBV9[:2]
    if PSSDBV1 == "6 " and _4():
        PSSDBV2 = PSSDBV9[2:]
        if _8():
            return 6

    PSSDBV1 = PSSDBV9[:4]
    if PSSDBV1 == "SIX " and _4():
        PSSDBV2 = PSSDBV9[4:]
        if _8():
            return 6

    PSSDBV1 = PSSDBV9[:10]
    if PSSDBV1 == "6 AND 1/4 ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[10:]
        return 6.25 if _8() else 0

    PSSDBV1 = PSSDBV9[:19]
    if PSSDBV1 == "SIX AND ONE FOURTH ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[19:]
        return 6.25 if _8() else 0

    PSSDBV1 = PSSDBV9[:19]
    if PSSDBV1 == "SIX AND ONE-FOURTH ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[19:]
        return 6.25 if _8() else 0

    PSSDBV1 = PSSDBV9[:17]
    if PSSDBV1 == "6 AND ONE FOURTH ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[17:]
        return 6.25 if _8() else 0

    PSSDBV1 = PSSDBV9[:17]
    if PSSDBV1 == "6 AND ONE-FOURTH ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[17:]
        return 6.25 if _8() else 0

    PSSDBV1 = PSSDBV9[:12]
    if PSSDBV1 == "SIX AND 1/4 ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[12:]
        return 6.25 if _8() else 0

    PSSDBV1 = PSSDBV9[:10]
    if PSSDBV1 == "6 AND 1/3 ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[10:]
        return 6.33 if _8() else 0

    PSSDBV1 = PSSDBV9[:18]
    if PSSDBV1 == "SIX AND ONE THIRD ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[18:]
        return 6.33 if _8() else 0

    PSSDBV1 = PSSDBV9[:18]
    if PSSDBV1 == "SIX AND ONE-THIRD ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[18:]
        return 6.33 if _8() else 0

    PSSDBV1 = PSSDBV9[:16]
    if PSSDBV1 == "6 AND ONE THIRD ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[16:]
        return 6.33 if _8() else 0

    PSSDBV1 = PSSDBV9[:16]
    if PSSDBV1 == "6 AND ONE-THIRD ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[16:]
        return 6.33 if _8() else 0

    PSSDBV1 = PSSDBV9[:12]
    if PSSDBV1 == "SIX AND 1/3 ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[12:]
        return 6.33 if _8() else 0

    PSSDBV1 = PSSDBV9[:10]
    if PSSDBV1 == "6 AND 1/2 ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[10:]
        return 6.5 if _8() else 0

    PSSDBV1 = PSSDBV9[:17]
    if PSSDBV1 == "SIX AND ONE HALF ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[17:]
        return 6.5 if _8() else 0

    PSSDBV1 = PSSDBV9[:17]
    if PSSDBV1 == "SIX AND ONE-HALF ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[17:]
        return 6.5 if _8() else 0

    PSSDBV1 = PSSDBV9[:15]
    if PSSDBV1 == "6 AND ONE HALF ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[15:]
        return 6.5 if _8() else 0

    PSSDBV1 = PSSDBV9[:15]
    if PSSDBV1 == "6 AND ONE-HALF ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[15:]
        return 6.5 if _8() else 0

    PSSDBV1 = PSSDBV9[:14]
    if PSSDBV1 == "SIX AND 1/2 ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[14:]
        return 6.5 if _8() else 0

    PSSDBV1 = PSSDBV9[:4]
    if PSSDBV1 == "6-7 ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[4:]
        return 7 if _8() else 0

    PSSDBV1 = PSSDBV9[:6]
    if PSSDBV1 == "6 - 7 ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[6:]
        return 7 if _8() else 0

    PSSDBV1 = PSSDBV9[:7]
    if PSSDBV1 == "6 TO 7 ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[7:]
        return 7 if _8() else 0

    PSSDBV1 = PSSDBV9[:7]
    if PSSDBV1 == "6 OR 7 ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[7:]
        return 7 if _8() else 0

    PSSDBV1 = PSSDBV9[:13]
    if PSSDBV1 == "SIX TO SEVEN ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[13:]
        return 7 if _8() else 0

    PSSDBV1 = PSSDBV9[:13]
    if PSSDBV1 == "SIX OR SEVEN ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[13:]
        return 7 if _8() else 0

    PSSDBV1 = PSSDBV9[:10]
    if PSSDBV1 == "SIX-SEVEN ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[10:]
        return 7 if _8() else 0

    PSSDBV1 = PSSDBV9[:12]
    if PSSDBV1 == "SIX - SEVEN ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[12:]
        return 7 if _8() else 0

    PSSDBV1 = PSSDBV9[:2]
    if PSSDBV1 == "7 " and _4():
        PSSDBV2 = PSSDBV9[2:]
        if _8():
            return 7

    PSSDBV1 = PSSDBV9[:6]
    if PSSDBV1 == "SEVEN " and _4():
        PSSDBV2 = PSSDBV9[6:]
        if _8():
            return 7

    PSSDBV1 = PSSDBV9[:10]
    if PSSDBV1 == "7 AND 1/4 ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[10:]
        return 7.25 if _8() else 0

    PSSDBV1 = PSSDBV9[:21]
    if PSSDBV1 == "SEVEN AND ONE FOURTH ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[21:]
        return 7.25 if _8() else 0

    PSSDBV1 = PSSDBV9[:21]
    if PSSDBV1 == "SEVEN AND ONE-FOURTH ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[21:]
        return 7.25 if _8() else 0

    PSSDBV1 = PSSDBV9[:17]
    if PSSDBV1 == "7 AND ONE FOURTH ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[17:]
        return 7.25 if _8() else 0

    PSSDBV1 = PSSDBV9[:17]
    if PSSDBV1 == "7 AND ONE-FOURTH ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[17:]
        return 7.25 if _8() else 0

    PSSDBV1 = PSSDBV9[:14]
    if PSSDBV1 == "SEVEN AND 1/4 ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[14:]
        return 7.25 if _8() else 0

    PSSDBV1 = PSSDBV9[:10]
    if PSSDBV1 == "7 AND 1/3 ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[10:]
        return 7.33 if _8() else 0

    PSSDBV1 = PSSDBV9[:20]
    if PSSDBV1 == "SEVEN AND ONE THIRD ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[20:]
        return 7.33 if _8() else 0

    PSSDBV1 = PSSDBV9[:20]
    if PSSDBV1 == "SEVEN AND ONE-THIRD ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[20:]
        return 7.33 if _8() else 0

    PSSDBV1 = PSSDBV9[:16]
    if PSSDBV1 == "7 AND ONE THIRD ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[16:]
        return 7.33 if _8() else 0

    PSSDBV1 = PSSDBV9[:16]
    if PSSDBV1 == "7 AND ONE-THIRD ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[16:]
        return 7.33 if _8() else 0

    PSSDBV1 = PSSDBV9[:14]
    if PSSDBV1 == "SEVEN AND 1/3 ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[14:]
        return 7.33 if _8() else 0

    PSSDBV1 = PSSDBV9[:10]
    if PSSDBV1 == "7 AND 1/2 ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[10:]
        return 7.5 if _8() else 0

    PSSDBV1 = PSSDBV9[:19]
    if PSSDBV1 == "SEVEN AND ONE HALF ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[19:]
        return 7.5 if _8() else 0

    PSSDBV1 = PSSDBV9[:19]
    if PSSDBV1 == "SEVEN AND ONE-HALF ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[19:]
        return 7.5 if _8() else 0

    PSSDBV1 = PSSDBV9[:15]
    if PSSDBV1 == "7 AND ONE HALF ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[15:]
        return 7.5 if _8() else 0

    PSSDBV1 = PSSDBV9[:15]
    if PSSDBV1 == "7 AND ONE-HALF ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[15:]
        return 7.5 if _8() else 0

    PSSDBV1 = PSSDBV9[:14]
    if PSSDBV1 == "SEVEN AND 1/2 ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[14:]
        return 7.5 if _8() else 0

    return ""


def _8():
    global PSSDBV2, PSSDBV3, PSSDBIFL
    PSSDBV3 = ""
    if PSSDBIFL:
        PSSDBV3 = UNITD(PSSDBV2)
    else:
        PSSDBV3 = UNIT(PSSDBV2)
    return bool(PSSDBV3)


def _4():
    global PSSDBV1, PSSDBV9
    if len(PSSDBV9) <= len(PSSDBV1):
        return 0
    return 1