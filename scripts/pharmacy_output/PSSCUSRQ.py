def PSSCUSRQ():
    # Request Customization changes
    def MESS():
        print("\nNo Action Taken.\n")
        input("Press Return to continue")
    
    def NDI():
        nonlocal PSSCQOUT
        print()
        PSSCQNDD = input("Enter Interacting Drug Names (free text): ")
        if PSSCQNDD == '^':
            PSSCQOUT = 1
            return
        
        PSSCQNSV = input("Enter Severity (1: Critical, 2: Significant): ")
        if PSSCQNSV == '^':
            PSSCQOUT = 1
            return
        
        print("\nYou must now enter a reason or references for this request. <word processing>\n")
        input("Press Return to continue, '^' to exit")
        print()
        print("References/Reason for Request:")
        while True:
            line = input()
            if line == '^':
                PSSCQOUT = 1
                break
            elif line == '':
                break
    
    def DISC():
        nonlocal PSSCQOUT
        print()
        PSSCQSDD = input("Enter Interacting Drug Names (free text): ")
        if PSSCQSDD == '^':
            PSSCQOUT = 1
            return
        
        PSSCQSSV = input("Change Severity To (1: Critical, 2: Significant): ")
        if PSSCQSSV == '^':
            PSSCQOUT = 1
            return
        
        print("\nYou must now enter a reason or references for this request. <word processing>\n")
        input("Press Return to continue, '^' to exit")
        print()
        print("References/Reason for Request:")
        while True:
            line = input()
            if line == '^':
                PSSCQOUT = 1
                break
            elif line == '':
                break
    
    def DTC():
        nonlocal PSSCQOUT
        print("\nYou must now enter a description of the change/problem. <word processing>\n")
        input("Press Return to continue, '^' to exit")
        print()
        print("Description of change/problem:")
        while True:
            line = input()
            if line == '^':
                PSSCQOUT = 1
                break
            elif line == '':
                break
    
    def DC():
        # Dosing Change
        pass
    
    def FIN():
        nonlocal PSSCQOUT
        PSSCQOUT = 0
    
    def TEST(PSSCQPMM):
        nonlocal PSSCQOUT, PSSCQCCT
        if PSSCQPMM not in (1, 2, 3, 4):
            print("\nProblem with option, please enter a Remedy ticket.\n")
            PSSCQOUT = 1
            return
        
        PSSCQCCT = 1 if PROD() else 0
        if not PSSCQCCT:
            print("\nNOTE: This is a test account. Regardless of your response to the 'Transmit'")
            print("prompt, this request will NOT be sent forward for national review.\n")
        
        transmit = input("Transmit? (Y/N): ")
        if transmit.upper() == 'N':
            PSSCQVIS = 1
            SEND(PSSCQPMM)
            print("\nMail message only sent to you in Vista Mail.")
            input("Press Return to continue")
        elif transmit.upper() == 'Y':
            SEND(PSSCQPMM)
            print("\nMail message transmitted for review.")
            input("Press Return to continue")
        else:
            PSSCQOUT = 1
    
    def SEND(PSSCQVAL):
        nonlocal PSSCQCCT
        if PSSCQVAL == 1:
            NDITXT()
        elif PSSCQVAL == 2:
            DISCTXT()
        elif PSSCQVAL == 3:
            DTCTXT()
        elif PSSCQVAL == 4:
            DCTXT()
        
        XMSUB = {
            1: "New Drug Interaction Request",
            2: "Drug Interaction Severity Change Request",
            3: "Duplicate Therapy Change Request",
            4: "Dosing Change Request"
        }.get(PSSCQVAL, "Unknown Request")
        
        XMDUZ = DUZ
        XMTEXT = "^TMP($J,'PSSCQTXT',"
        XMY = [DUZ]
        if not PSSCQVIS and PSSCQCCT:
            XMY.append("VAOITVHITPSCUSTOMREQ@va.gov")
        
        print("\nMail message transmitted or sent to you only in Vista Mail.")
        input("Press Return to continue")
    
    def NDITXT():
        print("\nRequest New Drug Interaction:")
        print(PSSCQNDD)
        print("\nSeverity:")
        print("CRITICAL" if PSSCQNSV == 1 else "SIGNIFICANT")
        print()
        print("References/Reason for Request:")
        for line in ^TMP($J,"PSSCQWP"):
            print(line)
    
    def DISCTXT():
        print("\nDrug-Drug Interaction:")
        print(PSSCQSDD)
        print("\nSeverity Change To:")
        print("CRITICAL" if PSSCQSSV == 1 else "SIGNIFICANT")
        print()
        print("References/Reason for Request:")
        for line in ^TMP($J,"PSSCQWP"):
            print(line)
    
    def DTCTXT():
        print("\nDuplicate Therapy Change Description/Problem:")
        print()
        print("References/Reason for Request:")
        for line in ^TMP($J,"PSSCQWP"):
            print(line)
    
    def DCTXT():
        # Dosing Change
        pass
    
    def KLWRD():
        ^TMP($J,"PSSCQWP") = []
    
    # Main code
    
    PSSCQOUT = 0
    while True:
        print()
        PSSCQANS = input("Select one of the above (N: New Drug Interaction, S: Drug Interaction Severity Change, T: Duplicate Therapy Change, D: Dosing Change): ")
        if PSSCQANS == 'N':
            NDI()
            FIN()
            if PSSCQOUT:
                MESS()
            break
        elif PSSCQANS == 'S':
            DISC()
            FIN()
            if PSSCQOUT:
                MESS()
            break
        elif PSSCQANS == 'T':
            DTC()
            FIN()
            if PSSCQOUT:
                MESS()
            break
        elif PSSCQANS == 'D':
            DC()
            FIN()
            if PSSCQOUT:
                MESS()
            break
        else:
            MESS()