def PSSDSFDB():
    # WOIFO/Steve Gordon - Allows for a user to disable FDB interface during an FDB update
    # 03/17/09
    ## 1.0;PHARMACY DATA MANAGEMENT;**136**;9/30/97;Build 89

    def EN():
        # driver
        # Called from PSS ENABLE/DISABLE DB LINK option
        if not DUZ:
            DUZMSG()
            return

        OLDVAL = int(^PS(59.73,1,0))
        if not LOCK():
            return

        if not ^PS(59.73,1,0):
            NEW()
        if not QSTION(OLDVAL):
            return
        CHANGE(OLDVAL)

        if OLDVAL != 0 and int(^PS(59.73,1,0)) == 0:
            BASE = "PSPRE"
            PING^PSSHRIT(BASE)
            if ^TMP($J,BASE,"OUT",0) == 0:
                print("Connected to Vendor database successfully.")
            else:
                print("Connection could not be made to Vendor database.")
            K ^TMP($J,BASE)

        PRSRTN()
        UNLOCK()

    def DUZMSG():
        # Writes a message that a DUZ is required
        print("You are not logged into the system.")
        print("This option requires a DUZ (user ID) to be defined!")
        PRSRTN()

    def QSTION(OLDVAL):
        # input: OLDVAL-original value of the .01 field of 59.73
        # output-response to verification question (1 for yes, 0 for no)
        NEWSTAT = "ENABLE" if OLDVAL else "DISABLE"
        CURSTAT = "DISABLE" if OLDVAL else "ENABLE"
        ENFLAG = 1 if CURSTAT == "ENABLE" else 0

        HELP(DIR)
        if not OLDVAL:
            DISMSG(DIR)
        else:
            ENMSG(DIR)

        DIR(0) = "Y^A"
        DIR("B") = "NO" if ENFLAG else "YES"
        ^DIR
        if Y and ENFLAG:
            return ASK(NEWSTAT)
        elif not ENFLAG:
            return +Y

        if ENFLAG:
            if FINAL:
                print("Vendor database connection", NEWSTAT + "D" + ".")
                if NEWSTAT == "DISABLE":
                    print("REMEMBER to ENABLE the Vendor database connection AFTER task completed.")
            if not FINAL:
                print("The connection to the Vendor database remains ENABLED.")
        else:
            if FINAL:
                print("Vendor database connection enabled.")
            if not FINAL:
                print("   WARNING! The connection to the Vendor Database remains DISABLED")
                if DS^PSSDSAPI() and DS^PSSDSAPI():
                    print("NO Drug-Drug Interactions, Duplicate Therapy or Dosing Order Checks will be")
                else:
                    print("NO Drug-Drug Interactions or Duplicate Therapy Checks will be")
                print("performed while the connection is disabled!!!")

        return FINAL

    def ASK(NEWSTAT):
        # input: NEWSTAT-Either ENABLE or DISABLE
        # output: Either 1 or 0 for yes or no
        DIR(0) = "Y^A"
        DIR("B") = "NO"
        if DS^PSSDSAPI() and DS^PSSDSAPI():
            DIR("A",1) = "NO Drug-Drug Interactions, Duplicate Therapy or Dosing Order Checks"
        else:
            DIR("A",1) = "NO Drug-Drug Interactions or Duplicate Therapy Order Checks"
        DIR("A",2) = "will be performed while the connection is disabled!!!"
        DIR("A",3) = ""
        DIR("A") = "Are you sure you want to " + NEWSTAT + " the connection to the Vendor Database"
        ^DIR
        return Y

    def DISMSG(DIR):
        # input: DIR Array
        # output: sets up DIR message array
        DIR("A",1) = "The connection to the Vendor database is currently ENABLED."
        DIR("A",2) = " "
        DIR("A",3) = ""
        DIR("A") = "Do you wish to DISABLE the connection to the Vendor database"

    def ENMSG(DIR):
        # input: DIR Array
        # output: sets up DIR message array
        DIR("A",1) = "    WARNING! The connection to the Vendor database is currently DISABLED."
        DIR("A",2) = " "
        if DS^PSSDSAPI() and DS^PSSDSAPI():
            DIR("A",3) = "NO Drug-Drug Interactions, Duplicate Therapy or Dosing Order Checks"
        else:
            DIR("A",3) = "NO Drug-Drug Interactions or Duplicate Therapy Order Checks"
        DIR("A",4) = "will be performed while the connection is disabled!!!"
        DIR("A",5) = " "
        DIR("A") = "Do you wish to ENABLE the Vendor database connection"

    def NEW():
        # There will only be one entry at the top level
        DINUM = 1
        X = 0
        DIC = "^PS(59.73,"
        DIC(0) = "Z"
        FILE^DICN()

    def CHANGE(NEWVAL):
        # edit flag once it is created.
        DIE = "^PS(59.73,"
        DR = ".01///^S X=NEWVAL"
        DA = 1
        ^DIE

    def ACT(NEWVAL):
        # creates an activity log whenever FDB flag is reset to a new value
        DIC = "^PS(59.73,1,1,"
        DIC(0) = "L"
        DA(1) = 1
        X = GETNOW()
        FILE^DICN()
        ACTION = "D" if NEWVAL else "E"
        DIE = "^PS(59.73,1,1,"
        DA = +Y
        DR = "1///^S X=+DUZ;2///^S X=ACTION"
        ^DIE

    def GETNOW():
        PSNOW = NOW^%DTC
        return PSNOW

    def LOCK():
        LOCKED = 1   # SUCCESSFUL
        L +^PS(59.73,0):0
        if $T:
            print("Another terminal is modifying this field!")
            LOCKED = 0
        return LOCKED

    def UNLOCK():
        L -^PS(59.73,0)

    def HELP(DIR):
        # Returns array of help for DIR call
        if DS^PSSDSAPI() and DS^PSSDSAPI():
            DIR("?") = "Enter either 'Y' or 'N'.  No Drug-Drug Interactions, Duplicate Therapy or Dosing Order Checks will be performed while the connection is disabled!!!"
        else:
            DIR("?") = "Enter either 'Y' or 'N'.  No Drug-Drug Interactions or Duplicate Therapy Order Checks will be performed while the connection is disabled!!!"

    def CHKSTAT():
        # Called from IN^PSSHRQ2 routine
        # RETURNS A -1 if FDB is disabled and 0 if enabled
        # along with a standard message in PSSHRVL1
        STAT = int(^PS(59.73,1,0))*-1  # Returns either -1 or 0
        if STAT:
            STAT = STAT + "_" + STATMSG^PSSHRVL1()
        return STAT

    def PRSRTN():
        # calls std routine to ask user to hit return
        DIR(0) = "E"
        DIR("A") = "Press Return to Continue"
        ^DIR

    EN()

PSSDSFDB()