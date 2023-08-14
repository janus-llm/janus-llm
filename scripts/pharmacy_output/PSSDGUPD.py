def PSSDGUPD():
    """
    BIR/PWC - builds HL7 V.2.4 drug update message
    """
    # IA: 10054 - ^LAB(60
    # IA: 10055 - ^LAB(61
    # IA: 2079 - ^PSNDF
    # IA: 2221 - ^PS(50.607
    # IA: 872 - ^ORD(101
    # IA: 10106 - $$HLDATE^HLFNC
    # IA: 2161 - INIT^HLFNC2
    # IA: 2164 - GENERATE^HLMA

    # entry point
    def DRG(DRG, NEW, DNSNAM, DNSPORT):
        """
        Entry point for DRG
        """
        # Local variables
        CNT, DOSF, DRG0, DRG2, DRG3, DRG6, DRG60, DRGN, DRGSYN, DRGZ, DRGZ1, MEDRT, PSSRESLT, PSSOPTNS, PROT, HL, HLA, ZPA, RXD, OBR, DOS1, DOS2, CLOZ2, LTMON, XX, WARN, LNF, VNF, SYIN, SYNINT, SYUN, VSN, TYPE, UNIT, WNS, WW, ORDITEM, CMOP, OPEXT, LABTST, SPEC, ZPANF, ZPACMOP

        HLA = {"HLS": {}}
        PROT = next((i for i, val in enumerate(ORD, 101, "PSS EXT MFU SERVER") if val == "PSS EXT MFU SERVER"), 0)
        if PROT == 0:
            print("Drug Update Protocol NOT Installed ")
            return

        INIT_HLFNC2(PROT, HL)
        if HL:
            return

        HL["ECH"] = "~^\\&"
        CNT = 0

        DRG0 = PSSDRUG[DRG][0]
        DRG2 = PSSDRUG[DRG][2]
        DRG3 = PSSDRUG[DRG][3]
        DRG6 = PSSDRUG[DRG][6]
        DRGN = PSSDRUG[DRG]["ND"]
        DRGZ = PSSDRUG[DRG]["CLOZ"]
        DRGZ1 = PSSDRUG[DRG]["CLOZ1"]
        DRG60 = PSSDRUG[DRG][660]

        WARN = DRG0[8]
        LNF = DRG0[9]
        VNF = DRG0[11]

        WNS = ""
        if WARN:
            for i in range(1, len(WARN) + 1):
                WW = WARN[i-1]
                if WW == "":
                    break
                WNS = WNS + WW + "^" + PS_54[WW][0] + "~"

        ORDITEM = DRG2
        CMOP = DRG3
        OPEXT = DRG6

        LABTST = DRGZ
        SPEC = DRGZ[3]

        # msh segment
        # CNT += 1
        # HLA["HLS"][CNT] = "MSH|~^\\&|PSS VISTA|STATION #~STATION DNS~DNS|PSS DISPENSE|~DISPENSE DNS NAME:PORT~DNS|" + H + "||MFN^M01|10001||P|2.4|||AL|AL|||||"

        # mfi segment
        CNT += 1
        HLA["HLS"][CNT] = "MFI|50^DRUG^99PSD||UPD|||NE"

        # the MFE and ZPA segments are multiples and a separate one will be sent
        # for each Drug and the matching synonyms.

        # mfe segment - DRUG
        CNT += 1
        HLA["HLS"][CNT] = "MFE|" + ("MAD" if NEW else "MUP") + "|||" + DRG0[0]

        # zpa segment - DRUG
        CNT += 1
        ZPA = ""
        ZPA += DRG0[0] + "|N|"    # main drug

        if LNF and VNF:
            ZPANF = "LFN^Local Non-Formulary^Pharm Formulary Listing~VFN^VISN Non-Formulary^Pharm Formulary Listing"
        elif LNF and not VNF:
            ZPANF = "LFN^Local Non-Formulary^Pharm Formulary Listing"
        elif not LNF and VNF:
            ZPANF = "VFN^VISN Non-Formulary^Pharm Formulary Listing"

        ZPA += ZPANF + "|"
        ZPA += HLDATE_HLFNC(^PSDRUG(DRG, "I"), "TS") + "|"
        ZPA += DRG0[10] + "|"
        ZPA += DRG0[2] + "|"
        ZPA += DRG0[3][0] + "|"
        ZPA += DRG0[3][1] + "|"
        ZPA += ("50^" + DRG0[6] + "^LPS50" if DRG0[6] else "") + "|"
        ZPA += WNS + "|"
        ZPA += (ORDITEM + "^" + PS_50_7[ORDITEM][0] + "^LPSD50.7" if ORDITEM and PS_50_7[ORDITEM] else "") + "|"

        DOSF = PS_50_7[ORDITEM][1] if ORDITEM and PS_50_7[ORDITEM] else ""
        ZPA += DOSF + "|"

        MEDRT = PS_50_7[ORDITEM][6] if ORDITEM and PS_50_7[ORDITEM] else ""
        ZPA += MEDRT + "|"

        ZPA += (DRGN[3] + "^" + PSNDF_50_68[DRGN[3]][0] + "^LPSD50.68" if DRGN[3] and PSNDF_50_68[DRGN[3]] else "") + "|"

        if CMOP and OPEXT:
            ZPACMOP = "OP^OP Dispense^Pharm dispense flag~CMOP^CMOP Dispense^Pharm dispense flag"
        elif not CMOP and OPEXT:
            ZPACMOP = "OP^OP Dispense^Pharm dispense flag"
        elif CMOP and not OPEXT:
            ZPACMOP = "CMOP^CMOP Dispense^Pharm dispense flag"

        ZPA += ZPACMOP + "|"
        ZPA += HLDATE_HLFNC(DRG60[9], "TS") + "|"
        ZPA += (LABTST + "^" + LAB_60[LABTST][0] + "^LLAB60" if LABTST and LAB_60[LABTST] else "") + "|"
        ZPA += (SPEC + "^" + LAB_61[SPEC][0] + "^LLAB61" if SPEC and LAB_61[SPEC] else "") + "|"
        ZPA += DRGZ1[0] + "|"
        ZPA += DRGZ[1] + "|"
        ZPA += ^PSDRUG(DRG, "DOS") + "|"

        UNIT = ^PSDRUG(DRG, "DOS")[1]
        ZPA += (UNIT + "^" + PS_50_607[UNIT][0] + "^LPSD50.607" if UNIT and PS_50_607[UNIT] else "") + "|"

        ZPA += (DRG60[3] + "&USD^UP" if DRG60[3] else "") + "|"
        ZPA += (DRG60[6] + "&USD^UP" if DRG60[6] else "") + "|"
        ZPA += DRG60[8] + "|"
        ZPA += DRG60[5] + "|"
        ZPA += DRG2[4] + "|"

        HLA["HLS"][CNT] = "ZPA|" + ZPA

        # rxd segment
        # a separate RXD segment will be sent for each multiple of possible dosages
        for XX in range(1, len(^PSDRUG(DRG, "DOS1")) + 1):
            DOS1 = ^PSDRUG(DRG, "DOS1")[XX-1]
            RXD = ""
            RXD += DOS1[4] + "|"
            RXD += DOS1[0] + "|"
            RXD += "^P&" + DOS1[2] + "&LPSD50.0903|"
            RXD += DOS1[3] + "|"
            HLA["HLS"][CNT] = "RXD|" + RXD

        # a separate RXD segment will be sent for each local possible dosages
        for XX in range(1, len(^PSDRUG(DRG, "DOS2")) + 1):
            DOS2 = ^PSDRUG(DRG, "DOS2")[XX-1]
            RXD = ""
            RXD += DOS2[3] + "|"
            RXD += ("^LP&" + DOS2 + "&LPSD50.0904" if DOS2 else "") + "|"
            RXD += DOS2[2] + "|"
            HLA["HLS"][CNT] = "RXD|" + RXD

        # obr segments - clozapine lab tests
        # a separate OBR segment will be sent for each clozapine multiple
        for XX in range(1, len(^PSDRUG(DRG, "CLOZ2")) + 1):
            CLOZ2 = ^PSDRUG(DRG, "CLOZ2")[XX-1]
            LTMON = CLOZ2
            SPEC = CLOZ2[3]
            TYPE = CLOZ2[4]
            OBR = ""
            OBR += (LTMON + "^" + LAB_60[LTMON][0] + "^LLAB60" if LTMON and LAB_60[LTMON] else "") + "|"
            OBR += (SPEC + "^" + LAB_61[SPEC][0] + "^LLAB61" if SPEC and LAB_61[SPEC] else "") + "|"
            OBR += (TYPE if TYPE == 1 else "WBC" if TYPE == 2 else "ANC" if TYPE == 3 else "") + "|"
            OBR += CLOZ2[2] + "|"
            HLA["HLS"][CNT] = "OBR|" + OBR

        # now send SYNONYMS for DRUG in multiple ZPA segments
        for XX in range(1, len(^PSDRUG(DRG, 1)) + 1):
            DRGSYN = ^PSDRUG(DRG, 1)[XX-1]
            SYIN = DRGSYN[3]
            VSN = DRGSYN[4]
            SYUN = DRGSYN[5]
            SYNINT = ("TRADE NAME" if SYIN == 0 else "QUICK CODE" if SYIN == 1 else "DRUG ACCOUNTABILITY" if SYIN == "D" else "CONTROLLED SUBSTANCE" if SYIN == "C" else "")
            ZPA = ""
            ZPA += DRGSYN[0] + "|Y|"
            ZPA += (VSN + "^" + PS_50_1[VSN][0] + "^LPS50.1" if VSN and PS_50_1[VSN] else "") + "|"
            ZPA += (SYUN + "^" + DIC_51_5[SYUN][0] + "^LPSD51.5" if SYUN and DIC_51_5[SYUN] else "") + "|"
            ZPA += (DRGSYN[6] + "&USD^UP" if DRGSYN[6] else "") + "|"
            ZPA += (DRGSYN[8] + "&USD^UP" if DRGSYN[8] else "") + "|"
            ZPA += DRGSYN[7] + "|"
            ZPA += DRGSYN[9] + "|"
            ZPA += DRGSYN[2] + "|"
            ZPA += SYNINT + "|"
            HLA["HLS"][CNT] = "ZPA|" + ZPA

        PSSOPTNS["SUBSCRIBER"] = "^^^^~" + DNSNAM + ":" + DNSPORT + "~DNS"
        GENERATE_HLMA("PSS EXT MFU SERVER", "LM", 1, PSSRESLT, "", PSSOPTNS)
        HLA["HLS"] = {}

    PSN()