# PSS52P6B ;BIR/LDT - API FOR INFORMATION FROM FILE 52.6 CONT.; 5 Sep 03
# 1.0;PHARMACY DATA MANAGEMENT;**85**;9/30/97

def ELYTES():
    SCR_S = ""
    if PSSFL > 0:
        ND = None
        SETSCRN_PSS52P6A()

    if PSSIEN > 0:
        PSSIEN2 = FIND1_DIC(52.6, "", "A", "`" + str(PSSIEN), "", SCR_S, "")
        if PSSIEN2 <= 0:
            TMP_J_LIST_0 = -1 + "^" + "NO DATA FOUND"
            return
        TMP_J_LIST_0 = 1
        GETS_DIQ(52.6, PSSIEN2, ".01;8*", "IE", "^TMP(\"PSS52P6\",$J)")
        PSS_1 = 0
        while PSS_1 in range(len(TMP_PSS52P6[$J][52.6])):
            TMP_J_LIST_PSSIEN2_0 = TMP_PSS52P6[$J][52.6][PSS_1][.01]["I"]
            TMP_J_LIST_B[TMP_PSS52P6[$J][52.6][PSS_1][.01]["I"]] = PSSIEN2
            PSS_1 += 1
        CNT = 0
        PSS_1 = 0
        while PSS_1 in range(len(TMP_PSS52P6[$J][52.62])):
            SETLTS_PSS52P6A()
            CNT += 1
            PSS_1 += 1
        TMP_J_LIST_PSSIEN_ELYTES_0 = CNT if CNT > 0 else "-1^NO DATA FOUND"

    if PSSIEN <= 0 and PSSFT != "":
        if "??" in PSSFT:
            LOOP_PSS52P6A(3)
            return

        FIND_DIC(52.6, "", "@;.01;2", "QP", PSSFT, "", "B", SCR_S, "", "")
        if ^TMP("DILIST", $J, 0) == 0:
            TMP_J_LIST_0 = -1 + "^" + "NO DATA FOUND"
            return
        if ^TMP("DILIST", $J, 0) > 0:
            TMP_J_LIST_0 = +^TMP("DILIST", $J, 0)
            PSSXX = 0
            while PSSXX in range(len(^TMP("DILIST", $J))):
                PSSIEN = +^TMP("DILIST", $J, PSSXX, 0)
                TMP_PSS52P6[$J] = GETS_DIQ(52.6, PSSIEN, "8*", "IE", "^TMP(\"PSS52P6\",$J)")
                TMP_J_LIST_PSSIEN_0 = ^TMP("DILIST", $J, PSSXX, 0)["^", 2
                TMP_J_LIST_B[$P(^TMP("DILIST", $J, PSSXX, 0)["^", 2), +PSSIEN] = ""
                CNT = 0
                PSS_1 = 0
                while PSS_1 in range(len(TMP_PSS52P6[$J][52.62])):
                    SETLTS_PSS52P6A()
                    CNT += 1
                    PSS_1 += 1
                TMP_J_LIST_PSSIEN_ELYTES_0 = CNT if CNT > 0 else "-1^NO DATA FOUND"

    K ^TMP("DILIST",$J), ^TMP("PSS52P6",$J)

def SYNONYM():
    SCR_S = ""
    if PSSFL > 0:
        ND = None
        SETSCRN_PSS52P6A()

    if PSSIEN > 0:
        PSSIEN2 = FIND1_DIC(52.6, "", "A", "`" + str(PSSIEN), "", SCR_S, "")
        if PSSIEN2 <= 0:
            TMP_J_LIST_0 = -1 + "^" + "NO DATA FOUND"
            return
        TMP_J_LIST_0 = 1
        GETS_DIQ(52.6, PSSIEN2, ".01;9*", "IE", "^TMP(\"PSS52P6\",$J)")
        PSS_1 = 0
        while PSS_1 in range(len(TMP_PSS52P6[$J][52.63])):
            SETSYN_PSS52P6A()
            CNT += 1
            PSS_1 += 1
        PSS_2 = 0
        while PSS_2 in range(len(TMP_PSS52P6[$J][52.6])):
            TMP_J_LIST_PSS_2_01 = TMP_PSS52P6[$J][52.6][PSS_2][.01]["I"]
            TMP_J_LIST_B[TMP_PSS52P6[$J][52.6][PSS_2][.01]["I"]] = +PSS_2
            PSS_2 += 1
        TMP_J_LIST_PSSIEN_SYN_0 = CNT if CNT > 0 else "-1^NO DATA FOUND"

    if PSSIEN <= 0 and PSSFT != "":
        if "??" in PSSFT:
            LOOP_PSS52P6A(4)
            return

        FIND_DIC(52.6, "", "@;.01;2", "QP", PSSFT, "", "B", SCR_S, "", "")
        if ^TMP("DILIST", $J, 0) == 0:
            TMP_J_LIST_0 = -1 + "^" + "NO DATA FOUND"
            return
        if ^TMP("DILIST", $J, 0) > 0:
            TMP_J_LIST_0 = +^TMP("DILIST", $J, 0)
            PSSXX = 0
            while PSSXX in range(len(^TMP("DILIST", $J))):
                PSSIEN = +^TMP("DILIST", $J, PSSXX, 0)
                TMP_PSS52P6[$J] = GETS_DIQ(52.6, PSSIEN, "9*", "IE", "^TMP(\"PSS52P6\",$J)")
                TMP_J_LIST_PSSIEN_0 = ^TMP("DILIST", $J, PSSXX, 0)["^", 2
                TMP_J_LIST_B[$P(^TMP("DILIST", $J, PSSXX, 0)["^", 2), +PSSIEN] = ""
                CNT = 0
                PSS_1 = 0
                while PSS_1 in range(len(TMP_PSS52P6[$J][52.63])):
                    SETSYN_PSS52P6A()
                    CNT += 1
                    PSS_1 += 1
                TMP_J_LIST_PSSIEN_SYN_0 = CNT if CNT > 0 else "-1^NO DATA FOUND"

    K ^TMP("DILIST",$J), ^TMP("PSS52P6",$J)

def DRGINFO():
    SCR_S = ""
    if PSSFL > 1:
        ND = None
        SETSCRN_PSS52P6A()

    if PSSIEN > 0:
        PSSIEN2 = FIND1_DIC(52.6, "", "A", "`" + str(PSSIEN), "", SCR_S, "")
        if PSSIEN2 <= 0:
            TMP_J_LIST_0 = -1 + "^" + "NO DATA FOUND"
            return
        TMP_J_LIST_0 = 1
        GETS_DIQ(52.6, PSSIEN2, ".01;10", "E", "^TMP(\"PSS52P6\",$J)")
        PSS_1 = 0
        while PSS_1 in range(len(TMP_PSS52P6[$J][52.6])):
            TMP_J_LIST_PSS_1_01 = TMP_PSS52P6[$J][52.6][PSS_1][.01]["E"]
            TMP_J_LIST_B[TMP_PSS52P6[$J][52.6][PSS_1][.01]["E"]] = +PSS_1
            PSS_3 = 0
            while PSS_3 in range(len(TMP_PSS52P6[$J][52.6][PSS_1][10])):
                SETDRI_PSS52P6A()
                PSS_3 += 1
            if not "^TMP($J,LIST,+PSS(1),\"DRGINF\")" in globals():
                TMP_J_LIST_PSS_1_DRGINF_0 = "-1^NO DATA FOUND"

    if PSSIEN <= 0 and PSSFT != "":
        if "??" in PSSFT:
            LOOP_PSS52P6A(5)
            return

        FIND_DIC(52.6, "", "@;.01", "QP", PSSFT, "", "B^C^D", SCR_S, "", "")
        if ^TMP("DILIST", $J, 0) == 0:
            TMP_J_LIST_0 = -1 + "^" + "NO DATA FOUND"
            return
        if ^TMP("DILIST", $J, 0) > 0:
            TMP_J_LIST_0 = +^TMP("DILIST", $J, 0)
            PSSXX = 0
            while PSSXX in range(len(^TMP("DILIST", $J))):
                PSSIEN = +^TMP("DILIST", $J, PSSXX, 0)
                TMP_PSS52P6[$J] = GETS_DIQ(52.6, PSSIEN, ".01;10", "E", "^TMP(\"PSS52P6\",$J)")
                PSS_1 = 0
                while PSS_1 in range(len(TMP_PSS52P6[$J][52.6])):
                    TMP_J_LIST_PSS_1_01 = TMP_PSS52P6[$J][52.6][PSS_1][.01]["E"]
                    TMP_J_LIST_B[TMP_PSS52P6[$J][52.6][PSS_1][.01]["E"]] = +PSS_1
                    PSS_3 = 0
                    while PSS_3 in range(len(TMP_PSS52P6[$J][52.6][PSS_1][10])):
                        SETDRI_PSS52P6A()
                        PSS_3 += 1
                    if not "^TMP($J,LIST,+PSS(1),\"DRGINF\")" in globals():
                        TMP_J_LIST_PSS_1_DRGINF_0 = "-1^NO DATA FOUND"

    K ^TMP("DILIST",$J), ^TMP("PSS52P6",$J)

def DRGIEN():
    SCR_S = ""
    if PSSFL > 0:
        ND = None
        SETSCRN_PSS52P6A()

    FIND_DIC(52.6, "", "@;.01", "QPX", PSS50, "", "AC", SCR_S, "", "")
    if ^TMP("DILIST", $J, 0) == 0:
        TMP_J_LIST_0 = -1 + "^" + "NO DATA FOUND"
        return
    if ^TMP("DILIST", $J, 0) > 0:
        TMP_J_LIST_0 = +^TMP("DILIST", $J, 0)
        XX = 0
        while XX in range(len(^TMP("DILIST", $J))):
            TMP_J_LIST_XX_01 = ^TMP("DILIST", $J, XX, 0)["^", 2
            TMP_J_LIST_AC[$P(^TMP("DILIST", $J, XX, 0)["^", 2), +^TMP("DILIST", $J, XX, 0)] = ""
            XX += 1

    K ^TMP("DILIST",$J)

def LOOKUP():
    SCR_S = ""
    PSSIEN, CNT, CNT2, CNT3, QFLG = None, None, None, None, None
    CNT3 = 0
    if PSSFL > 0:
        ND = None
        SETSCRN_PSS52P6A()

    if PSS50P7 > 0:
        FIND_DIC(52.6, "", "@;.01", "QPX", PSS50P7, "", "AOI", SCR_S, "", "")
        if ^TMP("DILIST", $J, 0) == 0:
            TMP_J_LIST_0 = -1 + "^" + "NO DATA FOUND"
            return
        PSSXX = 0
        while PSSXX in range(len(^TMP("DILIST", $J))):
            PSSIEN = +^TMP("DILIST", $J, PSSXX, 0)
            TMP_PSS52P6[$J] = GETS_DIQ(52.6, PSSIEN, ".01;14;6*;9*", "IE", "^TMP(\"PSS52P6\",$J)")
            PSS_1 = 0
            while PSS_1 in range(len(TMP_PSS52P6[$J][52.6])):
                TMP_J_LIST_PSS_1_01 = TMP_PSS52P6[$J][52.6][PSS_1][.01]["I"]
                TMP_J_LIST_B[TMP_PSS52P6[$J][52.6][PSS_1][.01]["I"]] = +PSS_1
                CNT3 += 1
                PSS_1 += 1
            TMP_J_LIST_0 = CNT3 if CNT3 > 0 else "-1^NO DATA FOUND"
            CNT = 0
            PSS_1 = 0
            while PSS_1 in range(len(TMP_PSS52P6[$J][52.61])):
                SETQCD_PSS52P6A()
                CNT += 1
                PSS_1 += 1
            TMP_J_LIST_PSSIEN_QCODE_0 = CNT if CNT > 0 else "-1^NO DATA FOUND"
            CNT2 = 0
            PSS_3 = 0
            while PSS_3 in range(len(TMP_PSS52P6[$J][52.63])):
                SETSYN2_PSS52P6A()
                CNT2 += 1
                PSS_3 += 1
            TMP_J_LIST_PSSIEN_SYN_0 = CNT2 if CNT2 > 0 else "-1^NO DATA FOUND"

    K ^TMP("DILIST",$J), ^TMP("PSS52P6",$J)

def POI():
    SCR_S = ""
    if PSSFL > 0:
        ND = None
        SETSCRN_PSS52P6A()

    FIND_DIC(52.6, "", "@;.01", "QPX", PSSOI, "", "AOI", SCR_S, "", "")
    if ^TMP("DILIST", $J, 0) == 0:
        TMP_J_LIST_0 = -1 + "^" + "NO DATA FOUND"
        return
    if ^TMP("DILIST", $J, 0) > 0:
        TMP_J_LIST_0 = +^TMP("DILIST", $J, 0)
        XX = 0
        while XX in range(len(^TMP("DILIST", $J))):
            TMP_J_LIST_XX_01 = ^TMP("DILIST", $J, XX, 0)["^", 2
            TMP_J_LIST_AOI[$P(^TMP("DILIST", $J, XX, 0)["^", 2), +^TMP("DILIST", $J, XX, 0)] = ""
            XX += 1

    K ^TMP("DILIST",$J)

def CHK():
    PSS = 0
    while PSS in range(len(PSS52P6[52.6])):
        PSS50 = PSS52P6[52.6][PSS][1]["I"] if PSS52P6[52.6][PSS][1]["I"] != "" else ""
        if +PSS50 <= 0:
            QFLG = 1
            continue
        PSSINACT = GETS_DIQ(50, +PSS50, "100", "I", "PSSINACT")
        PSS_4 = 0
        while PSS_4 in range(len(PSSINACT[50])):
            PSSINACT_1 = PSSINACT[50][PSS_4][1]["I"]
            if PSSINACT_1 != "" and PSSINACT_1 > PSSFL:
                QFLG = 1
            PSS_4 += 1

def main():
    ELYTES()
    SYNONYM()
    DRGINFO()
    DRGIEN()
    LOOKUP()
    POI()

main()