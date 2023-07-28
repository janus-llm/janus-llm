# BIR/JLC-CHECK FOR SCHEDULES WITH PRN IN NAMES ;02/10/2006
# 1.0;PHARMACY DATA MANAGEMENT;**93**;9/30/97

def EN():
    global ZTSAVE, ZTSK
    ZTRTN = "ENQN^PSS0093"
    ZTDESC = "PDM - Check for schedules with PRN in name"
    ZTIO = ""
    # ^%ZTLOAD is assumed to be translated elsewhere
    # ^%ZTLOAD(ZTRTN, ZTDESC, ZTIO, ZTSAVE, ZTSK) is assumed to be translated elsewhere
    print("\n\nThe check for PRN schedules is{} queued".format("" if ZTSK else " NOT"))
    if ZTSK:
        print(" (to start NOW).\n\nYOU WILL RECEIVE A MAILMAN MESSAGE WHEN TASK #{} HAS COMPLETED.".format(ZTSK))

def ENQN():
    IEN = 0
    PSS = 6
    PSS[6][0] = ""
    while True:
        IEN = $O(^PS(51.1,IEN))
        if not IEN:
            break
        SCHED = $P($G(^PS(51.1,IEN,0)), "^")
        if len(PSS[PSS][0]) > 55:
            PSS += 1
            PSS[PSS][0] = ""
        if "PRN" in SCHED:
            PSS[PSS][0] += SCHED + ", "

# Send mail message when check is complete.
def SENDMSG():
    global XMDUZ, XMSUB, XMTEXT, XMY
    XMDUZ = "MANAGEMENT,PHARMACY DATA"
    XMSUB = "CHECK FOR PRN SCHEDULES COMPLETE"
    XMTEXT = "PSS("
    XMY(DUZ) = ""
    NOW^%DTC()
    Y = %
    # ^DD("DD") is assumed to be translated elsewhere
    PSS[1][0] = "  The check for PRN schedules completed as of {}.".format(Y)
    PSS[2][0] = ""
    PSS[3][0] = "The following schedules contain PRN. Please change the schedule type"
    PSS[4][0] = "to PRN if appropriate."
    PSS[5][0] = ""
    # ^XMD is assumed to be translated elsewhere
    ^XMD()

EN()