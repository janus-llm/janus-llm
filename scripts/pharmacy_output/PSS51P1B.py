# BIR/LDT - API FOR INFORMATION FROM FILE 51.1 CONT.; 5 Sep 03
# 1.0;PHARMACY DATA MANAGEMENT;**85,91,118**;9/30/97;Build 8

def SETZRO():
    global PSS, PSS51P1, LIST
    LIST = str(LIST)
    PSS = [int(PSS[i]) for i in range(len(PSS))]
    PSS51P1 = [int(PSS51P1[i]) for i in range(len(PSS51P1))]
    TMP_1 = {"I": PSS51P1[51.1][PSS[1]][.01]}
    TMP_2 = {"I": PSS51P1[51.1][PSS[1]][.01]}
    TMP_2["E"] = PSS51P1[51.1][PSS[1]][.01]
    TMP_3 = {"I": PSS51P1[51.1][PSS[1]][1]}
    TMP_4 = {"I": PSS51P1[51.1][PSS[1]][2]}
    TMP_5 = {"I": PSS51P1[51.1][PSS[1]][4]}
    if PSS51P1[51.1][PSS[1]][5]["I"] == "":
        TMP_6 = ""
    else:
        TMP_6 = PSS51P1[51.1][PSS[1]][5]["I"] + "^" + PSS51P1[51.1][PSS[1]][5]["E"]
    TMP_7 = {"I": PSS51P1[51.1][PSS[1]][6]}
    TMP_8 = {"I": PSS51P1[51.1][PSS[1]][2.5]}
    TMP_9 = {"I": PSS51P1[51.1][PSS[1]][8]}
    TMP_10 = {"I": PSS51P1[51.1][PSS[1]][8.1]}

    TMP_11 = {"I": TMP_1}
    TMP_11["B"] = TMP_2
    TMP_11["B"]["E"] = TMP_2["E"]

    TMP_12 = {"I": TMP_3}
    TMP_13 = {"I": TMP_4}
    TMP_14 = {"I": TMP_5}
    TMP_15 = {"I": TMP_6}
    TMP_16 = {"I": TMP_7}
    TMP_17 = {"I": TMP_8}
    TMP_18 = {"I": TMP_9}
    TMP_19 = {"I": TMP_10}

    TMP_20 = {"I": LIST}
    TMP_20["+PSS(1)"] = TMP_11
    TMP_20[1] = TMP_12
    TMP_20[2] = TMP_13
    TMP_20[4] = TMP_14
    TMP_20[5] = TMP_15
    TMP_20[6] = TMP_16
    TMP_20[2.5] = TMP_17
    TMP_20[8] = TMP_18
    TMP_20[8.1] = TMP_19

    TMP_21 = {"I": TMP_1}
    TMP_21["B"] = TMP_2
    TMP_21["B"]["E"] = TMP_2["E"]

    TMP_22 = {"I": TMP_3}

    if PSS51P1[51.1][PSS[1]][.01]["I"] == "":
        TMP_23 = ""
    else:
        TMP_23 = PSS51P1[51.1][PSS[1]][.01]["I"] + "^" + PSS51P1[51.1][PSS[1]][.01]["E"]

    TMP_24 = {"I": TMP_23}
    TMP_24["B"] = TMP_2
    TMP_24["B"]["E"] = TMP_2["E"]

    TMP_25 = {"I": TMP_3}

    TMP_26 = {"I": TMP_4}

    TMP_27 = {"I": TMP_5}

    TMP_28 = {"I": TMP_6}

    TMP_29 = {"I": TMP_7}

    TMP_30 = {"I": TMP_8}

    TMP_31 = {"I": TMP_9}

    TMP_32 = {"I": TMP_10}

    TMP_33 = {"I": LIST}
    TMP_33["+PSS(1)"] = TMP_24
    TMP_33[1] = TMP_25

    TMP_34 = {"I": TMP_1}
    TMP_34["WARD"] = TMP_33

    TMP_35 = {"I": TMP_2}

    TMP_36 = {"I": TMP_3}

    return

def SETWARD():
    global PSS, PSS51P1, LIST
    LIST = str(LIST)
    PSS = [int(PSS[i]) for i in range(len(PSS))]
    PSS51P1 = [int(PSS51P1[i]) for i in range(len(PSS51P1))]
    TMP_37 = {"I": TMP_35}
    TMP_37[".01"] = PSS51P1[51.11][PSS[2]][.01]
    TMP_38 = {"I": PSS51P1[51.11][PSS[2]][1]}

    TMP_39 = {"I": LIST}
    TMP_39["+PSS(1)"] = TMP_34
    TMP_39["+PSS(2)"] = TMP_37
    TMP_39["+PSS(2)"][1] = TMP_38

    return

