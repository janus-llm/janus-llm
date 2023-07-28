def PSSUTIL3():
    PSSPKG = $P($$POSDOS^PSNAPIS(PSSND), "^", 3)
    D
    if PSSTOT > 1:
        PSSTOTX = PSSTOT - 1
        ^PSDRUG(PSSDIEN, "DOS") = PSSST + "^" + PSSUN
        PSSONLYO = 1
        PSSBOTH = 0
        ^PSDRUG(PSSDIEN, "DOS1", 0) = "^50.0903^" + $G(PSSTOTX) + "^" + $G(PSSTOTX)
        if not (PSSI & PSSO):
            LOC^PSSUTIL()

    PSSTOT = 1
    for PSSDUPD in [1, 2]:
        if PSSUPRA == "NO" and PSSDUPD == 2:
            continue
        PSSTODOS = PSSDUPD * PSSST
        ^PSDRUG(PSSDIEN, "DOS1", PSSTOT, 0) = PSSDUPD + "^" + PSSTODOS + "^" + PSSPKG
        ^PSDRUG(PSSDIEN, "DOS1", "B", PSSDUPD, PSSTOT) = ""
        PSSTOT = PSSTOT + 1


def TEST():
    K PSSNL, PSSNLF, PSSNLX
    if $G(PSNOUNPT) == "":
        return
    if $L(PSNOUNPT) <= 3:
        return
    PSSNL = $E(PSNOUNPT, ($L(PSNOUNPT) - 2), $L(PSNOUNPT))
    if $G(PSSNL) == "(S)" or $G(PSSNL) == "(s)":
        PSSNLF = 1
        if $G(PSDUPDPT) <= 1:
            PSSNLX = $E(PSNOUNPT, 1, ($L(PSNOUNPT) - 3))
        if $G(PSDUPDPT) > 1:
            PSSNLX = $E(PSNOUNPT, 1, ($L(PSNOUNPT) - 3)) + $E(PSSNL, 2)


def SUPRA(PSSND):
    PSSDOS, PSSCD, PSSDOSC, PSSPKG = $$POSDOS^PSNAPIS(PSSND).split("^")
    return "NO" if PSSCD == "N" and PSSDOSC == "O" else "NB" if PSSCD == "N" and PSSDOSC == "B" else "NN" if PSSCD == "N" and PSSDOSC == "N" else ""


def CHECK(PSSIEN):
    PSSNAT, PSSNAT1 = int($G(^PSDRUG(PSSIEN, "ND"))[2]), $P($G(^("ND")), "^")
    PSSNATND = $$DFSU^PSNAPIS(PSSNAT1, PSSNAT)
    PSSNATDF, PSSNATST, PSSNATUN = $P(PSSNATND, "^"), $P(PSSNATND, "^", 4), $P(PSSNATND, "^", 5)
    if not PSSNATDF or not PSSNATUN or not $G(PSSNATST):
        return 0
    if not $D(^PS(50.606, PSSNATDF)[0]) or not $D(^PS(50.607, PSSNATUN)[0]):
        return 0
    if not PSSNATST.isdigit() or not PSSNATST.replace(".", "").isdigit():
        return 0
    if $D(^PS(50.606, "ACONI", PSSNATDF, PSSNATUN)) and $O(^PS(50.606, "ADUPI", PSSNATDF, 0)):
        return 1
    if $D(^PS(50.606, "ACONO", PSSNATDF, PSSNATUN)) and $O(^PS(50.606, "ADUPO", PSSNATDF, 0)):
        return 1
    return 0


def NATND():
    PSSNAT = int($G(^PSDRUG(PSSIEN, "ND"))[3])
    PSSNAT1 = $P($G(^("ND")), "^")
    PSSNATND = $$DFSU^PSNAPIS(PSSNAT1, PSSNAT)
    PSSNATDF = $P(PSSNATND, "^")
    PSSNATST = $P(PSSNATND, "^", 4)
    PSSNATUN = $P(PSSNATND, "^", 5)


PSSUTIL3()