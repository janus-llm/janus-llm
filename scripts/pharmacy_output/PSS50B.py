def PSS50B(PSSIEN, PSSFT, PSSFL, PSSPK, PSSRTOI, LIST):
    import os
    # PSSIEN - IEN of entry in 50
    # PSSFT - Free Text name in 50
    # PSSFL - Inactive flag - "" - All entries
    #                        FileMan Date - Only entries with no Inactive Date or an Inactive Date greater than this date.
    # PSSPK - Application Package's Use - "" - All entries
    #                                         Alphabetic codes that represent the DHCP packages that consider this drug to be
    #                                         part of their formulary.
    # PSSRTOI - Orderable Item - return only entries matched to a Pharmacy Orderable Item
    # LIST - Subscript of ^TMP array in the form ^TMP($J,LIST,Field Number where Field Number is the Field Number of the data
    #        piece being returned.
    import DIERR
    import ZZERR
    import SCR
    import PSS
    import PSSMLCT
    import PSSP50

    if not LIST:
        return

    os.system("K ^TMP($J,LIST)")
    if (PSSIEN is None or PSSIEN <= 0) and (not PSSFT):
        os.system("S ^TMP($J,LIST,0)=-1_"^"_"NO DATA FOUND")
        return

    SCR["S"] = ""

    if (PSSFL > 0 or PSSPK or PSSRTOI == 1):
        PSS5ND = None
        PSSZ3 = None
        PSSZ4 = None
        os.system("SETSCRN^PSS50A")

    if PSSIEN:
        PSSIEN2 = os.system("FIND1^DIC(50,\"\",\"A\",\"`\"_PSSIEN,,SCR(\"S\"),\"\")")
        os.system("K ^TMP(\"PSSP50\",$J)")
        if PSSIEN2 <= 0:
            os.system("S ^TMP($J,LIST,0)=-1_"^"_"NO DATA FOUND")
        else:
            os.system("S ^TMP($J,LIST,0)=1")
            os.system("SETSUB1^PSS50AQM(+PSSIEN2),SETSUB4^PSS50AQM(+PSSIEN2)")
            os.system("K ^TMP(\"PSSP50\",$J)")
            os.system("GETS^DIQ(50,+PSSIEN2,\".01;9*;11:17.1;50;441*\",\"IE\",\"^TMP(\"\"PSSP50\"\",$J)\")")
            PSS[1] = 0
            while PSS[1]:
                os.system("SETINV^PSS50ATC")
                PSS[2] = 0
                PSSMLCT = 0
                while PSS[2]:
                    PSSMLCT += 1
                    os.system("SETSYN2^PSS50ATC")
                os.system("S ^TMP($J,LIST,+PSS(1),\"SYN\",0)=$S($G(PSSMLCT):PSSMLCT,1:\"-1^NO DATA FOUND\")")
                PSS[2] = 0
                PSSMLCT = 0
                while PSS[2]:
                    PSSMLCT += 1
                    os.system("SETIFC^PSS50ATC")
                os.system("S ^TMP($J,LIST,+PSS(1),\"IFC\",0)=$S($G(PSSMLCT):PSSMLCT,1:\"-1^NO DATA FOUND\")")
        os.system("K ^TMP(\"PSSP50\",$J)")
        return

    if PSSIEN:
        os.system("S ^TMP($J,LIST,0)=-1_"^"_"NO DATA FOUND")
        return

    if PSSFT:
        if PSSFT.find("??") != -1:
            os.system("LOOP^PSS50B1")
            return
        os.system("K ^TMP(\"DILIST\",$J)")
        os.system("FIND^DIC(50,,\"@;.01\",\"QP\",PSSFT,,\"B\",SCR(\"S\"),,\"\")")
        if os.system("+$G(^TMP(\"DILIST\",$J,0))=0"):
            os.system("S ^TMP($J,LIST,0)=-1_"^"_"NO DATA FOUND")
            return
        if os.system("+^TMP(\"DILIST\",$J,0)>0"):
            os.system("S ^TMP($J,LIST,0)=+^TMP(\"DILIST\",$J,0)")
            os.system("S PSSXX=0")
            PSSXX = 0
            while PSSXX:
                PSSIEN = os.system("+^TMP(\"DILIST\",$J,PSSXX,0)")
                os.system("SETSUB1^PSS50AQM(PSSIEN),SETSUB4^PSS50AQM(PSSIEN)")
                os.system("K ^TMP(\"PSSP50\",$J)")
                os.system("GETS^DIQ(50,+PSSIEN,\".01;9*;11:17.1;50;441*\",\"IE\",\"^TMP(\"\"PSSP50\"\",$J)\")")
                PSS[1] = 0
                while PSS[1]:
                    os.system("SETINV^PSS50ATC")
                    PSS[2] = 0
                    PSSMLCT = 0
                    while PSS[2]:
                        PSSMLCT += 1
                        os.system("SETSYN2^PSS50ATC")
                    os.system("S ^TMP($J,LIST,+PSS(1),\"SYN\",0)=$S($G(PSSMLCT):PSSMLCT,1:\"-1^NO DATA FOUND\")")
                    PSS[2] = 0
                    PSSMLCT = 0
                    while PSS[2]:
                        PSSMLCT += 1
                        os.system("SETIFC^PSS50ATC")
                    os.system("S ^TMP($J,LIST,+PSS(1),\"IFC\",0)=$S($G(PSSMLCT):PSSMLCT,1:\"-1^NO DATA FOUND\")")
                PSSXX = 0
        os.system("K ^TMP(\"DILIST\",$J),^TMP(\"PSSP50\",$J)")
        return

def NDF(PSSIEN, PSSFT, PSSFL, PSSPK, PSSRTOI, LIST):
    import os
    # PSSIEN - IEN of entry in 50
    # PSSFT - Free Text name in 50
    # PSSFL - Inactive flag - "" - All entries
    #                        FileMan Date - Only entries with no Inactive Date or an Inactive Date greater than this date.
    # PSSPK - Application Package's Use - "" - All entries
    #                                         Alphabetic codes that represent the DHCP packages that consider this drug to be
    #                                         part of their formulary.
    # PSSRTOI - Orderable Item - return only entries matched to a Pharmacy Orderable Item
    # LIST - Subscript of ^TMP array in the form ^TMP($J,LIST,Field Number where Field Number is the Field Number of the data
    #        piece being returned.
    import DIERR
    import ZZERR
    import PSSP50
    import SCR
    import PSS
    import PSSMLCT

    if not LIST:
        return

    os.system("K ^TMP($J,LIST)")
    if (PSSIEN is None or PSSIEN <= 0) and (not PSSFT):
        os.system("S ^TMP($J,LIST,0)=-1_"^"_"NO DATA FOUND")
        return

    SCR["S"] = ""

    if (PSSFL > 0 or PSSPK or PSSRTOI == 1):
        PSS5ND = None
        PSSZ3 = None
        PSSZ4 = None
        os.system("SETSCRN^PSS50A")

    if PSSIEN:
        PSSIEN2 = os.system("FIND1^DIC(50,\"\",\"A\",\"`\"_PSSIEN,,SCR(\"S\"),\"\")")
        os.system("K ^TMP(\"PSSP50\",$J)")
        if PSSIEN2 <= 0:
            os.system("S ^TMP($J,LIST,0)=-1_"^"_"NO DATA FOUND")
        else:
            os.system("S ^TMP($J,LIST,0)=1")
            os.system("K ^TMP(\"PSSP50\",$J)")
            os.system("GETS^DIQ(50,+PSSIEN2,\".01;20:25;27;29\",\"IE\",\"^TMP(\"\"PSSP50\"\",$J)\")")
            PSS[1] = 0
            while PSS[1]:
                os.system("SETND^PSS50NDF")
        os.system("K ^TMP(\"PSSP50\",$J)")
        return

    if PSSIEN:
        os.system("S ^TMP($J,LIST,0)=-1_"^"_"NO DATA FOUND")
        return

    if PSSFT:
        if PSSFT.find("??") != -1:
            os.system("LOOP^PSS50NDF")
            return
        os.system("K ^TMP(\"DILIST\",$J)")
        os.system("FIND^DIC(50,,\"@;.01\",\"QP\",PSSFT,,\"B\",SCR(\"S\"),,\"\")")
        if os.system("+$G(^TMP(\"DILIST\",$J,0))=0"):
            os.system("S ^TMP($J,LIST,0)=-1_"^"_"NO DATA FOUND")
            return
        if os.system("+^TMP(\"DILIST\",$J,0)>0"):
            os.system("S ^TMP($J,LIST,0)=+^TMP(\"DILIST\",$J,0)")
            os.system("S PSSXX=0")
            PSSXX = 0
            while PSSXX:
                PSSIEN = os.system("+^TMP(\"DILIST\",$J,PSSXX,0)")
                os.system("K ^TMP(\"PSSP50\",$J)")
                os.system("GETS^DIQ(50,+PSSIEN,\".01;20:25;27;29\",\"IE\",\"^TMP(\"\"PSSP50\"\",$J)\")")
                PSS[1] = 0
                while PSS[1]:
                    os.system("SETND^PSS50NDF")
                PSSXX = 0
        os.system("K ^TMP(\"DILIST\",$J),^TMP(\"PSSP50\",$J)")
        return

def DOSE(PSSIEN, PSSFT, PSSFL, PSSPK, PSSRTOI, LIST):
    import os
    # PSSIEN - IEN of entry in 50
    # PSSFT - Free Text name in 50
    # PSSFL - Inactive flag - "" - All entries
    #                        FileMan Date - Only entries with no Inactive Date or an Inactive Date greater than this date.
    # PSSPK - Application Package's Use - "" - All entries
    #                                         Alphabetic codes that represent the DHCP packages that consider this drug to be
    #                                         part of their formulary.
    # PSSRTOI - Orderable Item - return only entries matched to a Pharmacy Orderable Item
    # LIST - Subscript of ^TMP array in the form ^TMP($J,LIST,Field Number where Field Number is the Field Number of the data
    #        piece being returned.
    import DIERR
    import ZZERR
    import PSSP50
    import SCR
    import PSSMLCT
    import PSS

    if not LIST:
        return

    os.system("K ^TMP($J,LIST)")
    if (PSSIEN is None or PSSIEN <= 0) and (not PSSFT):
        os.system("S ^TMP($J,LIST,0)=-1_"^"_"NO DATA FOUND")
        return

    SCR["S"] = ""

    if (PSSFL > 0 or PSSPK or PSSRTOI == 1):
        PSS5ND = None
        PSSZ3 = None
        PSSZ4 = None
        os.system("SETSCRN^PSS50A")

    if PSSIEN:
        PSSIEN2 = os.system("FIND1^DIC(50,\"\",\"A\",\"`\"_PSSIEN,,SCR(\"S\"),\"\")")
        os.system("K ^TMP(\"PSSP50\",$J)")
        if PSSIEN2 <= 0:
            os.system("S ^TMP($J,LIST,0)=-1_"^"_"NO DATA FOUND")
        else:
            os.system("S ^TMP($J,LIST,0)=1")
            os.system("SETSUB7^PSS50AQM(+PSSIEN2),SETSUB8^PSS50AQM(+PSSIEN2)")
            os.system("K ^TMP(\"PSSP50\",$J)")
            os.system("GETS^DIQ(50,+PSSIEN2,\".01;901;902;903*;904*\",\"IE\",\"^TMP(\"\"PSSP50\"\",$J)\")")
            PSS[1] = 0
            while PSS[1]:
                os.system("SDOSE^PSS50DOS")
                PSS[2] = 0
                PSSMLCT = 0
                while PSS[2]:
                    PSSMLCT += 1
                    os.system("SDOSE2^PSS50DOS")
                os.system("S ^TMP($J,LIST,+PSS(1),\"POS\",0)=$S($G(PSSMLCT):PSSMLCT,1:\"-1^NO DATA FOUND\")")
                PSS[2] = 0
                PSSMLCT = 0
                while PSS[2]:
                    PSSMLCT += 1
                    os.system("SDOSE3^PSS50DOS")
                os.system("S ^TMP($J,LIST,+PSS(1),\"LOC\",0)=$S($G(PSSMLCT):PSSMLCT,1:\"-1^NO DATA FOUND\")")
        os.system("K ^TMP(\"PSSP50\",$J)")
        return

    if PSSIEN:
        os.system("S ^TMP($J,LIST,0)=-1_"^"_"NO DATA FOUND")
        return

    if PSSFT:
        if PSSFT.find("??") != -1:
            os.system("LOOP^PSS50DOS")
            return
        os.system("K ^TMP(\"DILIST\",$J)")
        os.system("FIND^DIC(50,,\"@;.01\",\"QP\",PSSFT,,\"B\",SCR(\"S\"),,\"\")")
        if os.system("+$G(^TMP(\"DILIST\",$J,0))=0"):
            os.system("S ^TMP($J,LIST,0)=-1_"^"_"NO DATA FOUND")
            return
        if os.system("+^TMP(\"DILIST\",$J,0)>0"):
            os.system("S ^TMP($J,LIST,0)=+^TMP(\"DILIST\",$J,0)")
            os.system("S PSSXX=0")
            PSSXX = 0
            while PSSXX:
                PSSIEN = os.system("+^TMP(\"DILIST\",$J,PSSXX,0)")
                os.system("K ^TMP(\"PSSP50\",$J)")
                os.system("GETS^DIQ(50,+PSSIEN,\".01;901;902;903*;904*\",\"IE\",\"^TMP(\"\"PSSP50\"\",$J)\")")
                PSS[1] = 0
                while PSS[1]:
                    os.system("SDOSE^PSS50DOS")
                    PSS[2] = 0
                    PSSMLCT = 0
                    while PSS[2]:
                        PSSMLCT += 1
                        os.system("SDOSE2^PSS50DOS")
                    os.system("S ^TMP($J,LIST,+PSS(1),\"POS\",0)=$S($G(PSSMLCT):PSSMLCT,1:\"-1^NO DATA FOUND\")")
                    PSS[2] = 0
                    PSSMLCT = 0
                    while PSS[2]:
                        PSSMLCT += 1
                        os.system("SDOSE3^PSS50DOS")
                    os.system("S ^TMP($J,LIST,+PSS(1),\"LOC\",0)=$S($G(PSSMLCT):PSSMLCT,1:\"-1^NO DATA FOUND\")")
                PSSXX = 0
        os.system("K ^TMP(\"DILIST\",$J),^TMP(\"PSSP50\",$J)")
        return