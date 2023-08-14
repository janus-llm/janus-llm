def CHL():
    PSSMRTL1 = len(PSSMRPP4)
    if PSSMRTL1 < 37:
        ^TMP($J,"PSSMRPTX",PSSMRPCT,0) = "     Recommend mapping to Standard Route: " + PSSMRPP4
        PSSMRPCT += 1
        return
    ^TMP($J,"PSSMRPTX",PSSMRPCT,0) = "     Recommend mapping to Standard Route:"
    PSSMRPCT += 1
    ^TMP($J,"PSSMRPTX",PSSMRPCT,0) = "       " + PSSMRPP4
    PSSMRPCT += 1

def ATTN():
    ^TMP($J,"PSSMRPTX",PSSMRPCT,0) = "PLEASE REVIEW, MAY REQUIRE YOUR ATTENTION!"
    PSSMRPCT += 1
    ^TMP($J,"PSSMRPTX",PSSMRPCT,0) = " "
    PSSMRPCT += 1

def ZERO():
    PSSMRPHH = 0
    ^TMP($J,"PSSMRPTX",PSSMRPCT,0) = "The following entries in the Standard Medication Routes (#51.23) File have had"
    PSSMRPCT += 1
    ^TMP($J,"PSSMRPTX",PSSMRPCT,0) = "changes to the associated First DataBank Med Route and/or Replacement Term."
    PSSMRPCT += 1
    ^TMP($J,"PSSMRPTX",PSSMRPCT,0) = " "
    PSSMRPCT += 1
    PSSMRPCT += 1
    while PSSMRPHH = 0:
        PSSMRPHH = $O(^TMP("XUMF EVENT",$J,51.23,"BEFORE",PSSMRPHH))
        if not PSSMRPHH:
            break
        PSSMRPJ1 = $P(^TMP("XUMF EVENT",$J,51.23,"BEFORE",PSSMRPHH,0),"^",2)
        PSSMRPJ2 = $P(^TMP("XUMF EVENT",$J,51.23,"AFTER",PSSMRPHH,0),"^",2)
        PSSMRPA1 = $P(^TMP("XUMF EVENT",$J,51.23,"BEFORE",PSSMRPHH,"VUID"),"^",3)
        PSSMRPA2 = $P(^TMP("XUMF EVENT",$J,51.23,"AFTER",PSSMRPHH,"VUID"),"^",3)
        PSSMRPA3,PSSMRPA4 = 0
        if PSSMRPJ1 != PSSMRPJ2:
            PSSMRPA3 = 1
        if PSSMRPA1 != PSSMRPA2:
            PSSMRPA4 = 1
        if not PSSMRPA3 and not PSSMRPA4:
            continue
        if PSSMRPA3:
            PSSMRPA5 = $S($G(PSSMRPJ2) != "": $G(PSSMRPJ2), 1: "<deleted>")
        if PSSMRPA4:
            PSSMRPA6 = $S(not $G(PSSMRPA2): "<deleted>", 1: $P(^PS(51.23,+$G(PSSMRPA2),0),"^"))
            PSSMRPA7 = $S(not $G(PSSMRPA2): "<deleted>", $P(^PS(51.23,+$G(PSSMRPA2),0),"^",2) != "": $P(^PS(51.23,+$G(PSSMRPA2),0),"^",2), 1: "(None)")
        PSSMRPJ5 = 1
        PSSMRPA8 = PSSMRPHH
        PSSMRPA9 = STAT^PSSMRTUP(PSSMRPA8)
        ^TMP($J,"PSSMRPTX",PSSMRPCT,0) = "   " + $P(^PS(51.23,+PSSMRPHH,0),"^") + $S(not PSSMRPA9: "   (Inactive)", 1: "")
        PSSMRPCT += 1
        if PSSMRPA3:
            ^TMP($J,"PSSMRPTX",PSSMRPCT,0) = "     FDB Route: " + $G(PSSMRPA5)
            PSSMRPCT += 1
        if PSSMRPA4:
            ^TMP($J,"PSSMRPTX",PSSMRPCT,0) = "     Replacement Term: " + $G(PSSMRPA6)
            PSSMRPCT += 1
            if $G(PSSMRPA2):
                ^TMP($J,"PSSMRPTX",PSSMRPCT,0) = "     Replacement Term FDB Route: " + $G(PSSMRPA7)
                PSSMRPCT += 1
    if not PSSMRPJ5:
        ^TMP($J,"PSSMRPTX",PSSMRPCT,0) = "   (None)"
        PSSMRPCT += 1
    ^TMP($J,"PSSMRPTX",PSSMRPCT,0) = " "
    PSSMRPCT += 1

def INACZ():
    PSSMRPWH = 0
    while PSSMRPWH = 0:
        PSSMRPWH = $O(^TMP("XUMF EVENT",$J,51.23,"BEFORE",PSSMRPWH))
        if not PSSMRPWH:
            break
        PSSMRPWJ = ^TMP("XUMF EVENT",$J,51.23,"BEFORE",PSSMRPWH,0)
        if PSSMRPWJ = "":
            continue
        PSSMRPW1 = $P(^TMP("XUMF EVENT",$J,51.23,"BEFORE",PSSMRPWH,0),"^",2)
        PSSMRPW2 = $P(^TMP("XUMF EVENT",$J,51.23,"AFTER",PSSMRPWH,0),"^",2)
        if PSSMRPW1 = PSSMRPW2:
            continue
        PSSMRPW7 = ""
        PSSMRPW8 = PSSMRPWH
        PSSMRPW9 = RPLCMNT^XTIDTRM(51.23,PSSMRPW8)
        if $P(PSSMRPW9,";") != PSSMRPWH:
            PSSMRPW7 = $P(PSSMRPW9,";")
        if not $D(^TMP($J,"PSSMRPCC","INACT",PSSMRPWH)):
            ^TMP($J,"PSSMRPCC","INACT",PSSMRPWH) = $S(not $P($G(^TMP("XUMF EVENT",$J,51.23,"AFTER",PSSMRPWH,"REPLACED BY")),"^"):0,1:$P($G(^TMP("XUMF EVENT",$J,51.23,"AFTER",PSSMRPWH,"REPLACED BY")),"^"))
        if not ^TMP($J,"PSSMRPCC","INACT",PSSMRPWH) and $G(PSSMRPW7):
            ^TMP($J,"PSSMRPCC","INACT",PSSMRPWH) = $G(PSSMRPW7)