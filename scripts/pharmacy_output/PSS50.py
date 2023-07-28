def DATA(PSSIEN, PSSFT, PSSFL, PSSPK, PSSRTOI, LIST):
    # Returns Drug File (#50) Data
    PSS50DAT.DATA(PSSIEN, PSSFT, PSSFL, PSSPK, PSSRTOI, LIST)

def CMOP(PSSIEN, PSSFT, PSSFL, PSSPK, PSSRTOI, LIST):
    # Returns CMOP information from Drug File (#50)
    PSS50CMP.CMOP(PSSIEN, PSSFT, PSSFL, PSSPK, PSSRTOI, LIST)

def DRG(PSSIEN, PSSFT, PSSFL, PSSPK, PSSRTOI, LIST):
    # Returns information from Drug File (#50) used by Inpatient Meds/Unit Dose
    PSS50DAT.DRG(PSSIEN, PSSFT, PSSFL, PSSPK, PSSRTOI, LIST)

def ATC(PSSIEN, PSSFT, PSSFL, PSSPK, LIST):
    # Returns ATC fields from the Drug File (#50)
    PSSRTOI = None
    PSS50ATC.ATC(PSSIEN, PSSFT, PSSFL, PSSPK, LIST)

def INV(PSSIEN, PSSFT, PSSFL, PSSPK, PSSRTOI, LIST):
    # Returns inventory fields from the Drug File (#50)
    PSS50B.INV(PSSIEN, PSSFT, PSSFL, PSSPK, PSSRTOI, LIST)

def NDF(PSSIEN, PSSFT, PSSFL, PSSPK, PSSRTOI, LIST):
    # Returns NDF fields from the Drug File (#50)
    PSS50B.NDF(PSSIEN, PSSFT, PSSFL, PSSPK, PSSRTOI, LIST)

def LAB(PSSIEN, PSSFT, PSSFL, PSSPK, PSSRTOI, LIST):
    # Returns Lab information from the Drug File (#50)
    PSS50LAB.LAB(PSSIEN, PSSFT, PSSFL, PSSPK, PSSRTOI, LIST)

def CLOZ(PSSIEN, PSSFT, PSSFL, PSSPK, PSSRTOI, LIST):
    # Returns Clozapine information from the Drug File (#50)
    PSS50B2.CLOZ(PSSIEN, PSSFT, PSSFL, PSSPK, PSSRTOI, LIST)

def ARWS(PSSIEN, PSSFT, LIST):
    # Returns fields utilized by the Automatic Replenishment/Ward Stock extract in PBM
    PSSFL = None
    PSSPK = None
    PSSRTOI = None
    PSS50WS.ARWS(PSSIEN, PSSFT, LIST)

def DOSE(PSSIEN, PSSFT, PSSFL, PSSPK, PSSRTOI, LIST):
    # Returns Dosing fields from the Drug File (#50)
    PSS50B.DOSE(PSSIEN, PSSFT, PSSFL, PSSPK, PSSRTOI, LIST)

def WS(PSSIEN, PSSFT, PSSFL, PSSPK, PSSRTOI, LIST):
    # Returns Ward Stock fields from the Drug File (#50)
    PSS50C.WS(PSSIEN, PSSFT, PSSFL, PSSPK, PSSRTOI, LIST)

def MRTN(PSSIEN, PSSFT, PSSFL, PSSPK, PSSRTOI, LIST):
    # Returns Lab Test Monitor fields from the Drug File (#50)
    PSS50C.MRTN(PSSIEN, PSSFT, PSSFL, PSSPK, PSSRTOI, LIST)

def ZERO(PSSIEN, PSSFT, PSSFL, PSSPK, PSSRTOI, LIST):
    # Returns Zero node information from the Drug File (#50)
    PSS50C.ZERO(PSSIEN, PSSFT, PSSFL, PSSPK, PSSRTOI, LIST)

def NOCMOP(PSSIEN, PSSFL):
    # Returns drugs from the Drug file (#50) with the CMOP Dispense Field set to Null or No
    return PSS50C.NOCMOP(PSSIEN, PSSFL if PSSFL else "")

def MSG(LIST):
    # Returns entries and data from the Drug File (#50) with data in the Quantity Dispense Message field
    PSS50C.MSG(LIST)

def IEN(LIST):
    # Returns Active Outpatient Drugs with a VA Product Name entry
    PSS50C.IEN(LIST)

