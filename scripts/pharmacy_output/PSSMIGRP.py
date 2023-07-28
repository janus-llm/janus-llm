def PSSMIGRP():
    pass

def VAP():
    if PSS["bodyName"] == "vaProductSyncRequest":
        RCNT = None
        PSS["child"] = 1
        PSS["FILE"] = 50.68
        PSSTITLE = PST = "syncResponse"
        while PSS["child"] != 0:
            PSS["child"] = CHILD(DOCHAND, 1, PSS["child"])
            if PSS["child"] == 0:
                break
            PSS["ELE"] = NAME(DOCHAND, PSS["child"])
            if PSS["ELE"] == "RequestType":
                PSS["RTYPE"] = TMP["MXMLDOM"][$J][DOCHAND][PSS["child"]]["T"][1]
            if PSS["ELE"] == "vaProductName":
                PSS["NAME"] = TMP["MXMLDOM"][$J][DOCHAND][PSS["child"]]["T"][1]
            if PSS["ELE"] == "vaProductIen":
                PSS["IEN"] = TMP["MXMLDOM"][$J][DOCHAND][PSS["child"]]["T"][1]
            if PSS["ELE"] == "vaGenericNameRecord":
                DOCHAND1 = PSS["child"]
                PSS["child1"] = 1
                while PSS["child1"] != 0:
                    PSS["child1"] = CHILD(DOCHAND, DOCHAND1, PSS["child1"])
                    if PSS["child1"] == 0:
                        break
                    PSS["ELE1"] = NAME(DOCHAND, PSS["child1"])
                    if PSS["ELE1"] == "vaGenericNameName":
                        PSS["GENNAME"] = TMP["MXMLDOM"][$J][DOCHAND][PSS["child1"]]["T"][1]
                    if PSS["ELE1"] == "vaGenericIen":
                        PSS["GENIEN"] = TMP["MXMLDOM"][$J][DOCHAND][PSS["child1"]]["T"][1]
            if PSS["ELE"] == "dosageFormRecord":
                DOCHAND1 = PSS["child"]
                PSS["child1"] = 1
                while PSS["child1"] != 0:
                    PSS["child1"] = CHILD(DOCHAND, DOCHAND1, PSS["child1"])
                    if PSS["child1"] == 0:
                        break
                    PSS["ELE1"] = NAME(DOCHAND, PSS["child1"])
                    if PSS["ELE1"] == "dosageFormName":
                        PSS["DFNAME"] = TMP["MXMLDOM"][$J][DOCHAND][PSS["child1"]]["T"][1]
                    if PSS["ELE1"] == "dosageFormIen":
                        PSS["DFIEN"] = TMP["MXMLDOM"][$J][DOCHAND][PSS["child1"]]["T"][1]
            if PSS["ELE"] == "strength":
                PSS["STRGEN"] = TMP["MXMLDOM"][$J][DOCHAND][PSS["child"]]["T"][1]
            if PSS["ELE"] == "units":
                PSS["UNITS"] = TMP["MXMLDOM"][$J][DOCHAND][PSS["child"]]["T"][1]
            if PSS["ELE"] == "nationalFormularyName":
                PSS["NFNAME"] = TMP["MXMLDOM"][$J][DOCHAND][PSS["child"]]["T"][1]
            if PSS["ELE"] == "vaPrintName":
                PSS["PRINTNAME"] = TMP["MXMLDOM"][$J][DOCHAND][PSS["child"]]["T"][1]
            if PSS["ELE"] == "vaProductIdentifier":
                PSS["PRODID"] = TMP["MXMLDOM"][$J][DOCHAND][PSS["child"]]["T"][1]
            if PSS["ELE"] == "transmitToCmop":
                PSS["TRANSTC"] = TMP["MXMLDOM"][$J][DOCHAND][PSS["child"]]["T"][1]
            if PSS["ELE"] == "vaDispenseUnitRecord":
                DOCHAND1 = PSS["child"]
                PSS["child1"] = 1
                while PSS["child1"] != 0:
                    PSS["child1"] = CHILD(DOCHAND, DOCHAND1, PSS["child1"])
                    if PSS["child1"] == 0:
                        break
                    PSS["ELE1"] = NAME(DOCHAND, PSS["child1"])
                    if PSS["ELE1"] == "vaDispenseUnitName":
                        PSS["DUNAME"] = TMP["MXMLDOM"][$J][DOCHAND][PSS["child1"]]["T"][1]
                    if PSS["ELE1"] == "vaDispenseUnitIen":
                        PSS["DUIEN"] = TMP["MXMLDOM"][$J][DOCHAND][PSS["child1"]]["T"][1]
            if PSS["ELE"] == "activeIngredientsRecord":
                RCNT = RCNT.get() + 1
                DOCHAND1 = PSS["child"]
                PSS["child1"] = 1
                while PSS["child1"] != 0:
                    PSS["child1"] = CHILD(DOCHAND, DOCHAND1, PSS["child1"])
                    if PSS["child1"] == 0:
                        break
                    PSS["ELE1"] = NAME(DOCHAND, PSS["child1"])
                    if PSS["ELE1"] == "activeIngredientsName":
                        PSS["AINAME" + RCNT] = TMP["MXMLDOM"][$J][DOCHAND][PSS["child1"]]["T"][1]
                    if PSS["ELE1"] == "activeIngredientsIen":
                        PSS["AIIEN" + RCNT] = TMP["MXMLDOM"][$J][DOCHAND][PSS["child1"]]["T"][1]
                    if PSS["ELE1"] == "activeIngredientsStrength":
                        PSS["AISTRG" + RCNT] = TMP["MXMLDOM"][$J][DOCHAND][PSS["child1"]]["T"][1]
                    if PSS["ELE1"] == "activeIngredientsUnitsName":
                        PSS["AIUNAME" + RCNT] = TMP["MXMLDOM"][$J][DOCHAND][PSS["child1"]]["T"][1]
                PSS["ACTID"] = RCNT
            if PSS["ELE"] == "gcnSeqNo":
                PSS["GCNSEQNO"] = TMP["MXMLDOM"][$J][DOCHAND][PSS["child"]]["T"][1]
            if PSS["ELE"] == "primaryVaDrugClassRecord":
                DOCHAND1 = PSS["child"]
                PSS["child1"] = 1
                while PSS["child1"] != 0:
                    PSS["child1"] = CHILD(DOCHAND, DOCHAND1, PSS["child1"])
                    if PSS["child1"] == 0:
                        break
                    PSS["ELE1"] = NAME(DOCHAND, PSS["child1"])
                    if PSS["ELE1"] == "primaryVaDrugClassCode":
                        PSS["PVADCCODE"] = TMP["MXMLDOM"][$J][DOCHAND][PSS["child1"]]["T"][1]
                    if PSS["ELE1"] == "primaryVaDrugClassClassification":
                        PSS["PVADCCLASS"] = TMP["MXMLDOM"][$J][DOCHAND][PSS["child1"]]["T"][1]
                    if PSS["ELE1"] == "primaryVaDrugClassIen":
                        PSS["PVADCIEN"] = TMP["MXMLDOM"][$J][DOCHAND][PSS["child1"]]["T"][1]
            if PSS["ELE"] == "nationalFormularyIndicator":
                PSS["NFINDICATOR"] = TMP["MXMLDOM"][$J][DOCHAND][PSS["child"]]["T"][1]
            if PSS["ELE"] == "csFederalSchedule":
                PSS["CSFSCHED"] = TMP["MXMLDOM"][$J][DOCHAND][PSS["child"]]["T"][1]
            if PSS["ELE"] == "singleMultiSourceProduct":
                PSS["SMSPROD"] = TMP["MXMLDOM"][$J][DOCHAND][PSS["child"]]["T"][1]
            if PSS["ELE"] == "excludeDrugDrugInteraction":
                PSS["EDDINTER"] = TMP["MXMLDOM"][$J][DOCHAND][PSS["child"]]["T"][1]
            if PSS["ELE"] == "overrideDfDoseChkExclusion":
                PSS["ODFDCHKX"] = TMP["MXMLDOM"][$J][DOCHAND][PSS["child"]]["T"][1]
            if PSS["ELE"] == "createPossibleDosage":
                PSS["CPDOSAGE"] = TMP["MXMLDOM"][$J][DOCHAND][PSS["child"]]["T"][1]
            if PSS["ELE"] == "masterEntryForVuid":
                PSS["MVUID"] = TMP["MXMLDOM"][$J][DOCHAND][PSS["child"]]["T"][1]
            if PSS["ELE"] == "vuid":
                PSS["VUID"] = TMP["MXMLDOM"][$J][DOCHAND][PSS["child"]]["T"][1]
            if PSS["ELE"] == "productPackage":
                PSS["PACK"] = TMP["MXMLDOM"][$J][DOCHAND][PSS["child"]]["T"][1]
            if PSS["ELE"] == "effectiveDateTimeRecord":
                DOCHAND1 = PSS["child"]
                PSS["child1"] = 1
                while PSS["child1"] != 0:
                    PSS["child1"] = CHILD(DOCHAND, DOCHAND1, PSS["child1"])
                    if PSS["child1"] == 0:
                        break
                    PSS["ELE1"] = NAME(DOCHAND, PSS["child1"])
                    if PSS["ELE1"] == "effectiveDateTime":
                        PSS["EFFDT"] = TMP["MXMLDOM"][$J][DOCHAND][PSS["child1"]]["T"][1]
                    if PSS["ELE1"] == "effectiveDateTimeStatus":
                        PSS["EDTS"] = TMP["MXMLDOM"][$J][DOCHAND][PSS["child1"]]["T"][1]
            if PSS["ELE"] == "possibleDosagesToCreate":
                PSS["PDTCREATE"] = TMP["MXMLDOM"][$J][DOCHAND][PSS["child"]]["T"][1]
            if PSS["ELE"] == "inactivationDate":
                PSS["INACTDATE"] = TMP["MXMLDOM"][$J][DOCHAND][PSS["child"]]["T"][1]
            if PSS["ELE"] == "fdaMedGuide":
                PSS["FDAMEDGUIDE"] = TMP["MXMLDOM"][$J][DOCHAND][PSS["child"]]["T"][1]
            if PSS["ELE"] == "serviceCode":
                PSS["SCODE"] = TMP["MXMLDOM"][$J][DOCHAND][PSS["child"]]["T"][1]

