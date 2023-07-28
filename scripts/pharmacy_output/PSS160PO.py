#PSS160PO ;BIR/RTR-Post Install routine for patch PSS*1*160 ;02/18/11
#;;1.0;PHARMACY DATA MANAGEMENT;**160**;9/30/97;Build 76
#;External reference to ^XOB(18.02 supported by DBIA 5814
#;External reference to ^XOB(18.12 supported by DBIA 5813
#
#
#EN ;Do Mail Message
def EN():
    PSSMXUA1 = None
    PSSMXUA2 = None
    PSSMXUA2 = 0
    while PSSMXUA1 is not None:
        PSSMXUA1 = None
        PSSMXUA2 = PSSMXUA2 + 1
    PSSMXUA2 = PSSMXUA2 + 1
    ADDVAL()
    MNUADD()
    SETWS()
    print("Generating Mail Message....")

#EN2 ;
def EN2():
    MAIL()
    print("Mail message sent.")
    if "^PS(59.7,1,81)" in "":
        "^PS(59.7,1,81)" = 1

#MAIL ;Send mail message
def MAIL():
    PSS60REC = None
    PSS60PLP = None
    XMTEXT = None
    XMY = None
    XMSUB = None
    XMDUZ = None
    XMMG = None
    XMSTRIP = None
    XMROU = None
    XMYBLOB = None
    XMZ = None
    XMDUN = None
    "^TMP($J,""PSS60PTX"")" = None
    while PSS60PLP is not None:
        PSS60PLP = None
        "^TMP($J,""PSS60PTX"",PSS60PLP)" = None
    XMSUB = "PSS*1*160 Installation Complete"
    XMDUZ = "PSS*1*160 Install"
    XMTEXT = "^TMP($J,""PSS60PTX"","
    PSS60REC = ""
    while PSS60REC != "":
        PSS60REC = None
        XMY(PSS60REC) = None
    DIFROM()
    "^TMP($J,""PSS60PTX"")" = None

#MNUADD ;Add PSS DRUG DOSING LOOKUP option to PSS DOSAGE MANAGEMENT menu option
def MNUADD():
    print("Linking New PSS DRUG DOSING LOOKUP Option....")
    PSSMXUA = None
    PSSMXUAF = None
    PSSMXUAF = 0
    PSSMXUA = ADD^XPDMENU("PSS DOSAGES MANAGEMENT", "PSS DRUG DOSING LOOKUP", "", 9)
    if not PSSMXUA:
        PSSMXUAF = 1
        print("Unable to link PSS DRUG DOSING LOOKUP Option....")
        print("Please log a Remedy Ticket for this issue.")
        "^TMP($J,""PSSMLMSG"",PSSMXUA2)" = "Unable to link PSS DRUG DOSING LOOKUP Option to PSS DOSAGES MANAGEMENT Menu"
        PSSMXUA2 = PSSMXUA2 + 1
        "^TMP($J,""PSSMLMSG"",PSSMXUA2)" = " "
        PSSMXUA2 = PSSMXUA2 + 1
        "^TMP($J,""PSSMLMSG"",PSSMXUA2)" = "Please log a Remedy Ticket and refer to this message."
        PSSMXUA2 = PSSMXUA2 + 1
        LINE()
    if not PSSMXUAF:
        print("New PSS DRUG DOSING LOOKUP option linked successfully...")

    print("Linking New PSS TRAILING SPACES REPORT Option....")
    PSSMXUA = None
    PSSMXUAF = None
    PSSMXUAF = 0
    PSSMXUA = ADD^XPDMENU("PSS DOSAGES MANAGEMENT", "PSS TRAILING SPACES REPORT", "", 10)
    if not PSSMXUA:
        PSSMXUAF = 1
        print("Unable to link PSS TRAILING SPACES REPORT Option....")
        print("Please log a Remedy Ticket for this issue.")
        "^TMP($J,""PSSMLMSG"",PSSMXUA2)" = "Unable to link PSS TRAILING SPACES REPORT Option to PSS DOSAGES MANAGEMENT Menu"
        PSSMXUA2 = PSSMXUA2 + 1
        "^TMP($J,""PSSMLMSG"",PSSMXUA2)" = " "
        PSSMXUA2 = PSSMXUA2 + 1
        "^TMP($J,""PSSMLMSG"",PSSMXUA2)" = "Please log a Remedy Ticket and refer to this message."
        PSSMXUA2 = PSSMXUA2 + 1
        LINE()
    if not PSSMXUAF:
        print("New PSS TRAILING SPACES REPORT option linked successfully...")