def SETLOC():
    global PSS, PSS51P1, LIST, PSSIEN
    LIST = str(LIST)
    PSS = [int(PSS[i]) for i in range(len(PSS))]
    PSS51P1 = [int(PSS51P1[i]) for i in range(len(PSS51P1))]
    TMP_40 = {"I": TMP_35}
    TMP_40[".01"] = PSS51P1[51.17][PSS[1]][.01]
    TMP_41 = {"I": PSS51P1[51.17][PSS[1]][1]}
    TMP_42 = {"I": PSS51P1[51.17][PSS[1]][2]}

    TMP_43 = {"I": LIST}
    TMP_43["+PSSIEN"] = PSSIEN
    TMP_43["HOSP"] = TMP_40
    TMP_43["HOSP"]["+PSS(1)"] = TMP_41
    TMP_43["HOSP"]["+PSS(1)"][1] = TMP_42

    return

def LOOP(PSSLP):
    global CNT, PSS, LIST
    CNT = 0
    PSS = [int(PSS[i]) for i in range(len(PSS))]
    LIST = str(LIST)
    PSS[3] = 0
    while True:
        PSS[3] = PSS[3] + 1
        if not PSS[3]:
            break
        eval(PSSLP)

    TMP_44 = {"I": LIST}
    TMP_44[0] = CNT

    return

def SETWRD2():
    global PSS, PSSIEN, PSS51P1, LIST
    LIST = str(LIST)
    PSS = [int(PSS[i]) for i in range(len(PSS))]
    PSSIEN = int(PSSIEN)
    PSS51P1 = [int(PSS51P1[i]) for i in range(len(PSS51P1))]
    TMP_45 = {"I": TMP_37}
    TMP_45[".01"] = PSS51P1[51.11][PSS[2]][.01]
    TMP_46 = {"I": PSS51P1[51.11][PSS[2]][1]}

    TMP_47 = {"I": LIST}
    TMP_47["+PSSIEN"] = PSSIEN
    TMP_47["WARD"] = TMP_45
    TMP_47["WARD"]["+PSS(2)"] = TMP_46
    TMP_47["WARD"][0] = 1

    return

def _1():
    global PSS, PSS51P1, LIST, PSSIEN, CNT
    PSS = [int(PSS[i]) for i in range(len(PSS))]
    PSS51P1 = [int(PSS51P1[i]) for i in range(len(PSS51P1))]
    TMP_48 = {"I": PSS[3]}
    TMP_48["PSS(3)"] = PSS[3]
    TMP_49 = {"I": PSS[3]}
    TMP_50 = TMP_48
    TMP_50[0] = ".01;1;2;4;5;6;2.5;8;8.1"
    TMP_51 = {"IE": PSS51P1}
    TMP_51[51.1] = {TMP_50: ""}
    TMP_52 = {"I": PSS[3]}
    TMP_52[51.1] = TMP_51[51.1]
    TMP_53 = {"IE": PSS51P1}
    TMP_53[51.1] = {TMP_50: ""}
    TMP_53[51.1][TMP_48] = ""
    TMP_54 = {"I": 0}
    TMP_54[51.1] = TMP_53[51.1]
    TMP_55 = {"I": PSS[3]}
    TMP_55[51.1] = TMP_53[51.1]
    TMP_56 = {"I": PSS[1]}
    TMP_56[51.1] = TMP_55[51.1]
    TMP_57 = {"I": 0}
    TMP_57[51.1] = TMP_56[51.1]
    TMP_58 = {"I": PSS[1]}
    TMP_58[51.1] = TMP_57[51.1]
    TMP_58[51.1][TMP_56] = ""
    TMP_59 = {"I": CNT}
    TMP_59[51.1] = TMP_58[51.1]
    TMP_59[51.1][TMP_56] = ""
    TMP_59[51.1][TMP_56][.01] = PSS51P1[51.1][PSS[1]][.01]["I"]
    TMP_59[51.1][TMP_56][.01]["I"] = PSS51P1[51.1][PSS[1]][.01]["I"]

    TMP_60 = {"I": CNT}
    TMP_60[51.1] = TMP_59[51.1]
    TMP_60[51.1][TMP_56] = ""
    TMP_60[51.1][TMP_56][.01] = PSS51P1[51.1][PSS[1]][.01]["I"]
    TMP_60[51.1][TMP_56]["I"] = PSS51P1[51.1][PSS[1]][.01]["I"]
    TMP_60[51.1][TMP_56]["E"] = PSS51P1[51.1][PSS[1]][.01]["E"]

    TMP_61 = {"I": TMP_1}
    TMP_61[51.1] = TMP_60[51.1]
    TMP_61[51.1][TMP_56] = ""
    TMP_61[51.1][TMP_56][.01] = PSS51P1[51.1][PSS[1]][.01]["I"]
    TMP_61[51.1][TMP_56]["I"] = PSS51P1[51.1][PSS[1]][.01]["I"]
    TMP_61[51.1][TMP_56]["E"] = PSS51P1[51.1][PSS[1]][.01]["E"]

    TMP_62 = {"I": TMP_3}
    TMP_62[51.1] = TMP_61[51.1]
    TMP_62[51.1][TMP_56] = ""
    TMP_62[51.1][TMP_56][1] = PSS51P1[51.1][PSS[1]][1]["I"]

    TMP_63 = {"I": TMP_4}
    TMP_63[51.1] = TMP_62[51.1]
    TMP_63[51.1][TMP_56] = ""
    TMP_63[51.1][TMP_56][2] = PSS51P1[51.1][PSS[1]][2]["I"]

    TMP_64 = {"I": TMP_5}
    TMP_64[51.1] = TMP_63[51.1]
    TMP_64[51.1][TMP_56] = ""
    TMP_64[51.1][TMP_56][4] = PSS51P1[51.1][PSS[1]][4]["I"]

    if PSS51P1[51.1][PSS[1]][5]["I"] == "":
        TMP_65 = ""
    else:
        TMP_65 = PSS51P1[51.1][PSS[1]][5]["I"] + "^" + PSS51P1[51.1][PSS[1]][5]["E"]

    TMP_66 = {"I": TMP_65}
    TMP_66[51.1] = TMP_64[51.1]
    TMP_66[51.1][TMP_56] = ""
    TMP_66[51.1][TMP_56][5] = PSS51P1[51.1][PSS[1]][5]["I"]

    TMP_67 = {"I": TMP_7}
    TMP_67[51.1] = TMP_66[51.1]
    TMP_67[51.1][TMP_56] = ""
    TMP_67[51.1][TMP_56][6] = PSS51P1[51.1][PSS[1]][6]["I"]

    TMP_68 = {"I": TMP_17}
    TMP_68[51.1] = TMP_67[51.1]
    TMP_68[51.1][TMP_56] = ""
    TMP_68[51.1][TMP_56][2.5] = PSS51P1[51.1][PSS[1]][2.5]["I"]

    TMP_69 = {"I": TMP_18}
    TMP_69[51.1] = TMP_68[51.1]
    TMP_69[51.1][TMP_56] = ""
    TMP_69[51.1][TMP_56][8] = PSS51P1[51.1][PSS[1]][8]["I"]

    TMP_70 = {"I": TMP_19}
    TMP_70[51.1] = TMP_69[51.1]
    TMP_70[51.1][TMP_56] = ""
    TMP_70[51.1][TMP_56][8.1] = PSS51P1[51.1][PSS[1]][8.1]["I"]

    TMP_71 = {"I": LIST}
    TMP_71[51.1] = TMP_70[51.1]
    TMP_71[51.1][TMP_56] = ""
    TMP_71[51.1][TMP_56][.01] = PSS51P1[51.1][PSS[1]][.01]["I"]
    TMP_71[51.1][TMP_56]["B"] = TMP_2
    TMP_71[51.1][TMP_56]["B"]["E"] = TMP_2["E"]

    return

