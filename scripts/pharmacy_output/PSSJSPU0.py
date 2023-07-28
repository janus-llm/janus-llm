def PSSJSPU0():
    # BIR/CML3,WRT-SCHEDULE PROCESSOR UTILITY CONT. ; 06/24/96 9:22
    # 1.0;PHARMACY DATA MANAGEMENT;;9/30/97

    def ENDSD():
        # calculate default start date
        import datetime
        now = datetime.datetime.now()
        if PSJTS == "O" or not PSJAT or PSJSCH in ["NOW", "STAT", "ONCE", "ONE-TIME", "ONE TIME", "ON CALL"]:
            PSJX = now.strftime("%Y-%m-%d")
            if not PSJX.split(".")[1]:
                x1 = PSJX + ".24"
                x2 = -1
                PSJX = (datetime.datetime.strptime(x1, "%Y-%m-%d.%H") + datetime.timedelta(days=x2)).strftime("%Y-%m-%d")
                return
        NT = now.time().hour * 60 * 60 + now.time().minute * 60 + now.time().second
        FT = "." + PSJAT.split("-")[0]
        LT = "." + PSJAT.split("-")[-1]
        if FT == LT:
            ET = FT
            x2 = NT > FT
            if x2:
                x2 = FT + 0.24 - NT < NT - FT
            else:
                x2 = NT + 0.24 - FT < FT - NT
            SADD()
            return
        if NT > LT:
            ET = FT if FT + 0.24 - NT < NT - LT else LT
            x2 = ET == FT
            SADD()
            return
        if NT < FT:
            ET = LT if NT + 0.24 - LT < FT - NT else FT
            x2 = ET == LT
        else:
            LT = 1
            x2 = 0
            f = 1
            while True:
                FT = "." + PSJAT.split("-")[f]
                if not FT:
                    break
                TT = FT - NT
                if TT < 0:
                    TT = -TT
                if TT < LT:
                    ET = FT
                    LT = TT
                f += 1
        SADD()

    def SADD():
        x = x1 = now.strftime("%Y-%m-%d")
        if x2:
            x1 = (datetime.datetime.strptime(x, "%Y-%m-%d") + datetime.timedelta(days=x2)).strftime("%Y-%m-%d")
        PSJX = x1 + ET

    ENDSD()