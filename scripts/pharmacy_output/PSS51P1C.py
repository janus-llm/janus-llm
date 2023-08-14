def PSS51P1C():
    # BIR/LDT - API FOR INFORMATION FROM FILE 51.1
    # 5 Sep 03
    # 1.0;PHARMACY DATA MANAGEMENT;**85**;9/30/97

    def SETZRO():
        # SETZRO subroutine
        # Set values for the zero node of the TMP global
        # based on the values in the PSS51P1 global
        ^TMP($J, LIST, +PSS(1), ".01") = $G(^TMP("PSS51P1",$J,51.1,PSS(1),.01,"I"))
        ^TMP($J, LIST, "B", $G(^TMP("PSS51P1",$J,51.1,PSS(1),.01,"I")), +PSS(1)) = ""
        ^TMP($J, LIST, +PSS(1), 1) = $G(^TMP("PSS51P1",$J,51.1,PSS(1),1,"I"))
        ^TMP($J, LIST, +PSS(1), 2) = $G(^TMP("PSS51P1",$J,51.1,PSS(1),2,"I"))
        ^TMP($J, LIST, +PSS(1), 4) = $G(^TMP("PSS51P1",$J,51.1,PSS(1),4,"I"))
        ^TMP($J, LIST, +PSS(1), 5) = $S($G(^TMP("PSS51P1",$J,51.1,PSS(1),5,"I"))="":"",1:^TMP("PSS51P1",$J,51.1,PSS(1),5,"I")_"^"_^TMP("PSS51P1",$J,51.1,PSS(1),5,"E"))
        ^TMP($J, LIST, +PSS(1), 6) = $G(^TMP("PSS51P1",$J,51.1,PSS(1),6,"I"))
        ^TMP($J, LIST, +PSS(1), 2.5) = $G(^TMP("PSS51P1",$J,51.1,PSS(1),2.5,"I"))
        ^TMP($J, LIST, +PSS(1), 8) = $G(^TMP("PSS51P1",$J,51.1,PSS(1),8,"I"))
        ^TMP($J, LIST, +PSS(1), 8.1) = $G(^TMP("PSS51P1",$J,51.1,PSS(1),8.1,"I"))

    def SETWARD():
        # SETWARD subroutine
        # Set values for the WARD node of the TMP global
        # based on the values in the PSS51P1 global
        ^TMP($J, LIST, +PSSIEN, "WARD", +PSS(2), ".01") = $S($G(^TMP("PSS51P1",$J,51.11,PSS(2),.01,"I"))="":"",1:^TMP("PSS51P1",$J,51.11,PSS(2),.01,"I")_"^"_^TMP("PSS51P1",$J,51.11,PSS(2),.01,"E"))
        ^TMP($J, LIST, +PSSIEN, "WARD", +PSS(2), 1) = $G(^TMP("PSS51P1",$J,51.11,PSS(2),1,"I"))

    def SETLOC():
        # SETLOC subroutine
        # Set values for the HOSP node of the TMP global
        # based on the values in the PSS51P1 global
        ^TMP($J, LIST, +PSSIEN, "HOSP", +PSS(3), ".01") = $S($G(^TMP("PSS51P1",$J,51.17,PSS(3),.01,"I"))="":"",1:^TMP("PSS51P1",$J,51.17,PSS(3),.01,"I")_"^"_^TMP("PSS51P1",$J,51.17,PSS(3),.01,"E"))
        ^TMP($J, LIST, +PSSIEN, "HOSP", +PSS(3), 1) = $G(^TMP("PSS51P1",$J,51.17,PSS(3),1,"I"))
        ^TMP($J, LIST, +PSSIEN, "HOSP", +PSS(3), 2) = $G(^TMP("PSS51P1",$J,51.17,PSS(3),2,"I"))

    def LOOP(PSSLP):
        # LOOP subroutine
        # Loop through all the entries in file 51.1
        # and call the appropriate subroutine based on the value of PSSLP
        N CNT, CNT2, CNT3, PSSIEN
        (CNT, PSSIEN) = (0, 0)
        while PSSIEN:
            if PSSLP == 1:
                SETZRO()
                (CNT2, PSS(2)) = (0, 0)
                while PSS(2):
                    SETWARD()
                    CNT2 = CNT2 + 1
                    PSS(2) = $O(^TMP("PSS51P1",$J,51.11,PSS(2)))
                ^TMP($J, LIST, +PSSIEN, "WARD", 0) = $S(CNT2 > 0: CNT2, 1: "-1^NO DATA FOUND")
                (CNT3, PSS(3)) = (0, 0)
                while PSS(3):
                    SETLOC()
                    CNT3 = CNT3 + 1
                    PSS(3) = $O(^TMP("PSS51P1",$J,51.17,PSS(3)))
                ^TMP($J, LIST, +PSSIEN, "HOSP", 0) = $S(CNT3 > 0: CNT3, 1: "-1^NO DATA FOUND")
            elif PSSLP == 2:
                K ^TMP("PSS51P1",$J)
                D GETS^DIQ(51.1, +PSSIEN, ".01;3*", "IE", "^TMP(""PSS51P1"",$J)")
                (PSS(1), CNT) = (0, 0)
                while PSS(1):
                    ^TMP($J, LIST, +PSS(1), ".01") = $G(^TMP("PSS51P1",$J,51.1,PSS(1),.01,"I"))
                    ^TMP($J, LIST, "B", $G(^TMP("PSS51P1",$J,51.1,PSS(1),.01,"E")), +PSS(1)) = ""
                    (PSS(2), CNT) = (0, 0)
                    while PSS(2):
                        SETWARD()
                        CNT = CNT + 1
                        PSS(2) = $O(^TMP("PSS51P1",$J,51.11,PSS(2)))
                    ^TMP($J, LIST, +PSS(1), "WARD", 0) = $S(CNT > 0: CNT, 1: "-1^NO DATA FOUND")
                    PSS(1) = +PSSIEN
                    (PSS(2), CNT) = (0, 0)
                    while PSS(2):
                        SETWARD()
                        CNT = CNT + 1
                        PSS(2) = $O(^TMP("PSS51P1",$J,51.11,PSS(2)))
                    ^TMP($J, LIST, +PSS(1), "WARD", 0) = $S(CNT > 0: CNT, 1: "-1^NO DATA FOUND FOR PSSIEN2 #" + PSSIEN2)
            else:
                break
            CNT = CNT + 1
            PSSIEN = $O(^PS(51.1,PSSIEN))
        ^TMP($J, LIST, 0) = $S(CNT > 0: CNT, 1: "-1^NO DATA FOUND")
        K ^TMP("DILIST",$J), ^TMP("PSS51P1",$J)

    def GETS():
        # GETS subroutine
        # Get the values from file 51.1 and store them in the PSS51P1 global
        D GETS^DIQ(51.1, +PSSIEN, ".01;1;2;4;5;6;2.5;8;8.1;3*;7*", "IE", "^TMP(""PSS51P1"",$J)")
        PSS(1) = 0
        while PSS(1):
            SETZRO()
            PSS(1) = $O(^TMP("PSS51P1",$J,51.1,PSS(1)))
        (CNT2, PSS(2)) = (0, 0)
        while PSS(2):
            SETWARD()
            CNT2 = CNT2 + 1
            PSS(2) = $O(^TMP("PSS51P1",$J,51.11,PSS(2)))
        ^TMP($J, LIST, +PSSIEN, "WARD", 0) = $S(CNT2 > 0: CNT2, 1: "-1^NO DATA FOUND")
        (CNT3, PSS(3)) = (0, 0)
        while PSS(3):
            SETLOC()
            CNT3 = CNT3 + 1
            PSS(3) = $O(^TMP("PSS51P1",$J,51.17,PSS(3)))
        ^TMP($J, LIST, +PSSIEN, "HOSP", 0) = $S(CNT3 > 0: CNT3, 1: "-1^NO DATA FOUND")

    def FIND():
        # FIND subroutine
        # Find the entries in file 51.1 based on the PSSFT value
        D FIND^DIC(51.1, , "@;.01;1", "QP", PSSFT, , "B", , , )
        if +$G(^TMP("DILIST",$J,0)) == 0:
            ^TMP($J, LIST, 0) = "-1^NO DATA FOUND"
        elif +^TMP("DILIST",$J,0) > 0:
            ^TMP($J, LIST, 0) = +^TMP("DILIST",$J,0)
            PSSXX = 0
            while PSSXX:
                PSSIEN = +^TMP("DILIST",$J,PSSXX,0)
                K ^TMP("PSS51P1",$J)
                GETS()
                PSS(1) = 0
                while PSS(1):
                    SETZRO()
                    PSS(1) = $O(^TMP("PSS51P1",$J,51.1,PSS(1)))
                (CNT2, PSS(2)) = (0, 0)
                while PSS(2):
                    SETWARD()
                    CNT2 = CNT2 + 1
                    PSS(2) = $O(^TMP("PSS51P1",$J,51.11,PSS(2)))
                ^TMP($J, LIST, +PSSIEN, "WARD", 0) = $S(CNT2 > 0: CNT2, 1: "-1^NO DATA FOUND")
                (CNT3, PSS(3)) = (0, 0)
                while PSS(3):
                    SETLOC()
                    CNT3 = CNT3 + 1
                    PSS(3) = $O(^TMP("PSS51P1",$J,51.17,PSS(3)))
                ^TMP($J, LIST, +PSSIEN, "HOSP", 0) = $S(CNT3 > 0: CNT3, 1: "-1^NO DATA FOUND")
                PSSXX = $O(^TMP("DILIST",$J,PSSXX))
        K ^TMP("DILIST",$J), ^TMP("PSS51P1",$J)

    # ALL entry point
    if +$G(PSSIEN) > 0:
        N PSSIEN2
        S PSSIEN2 = $$FIND1^DIC(51.1, , "A", "`"_PSSIEN, , , )
        if +PSSIEN2 <= 0:
            ^TMP($J, LIST, 0) = -1_"^"_"NO DATA FOUND"
        else:
            ^TMP($J, LIST, 0) = 1
            D GETS^DIQ(51.1, +PSSIEN2, ".01;1;2;4;5;6;2.5;8;8.1;3*;7*", "IE", "^TMP(""PSS51P1"",$J)")
            PSS(1) = 0
            while PSS(1):
                SETZRO()
                PSS(1) = $O(^TMP("PSS51P1",$J,51.1,PSS(1)))
            (CNT2, PSS(2)) = (0, 0)
            while PSS(2):
                SETWARD()
                CNT2 = CNT2 + 1
                PSS(2) = $O(^TMP("PSS51P1",$J,51.11,PSS(2)))
            ^TMP($J, LIST, +PSSIEN, "WARD", 0) = $S(CNT2 > 0: CNT2, 1: "-1^NO DATA FOUND")
            (CNT3, PSS(3)) = (0, 0)
            while PSS(3):
                SETLOC()
                CNT3 = CNT3 + 1
                PSS(3) = $O(^TMP("PSS51P1",$J,51.17,PSS(3)))
            ^TMP($J, LIST, +PSSIEN, "HOSP", 0) = $S(CNT3 > 0: CNT3, 1: "-1^NO DATA FOUND")
    elif +$G(PSSIEN) <= 0, $G(PSSFT)]"":
        if PSSFT["??":
            LOOP(1)
        else:
            FIND()
    K ^TMP("DILIST",$J), ^TMP("PSS51P1",$J)