def B(PSSFT, PSSFL, PSSPK, PSSRTOI, LIST):
    # Returns Drug information based on B cross reference
    PSS50D.B(PSSFT, PSSFL, PSSPK, PSSRTOI, LIST)

def VAC(PSSVAL, PSSFL, PSSPK, LIST):
    # Returns Generic Name based on National Drug Class
    PSSRTOI = None
    PSS50D.VAC(PSSVAL, PSSFL, PSSPK, LIST)

def NDC(PSSVAL, PSSFL, PSSPK, LIST):
    # Returns Generic Name or IEN for drugs when passed an NDC
    PSS50D.NDC(PSSVAL, PSSFL, PSSPK, LIST)

def ASP(PSSVAL, PSSFL, PSSPK, LIST):
    # Returns drug entries when passed an Orderable Item
    PSSRTOI = None
    PSS50D.ASP(PSSVAL, PSSFL, PSSPK, LIST)

def AND(PSSVAL, PSSFL, PSSPK, LIST):
    # Returns drug entries when passed a National Drug File entry
    PSSRTOI = None
    PSS50D.AND(PSSVAL, PSSFL, PSSPK, LIST)

def AP(PSSVAL, PSSFL, PSSPK, LIST):
    # Returns drug entries when passed a Primary Drug entry
    PSSRTOI = None
    PSS50D.AP(PSSVAL, PSSFL, PSSPK, LIST)

def DSPUNT(PSSIEN, PSSIEN2, LIST):
    # Returns Dispense Units Per Order Unit when passed in the Drug and Synonym
    PSS50C1.DSPUNT(PSSIEN, PSSIEN2, LIST)

def SKB(PSSIEN, PSSFL):
    # Sets and kills B cross reference on the Name field when the Drug is passed
    if not PSSIEN:
        return 0
    if not PSSFL:
        return 0
    if PSSFL not in ["SK"]:
        return 0
    return PSS50E.SKB(PSSIEN, PSSFL)

def AOC(PSSVAL, PSSFL, PSSPK, LIST):
    # Returns generic name or IEN for drugs when passed the VA CLASSIFICATION
    PSS50E.AOC(PSSVAL, PSSFL, PSSPK, LIST)

def C(PSSVAL, PSSFL, PSSPK, LIST):
    # Returns information from the Synonym multiple of the Drug File (#50)
    PSS50E.C(PSSVAL, PSSFL, PSSPK, LIST)

def AQ(PSSIEN):
    # Checks for existence of "AQ" x-ref for PSSIEN passed
    if not PSSIEN:
        return 0
    return int(bool(PSS50E.AQ(PSSIEN)))

def SKAQ(PSSIEN, PSSFL):
    # Sets and kills "AQ" x-ref on the CMOP Dispense field for PSSIEN passed
    if not PSSIEN:
        return 0
    if not PSSFL:
        return 0
    if PSSFL not in ["SK"]:
        return 0
    return PSS50E.SKAQ(PSSIEN, PSSFL)

def SKAQ1(PSSIEN):
    # Sets and kills "AQ1" x-ref on the CMOP ID field for PSSIEN passed
    if not PSSIEN:
        return 0
    return PSS50E.SKAQ1(PSSIEN)

def AQ1(PSSVAL, PSSFL, PSSPK, LIST):
    # Returns a list of drugs associated with the CMOP ID passed
    PSS50B1.AQ1(PSSVAL, PSSFL, PSSPK, LIST)

def A526(PSSIEN, LIST):
    # Returns a list of additives associated with the Drug passed
    PSS50E.A526(PSSIEN, LIST)

def A527(PSSIEN, LIST):
    # Returns a list of solutions associated with the drug passed
    PSS50E.A527(PSSIEN, LIST)

def AIU(PSSFT, PSSPK, PSSFL, LIST):
    # Returns a list of drugs based on Application Packages' Use and Inactive Date
    PSS50B1.AIU(PSSFT, PSSPK, PSSFL, LIST)

def IU(PSSFL, LIST):
    # Returns a list of drugs based on Application Packages' Use not containing "O", "U", "I", or "N"
    PSS50B1.IU(PSSFL, LIST)

