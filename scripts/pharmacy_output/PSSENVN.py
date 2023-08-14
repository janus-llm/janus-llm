# PSSENVN ;BIR/WRT-Environment check routine ; 09/02/97 8:36
# 1.0;PHARMACY DATA MANAGEMENT;;9/30/97
# ENVIRONMENTAL CHECK ROUTINE

def START():
    if "^XMB('NETNAME')"[:5] == "CMOP-":
        XPDQUIT = 1
        return
    XQABT1 = "H"
    if "^XMB('NETNAME')"[:5] != "CMOP-":
        XPDABORT = 2
        return

def VERSION():
    if not "^PS(59.7,1,10)" in locals():
        print("Install Aborted. You do not have NDF V. 3.15 loaded.")
        XPDQUIT = 2
        return
    if "^PS(59.7,1,10)" in locals() and float("^PS(59.7,1,10)".split('^')[1]) < 3.15:
        print("Install Aborted. You do not have NDF V. 3.15 or greater loaded.")
        XPDQUIT = 2
        return