def ALL(PSSIEN, PSSFT, LIST):
    # PSSIEN - IEN of entry in 9009032.5.
    # PSSFT - Free Text TYPE in 9009032.5.
    # LIST - Subscript of ^TMP array in the form ^TMP($J,LIST,Field Number where Field Number is the
    # Field Number of the data piece being returned.
    # Returns RECOMMENDATION field (#.01) of APSP INTERACTION RECOMMENDATION file (#9009032.5).
    import os
    import sys

    if LIST == "":
        return

    os.system("K ^TMP($J,LIST)")

    if PSSIEN <= 0 and PSSFT == "":
        os.system("S ^TMP($J,LIST,0)=-1_"^"_"NO DATA FOUND")
        return

    if PSSIEN != "" and PSSIEN <= 0:
        os.system("S ^TMP($J,LIST,0)=-1_"^"_"NO DATA FOUND")
        return

    if PSSIEN > 0:
        PSSIEN2 = os.system("D FIND1^DIC(9009032.5,"",""A"",""`""_PSSIEN,,,"")")
        if PSSIEN2 <= 0:
            os.system("S ^TMP($J,LIST,0)=-1_"^"_"NO DATA FOUND")
            return
        os.system("S ^TMP($J,LIST,0)=1")
        os.system("D GETS^DIQ(9009032.5,+PSSIEN2,"".01"",""I"",""PSS32P5"")")
        PSS = 0
        while PSS != "":
            os.system("D SETALL")
            PSS += 1

    if PSSIEN == "" and PSSFT != "":
        if PSSFT == "?":
            os.system("D LOOP")
        os.system("D FIND^DIC(9009032.5,,""@;.01;"",""QP""," + PSSFT + ",,""B"",,,"")")
        if os.system("+^TMP(""DILIST"",$J,0)") == 0:
            os.system("S ^TMP($J,LIST,0)=-1_"^"_"NO DATA FOUND")
            return
        if os.system("+^TMP(""DILIST"",$J,0)") > 0:
            os.system("S ^TMP($J,LIST,0)=+^TMP(""DILIST"",$J,0)")
            PSSXX = 0
            while PSSXX != "":
                PSSIEN = os.system("+^TMP(""DILIST"",$J," + PSSXX + ",0)")
                os.system("K PSS32P5")
                os.system("D GETS^DIQ(9009032.5,+PSSIEN,"".01"",""I"",""PSS32P5"")")
                PSS = 0
                while PSS != "":
                    os.system("D SETALL")
                    PSS += 1

    os.system("K ^TMP(""DILIST"",$J)")


def SETALL():
    os.system("S ^TMP($J,LIST,+PSS(1),.01)=$G(PSS32P5(9009032.5,PSS(1),.01,""I""))")
    os.system("S ^TMP($J,LIST,""B"",$G(PSS32P5(9009032.5,PSS(1),.01,""I"")),+PSS(1))=""")
    return


def LOOP():
    PSSIEN = 0
    while PSSIEN != "":
        os.system("D GETS^DIQ(9009032.5,+PSSIEN,"".01"",""I"",""PSS32P5"")")
        PSS = 0
        os.system("S ^TMP($J,LIST,0)=0")
        while PSS != "":
            os.system("D SETALL")
            PSS += 1
            os.system("S ^TMP($J,LIST,0)=^TMP($J,LIST,0)+1")
        PSSIEN += 1
    return