#ADDVAL ; Final validation of data
def ADDVAL():
    print("Validating new Dose Unit File (#51.24) entries.")
    PSSADUC1 = None
    PSSADUC2 = None
    PSSADUC5 = None
    PSSADUC6 = None
    PSSADUC7 = None
    PSSADUC8 = None
    PSSADUK1 = None
    PSSADUK2 = None
    PSSADUK3 = None
    PSSATYPE = None
    (PSSADUK1, PSSADUK2, PSSADUK3) = (0, 0, 0)
    PSSATYPE = "FILM(S)"
    PSSADUC1 = FIND1^DIC(51.24,"","X",PSSATYPE,"B")
    if int(PSSADUC1) != 52:
        ADDKTM()
        PSSADUK1 = 1
        ADDLUN()

    if ADDCHK():
        PSSADUK1 = 1
        ADDLUN()

    if "^PS(51.24,52,0)" != "FILM(S)^FILMS^1":
        PSSADUK1 = 1
        ADDLUN()

    for PSSADUC5 in ["FILM;1","FILMS;2"]:
        if PSSADUK1:
            break
        PSSADUC6 = PSSADUC5.split(";")[0]
        PSSADUC7 = PSSADUC5.split(";")[1]
        PSSADUC8 = FIND1^DIC(51.242,",52,","X",PSSADUC6,"B")
        if ADDCHK():
            PSSADUK1 = 1
            break
        if int(PSSADUC8) != int(PSSADUC7):
            PSSADUK1 = 1
            break

    if not PSSADUK1:
        ADDFLM()

    PSSATYPE = "ELISA UNIT(S)"
    PSSADUC2 = FIND1^DIC(51.24,"","X",PSSATYPE,"B")
    if int(PSSADUC2) != 53:
        ADDKTM()
        PSSADUK2 = 1
        ADDMIL()

    if ADDCHK():
        PSSADUK2 = 1
        ADDLNX()

    if "^PS(51.24,53,0)" != "ELISA UNIT(S)^ELISA UNIT^0":
        PSSADUK2 = 1
        ADDLNX()

    for PSSADUC5 in ["EL UNIT;1","ELISA UNITS;2","ELISA UNIT;3","EL.U.;4","ELISA UNT;5","ELU;6"]:
        if PSSADUK2:
            break
        PSSADUC6 = PSSADUC5.split(";")[0]
        PSSADUC7 = PSSADUC5.split(";")[1]
        PSSADUC8 = FIND1^DIC(51.242,",53,","X",PSSADUC6,"B")
        if ADDCHK():
            PSSADUK2 = 1
            break
        if int(PSSADUC8) != int(PSSADUC7):
            PSSADUK2 = 1
            break

    ADDKTM()
    if not PSSADUK2:
        ADDMIL2()

    if not PSSADUK3:
        ADDMIL()

    if not PSSADUK1 and not PSSADUK2 and not PSSADUK3:
        print("DOSE UNITS File (#51.24) entries are correct.")
        return
    if PSSADUK1:
        ADDMS("FILM(S)")
    if PSSADUK2:
        ADDMS("ELISA UNIT(S)")
    if PSSADUK3:
        ADDMS("MILLIONUNIT(S)")

#MAIL ;Send mail message
def MAIL():
    PSS60REC = None
    PSS60PLP = None
    XMTEXT = None
    XMY = None
    XMSUB = None
    XMDUZ = None
    XMMG = None
    XMSTRIP = None
    XMROU = None
    XMYBLOB = None
    XMZ = None
    XMDUN = None
    "^TMP($J,""PSS60PTX"")" = None
    while PSS60PLP is not None:
        PSS60PLP = None
        "^TMP($J,""PSS60PTX"",PSS60PLP)" = "^XPDGREF@(""PSSMLMSG"",PSS60PLP)"
    XMSUB = "PSS*1*160 Installation Complete"
    XMDUZ = "PSS*1*160 Install"
    XMTEXT = "^TMP($J,""PSS60PTX"","
    PSS60REC = ""
    while PSS60REC != "":
        PSS60REC = None
        XMY(PSS60REC) = None
    DIFROM()
    "^TMP($J,""PSS60PTX"")" = None

