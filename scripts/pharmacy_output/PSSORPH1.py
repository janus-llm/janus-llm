def PSSORPH1():
    # BIR/RTR-Dosage by Dispense Units per Dose ;03/24/00
    # 1.0;PHARMACY DATA MANAGEMENT;**34,38,49,64,69,138**;9/30/97;Build 5
    # Reference to ^PS(50.607 supported by DBIA 2221

    DLOOP = PD
    if not DLOOP:
        return
    # SET PSSX(1)=-1^DDRUG IS INACTIVE OR NOT APP USE ANYMORE?
    if (
        (
            (
                (I := $P($G(^PSDRUG(DLOOP, "I")), "^"))
                and (I <= DT)
            )
        )
        and (
            (PSSX[1] := "-1^Drug is inactive")
        )
    )
        return
    # I $P($G(^PSDRUG(DLOOP,2)),"^",3)'[TYPE S PSSX(1)="-1^Drug not marked for application" Q
    PSSTRN = $P($G(^PSDRUG(DLOOP, "DOS")), "^")
    PSSUNITZ = $P($G(^PSDRUG(DLOOP, "DOS")), "^", 2)
    PSSUNITX = $S(
        ($P($G(^PS(50.607, +PSSUNITZ, 0)), "^") != "")
        and ($P($G(^(0)), "^") not in "/"),
        $P($G(^(0)), "^"),
        1,
        "",
    )
    PSSDSE = +$P($G(^PS(50.7, POPD, 0)), "^", 2)
    PSSVERB = $P($G(^PS(50.606, PSSDSE, "MISC")), "^")
    PSSPREP = $P($G(^("MISC")), "^", 3)
    PSNNN = None
    for PSNN in range(0, 0):
        if not PSNN or (PSNNN := $P($G(^(PSNN, 0)), "^")) != "":
            break
    PSSDOSE = ""
    PSSUNTS = $P(
        $G(
            ^PS(
                50.607,
                +$P($G(^PSDRUG(DLOOP, "DOS")), "^", 2),
                0,
            )
        ),
        "^",
    )
    PSSUDOS = PSSUPD
    # S PSSDOSE=PSSUDOS*+PSSTRN
    PSSDOSE = +$FN(PSSUDOS * +PSSTRN, "", 10)
    if not PSSTRN or not PSSUNITZ:
        SET()
        LEADP()
        return
    if not PSSDOSE or not PSSUDOS:
        SET()
        LEADP()
        return
    DCNT1 = 1
    PARN()
    PSSX[DCNT1] = (
        str(PSSDOSE)
        + "^"
        + (
            str(PSSUNITZ)
            if "OX".find(TYPE) != -1
            else str(PSSUNTS)
        )
        + "^"
        + str(PSSUDOS)
        + "^"
        + str(DLOOP)
        + "^"
        + str(PSSTRN)
        + "^"
        + (str(PSSNP) if PSSNP != "" else str(PSNNN))
        + "^"
        + $P($G(^PS(50.606, +PSSDSE, 0)), "^")
        + "^"
        + str(PSSVERB)
        + "^"
        + str(PSSPREP)
    )
    PSSNP = None
    PSSA = 1
    SLS()
    PSIEN = DLOOP = +$P(PSSX[PSSA], "^", 4)
    PSSMAX = None
    if TYPE.find("O") != -1:
        MAX()
    PSSX["DD", PSIEN] = (
        $P($G(^PSDRUG(PSIEN, 0)), "^")
        + "^"
        + $P($G(^(660)), "^", 6)
        + "^"
        + $P($G(^(0)), "^", 9)
        + "^"
        + $P($G(^(660)), "^", 8)
        + "^"
        + $P($G(^("DOS")), "^")
        + "^"
        + str(PSSUNITX)
        + "^"
        + str(PSSMAX)
    )
    REQS()
    PSSX["DD", PSIEN] = (
        PSSX["DD", PSIEN]
        + "^"
        + str(PSSREQS)
        + "^"
        + str(PSNNN)
        + "^"
        + str(PSSVERB)
    )
    LEADP()


