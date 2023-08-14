def DRGNTCK(DOCHAND, NODE, BASE):
    # Handles the drugsNotChecked section
    # DOCHAND: Handle to XML document
    # NODE: Node associated with XML element
    # BASE: Base of output global
    # RETURNS: Nothing
    HASH = {}
    # Read error into hash variable
    NOTREAD(DOCHAND, NODE, HASH)
    # Write hashed variable to output global
    NOTWRITE(HASH, BASE)

def NOTREAD(DOCHAND, NODE, HASH):
    # Handles reading drugsNotChecked section of the XML document
    # DOCHAND: Handle to XML document
    # NODE: Node associated with drugsNotChecked XML element
    # HASH: ByRef, Hash used to store response
    # RETURNS: Variables in hash
    PSS = {"child": 0, "count": 0}
    while True:
        PSS["child"] = CHILD(DOCHAND, NODE, PSS["child"])
        if PSS["child"] < 1:
            break
        HASH[PSS["count"], "reason"] = VALUE(DOCHAND, PSS["child"], "status")
        HASH[PSS["count"], "reasonCode"] = ""
        HASH[PSS["count"], "reasonText"] = ""
        HASH[PSS["count"], "reasonSource"] = "PEPS"  # Always PEPS if returned from XML
        # Get drug element of drugNotChecked
        # No need to iterate over drug subelements because only 1 possible
        PARSEDRG(DOCHAND, CHILD(DOCHAND, PSS["child"]), HASH, PSS["count"])
        PSS["count"] += 1

def NOTWRITE(HASH, BASE):
    # Handles writing drugsNotChecked section of the XML document and
    # drugs pulled by validation logic as uncheckable (i.e. no gcn).
    # HASH: ByRef, Hash used to store response
    # BASE: Base of output global
    # RETURNS: Nothing. Stores values in output global.
    I = ""
    while I in HASH:
        PSS["PharmOrderNo"] = HASH[I, "orderNumber"]
        MESSAGE = GCNREASN(HASH[I, "ien"], HASH[I, "drugName"], HASH[I, "orderNumber"], 1)
        if int(MESSAGE.split("^")[2]) == 1:
            continue
        REASON = MESSAGE.split("^")[1]
        MESSAGE = MESSAGE.split("^")[0]
        DATASTR = "{}^{}_{}_{}_{}_{}_{}_{}_{}".format(
            HASH[I, "gcn"],
            HASH[I, "vuid"],
            HASH[I, "ien"],
            HASH[I, "drugName"],
            HASH[I, "cprsOrderNumber"],
            HASH[I, "package"],
            "",
            HASH[I, "reasonSource"],
            REASON,
        )
        TMP[J, BASE, "OUT", "EXCEPTIONS", HASH[I, "orderNumber"], NEXTEX(PSS, PSSHASH)] = DATASTR
        I += 1

def DRGDOSE(DOCHAND, NODE, BASE):
    # Handles the drugDoseChecks element
    # DOCHAND: Handle to XML document
    # NODE: Node associated with XML element
    # BASE: name to use for return global
    # RETURNS: Nothing
    PSS = {"child": 0, "doseCount": 0}
    PSMSGCNT = 0
    while True:
        PSS["child"] = CHILD(DOCHAND, NODE, PSS["child"])
        if PSS["child"] < 1:
            break
        PSS["childName"] = NAME(DOCHAND, PSS["child"])
        if PSS["childName"] == "message":
            PSMSGCNT += 1
            MSGREAD(DOCHAND, PSS["child"], MSGHASH, PSMSGCNT)
        elif PSS["childName"] == "drugDoseCheck":
            PSS["doseCount"] += 1
            DOSEREAD(DOCHAND, PSS["child"], DOSEHASH, PSS["doseCount"], MSGHASH, PSMSGCNT, BASE)

    MSGWRITE(MSGHASH, BASE, "DOSE")
    DOSEWRIT(DOSEHASH, BASE)

def MSGREAD(DOCHAND, NODE, HASH, COUNT):
    # Handles parsing message section
    # DOCHAND: Handle to XML document
    # NODE: Node associated with XML element
    # COUNT: Count of message sections
    # HASH: Where to store info
    # RETURNS: Nothing
    # Parse the message and store in hash
    PARSEMSG(DOCHAND, NODE, HASH, COUNT)

