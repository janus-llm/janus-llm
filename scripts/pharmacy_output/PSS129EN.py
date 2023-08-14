#BIR/RTR-ENVIRONMENT CHECK ROUTINE FOR PSS*1*129 ;05/14/08
#1.0;PHARMACY DATA MANAGEMENT;**129**;9/30/97;Build 67

if not XPDENV:
    exit()

def EN():
    PSSVJMES = ["Upon completion of the Post Install, a mail message will be sent",
                 "to the patch installer, and at least one pharmacy user. Please",
                 "enter one or more Pharmacy users (e.g., Pharmacy ADPAC or designee)",
                 "who should receive this message."]
    for message in PSSVJMES:
        print(message)
    
    PSSVJAR = {DUZ: ''}
    PSSVJFLG = 0

    while True:
        print(" ")
        pharmacy_user = input("Enter Pharmacy User: ")
        if not pharmacy_user:
            break
        if int(pharmacy_user) in PSSVJAR:
            print("Already selected.")
            continue
        PSSVJFLG = 1
        PSSVJAR[int(pharmacy_user)] = ''

    if not PSSVJFLG:
        print("At least one pharmacy user must be selected. Install aborted.")
        XPDABORT = 2
        return

    print(" ")
    continue_install = input("Continue with install (Y/N)? ")
    if continue_install.lower() != 'y':
        XPDABORT = 2
        return

    print(" ")
    for pharmacy_user in PSSVJAR:
        XPDGREF["PSSVJARX"][pharmacy_user] = ""