def SET():
    PARN()
    PSSX[1] = (
        "^"
        + (
            str(PSSUNITZ)
            if "OX".find(TYPE) != -1
            else str(PSSUNTS)
        )
        + "^^"
        + str(DLOOP)
        + "^"
        + str(PSSTRN)
        + "^"
        + (str(PSSNP) if PSSNP != "" else str(PSNNN))
        + "^"
        + $P($G(^PS(50.606, +PSSDSE, 0)), "^")
        + "^"
        + str(PSSVERB)
        + "^"
        + str(PSSPREP)
    )
    PSIEN = DLOOP = +$P(PSSX[1], "^", 4)
    PSSMAX = None
    if TYPE.find("O") != -1:
        MAX()
    PSSX["DD", PSIEN] = (
        $P($G(^PSDRUG(PSIEN, 0)), "^")
        + "^"
        + $P($G(^(660)), "^", 6)
        + "^"
        + $P($G(^(0)), "^", 9)
        + "^"
        + $P($G(^(660)), "^", 8)
        + "^"
        + $P($G(^("DOS")), "^")
        + "^"
        + str(PSSUNITX)
        + "^"
        + str(PSSMAX)
    )
    REQS()
    PSSX["DD", PSIEN] = (
        PSSX["DD", PSIEN]
        + "^"
        + str(PSSREQS)
        + "^"
        + str(PSNNN)
        + "^"
        + str(PSSVERB)
    )


def AMP():
    # Replace & with AND when returning local doses to CPRS
    PSSAB, PSSABT, PSSABA, PSSABL, PSSABZ, PSSABX, PSSABF1, PSSABF2 = None, None, None, None, None, None, None, None
    if PSLOCV == "&":
        PSLOCV = " AND "
        return
    if PSLOCV[0] == "&":
        if PSLOCV[1] == " ":
            PSLOCV = " AND" + PSLOCV[1:]
        else:
            PSLOCV = " AND " + PSLOCV[1:]
    PSSABL = len(PSLOCV)
    if PSLOCV[PSSABL-1] == "&":
        if PSLOCV[PSSABL-2] == " ":
            PSLOCV = PSLOCV[0:PSSABL-1] + "AND "
        else:
            PSLOCV = PSLOCV[0:PSSABL-1] + " AND "
    if "&" not in PSLOCV:
        return
    PSSABT = 0
    for PSSAB in range(1, len(PSLOCV) + 1):
        if PSLOCV[PSSAB-1] == "&":
            PSSABT += 1
    PSSABA = [None] * (PSSABT + 1)
    for PSSAB in range(1, PSSABT + 2):
        PSSABA[PSSAB-1] = PSLOCV.split("&")[0]
        PSLOCV = "&".join(PSLOCV.split("&")[1:])
    for PSSABZ in range(1, PSSABT + 1):
        PSSABF1, PSSABF2 = None, None
        if len(PSSABA[PSSABZ-1]) > 0:
            PSSABF1 = PSSABA[PSSABZ-1][-1]
        if PSSABA.get(PSSABZ, None) is not None:
            PSSABF2 = PSSABA[PSSABZ][0]
        PSSABA[PSSABZ-1] = (
            PSSABA[PSSABZ-1]
            + ("AND" if PSSABF1 == " " else " AND")
            + ("" if PSSABF2 == " " else " ")
        )
    PSLOCV = ""
    for PSSABX in range(1, PSSABT + 2):
        PSLOCV += PSSABA.get(PSSABX, "")
    return


def AMPCHK():
    # CHECK FOR THE "&" IN THE NOUN FILED OF THE DOSAGE FORM FILE #50.606
    PSLOCV = X
    AMP()
    X = PSLOCV.strip(" LR")
    return


PSSORPH1()