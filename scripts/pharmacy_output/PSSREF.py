# BIR/BAB-Cross Reference Utility
# 09/02/97 8:49

# Entry point to create xref for CMOP Dispense field edit
def ACT():
    if not "^PSDRUG(DA,3)" in globals():
        return
    if not globals()["^PSDRUG(DA,3)"]:
        return
    if not "^PSDRUG(DA,4,0)" in globals():
        globals()["^PSDRUG(DA,4,0)"] = "^50.0214DA^^"
    if not globals()["^PSDRUG(DA,4,0)"]:
        globals()["^PSDRUG(DA,4,0)"] = "^50.0214DA^^"
    PSX = 0
    Z = 0
    while Z:
        if not "^PSDRUG(DA,4,Z)" in globals():
            break
        if not globals()["^PSDRUG(DA,4,Z)"]:
            break
        PSX = Z
        Z += 1
    PSX += 1
    globals()["%"] = None  # Placeholder for NOW^%DTC function
    globals()["DUZ"] = None  # Placeholder for DUZ variable
    globals()["^PSDRUG(DA,4,PSX,0)"] = f"%^E^{DUZ}^CMOP Dispense^{'YES' if globals()['^PSDRUG(DA,3)'] == 1 else 'NO'}"
    globals()["^PSDRUG(DA,4,0)"] = globals()["^PSDRUG(DA,4,0)"].replace("^", "", 3)
    globals()["^PSDRUG(DA,4,0)"] = globals()["^PSDRUG(DA,4,0)"].replace("^", "", 4)
    globals()["PSX"] = None
    globals()["Z"] = None
    globals()["%"] = None
    return

# Called by ^DD(52.1,.01,"DEL",550,0)- PREVENTS DELETING REFILL DATE
def DEL():
    if not "^PSX(DA)" in globals():
        return
    if not globals()["^PSX(DA)"]:
        return
    if not globals()["^PSX(DA)"] == "L" and (not globals()["^PSX(DA)"] == 3):
        print("You cannot delete a refill date for a fill that is", end="")
        if globals()["^PSX(DA)"] == 1:
            print(" released by", end="")
        elif globals()["^PSX(DA)"] == 0:
            print(" in transmission to", end="")
        else:
            print(" being retransmitted to", end="")
        print(" the CMOP", end="")
        print()
    return

# Sets the "AR" xref if CMOP status in 52 =1
# ^PSRX("AR",RELEASE D/T,INTERNAL ENTRY # RX in 52,fill #
def AR():
    if not "X" in globals():
        return
    if globals()["X"] == 1:
        if not "^PSRX(DA(1),4,DA,0)" in globals():
            return
        if not globals()["^PSRX(DA(1),4,DA,0)"]:
            return
        if not "^PSRX(DA(1),2)" in globals():
            return
        if not globals()["^PSRX(DA(1),2)"]:
            return
        if not "^PSRX(DA(1),2)" in globals():
            return
        if not globals()["^PSRX(DA(1),2)"]:
            return
        if not "^PSRX(DA(1),4,DA,0)" in globals():
            return
        if not globals()["^PSRX(DA(1),4,DA,0)"]:
            return
        if globals()["^PSRX(DA(1),4,DA,0)"].split("^")[3] == 0 and globals()["^PSRX(DA(1),2)"].split("^")[13]:
            globals()["^PSRX('AR',^PSRX(DA(1),2).split("^")[13],DA(1),^PSRX(DA(1),4,DA,0).split("^")[3])] = ""
        if globals()["^PSRX(DA(1),4,DA,0)"].split("^")[3] > 0 and globals()["^PSRX(DA(1),1,^PSRX(DA(1),4,DA,0).split("^")[3],0)"]:
            if globals()["^PSRX(DA(1),1,^PSRX(DA(1),4,DA,0).split("^")[3],0)"].split("^")[18]:
                globals()["^PSRX('AR',^PSRX(DA(1),1,^PSRX(DA(1),4,DA,0).split("^")[3],0).split("^")[18],DA(1),^PSRX(DA(1),4,DA,0).split("^")[3])] = ""
    return

# Transmission D/T xref
# ^PSRX("AS",TRANS D/T,INTERNAL ENTRY # RX in 52, fill #
def AS():
    if not "X" in globals():
        return
    if globals()["X"] == 0:
        if not "^PSX(550.2,^PSRX(DA(1),4,DA,0).split("^")[0],0)" in globals():
            return
        if not globals()["^PSX(550.2,^PSRX(DA(1),4,DA,0).split("^")[0],0)"]:
            return
        globals()["^PSRX('AS',^PSX(550.2,^PSRX(DA(1),4,DA,0).split("^")[0],0).split("^")[6],DA(1),^PSRX(DA(1),4,DA,0).split("^")[3])] = ""
    return

def ASKILL():
    if not "^PSX(550.2,^PSRX(DA(1),4,DA,0).split("^")[0],0)" in globals():
        return
    if not globals()["^PSX(550.2,^PSRX(DA(1),4,DA,0).split("^")[0],0)"]:
        return
    globals()["^PSRX('AS',^PSX(550.2,^PSRX(DA(1),4,DA,0).split("^")[0],0).split("^")[6],DA(1),^PSRX(DA(1),4,DA,0).split("^")[3])] = ""
    return

# Called by ^DD(50,14.5,"DEL",0) to prevent deleting CMOP disp units.
def DISPUNIT():
    if "^PSDRUG('AQ',DA)" in globals():
        return
    if not globals()["^PSDRUG('AQ',DA)"]:
        print("The Dispense Unit of a CMOP drug cannot be deleted!", end="")
        print()
    return