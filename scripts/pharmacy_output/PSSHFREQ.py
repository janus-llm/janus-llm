def valfreq(freq):
    freq = trim(freq)

    if freq == "":
        return 0

    freq = upper(freq)

    if "." in freq:
        return 0
    if freq.isdigit():
        return 1

    result = smplfreq(freq)
    if result == 1:
        return result

    pss = {}
    pss["length"] = len(freq)
    pss["firstCharacter"] = freq[0]
    pss["lastCharacter"] = freq[-1]

    if pss["length"] > 4:
        return 0
    if pss["length"] < 3:
        return 0
    if pss["firstCharacter"] not in ["Q", "X"]:
        return 0

    pss["result"] = 1
    if pss["length"] == 4:
        chrTemp1 = freq[1]
        chrTemp2 = freq[2]
        intTemp1 = ord(chrTemp1) - 48
        intTemp2 = ord(chrTemp2) - 48

        if intTemp1 < 0:
            pss["result"] = 0
        if intTemp1 > 9:
            pss["result"] = 0
        if intTemp2 < 0:
            pss["result"] = 0
        if intTemp2 > 9:
            pss["result"] = 0

    if pss["length"] == 3:
        chrTemp1 = freq[1]
        intTemp1 = ord(chrTemp1) - 48

        if intTemp1 < 0:
            pss["result"] = 0
        if intTemp1 > 9:
            pss["result"] = 0

    if pss["result"] == 0:
        return 0

    qResult = ""
    if pss["firstCharacter"] == "Q":
        if pss["lastCharacter"] in ["D", "W", "L", "H"]:
            qResult = 1

    if qResult != "":
        return qResult

    xResult = ""
    if pss["firstCharacter"] == "X":
        if pss["lastCharacter"] in ["D", "W", "L"]:
            xResult = 1

    if xResult != "":
        return xResult

    return 0


def smplfreq(freq):
    validFreqs = {
        "QD": "",
        "BID": "",
        "TID": "",
        "QID": "",
        "QAM": "",
        "QSHIFT": "",
        "QOD": "",
        "QHS": "",
        "QPM": "",
    }

    if freq in validFreqs:
        return 1

    return 0


def trim(text):
    text = trimlead(text)
    text = trimend(text)
    return text


def trimlead(text):
    length = len(text)

    if length == 0:
        return text

    flag = 0
    for i in range(length):
        char = text[i]
        if char == " ":
            tempText = text[i+1:]
            mod = 1
        if char != " ":
            flag = 1
            break

    if flag == 1:
        return text
    if mod == 1:
        return tempText


def trimend(text):
    length = len(text)

    if length == 0:
        return text

    flag = 0
    for i in range(length, 0, -1):
        char = text[i-1]
        if char == " ":
            tempText = text[:i-1]
            mod = 1
        if char != " ":
            flag = 1
            break

    if flag == 1:
        return text
    if mod == 1:
        return tempText


def upper(text):
    lower = "abcdefghijklmnopqrstuvwxyz"
    upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    text = text.translate(str.maketrans(lower, upper))

    return text