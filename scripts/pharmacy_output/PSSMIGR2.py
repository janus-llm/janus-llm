def DSFO(IEN, RCNT, TYPE):
    import datetime
    CNT = 0
    XST = 0
    FNAME = "drugMigrationResponse_DosageForm.XML"
    FNUM = 50.606
    FNAME1 = "dosageForm"
    if IEN < 0:
        OUT^PSSMIGR(" Error... Invalid IEN")
        return
    if RCNT < 1:
        OUT^PSSMIGR(" Error... Invalid Starting Record Number")
        return
    if TYPE > 1 or TYPE < 0:
        OUT^PSSMIGR(" Error... Invalid TYPE")
        return
    while True:
        IEN = IEN + 1
        if +IEN == 0:
            ^TMP($J,50.606,"EOF") = 1
            XST = 1
            break
        if RCNT == CNT:
            XST = 1
            break
        PS0 = ^PS(50.606,IEN,0)
        NAME = PS0.split("^")[0]
        IND = PS0.split("^")[1]
        XTYPE = 0 if +IND else 1
        IND = datetime.datetime.strptime(IND, '%Y%m%d').strftime('%Y-%m-%d')
        PSM = ^PS(50.606,IEN,"MISC")
        EFDC = ^PS(50.606,IEN,1).split("^")[0]
        VERB = PSM.split("^")[0]
        PREP = PSM.split("^")[2]
        XIEN = "<dosageFormIen>" + str(IEN) + "</dosageFormIen>"
        XNAME = "<name>" + NAME + "</name>" if NAME else ""
        XIND = "<inactivationDate>" + IND + "</inactivationDate>" if IND else ""
        XEFDC = "<excludeFromDosageChecks>" + EFDC + "</excludeFromDosageChecks>" if EFDC else ""
        ^TMP($J,50.606,XTYPE,IEN) = XIEN + XNAME + XIND
        ^TMP($J,50.606,XTYPE,IEN,999999) = XEFDC
        if $D(^PS(50.606,IEN,"UNIT",0)):
            MIEN = 0
            while True:
                MIEN = MIEN + 1
                if MIEN == "B" or MIEN == "":
                    break
                PST0 = ^PS(50.606,IEN,"UNIT",MIEN,0)
                UNIT = PST0.split("^")[0]
                PACK = PST0.split("^")[1]
                UNAME = ^PS(50.607,UNIT,0).split("^")[0] if +UNIT else ""
                XIEN1 = "<unitsIen>" + str(MIEN) + "</unitsIen>"
                XUNIT = "<units>" + UNAME + "</units>" if UNAME else ""
                XPACK = "<package>" + PACK + "</package>" if PACK else ""
                ^TMP($J,50.606,XTYPE,IEN,91 + MIEN) = "<units>" + XIEN1 + XUNIT + XPACK + "</units>"
        if $D(^PS(50.606,IEN,"DUPD",0)):
            MIEN = 0
            while True:
                MIEN = MIEN + 1
                if MIEN == "B" or MIEN == "":
                    break
                PST0 = ^PS(50.606,IEN,"DUPD",MIEN,0)
                UNIT = PST0.split("^")[0]
                PACK = PST0.split("^")[1]
                XIEN1 = "<dispenseUnitsPerDoseIen>" + str(MIEN) + "</dispenseUnitsPerDoseIen>"
                XUNIT = "<dispenseUnitsPerDose>" + UNIT + "</dispenseUnitsPerDose>" if UNIT else ""
                XPACK = "<package>" + PACK + "</package>" if PACK else ""
                ^TMP($J,50.606,XTYPE,IEN,999 + MIEN) = "<dispenseUnitsPerDose>" + XIEN1 + XUNIT + XPACK + "</dispenseUnitsPerDose>"
        if XTYPE == TYPE:
            CNT = CNT + 1