def _2():
    global PSS, PSSIEN2, PSS51P1, LIST, CNT, PSSWDIEN
    PSS = [int(PSS[i]) for i in range(len(PSS))]
    PSS51P1 = [int(PSS51P1[i]) for i in range(len(PSS51P1))]
    LIST = str(LIST)
    PSSWDIEN = int(PSSWDIEN)
    TMP_72 = {"I": LIST}
    TMP_72["PSS51P1"] = PSS51P1
    TMP_72[51.1] = {TMP_49: ""}
    TMP_73 = {"I": PSS[3]}
    TMP_73[51.1] = TMP_72[51.1]
    TMP_73[51.1][TMP_49] = ""
    TMP_73[51.1][TMP_49][.01] = ""
    TMP_73[51.1][TMP_49][.01]["I"] = ""
    TMP_73[51.1][TMP_49][.01]["E"] = ""

    TMP_74 = {"I": PSS[3]}
    TMP_74[51.1] = TMP_73[51.1]
    TMP_74[51.1][TMP_49] = ""
    TMP_74[51.1][TMP_49][.01] = ""
    TMP_74[51.1][TMP_49][.01]["I"] = ""
    TMP_74[51.1][TMP_49][.01]["E"] = ""

    TMP_75 = {"I": PSS[3]}
    TMP_75[51.1] = TMP_73[51.1]
    TMP_75[51.1][TMP_49] = ""
    TMP_75[51.1][TMP_49][.01] = ""
    TMP_75[51.1][TMP_49][.01]["I"] = ""
    TMP_75[51.1][TMP_49][.01]["E"] = ""

    TMP_76 = {"I": CNT}
    TMP_76[51.1] = TMP_75[51.1]
    TMP_76[51.1][TMP_49] = ""
    TMP_76[51.1][TMP_49][.01] = ""
    TMP_76[51.1][TMP_49][.01]["I"] = ""
    TMP_76[51.1][TMP_49][.01]["E"] = ""

    TMP_77 = {"I": TMP_1}
    TMP_77[51.1] = TMP_76[51.1]
    TMP_77[51.1][TMP_49] = ""
    TMP_77[51.1][TMP_49][.01] = ""
    TMP_77[51.1][TMP_49][.01]["I"] = ""
    TMP_77[51.1][TMP_49][.01]["E"] = ""

    TMP_78 = {"I": CNT}
    TMP_78[51.1] = TMP_77[51.1]
    TMP_78[51.1][TMP_49] = ""
    TMP_78[51.1][TMP_49][.01] = ""
    TMP_78[51.1][TMP_49][.01]["I"] = ""
    TMP_78[51.1][TMP_49][.01]["E"] = ""

    TMP_79 = {"I": PSS[1]}
    TMP_79[51.1] = TMP_78[51.1]
    TMP_79[51.1][TMP_49] = ""
    TMP_79[51.1][TMP_49][.01] = PSS51P1[51.1][PSS[4]][.01]["I"]

    TMP_80 = {"I": CNT1}
    TMP_80[51.1] = TMP_79[51.1]
    TMP_80[51.1][TMP_49] = ""
    TMP_80[51.1][TMP_49][1] = PSS51P1[51.1][PSS[4]][1]["I"]

    TMP_81 = {"I": LIST}
    TMP_81["PSSIEN"] = PSSIEN
    TMP_81["WARD"] = TMP_80
    TMP_81["WARD"][0] = TMP_80

    return

