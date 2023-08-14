def PSSMSTR():
    # BIR/PWC-Send Master Drug File to External Interface ;04/05/04
    # 1.0;PHARMACY DATA MANAGEMENT;**82,193**;09/30/97;Build 17
    # Reference to ^PS(59 supported by IA # 1976

    # This routine will loop through the Drug file and send all drugs
    # to each dispensing machine for each outpatient site file.
    # It will only send to each site that has a dispensing machine running
    # HL7 V.2.4 and has the Master File Update enabled.
    # As part of Pharmacy Interface Automation Project (PIA), this routine
    # is modified to send all drugs to an active Pharmacy Automated Dispensing
    # Equipment (PADE), located at the point of care areas such as
    # Inpatient wards, Outpatient Clinics etc.
    # Task this job out

    def EN():
        # Begin processing PSS Master File All send drugs via HL7
        print(chr(12), end='')
        ZTSAVE,ZTRTN,ZTDESC,ZTIO,ZTDTH,X,Y = None, None, None, None, None, None
        KV()
        DIR = {}
        DIR["A"] = "Send Drug file to which External Interface below?"
        DIR[0] = "SO^1:Outpatient Interface (OPAI);2:Inpatient Interface (PADE)"
        DIR["?",1] = "  Option 1 is for sending to the Outpatient Pharmacy Automation Interface."
        DIR["?",2] = "  Option 2 is for sending to the Pharmacy Automated Dispensing Equipment (PADE)"
        DIR["?",3] = "  located at the point of care."
        DIR["?",4] = "  OR Enter '^' to quit."
        DIR["?",5] = ""
        DIR["?"] = "*Caution: This is usually done on the initial setup of the dispensing equipment."
        Y = input_func(DIR)
        if not Y:
            return
        print(f"\nYou selected to send the Drug file to the {Y[0]}\n")
        if Y == 1:
            ZTRTN = "BUILD^PSSMSTR"
            ZTDESC = "MASTER DRUG FILE UPDATE"
            ZTIO = ""
            ZTDTH = $H
            NOW^%DTC()
            PSSDTM = %
            ^%ZTLOAD()
        else:
            SPNAM, PROT = "PSS MFNM01 SERVER", None
            PROT = ^ORD(101, "B", SPNAM, 0)
            if not SNDHL7():
                print("\n*Drug transmission is not setup for PADE", end='')
                time.sleep(2)
                EN()
        EN1()
        return

    def BUILD():
        XX, DVER, DMFU, DNSNAM, DNSPORT = None, None, None, None, None
        while True:
            XX = $O(^PSDRUG(XX))
            if not XX:
                break
            while True:
                YY = $O(^PS(59, YY))
                if not YY:
                    break
                DVER = $$GET1^DIQ(59, YY_",", 105, "I")
                if DVER != "2.4":  # HL7 2.4
                    continue
                DMFU = $$GET1^DIQ(59, YY_",", 105.2)
                if DMFU != "YES":  # enable MFU
                    continue
                DNSNAM = $$GET1^DIQ(59, YY_",", 2006)  # DNS name of dispense machine
                DNSPORT = $$GET1^DIQ(59, YY_",", 2007)  # Port # of dispense machine
                if DNSNAM != "":
                    DRG^PSSDGUPD(XX, "NEW", DNSNAM, DNSPORT)
        XX, YY, DVER, DMFU, DNSNAM, DNSPORT = None, None, None, None, None, None
        return

    def PADE():
        PSSG, PSSAP, PSSDRG, SPNAM, I = None, None, None, None, None
        SPNAM = "PSS MFNM01 SERVER"
        PSSDRG = 0
        while True:
            PSSDRG = $O(^PSDRUG(PSSDRG))
            if not PSSDRG:
                break
            if $G(^PSDRUG(PSSDRG, "I")) and ($P($G(^("I")), "^") < DT):
                continue
            PSSAP = $P($G(^(2)), "^", 3)
            PSSG = 0
            for I in range(1, len(PSSCPK)+1):
                if PSSAP.contains(PSSCPK[I]):
                    PSSG = 1
                    break
            if not PSSG:
                continue
            SPADE()
        return

    def SPADE():
        XX, VR, DNSNAM, DNSPORT, PSSD, PSSNM = None, None, None, None, None, None
        XX = 0
        while True:
            XX = $O(^PS(58.7, XX))
            if not XX:
                break
            PSSD = $G(^PS(58.7, XX, 0))
            if not PSSD:
                continue
            PSSNM = $P(PSSD, "^")
            DNSNAM = $P(PSSD, "^", 2)
            DNSPORT = $P(PSSD, "^", 3)
            if PSSNM == "" or DNSNAM == "" or DNSPORT == "":
                continue
            VR = $P(PSSD, "^", 4)
            if VR and (VR < DT):
                continue
            VR = $P(PSSD, "^", 5)
            if VR == "X" or VR == "":
                continue
            PROCESS1^PSSHLDFS(SPNAM, PSSDRG, "MAD", DNSNAM, DNSPORT)
        return

    def SNDHL7():
        XX, VR, FLG, SPNAM, DNSNAM, DNSPORT, PSSD, PSSNM = None, None, None, None, None, None, None, None
        FLG = 0
        XX = 0
        while True:
            XX = $O(^PS(58.7, XX))
            if not XX or FLG:
                break
            PSSD = $G(^PS(58.7, XX, 0))
            if not PSSD:
                continue
            PSSNM = $P(PSSD, "^")
            DNSNAM = $P(PSSD, "^", 2)
            DNSPORT = $P(PSSD, "^", 3)
            if PSSNM == "" or DNSNAM == "" or DNSPORT == "":
                continue
            VR = $P(PSSD, "^", 4)
            if VR and (VR < DT):
                continue
            VR = $P(PSSD, "^", 5)
            if VR == "X" or VR == "":
                continue
            FLG = VR if VR == "U" else (2 if VR == "N" else 3)
        return FLG

    def KV():
        DIR, DIRUT, DUOUT, DTOUT = None, None, None, None
        return

    def SDRG():
        PSSDRUG, DIC, DUOUT, DTOUT = None, None, None, None
        PSSDRUG = {}
        while True:
            DIC(0) = "QEAM"
            DIC = "^PSDRUG("
            DIC("S") = "$S('$D(^PSDRUG(+Y,""I"")):1,'^(""I""):1,DT'>^(""I""):1,1:0)"
            Y = DIC()
            if Y < 0:
                break
            PSSDRUG(Y) = ""
        if DUOUT or DTOUT or (not PSSDRUG):
            EN()
        PSSDRG, SPNAM = None, "PSS MFNM01 SERVER"
        PSSDRG = 0
        while True:
            PSSDRG = $O(PSSDRUG(PSSDRG))
            if not PSSDRG:
                break
            SPADE()
        return

    EN()
    return