def DRUC():
    if PSS["bodyName"] == "drugClassSyncRequest":
        PSS["child"] = 1
        PSS["FILE"] = 50.605
        PSSTITLE = PST = "syncResponse"
        while PSS["child"] != 0:
            PSS["child"] = CHILD(DOCHAND, 1, PSS["child"])
            if PSS["child"] == 0:
                break
            PSS["ELE"] = NAME(DOCHAND, PSS["child"])
            if PSS["ELE"] == "RequestType":
                PSS["RTYPE"] = TMP["MXMLDOM"][$J][DOCHAND][PSS["child"]]["T"][1]
            if PSS["ELE"] == "drugClassCode":
                PSS["CLASSCODE"] = TMP["MXMLDOM"][$J][DOCHAND][PSS["child"]]["T"][1]
            if PSS["ELE"] == "drugClassIen":
                PSS["IEN"] = TMP["MXMLDOM"][$J][DOCHAND][PSS["child"]]["T"][1]
            if PSS["ELE"] == "drugClassClassification":
                PSS["CLASSCLASS"] = TMP["MXMLDOM"][$J][DOCHAND][PSS["child"]]["T"][1]
            if PSS["ELE"] == "ParentClass":
                DOCHAND1 = PSS["child"]
                PSS["child1"] = 1
                while PSS["child1"] != 0:
                    PSS["child1"] = CHILD(DOCHAND, DOCHAND1, PSS["child1"])
                    if PSS["child1"] == 0:
                        break
                    PSS["ELE1"] = NAME(DOCHAND, PSS["child1"])
                    if PSS["ELE1"] == "drugClassIen":
                        PSS["PCIEN"] = TMP["MXMLDOM"][$J][DOCHAND][PSS["child1"]]["T"][1]
                    if PSS["ELE1"] == "code":
                        PSS["PCODE"] = TMP["MXMLDOM"][$J][DOCHAND][PSS["child1"]]["T"][1]
                    if PSS["ELE1"] == "classification":
                        PSS["PCLASS"] = TMP["MXMLDOM"][$J][DOCHAND][PSS["child1"]]["T"][1]
            if PSS["ELE"] == "type":
                PSS["TYPE"] = TMP["MXMLDOM"][$J][DOCHAND][PSS["child"]]["T"][1]
            if PSS["ELE"] == "masterEntryForVuid":
                PSS["MASTERVUID"] = TMP["MXMLDOM"][$J][DOCHAND][PSS["child"]]["T"][1]
            if PSS["ELE"] == "vuid":
                PSS["VUID"] = TMP["MXMLDOM"][$J][DOCHAND][PSS["child"]]["T"][1]
            if PSS["ELE"] == "description":
                PSS["DESC"] = TMP["MXMLDOM"][$J][DOCHAND][PSS["child"]]["T"][1]
            if PSS["ELE"] == "effectiveDateTimeRecord":
                DOCHAND1 = PSS["child"]
                PSS["child1"] = 1
                while PSS["child1"] != 0:
                    PSS["child1"] = CHILD(DOCHAND, DOCHAND1, PSS["child1"])
                    if PSS["child1"] == 0:
                        break
                    PSS["ELE1"] = NAME(DOCHAND, PSS["child1"])
                    if PSS["ELE1"] == "effectiveDateTime":
                        PSS["EFFDATE"] = TMP["MXMLDOM"][$J][DOCHAND][PSS["child1"]]["T"][1]
                    if PSS["ELE1"] == "status":
                        PSS["STATUS"] = TMP["MXMLDOM"][$J][DOCHAND][PSS["child1"]]["T"][1]

