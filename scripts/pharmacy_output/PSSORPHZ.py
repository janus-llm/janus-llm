def PSSORPHZ():
    # BIR/RTR-Dosage by Dispense Units for report ;03/24/00
    # 1.0;PHARMACY DATA MANAGEMENT;**40**;9/30/97
    # Reference to ^PS(50.607 supported by DBIA 2221
    
    DLOOP = PD
    if not DLOOP:
        return
    # SET PSSX(1)=-1^DDRUG IS INACTIVE OR NOT APP USE ANYMORE?
    if (
        (PD := "^PSDRUG(DLOOP,\"I\")") and
        (PD := "^PSDRUG(DLOOP,\"I\")") and
        (PD := "^PSDRUG(DLOOP,2)") and
        (PD := "^PS(50.607,+$G(PSSUNITZ),0)") and
        (PD := "^PS(50.607,+$P($G(^PSDRUG(DLOOP,\"DOS\")),\"^\",2),0)") and
        (PD := PSSUPD) and
        (PD := "^PS(50.606,PSSDSE,\"NOUN\",PSNN,0)") and
        (PD := "^PS(50.607,+$P($G(^PSDRUG(DLOOP,\"DOS\")),\"^\",2),0)") and
        (PD := "^PS(50.606,+$G(PSSDSE),0)") and
        (PD := "^PSDRUG(DLOOP,0)") and
        (PD := "^PSDRUG(PSIEN,0)") and
        (PD := "^PSDRUG(PSIEN,660)") and
        (PD := "^PSDRUG(PSIEN,0)") and
        (PD := "^PSDRUG(PSIEN,660)") and
        (PD := "^PSDRUG(PSIEN,\"DOS\")") and
        (PD := "^PS(50.607,+$G(PSSUNITZ),0)") and
        (PD := "^PS(50.606,PSSDSE,0)") and
        (PD := "^PS(50.606,+$G(PSSDSE),0)")
    ):
        PSSX = {}
        PSSX[1] = (
            f"{PSSDOSE}^{PSSUNITZ if TYPE == 'O' else PSSUNTS}^{PSSUDOS}^{DLOOP}^{PSSTRN}^"
            f"{PSSNP if PSSNP else PSNNN}^{PD}^{PSSVERB}^{PSSPREP}"
        )
        PSSA = 1
        PSIEN, DLOOP = int(PSSX[PSSA].split("^")[3]), int(PSSX[PSSA].split("^")[3])
        PD = TYPE
        PSSX["DD"][PSIEN] = (
            f"{PD}^{PD}^{PD}^{PD}^{PD}^{PSSUNITX}^{PSSMAX}"
        )
        PD = PSIEN
        PD = PSSREQS
        PSSX["DD"][PSIEN] = (
            f"{PSSX['DD'][PSIEN]}^{PSSREQS}^{PSNNN}^{PSSVERB}"
        )
        return PSSX

    def SET():
        PSSX = {}
        PSSX[1] = (
            f"^{PSSUNITZ if TYPE == 'O' else PSSUNTS}^^{DLOOP}^{PSSTRN}^"
            f"{PSSNP if PSSNP else PSNNN}^{PD}^{PSSVERB}^{PSSPREP}"
        )
        PSIEN, DLOOP = int(PSSX[1].split("^")[3]), int(PSSX[1].split("^")[3])
        PD = TYPE
        PSSX["DD"][PSIEN] = (
            f"{PD}^{PD}^{PD}^{PD}^{PD}^{PSSUNITX}^{PSSMAX}"
        )
        PD = PSIEN
        PD = PSSREQS
        PSSX["DD"][PSIEN] = (
            f"{PSSX['DD'][PSIEN]}^{PSSREQS}^{PSNNN}^{PSSVERB}"
        )
    
    SET()
    PSSORPH()