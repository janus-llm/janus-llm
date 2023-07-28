def PSS208P():
    # ALB/MHA - Price per dispense unit - post install fix ;05/24/2017
    # 1.0;PHARMACY DATA MANAGEMENT;**208**;9/30/97;Build 14
    return

def EN():
    print("Starting post-install for PSS*1*208 ... ")
    DRG()
    print("Finished with post-install for PSS*1*208.")

def DRG():
    NS = "PSS208"
    DRG = 0
    data = {}
    data[NS] = []
    data[NS].append("The Price Per Dispense Unit (PPDU) field (#16) and the Price Per Order Unit")
    data[NS].append("(PPOU) field (#13) in the Drug file (#50) have been updated in the following")
    data[NS].append("entries:")
    data[NS].append("")
    data[NS].append("Generic Name")
    data[NS].append("NDC            Old PPDU   New PPDU")
    data[NS].append("               PPOU       PPOU")
    data[NS].append("============")
    CT = 8

    while DRG:
        NDC = ""
        PPDU = 0
        PPOU = 0
        # Your code for retrieving NDC, PPDU, and PPOU goes here

        if NDC:
            I = 0
            QT = 0
            SYN = ""
            SNDC = ""
            SPPDU = 0
            SINT = ""

            while I and not QT:
                SYN = ""
                SNDC = ""
                SPPDU = 0
                SINT = ""
                # Your code for retrieving SYN, SNDC, SPPDU, and SINT goes here

                if SINT and "D" in SINT and SPPDU:
                    if SNDC and SNDC == NDC and SPPDU > 221 and SPPDU != PPDU:
                        FIXPR(SYN, SNDC, SPPDU, DRG)
                        QT = 1

        DRG += 1

    GMAIL(CT, data)
    return

def FIXPR(SYN, SNDC, SPPDU, DRG):
    SOU = SYN[4]
    SPPOU = SYN[5]
    SDUOU = SYN[6]
    # Your code for updating the fields in the DRUG file goes here

    CT += 1
    data[NS].append(f"{DRG[0][:35]}({DRG[1]})")
    data[NS][CT] += " " * (44 - len(data[NS][CT])) + NDC
    data[NS][CT] += " " * (59 - len(data[NS][CT])) + f"{PPDU:8.2f}"
    data[NS][CT] += " " * (70 - len(data[NS][CT])) + f"{SPPDU:8.2f}"
    CT += 1
    data[NS][CT] += " " * (59 - len(data[NS][CT])) + f"{PPOU:8.2f}"
    data[NS][CT] += " " * (70 - len(data[NS][CT])) + f"{SPPOU:8.2f}"
    return

def GMAIL(CT, data):
    XMSUB = "PSS*1*208 Post-Install Drug Price Update Report"
    XMDUZ = "PHARMACY DATA MANAGEMENT PACKAGE"
    XMY = [DUZ]

    if "PSNMGR" in XUSEC:
        for PSSDUZ in XUSEC["PSNMGR"]:
            XMY.append(PSSDUZ)

    if "PSA ORDERS" in XUSEC:
        for PSSDUZ in XUSEC["PSA ORDERS"]:
            XMY.append(PSSDUZ)

    if "PSAMGR" in XUSEC:
        for PSSDUZ in XUSEC["PSDMGR"]:
            XMY.append(PSSDUZ)

    if CT == 8:
        data[NS][7] = "No discrepancy found, nothing to update..."

    XMTEXT = data[NS]
    return