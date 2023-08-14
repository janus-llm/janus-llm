def NUMF():
    PSSDBV1 = PSSDBV9[:11]
    if PSSDBV1 == "ONE FOURTH ":
        if not check_7():
            return 0
        PSSDBV2 = PSSDBV9[11:]
        return .25 if check_8() else 0
    
    PSSDBV1 = PSSDBV9[:11]
    if PSSDBV1 == "ONE-FOURTH ":
        if not check_7():
            return 0
        PSSDBV2 = PSSDBV9[11:]
        return .25 if check_8() else 0
    
    PSSDBV1 = PSSDBV9[:4]
    if PSSDBV1 == "1/4 ":
        if not check_7():
            return 0
        PSSDBV2 = PSSDBV9[4:]
        return .25 if check_8() else 0
    
    PSSDBV1 = PSSDBV9[:5]
    if PSSDBV1 == "0.25 ":
        if not check_7():
            return 0
        PSSDBV2 = PSSDBV9[5:]
        return .25 if check_8() else 0
    
    PSSDBV1 = PSSDBV9[:10]
    if PSSDBV1 == "ONE THIRD ":
        if not check_7():
            return 0
        PSSDBV2 = PSSDBV9[10:]
        return .33 if check_8() else 0
    
    PSSDBV1 = PSSDBV9[:10]
    if PSSDBV1 == "ONE-THIRD ":
        if not check_7():
            return 0
        PSSDBV2 = PSSDBV9[10:]
        return .33 if check_8() else 0
    
    PSSDBV1 = PSSDBV9[:4]
    if PSSDBV1 == "1/3 ":
        if not check_7():
            return 0
        PSSDBV2 = PSSDBV9[4:]
        return .33 if check_8() else 0
    
    PSSDBV1 = PSSDBV9[:5]
    if PSSDBV1 == "0.33 ":
        if not check_7():
            return 0
        PSSDBV2 = PSSDBV9[5:]
        return .33 if check_8() else 0
    
    PSSDBV1 = PSSDBV9[:9]
    if PSSDBV1 == "ONE HALF " and check_7():
        PSSDBV2 = PSSDBV9[9:]
        return .5 if check_8() else 0
    
    PSSDBV1 = PSSDBV9[:9]
    if PSSDBV1 == "ONE-HALF " and check_7():
        PSSDBV2 = PSSDBV9[9:]
        return .5 if check_8() else 0
    
    PSSDBV1 = PSSDBV9[:4]
    if PSSDBV1 == "1/2 " and check_7():
        PSSDBV2 = PSSDBV9[4:]
        return .5 if check_8() else 0
    
    PSSDBV1 = PSSDBV9[:4]
    if PSSDBV1 == "0.5 " and check_7():
        PSSDBV2 = PSSDBV9[4:]
        return .5 if check_8() else 0
    
    PSSDBV1 = PSSDBV9[:6]
    if PSSDBV1 == "0.5-1 ":
        if not check_7():
            return 0
        PSSDBV2 = PSSDBV9[6:]
        return 1 if check_8() else 0
    
    PSSDBV1 = PSSDBV9[:8]
    if PSSDBV1 == "0.5 - 1 ":
        if not check_7():
            return 0
        PSSDBV2 = PSSDBV9[8:]
        return 1 if check_8() else 0
    
    PSSDBV1 = PSSDBV9[:9]
    if PSSDBV1 == "0.5 TO 1 ":
        if not check_7():
            return 0
        PSSDBV2 = PSSDBV9[9:]
        return 1 if check_8() else 0
    
    PSSDBV1 = PSSDBV9[:9]
    if PSSDBV1 == "0.5 OR 1 ":
        if not check_7():
            return 0
        PSSDBV2 = PSSDBV9[9:]
        return 1 if check_8() else 0
    
    PSSDBV1 = PSSDBV9[:6]
    if PSSDBV1 == "1/2-1 ":
        if not check_7():
            return 0
        PSSDBV2 = PSSDBV9[6:]
        return 1 if check_8() else 0
    
    PSSDBV1 = PSSDBV9[:8]
    if PSSDBV1 == "1/2 - 1 ":
        if not check_7():
            return 0
        PSSDBV2 = PSSDBV9[8:]
        return 1 if check_8() else 0
    
    PSSDBV1 = PSSDBV9[:9]
    if PSSDBV1 == "1/2 TO 1 ":
        if not check_7():
            return 0
        PSSDBV2 = PSSDBV9[9:]
        return 1 if check_8() else 0
    
    PSSDBV1 = PSSDBV9[:9]
    if PSSDBV1 == "1/2 OR 1 ":
        if not check_7():
            return 0
        PSSDBV2 = PSSDBV9[9:]
        return 1 if check_8() else 0
    
    PSSDBV1 = PSSDBV9[:16]
    if PSSDBV1 == "ONE-HALF TO ONE ":
        if not check_7():
            return 0
        PSSDBV2 = PSSDBV9[16:]
        return 1 if check_8() else 0
    
    PSSDBV1 = PSSDBV9[:18]
    if PSSDBV1 == "ONE - HALF TO ONE ":
        if not check_7():
            return 0
        PSSDBV2 = PSSDBV9[18:]
        return 1 if check_8() else 0
    
    PSSDBV1 = PSSDBV9[:16]
    if PSSDBV1 == "ONE HALF TO ONE ":
        if not check_7():
            return 0
        PSSDBV2 = PSSDBV9[16:]
        return 1 if check_8() else 0
    
    PSSDBV1 = PSSDBV9[:16]
    if PSSDBV1 == "ONE-HALF OR ONE ":
        if not check_7():
            return 0
        PSSDBV2 = PSSDBV9[16:]
        return 1 if check_8() else 0
    
    PSSDBV1 = PSSDBV9[:18]
    if PSSDBV1 == "ONE - HALF OR ONE ":
        if not check_7():
            return 0
        PSSDBV2 = PSSDBV9[18:]
        return 1 if check_8() else 0
    
    PSSDBV1 = PSSDBV9[:16]
    if PSSDBV1 == "ONE HALF OR ONE ":
        if not check_7():
            return 0
        PSSDBV2 = PSSDBV9[16:]
        return 1 if check_8() else 0
    
    PSSDBV1 = PSSDBV9[:2]
    if PSSDBV1 == "1 " and check_7():
        PSSDBV2 = PSSDBV9[2:]
        return 1 if check_8() else 0
    
    PSSDBV1 = PSSDBV9[:4]
    if PSSDBV1 == "ONE " and check_7():
        PSSDBV2 = PSSDBV9[4:]
        return 1 if check_8() else 0
    
    PSSDBV1 = PSSDBV9[:10]
    if PSSDBV1 == "1 AND 1/4 ":
        if not check_7():
            return 0
        PSSDBV2 = PSSDBV9[10:]
        return 1.25 if check_8() else 0
    
    PSSDBV1 = PSSDBV9[:19]
    if PSSDBV1 == "ONE AND ONE FOURTH ":
        if not check_7():
            return 0
        PSSDBV2 = PSSDBV9[19:]
        return 1.25 if check_8() else 0
    
    PSSDBV1 = PSSDBV9[:19]
    if PSSDBV1 == "ONE AND ONE-FOURTH ":
        if not check_7():
            return 0
        PSSDBV2 = PSSDBV9[19:]
        return 1.25 if check_8() else 0
    
    PSSDBV1 = PSSDBV9[:17]
    if PSSDBV1 == "1 AND ONE FOURTH ":
        if not check_7():
            return 0
        PSSDBV2 = PSSDBV9[17:]
        return 1.25 if check_8() else 0
    
    PSSDBV1 = PSSDBV9[:17]
    if PSSDBV1 == "1 AND ONE-FOURTH ":
        if not check_7():
            return 0
        PSSDBV2 = PSSDBV9[17:]
        return 1.25 if check_8() else 0
    
    PSSDBV1 = PSSDBV9[:12]
    if PSSDBV1 == "ONE AND 1/4 ":
        if not check_7():
            return 0
        PSSDBV2 = PSSDBV9[12:]
        return 1.25 if check_8() else 0
    
    PSSDBV1 = PSSDBV9[:10]
    if PSSDBV1 == "1 AND 1/3 ":
        if not check_7():
            return 0
        PSSDBV2 = PSSDBV9[10:]
        return 1.33 if check_8() else 0
    
    PSSDBV1 = PSSDBV9[:18]
    if PSSDBV1 == "ONE AND ONE THIRD ":
        if not check_7():
            return 0
        PSSDBV2 = PSSDBV9[18:]
        return 1.33 if check_8() else 0
    
    PSSDBV1 = PSSDBV9[:18]
    if PSSDBV1 == "ONE AND ONE-THIRD ":
        if not check_7():
            return 0
        PSSDBV2 = PSSDBV9[18:]
        return 1.33 if check_8() else 0
    
    PSSDBV1 = PSSDBV9[:16]
    if PSSDBV1 == "1 AND ONE THIRD ":
        if not check_7():
            return 0
        PSSDBV2 = PSSDBV9[16:]
        return 1.33 if check_8() else 0
    
    PSSDBV1 = PSSDBV9[:16]
    if PSSDBV1 == "1 AND ONE-THIRD ":
        if not check_7():
            return 0
        PSSDBV2 = PSSDBV9[16:]
        return 1.33 if check_8() else 0
    
    PSSDBV1 = PSSDBV9[:12]
    if PSSDBV1 == "ONE AND 1/3 ":
        if not check_7():
            return 0
        PSSDBV2 = PSSDBV9[12:]
        return 1.33 if check_8() else 0
    
    PSSDBV1 = PSSDBV9[:10]
    if PSSDBV1 == "1 AND 1/2 ":
        if not check_7():
            return 0
        PSSDBV2 = PSSDBV9[10:]
        return 1.5 if check_8() else 0
    
    PSSDBV1 = PSSDBV9[:17]
    if PSSDBV1 == "ONE AND ONE HALF ":
        if not check_7():
            return 0
        PSSDBV2 = PSSDBV9[17:]
        return 1.5 if check_8() else 0
    
    PSSDBV1 = PSSDBV9[:17]
    if PSSDBV1 == "ONE AND ONE-HALF ":
        if not check_7():
            return 0
        PSSDBV2 = PSSDBV9[17:]
        return 1.5 if check_8() else 0
    
    PSSDBV1 = PSSDBV9[:15]
    if PSSDBV1 == "1 AND ONE HALF ":
        if not check_7():
            return 0
        PSSDBV2 = PSSDBV9[15:]
        return 1.5 if check_8() else 0
    
    PSSDBV1 = PSSDBV9[:15]
    if PSSDBV1 == "1 AND ONE-HALF ":
        if not check_7():
            return 0
        PSSDBV2 = PSSDBV9[15:]
        return 1.5 if check_8() else 0
    
    PSSDBV1 = PSSDBV9[:12]
    if PSSDBV1 == "ONE AND 1/2 ":
        if not check_7():
            return 0
        PSSDBV2 = PSSDBV9[12:]
        return 1.5 if check_8() else 0
    
    PSSDBV1 = PSSDBV9[:4]
    if PSSDBV1 == "1-2 ":
        if not check_7():
            return 0
        PSSDBV2 = PSSDBV9[4:]
        return 2 if check_8() else 0
    
    PSSDBV1 = PSSDBV9[:6]
    if PSSDBV1 == "1 - 2 ":
        if not check_7():
            return 0
        PSSDBV2 = PSSDBV9[6:]
        return 2 if check_8() else 0
    
    PSSDBV1 = PSSDBV9[:7]
    if PSSDBV1 == "1 TO 2 ":
        if not check_7():
            return 0
        PSSDBV2 = PSSDBV9[7:]
        return 2 if check_8() else 0
    
    PSSDBV1 = PSSDBV9[:7]
    if PSSDBV1 == "1 OR 2 ":
        if not check_7():
            return 0
        PSSDBV2 = PSSDBV9[7:]
        return 2 if check_8() else 0
    
    PSSDBV1 = PSSDBV9[:11]
    if PSSDBV1 == "ONE TO TWO ":
        if not check_7():
            return 0
        PSSDBV2 = PSSDBV9[11:]
        return 2 if check_8() else 0
    
    PSSDBV1 = PSSDBV9[:11]
    if PSSDBV1 == "ONE OR TWO ":
        if not check_7():
            return 0
        PSSDBV2 = PSSDBV9[11:]
        return 2 if check_8() else 0
    
    PSSDBV1 = PSSDBV9[:8]
    if PSSDBV1 == "ONE-TWO ":
        if not check_7():
            return 0
        PSSDBV2 = PSSDBV9[8:]
        return 2 if check_8() else 0
# <<<child_1>>>
# <<<child_2>>>
# <<<child_3>>>