def EN():
    MNUADD()
    BMES("Generating Mail Message....")
    MAIL()
    BMES("Mail message sent.")

def MAIL():
    PSS17PLP = 0
    XMTEXT = ""
    XMY = ""
    XMSUB = "PSS*1*117 Installation Complete"
    XMDUZ = "PSS*1*117 Install"
    XMROU = ""
    XMYBLOB = ""
    XMZ = ""
    XMDUN = ""
    PSS17REC = ""
    ^TMP($J,"PSS17PTX") = ""
    while True:
        PSS17PLP = $O(@XPDGREF@("PSSMLMSG",PSS17PLP))
        if not PSS17PLP:
            break
        ^TMP($J,"PSS17PTX",PSS17PLP) = @XPDGREF@("PSSMLMSG",PSS17PLP)
    DIFROM()
    ^TMP($J,"PSS17PTX") = ""

def MNUADD():
    BMES("Linking New PSS Menus....")
    PSSMNUAF = 1
    PSSMNUA2 = 0
    while True:
        PSSMNUA1 = $O(@XPDGREF@("PSSMLMSG",PSSMNUA1))
        if not PSSMNUA1:
            break
        PSSMNUA2 += 1
    PSSMNUA2 += 1
    PSSMNUA = ADD("PSS MGR", "PSS ORDER CHECK MANAGEMENT", "", 4)
    if not PSSMNUA:
        MNUADD1()
    PSSMNUA = ADD("PSS ORDER CHECK MANAGEMENT", "PSS ORDER CHECK CHANGES", "", 1)
    if not PSSMNUA:
        MNUADD2()
    PSSMNUA = ADD("PSS ORDER CHECK MANAGEMENT", "PSS REPORT LOCAL INTERACTIONS", "", 2)
    if not PSSMNUA:
        MNUADD3()
    PSSMNUA = ADD("PSS PEPS SERVICES", "PSS SCHEDULE PEPS INTERFACE CK", "", 3)
    if not PSSMNUA:
        MNUADD4()
    PSSMNUA = ADD("PSS ADDITIVE/SOLUTION", "PSS IV ADDITIVE REPORT", "", 1)
    if not PSSMNUA:
        MNUADD11()
    PSSMNUA = ADD("PSS ADDITIVE/SOLUTION", "PSS IV SOLUTION REPORT", "", 2)
    if not PSSMNUA:
        MNUADD12()
    PSSMNUA = ADD("PSS ADDITIVE/SOLUTION", "PSS MARK PREMIX SOLUTIONS", "", 3)
    if not PSSMNUA:
        MNUADD13()
    REB()
    if PSSMNUAF:
        BMES("All Menu options linked successfully....")
    
def MNUADD1():
    PSSMNUAF = 0
    BMES("Unable to link PSS ORDER CHECK MANAGEMENT Menu Option....")
    @XPDGREF@("PSSMLMSG",PSSMNUA2) = "Unable to link PSS ORDER CHECK MANAGEMENT Menu Option to PSS MGR Menu"
    PSSMNUA2 += 1
    @XPDGREF@("PSSMLMSG",PSSMNUA2) = "Please Log a Remedy Ticket and refer to this message."
    PSSMNUA2 += 1
    @XPDGREF@("PSSMLMSG",PSSMNUA2) = " "
    PSSMNUA2 += 1

def MNUADD2():
    PSSMNUAF = 0
    BMES("Unable to link PSS ORDER CHECK CHANGES Option....")
    @XPDGREF@("PSSMLMSG",PSSMNUA2) = "Unable to link PSS ORDER CHECK CHANGES to PSS ORDER CHECK MANAGEMENT Menu"
    PSSMNUA2 += 1
    @XPDGREF@("PSSMLMSG",PSSMNUA2) = "Please Log a Remedy Ticket and refer to this message."
    PSSMNUA2 += 1
    @XPDGREF@("PSSMLMSG",PSSMNUA2) = " "
    PSSMNUA2 += 1