def DOSEREAD(DOCHAND, NODE, HASH, COUNT, MSGHASH, MSGCNT, BASE):
    # Reads in the drugDoseCheck XML element
    # DOCHAND: Handle to XML document
    # NODE: Node associated with XML element
    # BASE: Name for return array
    # MSGHASH: array of messages about drug
    # MSGCNT: a counter on the messages (they can occur at the drugDosechecks or drugDoseCheck level)
    # RETURNS: Nothing, values stored in hash
    PSS = {"messageCount": MSGCNT}
    # need drugname and drugien for return node, get them first
    PSS["child"] = 0
    while True:
        PSS["child"] = CHILD(DOCHAND, NODE, PSS["child"])
        if PSS["child"] < 1:
            break
        PSS["childName"] = NAME(DOCHAND, PSS["child"])
        if PSS["childName"] == "message":
            PSS["messageCount"] += 1
            MSGREAD(DOCHAND, PSS["child"], MSGHASH, PSS["messageCount"])
        elif PSS["childName"] == "drug":
            PARSEDRG(DOCHAND, PSS["child"], HASH, COUNT)
        elif PSS["childName"] == "singleDoseStatus":
            HASH[COUNT, "singleDoseStatus"] = GETTEXT(DOCHAND, PSS["child"])
        elif PSS["childName"] == "singleDoseStatusCode":
            HASH[COUNT, "singleDoseStatusCode"] = GETTEXT(DOCHAND, PSS["child"])
        elif PSS["childName"] == "singleDoseMessage":
            HASH[COUNT, "singleDoseMessage"] = GETTEXT(DOCHAND, PSS["child"])
            if HASH[COUNT, "singleDoseStatusCode"] == 5:
                MSG(HASH, COUNT, "S")
        elif PSS["childName"] == "singleDoseMax":
            HASH[COUNT, "singleDoseMax"] = GETTEXT(DOCHAND, PSS["child"])
        elif PSS["childName"] == "rangeDoseStatus":
            HASH[COUNT, "rangeDoseStatus"] = GETTEXT(DOCHAND, PSS["child"])
        elif PSS["childName"] == "rangeDoseStatusCode":
            HASH[COUNT, "rangeDoseStatusCode"] = GETTEXT(DOCHAND, PSS["child"])
        elif PSS["childName"] == "rangeDoseMessage":
            HASH[COUNT, "rangeDoseMessage"] = GETTEXT(DOCHAND, PSS["child"])
            if HASH[COUNT, "rangeDoseStatusCode"] == 5:
                MSG(HASH, COUNT, "R")
        elif PSS["childName"] == "rangeDoseLow":
            HASH[COUNT, "rangeDoseLow"] = GETTEXT(DOCHAND, PSS["child"])
        elif PSS["childName"] == "rangeDoseHigh":
            HASH[COUNT, "rangeDoseHigh"] = GETTEXT(DOCHAND, PSS["child"])
        elif PSS["childName"] == "doseHigh":
            HASH[COUNT, "doseHigh"] = GETTEXT(DOCHAND, PSS["child"])
        elif PSS["childName"] == "doseHighUnit":
            HASH[COUNT, "doseHighUnit"] = GETTEXT(DOCHAND, PSS["child"])
        elif PSS["childName"] == "doseLow":
            HASH[COUNT, "doseLow"] = GETTEXT(DOCHAND, PSS["child"])
        elif PSS["childName"] == "doseLowUnit":
            HASH[COUNT, "doseLowUnit"] = GETTEXT(DOCHAND, PSS["child"])
        elif PSS["childName"] == "doseRouteDescription":
            HASH[COUNT, "doseRouteDescription"] = GETTEXT(DOCHAND, PSS["child"])
            if HASH[COUNT, "doseRouteDescription"] == "":
                PSSNORTE = [6, 7, 31]
                for PSSNORTE in PSSNORTE:
                    PSSDBCAR(HASH[COUNT, "orderNumber"]) = 1
                PSSDBCAR(HASH[COUNT, "orderNumber"]) = " for " + PSSDBCAR(HASH[COUNT, "orderNumber"]) + " route: "
        elif PSS["childName"] == "doseFormHigh":
            HASH[COUNT, "doseFormHigh"] = GETTEXT(DOCHAND, PSS["child"])
        elif PSS["childName"] == "doseFormHighUnit":
            HASH[COUNT, "doseFormHighUnit"] = GETTEXT(DOCHAND, PSS["child"])
        elif PSS["childName"] == "doseFormLow":
            HASH[COUNT, "doseFormLow"] = GETTEXT(DOCHAND, PSS["child"])
        elif PSS["childName"] == "doseFormLowUnit":
            HASH[COUNT, "doseFormLowUnit"] = GETTEXT(DOCHAND, PSS["child"])
        elif PSS["childName"] == "chemoInjectable":
            HASH[COUNT, "chemoInjectable"] = GETTEXT(DOCHAND, PSS["child"])
        elif PSS["childName"] == "dailyDoseStatus":
            HASH[COUNT, "dailyDoseStatus"] = GETTEXT(DOCHAND, PSS["child"])
        elif PSS["childName"] == "dailyDoseStatusCode":
            HASH[COUNT, "dailyDoseStatusCode"] = GETTEXT(DOCHAND, PSS["child"])
        elif PSS["childName"] == "dailyDoseMessage":
            HASH[COUNT, "dailyDoseMessage"] = GETTEXT(DOCHAND, PSS["child"])
            if HASH[COUNT, "dailyDoseStatusCode"] == 5:
                MSG(HASH, COUNT, "D")
        elif PSS["childName"] == "maxDailyDoseStatus":
            HASH[COUNT, "maxDailyDoseStatus"] = GETTEXT(DOCHAND, PSS["child"])
        elif PSS["childName"] == "maxDailyDoseStatusCode":
            HASH[COUNT, "maxDailyDoseStatusCode"] = GETTEXT(DOCHAND, PSS["child"])
        elif PSS["childName"] == "maxDailyDoseMessage":
            HASH[COUNT, "maxDailyDoseMessage"] = GETTEXT(DOCHAND, PSS["child"])
            if HASH[COUNT, "maxDailyDoseStatusCode"] == 5:
                MSG(HASH, COUNT, "M")
        elif PSS["childName"] == "maxLifetimeDose":
            HASH[COUNT, "maxLifetimeDose"] = GETTEXT(DOCHAND, PSS["child"])
        elif PSS["childName"] == "frequencyStatus":
            HASH[COUNT, "frequencyStatus"] = GETTEXT(DOCHAND, PSS["child"])
        elif PSS["childName"] == "frequencyStatusCode":
            HASH[COUNT, "frequencyStatusCode"] = GETTEXT(DOCHAND, PSS["child"])
        elif PSS["childName"] == "frequencyMessage":
            HASH[COUNT, "frequencyMessage"] = GETTEXT(DOCHAND, PSS["child"])
        elif PSS["childName"] == "frequencyHigh":
            HASH[COUNT, "frequencyHigh"] = GETTEXT(DOCHAND, PSS["child"])
        elif PSS["childName"] == "frequencyLow":
            HASH[COUNT, "frequencyLow"] = GETTEXT(DOCHAND, PSS["child"])
        elif PSS["childName"] == "maxLifetimeOrderMessage":
            HASH[COUNT, "maxLifetimeOrderMessage"] = GETTEXT(DOCHAND, PSS["child"])
        elif PSS["childName"] == "maxLifetimeOrderStatus":
            HASH[COUNT, "maxLifetimeOrderStatus"] = GETTEXT(DOCHAND, PSS["child"])
        elif PSS["childName"] == "maxLifetimeOrderStatusCode":
            HASH[COUNT, "maxLifetimeOrderStatusCode"] = GETTEXT(DOCHAND, PSS["child"])
        elif PSS["childName"] == "maxSingleNTEDose":
            HASH[COUNT, "maxSingleNTEDose"] = GETTEXT(DOCHAND, PSS["child"])
        elif PSS["childName"] == "maxSingleNTEDoseUnit":
            HASH[COUNT, "maxSingleNTEDoseUnit"] = GETTEXT(DOCHAND, PSS["child"])
        elif PSS["childName"] == "maxSingleNTEDoseForm":
            HASH[COUNT, "maxSingleNTEDoseForm"] = GETTEXT(DOCHAND, PSS["child"])
        elif PSS["childName"] == "maxSingleNTEDoseFormUnit":
            HASH[COUNT, "maxSingleNTEDoseFormUnit"] = GETTEXT(DOCHAND, PSS["child"])
        elif PSS["childName"] == "maxDailyDose":
            HASH[COUNT, "maxDailyDose"] = GETTEXT(DOCHAND, PSS["child"])
        elif PSS["childName"] == "maxDailyDoseUnit":
            HASH[COUNT, "maxDailyDoseUnit"] = GETTEXT(DOCHAND, PSS["child"])
        elif PSS["childName"] == "maxDailyDoseForm":
            HASH[COUNT, "maxDailyDoseForm"] = GETTEXT(DOCHAND, PSS["child"])
        elif PSS["childName"] == "maxDailyDoseFormUnit":
            HASH[COUNT, "maxDailyDoseFormUnit"] = GETTEXT(DOCHAND, PSS["child"])
    if HASH[COUNT, "orderNumber"]:
        if not PSSDBCAR[HASH[COUNT, "orderNumber"]]:
            if HASH[COUNT, "maxDailyDoseStatusCode"] == 5 and "frequency check failed" in HASH[COUNT, "maxDailyDoseMessage"]:
                PSSDBCAR[HASH[COUNT, "orderNumber"]] = 1
        if not PSSDBCAR[HASH[COUNT, "orderNumber"]]:
            if HASH[COUNT, "frequencyLow"] <= 0 or HASH[COUNT, "frequencyHigh"] <= 0:
                return
            PSSOFREQ = ORDFREQ(PSSDBAR["FREQZZ"][2])
            if "." in PSSOFREQ:
                PSSOFREQ = ROUNDNUM(PSSOFREQ)
            PSSLFREQ = HASH[COUNT, "frequencyLow"]
            if "." in PSSLFREQ:
                PSSLFREQ = ROUNDNUM(PSSLFREQ)
            PSSHFREQ = HASH[COUNT, "frequencyHigh"]
            if "." in PSSHFREQ:
                PSSHFREQ = ROUNDNUM(PSSHFREQ)
            if (PSSLFREQ < 0.01 or PSSHFREQ < 0.01) and (PSSOFREQ < PSSLFREQ or PSSOFREQ > PSSHFREQ):
                PSSDBCAR[HASH[COUNT, "orderNumber"]] = 1
            if PSSOFREQ < 1 and PSSLFREQ >= 1 and PSSHFREQ >= 1:
                PSSDBCAR[HASH[COUNT, "orderNumber"]] = 1
            if PSSOFREQ >= 1 and PSSLFREQ < 1 and PSSHFREQ < 1:
                PSSDBCAR[HASH[COUNT, "orderNumber"]] = 1

def MSG(HASH, COUNT, TYPE):
    # INPUTS: HASH array (by ref)
    #         COUNT: Index of current array
    #         TYPE: Either "R" for Daily dose Range or "S" for maximum single dose
    # RETURNS: None
    MSG = DOSEMSG(HASH[COUNT, "drugName"], TYPE)
    if TYPE == "R":
        REASON = HASH[COUNT, "rangeDoseMessage"]
    elif TYPE == "S":
        REASON = HASH[COUNT, "singleDoseMessage"]
    elif TYPE == "D":
        REASON = HASH[COUNT, "dailyDoseMessage"]
    elif TYPE == "M":
        REASON = HASH[COUNT, "maxDailyDoseMessage"]
    HASH[COUNT, "msg"] = MSG
    HASH[COUNT, "text"] = "Unavailable" if REASON == "" else REASON
    WRTNODE(COUNT, "DOSE", HASH)

def CHKVAL(HASH, I, SUB):
    # INPUTS: HASH array (by ref)
    #         I: Index of current array
    #         SUB: subscript
    # RETURNS: If node has value
    return len(HASH[I, SUB])