#MNUADD ;Add PSS DRUG DOSING LOOKUP option to PSS DOSAGE MANAGEMENT menu option
def MNUADD():
    print("Linking New PSS DRUG DOSING LOOKUP Option....")
    PSSMXUA = None
    PSSMXUAF = None
    PSSMXUAF = 0
    PSSMXUA = ADD^XPDMENU("PSS DOSAGES MANAGEMENT", "PSS DRUG DOSING LOOKUP", "", 9)
    if not PSSMXUA:
        PSSMXUAF = 1
        print("Unable to link PSS DRUG DOSING LOOKUP Option....")
        print("Please log a Remedy Ticket for this issue.")
        "^TMP($J,""PSSMLMSG"",PSSMXUA2)" = "Unable to link PSS DRUG DOSING LOOKUP Option to PSS DOSAGES MANAGEMENT Menu"
        PSSMXUA2 = PSSMXUA2 + 1
        "^TMP($J,""PSSMLMSG"",PSSMXUA2)" = " "
        PSSMXUA2 = PSSMXUA2 + 1
        "^TMP($J,""PSSMLMSG"",PSSMXUA2)" = "Please log a Remedy Ticket and refer to this message."
        PSSMXUA2 = PSSMXUA2 + 1
        LINE()
    if not PSSMXUAF:
        print("New PSS DRUG DOSING LOOKUP option linked successfully...")

    print("Linking New PSS TRAILING SPACES REPORT Option....")
    PSSMXUA = None
    PSSMXUAF = None
    PSSMXUAF = 0
    PSSMXUA = ADD^XPDMENU("PSS DOSAGES MANAGEMENT", "PSS TRAILING SPACES REPORT", "", 10)
    if not PSSMXUA:
        PSSMXUAF = 1
        print("Unable to link PSS TRAILING SPACES REPORT Option....")
        print("Please log a Remedy Ticket for this issue.")
        "^TMP($J,""PSSMLMSG"",PSSMXUA2)" = "Unable to link PSS TRAILING SPACES REPORT Option to PSS DOSAGES MANAGEMENT Menu"
        PSSMXUA2 = PSSMXUA2 + 1
        "^TMP($J,""PSSMLMSG"",PSSMXUA2)" = " "
        PSSMXUA2 = PSSMXUA2 + 1
        "^TMP($J,""PSSMLMSG"",PSSMXUA2)" = "Please log a Remedy Ticket and refer to this message."
        PSSMXUA2 = PSSMXUA2 + 1
        LINE()
    if not PSSMXUAF:
        print("New PSS TRAILING SPACES REPORT option linked successfully...")

#ADDVAL ; Final validation of data
def ADDVAL():
    print("Validating new Dose Unit File (#51.24) entries.")
    PSSADUC1 = None
    PSSADUC2 = None
    PSSADUC5 = None
    PSSADUC6 = None
    PSSADUC7 = None
    PSSADUC8 = None
    PSSADUK1 = None
    PSSADUK2 = None
    PSSADUK3 = None
    PSSATYPE = None
    (PSSADUK1, PSSADUK2, PSSADUK3) = (0, 0, 0)
    PSSATYPE = "FILM(S)"
    PSSADUC1 = FIND1^DIC(51.24,"","X",PSSATYPE,"B")
    if int(PSSADUC1) != 52:
        ADDKTM()
        PSSADUK1 = 1
        ADDLUN()

    if ADDCHK():
        PSSADUK1 = 1
        ADDLUN()

    if "^PS(51.24,52,0)" != "FILM(S)^FILMS^1":
        PSSADUK1 = 1
        ADDLUN()

    for PSSADUC5 in ["FILM;1","FILMS;2"]:
        if PSSADUK1:
            break
        PSSADUC6 = PSSADUC5.split(";")[0]
        PSSADUC7 = PSSADUC5.split(";")[1]
        PSSADUC8 = FIND1^DIC(51.242,",52,","X",PSSADUC6,"B")
        if ADDCHK():
            PSSADUK1 = 1
            break
        if int(PSSADUC8) != int(PSSADUC7):
            PSSADUK1 = 1
            break

    if not PSSADUK1:
        ADDFLM()

    PSSATYPE = "ELISA UNIT(S)"
    PSSADUC2 = FIND1^DIC(51.24,"","X",PSSATYPE,"B")
    if int(PSSADUC2) != 53:
        ADDKTM()
        PSSADUK2 = 1
        ADDMIL()

    if ADDCHK():
        PSSADUK2 = 1
        ADDLNX()

    if "^PS(51.24,53,0)" != "ELISA UNIT(S)^ELISA UNIT^0":
        PSSADUK2 = 1
        ADDLNX()

    for PSSADUC5 in ["EL UNIT;1","ELISA UNITS;2","ELISA UNIT;3","EL.U.;4","ELISA UNT;5","ELU;6"]:
        if PSSADUK2:
            break
        PSSADUC6 = PSSADUC5.split(";")[0]
        PSSADUC7 = PSSADUC5.split(";")[1]
        PSSADUC8 = FIND1^DIC(51.242,",53,","X",PSSADUC6,"B")
        if ADDCHK():
            PSSADUK2 = 1
            break
        if int(PSSADUC8) != int(PSSADUC7):
            PSSADUK2 = 1
            break

    ADDKTM()
    if not PSSADUK2:
        ADDMIL2()

    if not PSSADUK3:
        ADDMIL()

    if not PSSADUK1 and not PSSADUK2 and not PSSADUK3:
        print("DOSE UNITS File (#51.24) entries are correct.")
        return
    if PSSADUK1:
        ADDMS("FILM(S)")
    if PSSADUK2:
        ADDMS("ELISA UNIT(S)")
    if PSSADUK3:
        ADDMS("MILLIONUNIT(S)")