def MNUADD3():
    PSSMNUAF = 0
    BMES("Unable to link PSS REPORT LOCAL INTERACTIONS Option....")
    @XPDGREF@("PSSMLMSG",PSSMNUA2) = "Unable to link PSS REPORT LOCAL INTERACTIONS to PSS ORDER CHECK MANAGEMENT Menu"
    PSSMNUA2 += 1
    @XPDGREF@("PSSMLMSG",PSSMNUA2) = "Please Log a Remedy Ticket and refer to this message."
    PSSMNUA2 += 1
    @XPDGREF@("PSSMLMSG",PSSMNUA2) = " "
    PSSMNUA2 += 1

def MNUADD4():
    PSSMNUAF = 0
    BMES("Unable to link PSS SCHEDULE PEPS INTERFACE CK Option....")
    @XPDGREF@("PSSMLMSG",PSSMNUA2) = "Unable to link PSS SCHEDULE PEPS INTERFACE CK to PSS PEPS SERVICES Menu"
    PSSMNUA2 += 1
    @XPDGREF@("PSSMLMSG",PSSMNUA2) = "Please Log a Remedy Ticket and refer to this message."
    PSSMNUA2 += 1
    @XPDGREF@("PSSMLMSG",PSSMNUA2) = " "
    PSSMNUA2 += 1

def MNUADD11():
    PSSMNUAF = 0
    BMES("Unable to link PSS IV ADDITIVE REPORT Option....")
    @XPDGREF@("PSSMLMSG",PSSMNUA2) = "Unable to link PSS IV ADDITIVE REPORT to PSS ADDITIVE/SOLUTION Menu"
    PSSMNUA2 += 1
    @XPDGREF@("PSSMLMSG",PSSMNUA2) = "Please Log a Remedy Ticket and refer to this message."
    PSSMNUA2 += 1
    @XPDGREF@("PSSMLMSG",PSSMNUA2) = " "
    PSSMNUA2 += 1

def MNUADD12():
    PSSMNUAF = 0
    BMES("Unable to link PSS IV SOLUTION REPORT Option....")
    @XPDGREF@("PSSMLMSG",PSSMNUA2) = "Unable to link PSS IV SOLUTION REPORT to PSS ADDITIVE/SOLUTION Menu"
    PSSMNUA2 += 1
    @XPDGREF@("PSSMLMSG",PSSMNUA2) = "Please Log a Remedy Ticket and refer to this message."
    PSSMNUA2 += 1
    @XPDGREF@("PSSMLMSG",PSSMNUA2) = " "
    PSSMNUA2 += 1

def MNUADD13():
    PSSMNUAF = 0
    BMES("Unable to link PSS MARK PREMIX SOLUTIONS Option....")
    @XPDGREF@("PSSMLMSG",PSSMNUA2) = "Unable to link PSS MARK PREMIX SOLUTIONS to PSS ADDITIVE/SOLUTION Menu"
    PSSMNUA2 += 1
    @XPDGREF@("PSSMLMSG",PSSMNUA2) = "Please Log a Remedy Ticket and refer to this message."
    PSSMNUA2 += 1
    @XPDGREF@("PSSMLMSG",PSSMNUA2) = " "
    PSSMNUA2 += 1

def REB():
    PSSMNUR = DELETE("PSS MGR", "PSS WARNING BUILDER")
    PSSMNUR = DELETE("PSS MGR", "PSS WARNING MAPPING")
    PSSMNUR = DELETE("PSS MGR", "PSS PEPS SERVICES")
    PSSMNUA = ADD("PSS MGR", "PSS ADDITIVE/SOLUTION", "", 17)
    if not PSSMNUA:
        MNUADD5()
    PSSMNUA = ADD("PSS MGR", "PSS WARNING BUILDER", "", 18)
    if not PSSMNUA:
        MNUADD6()
    PSSMNUA = ADD("PSS MGR", "PSS WARNING MAPPING", "", 19)
    if not PSSMNUA:
        MNUADD7()
    PSSMNUA = ADD("PSS MGR", "PSS PEPS SERVICES", "", 20)
    if not PSSMNUA:
        MNUADD8()

