def dosn():
    global PSSST, PSSUN, PSSNAME, PSSIND, PSSDOSA, PSSXYZ, PSSNATST, POSDOS, LPDOS, PSSDIEN, PSSONLYI, PSSONLYO, PSSTALK, PSSIZZ, PSSOZZ, PSSSKIPP, PSSWDXF, PSSUPRA, PSSIEN
    PSSIEN = DA

def dosnx():
    stun()
    if PSSST == "" and $O(^PSDRUG(PSSIEN, "DOS1", 0)):
        K ^PSDRUG(PSSIEN, "DOS")
        K ^PSDRUG(PSSIEN, "DOS1")
    PSSIZZ = 0
    PSSOZZ = 0
    if not PSSSKIPP:
        PSSSKIPP = 0
    PSSXYZ = 0
    check()
    xnw()

def stun():
    global PSSST, PSSUN
    PSSST = $P(^PSDRUG(PSSIEN, "DOS"), "^")
    PSSUN = $P(^PSDRUG(PSSIEN, "DOS"), "^", 2)

def check():
    global PSSUPRA, PSSNAT, PSSNAT1, PSSNATND, PSSNATDF, PSSNATUN, PSSNATST, PSSIZZ, PSSOZZ
    natnd()
    if PSSST != "" or PSSNATST != "":
        if (PSSUN or PSSNATUN) and (PSSNATDF and PSSNATST != ""):
            if PSSNATST not in ("", ".", ".0") and PSSNATST.isnumeric():
                if PSSNATDF in ^PS(50.606("ACONI", PSSNATUN)) and $O(^PS(50.606("ADUPI", PSSNATDF, 0))):
                    PSSXYZ = 1
                    PSSIZZ = 1
                if PSSNATDF in ^PS(50.606("ACONO", PSSNATUN)) and $O(^PS(50.606("ADUPO", PSSNATDF, 0))):
                    PSSXYZ = 1
                    PSSOZZ = 1

def natnd():
    global PSSNAT, PSSNAT1, PSSNATND, PSSNATDF, PSSNATST, PSSNATUN, PSSUPRA
    PSSNAT = +$P(^PSDRUG(PSSIEN, "ND"), "^", 3)
    PSSNAT1 = $P(^PSDRUG(PSSIEN, "ND"), "^")
    PSSNATND = $$DFSU^PSNAPIS(PSSNAT1, PSSNAT)
    PSSNATDF = $P(PSSNATND, "^")
    PSSNATST = $P(PSSNATND, "^", 4)
    PSSNATUN = $P(PSSNATND, "^", 5)
    PSSUPRA = $$SUPRA^PSSUTIL3(PSSNAT)

def xnw():
    if $G(PSSXYZ) and not $O(^PSDRUG(PSSIEN, "DOS1", 0)):
        D ^DIR K DIR
        if Y == 1:
            PSSSKIPP = 1
            D EN2^PSSUTIL(PSSIEN, 1)
        G DOSNX

def dosa():
    global PSSST, PSSUN, PSSDOSA, PSSWDXF, PSSXYZ, POSDOS, PDS, LPDOS
    PSSST = $P(^PSDRUG(PSSIEN, "DOS"), "^")
    PSSWDXF = 0
    if $P(^PSDRUG(PSSIEN, "DOS"), "^") != "" or $O(^PSDRUG(PSSIEN, "DOS1", 0)):
        if $P(^PSDRUG(PSSIEN, "DOS"), "^") != "" and $O(^PSDRUG(PSSIEN, "DOS1", 0)):
            N PSSDESTP
            XNWS()
        if $G(PSSXYZ) and not $O(^PSDRUG(PSSIEN, "DOS1", 0)):
            D ^DIR K DIR
            if Y == 1:
                PSSSKIPP = 1
                D EN2^PSSUTIL(PSSIEN, 1)
            G DOSNX
        DOSA()

