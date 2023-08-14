def PSPA():
    import datetime
    import os
    GLOBAL = os.popen("DID 55 GLOBAL NAME").read().strip()
    # Don't leave any old stuff around.
    os.system("K ^PXRMINDX(55),^PXRMINDX('55NVA')")
    ENTRIES = int(os.popen("D Q").read().split("^")[3])
    TENP = ENTRIES // 10
    TENP = int(str(TENP).split(".")[0])
    if TENP < 1:
        TENP = 1
    print("Building indexes for PHARMACY PATIENT FILE")
    print("There are", ENTRIES, "entries to process.")
    START = datetime.datetime.now()
    DFN, IND, NE, NERROR = 0, 0, 0, 0
    while True:
        DFN = int(os.popen("D ^PS(55) Q").read().split("^")[3])
        if DFN == 0:
            break
        IND += 1
        if IND % TENP == 0:
            print("Processing entry", IND)
        if IND % 10000 == 0:
            print(".")
        # Process Unit Dose.
        DA = 0
        while True:
            DA = int(
                os.popen(
                    "D ^PS(55,DFN,5) Q"
                ).read().split("^")[3]
            )
            if DA == 0:
                break
            TEMP = os.popen(
                "G ^PS(55,DFN,5,DA,2) Q"
            ).read()
            STARTD = TEMP.split("^")[2]
            if STARTD == "":
                IDEN = "DFN=" + str(DFN) + " D1=" + str(DA) + " Unit Dose missing start date"
                print("ADDERROR", GLOBAL, IDEN, NERROR)
                continue
            SDATE = TEMP.split("^")[4]
            if SDATE == 1:
                continue
            if SDATE == "":
                IDEN = "DFN=" + str(DFN) + " D1=" + str(DA) + " Unit Dose missing stop date"
                print("ADDERROR", GLOBAL, IDEN, NERROR)
                continue
            DA1 = 0
            while True:
                DA1 = int(
                    os.popen(
                        "D ^PS(55,DFN,5,DA,1) Q"
                    ).read().split("^")[3]
                )
                if DA1 == 0:
                    break
                DRUG = os.popen(
                    "G ^PS(55,DFN,5,DA,1,DA1,0) S DRUG=$P(^(0),U,1) Q"
                ).read().strip()
                if DRUG == "":
                    IDEN = "DFN=" + str(DFN) + " D1=" + str(DA) + " D2=" + str(DA1) + " Unit Dose missing drug"
                    print("ADDERROR", GLOBAL, IDEN, NERROR)
                    continue
                DAS = str(DFN) + ";5;" + str(DA) + ";1;" + str(DA1) + ";0"
                os.popen(
                    "S ^PXRMINDX(55,'IP',DRUG,DFN,STARTD,SDATE,DAS)='' Q"
                ).read()
                os.popen(
                    "S ^PXRMINDX(55,'PI',DFN,DRUG,STARTD,SDATE,DAS)='' Q"
                ).read()
                NE += 1
        # Process the IV multiple.
        DA = 0
        while True:
            DA = int(
                os.popen(
                    "D ^PS(55,DFN,'IV') Q"
                ).read().split("^")[3]
            )
            if DA == 0:
                break
            TEMP = os.popen(
                "G ^PS(55,DFN,'IV',DA,0) Q"
            ).read()
            STARTD = TEMP.split("^")[2]
            if STARTD == "":
                IDEN = "DFN=" + str(DFN) + " D1=" + str(DA) + " IV missing start date"
                print("ADDERROR", GLOBAL, IDEN, NERROR)
                continue
            SDATE = TEMP.split("^")[3]
            if SDATE == 1:
                continue
            if SDATE == "":
                IDEN = "DFN=" + str(DFN) + " D1=" + str(DA) + " IV missing stop date"
                print("ADDERROR", GLOBAL, IDEN, NERROR)
                continue
            # Process Additives
            DA1 = 0
            while True:
                DA1 = int(
                    os.popen(
                        "D ^PS(55,DFN,'IV',DA,'AD') Q"
                    ).read().split("^")[3]
                )
                if DA1 == 0:
                    break
                ADD = os.popen(
                    "G ^PS(55,DFN,'IV',DA,'AD',DA1,0) S ADD=$P(^(0),U,1) Q"
                ).read().strip()
                if ADD == "":
                    IDEN = "DFN=" + str(DFN) + " D1=" + str(DA) + " D2=" + str(DA1) + " IV missing additive"
                    print("ADDERROR", GLOBAL, IDEN, NERROR)
                    continue
                DRUG = os.popen(
                    "S DRUG=$P(^PS(52.6,ADD,0),U,2) Q"
                ).read().strip()
                if DRUG == "":
                    IDEN = "DFN=" + str(DFN) + " D1=" + str(DA) + " D2=" + str(DA1) + " IV additive missing drug"
                    print("ADDERROR", GLOBAL, IDEN, NERROR)
                    continue
                NE += 1
                DAS = str(DFN) + ";IV;" + str(DA) + ";AD;" + str(DA1) + ";0"
                os.popen(
                    "S ^PXRMINDX(55,'IP',DRUG,DFN,STARTD,SDATE,DAS)='' Q"
                ).read()
                os.popen(
                    "S ^PXRMINDX(55,'PI',DFN,DRUG,STARTD,SDATE,DAS)='' Q"
                ).read()
            # Process Solutions
            DA1 = 0
            while True:
                DA1 = int(
                    os.popen(
                        "D ^PS(55,DFN,'IV',DA,'SOL') Q"
                    ).read().split("^")[3]
                )
                if DA1 == 0:
                    break
                SOL = os.popen(
                    "G ^PS(55,DFN,'IV',DA,'SOL',DA1,0) S SOL=$P(^(0),U,1) Q"
                ).read().strip()
                if SOL == "":
                    IDEN = "DFN=" + str(DFN) + " D1=" + str(DA) + " D2=" + str(DA1) + " IV-SOL missing solution"
                    print("ADDERROR", GLOBAL, IDEN, NERROR)
                    continue
                DRUG = os.popen(
                    "S DRUG=$P(^PS(52.7,SOL,0),U,2) Q"
                ).read().strip()
                if DRUG == "":
                    IDEN = "DFN=" + str(DFN) + " D1=" + str(DA) + " D2=" + str(DA1) + " IV-SOL missing Drug"
                    print("ADDERROR", GLOBAL, IDEN, NERROR)
                    continue
                NE += 1
                DAS = str(DFN) + ";IV;" + str(DA) + ";SOL;" + str(DA1) + ";0"
                os.popen(
                    "S ^PXRMINDX(55,'IP',DRUG,DFN,STARTD,SDATE,DAS)='' Q"
                ).read()
                os.popen(
                    "S ^PXRMINDX(55,'PI',DFN,DRUG,STARTD,SDATE,DAS)='' Q"
                ).read()
        # Process the NVA multiple.
        DA = 0
        while True:
            DA = int(
                os.popen(
                    "D ^PS(55,DFN,'NVA') Q"
                ).read().split("^")[3]
            )
            if DA == 0:
                break
            TEMP = os.popen(
                "G ^PS(55,DFN,'NVA',DA,0) Q"
            ).read()
            STARTD = TEMP.split("^")[9]
            if STARTD == "":
                STARTD = TEMP.split("^")[10]
            if STARTD == "":
                IDEN = "DFN=" + str(DFN) + " D1=" + str(DA) + " NVA missing start date"
                print("ADDERROR", GLOBAL, IDEN, NERROR)
                continue
            SDATE = TEMP.split("^")[7]
            if SDATE == "":
                SDATE = "U" + str(DFN)
            DAS = str(DFN) + ";NVA;" + str(DA) + ";0"
            POI = TEMP.split("^")[1]
            os.popen(
                "S ^PXRMINDX('55NVA','IP',POI,DFN,STARTD,SDATE,DAS)='' Q"
            ).read()
            os.popen(
                "S ^PXRMINDX('55NVA','PI',DFN,POI,STARTD,SDATE,DAS)='' Q"
            ).read()
    END = datetime.datetime.now()
    TEXT = str(NE) + " PHARMACY PATIENTS results indexed."
    print(TEXT)
    TEXT = str(NERROR) + " errors were encountered."
    print(TEXT)
    print("Time elapsed:", str(END - START))
    # If there were errors send a message.
    if NERROR > 0:
        ERRMSG(NERROR, GLOBAL)
    # Send a MailMan message with the results.
    COMMSG(GLOBAL, START, END, NE, NERROR)
    os.system("S ^PXRMINDX(55,'GLOBAL NAME')=$$GET1^DID(55,'','','GLOBAL NAME')")
    os.system("S ^PXRMINDX(55,'BUILT BY')=DUZ")
    os.system("S ^PXRMINDX(55,'DATE BUILT')=$$NOW^XLFDT")
    os.system("S ^PXRMINDX('55NVA','GLOBAL NAME')=^PXRMINDX(55,'GLOBAL NAME')")
    os.system("S ^PXRMINDX('55NVA','BUILT BY')=^PXRMINDX(55,'BUILT BY')")
    os.system("S ^PXRMINDX('55NVA','DATE BUILT')=^PXRMINDX(55,'DATE BUILT')")
    return