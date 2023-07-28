def PSS551(LIST, DFN=None, PO=None, PSDATE=None, PEDATE=None):
    """
    BHM/DB - API FOR PHARMACY PATIENT FILE
    15 JUN 05
    1.0;PHARMACY DATA MANAGEMENT;**108,118,133,169,173**;9/30/97;Build 9

    DFN: IEN of Patient [REQUIRED]
    PO: Order # [optional]
    PSDATE: Start Date [optional]
    PEDATE: End Date [optional]
    If a start date is sent, an end date must also be sent
    LIST: Subscript name used in ^TMP global [REQUIRED]
    """

    import os
    import tempfile

    PSSPO = None
    PSSIEN = None
    DA = None
    DR = None
    DIC = None
    PSS = None
    CNT1 = None
    X = None
    PSSTMP = None

    if LIST is None:
        return

    tmp_file = tempfile.NamedTemporaryFile(delete=False)
    tmp_file.close()

    os.makedirs(os.path.dirname(tmp_file.name), exist_ok=True)
    with open(tmp_file.name, "w") as f:
        f.write("")
    
    with open(tmp_file.name, "r") as f:
        if DFN is None:
            f.write(f"^TMP($J,{LIST},0)=-1^NO DATA FOUND")
            return

        PSSIEN = DFN
        PSSPO = PO
        f.write(f"^TMP($J,{LIST},0)=0")
        
        if PSSPO > 0 and PSSIEN > 0:
            DA = PSSIEN
            IEN = DA(55.06)
            f.write("G DIQ431")

        if PSSPO == "" and PSDATE != "" and PEDATE != "":
            PSDATE = f"{''.join(PSDATE.split('.')[:2])}.000001" if not PSDATE.split('.')[1] else PSDATE
            PEDATE = f"{''.join(PEDATE.split('.')[:2])}.999999" if not PEDATE.split('.')[1] else PEDATE
            PSS56 = None
            f.write("G DT431")

        if PSSPO == "":
            PSSPO1 = None
            PSSPO = 0
            while True:
                PSSPO1 = next((PSSPO1 for PSSPO1 in range(len(PS.PO)) if PSSPO1 == PSSPO), None)
                if PSSPO1 is None:
                    break

                PSSPO = PSSPO1
                PO = PSSPO
                f.write("G DIQ431")

    def DIQ431():
        nonlocal PSSIEN
        nonlocal PSSPO
        nonlocal DA
        nonlocal DR
        nonlocal DIC
        nonlocal PSS
        nonlocal CNT1
        nonlocal X
        nonlocal PSSTMP

        if not os.path.exists(f"^PS(55,{DFN},5,{PO},0)"):
            return

        PSSIEN = f"{PO},{DFN},"
        DIQ = None
        f.write(f"GETS^DIQ(55.06,{PSSIEN},'.01;.5;1;2*;3;4;5;6;7;10;11;12;26;27;27.1;28;34;66;109','IE','^TMP('PSS5506',$J))")

        for X in [".01", ".5", "1", "3", "4", "5", "6", "7", "10", "11", "12", "26", "27", "27.1", "28", "34", "66", "109"]:
            f.write(f"^TMP($J,{LIST},{PSSPO},{X})=^TMP('PSS5506',$J,55.06,{PSSIEN},{X},'I')")

        for X in [".5", "1", "3", "4", "5", "6", "7", "10", "27", "27.1", "28", "34"]:
            f.write(f"^TMP($J,{LIST},{PSSPO},{X})={'^TMP('PSS5506',$J,55.06,{PSSIEN},{X},'E')' if ^TMP('PSS5506',$J,55.06,{PSSIEN},{X},'E') != '' else ''}")

        PSSTMP = f"^PS(55,{DFN},5,{PO},.2)"
        f.write(f"^TMP($J,{LIST},IEN,108)={'' if PSSTMP == '' else ORDITEM^PSS55(+PSSTMP)}")

        PSS = 0
        CNT1 = 0
        while True:
            PSS = next((PSS for PSS in range(len(^TMP('PSS5506',$J,55.07))) if PSS == PSS(1)), None)
            if PSS is None:
                break
            
            f.write(f"^TMP($J,{LIST},{PSSPO},'DDRUG',{PSS(1)},.11)={'^TMP('PSS5506',$J,55.07,{PSS(1)},.11,'I')}")
            f.write(f"^TMP($J,{LIST},{PSSPO},'DDRUG',{PSS(1)},.12)={'^TMP('PSS5506',$J,55.07,{PSS(1)},.12,'I')}")
            f.write(f"^TMP($J,{LIST},{PSSPO},'DDRUG',{PSS(1)},.01)={'^TMP('PSS5506',$J,55.07,{PSS(1)},.01,'I')' if ^TMP('PSS5506',$J,55.07,{PSS(1)},.01,'E') != '' else ''}")
            f.write(f"^TMP($J,{LIST},{PSSPO},'DDRUG',{PSS(1)},.02)={'^TMP('PSS5506',$J,55.07,{PSS(1)},.02,'I')}")
            f.write(f"^TMP($J,{LIST},{PSSPO},'DDRUG',{PSS(1)},.03)={'^TMP('PSS5506',$J,55.07,{PSS(1)},.03,'I')' if ^TMP('PSS5506',$J,55.07,{PSS(1)},.03,'E') != '' else ''}")
            f.write(f"^TMP($J,{LIST},{PSSPO},'DDRUG',{PSS(1)},.04)={'^TMP('PSS5506',$J,55.07,{PSS(1)},.04,'I')}")
            f.write(f"^TMP($J,{LIST},{PSSPO},'DDRUG',{PSS(1)},.05)={'^TMP('PSS5506',$J,55.07,{PSS(1)},.05,'I')}")
            f.write(f"^TMP($J,{LIST},{PSSPO},'DDRUG',{PSS(1)},.06)={'^TMP('PSS5506',$J,55.07,{PSS(1)},.06,'I')}")
            f.write(f"^TMP($J,{LIST},{PSSPO},'DDRUG',{PSS(1)},.07)={'^TMP('PSS5506',$J,55.07,{PSS(1)},.07,'I')}")
            f.write(f"^TMP($J,{LIST},{PSSPO},'DDRUG',{PSS(1)},.08)={'^TMP('PSS5506',$J,55.07,{PSS(1)},.08,'I')}")
            f.write(f"^TMP($J,{LIST},{PSSPO},'DDRUG',{PSS(1)},.09)={'^TMP('PSS5506',$J,55.07,{PSS(1)},.09,'I')}")
            f.write(f"^TMP($J,{LIST},{PSSPO},'DDRUG',{PSS(1)},.1)={'^TMP('PSS5506',$J,55.07,{PSS(1)},.1,'I')}")
            CNT1 += 1

        f.write(f"^TMP($J,{LIST},'B',{PSSPO})=''")
        f.write(f"^TMP($J,{LIST},0)=^TMP($J,{LIST},0)+1")
        f.write(f"^TMP($J,{LIST},{PSSPO},'DDRUG',0)={-1^NO DATA FOUND if CNT1 == 0 else CNT1}")
        f.write(f"^TMP($J,{LIST},0)={-1^NO DATA FOUND if ^TMP($J,{LIST},0) == 0 else ^TMP($J,{LIST},0)}")

    def DT431():
        nonlocal PSDATE
        nonlocal PEDATE
        nonlocal PSSPO
        nonlocal PO
        nonlocal PSS56

        while True:
            PSDATE = next((PSDATE for PSDATE in range(len(^PS(55,DFN,5,'AUS'))) if PSDATE == PSDATE), None)
            if PSDATE is None:
                break

            PSS56 = 0
            while True:
                PSS56 = next((PSS56 for PSS56 in range(len(^PS(55,DFN,5,'AUS',PSDATE))) if PSS56 == PSS56), None)
                if PSS56 is None:
                    break

                PSSPO = PSS56
                PO = PSSPO
                f.write("G DIQ431")

        f.write(f"^TMP($J,{LIST},0)={-1^NO DATA FOUND if ^TMP($J,{LIST},0) == 0 else ^TMP($J,{LIST},0)}")
        CNT1 = None
        LIST = None
        DA = None
        DFN = None
        DIC = None
        DIQ = None
        DR = None
        IEN = None
        PEDATE = None
        PO = None
        PSDATE = None
        PSS = None
        PSS56 = None
        PSSPO = None
        PSSPO1 = None
        X = None

    # Function calls
    LOOP431()
    DT431()

    os.remove(tmp_file.name)

    return