# PSSP110 ; Post init routine for patch PSS*1*110 03/30/2006 4:57P
# ;;1.0;PHARMACY DATA MANAGEMENT;**110**;9/30/97

def EN():
    # Convert the NAME field in files #51 & 51.1 to all CAPS
    import os
    import filecmp
    import shutil
    import tempfile
    import difflib
    import subprocess
    import datetime

    DD = None
    D0 = None
    DA = None
    DIE = None
    DR = None
    PSSI = None
    PSSJ = None
    PSSCNT = None
    PSSTXT = None
    PSSLN = None
    PSSAST = None
    XMDUZ = None
    XMSUB = None
    XMTEXT = None
    XMY = None
    DIFROM = None
    PSSFLG = None
    
    if os.environ.get("U") is None:
        os.environ["U"] = "^"
    
    XMDUZ = "PSS*1*110 Post Init"
    XMY = {os.getuid(): ""}

    # File 51 (Medication Instruction)
    DIE = "^PS(51,"
    CON()
    XMSUB = "File #51 modified records"
    MSG1()

    # File 51.1 (Administration Schedule)
    DIE = "^PS(51.1,"
    CON()
    XMSUB = "File #51.1 modified records"
    MSG1()

    # File 51.2 (Medication Routes)
    #XMSUB = "File #51.2 'to be' modified records"
    #COM()

    ENQ()

def CON():
    # Convert ONLY lowercase alphabet to uppercase.  All other characters
    # in the NAME field are left alone.
    global DD, D0, DA, DIE, DR, PSSI, PSSJ, PSSCNT, PSSTXT, PSSLN, PSSAST, PSSFLG

    PSSI = ""
    PSSCNT = 0
    PSSLN = 2
    PSSFLG = ""

    while True:
        PSSI = next((x for x in sorted(DIE + '"B"') if x > PSSI), None)
        if PSSI is None:
            break
        if not PSSI.islower():
            continue
        PSSJ = PSSI.upper()
        PSSAST = "*"
        if not next((x for x in sorted(DIE + '"B"') if x > PSSJ), None):
            DA = next((x for x in sorted(DIE + '"B"', key=lambda y: y == PSSI) if y > 0), None)
            if DA is not None:
                DR = ".01///" + PSSJ
                #DIE ^DIE
                PSSAST = ""
            else:
                PSSFLG = "1"
            PSSCNT += 1
            PSSLN += 1
            PSSTXT[PSSLN] = PSSAST + PSSI

def COM():
    # Compile a list of all medication routes that do NOT
    # have an abbreviation and send it to DUZ.
    global DD, D0, DA, DIE, DR, PSSI, PSSJ, PSSCNT, PSSLN, PSSTXT

    PSSI = ""
    PSSCNT = 0
    PSSLN = 2

    while True:
        PSSI = next((x for x in sorted(DIE) if x > PSSI), None)
        if PSSI is None:
            break
        if PSSI:
            PSSJ = DIE[PSSI]
            if not PSSJ[2]:
                PSSCNT += 1
                PSSLN += 1
                PSSTXT[PSSLN] = PSSJ[0]

    if PSSCNT < 1:
        PSSTXT[1] = "All medication routes have abbreviations!"
        SEND()

    PSSTXT[1] = "The following medication route/s does/do not"
    PSSTXT[2] = "have a corresponding abbreviation:"
    SEND()

def MSG1():
    # Send message to user DUZ for files 51 & 51.1
    global DD, D0, DA, DIE, DR, PSSI, PSSJ, PSSCNT, PSSLN, PSSTXT, XMDUZ, XMY, XMTEXT

    if PSSCNT < 1:
        PSSTXT[1] = "No NAME conversion was neccessary!"
        SEND()

    PSSTXT[1] = "The following NAME/s was/were converted"
    PSSTXT[2] = "from lowercase to uppercase:"
    if PSSFLG == "1":
        PSSLN += 1
        PSSTXT[PSSLN] = "Record/s marked with an '*' was/were skipped."
        PSSLN += 1
        PSSTXT[PSSLN] = "Conversion to uppercase would have created a"
        PSSLN += 1
        PSSTXT[PSSLN] = "duplicate NAME.  Please check!!"
    SEND()

def SEND():
    global DD, D0, DA, DIE, DR, PSSI, PSSJ, PSSCNT, PSSLN, PSSTXT, XMTEXT, XMDUZ, XMY

    XMTEXT = "PSSTXT("
    XMDUZ = "PSS*1*110 Post Init"
    XMY = {os.getuid(): ""}
    # ^XMD

def ENQ():
    pass

EN()