def MNUADD5():
    PSSMNUAF = 0
    BMES("Unable to link PSS ADDITIVE/SOLUTION Option....")
    @XPDGREF@("PSSMLMSG",PSSMNUA2) = "Unable to link PSS ADDITIVE/SOLUTION to PSS MGR Menu"
    PSSMNUA2 += 1
    @XPDGREF@("PSSMLMSG",PSSMNUA2) = "Please Log a Remedy Ticket and refer to this message."
    PSSMNUA2 += 1
    @XPDGREF@("PSSMLMSG",PSSMNUA2) = " "
    PSSMNUA2 += 1

def MNUADD6():
    PSSMNUAF = 0
    BMES("Unable to re-link PSS WARNING BUILDER Option....")
    @XPDGREF@("PSSMLMSG",PSSMNUA2) = "Unable to RE-link PSS WARNING BUILDER to PSS MGR Menu"
    PSSMNUA2 += 1
    @XPDGREF@("PSSMLMSG",PSSMNUA2) = "Please Log a Remedy Ticket and refer to this message."
    PSSMNUA2 += 1
    @XPDGREF@("PSSMLMSG",PSSMNUA2) = " "
    PSSMNUA2 += 1

def MNUADD7():
    PSSMNUAF = 0
    BMES("Unable to re-link PSS WARNING MAPPING CK Option....")
    @XPDGREF@("PSSMLMSG",PSSMNUA2) = "Unable to re-link PSS WARNING MAPPING to PSS MGR Menu"
    PSSMNUA2 += 1
    @XPDGREF@("PSSMLMSG",PSSMNUA2) = "Please Log a Remedy Ticket and refer to this message."
    PSSMNUA2 += 1
    @XPDGREF@("PSSMLMSG",PSSMNUA2) = " "
    PSSMNUA2 += 1

def MNUADD8():
    PSSMNUAF = 0
    BMES("Unable to re-link PSS PEPS SERVICES Option....")
    @XPDGREF@("PSSMLMSG",PSSMNUA2) = "Unable to re-link PSS PEPS SERVICES to PSS MGR Menu"
    PSSMNUA2 += 1
    @XPDGREF@("PSSMLMSG",PSSMNUA2) = "Please Log a Remedy Ticket and refer to this message."
    PSSMNUA2 += 1

def MNUADD11():
    PSSMNUAF = 0
    BMES("Unable to link PSS IV ADDITIVE REPORT Option....")
    @XPDGREF@("PSSMLMSG",PSSMNUA2) = "Unable to link PSS IV ADDITIVE REPORT to PSS ADDITIVE/SOLUTION Menu"
    PSSMNUA2 += 1
    @XPDGREF@("PSSMLMSG",PSSMNUA2) = "Please Log a Remedy Ticket and refer to this message."
    PSSMNUA2 += 1
    @XPDGREF@("PSSMLMSG",PSSMNUA2) = " "
    PSSMNUA2 += 1

def MNUADD12():
    PSSMNUAF = 0
    BMES("Unable to link PSS IV SOLUTION REPORT Option....")
    @XPDGREF@("PSSMLMSG",PSSMNUA2) = "Unable to link PSS IV SOLUTION REPORT to PSS ADDITIVE/SOLUTION Menu"
    PSSMNUA2 += 1
    @XPDGREF@("PSSMLMSG",PSSMNUA2) = "Please Log a Remedy Ticket and refer to this message."
    PSSMNUA2 += 1
    @XPDGREF@("PSSMLMSG",PSSMNUA2) = " "
    PSSMNUA2 += 1

def MNUADD13():
    PSSMNUAF = 0
    BMES("Unable to link PSS MARK PREMIX SOLUTIONS Option....")
    @XPDGREF@("PSSMLMSG",PSSMNUA2) = "Unable to link PSS MARK PREMIX SOLUTIONS to PSS ADDITIVE/SOLUTION Menu"
    PSSMNUA2 += 1
    @XPDGREF@("PSSMLMSG",PSSMNUA2) = "Please Log a Remedy Ticket and refer to this message."
    PSSMNUA2 += 1
    @XPDGREF@("PSSMLMSG",PSSMNUA2) = " "
    PSSMNUA2 += 1