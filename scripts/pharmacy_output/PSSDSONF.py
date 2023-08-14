def PSSDSONF():
    # BIR/RTR-Dosing On/Off Parameter ;07/09/12
    # 1.0;PHARMACY DATA MANAGEMENT;**160**;9/30/97;Build 76

    def EN():
        # Turn Dosing On and Off
        PSSDONA = int(^PS(59.7,1,81))
        PSSDONTS = 1 if not PROD^XUPROD() else 0

        print("Dosing Order Checks are currently ENABLED." if PSSDONA else "WARNING! Dosing Order Checks are currently DISABLED.")

        if PSSDONA:
            ON()
        else:
            print("No Dosing Order Checks will be performed during order entry in CPRS or Pharmacy while Dosing Order Checks are disabled!!!")
            LCK()
            if not PSSDONLK:
                END()
                return
            answer = input("Do you wish to ENABLE Dosing Order Checks (YES/NO)? ")
            if answer != "YES":
                print("WARNING! Dosing Order Checks remain DISABLED.")
                UNLCK()
                END()
                return
            PSSDONR = {}
            PSSDONR["59.7,1,95"] = 1
            FILE^DIE("", PSSDONR)
            if not int(^PS(59.7,1,81)):
                print("UNABLE to enable Dosing Order Checks! Please contact local support for assistance.")
                UNLCK()
                END()
                return
            print("Dosing Order Checks ENABLED.")
            TMES()
            SEND(1,0)
            SEND(1,1)
            UNLCK()
            END()

    def ON():
        LCK()
        if not PSSDONLK:
            END()
            return
        answer = input("Do you wish to DISABLE Dosing Order Checks (YES/NO)? ")
        if answer != "YES":
            print("Dosing Order Checks remain ENABLED.")
            UNLCK()
            END()
            return
        answer = input("Have you received authorization from Pharmacy Benefits Management (PBM) to take this action (YES/NO)? ")
        if answer != "YES":
            print("Dosing Order Checks remain ENABLED.")
            UNLCK()
            END()
            return
        print("NO Dosing Order Checks will be performed during order entry in CPRS or Pharmacy while Dosing Order Checks are disabled!!!")
        print("Notification of this action will be sent to PBM and local VistA PSS ORDER CHECKS mail group.")
        answer = input("Are you sure you want to DISABLE Dosing Order Checks (YES/NO)? ")
        if answer != "YES":
            print("Dosing Order Checks remain ENABLED.")
            UNLCK()
            END()
            return
        PSSDONR = {}
        PSSDONR["59.7,1,95"] = 0
        FILE^DIE("", PSSDONR)
        if int(^PS(59.7,1,81)):
            print("UNABLE to disable Dosing Order Checks! Please contact local support for assistance.")
            UNLCK()
            END()
            return
        print("Dosing Order Checks DISABLED.")
        TMES()
        SEND(0,0)
        SEND(0,1)
        UNLCK()
        END()

    def TMES():
        if not PSSDONTS:
            print("Note: This is a TEST account. This request will NOT be sent forward to PBM on Outlook mail.")
        else:
            print("NOTIFICATION OF THIS ACTION has been forwarded to PBM and local VistA PSS ORDER CHECKS mail group.")

    def SEND(PSSDONW, PSSDONAB):
        if not PSSDONTS and PSSDONAB:
            return
        XMSUB = "DOSING ORDER CHECKS " + ("ENABLED" if PSSDONW else "DISABLED")
        XMDUZ = DUZ
        NOW^%DTC()
        PSSDONSC = %Y
        PSSDONLC = $$SITE^VASITE()[2]
        PSSDONDZ = $$GET1^DIQ(200, DUZ + ", .01")
        ^TMP($J, "PSSDSOTX") = [PSSDONDZ + " from " + PSSDONLC, "has " + ("ENABLED" if PSSDONW else "DISABLED") + " Dosing Order Checks on " + PSSDONSC + "."]
        XMTEXT = "^TMP($J, ""PSSDSOTX"")"
        if not PSSDONAB:
            XMY(DUZ) = ""
            XMY("G.PSS ORDER CHECKS") = ""
        if PSSDONTS and PSSDONAB:
            XMY("MOCHADOSINGDISCONNECTNOTIFY@va.gov") = ""
        ^XMD()
        K ^TMP($J, "PSSDSOTX")

    def LCK():
        PSSDONLK = 0
        L +^PS(59.7,1,81):$S($G(DILOCKTM) > 0:DILOCKTM, 1:3)
        if not $T:
            print("Another person is editing the Dosing On/Off Switch.")
            return
        PSSDONLK = 1

    def UNLCK():
        L -^PS(59.7,1,81)

    def END():
        input("Press Return to continue")
    
    def ACLOG():
        if X1[0] == X2[0]:
            return
        PSSDHAH("DA") = DA
        NOW^%DTC()
        PSSDHAHX(59.782, "+1," + PSSDHAH("DA") + ",", ".01") = %
        PSSDHAHX(59.782, "+1," + PSSDHAH("DA") + ",", "1") = DUZ
        PSSDHAHX(59.782, "+1," + PSSDHAH("DA") + ",", "2") = X2[0]
        UPDATE^DIE("", PSSDHAHX)
    
    EN()

PSSDSONF()