def _3():
    global PSS, PSS51P1, LIST, PSSIEN, CNT1
    PSS = [int(PSS[i]) for i in range(len(PSS))]
    PSS51P1 = [int(PSS51P1[i]) for i in range(len(PSS51P1))]
    LIST = str(LIST)
    PSSIEN = int(PSSIEN)
    TMP_82 = {"I": LIST}
    TMP_82["+PSSIEN"] = PSSIEN
    TMP_82["HOSP"] = TMP_40
    TMP_82["HOSP"]["+PSS(1)"] = TMP_41
    TMP_82["HOSP"]["+PSS(1)"][1] = TMP_42

    TMP_83 = {"I": CNT1}
    TMP_83["+PSSIEN"] = PSSIEN
    TMP_83["HOSP"] = TMP_40
    TMP_83["HOSP"]["+PSS(1)"] = TMP_41
    TMP_83["HOSP"]["+PSS(1)"][1] = TMP_42

    TMP_84 = {"I": PSS[2]}
    TMP_84["+PSSIEN"] = PSSIEN
    TMP_84["HOSP"] = TMP_40
    TMP_84["HOSP"]["+PSS(1)"] = TMP_41
    TMP_84["HOSP"]["+PSS(1)"][1] = TMP_42

    return

def _4():
    global PSS, PSS51P1, LIST, CNT
    PSS = [int(PSS[i]) for i in range(len(PSS))]
    PSS51P1 = [int(PSS51P1[i]) for i in range(len(PSS51P1))]
    LIST = str(LIST)
    TMP_85 = {"I": PSS[3]}
    TMP_85[51.1] = TMP_72[51.1]
    TMP_85[51.1][TMP_49] = ""
    TMP_85[51.1][TMP_49][.01] = PSS51P1[51.1][PSS[4]][.01]["I"]

    TMP_86 = {"I": CNT}
    TMP_86[51.1] = TMP_85[51.1]
    TMP_86[51.1][TMP_49] = ""
    TMP_86[51.1][TMP_49][.01] = PSS51P1[51.1][PSS[4]][.01]["I"]

    TMP_87 = {"I": TMP_85}
    TMP_87[51.1] = TMP_86[51.1]
    TMP_87[51.1][TMP_49] = ""
    TMP_87[51.1][TMP_49][.01] = PSS51P1[51.1][PSS[4]][.01]["I"]

    TMP_88 = {"I": CNT}
    TMP_88[51.1] = TMP_87[51.1]
    TMP_88[51.1][TMP_49] = ""
    TMP_88[51.1][TMP_49][.01] = PSS51P1[51.1][PSS[4]][.01]["I"]

    return

