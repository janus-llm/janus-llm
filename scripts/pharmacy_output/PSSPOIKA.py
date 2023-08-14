#PSSPOIKA ;BIR/RTR-Orderable Item reports ;09/01/98
#;;1.0;PHARMACY DATA MANAGEMENT;**15,38**;9/30/97
PSSITE = +$O(^PS(59.7,0))
if +$P($G(^PS(59.7,PSSITE,80)),"^",2) < 2:
    print("\nOrderable Item Auto-Create has not been completed yet!")
    PSSITE = None
    input("Press RETURN to continue")
else:
    PSSITE = None

option = input("Enter M to see all the IV Solutions, IV Additives, and Dispense Drugs that are matched to an Orderable Item. Enter N to see all IV Additives, IV Solutions, and Dispense Drugs that are not matched to an Orderable Item.")
if option == "M":
    PSREP = 1
elif option == "N":
    PSREP = 0

print("\n** WARNING **  THIS REPORT MAY BE VERY LONG  ** WARNING **")
KMES^PSSPOIM1()

print("\nThis report must be QUEUED to a printer!")
while True:
    device = input("Enter the device to queue the report: ")
    if device == "Q":
        break

ZTRTN = "MATCH^PSSPOIKA" if PSREP else "NOT^PSSPOIKA"
ZTDESC = "Matched Orderable Item Report" if PSREP else "Not matched Drug report"
try:
    ZTLOAD(ZTRTN, ZTDESC)
except:
    pass

AA = None
BB = None
CC = None
DOSE = None
DTOUT = None
DUOUT = None
EE = None
GFLAG = None
LIN = None
MM = None
NDNODE = None
NME = None
NN = None
PSPOI = None
PSREP = None
REA = None
Y = None
ZFG = None
ZFLAG = None
RR = None
SS = None
ZZ = None
PAGE = None
KK = None
LL = None
TT = None
WW = None
VV = None
PSDIS = None