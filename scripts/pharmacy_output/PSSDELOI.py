# BIR/RTR-Delete Orderable Item File and all pointers; 09/02/97 8:34
# 1.0;PHARMACY DATA MANAGEMENT;;9/30/97

PSSITE = +$O(^PS(59.7,0))
if +$P($G(^PS(59.7,PSSITE,80)),"^",2) > 1:
    print("\nOrderable Item Auto-create has already run to completion!\n")
    del PSSITE
    return

input_ok = input("\nAre you sure it's OK to delete the Orderable Item File? (Y/N) ")
if input_ok != 'Y':
    print("\nNo action taken!")
    return

print("\nTHIS WILL JUST TAKE A FEW MINUTES, PLEASE WAIT\n")

PSCREATE = 1

for ZZ in range(0, len(^PS(50.7))):
    DA = ZZ
    DIK = "^PS(50.7,"
    del ^PS(50.7,DA)

for XX in range(0, len(^PSDRUG)):
    RR = $P(^PSDRUG(XX,2),"^")
    if RR:
        DA = XX
        DIE = "^PSDRUG("
        DR = "2.1////" + "@"
        ^DIE(DA,DR)

for YY in range(0, len(^PS(52.6))):
    RR = $P(^PS(52.6,YY,0),"^",11)
    if RR:
        DA = YY
        DIE = "^PS(52.6,"
        DR = "15////" + "@"
        ^DIE(DA,DR)

for BB in range(0, len(^PS(52.7))):
    RR = $P(^PS(52.7,BB,0),"^",11)
    if RR:
        DA = BB
        DIE = "^PS(52.7,"
        DR = "9////" + "@"
        ^DIE(DA,DR)

$P(^PS(59.7,PSSITE,80),"^",2) = 0

print("\nDONE!\n")

del DIE, DA, YY, BB, XX, ZZ, PSSITE, PSCREATE