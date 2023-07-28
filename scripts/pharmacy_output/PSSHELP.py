# PSSHELP ;BIR/SAB-PDM UTILITY ROUTINE ; 09/02/97 8:37
# 1.0;PHARMACY DATA MANAGEMENT;**125**;9/30/97;Build 2

def ADD():
    print()
    DIC["A"] = "Select Drug Interaction: "
    DIC["0"] = "AEMQL"
    DIC = DIE = "^PS(56,"
    DIC["S"] = "I '$P(^(0),""^"",5)"
    DLAYGO = 56
    DIC_result = DIC()
    
    if DIC_result != "^":
        if DIC_result >= 0:
            DA = DIC_result
            DR = "[PSS INTERACT]"
            # Lock the global node
            if lock_node := $S(DILOCKTM > 0, DILOCKTM, 3):
                L_node = lock_node
                print()  # Placeholder for processing code
                # Unlock the global node
                L_node = None
            else:
                print("\nAlready being edited.")
            
            if "DA" in locals():
                # Unlock the global node
                L_node = None
                del DA
            
            ADD()

    del X, DIC, DIE, DA

def CRI():
    print()
    DIC["A"] = "Select Drug Interaction: "
    DIC["0"] = "AEQM"
    DIC = DIE = "^PS(56,"
    DIC["S"] = "I $P(^(0),""^"",4)=2"
    DIC_result = DIC()
    
    if DIC_result != "^":
        if DIC_result >= 0:
            DA = DIC_result
            DR = 3
            # Lock the global node
            if lock_node := $S(DILOCKTM > 0, DILOCKTM, 3):
                L_node = lock_node
                print()  # Placeholder for processing code
                # Unlock the global node
                L_node = None
            else:
                print("\nAlready being edited.")
            
            if "DA" in locals():
                # Unlock the global node
                L_node = None
                del DA
            
            CRI()
    
    QU()
    return

def QU():
    del X, DIC, DIE, DA
    return

ADD()
CRI()
QU()