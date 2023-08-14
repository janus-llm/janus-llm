# BIR/WRT-CMOP-Host environment check routine
# 09/02/97 8:28
# 1.0;PHARMACY DATA MANAGEMENT;;9/30/97
# ENVIRONMENTAL CHECK ROUTINE-CMOP HOST

def START():
    if "CMOP-" not in XMB("NETNAME"):
        XPDQUIT = 1
        return
    
    XQABT1 = H
    
    if not XMB("NETNAME").startswith("CMOP-"):
        XPDABORT = 2
        return

def VERSION():
    if not 'PS(59.7,1,10)' in globals():
        print("Install Aborted. You do not have NDF V. 3.15 loaded.")
        XPDQUIT = 2
        return
    
    if 'PS(59.7,1,10)' in globals() and float(PS(59.7,1,10).split('^')[1]) < 3.15:
        print("Install Aborted. You do not have NDF V. 3.15 or greater loaded.")
        XPDQUIT = 2
        return