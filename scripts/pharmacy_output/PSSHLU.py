def INIT():
    # set up HL7 application variables
    # if '$D(HLNDAP) S HLNDAP=0,HLNDAP=$O(^HL(770,"B","OE/RR",HLNDAP)),HLSDT="PS" D INIT^HLTRANS I $D(HLERR) W !!?7,"THE HL7 INITIALIZATION FAILED",!! Q
    PSJI = 1
    PSSHINST = $P($G(^DIC(4,+$P($G(^XMB(1,1,"XUS")),"^",17),99)),"^")
    ^TMP("HLS",$J,"PS",PSJI) = "MSH|^~\&|PHARMACY|"_$G(PSSHINST)_"|||||MFN"
    K PSSHINST
    PSJCLEAR = "F J=0:1:LIMIT S FIELD(J)="""""

def SEGMENT(LIMIT):
    SUBSEG = 0
    SEGMENT(SUBSEG) = ""
    for J in range(0, LIMIT+1):
        if SEGMENT(SUBSEG) <= "":
            SEGMENT(SUBSEG) = FIELD(J)
        else:
            SEGLENGT = len(SEGMENT(SUBSEG)) + len(FIELD(J))
            if SEGLENGT < 245:
                SEGMENT(SUBSEG) = SEGMENT(SUBSEG) + "|" + FIELD(J)
            elif len(SEGMENT(SUBSEG)) == 245:
                SUBSEG = SUBSEG + 1
                SEGMENT(SUBSEG) = "|" + FIELD(J)
            else:
                SEGMENT(SUBSEG) = SEGMENT(SUBSEG) + "|" + FIELD(J)[:244-len(SEGMENT(SUBSEG))]
                SUBSEG = SUBSEG + 1
                SEGMENT(SUBSEG) = FIELD(J)[SEGLENGT-245:SEGLENGT+1]
    PSJI = PSJI + 1
    ^TMP("HLS",$J,"PS",PSJI) = SEGMENT(0)
    for J in range(1, len(SEGMENT)):
        ^TMP("HLS",$J,"PS",PSJI,J) = SEGMENT(J)

def CALL(HLEVN):
    # call DHCP HL7 package -or- protocol, to pass Orders
    # HLEVN = number of segments in message
    # D EN^HLTRANS W:$D(HLERR) !!?7,"***ERROR IN CREATING HL7 MAIL MESSAGE***"
    MSG = "^TMP(""HLS"",$J,""PS"")"
    D MSG^XQOR("PS EVSEND OR",.MSG)

def MF(HLEVN):
    # call DHCP HL7 -or- protocol, to pass Master File transactions
    # HLEVN = number of segments in message
    # D EN^HLTRANS W:$D(HLERR) !!?7,"***ERROR IN CREATING HL7 MAIL MESSAGE***"
    MSG = "^TMP(""HLS"",$J,""PS"")"
    D MSG^XQOR("PS MFSEND OR",.MSG)

def SCH(HLEVN):
    # call to pass Schedule file to OE/RR
    MSG = "^TMP(""HLS"",$J,""PS"")"
    D MSG^XQOR("PS EVSEND SCH",.MSG)

def USAGE(POI):
    USAGE = {}
    for I in ["O", "I", "B", "A", "V"]:
        USAGE[I] = 0
    if $P($G(^PS(50.7,POI,0)),"^",3):
        return IVFLAG()
    else:
        I = ""
        for PSSDDINX in range(0, len(^PS(50.7,"A50",POI))):
            if !$P($G(^PSDRUG(PSSDDINX,"I")),"^") or +$P($G(^("I")),"^") > DT:
                USAGE = $P($G(^PSDRUG(PSSDDINX,2)),"^",3)
                USAGE = USAGE.replace("U", "I")
                for I in ["O", "I"]:
                    if USAGE in I:
                        USAGE[I] = USAGE[I] + 1
            for PSSOAD in range(0, len(^PSDRUG("A526",PSSDDINX))):
                if $P($G(^PS(52.6,PSSOAD,"I")),"^") and +$P($G(^PS(52.6,PSSOAD,"I")),"^") <= DT:
                    USAGE["I"] = USAGE["I"] + 1
                    USAGE["V"] = USAGE["V"] + 1
                    if $P($G(^PS(52.6,PSSOAD,0)),"^",13):
                        USAGE["A"] = USAGE["A"] + 1
            for PSSOSD in range(0, len(^PSDRUG("A527",PSSDDINX))):
                if $P($G(^PS(52.7,PSSOSD,"I")),"^") and +$P($G(^PS(52.7,PSSOSD,"I")),"^") <= DT:
                    USAGE["I"] = USAGE["I"] + 1
                    USAGE["V"] = USAGE["V"] + 1
                    if $P($G(^PS(52.7,PSSOSD,0)),"^",13):
                        USAGE["B"] = USAGE["B"] + 1
    return IVFLAG()

def IVFLAG():
    USAGE = ""
    for I in ["O", "I", "B", "A", "V"]:
        USAGE = USAGE + I + USAGE[I]
    return USAGE