#SETWS ;define DOSING_INFO web service
def SETWS():
    PSSWSERV = None
    PSSWSER2 = None
    PSSWPEPS = None
    PSSWSCNT = None
    PSSWSMSG = None
    PSSWSSTA = None
    PSSWSERR = None
    DA = None
    DIE = None
    DIC = None
    DR = None
    X = None
    Y = None
    DLAYGO = None
    PSSWSCNT = 0
    DIC = "^XOB(18.12,"
    X = "PEPS"
    DIC(0) = "X"
    DIC(0) = "X"
    DIC(0) = "X"
    DIC(0) = "X"
    Y = None
    PSSWPEPS = +Y
    print("Beginning DOSING_INFO Web Service definition for PEPS web server: ")
    if PSSWPEPS == -1:
        print("PEPS Web Server is not defined. Please contact product support.")
        PSSWSERR = 1
        "^TMP($J,""PSSMLMSG"",PSSMXUA2)" = "PEPS Web Server isn't defined and DOSING_INFO Web Service couldn't be"
        PSSMXUA2 = PSSMXUA2 + 1
        "^TMP($J,""PSSMLMSG"",PSSMXUA2)" = "created.  Please log a Remedy Ticket and refer to this message."
        PSSMXUA2 = PSSMXUA2 + 1
        LINE()

    "^XOB(18.02,"
    X = "DOSING_INFO"
    DIC(0) = "X"
    DIC(0) = "X"
    DIC(0) = "X"
    DIC(0) = "X"
    Y = None
    PSSWSERV = +Y
    L +^XOB(18.12,PSSWPEPS):20
    if not T:
        print("Unable to lock file 18.12 to enable DOSING_INFO web service. Please ")
        print("contact product support.")
        "^TMP($J,""PSSMLMSG"",PSSMXUA2)" = "Unable to lock file 18.12 to enable DOSING_INFO web service."
        PSSMXUA2 = PSSMXUA2 + 1
        "^TMP($J,""PSSMLMSG"",PSSMXUA2)" = "Please log a Remedy Ticket and refer to this message."
        PSSMXUA2 = PSSMXUA2 + 1
        PSSWSERR = 1

    if PSSWSER2 == -1:
        PSSENABL()
        return

    PSSWSSTA = GET1^DIQ(18.121,PSSWSER2_",1",".06","I")
    PSSENAB2()
    return

#PSSENABL ;
def PSSENABL():
    DIC = "^XOB(18.12,"_PSSWPEPS_",100,"
    DLAYGO = 18.121
    DIC(0) = "L"
    DA(1) = PSSWPEPS
    X = "DOSING_INFO"
    "^XOB(18.12,"_PSSWPEPS_",100)" = ""
    PSSENAB2()
    return

#PSSENAB2 ;
def PSSENAB2():
    DIE = "^XOB(18.12,"_PSSWPEPS_",100,"
    DR = ".06///ENABLE"
    DA(1) = PSSWPEPS
    DA = PSSWSER2
    "^XOB(18.12,"_PSSWPEPS_",100,"_PSSWSER2_",1)" = ""
    PSSWSSTA = GET1^DIQ(18.121,PSSWSER2_",1",".06","I")
    if PSSWSSTA:
        print("DOSING_INFO web service has been enabled.")
    return

#LINE ;
def LINE():
    "^TMP($J,""PSSMLMSG"",PSSMXUA2)" = " "
    PSSMXUA2 = PSSMXUA2 + 1
    return

