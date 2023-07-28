# PSSPRMIX ;BIR/RTR-PREMIX REPORT ;07/14/07
# 1.0;PHARMACY DATA MANAGEMENT;**129**;9/30/07;Build 67

def REP():
    print("\nThis report displays only those solutions in the IV Solutions (#52.7) File")
    print("that are marked as PreMix IV Solutions, or it displays all Solutions.")
    PSSPRTP = input("Print report for PreMix (P), or All IV Solutions (A): (P/A): Premix (P): ")

    if PSSPRTP != "P" and PSSPRTP != "A":
        print("\nNo Action taken.")
        return

    print("\nThis report is designed for 80 column format!")

    if input("Press Return to continue or enter '^' to exit: ") == '^':
        return

    print("\nSolution PreMix report for IV Solutions marked as PreMix" if PSSPRTP == "P" else "Solution PreMix report for all IV Solutions")
    print("Page: 1")
    print("-" * 79)

    PSSPRM = ""
    PSSPRMCT = 1
    while not PSSPROUT and PSSPRM != None:
        PSSPRM = next(iter(PSSPRMAR), None)
        if PSSPRM == None:
            break

        PSSPRMIN = 0
        while PSSPRMIN != None:
            PSSPRMIN = next(iter(PSSPRMAR), None)
            if PSSPRMIN == None:
                break

            PSSPRMAR = {}
            PSSPRMTP = f"{PSSPRMIN},"
            GETS^DIQ(52.7, PSSPRMTP, ".01;.02;1;2;8;9;17;18", "IE", PSSPRMAR)

            if PSSPRTP == "P" and not PSSPRMAR[52.7][PSSPRMTP][18]["I"]:
                continue

            PSSPRMFD = 1

            if PSSPRML3 < 37:
                print(f"\n{' '*18}Print Name: {PSSPRMAR[52.7][PSSPRMTP][.01]['E']}")
                print(f"{' '*30}Volume: {PSSPRMAR[52.7][PSSPRMTP][2]['E']}")
            else:
                print(f"\n{' '*18}Print Name: {PSSPRMAR[52.7][PSSPRMTP][.01]['E']}")
                print(f"{' '*30}Volume: {PSSPRMAR[52.7][PSSPRMTP][2]['E']}")

            print(f"\n{' '*14}Print Name {{2}}: {PSSPRMAR[52.7][PSSPRMTP][.02]['E']}")

            print(f"\n{' '*20}Synonyms: ")
            for PSSPRMSY in PSSPRMIN[3]:
                PSSPRMSU = f"{PSSPRMSY},{PSSPRMIN},"
                PSSPRMSX = GET1^DIQ(52.703, PSSPRMSU, ".01")
                if PSSPRMSC:
                    print(f"{' '*30}{PSSPRMSX}")
                else:
                    print(f"{' '*30}{PSSPRMSX}")
                    PSSPRMSC = 1

            print(f"\n{' '*16}Generic Drug: {PSSPRMAR[52.7][PSSPRMTP][1]['E']}")

            PSSPRML1 = len(PSSPRMAR[52.7][PSSPRMTP][9]['E'])
            PSSPRMDF = PSSPRMAR[52.7][PSSPRMTP][9]['I']
            PSSPRML2 = 0
            if PSSPRMDF:
                PSSPRMDZ = f"{PSSPRMDF},"
                PSSPRMDQ = GET1^DIQ(50.7, PSSPRMDZ, ".02")
                PSSPRML2 = len(PSSPRMDQ)
            PSSPRML3 = PSSPRML1 + PSSPRML2

            print(f"\n{' '*5}Pharmacy Orderable Item: {PSSPRMAR[52.7][PSSPRMTP][9]['E']}")
            if PSSPRML3 < 47:
                print(f"{' '*30}{PSSPRMDQ}")
            else:
                print(f"{' '*30}{PSSPRMDQ}")

            print(f"\n{' '*11}Inactivation Date: {PSSPRMAR[52.7][PSSPRMTP][8]['E']}")
            print(f"\nUsed in IV Fluid Order Entry: {PSSPRMAR[52.7][PSSPRMTP][17]['E']}")
            print(f"{' '*22}PreMix: {PSSPRMAR[52.7][PSSPRMTP][18]['E']}")

            if PSSPRTP == "P":
                if not PSSPROUT and not PSSPRMFD:
                    print("\nNo IV Solutions marked as PreMixes found.")
            else:
                print("\nEnd of Report.")

    if PSSPRMDV == "C":
        print("\nEnd of Report.")
        if input("Press Return to continue: "):
            return
    else:
        print()

    print("\nEnd of Report.")
    ^%ZISC
    if ZTQUEUED:
        ZTREQ = "@"

REP()