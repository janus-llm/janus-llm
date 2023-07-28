def SKB(PSSIEN2, PSSFL2):
    if not PSSIEN2:
        return 0
    if PSSFL2 not in ['S', 'K']:
        return 0
    if PSSFL2 == 'S' and psdrugs:
        psdrug = psdrugs[int(PSSIEN2)]
        psdrug_name = psdrug[0]
        psdrug_ien = psdrug[1]
        psdrug_b = psdrug_name[:40]
        psdrugs_b[psdrug_b] = psdrug_ien
        return 1
    if PSSFL2 == 'K' and psdrugs:
        psdrug = psdrugs[int(PSSIEN2)]
        psdrug_name = psdrug[0]
        psdrug_ien = psdrug[1]
        psdrug_b = psdrug_name[:40]
        psdrugs_b.pop(psdrug_b, None)
        return 1
    return 0

def AOC(PSSVAL, PSSFL, PSSPK, LIST):
    PSSVAL = str(PSSVAL)
    PSSFL = int(PSSFL) if PSSFL else 0
    PSSPK = str(PSSPK)

    if not LIST:
        return
    tmp_list = []
    if not PSSVAL:
        tmp_list.append(-1)
        tmp_list.append("NO DATA FOUND")
        return tmp_list

    tmp_list.append(0)
    for psdrug in psdrugs:
        psdrug_ien = psdrug[1]
        psdrug_aoc = psdrug[2]
        psdrug_va_classification = psdrug[3]
        psdrug_inactive_date = psdrug[4]
        psdrug_application_package = psdrug[5]
        if PSSFL > 0 and psdrug_inactive_date > 0 and psdrug_inactive_date <= PSSFL:
            continue
        if PSSPK and psdrug_application_package and PSSPK not in psdrug_application_package:
            continue
        tmp_list[0] += 1
        tmp_list[psdrug_ien] = {}
        tmp_list[psdrug_ien][0.01] = psdrug_va_classification
        if psdrug_aoc not in tmp_list:
            tmp_list[psdrug_aoc] = {}
        tmp_list[psdrug_aoc][psdrug_ien] = ''
    if tmp_list[0] <= 0:
        tmp_list[0] = -1
        tmp_list.append("NO DATA FOUND")
    return tmp_list

def C(PSSVAL, PSSFL, PSSPK, LIST):
    PSSVAL = str(PSSVAL)
    PSSFL = int(PSSFL) if PSSFL else 0
    PSSPK = str(PSSPK)

    if not LIST:
        return
    tmp_list = []
    if not PSSVAL:
        tmp_list.append(-1)
        tmp_list.append("NO DATA FOUND")
        return tmp_list

    tmp_list.append(0)
    for psdrug in psdrugs:
        psdrug_ien = psdrug[1]
        psdrug_c = psdrug[6]
        psdrug_synonym = psdrug[7]
        psdrug_inactive_date = psdrug[4]
        psdrug_application_package = psdrug[5]
        if PSSFL > 0 and psdrug_inactive_date > 0 and psdrug_inactive_date <= PSSFL:
            continue
        if PSSPK and psdrug_application_package and PSSPK not in psdrug_application_package:
            continue
        tmp_list[0] += 1
        tmp_list[psdrug_ien] = {}
        tmp_list[psdrug_ien][0.01] = psdrug_synonym
        if psdrug_c not in tmp_list:
            tmp_list[psdrug_c] = {}
        tmp_list[psdrug_c][psdrug_ien] = ''
        PSSP50 = {}
        PSSP50[50.1] = {}
        PSSP50[50.1][0.01] = psdrug_synonym
        PSSP50[50.1][2] = psdrug.Application_Package
        PSSP50[50.1][1] = psdrug[8]
        PSSP50[50.1][400] = psdrug[9]
        PSSP50[50.1][401] = psdrug[10]
        PSSP50[50.1][402] = psdrug[11]
        PSSP50[50.1][403] = psdrug[12]
        PSSP50[50.1][404] = psdrug[13]
        PSSP50[50.1][405] = psdrug[14]
        tmp_list[psdrug_ien][50.1] = PSSP50[50.1]
    if tmp_list[0] <= 0:
        tmp_list[0] = -1
        tmp_list.append("NO DATA FOUND")
    return tmp_list

def SKAQ(PSSIEN2, PSSFL2):
    PSSIEN2 = int(PSSIEN2)
    if not PSSIEN2:
        return 0
    if PSSFL2 not in ['S', 'K']:
        return 0
    if PSSFL2 == 'S' and psdrugs:
        psdrug = psdrugs[int(PSSIEN2)]
        psdrug_ien = psdrug[1]
        psdrug_3 = psdrug[15]
        if psdrug_3 == 1:
            psdrugs_aq[psdrug_ien] = ''
        return 1
    if PSSFL2 == 'K' and psdrugs:
        psdrug = psdrugs[int(PSSIEN2)]
        psdrug_ien = psdrug[1]
        psdrug_3 = psdrug[15]
        if psdrug_3 == 0:
            psdrugs_aq.pop(psdrug_ien, None)
        return 1
    return 0

