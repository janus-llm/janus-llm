# BIR/WRT-Option Delete environment check routine
# 09/09/97 15:15
# 1.0;PHARMACY DATA MANAGEMENT;;9/30/97

# ENVIRONMENTAL CHECK ROUTINE-OPTION DELETE
def START():
    if not ('^PS(59.7,1,49.99)' in globals() or '^PS(59.7,1,49.99)' in locals()):
        XPDQUIT = 1
        return
    if ('^PS(59.7,1,49.99)' in globals() or '^PS(59.7,1,49.99)' in locals()) and float(^PS(59.7,1,49.99).split("^")[1]) < 7.0:
        XPDQUIT = 1
        return