#ADDFLM ;Validate synonyms and cross references for FILM(S)
def ADDFLM():
    if "^PS(51.24,52,1,1,0)" != "FILM":
        PSSADUK1 = 1
        return
    if "^PS(51.24,52,1,2,0)" != "FILMS":
        PSSADUK1 = 1
        return
    if not "^PS(51.24,52,1,""B"",""FILM"",1)":
        PSSADUK1 = 1
        return
    if not "^PS(51.24,52,1,""B"",""FILMS"",2)":
        PSSADUK1 = 1
        return
    if not "^PS(51.24,""B"",""FILM(S)"",52)":
        PSSADUK1 = 1
        return
    if not "^PS(51.24,""C"",""FILMS"",52)":
        PSSADUK1 = 1
        return
    if not "^PS(51.24,""D"",""FILM"",52,1)":
        PSSADUK1 = 1
        return
    if not "^PS(51.24,""D"",""FILMS"",52,2)":
        PSSADUK1 = 1
        return

#ADDELU ;Validate synonyms and cross references for ELISA UNIT(S)
def ADDELU():
    if "^PS(51.24,53,1,1,0)" != "EL UNIT":
        PSSADUK2 = 1
        return
    if "^PS(51.24,53,1,2,0)" != "ELISA UNITS":
        PSSADUK2 = 1
        return
    if "^PS(51.24,53,1,3,0)" != "ELISA UNIT":
        PSSADUK2 = 1
        return
    if "^PS(51.24,53,1,4,0)" != "EL.U.":
        PSSADUK2 = 1
        return
    if "^PS(51.24,53,1,5,0)" != "ELISA UNT":
        PSSADUK2 = 1
        return
    if "^PS(51.24,53,1,6,0)" != "ELU":
        PSSADUK2 = 1
        return
    if not "^PS(51.24,53,1,""B"",""EL UNIT"",1)":
        PSSADUK2 = 1
        return
    if not "^PS(51.24,53,1,""B"",""EL.U."",4)":
        PSSADUK2 = 1
        return
    if not "^PS(51.24,53,1,""B"",""ELISA UNIT"",3)":
        PSSADUK2 = 1
        return
    if not "^PS(51.24,53,1,""B"",""ELISA UNITS"",2)":
        PSSADUK2 = 1
        return
    if not "^PS(51.24,53,1,""B"",""ELISA UNT"",5)":
        PSSADUK2 = 1
        return
    if not "^PS(51.24,53,1,""B"",""ELU"",6)":
        PSSADUK2 = 1
        return
    if not "^PS(51.24,""B"",""ELISA UNIT(S)"",53)":
        PSSADUK2 = 1
        return
    if not "^PS(51.24,""C"",""ELISA UNIT"",53)":
        PSSADUK2 = 1
        return
    if not "^PS(51.24,""D"",""EL UNIT"",53,1)":
        PSSADUK2 = 1
        return
    if not "^PS(51.24,""D"",""EL.U."",53,4)":
        PSSADUK2 = 1
        return
    if not "^PS(51.24,""D"",""ELISA UNIT"",53,3)":
        PSSADUK2 = 1
        return
    if not "^PS(51.24,""D"",""ELISA UNITS"",53,2)":
        PSSADUK2 = 1
        return
    if not "^PS(51.24,""D"",""ELISA UNT"",53,5)":
        PSSADUK2 = 1
        return
    if not "^PS(51.24,""D"",""ELU"",53,6)":
        PSSADUK2 = 1
        return

#ADDFLM ;Validate synonyms and cross references for FILM(S)
def ADDFLM():
    if "^PS(51.24,52,1,1,0)" != "FILM":
        PSSADUK1 = 1
        return
    if "^PS(51.24,52,1,2,0)" != "FILMS":
        PSSADUK1 = 1
        return
    if not "^PS(51.24,52,1,""B"",""FILM"",1)":
        PSSADUK1 = 1
        return
    if not "^PS(51.24,52,1,""B"",""FILMS"",2)":
        PSSADUK1 = 1
        return
    if not "^PS(51.24,""B"",""FILM(S)"",52)":
        PSSADUK1 = 1
        return
    if not "^PS(51.24,""C"",""FILMS"",52)":
        PSSADUK1 = 1
        return
    if not "^PS(51.24,""D"",""FILM"",52,1)":
        PSSADUK1 = 1
        return
    if not "^PS(51.24,""D"",""FILMS"",52,2)":
        PSSADUK1 = 1
        return

