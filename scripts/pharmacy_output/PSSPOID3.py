# PSSPOID3 ;BIR/RTR/WRT-Edit Orderable Item from matching option ;02/04/00
# ;;1.0;PHARMACY DATA MANAGEMENT;**38,47**;9/30/97
import datetime

# Variable Definitions
DA = 0
PSBEFORE = 0
PSAFTER = 0
PSINORDE = ""
PSSDTENT = 0
PSCREATE = 0
PSSDACTI = []
PSSSACTI = []
PSSAACTI = []
PSSDACT = []
PSSSACT = []
PSSAACT = []

PSSDTENT = 0
print("\n")
MFLG = 0
PSBEFORE = int(^PS(50.7,PSSOOIEN,0).split("^")[4])
PSAFTER = 0
PSINORDE = ""
print("\n")
print("This Orderable Item is ", "Non-Formulary." if ^PS(50.7,PSSOOIEN,0).split("^")[12] else "Formulary.")
DIE = "^PS(50.7,"
DA = PSSOOIEN
DR = 6
PSCREATE = 1
^DIE
DIE = ""
PSCREATE = 0
if DTOUT or Y:
    quit()
DIR = {}
DIR[0] = "DO"
DIR["A"] = "INACTIVE DATE"
^DIR
DIR = ""
if Y.contains("^") or DTOUT or DUOUT:
    quit()
if PSBEFORE and not Y:
    print("Inactive Date deleted!")
PSSDTENT = Y
if Y:
    print(Y)
PSSOTH = 1 if ^PS(59.7,1,40.2).split("^") else 0
DIE = "^PS(50.7,"
DA = PSSOOIEN
DR = ".05;.06;.07;.08;7;S:'$G(PSSOTH) Y=""@1"";7.1;@1"
PSCREATE = 1
^DIE
DIE = ""
PSCREATE = 0
PSSOTH = ""
^PS(50.7,PSSOOIEN,0).split("^")[4] = PSSDTENT
PSAFTER = PSSDTENT
if PSBEFORE and not ^PS(50.7,PSSOOIEN,0).split("^")[4]:
    PSINORDE = "D"
if ^PS(50.7,PSSOOIEN,0).split("^")[4]:
    PSINORDE = "I"
if PSINORDE:
    CHECK^PSSPOID2(PSSOOIEN)
    if PSINORDE == "D":
        if PSSDACTI or PSSSACTI or PSSAACTI:
            print("\n")
            print("There are inactive ", "drugs, " if PSSDACTI else "", "additives, " if PSSAACTI else "", "solutions," if PSSSACTI else "", "\n", "matched to this Pharmacy Orderable Item.")
    else:
        if PSSDACT or PSSSACT or PSSAACT:
            print("\n")
            print("There are active ", "drugs, " if PSSDACT else "", "additives, " if PSSAACT else "", "solutions," if PSSSACT else "", "\n", "matched to this Pharmacy Orderable Item.")
if PSINORDE == "D" and (PSSDACTI or PSSSACTI or PSSAACTI):
    REST^PSSPOIDT(PSSOOIEN)
if PSINORDE == "I" and (PSSDACT or PSSSACT or PSSAACT):
    REST^PSSPOIDT(PSSOOIEN)
DIK = "^PS(50.7,"
DA = PSSOOIEN
DIK(1) = ".04"
^DIK
DIK = ""
PSBEFORE = 0
PSAFTER = 0
PSINORDE = ""
PSSDTENT = 0
PSSDACT = []
PSSDACTI = []
PSSSACT = []
PSSSACTI = []
PSSAACT = []
PSSAACTI = []