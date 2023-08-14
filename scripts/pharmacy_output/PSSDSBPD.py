def NUMC():
    PSSDBV1 = PSSDBV9[:4]
    if PSSDBV1 == "7-8 ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[4:]
        return 8 if check_8() else 0

    PSSDBV1 = PSSDBV9[:6]
    if PSSDBV1 == "7 - 8 ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[6:]
        return 8 if check_8() else 0

    PSSDBV1 = PSSDBV9[:7]
    if PSSDBV1 == "7 TO 8 ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[7:]
        return 8 if check_8() else 0

    PSSDBV1 = PSSDBV9[:7]
    if PSSDBV1 == "7 OR 8 ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[7:]
        return 8 if check_8() else 0

    PSSDBV1 = PSSDBV9[:15]
    if PSSDBV1 == "SEVEN TO EIGHT ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[15:]
        return 8 if check_8() else 0

    PSSDBV1 = PSSDBV9[:15]
    if PSSDBV1 == "SEVEN OR EIGHT ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[15:]
        return 8 if check_8() else 0

    PSSDBV1 = PSSDBV9[:12]
    if PSSDBV1 == "SEVEN-EIGHT ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[12:]
        return 8 if check_8() else 0

    PSSDBV1 = PSSDBV9[:14]
    if PSSDBV1 == "SEVEN - EIGHT ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[14:]
        return 8 if check_8() else 0

    PSSDBV1 = PSSDBV9[:2]
    if PSSDBV1 == "8 " and check_4():
        PSSDBV2 = PSSDBV9[2:]
        if check_8():
            return 8

    PSSDBV1 = PSSDBV9[:6]
    if PSSDBV1 == "EIGHT " and check_4():
        PSSDBV2 = PSSDBV9[6:]
        if check_8():
            return 8

    PSSDBV1 = PSSDBV9[:10]
    if PSSDBV1 == "8 AND 1/4 ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[10:]
        return 8.25 if check_8() else 0

    PSSDBV1 = PSSDBV9[:21]
    if PSSDBV1 == "EIGHT AND ONE FOURTH ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[21:]
        return 8.25 if check_8() else 0

    PSSDBV1 = PSSDBV9[:21]
    if PSSDBV1 == "EIGHT AND ONE-FOURTH ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[21:]
        return 8.25 if check_8() else 0

    PSSDBV1 = PSSDBV9[:17]
    if PSSDBV1 == "8 AND ONE FOURTH ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[17:]
        return 8.25 if check_8() else 0

    PSSDBV1 = PSSDBV9[:17]
    if PSSDBV1 == "8 AND ONE-FOURTH ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[17:]
        return 8.25 if check_8() else 0

    PSSDBV1 = PSSDBV9[:14]
    if PSSDBV1 == "EIGHT AND 1/4 ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[14:]
        return 8.25 if check_8() else 0

    PSSDBV1 = PSSDBV9[:10]
    if PSSDBV1 == "8 AND 1/3 ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[10:]
        return 8.33 if check_8() else 0

    PSSDBV1 = PSSDBV9[:20]
    if PSSDBV1 == "EIGHT AND ONE THIRD ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[20:]
        return 8.33 if check_8() else 0

    PSSDBV1 = PSSDBV9[:20]
    if PSSDBV1 == "EIGHT AND ONE-THIRD ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[20:]
        return 8.33 if check_8() else 0

    PSSDBV1 = PSSDBV9[:16]
    if PSSDBV1 == "8 AND ONE THIRD ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[16:]
        return 8.33 if check_8() else 0

    PSSDBV1 = PSSDBV9[:16]
    if PSSDBV1 == "8 AND ONE-THIRD ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[16:]
        return 8.33 if check_8() else 0

    PSSDBV1 = PSSDBV9[:14]
    if PSSDBV1 == "EIGHT AND 1/3 ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[14:]
        return 8.33 if check_8() else 0

    PSSDBV1 = PSSDBV9[:10]
    if PSSDBV1 == "8 AND 1/2 ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[10:]
        return 8.5 if check_8() else 0

    PSSDBV1 = PSSDBV9[:19]
    if PSSDBV1 == "EIGHT AND ONE HALF ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[19:]
        return 8.5 if check_8() else 0

    PSSDBV1 = PSSDBV9[:19]
    if PSSDBV1 == "EIGHT AND ONE-HALF ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[19:]
        return 8.5 if check_8() else 0

    PSSDBV1 = PSSDBV9[:15]
    if PSSDBV1 == "8 AND ONE HALF ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[15:]
        return 8.5 if check_8() else 0

    PSSDBV1 = PSSDBV9[:15]
    if PSSDBV1 == "8 AND ONE-HALF ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[15:]
        return 8.5 if check_8() else 0

    PSSDBV1 = PSSDBV9[:14]
    if PSSDBV1 == "EIGHT AND 1/2 ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[14:]
        return 8.5 if check_8() else 0

    PSSDBV1 = PSSDBV9[:4]
    if PSSDBV1 == "8-9 ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[4:]
        return 9 if check_8() else 0

    PSSDBV1 = PSSDBV9[:6]
    if PSSDBV1 == "8 - 9 ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[6:]
        return 9 if check_8() else 0

    PSSDBV1 = PSSDBV9[:7]
    if PSSDBV1 == "8 TO 9 ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[7:]
        return 9 if check_8() else 0

    PSSDBV1 = PSSDBV9[:7]
    if PSSDBV1 == "8 OR 9 ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[7:]
        return 9 if check_8() else 0

    PSSDBV1 = PSSDBV9[:14]
    if PSSDBV1 == "EIGHT TO NINE ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[14:]
        return 9 if check_8() else 0

    PSSDBV1 = PSSDBV9[:14]
    if PSSDBV1 == "EIGHT OR NINE ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[14:]
        return 9 if check_8() else 0

    PSSDBV1 = PSSDBV9[:11]
    if PSSDBV1 == "EIGHT-NINE ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[11:]
        return 9 if check_8() else 0

    PSSDBV1 = PSSDBV9[:13]
    if PSSDBV1 == "EIGHT - NINE ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[13:]
        return 9 if check_8() else 0

    PSSDBV1 = PSSDBV9[:2]
    if PSSDBV1 == "9 " and check_4():
        PSSDBV2 = PSSDBV9[2:]
        if check_8():
            return 9

    PSSDBV1 = PSSDBV9[:5]
    if PSSDBV1 == "NINE " and check_4():
        PSSDBV2 = PSSDBV9[5:]
        if check_8():
            return 9

    PSSDBV1 = PSSDBV9[:10]
    if PSSDBV1 == "9 AND 1/4 ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[10:]
        return 9.25 if check_8() else 0

    PSSDBV1 = PSSDBV9[:20]
    if PSSDBV1 == "NINE AND ONE FOURTH ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[20:]
        return 9.25 if check_8() else 0

    PSSDBV1 = PSSDBV9[:20]
    if PSSDBV1 == "NINE AND ONE-FOURTH ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[20:]
        return 9.25 if check_8() else 0

    PSSDBV1 = PSSDBV9[:17]
    if PSSDBV1 == "9 AND ONE FOURTH ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[17:]
        return 9.25 if check_8() else 0

    PSSDBV1 = PSSDBV9[:17]
    if PSSDBV1 == "9 AND ONE-FOURTH ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[17:]
        return 9.25 if check_8() else 0

    PSSDBV1 = PSSDBV9[:13]
    if PSSDBV1 == "NINE AND 1/4 ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[13:]
        return 9.25 if check_8() else 0

    PSSDBV1 = PSSDBV9[:10]
    if PSSDBV1 == "9 AND 1/3 ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[10:]
        return 9.33 if check_8() else 0

    PSSDBV1 = PSSDBV9[:20]
    if PSSDBV1 == "NINE AND ONE THIRD ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[20:]
        return 9.33 if check_8() else 0

    PSSDBV1 = PSSDBV9[:20]
    if PSSDBV1 == "NINE AND ONE-THIRD ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[20:]
        return 9.33 if check_8() else 0

    PSSDBV1 = PSSDBV9[:17]
    if PSSDBV1 == "10 AND ONE THIRD ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[17:]
        return 9.33 if check_8() else 0

    PSSDBV1 = PSSDBV9[:17]
    if PSSDBV1 == "10 AND ONE-THIRD ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[17:]
        return 9.33 if check_8() else 0

    PSSDBV1 = PSSDBV9[:13]
    if PSSDBV1 == "NINE AND 1/3 ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[13:]
        return 9.33 if check_8() else 0

    PSSDBV1 = PSSDBV9[:10]
    if PSSDBV1 == "9 AND 1/2 ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[10:]
        return 9.5 if check_8() else 0

    PSSDBV1 = PSSDBV9[:19]
    if PSSDBV1 == "NINE AND ONE HALF ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[19:]
        return 9.5 if check_8() else 0

    PSSDBV1 = PSSDBV9[:19]
    if PSSDBV1 == "NINE AND ONE-HALF ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[19:]
        return 9.5 if check_8() else 0

    PSSDBV1 = PSSDBV9[:15]
    if PSSDBV1 == "9 AND ONE HALF ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[15:]
        return 9.5 if check_8() else 0

    PSSDBV1 = PSSDBV9[:15]
    if PSSDBV1 == "9 AND ONE-HALF ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[15:]
        return 9.5 if check_8() else 0

    PSSDBV1 = PSSDBV9[:14]
    if PSSDBV1 == "NINE AND 1/2 ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[14:]
        return 9.5 if check_8() else 0

    PSSDBV1 = PSSDBV9[:4]
    if PSSDBV1 == "8-9 ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[4:]
        return 9 if check_8() else 0

    PSSDBV1 = PSSDBV9[:6]
    if PSSDBV1 == "8 - 9 ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[6:]
        return 9 if check_8() else 0

    PSSDBV1 = PSSDBV9[:7]
    if PSSDBV1 == "8 TO 9 ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[7:]
        return 9 if check_8() else 0

    PSSDBV1 = PSSDBV9[:7]
    if PSSDBV1 == "8 OR 9 ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[7:]
        return 9 if check_8() else 0

    PSSDBV1 = PSSDBV9[:14]
    if PSSDBV1 == "EIGHT TO NINE ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[14:]
        return 9 if check_8() else 0

    PSSDBV1 = PSSDBV9[:14]
    if PSSDBV1 == "EIGHT OR NINE ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[14:]
        return 9 if check_8() else 0

    PSSDBV1 = PSSDBV9[:11]
    if PSSDBV1 == "EIGHT-NINE ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[11:]
        return 9 if check_8() else 0

    PSSDBV1 = PSSDBV9[:13]
    if PSSDBV1 == "EIGHT - NINE ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[13:]
        return 9 if check_8() else 0

    PSSDBV1 = PSSDBV9[:2]
    if PSSDBV1 == "9 " and check_4():
        PSSDBV2 = PSSDBV9[2:]
        if check_8():
            return 9

    PSSDBV1 = PSSDBV9[:5]
    if PSSDBV1 == "NINE " and check_4():
        PSSDBV2 = PSSDBV9[5:]
        if check_8():
            return 9

    PSSDBV1 = PSSDBV9[:10]
    if PSSDBV1 == "9 AND 1/4 ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[10:]
        return 9.25 if check_8() else 0

    PSSDBV1 = PSSDBV9[:20]
    if PSSDBV1 == "NINE AND ONE FOURTH ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[20:]
        return 9.25 if check_8() else 0

    PSSDBV1 = PSSDBV9[:20]
    if PSSDBV1 == "NINE AND ONE-FOURTH ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[20:]
        return 9.25 if check_8() else 0

    PSSDBV1 = PSSDBV9[:18]
    if PSSDBV1 == "10 AND ONE FOURTH ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[18:]
        return 9.25 if check_8() else 0

    PSSDBV1 = PSSDBV9[:18]
    if PSSDBV1 == "10 AND ONE-FOURTH ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[18:]
        return 9.25 if check_8() else 0

    PSSDBV1 = PSSDBV9[:12]
    if PSSDBV1 == "TEN AND 1/4 ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[12:]
        return 10.25 if check_8() else 0

    PSSDBV1 = PSSDBV9[:19]
    if PSSDBV1 == "TEN AND ONE FOURTH ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[19:]
        return 10.25 if check_8() else 0

    PSSDBV1 = PSSDBV9[:19]
    if PSSDBV1 == "TEN AND ONE-FOURTH ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[19:]
        return 10.25 if check_8() else 0

    PSSDBV1 = PSSDBV9[:17]
    if PSSDBV1 == "10 AND ONE FOURTH ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[17:]
        return 10.25 if check_8() else 0

    PSSDBV1 = PSSDBV9[:17]
    if PSSDBV1 == "10 AND ONE-FOURTH ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[17:]
        return 10.25 if check_8() else 0

    PSSDBV1 = PSSDBV9[:12]
    if PSSDBV1 == "TEN AND 1/4 ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[12:]
        return 10.25 if check_8() else 0

    PSSDBV1 = PSSDBV9[:11]
    if PSSDBV1 == "10 AND 1/3 ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[11:]
        return 10.33 if check_8() else 0

    PSSDBV1 = PSSDBV9[:18]
    if PSSDBV1 == "TEN AND ONE THIRD ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[18:]
        return 10.33 if check_8() else 0

    PSSDBV1 = PSSDBV9[:18]
    if PSSDBV1 == "TEN AND ONE-THIRD ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[18:]
        return 10.33 if check_8() else 0

    PSSDBV1 = PSSDBV9[:17]
    if PSSDBV1 == "10 AND ONE THIRD ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[17:]
        return 10.33 if check_8() else 0

    PSSDBV1 = PSSDBV9[:17]
    if PSSDBV1 == "10 AND ONE-THIRD ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[17:]
        return 10.33 if check_8() else 0

    PSSDBV1 = PSSDBV9[:13]
    if PSSDBV1 == "TEN AND 1/3 ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[13:]
        return 10.33 if check_8() else 0

    PSSDBV1 = PSSDBV9[:11]
    if PSSDBV1 == "10 AND 1/2 ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[11:]
        return 10.5 if check_8() else 0

    PSSDBV1 = PSSDBV9[:17]
    if PSSDBV1 == "TEN AND ONE HALF ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[17:]
        return 10.5 if check_8() else 0

    PSSDBV1 = PSSDBV9[:17]
    if PSSDBV1 == "TEN AND ONE-HALF ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[17:]
        return 10.5 if check_8() else 0

    PSSDBV1 = PSSDBV9[:16]
    if PSSDBV1 == "10 AND ONE HALF ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[16:]
        return 10.5 if check_8() else 0

    PSSDBV1 = PSSDBV9[:16]
    if PSSDBV1 == "10 AND ONE-HALF ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[16:]
        return 10.5 if check_8() else 0

    PSSDBV1 = PSSDBV9[:12]
    if PSSDBV1 == "TEN AND 1/2 ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[12:]
        return 10.5 if check_8() else 0

    PSSDBV1 = PSSDBV9[:4]
    if PSSDBV1 == "10 " and check_4():
        PSSDBV2 = PSSDBV9[4:]
        if check_8():
            return 10

    PSSDBV1 = PSSDBV9[:5]
    if PSSDBV1 == "TEN " and check_4():
        PSSDBV2 = PSSDBV9[5:]
        if check_8():
            return 10

    PSSDBV1 = PSSDBV9[:11]
    if PSSDBV1 == "10 AND 1/4 ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[11:]
        return 10.25 if check_8() else 0

    PSSDBV1 = PSSDBV9[:19]
    if PSSDBV1 == "TEN AND ONE FOURTH ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[19:]
        return 10.25 if check_8() else 0

    PSSDBV1 = PSSDBV9[:19]
    if PSSDBV1 == "TEN AND ONE-FOURTH ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[19:]
        return 10.25 if check_8() else 0

    PSSDBV1 = PSSDBV9[:18]
    if PSSDBV1 == "10 AND ONE FOURTH ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[18:]
        return 10.25 if check_8() else 0

    PSSDBV1 = PSSDBV9[:18]
    if PSSDBV1 == "10 AND ONE-FOURTH ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[18:]
        return 10.25 if check_8() else 0

    PSSDBV1 = PSSDBV9[:12]
    if PSSDBV1 == "TEN AND 1/4 ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[12:]
        return 10.25 if check_8() else 0

    PSSDBV1 = PSSDBV9[:11]
    if PSSDBV1 == "10 AND 1/3 ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[11:]
        return 10.33 if check_8() else 0

    PSSDBV1 = PSSDBV9[:18]
    if PSSDBV1 == "TEN AND ONE THIRD ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[18:]
        return 10.33 if check_8() else 0

    PSSDBV1 = PSSDBV9[:18]
    if PSSDBV1 == "TEN AND ONE-THIRD ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[18:]
        return 10.33 if check_8() else 0

    PSSDBV1 = PSSDBV9[:17]
    if PSSDBV1 == "10 AND ONE THIRD ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[17:]
        return 10.33 if check_8() else 0

    PSSDBV1 = PSSDBV9[:17]
    if PSSDBV1 == "10 AND ONE-THIRD ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[17:]
        return 10.33 if check_8() else 0

    PSSDBV1 = PSSDBV9[:13]
    if PSSDBV1 == "TEN AND 1/3 ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[13:]
        return 10.33 if check_8() else 0

    PSSDBV1 = PSSDBV9[:11]
    if PSSDBV1 == "10 AND 1/2 ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[11:]
        return 10.5 if check_8() else 0

    PSSDBV1 = PSSDBV9[:17]
    if PSSDBV1 == "TEN AND ONE HALF ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[17:]
        return 10.5 if check_8() else 0

    PSSDBV1 = PSSDBV9[:17]
    if PSSDBV1 == "TEN AND ONE-HALF ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[17:]
        return 10.5 if check_8() else 0

    PSSDBV1 = PSSDBV9[:16]
    if PSSDBV1 == "10 AND ONE HALF ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[16:]
        return 10.5 if check_8() else 0

    PSSDBV1 = PSSDBV9[:16]
    if PSSDBV1 == "10 AND ONE-HALF ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[16:]
        return 10.5 if check_8() else 0

    PSSDBV1 = PSSDBV9[:12]
    if PSSDBV1 == "TEN AND 1/2 ":
        if not check_4():
            return 0
        PSSDBV2 = PSSDBV9[12:]
        return 10.5 if check_8() else 0

    return ""

def check_8():
    PSSDBV3 = ""
    if PSSDBIFL:
        PSSDBV3 = UNITD(PSSDBV2)
    else:
        PSSDBV3 = UNIT(PSSDBV2)
    return False if PSSDBV3 == "" else True

def check_4():
    if len(PSSDBV9) <= len(PSSDBV1):
        return 0
    return 1