#ADDMIL ;Validate synonyms and cross references for MILLIONUNIT(S)
def ADDMIL():
    if "^PS(51.24,23,1,1,0)" != "MU":
        PSSADUK3 = 1
        return
    if "^PS(51.24,23,1,2,0)" != "MIU":
        PSSADUK3 = 1
        return
    if "^PS(51.24,23,1,3,0)" != "MILU":
        PSSADUK3 = 1
        return
    if "^PS(51.24,23,1,4,0)" != "MILI U":
        PSSADUK3 = 1
        return
    if "^PS(51.24,23,1,5,0)" != "MILI UNIT":
        PSSADUK3 = 1
        return
    if "^PS(51.24,23,1,6,0)" != "MILI UNITS":
        PSSADUK3 = 1
        return
    if "^PS(51.24,23,1,7,0)" != "MILLION UNT":
        PSSADUK3 = 1
        return
    if "^PS(51.24,23,1,8,0)" != "MILLION UNIT":
        PSSADUK3 = 1
        return
    if "^PS(51.24,23,1,9,0)" != "MILLION UNITS":
        PSSADUK3 = 1
        return
    if not "^PS(51.24,23,1,""B"",""MILI U"",4)":
        PSSADUK3 = 1
        return
    if not "^PS(51.24,23,1,""B"",""MILI UNIT"",5)":
        PSSADUK3 = 1
        return
    if not "^PS(51.24,23,1,""B"",""MILI UNITS"",6)":
        PSSADUK3 = 1
        return
    if not "^PS(51.24,23,1,""B"",""MILLION UNIT"",8)":
        PSSADUK3 = 1
        return
    if not "^PS(51.24,23,1,""B"",""MILLION UNITS"",9)":
        PSSADUK3 = 1
        return
    if not "^PS(51.24,23,1,""B"",""MILLION UNT"",7)":
        PSSADUK3 = 1
        return
    if not "^PS(51.24,23,1,""B"",""MILU"",3)":
        PSSADUK3 = 1
        return
    if not "^PS(51.24,23,1,""B"",""MIU"",2)":
        PSSADUK3 = 1
        return
    if not "^PS(51.24,23,1,""B"",""MU"",1)":
        PSSADUK3 = 1
        return
    if not "^PS(51.24,""B"",""MILLIONUNIT(S)"",23)":
        PSSADUK3 = 1
        return
    if not "^PS(51.24,""C"",""MILLIONUNIT(S)"",23)":
        PSSADUK3 = 1
        return 
    if not "^PS(51.24,""D"",""MILI U"",23,4)":
        PSSADUK3 = 1
        return
    if not "^PS(51.24,""D"",""MILI UNIT"",23,5)":
        PSSADUK3 = 1
        return
    if not "^PS(51.24,""D"",""MILI UNITS"",23,6)":
        PSSADUK3 = 1
        return
    if not "^PS(51.24,""D"",""MILLION UNIT"",23,8)":
        PSSADUK3 = 1
        return
    if not "^PS(51.24,""D"",""MILLION UNITS"",23,9)":
        PSSADUK3 = 1
        return
    if not "^PS(51.24,""D"",""MILLION UNT"",23,7)":
        PSSADUK3 = 1
        return
    if not "^PS(51.24,""D"",""MILU"",23,3)":
        PSSADUK3 = 1
        return
    if not "^PS(51.24,""D"",""MIU"",23,2)":
        PSSADUK3 = 1
        return
    if not "^PS(51.24,""D"",""MU"",23,1)":
        PSSADUK3 = 1
        return

#SETWS ;define DOSING_INFO web service
def SETWS():
    PSSWSERV = None
    PSSWSER2 = None
    PSSWPEPS = None
    PSSWSCNT = None
    PSSWSMSG = None
    PSSWSSTA = None
    PSSWSERR = None
    DA = None
    DIE = None
    DIC = None
    DR = None
    X = None
    Y = None
    DLAYGO = None
    PSSWSCNT = 0
    DIC = "^XOB(18.12,"
    X = "PEPS"
    DIC(0) = "X"
    DIC(0) = "X"
    DIC(0) = "X"
    DIC(0) = "X"
    Y = None
    PSSWPEPS = +Y
    print("Beginning DOSING_INFO Web Service definition for PEPS web server: ")
    if PSSWPEPS == -1:
        print("PEPS Web Server is not defined. Please contact product support.")
        PSSWSERR = 1
        "^TMP($J,""PSSMLMSG"",PSSMXUA2)" = "PEPS Web Server isn't defined and DOSING_INFO Web Service couldn't be"
        PSSMXUA2 = PSSMXUA2 + 1
        "^TMP($J,""PSSMLMSG"",PSSMXUA2)" = "created.  Please log a Remedy Ticket and refer to this message."
        PSSMXUA2 = PSSMXUA2 + 1
        LINE()

    "^XOB(18.02,"
    X = "DOSING_INFO"
    DIC(0) = "X"
    DIC(0) = "X"
    DIC(0) = "X"
    DIC(0) = "X"
    Y = None
    PSSWSERV = +Y
    L +^XOB(18.12,PSSWPEPS):20
    if not T:
        print("Unable to lock file 18.12 to enable DOSING_INFO web service. Please ")
        print("contact product support.")
        "^TMP($J,""PSSMLMSG"",PSSMXUA2)" = "Unable to lock file 18.12 to enable DOSING_INFO web service."
        PSSMXUA2 = PSSMXUA2 + 1
        "^TMP($J,""PSSMLMSG"",PSSMXUA2)" = "Please log a Remedy Ticket and refer to this message."
        PSSMXUA2 = PSSMXUA2 + 1
        PSSWSERR = 1

    if PSSWSER2 == -1:
        PSSENABL()
        return

    PSSWSSTA = GET1^DIQ(18.121,PSSWSER2_",1",".06","I")
    PSSENAB2()
    return

