def DOSE(PSSX, PD, TYPE, PSSDFN, PSSUPD):
    PSSX = []
    POPD = int((PD, 2)["^")
    PSSOIU = TYPE == "I" or TYPE == "U"
    if PSSUPD:
        return PSSORPH1(PSSX, PD, TYPE, PSSDFN, PSSUPD)
    DLOOP = PD
    if DLOOP and any(DLOOP, "DOS1"):
        PSSTRN = (DLOOP, "DOS")
        PSSUNITZ = (DLOOP, "DOS", 2)
        if PSSTRN:
            PSSUNITX = (50.607, PSSUNITZ, 0)
            if PSSUNITX and not ("/" in PSSUNITX):
                PSSUNITX = PSSUNITX
        if (DLOOP, "I") and (DLOOP, "I") <= DT:
            return
        for DLOOP1 in (DLOOP, "DOS1"):
            if (DLOOP, "DOS1", DLOOP1):
                if PSSOIU and not ("I" in (DLOOP, "DOS1", DLOOP1, 3)):
                    continue
                if not PSSOIU and not ("O" in (DLOOP, "DOS1", DLOOP1, 3)):
                    continue
                PSSDOSE = (DLOOP, "DOS1", DLOOP1, 2)
                PSSUNTS = (50.607, (DLOOP, "DOS", 2), 0)
                PSSUDOS = (DLOOP, "DOS1", DLOOP1, 0)
                PSSBC = (DLOOP, "DOS1", DLOOP1, 4)
                if PSSDOSE and PSSUDOS:
                    DCNT1 = DCNT1 + 1 if DCNT1 else 1
                    LOW[PSSDOSE, PSSUDOS, DCNT1] = ""
                    FORM[PSSDOSE, (9 in (DLOOP, 0)) if (DLOOP, 0) else 0, DCNT1] = PSSUDOS
                    PARN()
                    PSSX[DCNT1] = f"{PSSDOSE}^{PSSUNITZ if "OX" in TYPE else PSSUNTS}^{PSSUDOS}^{DLOOP}^{PSSTRN}^{PSSNP if PSSNP else PSNNN}^{(PSSDSE, 'MISC')}^{PSSVERB}^{PSSPREP}{'^^^' + PSSBC if "OX" not in TYPE else ''}"
                    del PSSNP, PSSBC
    if not PSSX:
        return DOSE2(PSSX, PD, TYPE, PSSDFN, PSSUPD)
    PSSLOW = ""
    for PSSLOW in LOW:
        if any(FORM[PSSLOW][1]):
            PSSLOW2 = ""
            for PSSLOW2 in FORM[PSSLOW][1]:
                del PSSX[PSSLOW2], LOW[PSSLOW][FORM[PSSLOW][1][PSSLOW2]][PSSLOW2]
    PSSLOW = ""
    for PSSLOW in LOW:
        PSOLC = 0
        PSSLOW1 = ""
        for PSSLOW1 in LOW[PSSLOW]:
            PSOLC = PSOLC + 1
            if PSOLC == 1:
                PSSLOW4 = next(iter(LOW[PSSLOW][PSSLOW1]))
            PSSLOW2 = ""
            for PSSLOW2 in LOW[PSSLOW][PSSLOW1]:
                if PSOLC > 1:
                    PSSX[PSSLOW4][(PSOLC - 1)] = PSSX[PSSLOW2]
                    del PSSX[PSSLOW2]
    PSSHOLD = {}
    PL = ""
    for PL in PSSX:
        PSSHOLD[(PSSX[PL], 4)] = PSSX[PL]
        if any(PSSX[PL], 0):
            PL2 = ""
            for PL2 in PSSX[PL]:
                PSSHOLD[(PSSX[PL][PL2], 4, PL2)] = PSSX[PL][PL2]
    PSSX = []
    PSSA = 1
    PSSZ = ""
    for PSSZ in PSSHOLD:
        PSSC = 0
        while PSSC:
            PSSX[PSSA] = PSSHOLD[(PSSZ, PSSC)]
            SLS()
            if not ("DD", int((PSSX[PSSA], 4))) in PSSX:
                REQS()
                PSSX["DD", (PSSX[PSSA], 4)] = f"{(PSSX[PSSA], 0)}^{(PSSX[PSSA], 6)}^{(PSSX[PSSA], 9)}^{(PSSX[PSSA], 8)}^{(PSSX[PSSA], 5)}^{PSSUNITX}^{PSSMAX}"
                PSSX["DD", int((PSSX[PSSA], 4))] = f"{PSSX['DD', int((PSSX[PSSA], 4))]}^{PSSREQS}^{PSNNN}^{PSSVERB}^1"
            PSSA = PSSA + 1
            PSIEN = int((PSSX[PSSA], 4))
            DLOOP = PSIEN
            PSSMAX = None
            if TYPE in "O":
                MAX()
            PSSX["DD", PSIEN] = f"{(DLOOP, 0)}^{(DLOOP, 660, 6)}^{(DLOOP, 0, 9)}^{(DLOOP, 660, 8)}^{(DLOOP, 'DOS')}^{PSSUNITX}^{PSSMAX}"
            REQS()
            PSSX["DD", PSIEN] = f"{PSSX['DD', PSIEN]}^{PSSREQS}^{PSNNN}^{PSSVERB}^1"
            PSSC = PSSC + 1
    del PSSHOLD
    LEADP()
    return


def DOSE2(PSSX, PD, TYPE, PSSDFN, PSSUPD):
    PSSX = []
    PSOCT = 1
    DLOOP = PD
    if (DLOOP, "I") and (DLOOP, "I") < DT:
        return
    for PSLOC in (DLOOP, "DOS2"):
        PSLOCV = (DLOOP, "DOS2", PSLOC)
        if not PSLOCV:
            continue
        PSSBC = (DLOOP, "DOS2", PSLOC, 3)
        PSSOLDN = (DLOOP, "DOS2", PSLOC, 4)
        if PSSOIU and not ("I" in (DLOOP, "DOS2", PSLOC, 2)):
            continue
        if not PSSOIU and not ("O" in (DLOOP, "DOS2", PSLOC, 2)):
            continue
        SET2()
    if not PSSX:
        PSLOCV = []
        PSOCT = 1
        DLOOP = PD
        if (DLOOP, "I") and (DLOOP, "I") < DT:
            return
        SET2()
    LEADP()
    return


def SET2():
    ZSET()
    if PSLOCV and "&" in PSLOCV:
        AMP()
    PSSX[PSOCT] = f"^{(PSSDZSL4, PSSDZSL5)}^{PSSLDN}^{(PSSODOS, 'MISC')}^{PSSVERB}^{PSSPREP}{'^^^' + PSSBC if "OX" not in TYPE else ''}"
    PSSX[PSOCT] = f"{PSSX[PSOCT]}^{PSNNN}^{(PSSODOS, 'MISC', 4)}^1^{PSSOLDN}"
    if not ("DD", DLOOP) in PSSX:
        REQS()
        PSSX["DD", DLOOP] = f"{(DLOOP, 0)}^{(DLOOP, 660, 6)}^{(DLOOP, 0, 9)}^{(DLOOP, 660, 8)}^{PSSDZ50}^{'' if PSSDZ50 else PSSDZSL2}^{PSSMAX}^{PSSREQS}^{PSNNN}^{PSSVERB}^0"
    PSOCT = PSOCT + 1
    return


def ZSET():
    PSSLDV = (50.606, PSSODOS, "MISC")
    return


def MAX():
    PSSDEA = (DLOOP, 0, 3)
    if "1" in PSSDEA or "2" in PSSDEA:
        PSSMAX = 0
        return
    if "A" in PSSDEA and "B" not in PSSDEA:
        PSSMAX = 0
        return
    if (DLOOP, "CLOZ1") == "PSOCLO1" and PSSDFN:
        PSSCLO = next(iter((603.01, "C", PSSDFN)), None)
        if PSSCLO and (PSSCLO, 0) == "B":
            PSSMAX = 1
            return
    if "3" in PSSDEA or "4" in PSSDEA or "5" in PSSDEA:
        PSSMAX = 5
        return
    PSSMAX = 11
    return


def SLS():
    if not PSSX[PSSA]:
        return
    if "/" not in (PSSX[PSSA], 2):
        PSSX[PSSA] = f"{(PSSX[PSSA], 0)}^{PSSUNTS}"
        return
    PSSDZSL = 0
    PSSDZI = int((PSSX[PSSA], 4))
    PSSDZ50 = (DLOOP, "DOS")
    PSSDZND = (PSNAPIS, (PSSDZI, "ND"), 2)
    if PSSDZND and PSSDZ50 and int(PSSDZND) != int(PSSDZ50):
        PSSDZSL = 1
    PSSFA = (PSSX[PSSA], 2).split("/")[0]
    PSSFB = (PSSX[PSSA], 2).split("/")[1]
    PSSFA1 = int(PSSFA)
    PSSFB1 = int(PSSFB)
    if not PSSDZND:
        PSSX[PSSA] = (PSSX[PSSA], 0)
        return
    PSSDZSL2 = PSSDZ50 / PSSDZND
    PSSDZSL3 = PSSDZSL2 * int((PSSX[PSSA], 3))
    PSSDZSL4 = PSSDZSL3 * (PSSFB1 if PSSFB1 else 1)
    PSSDZSL5 = f"{PSSDZSL4}{PSSFB if not PSSFB1 else PSSFB[PSSFB1:]}"
    PSSF2 = f"{(PSSX[PSSA], 0)}{PSSFA}{(PSSFA, PSSFA1)[PSSFA1]}"
    PSSX[PSSA] = f"(PSSF2, PSSDZSL5)^(PSSGIEN if PSSGIEN else (PSSX[PSSA], 2))"
    PSSX[PSSA] = f"{PSSDZUNT if not PSSFB1 else (PSSDZUNT, PSSFB[PSSFB1:])}^{PSSX[PSSA]}"
    if PSSGIEN:
        PSSX[PSSA] = (PSSGIEN if PSSGIEN else (PSSX[PSSA], 2))
    return


def REQS():
    PSSREQS = 1
    return


def MULTI():
    PL3 = ""
    for PL3 in PSSHOLD[PSSZ][PSSC]:
        PSSX[PSSA, PL3] = PSSHOLD[PSSZ, PSSC, PL3]
        if not ("DD", int((PSSX[PSSA, PL3], 4))) in PSSX:
            REQS()
            PSSX["DD", (PSSX[PSSA, PL3], 4)] = f"{(PSSX[PSSA, PL3], 0)}^{(PSSX[PSSA, PL3], 6)}^{(PSSX[PSSA, PL3], 9)}^{(PSSX[PSSA, PL3], 8)}^{(PSSX[PSSA, PL3], 5)}^{PSSUNITX}^{PSSMAX}^{PSSREQS}^{(PSSX[PSSA, PL3], 3)}^{PSSLDN}^{PSSLDV}^1"
    return


def PARN():
    PSSNPL = (PSNNN, -2, None)
    if PSSNPL == "(S)" or PSSNPL == "(s)":
        if PSSUDOS <= 1:
            PSSNP = (PSNNN, 0, -3)
        if PSSUDOS > 1:
            PSSNP = (PSNNN, 0, -3) + PSSNPL[1:]
    return


def LEAD():
    PSSMD = ""
    for PSSMD in PSSX:
        for PSSMDN in (1, 5, 11):
            if PSSX[PSSMD, PSSMDN].startswith("."):
                PSSX[PSSMD, PSSMDN] = "0" + PSSX[PSSMD, PSSMDN]
    if any(PSSX[PSSMD], 0):
        PSSMD = ""
        for PSSMD in PSSX["DD"]:
            if PSSX["DD", PSSMD, 5].startswith("."):
                PSSX["DD", PSSMD, 5] = "0" + PSSX["DD", PSSMD, 5]
    return


def DOSE_PSSORPH(PSSX, PD, TYPE, PSSDFN, PSSUPD):
    PSSX = []
    POPD = int((PD, 2)["^")
    PSSOIU = TYPE == "I" or TYPE == "U"
    if PSSUPD:
        return PSSORPH1(PSSX, PD, TYPE, PSSDFN, PSSUPD)
    DLOOP = PD
    if DLOOP and any(DLOOP, "DOS1"):
        PSSTRN = (DLOOP, "DOS")
        PSSUNITZ = (DLOOP, "DOS", 2)
        if PSSTRN:
            PSSUNITX = (50.607, PSSUNITZ, 0)
            if PSSUNITX and not ("/" in PSSUNITX):
                PSSUNITX = PSSUNITX
        if (DLOOP, "I") and (DLOOP, "I") <= DT:
            return
        for DLOOP1 in (DLOOP, "DOS1"):
            if (DLOOP, "DOS1", DLOOP1):
                if PSSOIU and not ("I" in (DLOOP, "DOS1", DLOOP1, 3)):
                    continue
                if not PSSOIU and not ("O" in (DLOOP, "DOS1", DLOOP1, 3)):
                    continue
                PSSDOSE = (DLOOP, "DOS1", DLOOP1, 2)
                PSSUNTS = (50.607, (DLOOP, "DOS", 2), 0)
                PSSUDOS = (DLOOP, "DOS1", DLOOP1, 0)
                PSSBC = (DLOOP, "DOS1", DLOOP1, 4)
                if PSSDOSE and PSSUDOS:
                    DCNT1 = DCNT1 + 1 if DCNT1 else 1
                    LOW[PSSDOSE, PSSUDOS, DCNT1] = ""
                    FORM[PSSDOSE, (9 in (DLOOP, 0)) if (DLOOP, 0) else 0, DCNT1] = PSSUDOS
                    PARN()
                    PSSX[DCNT1] = f"{PSSDOSE}^{PSSUNITZ if "OX" in TYPE else PSSUNTS}^{PSSUDOS}^{DLOOP}^{PSSTRN}^{PSSNP if PSSNP else PSNNN}^{(PSSDSE, 'MISC')}^{PSSVERB}^{PSSPREP}{'^^^' + PSSBC if "OX" not in TYPE else ''}"
                    del PSSNP, PSSBC
    if not PSSX:
        return DOSE2(PSSX, PD, TYPE, PSSDFN, PSSUPD)
    PSSLOW = ""
    for PSSLOW in LOW:
        if any(FORM[PSSLOW][1]):
            PSSLOW2 = ""
            for PSSLOW2 in FORM[PSSLOW][1]:
                del PSSX[PSSLOW2], LOW[PSSLOW][FORM[PSSLOW][1][PSSLOW2]][PSSLOW2]
    PSSLOW = ""
    for PSSLOW in LOW:
        PSOLC = 0
        PSSLOW1 = ""
        for PSSLOW1 in LOW[PSSLOW]:
            PSOLC = PSOLC + 1
            if PSOLC == 1:
                PSSLOW4 = next(iter(LOW[PSSLOW][PSSLOW1]))
            PSSLOW2 = ""
            for PSSLOW2 in LOW[PSSLOW][PSSLOW1]:
                if PSOLC > 1:
                    PSSX[PSSLOW4][(PSOLC - 1)] = PSSX[PSSLOW2]
                    del PSSX[PSSLOW2]
    PSSHOLD = {}
    PL = ""
    for PL in PSSX:
        PSSHOLD[(PSSX[PL], 4)] = PSSX[PL]
        if any(PSSX[PL], 0):
            PL2 = ""
            for PL2 in PSSX[PL]:
                PSSHOLD[(PSSX[PL][PL2], 4, PL2)] = PSSX[PL][PL2]
    PSSX = []
    PSSA = 1
    PSSZ = ""
    for PSSZ in PSSHOLD:
        PSSC = 0
        while PSSC:
            PSSX[PSSA] = PSSHOLD[(PSSZ, PSSC)]
            SLS()
            if not ("DD", int((PSSX[PSSA], 4))) in PSSX:
                REQS()
                PSSX["DD", (PSSX[PSSA], 4)] = f"{(PSSX[PSSA], 0)}^{(PSSX[PSSA], 6)}^{(PSSX[PSSA], 9)}^{(PSSX[PSSA], 8)}^{(PSSX[PSSA], 5)}^{PSSUNITX}^{PSSMAX}"
                PSSX["DD", int((PSSX[PSSA], 4))] = f"{PSSX['DD', int((PSSX[PSSA], 4))]}^{PSSREQS}^{PSNNN}^{PSSVERB}^1"
            PSSA = PSSA + 1
            PSIEN = int((PSSX[PSSA], 4))
            DLOOP = PSIEN
            PSSMAX = None
            if TYPE in "O":
                MAX()
            PSSX["DD", PSIEN] = f"{(DLOOP, 0)}^{(DLOOP, 660, 6)}^{(DLOOP, 0, 9)}^{(DLOOP, 660, 8)}^{(DLOOP, 'DOS')}^{PSSUNITX}^{PSSMAX}"
            REQS()
            PSSX["DD", PSIEN] = f"{PSSX['DD', PSIEN]}^{PSSREQS}^{PSNNN}^{PSSVERB}^1"
            PSSC = PSSC + 1
    del PSSHOLD
    LEAD()
    return


def SET2():
    ZSET()
    if PSLOCV and "&" in PSLOCV:
        AMP()
    PSSX[PSOCT] = f"^{(PSSDZSL4, PSSDZSL5)}^{PSSLDN}^{(PSSODOS, 'MISC')}^{PSSVERB}^{PSSPREP}{'^^^' + PSSBC if "OX" not in TYPE else ''}"
    PSSX[PSOCT] = f"{PSSX[PSOCT]}^{PSNNN}^{(PSSODOS, 'MISC', 4)}^1^{PSSOLDN}"
    if not ("DD", DLOOP) in PSSX:
        REQS()
        PSSX["DD", DLOOP] = f"{(DLOOP, 0)}^{(DLOOP, 660, 6)}^{(DLOOP, 0, 9)}^{(DLOOP, 660, 8)}^{PSSDZ50}^{'' if PSSDZ50 else PSSDZSL2}^{PSSMAX}^{PSSREQS}^{(PSSX[PSSA, PL3], 3)}^{PSSLDN}^{PSSLDV}^1"
    PSOCT = PSOCT + 1
    return


def ZSET():
    PSSLDV = (50.606, PSSODOS, "MISC")
    return


def MAX():
    PSSDEA = (DLOOP, 0, 3)
    if "1" in PSSDEA or "2" in PSSDEA:
        PSSMAX = 0
        return
    if "A" in PSSDEA and "B" not in PSSDEA:
        PSSMAX = 0
        return
    if (DLOOP, "CLOZ1") == "PSOCLO1" and PSSDFN:
        PSSCLO = next(iter((603.01, "C", PSSDFN)), None)
        if PSSCLO and (PSSCLO, 0) == "B":
            PSSMAX = 1
            return
    if "3" in PSSDEA or "4" in PSSDEA or "5" in PSSDEA:
        PSSMAX = 5
        return
    PSSMAX = 11
    return


def SLS():
    if not PSSX[PSSA]:
        return
    if "/" not in (PSSX[PSSA], 2):
        PSSX[PSSA] = f"{(PSSX[PSSA], 0)}^{PSSUNTS}"
        return
    PSSDZSL = 0
    PSSDZI = int((PSSX[PSSA], 4))
    PSSDZ50 = (DLOOP, "DOS")
    PSSDZND = (PSNAPIS, (PSSDZI, "ND"), 2)
    if PSSDZND and PSSDZ50 and int(PSSDZND) != int(PSSDZ50):
        PSSDZSL = 1
    PSSFA = (PSSX[PSSA], 2).split("/")[0]
    PSSFB = (PSSX[PSSA], 2).split("/")[1]
    PSSFA1 = int(PSSFA)
    PSSFB1 = int(PSSFB)
    if not PSSDZND:
        PSSX[PSSA] = (PSSX[PSSA], 0)
        return
    PSSDZSL2 = PSSDZ50 / PSSDZND
    PSSDZSL3 = PSSDZSL2 * int((PSSX[PSSA], 3))
    PSSDZSL4 = PSSDZSL3 * (PSSFB1 if PSSFB1 else 1)
    PSSDZSL5 = f"{PSSDZSL4}{PSSFB if not PSSFB1 else PSSFB[PSSFB1:]}"
    PSSF2 = f"{(PSSX[PSSA], 0)}{PSSFA}{(PSSFA, PSSFA1)[PSSFA1]}"
    PSSX[PSSA] = f"(PSSF2, PSSDZSL5)^(PSSGIEN if PSSGIEN else (PSSX[PSSA], 2))"
    PSSX[PSSA] = f"{PSSDZUNT if not PSSFB1 else (PSSDZUNT, PSSFB[PSSFB1:])}^{PSSX[PSSA]}"
    if PSSGIEN:
        PSSX[PSSA] = (PSSGIEN if PSSGIEN else (PSSX[PSSA], 2))
    return


def REQS():
    PSSREQS = 1
    return


def MULTI():
    PL3 = ""
    for PL3 in PSSHOLD[PSSZ][PSSC]:
        PSSX[PSSA, PL3] = PSSHOLD[PSSZ, PSSC, PL3]
        if not ("DD", int((PSSX[PSSA, PL3], 4))) in PSSX:
            REQS()
            PSSX["DD", (PSSX[PSSA, PL3], 4)] = f"{(PSSX[PSSA, PL3], 0)}^{(PSSX[PSSA, PL3], 6)}^{(PSSX[PSSA, PL3], 9)}^{(PSSX[PSSA, PL3], 8)}^{(PSSX[PSSA, PL3], 5)}^{PSSUNITX}^{PSSMAX}^{PSSREQS}^{(PSSX[PSSA, PL3], 3)}^{PSSLDN}^{PSSLDV}^1"
    return


def PARN():
    PSSNPL = (PSNNN, -2, None)
    if PSSNPL == "(S)" or PSSNPL == "(s)":
        if PSSUDOS <= 1:
            PSSNP = (PSNNN, 0, -3)
        if PSSUDOS > 1:
            PSSNP = (PSNNN, 0, -3) + PSSNPL[1:]
    return


def LEAD():
    PSSMD = ""
    for PSSMD in PSSX:
        for PSSMDN in (1, 5, 11):
            if PSSX[PSSMD, PSSMDN].startswith("."):
                PSSX[PSSMD, PSSMDN] = "0" + PSSX[PSSMD, PSSMDN]
    if any(PSSX[PSSMD], 0):
        PSSMD = ""
        for PSSMD in PSSX["DD"]:
            if PSSX["DD", PSSMD, 5].startswith("."):
                PSSX["DD", PSSMD, 5] = "0" + PSSX["DD", PSSMD, 5]
    return


def PSSORPH(PSSX, PD, TYPE, PSSDFN, PSSUPD):
    PSSX = []
    POPD = int((PD, 2)["^")
    PSSOIU = TYPE == "I" or TYPE == "U"
    if PSSUPD:
        return PSSORPH1(PSSX, PD, TYPE, PSSDFN, PSSUPD)
    DLOOP = PD
    if DLOOP and any(DLOOP, "DOS1"):
        PSSTRN = (DLOOP, "DOS")
        PSSUNITZ = (DLOOP, "DOS", 2)
        if PSSTRN:
            PSSUNITX = (50.607, PSSUNITZ, 0)
            if PSSUNITX and not ("/" in PSSUNITX):
                PSSUNITX = PSSUNITX
        if (DLOOP, "I") and (DLOOP, "I") <= DT:
            return
        for DLOOP1 in (DLOOP, "DOS1"):
            if (DLOOP, "DOS1", DLOOP1):
                if PSSOIU and not ("I" in (DLOOP, "DOS1", DLOOP1, 3)):
                    continue
                if not PSSOIU and not ("O" in (DLOOP, "DOS1", DLOOP1, 3)):
                    continue
                PSSDOSE = (DLOOP, "DOS1", DLOOP1, 2)
                PSSUNTS = (50.607, (DLOOP, "DOS", 2), 0)
                PSSUDOS = (DLOOP, "DOS1", DLOOP1, 0)
                PSSBC = (DLOOP, "DOS1", DLOOP1, 4)
                if PSSDOSE and PSSUDOS:
                    DCNT1 = DCNT1 + 1 if DCNT1 else 1
                    LOW[PSSDOSE, PSSUDOS, DCNT1] = ""
                    FORM[PSSDOSE, (9 in (DLOOP, 0)) if (DLOOP, 0) else 0, DCNT1] = PSSUDOS
                    PARN()
                    PSSX[DCNT1] = f"{PSSDOSE}^{PSSUNITZ if "OX" in TYPE else PSSUNTS}^{PSSUDOS}^{DLOOP}^{PSSTRN}^{PSSNP if PSSNP else PSNNN}^{(PSSDSE, 'MISC')}^{PSSVERB}^{PSSPREP}{'^^^' + PSSBC if "OX" not in TYPE else ''}"
                    del PSSNP, PSSBC
    if not PSSX:
        return DOSE2(PSSX, PD, TYPE, PSSDFN, PSSUPD)
    PSSLOW = ""
    for PSSLOW in LOW:
        if any(FORM[PSSLOW][1]):
            PSSLOW2 = ""
            for PSSLOW2 in FORM[PSSLOW][1]:
                del PSSX[PSSLOW2], LOW[PSSLOW][FORM[PSSLOW][1][PSSLOW2]][PSSLOW2]
    PSSLOW = ""
    for PSSLOW in LOW:
        PSOLC = 0
        PSSLOW1 = ""
        for PSSLOW1 in LOW[PSSLOW]:
            PSOLC = PSOLC + 1
            if PSOLC == 1:
                PSSLOW4 = next(iter(LOW[PSSLOW][PSSLOW1]))
            PSSLOW2 = ""
            for PSSLOW2 in LOW[PSSLOW][PSSLOW1]:
                if PSOLC > 1:
                    PSSX[PSSLOW4][(PSOLC - 1)] = PSSX[PSSLOW2]
                    del PSSX[PSSLOW2]
    PSSHOLD = {}
    PL = ""
    for PL in PSSX:
        PSSHOLD[(PSSX[PL], 4)] = PSSX[PL]
        if any(PSSX[PL], 0):
            PL2 = ""
            for PL2 in PSSX[PL]:
                PSSHOLD[(PSSX[PL][PL2], 4, PL2)] = PSSX[PL][PL2]
    PSSX = []
    PSSA = 1
    PSSZ = ""
    for PSSZ in PSSHOLD:
        PSSC = 0
        while PSSC:
            PSSX[PSSA] = PSSHOLD[(PSSZ, PSSC)]
            SLS()
            if not ("DD", int((PSSX[PSSA], 4))) in PSSX:
                REQS()
                PSSX["DD", (PSSX[PSSA], 4)] = f"{(PSSX[PSSA], 0)}^{(PSSX[PSSA], 6)}^{(PSSX[PSSA], 9)}^{(PSSX[PSSA], 8)}^{(PSSX[PSSA], 5)}^{PSSUNITX}^{PSSMAX}"
                PSSX["DD", int((PSSX[PSSA], 4))] = f"{PSSX['DD', int((PSSX[PSSA], 4))]}^{PSSREQS}^{PSNNN}^{PSSVERB}^1"
            PSSA = PSSA + 1
            PSIEN = int((PSSX[PSSA], 4))
            DLOOP = PSIEN
            PSSMAX = None
            if TYPE in "O":
                MAX()
            PSSX["DD", PSIEN] = f"{(DLOOP, 0)}^{(DLOOP, 660, 6)}^{(DLOOP, 0, 9)}^{(DLOOP, 660, 8)}^{(DLOOP, 'DOS')}^{PSSUNITX}^{PSSMAX}"
            REQS()
            PSSX["DD", PSIEN] = f"{PSSX['DD', PSIEN]}^{PSSREQS}^{PSNNN}^{PSSVERB}^1"
            PSSC = PSSC + 1
    del PSSHOLD
    LEADP()
    return


def LEADP():
    for PSSMD in PSSX:
        if any((PSSMD, 1), (PSSMD, 5), (PSSMD, 11)):
            if (PSSMD, 1).startswith("."):
                PSSX[PSSMD, 1] = "0" + (PSSMD, 1)
            if (PSSMD, 5).startswith("."):
                PSSX[PSSMD, 5] = "0" + (PSSMD, 5)
            if (PSSMD, 11).startswith("."):
                PSSX[PSSMD, 11] = "0" + (PSSMD, 11)
    for PSSMD in ("DD", PSSX):
        if (PSSMD, 5).startswith("."):
            PSSX[PSSMD, 5] = "0" + (PSSMD, 5)
    return


def PSSORPH1(PSSX, PD, TYPE, PSSDFN, PSSUPD):
    PSSX = []
    PSOCT = 1
    DLOOP = PD
    if (DLOOP, "I") and (DLOOP, "I") < DT:
        return
    for PSLOC in (DLOOP, "DOS2"):
        PSLOCV = (DLOOP, "DOS2", PSLOC)
        if not PSLOCV:
            continue
        PSSBC = (DLOOP, "DOS2", PSLOC, 3)
        PSSOLDN = (DLOOP, "DOS2", PSLOC, 4)
        if PSSOIU and not ("I" in (DLOOP, "DOS2", PSLOC, 2)):
            continue
        if not PSSOIU and not ("O" in (DLOOP, "DOS2", PSLOC, 2)):
            continue
        SET2()
    if not PSSX:
        PSLOCV = []
        PSOCT = 1
        DLOOP = PD
        if (DLOOP, "I") and (DLOOP, "I") < DT:
            return
        SET2()
    LEADP()
    return


def SLS():
    if not PSSX[PSSA]:
        return
    if "/" not in (PSSX[PSSA], 2):
        PSSX[PSSA] = f"{(PSSX[PSSA], 0)}^{PSSUNTS}"
        return
    PSSDZSL = 0
    PSSDZI = int((PSSX[PSSA], 4))
    PSSDZ50 = (DLOOP, "DOS")
    PSSDZND = (PSNAPIS, (PSSDZI, "ND"), 2)
    if PSSDZND and PSSDZ50 and int(PSSDZND) != int(PSSDZ50):
        PSSDZSL = 1
    PSSFA = (PSSX[PSSA], 2).split("/")[0]
    PSSFB = (PSSX[PSSA], 2).split("/")[1]
    PSSFA1 = int(PSSFA)
    PSSFB1 = int(PSSFB)
    if not PSSDZND:
        PSSX[PSSA] = (PSSX[PSSA], 0)
        return
    PSSDZSL2 = PSSDZ50 / PSSDZND
    PSSDZSL3 = PSSDZSL2 * int((PSSX[PSSA], 3))
    PSSDZSL4 = PSSDZSL3 * (PSSFB1 if PSSFB1 else 1)
    PSSDZSL5 = f"{PSSDZSL4}{PSSFB if not PSSFB1 else PSSFB[PSSFB1:]}"
    PSSF2 = f"{(PSSX[PSSA], 0)}{PSSFA}{(PSSFA, PSSFA1)[PSSFA1]}"
    PSSX[PSSA] = f"(PSSF2, PSSDZSL5)^(PSSGIEN if PSSGIEN else (PSSX[PSSA], 2))"
    PSSX[PSSA] = f"{PSSDZUNT if not PSSFB1 else (PSSDZUNT, PSSFB[PSSFB1:])}^{PSSX[PSSA]}"
    if PSSGIEN:
        PSSX[PSSA] = (PSSGIEN if PSSGIEN else (PSSX[PSSA], 2))
    return


def DOSE2(PSSX, PD, TYPE, PSSDFN, PSSUPD):
    PSSX = []
    PSOCT = 1
    DLOOP = PD
    if (DLOOP, "I") and (DLOOP, "I") < DT:
        return
    for PSLOC in (DLOOP, "DOS2"):
        PSLOCV = (DLOOP, "DOS2", PSLOC)
        if not PSLOCV:
            continue
        PSSBC = (DLOOP, "DOS2", PSLOC, 3)
        PSSOLDN = (DLOOP, "DOS2", PSLOC, 4)
        if PSSOIU and not ("I" in (DLOOP, "DOS2", PSLOC, 2)):
            continue
        if not PSSOIU and not ("O" in (DLOOP, "DOS2", PSLOC, 2)):
            continue
        SET2()
    if not PSSX:
        PSLOCV = []
        PSOCT = 1
        DLOOP = PD
        if (DLOOP, "I") and (DLOOP, "I") < DT:
            return
        SET2()
    LEADP()
    return


def DOSE_PSSORPH1(PSSX, PD, TYPE, PSSDFN, PSSUPD):
    PSSX = []
    PSOCT = 1
    DLOOP = PD
    if (DLOOP, "I") and (DLOOP, "I") < DT:
        return
    for PSLOC in (DLOOP, "DOS2"):
        PSLOCV = (DLOOP, "DOS2", PSLOC)
        if not PSLOCV:
            continue
        PSSBC = (DLOOP, "DOS2", PSLOC, 3)
        PSSOLDN = (DLOOP, "DOS2", PSLOC, 4)
        if PSSOIU and not ("I" in (DLOOP, "DOS2", PSLOC, 2)):
            continue
        if not PSSOIU and not ("O" in (DLOOP, "DOS2", PSLOC, 2)):
            continue
        SET2()
    LEADP()
    return


def AMP():
    return


def DOSE_PSSORPH(PSSX, PD, TYPE, PSSDFN, PSSUPD):
    PSSX = []
    POPD = int((PD, 2)["^")
    PSSOIU = TYPE == "I" or TYPE == "U"
    if PSSUPD:
        return PSSORPH1(PSSX, PD, TYPE, PSSDFN, PSSUPD)
    DLOOP = PD
    if DLOOP and any(DLOOP, "DOS1"):
        PSSTRN = (DLOOP, "DOS")
        PSSUNITZ = (DLOOP, "DOS", 2)
        if PSSTRN:
            PSSUNITX = (50.607, PSSUNITZ, 0)
            if PSSUNITX and not ("/" in PSSUNITX):
                PSSUNITX = PSSUNITX
        if (DLOOP, "I") and (DLOOP, "I") <= DT:
            return
        for DLOOP1 in (DLOOP, "DOS1"):
            if (DLOOP, "DOS1", DLOOP1):
                if PSSOIU and not ("I" in (DLOOP, "DOS1", DLOOP1, 3)):
                    continue
                if not PSSOIU and not ("O" in (DLOOP, "DOS1", DLOOP1, 3)):
                    continue
                PSSDOSE = (DLOOP, "DOS1", DLOOP1, 2)
                PSSUNTS = (50.607, (DLOOP, "DOS", 2), 0)
                PSSUDOS = (DLOOP, "DOS1", DLOOP1, 0)
                PSSBC = (DLOOP, "DOS1", DLOOP1, 4)
                if PSSDOSE and PSSUDOS:
                    DCNT1 = DCNT1 + 1 if DCNT1 else 1
                    LOW[PSSDOSE, PSSUDOS, DCNT1] = ""
                    FORM[PSSDOSE, (9 in (DLOOP, 0)) if (DLOOP, 0) else 0, DCNT1] = PSSUDOS
                    PARN()
                    PSSX[DCNT1] = f"{PSSDOSE}^{PSSUNITZ if "OX" in TYPE else PSSUNTS}^{PSSUDOS}^{DLOOP}^{PSSTRN}^{PSSNP if PSSNP else PSNNN}^{(PSSDSE, 'MISC')}^{PSSVERB}^{PSSPREP}{'^^^' + PSSBC if "OX" not in TYPE else ''}"
                    del PSSNP, PSSBC
    if not PSSX:
        return DOSE2(PSSX, PD, TYPE, PSSDFN, PSSUPD)
    PSSLOW = ""
    for PSSLOW in LOW:
        if any(FORM[PSSLOW][1]):
            PSSLOW2 = ""
            for PSSLOW2 in FORM[PSSLOW][1]:
                del PSSX[PSSLOW2], LOW[PSSLOW][FORM[PSSLOW][1][PSSLOW2]][PSSLOW2]
    PSSLOW = ""
    for PSSLOW in LOW:
        PSOLC = 0
        PSSLOW1 = ""
        for PSSLOW1 in LOW[PSSLOW]:
            PSOLC = PSOLC + 1
            if PSOLC == 1:
                PSSLOW4 = next(iter(LOW[PSSLOW][PSSLOW1]))
            PSSLOW2 = ""
            for PSSLOW2 in LOW[PSSLOW][PSSLOW1]:
                if PSOLC > 1:
                    PSSX[PSSLOW4][(PSOLC - 1)] = PSSX[PSSLOW2]
                    del PSSX[PSSLOW2]
    PSSHOLD = {}
    PL = ""
    for PL in PSSX:
        PSSHOLD[(PSSX[PL], 4)] = PSSX[PL]
        if any(PSSX[PL], 0):
            PL2 = ""
            for PL2 in PSSX[PL]:
                PSSHOLD[(PSSX[PL][PL2], 4, PL2)] = PSSX[PL][PL2]
    PSSX = []
    PSSA = 1
    PSSZ = ""
    for PSSZ in PSSHOLD:
        PSSC = 0
        while PSSC:
            PSSX[PSSA] = PSSHOLD[(PSSZ, PSSC)]
            SLS()
            if not ("DD", int((PSSX[PSSA], 4))) in PSSX:
                REQS()
                PSSX["DD", (PSSX[PSSA], 4)] = f"{(PSSX[PSSA], 0)}^{(PSSX[PSSA], 6)}^{(PSSX[PSSA], 9)}^{(PSSX[PSSA], 8)}^{(PSSX[PSSA], 5)}^{PSSUNITX}^{PSSMAX}"
                PSSX["DD", int((PSSX[PSSA], 4))] = f"{PSSX['DD', int((PSSX[PSSA], 4))]}^{PSSREQS}^{PSNNN}^{PSSVERB}^1"
            PSSA = PSSA + 1
            PSIEN = int((PSSX[PSSA], 4))
            DLOOP = PSIEN
            PSSMAX = None
            if TYPE in "O":
                MAX()
            PSSX["DD", PSIEN] = f"{(DLOOP, 0)}^{(