def DOF():
    if PSS["bodyName"] == "dosageFormSyncRequest":
        UNCT = DCNT = None
        PSS["child"] = 1
        PSS["FILE"] = 50.606
        PSSTITLE = PST = "syncResponse"
        while PSS["child"] != 0:
            PSS["child"] = CHILD(DOCHAND, 1, PSS["child"])
            if PSS["child"] == 0:
                break
            PSS["ELE"] = NAME(DOCHAND, PSS["child"])
            if PSS["ELE"] == "RequestType":
                PSS["RTYPE"] = TMP["MXMLDOM"][$J][DOCHAND][PSS["child"]]["T"][1]
            if PSS["ELE"] == "dosageFormName":
                PSS["NAME"] = TMP["MXMLDOM"][$J][DOCHAND][PSS["child"]]["T"][1]
            if PSS["ELE"] == "excludeFromDosageChecks":
                PSS["EXCLUDE"] = TMP["MXMLDOM"][$J][DOCHAND][PSS["child"]]["T"][1]
            if PSS["ELE"] == "dosageFormIen":
                PSS["IEN"] = TMP["MXMLDOM"][$J][DOCHAND][PSS["child"]]["T"][1]
            if PSS["ELE"] == "inactivationDate":
                PSS["INACTDATE"] = TMP["MXMLDOM"][$J][DOCHAND][PSS["child"]]["T"][1]
            if PSS["ELE"] == "unitsRecord":
                UNCT = UCNT = 0
                while PSS["child1"] != 0:
                    PSS["child1"] = CHILD(DOCHAND, DOCHAND1, PSS["child1"])
                    if PSS["child1"] == 0:
                        break
                    PSS["ELE1"] = NAME(DOCHAND, PSS["child1"])
                    if PSS["ELE1"] == "units":
                        PSS["UNITS" + UCNT] = TMP["MXMLDOM"][$J][DOCHAND][PSS["child1"]]["T"][1]
                    if PSS["ELE1"] == "unitsIen":
                        PSS["UNITSIEN" + UCNT] = TMP["MXMLDOM"][$J][DOCHAND][PSS["child1"]]["T"][1]
                    if PSS["ELE1"] == "package":
                        PSS["PACKAGE" + UCNT] = TMP["MXMLDOM"][$J][DOCHAND][PSS["child1"]]["T"][1]
                    PSS["UNITS"] = UCNT
            if PSS["ELE"] == "dispenseUnitsPerDose":
                DCNT = PERDOSE = 0
                while PSS["child1"] != 0:
                    PSS["child1"] = CHILD(DOCHAND, DOCHAND1, PSS["child1"])
                    if PSS["child1"] == 0:
                        break
                    PSS["ELE1"] = NAME(DOCHAND, PSS["child1"])
                    if PSS["ELE1"] == "dispenseUnitsPerDoseNumber":
                        PSS["PDDOSE" + DCNT] = TMP["MXMLDOM"][$J][DOCHAND][PSS["child1"]]["T"][1]
                    if PSS["ELE1"] == "package":
                        PSS["PDPACKAGE" + DCNT] = TMP["MXMLDOM"][$J][DOCHAND][PSS["child1"]]["T"][1]
                    PSS["PERDOSE"] = DCNT