def SKAIU(PSSIEN, PSSFL):
    # Sets and Kills the "AIU" x-ref on the APPLICATION PACKAGES' USE field for PSSIEN and PSSPK passed
    if not PSSIEN:
        return 0
    if not PSSFL:
        return 0
    if PSSFL not in ["SK"]:
        return 0
    return PSS50E.SKAIU(PSSIEN, PSSFL)

def SKIU(PSSIEN):
    # Sets and Kills the "IU" x-ref on the APPLICATION PACKAGES' USE field for PSSIEN and PSSPK passed
    if not PSSIEN:
        return 0
    return PSS50E.SKIU(PSSIEN)

def AB(PSSVAL, PSSFL, PSSPK, LIST):
    # Returns a list of drugs associated with an IFCAP Item Number
    PSS50C.AB(PSSVAL, PSSFL, PSSPK, LIST)

def AVSN(PSSVAL, PSSFL, PSSPK, LIST):
    # Returns synonym multiple for Synonym value passed
    PSS50B1.AVSN(PSSVAL, PSSFL, PSSPK, LIST)

def FRMALT(PSSIEN, PSSFT, PSSFL, PSSPK, LIST):
    # Returns the Formulary Altenative for the drug value passed
    PSSRTOI = None
    PSS50B2.FRMALT(PSSIEN, PSSFT, PSSFL, PSSPK, PSSRTOI, LIST)

def LABEL(PSSIEN, LIST):
    # Returns Information for the scanner for the drug IEN passed
    PSS50A1.LABEL(PSSIEN, LIST)

def SORT(PSSIEN, LIST):
    # Returns a list of drugs for the IEN passed
    PSS50A1.SORT(PSSIEN, LIST)

def OLDNM(PSSIEN, PSSFT, PSSFL, PSSPK, LIST):
    # Returns OLD NAME multiple from the Drug File (#50)
    PSSRTOI = None
    PSS50F.OLDNM(PSSIEN, PSSFT, PSSFL, PSSPK, PSSRTOI, LIST)

def ADDOLDNM(PSSIEN, PSSONM, PSSDT):
    # Adds an entry to the OLD NAME Multiple of the Drug file (#50)
    return PSS50F.ADDOLDNM(PSSIEN, PSSONM, PSSDT)

def LIST(PSSFT, PSSFL, PSSD, PSSPK, LIST):
    # Returns a list containing GENERIC NAME field (#.01) and PHARMCY ORDERABLE ITEM field (#2.1)
    PSSRTOI = None
    PSS50F1.LIST(PSSFT, PSSFL, PSSD, PSSPK, PSSRTOI, LIST)

def EDTIFCAP(PSSIEN, PSSVAL):
    # Adds an entry to the IFCAP ITEM NUMBER multiple of the DRUG file (#50)
    return PSS50F.EDTIFCAP(PSSIEN, PSSVAL)

def LOOKUP(PSSFT, PSSFL, PSSPK, PSSRTOI, PSSIFCAP, PSSCMOP, PSSD, LIST):
    PSS50F1.LOOKUP(PSSFT, PSSFL, PSSPK, PSSRTOI, PSSIFCAP, PSSCMOP, PSSD, LIST)

def CSYN(PSSIEN, PSSVAL, LIST):
    # returns synonym information from the synonym multiple of the Drug file (#50)
    PSS50C1.CSYN(PSSIEN, PSSVAL, LIST)

def PSSBILSD(PSSIEN):
    # returns eBillable & Sensitive Diagnosis Drug fields from the Drug File(#50)
    #   Input:PSSIEN -  File #50 Drug IEN
    #  Output:Drug File billable and sensitive diagnosis drug fields
    #         EPHBILL -  EPHARMACY BILLABLE field #84
    #         EPHTRI -   EPHARMACY BILLABLE (TRICARE) field #85
    #         EPHCHAMP - EPHARMACY BILLABLE (CHAMPVA) field #86
    #         EPHSENS -  EPHARMACY SENSITIVE DIAGNOSIS DRUG field #87
    #
    #         EPHBILSD=EPHBILL^EPHTRI^EPHCHAMP^EPHSENS
    #
    EPHNODE = PSS50E.PSSBILSD(PSSIEN)
    EPHBILL = EPHNODE[0]
    EPHTRI = EPHNODE[1]
    EPHCHAMP = EPHNODE[2]
    EPHSENS = EPHNODE[3]
    EPHBILSD = EPHBILL + "_" + EPHTRI + "_" + EPHCHAMP + "_" + EPHSENS
    return EPHBILSD