def SKAQ1(PSSIEN2):
    PSSIEN2 = int(PSSIEN2)
    if not PSSIEN2:
        return 0
    qflg = False
    for psdrug_aq1 in psdrugs_aq1:
        if psdrug_aq1:
            psdrugs_aq1.remove(psdrug_aq1)
            qflg = True
    psdrug_nd = psdrug_nds[PSSIEN2]
    if psdrug_nd[9]:
        psdrug_aq1 = psdrug_nd[9][:30]
        psdrugs_aq1.append(psdrug_aq1)
        qflg = True
    if qflg:
        return 1
    return 0

def A526(PSSIEN):
    PSSIEN = int(PSSIEN)
    if not PSSIEN:
        return 0
    tmp_list = []
    for psdrug_a526 in psdrugs_a526:
        if psdrug_a526:
            psdrugs_a526.remove(psdrug_a526)
            tmp_list.append(psdrug_a526)
            tmp_list[psdrug_a526] = {}
            tmp_list[psdrug_a526][0.01] = psdrug_a526[0]
            psdrugs_a526[psdrug_a526[0]] = psdrug_a526[1]
    if not tmp_list:
        tmp_list.append(-1)
        tmp_list.append("NO DATA FOUND")
    return tmp_list

def A527(PSSIEN):
    PSSIEN = int(PSSIEN)
    if not PSSIEN:
        return 0
    tmp_list = []
    for psdrug_a527 in psdrugs_a527:
        if psdrug_a527:
            psdrugs_a527.remove(psdrug_a527)
            tmp_list.append(psdrug_a527)
            tmp_list[psdrug_a527] = {}
            tmp_list[psdrug_a527][0.01] = psdrug_a527[0]
            psdrugs_a527[psdrug_a527[0]] = psdrug_a527[1]
    if not tmp_list:
        tmp_list.append(-1)
        tmp_list.append("NO DATA FOUND")
    return tmp_list

def SKAIU(PSSIEN2, PSSFL2):
    PSSIEN2 = int(PSSIEN2)
    if not PSSIEN2:
        return 0
    if PSSFL2 not in ['S', 'K']:
        return 0
    psdrug = psdrugs[PSSIEN2]
    psdrug_ien = psdrug[1]
    psdrug_2 = psdrug[16]
    if PSSFL2 == 'S' and psdrug_2:
        psdrug_aiu[psdrug_ien] = ''
        return 1
    if PSSFL2 == 'K' and not psdrug_2:
        psdrug_aiu.pop(psdrug_ien, None)
        return 1
    return 0

def SKIU(PSSIEN2):
    PSSIEN2 = int(PSSIEN2)
    if not PSSIEN2:
        return 0
    qflg = False
    for psdrug_iu in psdrugs_iu:
        if psdrug_iu:
            psdrugs_iu.remove(psdrug_iu)
            qflg = True
    psdrug_2 = psdrug_2s[PSSIEN2]
    if psdrug_2:
        psdrugs_iu.append(psdrug_2)
        qflg = True
    if qflg:
        return 1
    return 0

def FNAME(PSSFNO2, PSSFILE2):
    PSSFNO2 = int(PSSFNO2)
    PSSFILE2 = int(PSSFILE2)
    if not PSSFNO2 or not PSSFILE2:
        return ''
    if 50 <= PSSFILE2 <= 59:
        return psfile_names[PSSFILE2]
    for fname in psfile_names:
        if fname == PSSFILE2:
            return psfile_names[fname]
    return ''

psdrugs = {
    1: ['Drug1', 123, 'AOC1', 'VA Classification1', 0, 'Application Package1', 1],
    2: ['Drug2', 456, 'AOC2', 'VA Classification2', 0, 'Application Package2', 1],
    3: ['Drug3', 789, 'AOC3', 'VA Classification3', 0, 'Application Package3', 1]
}

psdrugs_b = {}

psdrugs_aq = {}

psdrugs_aq1 = []

psdrugs_a526 = []

psdrugs_a527 = []

psdrugs_aiu = {}

psdrugs_iu = []

psdrug_nds = {
    1: {
        9: 'A',
        10: 'B',
        11: 'C'
    },
    2: {
        9: 'D',
        10: 'E',
        11: 'F'
    },
    3: {
        9: 'G',
        10: 'H',
        11: 'I'
    }
}

psdrug_2s = {
    1: 'J',
    2: 'K',
    3: 'L'
}

psfile_names = {
    50: 'File50',
    50.04: 'File50.04',
    50.07: 'File50.07',
    550: 'File550',
    550.04: 'File550.04'
}