def xnw():
    global PSSUPRA, PSSNAT, PSSNAT1, PSSNATND, PSSNATDF, PSSNATUN, PSSNATST
    N PSSDESTP
    W !!, "Strength from National Drug File match => ", $S($E($G(PSSNATST), 1) == "." : "0", 1: ""), $G(PSSNATST), "    ", $P($G(^PS(50.607, +$G(PSSUN), 0)), "^")
    W !, "Strength currently in the Drug File    => ", $S($E($P($G(^PSDRUG(PSSIEN, "DOS")), "^"), 1) == "." : "0", 1: ""), $P($G(^PSDRUG(PSSIEN, "DOS")), "^"), "    ", $S($P($G(^PS(50.607, +$G(PSSUN), 0)), "^")'["/" : $P($G(^(0)), "^"), 1: "")
    S PSSDESTP = 1
    D MS^PSSDSPOP
    K PSSDESTP

def dosa1():
    global PSSDOSA
    N DIC, DIR, DIE, DR, X, Y, DTOUT, DUOUT
    S DIC("W") = "W ""  ""_$S($E($P($G(^PSDRUG(PSSIEN,""DOS1"",+Y,0)),""^"",2),1)=""."":""0"",1:"""")_$P($G(^PSDRUG(PSSIEN,""DOS1"",+Y,0)),""^"",2)_""    ""_$P($G(^PSDRUG(PSSIEN,""DOS1"",+Y,0)),""^"",3)"
    D ^DIC K DIC
    I Y < 1 or $D(DTOUT) or $D(DUOUT):
        G DOSLOC
    S PSSDOSA = +Y
    W !
    S DIE("NO^") = ""
    S DA(1) = PSSIEN
    S DA = PSSDOSA
    S DR = ".01;2"
    S DIE = "^PSDRUG("_PSSIEN_",""DOS1"","
    D ^DIE K DIE
    D:'$D(Y) and not $D(DTOUT) BCMA^PSSDOSER
    I $D(Y) or $D(DTOUT):
        G DOSLOC
    W !
    G DOSA1

def dosloc():
    global PSSPCI, PSSPCO, PSSPCZ
    S PSSPCI = 0
    S PSSPCO = 0
    F PSSPCZ = 0:0 S PSSPCZ = $O(^PSDRUG(PSSIEN, "DOS1", PSSPCZ)) Q:'PSSPCZ  D
        I $P($G(^PSDRUG(PSSIEN, "DOS1", PSSPCZ, 0)), "^", 2) != "":
            S:PSSPCO=1 PSSPCI=1
            S:PSSPCO=0 PSSPCO=1
    I PSSPCI and PSSPCO:
        K DIR
        S DIR(0) = "Y"
        S DIR("B") = "N"
        S DIR("A") = "Enter/Edit Local Possible Dosages"
        D ^DIR K DIR
        I Y != 1:
            K PSSPCI
            K PSSPCO
            K PSSPCZ
            W !
            D END
            Q
    K PSSPCI
    K PSSPCO
    K PSSPCZ
    G LOCX

def loc():
    stun()
    natnd()
    pr()
    W !
    K DIC
    S DA(1) = PSSIEN
    S DIC = "^PSDRUG("_PSSIEN_",""DOS2"","
    S DIC(0) = "QEAMLZ"
    D ^DIC K DIC
    I Y < 1 or $D(DTOUT) or $D(DUOUT):
        D END
        Q
    S PSSDOSA = +Y
    S PSSOTH = $S($P($G(^PS(59.7, 1, 40.2)), "^"):1, 1:0)
    W !
    K DIE
    S DA(1) = PSSIEN
    S DA = PSSDOSA
    S DR = ".01;S:'$G(PSSOTH) Y=""@1"";3;@1;1"
    S DIE = "^PSDRUG("_PSSIEN_",""DOS2"","
    D ^DIE K DIE,PSSOTH
    I $D(Y) or $D(DTOUT):
        D END
        Q
    I $$TEST^PSSDSPOP(PSSIEN):
        K DA
        K DIE
        K DR
        N DIDEL
        S DA(1) = PSSIEN
        S DA = PSSDOSA
        S DR = "4;5"
        S DIE = "^PSDRUG("_PSSIEN_",""DOS2"","
        D ^DIE K DIE,DA,DR,DIDEL
        I $D(Y) or $D(DTOUT):
            D END
            Q
    G LOC

def lpd():
    S PSSWDXF = 0
    D:($Y + 5) > IOSL QASK
    Q:PSSWDXF
    W !!
    W "LOCAL POSSIBLE DOSAGES:"
    D
        F PDS = 0:0 S PDS = $O(^PSDRUG(PSSIEN, "DOS2", PDS)) Q:'PDS or PSSWDXF  D
            D:($Y + 5) > IOSL QASK
            Q:PSSWDXF
            S LPDOS = $G(^PSDRUG(PSSIEN, "DOS2", PDS, 0))
            W !,"  "
            I $L($P(LPDOS, "^")) <= 27:
                W $P(LPDOS, "^"), ?55, "PACKAGE: ", $P(LPDOS, "^", 2)
                D wxfpt(lpdos)
                Q
            W !, ?10, $P(LPDOS, "^")
            W !
            W ?55, "PACKAGE: ", $P(LPDOS, "^", 2)
            D wxfpt(lpdos)

def wxfpt(psswdxvl):
    N PSSWDX1, PSSWDX2, PSSWDX3, PSSWDX4, PSSWDX5, PSSWDX6
    S PSSWDX4 = ""
    S PSSWDX1 = $P(PSSWDXVL, "^", 3)
    S PSSWDX2 = $P(PSSWDXVL, "^", 5)
    S PSSWDX3 = $P(PSSWDXVL, "^", 6)
    I PSSWDX2:
        S PSSWDX4 = $P($G(^PS(51.24, +PSSWDX2, 0)), "^")
    S PSSWDX5 = $S($E(PSSWDX3) = "." : "0", 1: "")_PSSWDX3
    S PSSWDX6 = $L(PSSWDX5)
    D:($Y + 5) > IOSL QASK
    Q:PSSWDXF
    W !?4, "BCMA UNITS PER DOSE: ", PSSWDX1
    I PSSWDX6 < 12:
        D:($Y + 5) > IOSL QASK
        Q:PSSWDXF
        W !?4, "       NUMERIC DOSE: ", PSSWDX5, ?38, "DOSE UNIT: ", PSSWDX4
    D:($Y + 5) > IOSL QASK
    Q:PSSWDXF
    W !
    W ?4, "       NUMERIC DOSE: ", PSSWDX5
    D:($Y + 5) > IOSL QASK
    Q:PSSWDXF
    W !
    W ?38, "DOSE UNIT: ", PSSWDX4

def dosloc():
    S (PSSPCI, PSSPCO) = 0
    F PSSPCZ = 0:0 S PSSPCZ = $O(^PSDRUG(PSSIEN, "DOS1", PSSPCZ)) Q:'PSSPCZ  D
        I $P($G(^PSDRUG(PSSIEN, "DOS1", PSSPCZ, 0)), "^", 2) != "":
            S:PSSPCO=1 PSSPCI=1
            S:PSSPCO=0 PSSPCO=1
    I PSSPCI and PSSPCO:
        K DIR
        S DIR(0) = "Y"
        S DIR("B") = "N"
        S DIR("A") = "Enter/Edit Local Possible Dosages"
        D ^DIR K DIR
        I Y != 1:
            K PSSPCI
            K PSSPCO
            K PSSPCZ
            W !
            D END
            Q
    K PSSPCI
    K PSSPCO
    K PSSPCZ
    G LOCX

def locx():
    I PSSSKIPP:
        G LOC
    I PSSIZZ and PSSOZZ:
        G LOC
    K PSSONLYO, PSSONLYI
    I PSSIZZ and not PSSOZZ:
        S PSSONLYO = 1
    I PSSOZZ and not PSSIZZ:
        S PSSONLYI = 1
    S PSSTALK = 1
    S PSSDIEN = PSSIEN
    LOC()