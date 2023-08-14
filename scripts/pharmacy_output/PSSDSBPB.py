def NUMX():
    PSSQVJ1 = PSSQVLCD[:5]
    if PSSQVJ1 == "0.33 ":
        if not _6():
            return 0
        PSSQVJ2 = PSSQVLCD[5:]
        return 0.33 if _6() else 0
    PSSQVJ1 = PSSQVLCD[:4]
    if PSSQVJ1 == "1/3 ":
        if not _6():
            return 0
        PSSQVJ2 = PSSQVLCD[4:]
        return 0.33 if _6() else 0
    PSSQVJ1 = PSSQVLCD[:10]
    if PSSQVJ1 == "ONE THIRD ":
        if not _6():
            return 0
        PSSQVJ2 = PSSQVLCD[10:]
        return 0.33 if _6() else 0
    PSSQVJ1 = PSSQVLCD[:10]
    if PSSQVJ1 == "ONE-THIRD ":
        if not _6():
            return 0
        PSSQVJ2 = PSSQVLCD[10:]
        return 0.33 if _6() else 0
    PSSQVJ1 = PSSQVLCD[:5]
    if PSSQVJ1 == "0.25 ":
        if not _6():
            return 0
        PSSQVJ2 = PSSQVLCD[5:]
        return 0.25 if _6() else 0
    PSSQVJ1 = PSSQVLCD[:4]
    if PSSQVJ1 == "1/4 ":
        if not _6():
            return 0
        PSSQVJ2 = PSSQVLCD[4:]
        return 0.25 if _6() else 0
    PSSQVJ1 = PSSQVLCD[:11]
    if PSSQVJ1 == "ONE FOURTH ":
        if not _6():
            return 0
        PSSQVJ2 = PSSQVLCD[11:]
        return 0.25 if _6() else 0
    PSSQVJ1 = PSSQVLCD[:11]
    if PSSQVJ1 == "ONE-FOURTH ":
        if not _6():
            return 0
        PSSQVJ2 = PSSQVLCD[11:]
        return 0.25 if _6() else 0
    PSSQVJ1 = PSSQVLCD[:2]
    if PSSQVJ1 == "4 ":
        if not _6() or not _9():
            return 0
        PSSQVJ2 = PSSQVLCD[2:]
        return 4 if _6() and _9() else 0
    PSSQVJ1 = PSSQVLCD[:5]
    if PSSQVJ1 == "FOUR ":
        if not _6() or not _9():
            return 0
        PSSQVJ2 = PSSQVLCD[5:]
        return 4 if _6() and _9() else 0
    PSSQVJ1 = PSSQVLCD[:2]
    if PSSQVJ1 == "3 ":
        if not _6() or not _9():
            return 0
        PSSQVJ2 = PSSQVLCD[2:]
        return 3 if _6() and _9() else 0
    PSSQVJ1 = PSSQVLCD[:6]
    if PSSQVJ1 == "THREE ":
        if not _6() or not _9():
            return 0
        PSSQVJ2 = PSSQVLCD[6:]
        return 3 if _6() and _9() else 0
    PSSQVJ1 = PSSQVLCD[:2]
    if PSSQVJ1 == "2 ":
        if not _6() or not _9():
            return 0
        PSSQVJ2 = PSSQVLCD[2:]
        return 2 if _6() and _9() else 0
    PSSQVJ1 = PSSQVLCD[:4]
    if PSSQVJ1 == "TWO ":
        if not _6() or not _9():
            return 0
        PSSQVJ2 = PSSQVLCD[4:]
        return 2 if _6() and _9() else 0
    PSSQVJ1 = PSSQVLCD[:2]
    if PSSQVJ1 == "1 ":
        if not _6() or not _9():
            return 0
        PSSQVJ2 = PSSQVLCD[2:]
        return 1 if _6() and _9() else 0
    PSSQVJ1 = PSSQVLCD[:4]
    if PSSQVJ1 == "ONE ":
        if not _6() or not _9():
            return 0
        PSSQVJ2 = PSSQVLCD[4:]
        return 1 if _6() and _9() else 0
    return 0

def _6():
    if " " in PSSQVJ2:
        return 0
    if "-" in PSSQVJ2:
        return 0
    if "&" in PSSQVJ2:
        return 0
    if "\\" in PSSQVJ2:
        return 0
    if "/" in PSSQVJ2:
        return 0
    return 1

def _7():
    if len(PSSQVLCD) <= len(PSSQVJ1):
        return 0
    return 1

