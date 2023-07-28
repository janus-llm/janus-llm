def DOSEWRIT(HASH, BASE):
    """
    Handles writing the drug dose output global
    
    :param HASH: Variable containing drug dose values
    :param BASE: Base of output global
    :return: Nothing
    """
    I = ""
    while I != "" and not I:
        NODE = f"^TMP($JOB,{BASE},\"OUT\",\"DOSE\",{HASH[I][\"orderNumber\"]},{HASH[I][\"drugName\"]})"
        IEN = HASH[I]["ien"]

        if CHKVAL(HASH, I, "singleDoseStatus"):
            NODE["SINGLE"]["STATUS"][IEN] = HASH[I]["singleDoseStatus"]
        if CHKVAL(HASH, I, "singleDoseStatusCode"):
            NODE["SINGLE"]["STATUSCODE"][IEN] = HASH[I]["singleDoseStatusCode"]
        if CHKVAL(HASH, I, "singleDoseMessage"):
            NODE["SINGLE"]["MESSAGE"][IEN] = HASH[I]["singleDoseMessage"]
        if CHKVAL(HASH, I, "singleDoseMax"):
            NODE["SINGLE"]["MAX"][IEN] = HASH[I]["singleDoseMax"]

        if CHKVAL(HASH, I, "rangeDoseLow"):
            NODE["RANGE"]["LOW"][IEN] = HASH[I]["rangeDoseLow"]
        if CHKVAL(HASH, I, "rangeDoseHigh"):
            NODE["RANGE"]["HIGH"][IEN] = HASH[I]["rangeDoseHigh"]
        if CHKVAL(HASH, I, "rangeDoseStatus"):
            NODE["RANGE"]["STATUS"][IEN] = HASH[I]["rangeDoseStatus"]
        if CHKVAL(HASH, I, "rangeDoseStatusCode"):
            NODE["RANGE"]["STATUSCODE"][IEN] = HASH[I]["rangeDoseStatusCode"]
        if CHKVAL(HASH, I, "rangeDoseMessage"):
            NODE["RANGE"]["MESSAGE"][IEN] = HASH[I]["rangeDoseMessage"]

        if CHKVAL(HASH, I, "doseFormHigh"):
            NODE["GENERAL"]["DOSEFORMHIGH"][IEN] = HASH[I]["doseFormHigh"]
        if CHKVAL(HASH, I, "doseFormHighUnit"):
            NODE["GENERAL"]["DOSEFORMHIGHUNIT"][IEN] = HASH[I]["doseFormHighUnit"]
        if CHKVAL(HASH, I, "doseFormLow"):
            NODE["GENERAL"]["DOSEFORMLOW"][IEN] = HASH[I]["doseFormLow"]
        if CHKVAL(HASH, I, "doseFormLowUnit"):
            NODE["GENERAL"]["DOSEFORMLOWUNIT"][IEN] = HASH[I]["doseFormLowUnit"]

        NODE["GENERAL"]["DOSEHIGH"][IEN] = HASH[I]["doseHigh"]
        NODE["GENERAL"]["DOSEHIGHUNIT"][IEN] = HASH[I]["doseHighUnit"]
        NODE["GENERAL"]["DOSELOW"][IEN] = HASH[I]["doseLow"]
        NODE["GENERAL"]["DOSELOWUNIT"][IEN] = HASH[I]["doseLowUnit"]
        NODE["GENERAL"]["DOSEROUTEDESCRIPTION"][IEN] = HASH[I]["doseRouteDescription"]
        NODE["GENERAL"]["MESSAGE"][IEN] = BUILDMSG(I, HASH)

        if CHKVAL(HASH, I, "chemoInjectable"):
            NODE["CHEMO"] = HASH[I]["chemoInjectable"]

        if CHKVAL(HASH, I, "dailyDoseStatus"):
            NODE["DAILY"]["STATUS"][IEN] = HASH[I]["dailyDoseStatus"]
        if CHKVAL(HASH, I, "dailyDoseStatusCode"):
            NODE["DAILY"]["STATUSCODE"][IEN] = HASH[I]["dailyDoseStatusCode"]
        if CHKVAL(HASH, I, "dailyDoseMessage"):
            NODE["DAILY"]["MESSAGE"][IEN] = HASH[I]["dailyDoseMessage"]

        if CHKVAL(HASH, I, "maxDailyDoseStatus"):
            NODE["DAILYMAX"]["STATUS"][IEN] = HASH[I]["maxDailyDoseStatus"]
        if CHKVAL(HASH, I, "maxDailyDoseStatusCode"):
            NODE["DAILYMAX"]["STATUSCODE"][IEN] = HASH[I]["maxDailyDoseStatusCode"]
        if CHKVAL(HASH, I, "maxDailyDoseMessage"):
            NODE["DAILYMAX"]["MESSAGE"][IEN] = HASH[I]["maxDailyDoseMessage"]

        if CHKVAL(HASH, I, "maxLifetimeDose"):
            NODE["MAXLIFETIME"]["DOSE"][IEN] = HASH[I]["maxLifetimeDose"]

        if CHKVAL(HASH, I, "frequencyStatus"):
            NODE["FREQ"]["FREQUENCYSTATUS"][IEN] = HASH[I]["frequencyStatus"]
        if CHKVAL(HASH, I, "frequencyStatusCode"):
            NODE["FREQ"]["FREQUENCYSTATUSCODE"][IEN] = HASH[I]["frequencyStatusCode"]
        if CHKVAL(HASH, I, "frequencyMessage"):
            NODE["FREQ"]["FREQUENCYMESSAGE"][IEN] = HASH[I]["frequencyMessage"]
        if CHKVAL(HASH, I, "frequencyHigh"):
            NODE["FREQ"]["FREQUENCYHIGH"][IEN] = HASH[I]["frequencyHigh"]
            CSTMFREQ(HASH, I, NODE, IEN)
        if CHKVAL(HASH, I, "frequencyLow"):
            NODE["FREQ"]["FREQUENCYLOW"][IEN] = HASH[I]["frequencyLow"]
            CSTMFREQ(HASH, I, NODE, IEN)

        if "single" in HASH[I]:
            WRITEDSP(NODE, HASH, I, IEN, "single", "", "")
        if "rangeLow" in HASH[I]:
            WRITEDSP(NODE, HASH, I, IEN, "rangeLow", "", "")
        if "rangeHigh" in HASH[I]:
            WRITEDSP(NODE, HASH, I, IEN, "rangeHigh", "", "")
        if "daily" in HASH[I]:
            WRITEDSP(NODE, HASH, I, IEN, "daily", "", "")
        if "maxDaily" in HASH[I]:
            WRITEDSP(NODE, HASH, I, IEN, "maxDaily", "DAILYMAX", "")
        if "maxLifetime" in HASH[I]:
            WRITEDSP(NODE, HASH, I, IEN, "maxLifetime", "", "")
        if "maxLifetimeOrder" in HASH[I]:
            WRITEDSP(NODE, HASH, I, IEN, "maxLifetimeOrder", "", "")

        if CHKVAL(HASH, I, "maxLifetimeOrderMessage"):
            NODE["MAXLIFETIMEORDER"]["MESSAGE"][IEN] = HASH[I]["maxLifetimeOrderMessage"]
        if CHKVAL(HASH, I, "maxLifetimeOrderStatus"):
            NODE["MAXLIFETIMEORDER"]["STATUS"][IEN] = HASH[I]["maxLifetimeOrderStatus"]
        if CHKVAL(HASH, I, "maxLifetimeOrderStatusCode"):
            NODE["MAXLIFETIMEORDER"]["STATUSCODE"][IEN] = HASH[I]["maxLifetimeOrderStatusCode"]

        if CHKVAL(HASH, I, "maxSingleNTEDose"):
            NODE["MAXSINGLENTE"]["DOSE"][IEN] = HASH[I]["maxSingleNTEDose"]
        if CHKVAL(HASH, I, "maxSingleNTEDoseUnit"):
            NODE["MAXSINGLENTE"]["DOSEUNIT"][IEN] = HASH[I]["maxSingleNTEDoseUnit"]
        if CHKVAL(HASH, I, "maxSingleNTEDoseForm"):
            NODE["MAXSINGLENTE"]["DOSEFORM"][IEN] = HASH[I]["maxSingleNTEDoseForm"]
        if CHKVAL(HASH, I, "maxSingleNTEDoseFormUnit"):
            NODE["MAXSINGLENTE"]["DOSEFORMUNIT"][IEN] = HASH[I]["maxSingleNTEDoseFormUnit"]

        if CHKVAL(HASH, I, "maxDailyDose"):
            NODE["DAILYMAX"]["DOSE"][IEN] = HASH[I]["maxDailyDose"]
        if CHKVAL(HASH, I, "maxDailyDoseUnit"):
            NODE["DAILYMAX"]["DOSEUNIT"][IEN] = HASH[I]["maxDailyDoseUnit"]
        if CHKVAL(HASH, I, "maxDailyDoseForm"):
            NODE["DAILYMAX"]["DOSEFORM"][IEN] = HASH[I]["maxDailyDoseForm"]
        if CHKVAL(HASH, I, "maxDailyDoseFormUnit"):
            NODE["DAILYMAX"]["DOSEFORMUNIT"][IEN] = HASH[I]["maxDailyDoseFormUnit"]

        if HASH[I]["orderNumber"] != "" and PSSDBCAR(HASH[I]["orderNumber"]).split("^")[29]:
            PSSFSCO = HASH[I]["orderNumber"]
            PSSFSCB = BASE
            PSSFSCN = HASH[I]["drugName"]
            PSSFSCI = HASH[I]["ien"]
            MAXD(PSSFSCO, PSSFSCB, PSSFSCN, PSSFSCI, PSSDBCAR)

        I = I + 1