#PSSENABL ;
def PSSENABL():
    DIC = "^XOB(18.12,"_PSSWPEPS_",100,"
    DLAYGO = 18.121
    DIC(0) = "L"
    DA(1) = PSSWPEPS
    X = "DOSING_INFO"
    "^XOB(18.12,"_PSSWPEPS_",100)" = ""
    PSSENAB2()
    return

#PSSENAB2 ;
def PSSENAB2():
    DIE = "^XOB(18.12,"_PSSWPEPS_",100,"
    DR = ".06///ENABLE"
    DA(1) = PSSWPEPS
    DA = PSSWSER2
    "^XOB(18.12,"_PSSWPEPS_",100,"_PSSWSER2_",1)" = ""
    PSSWSSTA = GET1^DIQ(18.121,PSSWSER2_",1",".06","I")
    if PSSWSSTA:
        print("DOSING_INFO web service has been enabled.")
    return

#LINE ;
def LINE():
    "^TMP($J,""PSSMLMSG"",PSSMXUA2)" = " "
    PSSMXUA2 = PSSMXUA2 + 1
    return

#ADDMIL2 ;Validate synonyms and cross references for MILLIONUNIT(S)
def ADDMIL2():
    if "^PS(51.24,23,1,1,0)" != "MU":
        PSSADUK3 = 1
        return
    if "^PS(51.24,23,1,2,0)" != "MIU":
        PSSADUK3 = 1
        return
    if "^PS(51.24,23,1,3,0)" != "MILU":
        PSSADUK3 = 1
        return
    if "^PS(51.24,23,1,4,0)" != "MILI U":
        PSSADUK3 = 1
        return
    if "^PS(51.24,23,1,5,0)" != "MILI UNIT":
        PSSADUK3 = 1
        return
    if "^PS(51.24,23,1,6,0)" != "MILI UNITS":
        PSSADUK3 = 1
        return
    if "^PS(51.24,23,1,7,0)" != "MILLION UNT":
        PSSADUK3 = 1
        return
    if "^PS(51.24,23,1,8,0)" != "MILLION UNIT":
        PSSADUK3 = 1
        return
    if "^PS(51.24,23,1,9,0)" != "MILLION UNITS":
        PSSADUK3 = 1
        return
    if not "^PS(51.24,23,1,""B"",""MILI U"",4)":
        PSSADUK3 = 1
        return
    if not "^PS(51.24,23,1,""B"",""MILI UNIT"",5)":
        PSSADUK3 = 1
        return
    if not "^PS(51.24,23,1,""B"",""MILI UNITS"",6)":
        PSSADUK3 = 1
        return
    if not "^PS(51.24,23,1,""B"",""MILLION UNIT"",8)":
        PSSADUK3 = 1
        return
    if not "^PS(51.24,23,1,""B"",""MILLION UNITS"",9)":
        PSSADUK3 = 1
        return
    if not "^PS(51.24,23,1,""B"",""MILLION UNT"",7)":
        PSSADUK3 = 1
        return
    if not "^PS(51.24,23,1,""B"",""MILU"",3)":
        PSSADUK3 = 1
        return
    if not "^PS(51.24,23,1,""B"",""MIU"",2)":
        PSSADUK3 = 1
        return
    if not "^PS(51.24,23,1,""B"",""MU"",1)":
        PSSADUK3 = 1
        return
    if not "^PS(51.24,""B"",""MILLIONUNIT(S)"",23)":
        PSSADUK3 = 1
        return
    if not "^PS(51.24,""C"",""MILLIONUNIT(S)"",23)":
        PSSADUK3 = 1
        return 
    if not "^PS(51.24,""D"",""MILI U"",23,4)":
        PSSADUK3 = 1
        return
    if not "^PS(51.24,""D"",""MILI UNIT"",23,5)":
        PSSADUK3 = 1
        return
    if not "^PS(51.24,""D"",""MILI UNITS"",23,6)":
        PSSADUK3 = 1
        return
    if not "^PS(51.24,""D"",""MILLION UNIT"",23,8)":
        PSSADUK3 = 1
        return
    if not "^PS(51.24,""D"",""MILLION UNITS"",23,9)":
        PSSADUK3 = 1
        return
    if not "^PS(51.24,""D"",""MILLION UNT"",23,7)":
        PSSADUK3 = 1
        return
    if not "^PS(51.24,""D"",""MILU"",23,3)":
        PSSADUK3 = 1
        return
    if not "^PS(51.24,""D"",""MIU"",23,2)":
        PSSADUK3 = 1
        return
    if not "^PS(51.24,""D"",""MU"",23,1)":
        PSSADUK3 = 1
        return