def _5():
    global PSS, PSS51P1, LIST, PSSPP, PSSTYP, PSSWDIEN, PSSFREQ, CNT, PSSIEN
    PSS = [int(PSS[i]) for i in range(len(PSS))]
    PSS51P1 = [int(PSS51P1[i]) for i in range(len(PSS51P1))]
    LIST = str(LIST)
    PSSPP = str(PSSPP)
    PSSTYP = str(PSSTYP)
    PSSFREQ = str(PSSFREQ)
    TMP_89 = {"I": PSS[3]}
    TMP_89[51.1] = {"@": ""}
    TMP_89[51.1][".01"] = ".01;1;2;2.5;4;5IE;8"
    TMP_90 = {"I": PSS[3]}
    TMP_90[51.1] = {"Q": ""}
    TMP_90[51.1]["`_PSS(3)"] = ""
    TMP_90[51.1][TMP_49] = ""
    TMP_90[51.1][TMP_49]["@"] = ""

    TMP_91 = {"I": PSS[3]}
    TMP_91[51.1] = {"Q": ""}
    TMP_91[51.1]["`_PSS(3)"] = ""
    TMP_91[51.1][TMP_49] = ""
    TMP_91[51.1][TMP_49]["@"] = ""

    TMP_92 = {"I": CNT}
    TMP_92[51.1] = TMP_91[51.1]
    TMP_92[51.1][TMP_49] = ""
    TMP_92[51.1][TMP_49]["@"] = ""

    TMP_93 = {"I": TMP_1}
    TMP_93[51.1] = TMP_92[51.1]
    TMP_93[51.1][TMP_49] = ""
    TMP_93[51.1][TMP_49]["@"] = ""

    TMP_94 = {"I": PSS[3]}
    TMP_94[51.1] = TMP_90[51.1]
    TMP_94[51.1][TMP_49] = ""
    TMP_94[51.1][TMP_49][.01] = PSS51P1[51.1][PSS[3]][.01]

    TMP_95 = {"I": CNT}
    TMP_95[51.1] = TMP_94[51.1]
    TMP_95[51.1][TMP_49] = ""
    TMP_95[51.1][TMP_49][.01] = PSS51P1[51.1][PSS[3]][.01]

    TMP_96 = {"I": PSS[3]}
    TMP_96[51.1] = TMP_95[51.1]
    TMP_96[51.1][TMP_49] = ""
    TMP_96[51.1][TMP_49][.01] = PSS51P1[51.1][PSS[3]][.01]

    TMP_97 = {"I": CNT}
    TMP_97[51.1] = TMP_96[51.1]
    TMP_97[51.1][TMP_49] = ""
    TMP_97[51.1][TMP_49][.01] = PSS51P1[51.1][PSS[3]][.01]

    TMP_98 = {"I": TMP_50}
    TMP_98[51.1] = TMP_97[51.1]
    TMP_98[51.1][TMP_49] = ""
    TMP_98[51.1][TMP_49][.01] = PSS51P1[51.1][PSS[3]][.01]

    TMP_99 = {"I": TMP_50}
    TMP_99[51.1] = TMP_98[51.1]
    TMP_99[51.1][TMP_49] = ""
    TMP_99[51.1][TMP_49][.01] = PSS51P1[51.1][PSS[3]][.01]

    TMP_100 = {"I": PSS[3]}
    TMP_100[51.1] = TMP_99[51.1]
    TMP_100[51.1][TMP_49] = ""
    TMP_100[51.1][TMP_49][.01] = PSS51P1[51.1][PSS[3]][.01]

    TMP_101 = {"I": CNT}
    TMP_101[51.1] = TMP_100[51.1]
    TMP_101[51.1][TMP_49] = ""
    TMP_101[51.1][TMP_49][.01] = PSS51P1[51.1][PSS[3]][.01]

    TMP_102 = {"I": PSS[3]}
    TMP_102[51.1] = TMP_101[51.1]
    TMP_102[51.1][TMP_49] = ""
    TMP_102[51.1][TMP_49][.01] = PSS51P1[51.1][PSS[3]][.01]

    TMP_103 = {"I": CNT}
    TMP_103[51.1] = TMP_102[51.1]
    TMP_103[51.1][TMP_49] = ""
    TMP_103[51.1][TMP_49][.01] = PSS51P1[51.1][PSS[3]][.01]

    TMP_104 = {"I": TMP_50}
    TMP_104[51.1] = TMP_103[51.1]
    TMP_104[51.1][TMP_49] = ""
    TMP_104[51.1][TMP_49][.01] = PSS51P1[51.1][PSS[3]][.01]

    TMP_105 = {"I": CNT}
    TMP_105[51.1] = TMP_104[51.1]
    TMP_105[51.1][TMP_49] = ""
    TMP_105[51.1][TMP_49][.01] = PSS51P1[51.1][PSS[3]][.01]

    TMP_106 = {"I": PSS[3]}
    TMP_106[51.1] = TMP_105[51.1]
    TMP_106[51.1][TMP_49] = ""
    TMP_106[51.1][TMP_49][.01] = PSS51P1[51.1][PSS[3]][.01]

    TMP_107 = {"I": CNT}
    TMP_107[51.1] = TMP_106[51.1]
    TMP_107[51.1][TMP_49] = ""
    TMP_107[51.1][TMP_49][.01] = PSS51P1[51.1][PSS[3]][.01]

    TMP_108 = {"I": PSS[3]}
    TMP_108[51.1] = TMP_107[51.1]
    TMP_108[51.1][TMP_49] = ""
    TMP_108[51.1][TMP_49][.01] = PSS51P1[51.1][PSS[3]][.01]

    TMP_109 = {"I": CNT}
    TMP_109[51.1] = TMP_108[51.1]
    TMP_109[51.1][TMP_49] = ""
    TMP_109[51.1][TMP_49][.01] = PSS51P1[51.1][PSS[3]][.01]

    TMP_110 = {"I": PSS[3]}
    TMP_110[51.1] = TMP_109[51.1]
    TMP_110[51.1][TMP_49] = ""
    TMP_110[51.1][TMP_49][.01] = PSS51P1[51.1][PSS[3]][.01]

    TMP_111 = {"I": CNT}
    TMP_111[51.1] = TMP_110[51.1]
    TMP_111[51.1][TMP_49] = ""
    TMP_111[51.1][TMP_49][.01] = PSS51P1[51.1][PSS[3]][.01]

    TMP_112 = {"I": PSS[3]}
    TMP_112[51.1] = TMP_111[51.1]
    TMP_112[51.1][TMP_49] = ""
    TMP_112[51.1][TMP_49][.01] = PSS51P1[51.1][PSS[3]][.01]

    TMP_113 = {"I": CNT}
    TMP_113[51.1] = TMP_112[51.1]
    TMP_113[51.1][TMP_49] = ""
    TMP_113[51.1][TMP_49][.01] = PSS51P1[51.1][PSS[3]][.01]

    TMP_114 = {"I": PSS[3]}
    TMP_114[51.1] = TMP_113[51.1]
    TMP_114[51.1][TMP_49] = ""
    TMP_114[51.1][TMP_49][.01] = PSS51P1[51.1][PSS[3]][.01]

    TMP_115 = {"I": CNT}
    TMP_115[51.1] = TMP_114[51.1]
    TMP_115[51.1][TMP_49] = ""
    TMP_115[51.1][TMP_49][.01] = PSS51P1[51.1][PSS[3]][.01]

    TMP_116 = {"I": PSS[3]}
    TMP_116[51.1] = TMP_115[51.1]
    TMP_116[51.1][TMP_49] = ""
    TMP_116[51.1][TMP_49][.01] = PSS51P1[51.1][PSS[3]][.01]

    TMP_117 = {"I": CNT}
    TMP_117[51.1] = TMP_116[51.1]
    TMP_117[51.1][TMP_49] = ""
    TMP_117[51.1][TMP_49][.01] = PSS51P1[51.1][PSS[3]][.01]

    TMP_118 = {"I": PSS[3]}
    TMP_118[51.1] = TMP_117[51.1]
    TMP_118[51.1][TMP_49] = ""
    TMP_118[51.1][TMP_49][.01] = PSS51P1[51.1][PSS[3]][.01]

    TMP_119 = {"I": CNT}
    TMP_119[51.1] = TMP_118[51.1]
    TMP_119[51.1][TMP_49] = ""
    TMP_119[51.1][TMP_49][.01] = PSS51P1[51.1][PSS[3]][.01]

    TMP_120 = {"I": PSS[3]}
    TMP_120[51.1] = TMP_119[51.1]
    TMP_120[51.1][TMP_49] = ""
    TMP_120[51.1][TMP_49][.01] = PSS51P1[51.1][PSS[3]][.01]

    TMP_121 = {"I": CNT}
    TMP_121[51.1] = TMP_120[51.1]
    TMP_121[51.1][TMP_49] = ""
    TMP_121[51.1][TMP_49][.01] = PSS51P1[51.1][PSS[3]][.01]

    TMP_122 = {"I": PSS[3]}
    TMP_122[51.1] = TMP_121[51.1]
    TMP_122[51.1][TMP_49] = ""
    TMP_122[51.1][TMP_49][.01] = PSS51P1[51.1][PSS[3]][.01]

    TMP_123 = {"I": CNT}
    TMP_123[51.1] = TMP_122[51.1]
    TMP_123[51.1][TMP_49] = ""
    TMP_123[51.1][TMP_49][.01] = PSS51P1[51.1][PSS[3]][.01]

    TMP_124 = {"I": PSS[3]}
    TMP_124[51.1] = TMP_123[51.1]
    TMP_124[51.1][TMP_49] = ""
    TMP_124[51.1][TMP_49][.01] = PSS51P1[51.1][PSS[3]][.01]

    TMP_125 = {"I": CNT}
    TMP_125[51.1] = TMP_124[51.1]
    TMP_125[51.1][TMP_49] = ""
    TMP_125[51.1][TMP_49][.01] = PSS51P1[51.1][PSS[3]][.01]

    TMP_126 = {"I": PSS[3]}
    TMP_126[51.1] = TMP_125[51.1]
    TMP_126[51.1][TMP_49] = ""
    TMP_126[51.1][TMP_49][.01] = PSS51P1[51.1][PSS[3]][.01]

    TMP_127 = {"I": CNT}
    TMP_127[51.1] = TMP_126[51.1]
    TMP_127[51.1][TMP_49] = ""
    TMP_127[51.1][TMP_49][.01] = PSS51P1[51.1][PSS[3]][.01]

    TMP_128 = {"I": PSS[3]}
    TMP_128[51.1] = TMP_127[51.1]
    TMP_128[51.1][TMP_49] = ""
    TMP_128[51.1][TMP_49][.01] = PSS51P1[51.1][PSS[3]][.01]

    TMP_129 = {"I": CNT}
    TMP_129[51.1] = TMP_128[51.1]
    TMP_129[51.1][TMP_49] = ""
    TMP_129[51.1][TMP_49][.01] = PSS51P1[51.1][PSS[3]][.01]

    TMP_130 = {"I": PSS[3]}
    TMP_130[51.1] = TMP_129[51.1]
    TMP_130[51.1][TMP_49] = ""
    TMP_130[51.1][TMP_49][.01] = PSS51P1[51.1][PSS[3]][.01]

    TMP_131 = {"I": CNT}
    TMP_131[51.1] = TMP_130[51.1]
    TMP_131[51.1][TMP_49] = ""
    TMP_131[51.1][TMP_49][.01] = PSS51P1[51.1][PSS[3]][.01]

    TMP_132 = {"I": PSS[3]}
    TMP_132[51.1] = TMP_131[51.1]
    TMP_132[51.1][TMP_49] = ""
    TMP_132[51.1][TMP_49][.01] = PSS51P1[51.1][PSS[3]][.01]

    TMP_133 = {"I": CNT}
    TMP_133[51.1] = TMP_132[51.1]
    TMP_133[51.1][TMP_49] = ""
    TMP_133[51.1][TMP_49][.01] = PSS51P1[51.1][PSS[3]][.01]

    TMP_134 = {"I": PSS[3]}
    TMP_134[51.1] = TMP_133[51.1]
    TMP_134[51.1][TMP_49] = ""
    TMP_134[51.1][TMP_49][.01] = PSS51P1[51.1][PSS[3]][.01]

    TMP_135 = {"I": CNT}
    TMP_135[51.1] = TMP_134[51.1]
    TMP_135[51.1][TMP_49] = ""
    TMP_135[51.1][TMP_49][.01] = PSS51P1[51.1][PSS[3]][.01]

    TMP_136 = {"I": PSS[3]}
    TMP_136[51.1] = TMP_135[51.1]
    TMP_136[51.1][TMP_49] = ""
    TMP_136[51.1][TMP_49][.01] = PSS51P1[51.1][PSS[3]][.01]

    TMP_137 = {"I": CNT}
    TMP_137[51.1] = TMP_136[51.1]
    TMP_137[51.1][TMP_49] = ""
    TMP_137[51.1][TMP_49][.01] = PSS51P1[51.1][PSS[3]][.01]

    TMP_138 = {"I": PSS[3]}
    TMP_138[51.1] = TMP_137[51.1]
    TMP_138[51.1][TMP_49] = ""
    TMP_138[51.1][TMP_49][.01] = PSS51P1[51.1][PSS[3]][.01]

    TMP_139 = {"I": CNT}
    TMP_139[51.1] = TMP_138[51.1]
    TMP_139[51.1][TMP_49] = ""
    TMP_139[51.1][TMP_49][.01] = PSS51P1[51.1][PSS[3]][.01]

    TMP_140 = {"I": PSS[3]}
    TMP_140[51.1] = TMP_139[51.1]
    TMP_140[51.1][TMP_49] = ""
    TMP_140[51.1][TMP_49][.01] = PSS51P1[51.1][PSS[3]][.01]

    TMP_141 = {"I": CNT}
    TMP_141[51.1] = TMP_140[51.1]
    TMP_141[51.1][TMP_49] = ""
    TMP_141[51.1][TMP_49][.01] = PSS51P1[51.1][PSS[3]][.01]

    TMP_142 = {"I": PSS[3]}
    TMP_142[51.1] = TMP_141[51.1]
    TMP_142[51.1][TMP_49] = ""
    TMP_142[51.1][TMP_49][.01] = PSS51P1[51.1][PSS[3]][.01]

    TMP_143 = {"I": CNT}
    TMP_143[51.1] = TMP_142[51.1]
    TMP_143[51.1][TMP_49] = ""
    TMP_143[51.1][TMP_49][.01] = PSS51P1[51.1][PSS[3]][.01]

    TMP_144 = {"I": PSS[3]}
    TMP_144[51.1] = TMP_143[51.1]
    TMP_144[51.1][TMP_49] = ""
    TMP_144[51.1][TMP_49][.01] = PSS51P1[51.1][PSS[3]][.01]

    TMP_145 = {"I": CNT}
    TMP_145[51.1] = TMP_144[51.1]
    TMP_145[51.1][TMP_49] = ""
    TMP_145[51.1][TMP_49][.01] = PSS51P1[51.1][PSS[3]][.01]

    TMP_146 = {"I": PSS[3]}
    TMP_146[51.1] = TMP_145[51.1]
    TMP_146[51.1][TMP_49] = ""
    TMP_146[51.1][TMP_49][.01] = PSS51P1[51.1][PSS[3]][.01]

    TMP_147 = {"I": CNT}
    TMP_147[51.1] = TMP_146[51.1]
    TMP_147[51.1][TMP_49] = ""
    TMP_147[51.1][TMP_49][.01] = PSS51P1[51.1][PSS[3]][.01]

    TMP_148 = {"I": PSS[3]}
    TMP_148[51.1] = TMP_147[51.1]
    TMP_148[51.1][TMP_49] = ""
    TMP_148[51.1][TMP_49][.01] = PSS51P1[51.1][PSS[3]][.01]

    TMP_149 = {"I": CNT}
    TMP_149[51.1] = TMP_148[51.1]
    TMP_149[51.1][TMP_49] = ""
    TMP_149[51.1][TMP_49][.01] = PSS51P1[51.1][PSS[3]][.01]

    TMP_150 = {"I": PSS[3]}
    TMP_150[51.1] = TMP_149[51.1]
    TMP_150[51.1][TMP_49] = ""
    TMP_150[51.1][TMP_49][.01] = PSS51P1[51.1][PSS[3]][.01]

    TMP_151 = {"I": CNT}
    TMP_151[51.1] = TMP_150[51.1]
    TMP_151[51.1][TMP_49] = ""
    TMP_151[51.1][TMP_49][.01] = PSS51P1[51.1][PSS[3]][.01]

    TMP_152 = {"I": PSS[3]}
    TMP_152[51.1] = TMP_151[51.1]
    TMP_152[51.1][TMP_49] = ""
    TMP_152[51.1][TMP_49][.01] = PSS51P1[51.1][PSS[3]][.01]

    TMP_153 = {"I": CNT}
    TMP_153[51.1] = TMP_152[51.1]
    TMP_153[51.1][TMP_49] = ""
    TMP_153[51.1][TMP_49][.01] = PSS51P1[51.1][PSS[3]][.01]

    TMP_154 = {"I": PSS[3]}
    TMP_154[51.1] = TMP_153[51.1]
    TMP_154[51.1][TMP_49] = ""
    TMP_154[51.1][TMP_49][.01] = PSS51P1[51.1][PSS[3]][.01]

    TMP_155 = {"I": CNT}
    TMP_155[51.1] = TMP_154[51.1]
    TMP_155[51.1][TMP_49] = ""
    TMP_155[51.1][TMP_49][.01] = PSS51P1[51.1][PSS[3]][.01]

    TMP_156 = {"I": PSS[3]}
    TMP_156[51.1] = TMP_155[51.1]
    TMP_156[51.1][TMP_49] = ""
    TMP_156[51.1][TMP_49][.01] = PSS51P1[51.1][PSS[3]][.01]

    TMP_157 = {"I": CNT}
    TMP_157[51.1] = TMP_156[51.1]
    TMP_157[51.1][TMP_49] = ""
    TMP_157[51.1][TMP_49][.01] = PSS51P1[51.1][PSS[3]][.01]

    TMP_158 = {"I": PSS[3]}
    TMP_158[51.1] = TMP_157[51.1]
    TMP_158[51.1][TMP_49] = ""
    TMP_158[51.1][TMP_49][.01] = PSS51P1[51.1][PSS[3]][.01]

    TMP_159 = {"I": CNT}
    TMP_159[51.1] = TMP_158[51.1]
    TMP_159[51.1][TMP_49] = ""
    TMP_159[51.1][TMP_49][.01] = PSS51P1[51.1][PSS[3]][.01]

    TMP_160 = {"I": PSS[3]}
    TMP_160[51.1] = TMP_159[51.1]
    TMP_160[51.1][TMP_49] = ""
    TMP_160[51.1][TMP_49][.01] = PSS51P1[51.1][PSS[3]][.01]

    TMP_161 = {"I": CNT}
    TMP_161[51.1] = TMP_160[51.1]
    TMP_161[51.1][TMP_49] = ""
    TMP_161[51.1][TMP_49][.01] = PSS51P1[51.1][PSS[3]][.01]

    TMP_162 = {"I": PSS[3]}
    TMP_162[51.1] = TMP_161[51.1]
    TMP_162[51.1][TMP_49] = ""
    TMP_162[51.1][TMP_49][.01] = PSS51P1[51.1][PSS[3]][.01]

    TMP_163 = {"I": CNT}
    TMP_163[51.1] = TMP_162[51.1]
    TMP_163[51.1][TMP_49] = ""
    TMP_163[51.1][TMP_49][.01] = PSS51P1[51.1][PSS[3]][.01]

    TMP_164 = {"I": PSS[3]}
    TMP_164[51.1] = TMP_163[51.1]
    TMP_164[51.1][TMP_49] = ""
    TMP_164[51.1][TMP_49][.01] = PSS51P1[51.1][PSS[3]][.01]

    TMP_165 = {"I": CNT}
    TMP_165[51.1] = TMP_164[51.1]
    TMP_165[51.1][TMP_49] = ""
    TMP_165[51.1][TMP_49][.01] = PSS51P1[51.1][PSS[3]][.01]

    TMP_166 = {"I": PSS[3]}
    TMP_166[51.1] = TMP_165[51.1]
    TMP_166[51.1][TMP_49] = ""
    TMP_166[51.1][TMP_49][.01] = PSS51P1[51.1][PSS[3]][.01]

    TMP_167 = {"I": CNT}
    TMP_167[51.1] = TMP_166[51.1]
    TMP_167[51.1][TMP_49] = ""
    TMP_167[51.1][TMP_49][.01] = PSS51P1[51.1][PSS[3]][.01]

    TMP_168 = {"I": PSS[3]}
    TMP_168[51.1] = TMP_167[51.1]
    TMP_168[51.1][TMP_49] = ""
    TMP_168[51.1][TMP_49][.01] = PSS51P1[51.1][PSS[3]][.01]

    TMP_169 = {"I": CNT}
    TMP_169[51.1] = TMP_168[51.1]
    TMP_169[51.1][TMP_49] = ""
    TMP_169[51.1][TMP_49][.01] = PSS51P1[51.1][PSS[3]][.01]

    TMP_170 = {"I": PSS[3]}
    TMP_170[51.1] = TMP_169[51.1]
    TMP_170[51.1][TMP_49] = ""
    TMP_170[51.1][TMP_49][.01] = PSS51P1[51.1][PSS[3]][.01]

    TMP_171 = {"I": CNT}
    TMP_171[51.1] = TMP_170[51.1]
    TMP_171[51.1][TMP_49] = ""
    TMP_171[51.1][TMP_49][.01] = PSS51P1[51.1][PSS[3]][.01]

    TMP_172 = {"I": PSS[3]}
    TMP_172[51.1] = TMP_171[51