def _9():
    if "4" not in PSSQVJ2 and "3" not in PSSQVJ2 and "2" not in PSSQVJ2 and "FOURTH" not in PSSQVJ2 and "THIRD" not in PSSQVJ2 and "HALF" not in PSSQVJ2:
        return 1
    return 0

def NUMC():
    PSSDBV1 = PSSDBV9[:4]
    if PSSDBV1 == "3-4 ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[4:]
        return 4 if _8() else 0
    PSSDBV1 = PSSDBV9[:6]
    if PSSDBV1 == "3 - 4 ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[6:]
        return 4 if _8() else 0
    PSSDBV1 = PSSDBV9[:7]
    if PSSDBV1 == "3 TO 4 ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[7:]
        return 4 if _8() else 0
    PSSDBV1 = PSSDBV9[:7]
    if PSSDBV1 == "3 OR 4 ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[7:]
        return 4 if _8() else 0
    PSSDBV1 = PSSDBV9[:14]
    if PSSDBV1 == "THREE TO FOUR ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[14:]
        return 4 if _8() else 0
    PSSDBV1 = PSSDBV9[:14]
    if PSSDBV1 == "THREE OR FOUR ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[14:]
        return 4 if _8() else 0
    PSSDBV1 = PSSDBV9[:11]
    if PSSDBV1 == "THREE-FOUR ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[11:]
        return 4 if _8() else 0
    PSSDBV1 = PSSDBV9[:13]
    if PSSDBV1 == "THREE - FOUR ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[13:]
        return 4 if _8() else 0
    PSSDBV1 = PSSDBV9[:2]
    if PSSDBV1 == "4 ":
        if _4():
            PSSDBV2 = PSSDBV9[2:]
            if _8():
                return 4
    PSSDBV1 = PSSDBV9[:5]
    if PSSDBV1 == "FOUR ":
        if _4():
            PSSDBV2 = PSSDBV9[5:]
            if _8():
                return 4
    PSSDBV1 = PSSDBV9[:10]
    if PSSDBV1 == "4 AND 1/4 ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[10:]
        return 4.25 if _8() else 0
    PSSDBV1 = PSSDBV9[:20]
    if PSSDBV1 == "FOUR AND ONE FOURTH ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[20:]
        return 4.25 if _8() else 0
    PSSDBV1 = PSSDBV9[:20]
    if PSSDBV1 == "FOUR AND ONE-FOURTH ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[20:]
        return 4.25 if _8() else 0
    PSSDBV1 = PSSDBV9[:17]
    if PSSDBV1 == "4 AND ONE FOURTH ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[17:]
        return 4.25 if _8() else 0
    PSSDBV1 = PSSDBV9[:17]
    if PSSDBV1 == "4 AND ONE-FOURTH ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[17:]
        return 4.25 if _8() else 0
    PSSDBV1 = PSSDBV9[:13]
    if PSSDBV1 == "FOUR AND 1/4 ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[13:]
        return 4.25 if _8() else 0
    PSSDBV1 = PSSDBV9[:10]
    if PSSDBV1 == "4 AND 1/3 ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[10:]
        return 4.33 if _8() else 0
    PSSDBV1 = PSSDBV9[:19]
    if PSSDBV1 == "FOUR AND ONE THIRD ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[19:]
        return 4.33 if _8() else 0
    PSSDBV1 = PSSDBV9[:19]
    if PSSDBV1 == "FOUR AND ONE-THIRD ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[19:]
        return 4.33 if _8() else 0
    PSSDBV1 = PSSDBV9[:16]
    if PSSDBV1 == "4 AND ONE THIRD ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[16:]
        return 4.33 if _8() else 0
    PSSDBV1 = PSSDBV9[:16]
    if PSSDBV1 == "4 AND ONE-THIRD ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[16:]
        return 4.33 if _8() else 0
    PSSDBV1 = PSSDBV9[:13]
    if PSSDBV1 == "FOUR AND 1/3 ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[13:]
        return 4.33 if _8() else 0
    PSSDBV1 = PSSDBV9[:10]
    if PSSDBV1 == "4 AND 1/2 ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[10:]
        return 4.5 if _8() else 0
    PSSDBV1 = PSSDBV9[:18]
    if PSSDBV1 == "FOUR AND ONE HALF ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[18:]
        return 4.5 if _8() else 0
    PSSDBV1 = PSSDBV9[:18]
    if PSSDBV1 == "FOUR AND ONE-HALF ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[18:]
        return 4.5 if _8() else 0
    PSSDBV1 = PSSDBV9[:15]
    if PSSDBV1 == "4 AND ONE HALF ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[15:]
        return 4.5 if _8() else 0
    PSSDBV1 = PSSDBV9[:15]
    if PSSDBV1 == "4 AND ONE-HALF ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[15:]
        return 4.5 if _8() else 0
    PSSDBV1 = PSSDBV9[:13]
    if PSSDBV1 == "FOUR AND 1/2 ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[13:]
        return 4.5 if _8() else 0
    PSSDBV1 = PSSDBV9[:10]
    if PSSDBV1 == "5 AND 1/4 ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[10:]
        return 5.25 if _8() else 0
    PSSDBV1 = PSSDBV9[:20]
    if PSSDBV1 == "FIVE AND ONE FOURTH ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[20:]
        return 5.25 if _8() else 0
    PSSDBV1 = PSSDBV9[:20]
    if PSSDBV1 == "FIVE AND ONE-FOURTH ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[20:]
        return 5.25 if _8() else 0
    PSSDBV1 = PSSDBV9[:17]
    if PSSDBV1 == "5 AND ONE FOURTH ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[17:]
        return 5.25 if _8() else 0
    PSSDBV1 = PSSDBV9[:17]
    if PSSDBV1 == "5 AND ONE-FOURTH ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[17:]
        return 5.25 if _8() else 0
    PSSDBV1 = PSSDBV9[:13]
    if PSSDBV1 == "FIVE AND 1/4 ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[13:]
        return 5.25 if _8() else 0
    PSSDBV1 = PSSDBV9[:10]
    if PSSDBV1 == "5 AND 1/3 ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[10:]
        return 5.33 if _8() else 0
    PSSDBV1 = PSSDBV9[:19]
    if PSSDBV1 == "FIVE AND ONE THIRD ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[19:]
        return 5.33 if _8() else 0
    PSSDBV1 = PSSDBV9[:19]
    if PSSDBV1 == "FIVE AND ONE-THIRD ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[19:]
        return 5.33 if _8() else 0
    PSSDBV1 = PSSDBV9[:16]
    if PSSDBV1 == "5 AND ONE THIRD ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[16:]
        return 5.33 if _8() else 0
    PSSDBV1 = PSSDBV9[:16]
    if PSSDBV1 == "5 AND ONE-THIRD ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[16:]
        return 5.33 if _8() else 0
    PSSDBV1 = PSSDBV9[:13]
    if PSSDBV1 == "FIVE AND 1/3 ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[13:]
        return 5.33 if _8() else 0
    PSSDBV1 = PSSDBV9[:10]
    if PSSDBV1 == "5 AND 1/2 ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[10:]
        return 5.5 if _8() else 0
    PSSDBV1 = PSSDBV9[:18]
    if PSSDBV1 == "FIVE AND ONE HALF ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[18:]
        return 5.5 if _8() else 0
    PSSDBV1 = PSSDBV9[:18]
    if PSSDBV1 == "FIVE AND ONE-HALF ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[18:]
        return 5.5 if _8() else 0
    PSSDBV1 = PSSDBV9[:15]
    if PSSDBV1 == "5 AND ONE HALF ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[15:]
        return 5.5 if _8() else 0
    PSSDBV1 = PSSDBV9[:15]
    if PSSDBV1 == "5 AND ONE-HALF ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[15:]
        return 5.5 if _8() else 0
    PSSDBV1 = PSSDBV9[:13]
    if PSSDBV1 == "FIVE AND 1/2 ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[13:]
        return 5.5 if _8() else 0
    PSSDBV1 = PSSDBV9[:4]
    if PSSDBV1 == "4-5 ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[4:]
        return 5 if _8() else 0
    PSSDBV1 = PSSDBV9[:6]
    if PSSDBV1 == "4 - 5 ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[6:]
        return 5 if _8() else 0
    PSSDBV1 = PSSDBV9[:7]
    if PSSDBV1 == "4 TO 5 ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[7:]
        return 5 if _8() else 0
    PSSDBV1 = PSSDBV9[:7]
    if PSSDBV1 == "4 OR 5 ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[7:]
        return 5 if _8() else 0
    PSSDBV1 = PSSDBV9[:13]
    if PSSDBV1 == "FOUR TO FIVE ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[13:]
        return 5 if _8() else 0
    PSSDBV1 = PSSDBV9[:13]
    if PSSDBV1 == "FOUR OR FIVE ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[13:]
        return 5 if _8() else 0
    PSSDBV1 = PSSDBV9[:10]
    if PSSDBV1 == "FOUR-FIVE ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[10:]
        return 5 if _8() else 0
    PSSDBV1 = PSSDBV9[:12]
    if PSSDBV1 == "FOUR - FIVE ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[12:]
        return 5 if _8() else 0
    PSSDBV1 = PSSDBV9[:2]
    if PSSDBV1 == "5 ":
        if _4():
            PSSDBV2 = PSSDBV9[2:]
            if _8():
                return 5
    PSSDBV1 = PSSDBV9[:5]
    if PSSDBV1 == "FIVE ":
        if _4():
            PSSDBV2 = PSSDBV9[5:]
            if _8():
                return 5
    PSSDBV1 = PSSDBV9[:10]
    if PSSDBV1 == "5 AND 1/4 ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[10:]
        return 5.25 if _8() else 0
    PSSDBV1 = PSSDBV9[:20]
    if PSSDBV1 == "FIVE AND ONE FOURTH ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[20:]
        return 5.25 if _8() else 0
    PSSDBV1 = PSSDBV9[:20]
    if PSSDBV1 == "FIVE AND ONE-FOURTH ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[20:]
        return 5.25 if _8() else 0
    PSSDBV1 = PSSDBV9[:17]
    if PSSDBV1 == "5 AND ONE FOURTH ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[17:]
        return 5.25 if _8() else 0
    PSSDBV1 = PSSDBV9[:17]
    if PSSDBV1 == "5 AND ONE-FOURTH ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[17:]
        return 5.25 if _8() else 0
    PSSDBV1 = PSSDBV9[:13]
    if PSSDBV1 == "FIVE AND 1/4 ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[13:]
        return 5.25 if _8() else 0
    PSSDBV1 = PSSDBV9[:10]
    if PSSDBV1 == "5 AND 1/3 ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[10:]
        return 5.33 if _8() else 0
    PSSDBV1 = PSSDBV9[:19]
    if PSSDBV1 == "FIVE AND ONE THIRD ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[19:]
        return 5.33 if _8() else 0
    PSSDBV1 = PSSDBV9[:19]
    if PSSDBV1 == "FIVE AND ONE-THIRD ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[19:]
        return 5.33 if _8() else 0
    PSSDBV1 = PSSDBV9[:16]
    if PSSDBV1 == "5 AND ONE THIRD ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[16:]
        return 5.33 if _8() else 0
    PSSDBV1 = PSSDBV9[:16]
    if PSSDBV1 == "5 AND ONE-THIRD ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[16:]
        return 5.33 if _8() else 0
    PSSDBV1 = PSSDBV9[:13]
    if PSSDBV1 == "FIVE AND 1/3 ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[13:]
        return 5.33 if _8() else 0
    PSSDBV1 = PSSDBV9[:10]
    if PSSDBV1 == "5 AND 1/2 ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[10:]
        return 5.5 if _8() else 0
    PSSDBV1 = PSSDBV9[:18]
    if PSSDBV1 == "FIVE AND ONE HALF ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[18:]
        return 5.5 if _8() else 0
    PSSDBV1 = PSSDBV9[:18]
    if PSSDBV1 == "FIVE AND ONE-HALF ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[18:]
        return 5.5 if _8() else 0
    PSSDBV1 = PSSDBV9[:15]
    if PSSDBV1 == "5 AND ONE HALF ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[15:]
        return 5.5 if _8() else 0
    PSSDBV1 = PSSDBV9[:15]
    if PSSDBV1 == "5 AND ONE-HALF ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[15:]
        return 5.5 if _8() else 0
    PSSDBV1 = PSSDBV9[:13]
    if PSSDBV1 == "FIVE AND 1/2 ":
        if not _4():
            return 0
        PSSDBV2 = PSSDBV9[13:]
        return 5.5 if _8() else 0
    return ""

def _8():
    PSSDBV3 = ""
    if PSSDBIFL:
        PSSDBV3 = UNITD(PSSDBV2)
    else:
        PSSDBV3 = UNIT(PSSDBV2)
    return True if PSSDBV3 != "" else False

def _4():
    if len(PSSDBV9) <= len(PSSDBV1):
        return 0
    return 1

def UNITD(PSSDBV2):
    # Placeholder for UNITD implementation
    pass

def UNIT(PSSDBV2):
    # Placeholder for UNIT implementation
    pass

def TEST():
    while True:
        PSSQVLCD = input("Possible Dosage: ")
        if PSSQVLCD == "":
            break
        print(NUMX())

TEST()