#SETWS ;define DOSING_INFO web service
def SETWS():
    PSSWSERV = None
    PSSWSER2 = None
    PSSWPEPS = None
    PSSWSCNT = None
    PSSWSMSG = None
    PSSWSSTA = None
    PSSWSERR = None
    DA = None
    DIE = None
    DIC = None
    DR = None
    X = None
    Y = None
    DLAYGO = None
    PSSWSCNT = 0
    DIC = "^XOB(18.12,"
    X = "PEPS"
    DIC(0) = "X"
    DIC(0) = "X"
    DIC(0) = "X"
    DIC(0) = "X"
    Y = None
    PSSWPEPS = +Y
    print("Beginning DOSING_INFO Web Service definition for PEPS web server: ")
    if PSSWPEPS == -1:
        print("PEPS Web Server is not defined. Please contact product support.")
        PSSWSERR = 1
        "^TMP($J,""PSSMLMSG"",PSSMXUA2)" = "PEPS Web Server isn't defined and DOSING_INFO Web Service couldn't be"
        PSSMXUA2 = PSSMXUA2 + 1
        "^TMP($J,""PSSMLMSG"",PSSMXUA2)" = "created.  Please log a Remedy Ticket and refer to this message."
        PSSMXUA2 = PSSMXUA2 + 1
        LINE()

    "^XOB(18.02,"
    X = "DOSING_INFO"
    DIC(0) = "X"
    DIC(0) = "X"
    DIC(0) = "X"
    DIC(0) = "X"
    Y = None
    PSSWSERV = +Y
    L +^XOB(18.12,PSSWPEPS):20
    if not T:
        print("Unable to lock file 18.12 to enable DOSING_INFO web service. Please ")
        print("contact product support.")
        "^TMP($J,""PSSMLMSG"",PSSMXUA2)" = "Unable to lock file 18.12 to enable DOSING_INFO web service."
        PSSMXUA2 = PSSMXUA2 + 1
        "^TMP($J,""PSSMLMSG"",PSSMXUA2)" = "Please log a Remedy Ticket and refer to this message."
        PSSMXUA2 = PSSMXUA2 + 1
        PSSWSERR = 1

    if PSSWSER2 == -1:
        PSSENABL()
        return

    PSSWSSTA = GET1^DIQ(18.121,PSSWSER2_",1",".06","I")
    PSSENAB2()
    return

#PSSENABL ;
def PSSENABL():
    DIC = "^XOB(18.12,"_PSSWPEPS_",100,"
    DLAYGO = 18.121
    DIC(0) = "L"
    DA(1) = PSSWPEPS
    X = "DOSING_INFO"
    "^XOB(18.12,"_PSSWPEPS_",100)" = ""
    PSSENAB2()
    return

#PSSENAB2 ;
def PSSENAB2():
    DIE = "^XOB(18.12,"_PSSWPEPS_",100,"
    DR = ".06///ENABLE"
    DA(1) = PSSWPEPS
    DA = PSSWSER2
    "^XOB(18.12,"_PSSWPEPS_",100,"_PSSWSER2_",1)" = ""
    PSSWSSTA = GET1^DIQ(18.121,PSSWSER2_",1",".06","I")
    if PSSWSSTA:
        print("DOSING_INFO web service has been enabled.")
    return

#LINE ;
def LINE():
    "^TMP