def VAPD(IEN, RCNT, TYPE):
    import datetime
    CNT = 0
    ^TMP($J,50.68,"EOF") = 0
    FNAME = "drugMigrationResponse_VAProduct.XML"
    FNUM = 50.68
    FNAME1 = "vaProduct"
    if IEN < 0:
        OUT^PSSMIGR(" Error... Invalid IEN")
        return
    if RCNT < 1:
        OUT^PSSMIGR(" Error... Invalid Starting Record Number")
        return
    if TYPE > 1 or TYPE < 0:
        OUT^PSSMIGR(" Error... Invalid TYPE")
        return
    while True:
        IEN = IEN + 1
        if +IEN == 0:
            ^TMP($J,50.68,"EOF") = 1
            XST = 1
            break
        if RCNT == CNT:
            XST = 1
            break
        if !$D(^PSNDF(50.68,IEN,0)):
            continue
        PS0 = ^PSNDF(50.68,IEN,0)
        NAME = PS0.split("^")[0]
        VAGN = PS0.split("^")[1]
        DOSF = PS0.split("^")[2]
        STRG = PS0.split("^")[3]
        NAFN = PS0.split("^")[5]
        UNIT = PS0.split("^")[4]
        UNIT = ^PS(50.607,UNIT,0).split("^")[0] if +UNIT else ""
        VAGN = ^PSNDF(50.6,VAGN,0).split("^")[0] if VAGN else ""
        DOSF = ^PS(50.606,DOSF,0).split("^")[0] if DOSF else ""
        PS1 = ^PSNDF(50.68,IEN,1)
        VAPN = PS1.split("^")[0]
        VAPI = PS1.split("^")[1]
        TRTC = PS1.split("^")[2]
        VADU = PS1.split("^")[3]
        GCNS = PS1.split("^")[4]
        PREG = PS1.split("^")[5]
        NLTG = PS1.split("^")[6]
        VADU = ^PSNDF(50.64,+VADU,0).split("^")[0] if VADU else ""
        PVDC = ^PSNDF(50.68,IEN,3).split("^")[0]
        OVCK = ^PSNDF(50.68,IEN,9).split("^")[0]
        EDCK = ^PSNDF(50.68,IEN,8).split("^")[0]
        if +PVDC and $D(^PS(50.605,PVDC,0)):
            PS01 = ^PS(50.605,PVDC,0)
            CODE1 = PS01.split("^")[0]
            CLASS1 = PS01.split("^")[1]
            XIEN1 = "<vaDrugClassIen>" + str(PVDC) + "</vaDrugClassIen>"
            XCODE1 = "<code>" + CODE1 + "</code>" if CODE1 else ""
            XCLASS1 = "<classification>" + CLASS1 + "</classification>" if CLASS1 else ""
            XTMP = XIEN1 + XCODE1 + XCLASS1
        SVDC = ^PSNDF(50.68,IEN,4,0).split("^")[0]
        NAFI = ^PSNDF(50.68,IEN,5).split("^")[0]
        NAFR = ^PSNDF(50.68,IEN,6,0).split("^")[0]
        PS7 = ^PSNDF(50.68,IEN,7)
        CSFS = PS7.split("^")[0]
        SMSP = PS7.split("^")[1]
        INAD = PS7.split("^")[2]
        MASD = PS7.split("^")[3]
        MISD = PS7.split("^")[4]
        MADD = PS7.split("^")[5]
        MIDD = PS7.split("^")[6]
        MACD = PS7.split("^")[7]
        XTYPE = 0 if +INAD else 1
        INAD = datetime.datetime.strptime(INAD, '%Y%m%d').strftime('%Y-%m-%d')
        VUID = ^PSNDF(50.68,IEN,"VUID").split("^")[0]
        MVUID = ^PSNDF(50.68,IEN,"VUID").split("^")[1]
        DOS = ^PSNDF(50.68,IEN,"DOS")
        CPD = DOS.split("^")[0]
        PDTC = DOS.split("^")[1]
        PP = DOS.split("^")[2]
        FMG = ^PSNDF(50.68,IEN,"MG").split("^")[0]
        SVC = ^PSNDF(50.68,IEN,"PFS").split("^")[0]
        XIEN = "<ndfProductIen>" + str(IEN) + "</ndfProductIen>"
        XNAME = "<name><![CDATA[" + NAME + "]]></name>" if NAME else ""
        XVAGN = "<vaGenericName><![CDATA[" + VAGN + "]]></vaGenericName>" if VAGN else ""
        XDOSF = "<dosageForm>" + DOSF + "</dosageForm>" if DOSF else ""
        XSTRG = "<strength><![CDATA[" + STRG + "]]></strength>" if STRG else ""
        XUNIT = "<units>" + UNIT + "</units>" if UNIT else ""
        XNAFN = "<nationalFormularyName><![CDATA[" + NAFN + "]]></nationalFormularyName>" if NAFN else ""
        XVAPN = "<vaPrintName><![CDATA[" + VAPN + "]]></vaPrintName>" if VAPN else ""
        XVAPI = "<vaProductIdentifier>" + VAPI + "</vaProductIdentifier>" if VAPI else ""
        XTRTC = "<transmitToCmop>" + TRTC + "</transmitToCmop>" if TRTC else ""
        XVADU = "<vaDispenseUnit>" + VADU + "</vaDispenseUnit>" if VADU else ""
        XGCNS = "<gcnSeqNo>" + GCNS + "</gcnSeqNo>" if GCNS else ""
        XPVDC = "<primaryVaDrugClass>" + XTMP + "</primaryVaDrugClass>" if PVDC else ""
        XNAFI = "<nationalFormularyIndicator>" + NAFI + "</nationalFormularyIndicator>" if NAFI else ""
        XCSFS = "<csFederalSchedule>" + CSFS + "</csFederalSchedule>" if CSFS else ""
        XSMSP = "<singleMultiSourceProduct>" + SMSP + "</singleMultiSourceProduct>" if SMSP else ""
        XINAD = "<inactivationDate>" + INAD + "</inactivationDate>" if INAD else ""
        XOVCK = "<overrideDfDoseChkExclusion>" + OVCK + "</overrideDfDoseChkExclusion>" if OVCK else ""
        XEDCK = "<excludeDrugDrugInteraction>" + EDCK + "</excludeDrugDrugInteraction>" if EDCK else ""
        XCPD = "<createPossibleDosage>" + CPD + "</createPossibleDosage>" if CPD else ""
        XPP = "<productPackage>" + PP + "</productPackage>" if PP else ""
        XMVUID = "<masterEntryForVuid>" + MVUID + "</masterEntryForVuid>" if MVUID else ""
        XVUID = "<vuid>" + VUID + "</vuid>" if VUID else ""
        XFMG = "<fdaMedGuide>" + FMG + "</fdaMedGuide>" if FMG else ""
        XSVC = "<serviceCode>" + SVC + "</serviceCode>" if SVC else ""
        XPDTC = "<possibleDosagesToCreate>" + PDTC + "</possibleDosagesToCreate>" if PDTC else ""
        XML = XIEN + XNAME + XVAGN + XDOSF + XSTRG + XUNIT + XNAFN + XVAPN + XVAPI + XTRTC + XVADU + XGCNS
        XML2 = XPVDC + XNAFI + XCSFS + XSMSP + XINAD + XOVCK + XEDCK + XCPD + XPP + XMVUID + XVUID
        XML3 = XFMG + XSVC + XPDTC
        ^TMP($J,50.68,XTYPE,IEN) = XML
        ^TMP($J,50.68,XTYPE,IEN,9999) = XML2
        ^TMP($J,50.68,XTYPE,IEN,99999) = XML3
        if $D(^PSNDF(50.68,IEN,2,0)):
            MIEN = 0
            while True:
                MIEN = MIEN + 1
                if MIEN == "B" or MIEN == "":
                    break
                PST0 = ^PSNDF(50.68,IEN,2,MIEN,0)
                ACTI = PST0.split("^")[0]
                STRN = PST0.split("^")[1]
                UNTS = PST0.split("^")[2]
                ACTI = ^PS(50.416,+ACTI,0).split("^")[0]
                UNTS = ^PS(50.607,+UNTS,0).split("^")[0]
                XMIEN = "<activeIngredientIen>" + str(MIEN) + "</activeIngredientIen>"
                XACTI = "<ingredientName><![CDATA[" + ACTI + "]]></ingredientName>" if ACTI else ""
                XSTRN = "<strength><![CDATA[" + STRN + "]]></strength>" if STRN else ""
                XUNTS = "<units>" + UNTS + "</units>" if UNTS else ""
                XTMP = XMIEN + XACTI + XSTRN + XUNTS
                ^TMP($J,50.68,XTYPE,IEN,MIEN) = "<activeIngredients>" + XTMP + "</activeIngredients>"
        if $D(^PSNDF(50.68,IEN,"TERMSTATUS",0)):
            MIEN = 0
            while True:
                MIEN = MIEN + 1
                if MIEN == "B":
                    break
                PST0 = ^PSNDF(50.68,IEN,"TERMSTATUS",MIEN,0)
                EDT = PST0.split("^")[0]
                STA = PST0.split("^")[1]
                EDT = datetime.datetime.strptime(EDT, '%Y%m%d').strftime('%Y-%m-%d')
                XEDT = "<effectiveDateTime>" + EDT + "</effectiveDateTime>"
                XSTA = "<status>" + STA + "</status>"
                ^TMP($J,50.68,XTYPE,IEN,9999 + MIEN) = "<effectiveDateTime>" + XEDT + XSTA + "</effectiveDateTime>"
        if XTYPE == TYPE:
            CNT = CNT + 1